## \file src/webdriver/ai_browser/use_llm.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для запуска задач с использованием LLM через LangChain и стандартных агентов.
==================================================================================
Использует инструменты API поиска и асинхронные инструменты управления
браузером/контентом из модуля 'controllers'.

Предоставляет функциональность для:
- Конфигурирования моделей (Gemini, OpenAI).
- Установки API ключей для LLM и поисковых сервисов.
- Асинхронной инициализации контроллеров (браузер, извлечение данных, формы и т.д.).
- Создания инструментов LangChain для контроллеров и активных поисковиков.
- Запуска задачи с использованием LLM и доступных инструментов.
- Выполнения задачи до конечного результата (`run_task`) с логикой повтора при ошибках квоты.
- Стриминга выполнения задачи (`stream_task`).

Зависимости:
    - langchain-openai, langchain-google-genai, langchain-core, langchainhub, langchain
    - langchain-community (для SerpAPIWrapper, DuckDuckGoSearchRun, TavilySearchResults)
    - google-search-results (для SerpAPIWrapper)
    - duckduckgo-search (для DuckDuckGoSearchRun)
    - tavily-python (для TavilySearchResults)
    - google-api-core (для обработки ошибок квоты Google API)
    - python-dotenv
    - playwright, beautifulsoup4, lxml
    - src.gs, src.logger, src.utils, header
    - src.webdriver.llm_driver.controllers

```rst
.. module:: src.webdriver.ai_browser.use_llm
```
"""

# Стандартные библиотеки
import asyncio
import json # Для парсинга результата в main
import logging # Стандартный logging
import os
from pathlib import Path
from types import SimpleNamespace
from typing import (Any, AsyncIterator, Callable, Coroutine, Dict, List, # pylint: disable=unused-import
                    Optional, Tuple, Type, TypeAlias, Union)

# LangChain компоненты
from langchain import hub
from langchain.agents import AgentExecutor, Tool, create_react_agent
# --- Инструменты поиска ---
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities import SerpAPIWrapper
# --- Ядро LangChain ---
from langchain_core.exceptions import LangChainException
from langchain_core.language_models.chat_models import BaseChatModel
# --- Модели LangChain ---
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
# --- Исключения Google API ---
from google.api_core import exceptions as google_api_exceptions


from google.api_core import exceptions as google_api_exceptions
from duckduckgo_search.exceptions import DuckDuckGoSearchException 
from langchain_core.exceptions import LangChainException

# --- Внутренние модули ---
import header

from header import __root__
from src import gs
from src.logger import logger
from src.utils.jjson import j_loads_ns 
from src.utils.printer import pprint as print

# --- ИМПОРТ АСИНХРОННЫХ КОНТРОЛЛЕРОВ ---
# Путь к модулю с контроллерами
CONTROLLERS_MODULE_PATH: str = 'src.webdriver.llm_driver.controllers'
# Флаг доступности основного BrowserController
BROWSER_CONTROLLER_AVAILABLE: bool = False 
# Флаг доступности BeautifulSoup, необходимый для некоторых контроллеров
BS4_AVAILABLE: bool = False
try:
    # pylint: disable=import-error
    # Попытка импорта контроллеров
    from src.webdriver.llm_driver.controllers import (
        BS4_AVAILABLE, BrowserController, DataExtractionController,
        DownloadController, FormController, JavaScriptExecutionController,
        ScreenshotController, StateManager
    )
    # Установка флага успешного импорта
    BROWSER_CONTROLLER_AVAILABLE = True
    logger.info(f'Асинхронные контроллеры успешно импортированы из {CONTROLLERS_MODULE_PATH}.')
except ImportError as import_ex:
    # Логирование ошибки в случае неудачного импорта
    logger.error(f'КРИТИЧЕСКАЯ ОШИБКА: Не удалось импортировать контроллеры из {CONTROLLERS_MODULE_PATH}.', import_ex, exc_info=True)
    class BrowserController: # type: ignore
        """ Заглушка BrowserController на случай ошибки импорта. """
        _is_started: bool = False
        def __init__(self, *args: Any, **kwargs: Any) -> None: logger.debug('Инициализирован ЗАГЛУШКА BrowserController.', exc_info=False)
        async def start(self) -> bool: logger.error('Заглушка: start не реализован.'); return False
        async def navigate(self, u: str) -> str: return f'Ошибка: Заглушка BrowserController, navigate({u}).'
        async def scrape_text(self, s: Optional[str]=None) -> str: return 'Ошибка: Заглушка BrowserController, scrape_text.'
        async def scrape_html(self, s: Optional[str]=None) -> str: return 'Ошибка: Заглушка BrowserController, scrape_html.'
        async def click_element(self, s: str) -> str: return f'Ошибка: Заглушка BrowserController, click_element({s}).'
        def get_current_url(self) -> str: return 'Ошибка: Заглушка BrowserController.'
        async def close(self) -> None: logger.debug('Вызван close ЗАГЛУШКИ BrowserController.', exc_info=False)
    # Установка флагов недоступности контроллеров
    BROWSER_CONTROLLER_AVAILABLE = False; BS4_AVAILABLE = False
# --- КОНЕЦ ИМПОРТА КОНТРОЛЛЕРОВ ---

# Загрузка переменных окружения
from dotenv import load_dotenv
# Определение пути к .env файлу
dotenv_path: Path = __root__ / '.env'
# Проверка существования .env файла и его загрузка
if dotenv_path.exists():
    load_dotenv(dotenv_path=dotenv_path); logger.info(f'Загружены переменные окружения из: {dotenv_path}')
else: logger.warning(f'.env файл не найден по пути: {dotenv_path}.')


class Config:
    """ Класс для хранения статической конфигурации приложения. """
    # Конечная точка для конфигурационных файлов, связанных с llm_driver
    ENDPOINT: Path = __root__ / 'src' / 'webdriver' / 'llm_driver'
    # Переменная для хранения загруженной конфигурации в виде SimpleNamespace
    config: SimpleNamespace | None # Изменено на Optional[SimpleNamespace] и добавлена проверка

    # --- ЗАГРУЗКА КОНФИГА ---
    try:
        # Путь к файлу конфигурации use_llm.json
        config_path: Path = ENDPOINT / 'use_llm.json'
        # Проверка существования файла конфигурации
        if config_path.exists():
            # Загрузка конфигурации из JSON файла в SimpleNamespace
            config = j_loads_ns(config_path)
            # Проверка, что конфигурация успешно загружена
            if not config: logger.error(f'Файл конфигурации {config_path} пуст/некорректен!')
            else: logger.info(f'Конфигурация успешно загружена из {config_path}')
        else: 
            # Логирование критической ошибки, если файл конфигурации не найден
            logger.error(f'КРИТИЧЕСКАЯ ОШИБКА: Файл конфигурации НЕ НАЙДЕН: {config_path}!'); config = None
    except Exception as ex: 
        # Логирование критической ошибки при загрузке или парсинге конфигурации
        logger.error(f'КРИТИЧЕСКАЯ ОШИБКА при загрузке/парсинге {config_path}.', ex, exc_info=True); config = None

    # --- ИНИЦИАЛИЗАЦИЯ АТРИБУТОВ КЛАССА ---
    # LLM API ключи и статусы
    GEMINI_API_KEY: Optional[str] = None; GEMINI_STATUS: str = 'inactive'; GEMINI_MODEL_NAME: str = ''
    OPENAI_API_KEY: Optional[str] = None; OPENAI_API_STATUS: str = 'inactive'; OPENAI_MODEL_NAME: str = ''
    # Search Providers API ключи и статусы
    SERPAPI_API_KEY: Optional[str] = None
    TAVILY_API_KEY: Optional[str] = None
    # Статусы поисковых провайдеров по умолчанию
    SEARCH_PROVIDERS_STATUS: Dict[str, str] = {"serpapi": "inactive", "duckduckgo": "active", "tavily": "inactive"}

    # --- Чтение настроек из Config ---
    try:
        # Проверка, что конфигурация была загружена
        if config:
            # Настройки LLM моделей
            if hasattr(config, 'models'):
                models_config: SimpleNamespace = config.models
                gemini_conf: Optional[SimpleNamespace] = getattr(models_config, 'gemini', None)
                GEMINI_STATUS = getattr(gemini_conf, 'status', 'inactive') if gemini_conf else 'inactive'
                GEMINI_MODEL_NAME = getattr(gemini_conf, 'model_name', '') if gemini_conf else ''
                
                openai_conf: Optional[SimpleNamespace] = getattr(models_config, 'openai', None)
                OPENAI_API_STATUS = getattr(openai_conf, 'status', 'inactive') if openai_conf else 'inactive'
                OPENAI_MODEL_NAME = getattr(openai_conf, 'model_name', '') if openai_conf else ''
                
                # Статусы поисковиков могут быть определены в секции 'models' (Вариант А)
                serp_m_conf: Optional[SimpleNamespace] = getattr(models_config, 'serpapi', None)
                SEARCH_PROVIDERS_STATUS["serpapi"] = getattr(serp_m_conf, 'status', SEARCH_PROVIDERS_STATUS["serpapi"]) if serp_m_conf else SEARCH_PROVIDERS_STATUS["serpapi"]
                
                tav_m_conf: Optional[SimpleNamespace] = getattr(models_config, 'tavily', None)
                SEARCH_PROVIDERS_STATUS["tavily"] = getattr(tav_m_conf, 'status', SEARCH_PROVIDERS_STATUS["tavily"]) if tav_m_conf else SEARCH_PROVIDERS_STATUS["tavily"]
                
                ddg_m_conf: Optional[SimpleNamespace] = getattr(models_config, 'duckduckgo', None)
                SEARCH_PROVIDERS_STATUS["duckduckgo"] = getattr(ddg_m_conf, 'status', SEARCH_PROVIDERS_STATUS["duckduckgo"]) if ddg_m_conf else SEARCH_PROVIDERS_STATUS["duckduckgo"]

            # Статусы поисковиков также могут быть определены в секции 'search_providers' (Вариант Б - переопределяет Вариант А)
            if hasattr(config, 'search_providers'):
                search_config: SimpleNamespace = config.search_providers
                serp_s_conf: Optional[SimpleNamespace] = getattr(search_config, 'serpapi', None)
                SEARCH_PROVIDERS_STATUS["serpapi"] = getattr(serp_s_conf, 'status', SEARCH_PROVIDERS_STATUS["serpapi"]) if serp_s_conf else SEARCH_PROVIDERS_STATUS["serpapi"]
                
                tav_s_conf: Optional[SimpleNamespace] = getattr(search_config, 'tavily', None)
                SEARCH_PROVIDERS_STATUS["tavily"] = getattr(tav_s_conf, 'status', SEARCH_PROVIDERS_STATUS["tavily"]) if tav_s_conf else SEARCH_PROVIDERS_STATUS["tavily"]
                
                ddg_s_conf: Optional[SimpleNamespace] = getattr(search_config, 'duckduckgo', None)
                SEARCH_PROVIDERS_STATUS["duckduckgo"] = getattr(ddg_s_conf, 'status', SEARCH_PROVIDERS_STATUS["duckduckgo"]) if ddg_s_conf else SEARCH_PROVIDERS_STATUS["duckduckgo"]
        else: 
            # Логирование предупреждения, если конфигурация не загружена
            logger.warning('Config не загружен. Используются статусы по умолчанию.')
    except AttributeError as ex: 
        # Логирование критической ошибки при чтении структуры конфигурации
        logger.critical(f'Ошибка чтения структуры config: {ex}. Используются статусы по умолчанию.', None, exc_info=False)
        GEMINI_STATUS = 'inactive'; OPENAI_API_STATUS = 'inactive'
        SEARCH_PROVIDERS_STATUS = {"serpapi": "inactive", "duckduckgo": "active", "tavily": "inactive"}

    # --- Установка API ключей ---
    # Попытка установки API ключей из gs.credentials, затем из переменных окружения
    try:
        # Попытка извлечения ключа Gemini из gs.credentials
        try: GEMINI_API_KEY = gs.credentials.gemini.katia.api_key
        except AttributeError: pass # Ошибка игнорируется, если ключ не найден
        # Попытка извлечения ключа OpenAI из gs.credentials
        try: OPENAI_API_KEY = gs.credentials.openai.hypotez.api_key
        except AttributeError: pass
        # Попытка извлечения ключа SerpAPI из gs.credentials
        try: SERPAPI_API_KEY = gs.credentials.serpapi.onela.api_key
        except AttributeError: pass
        # Попытка извлечения ключа Tavily из gs.credentials
        try: TAVILY_API_KEY = gs.credentials.tavily.default.api_key # <-- Укажите ваш путь
        except AttributeError: pass

        # Если ключи не найдены в gs.credentials, попытка извлечения из переменных окружения
        if not GEMINI_API_KEY: GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
        if not OPENAI_API_KEY: OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
        if not SERPAPI_API_KEY: SERPAPI_API_KEY = os.environ.get('SERPAPI_API_KEY')
        if not TAVILY_API_KEY: TAVILY_API_KEY = os.environ.get('TAVILY_API_KEY')

        # Установка ключей в переменные окружения, если они были найдены (некоторые SDK ожидают их там)
        if GEMINI_API_KEY: os.environ['GOOGLE_API_KEY'] = GEMINI_API_KEY
        if OPENAI_API_KEY: os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
        if SERPAPI_API_KEY: os.environ['SERPAPI_API_KEY'] = SERPAPI_API_KEY
        if TAVILY_API_KEY: os.environ['TAVILY_API_KEY'] = TAVILY_API_KEY

        # Логирование статуса конфигурации и наличия ключей
        logger.info(f'Config Gemini: Status={GEMINI_STATUS}, Model={GEMINI_MODEL_NAME}, Key Present={bool(GEMINI_API_KEY)}')
        logger.info(f'Config OpenAI: Status={OPENAI_API_STATUS}, Model={OPENAI_MODEL_NAME}, Key Present={bool(OPENAI_API_KEY)}')
        logger.info(f'Config SerpAPI: Status={SEARCH_PROVIDERS_STATUS.get("serpapi", "N/A")}, Key Present={bool(SERPAPI_API_KEY)}')
        logger.info(f'Config DuckDuckGo: Status={SEARCH_PROVIDERS_STATUS.get("duckduckgo", "N/A")}')
        logger.info(f'Config Tavily: Status={SEARCH_PROVIDERS_STATUS.get("tavily", "N/A")}, Key Present={bool(TAVILY_API_KEY)}')

    except ImportError: logger.warning("Модуль 'src.gs' не найден.")
    except NameError: logger.warning("Объект 'gs.credentials' не найден.")
    except Exception as ex: 
        # Логирование ошибки при установке API ключей
        logger.error('Ошибка при установке API ключей в Config.', ex, exc_info=True)

# ===============================================================
# Функция стриминга
# ===============================================================
async def stream_agent_execution( executor: AgentExecutor, task_input: Dict[str, Any]) -> Tuple[Optional[str], List[Dict[str, Any]]]:
    """
    Асинхронно выполняет агент и стримит шаги выполнения задачи.

    Args:
        executor (AgentExecutor): Инициализированный экземпляр AgentExecutor.
        task_input (Dict[str, Any]): Словарь с входными данными для задачи (например, {'input': 'текст задачи'}).

    Returns:
        Tuple[Optional[str], List[Dict[str, Any]]]: Кортеж, где первый элемент - финальный ответ агента (если есть),
                                                    а второй - список всех чанков, полученных во время стриминга.
    """
    # Инициализация переменных для хранения результата и промежуточных данных
    final_answer: Optional[str] = None
    all_chunks: List[Dict[str, Any]] = []
    run_id: Optional[str] = None # ID текущего запуска агента
    logger.info(f'--- Начало стриминга для входа: {str(task_input)[:200]}... ---')
    try:
        # Асинхронная итерация по чанкам, возвращаемым методом astream агента
        async for chunk in executor.astream(task_input):
            # Добавление каждого чанка в список всех чанков
            all_chunks.append(chunk)
            # Обработка чанков типа 'actions' (планируемые действия агента)
            if actions := chunk.get('actions'):
                for action in actions:
                    tool: str = getattr(action, 'tool', 'N/A') # Имя используемого инструмента
                    tool_input: Any = getattr(action, 'tool_input', 'N/A') # Входные данные для инструмента
                    log_msg: str = getattr(action, 'log', '').strip() # Лог/мысли агента
                    logger.info(f"Планируемое действие: Tool=[{tool}], Input=[{str(tool_input)[:100]}...]")
                    if log_msg: logger.debug(f'  Log (Мысли): {log_msg}', exc_info=False)
            # Обработка чанков типа 'steps' (результаты выполненных действий)
            elif steps := chunk.get('steps'):
                for step in steps:
                    observation: Any = getattr(step, 'observation', None) # Результат (наблюдение) от инструмента
                    action_log: str = getattr(step.action, 'log', '').strip() # Лог/мысли агента перед наблюдением
                    tool_used: str = getattr(step.action, 'tool', 'N/A') # Инструмент, который был использован
                    if observation is not None: logger.info(f"Результат действия (Observation) от Tool=[{tool_used}]: {str(observation)[:300]}...")
                    if action_log: logger.debug(f"  Log (Мысли перед Observation): {action_log}", exc_info=False)
            # Обработка чанка типа 'output' (финальный ответ агента)
            elif output := chunk.get('output'): 
                logger.info(f'Финальный ответ: {output}'); final_answer = output
            # Обработка чанков типа 'messages' (промежуточные сообщения)
            elif messages := chunk.get('messages'):
                 for msg in messages:
                     if content := getattr(msg, 'content', None): logger.debug(f'Message Chunk: {content}', exc_info=False)
            # Извлечение и логирование ID запуска агента, если он изменился
            current_run_info: Dict[str, Any] = chunk.get('__run', {})
            current_run_id: Optional[str] = getattr(current_run_info, 'id', None)
            if current_run_id and current_run_id != run_id: 
                run_id = current_run_id; logger.debug(f'Agent Run ID: {run_id}', exc_info=False)
    except LangChainException as ex: 
        # Логирование ошибок LangChain
        logger.error('Ошибка LangChain во время стриминга.', ex, exc_info=True)
    except Exception as ex: 
        # Логирование неожиданных ошибок
        logger.error('Неожиданная ошибка во время стриминга.', ex, exc_info=True)
    logger.info(f'--- Стриминг завершен. Всего чанков: {len(all_chunks)}. ---')
    return final_answer, all_chunks
# ===============================================================

class Driver:
    """ 
    Класс для управления LLM, контроллерами и агентами LangChain.
    Оркестрирует инициализацию моделей, браузерных контроллеров и инструментов LangChain,
    а также запуск задач с использованием LLM.
    """
    # Ссылка на класс конфигурации
    config_class: Type[Config] = Config
    # Экземпляры LLM моделей
    gemini: Optional[BaseChatModel] = None
    openai: Optional[BaseChatModel] = None
    # Список доступных инструментов LangChain
    tools: List[Tool] = []
    # Экземпляры браузерных контроллеров
    browser: Optional[BrowserController] = None
    data_extractor: Optional[DataExtractionController] = None
    form_controller: Optional[FormController] = None
    screenshot_controller: Optional[ScreenshotController] = None
    download_controller: Optional[DownloadController] = None
    js_executor: Optional[JavaScriptExecutionController] = None
    state_manager: Optional[StateManager] = None
    # Флаг, указывающий, был ли Driver полностью инициализирован (включая асинхронную часть)
    _initialized: bool = False
    # API ключи для поисковых сервисов
    _serpapi_key: Optional[str] = None
    _tavily_key: Optional[str] = None
    # Статусы активности поисковых провайдеров
    _search_provider_statuses: Dict[str, str] = {} 
    # Параметры для инициализации браузера
    _start_browser: bool
    _browser_headless: bool
    _browser_timeout: int

    def __init__(self,
                 GEMINI_API_KEY: Optional[str] = None, OPENAI_API_KEY: Optional[str] = None,
                 SERPAPI_API_KEY: Optional[str] = None, TAVILY_API_KEY: Optional[str] = None,
                 openai_model_name: Optional[str] = None, gemini_model_name: Optional[str] = None,
                 start_browser: bool = True, browser_headless: bool = True, browser_timeout: int = 30000,
                 **kwargs: Any) -> None:
        """
        Синхронно инициализирует LLM и сохраняет параметры для асинхронной инициализации.

        Args:
            GEMINI_API_KEY (Optional[str]): API ключ для Gemini.
            OPENAI_API_KEY (Optional[str]): API ключ для OpenAI.
            SERPAPI_API_KEY (Optional[str]): API ключ для SerpAPI.
            TAVILY_API_KEY (Optional[str]): API ключ для Tavily.
            openai_model_name (Optional[str]): Имя модели OpenAI.
            gemini_model_name (Optional[str]): Имя модели Gemini.
            start_browser (bool): Флаг, запускать ли браузер при инициализации.
            browser_headless (bool): Флаг, запускать ли браузер в безголовом режиме.
            browser_timeout (int): Таймаут для операций браузера в миллисекундах.
            **kwargs (Any): Дополнительные неиспользуемые аргументы.
        """
        # Переменные для хранения ключей и имен моделей
        openai_api_key_local: Optional[str] # Локальная область видимости
        gemini_api_key_local: Optional[str] # Локальная область видимости
        openai_model_name_local: str # Локальная область видимости
        gemini_model_name_local: str # Локальная область видимости
        openai_status_local: str # Локальная область видимости
        gemini_status_local: str # Локальная область видимости

        logger.info('--- Начало СИНХРОННОЙ инициализации Driver ---')
        # Сохранение параметров для инициализации браузера
        self._start_browser = start_browser
        self._browser_headless = browser_headless
        self._browser_timeout = browser_timeout
        # Получение API ключей для поисковых сервисов из аргументов или из Config
        self._serpapi_key = SERPAPI_API_KEY or self.config_class.SERPAPI_API_KEY
        self._tavily_key = TAVILY_API_KEY or self.config_class.TAVILY_API_KEY
        # Копирование статусов поисковых провайдеров из Config
        self._search_provider_statuses = self.config_class.SEARCH_PROVIDERS_STATUS.copy()
        # Установка флага инициализации в False
        self._initialized = False

        # Инициализация атрибутов экземпляра значениями по умолчанию
        self.openai = None; self.gemini = None; self.tools = []; self.browser = None; self.data_extractor = None; self.form_controller = None
        self.screenshot_controller = None; self.download_controller = None; self.js_executor = None; self.state_manager = None

        # Определение API ключей и имен моделей для OpenAI и Gemini
        openai_api_key_local = OPENAI_API_KEY or self.config_class.OPENAI_API_KEY
        gemini_api_key_local = GEMINI_API_KEY or self.config_class.GEMINI_API_KEY
        openai_model_name_local = openai_model_name or self.config_class.OPENAI_MODEL_NAME
        gemini_model_name_local = gemini_model_name or self.config_class.GEMINI_MODEL_NAME
        openai_status_local = self.config_class.OPENAI_API_STATUS
        gemini_status_local = self.config_class.GEMINI_STATUS

        # Установка API ключей в переменные окружения (для некоторых SDK)
        if gemini_api_key_local: os.environ['GEMINI_API_KEY'] = gemini_api_key_local
        if openai_api_key_local: os.environ['OPENAI_API_KEY'] = openai_api_key_local
        if self._serpapi_key: os.environ['SERPAPI_API_KEY'] = self._serpapi_key
        if self._tavily_key: os.environ['TAVILY_API_KEY'] = self._tavily_key

        # Инициализация моделей LLM
        self.openai = self._initialize_openai(openai_api_key_local, openai_status_local, openai_model_name_local)
        self.gemini = self._initialize_gemini(gemini_api_key_local, gemini_status_local, gemini_model_name_local)

        # Логирование неиспользованных аргументов, если они есть
        if kwargs: logger.warning(f'Неиспользованные аргументы: {kwargs}', exc_info=False)
        logger.info('--- Синхронная инициализация Driver завершена. Вызовите async_init() ---')

    async def async_init(self) -> bool:
        """ 
        Асинхронно инициализирует BrowserController, зависимые контроллеры и инструменты LangChain.
        Этот метод должен быть вызван после синхронного __init__.

        Returns:
            bool: True, если асинхронная инициализация прошла успешно, иначе False.
        """
        # Проверка, не был ли Driver уже инициализирован
        if self._initialized: 
            logger.info('Driver уже инициализирован.'); return True
        logger.info('--- Начало АСИНХРОННОЙ инициализации Driver ---')
        # Очистка списка инструментов перед новой инициализацией
        self.tools = []
        # Асинхронная инициализация браузера и связанных контроллеров
        await self._async_initialize_browser_and_controllers(self._start_browser, self._browser_headless, self._browser_timeout)
        # Создание инструментов LangChain на основе инициализированных контроллеров
        self._create_tools()
        logger.info(f'Итоговый список доступных инструментов Driver: {[tool.name for tool in self.tools]}')
        # Установка флага успешной инициализации
        self._initialized = True
        logger.info('--- Асинхронная инициализация Driver завершена ---')
        return True

    def _initialize_openai(self, api_key: Optional[str], status: str, model_name: str) -> Optional[BaseChatModel]:
        """ 
        Синхронно инициализирует модель OpenAI (ChatOpenAI).

        Args:
            api_key (Optional[str]): API ключ для OpenAI.
            status (str): Статус активности модели ('active' для инициализации).
            model_name (str): Имя модели OpenAI (например, 'gpt-3.5-turbo').

        Returns:
            Optional[BaseChatModel]: Экземпляр ChatOpenAI или None, если инициализация не удалась.
        """
        llm: Optional[BaseChatModel] = None
        # Проверка наличия API ключа, активного статуса и имени модели
        if api_key and status.lower() == 'active' and model_name:
            logger.info(f'Инициализация OpenAI: Model={model_name}')
            try: 
                # Создание экземпляра ChatOpenAI
                llm = ChatOpenAI(model_name=model_name, openai_api_key=api_key, temperature=0.1)
                logger.info('OpenAI LLM инициализирован.')
            except Exception as ex: 
                # Логирование ошибки инициализации
                logger.error('Ошибка инициализации OpenAI.', ex, exc_info=True)
        else: 
            # Логирование предупреждения, если условия для инициализации не выполнены
            logger.warning(f'OpenAI LLM не инициализирован (Key={bool(api_key)}, Status={status}, Model={model_name})', exc_info=False)
        return llm

    def _initialize_gemini(self, api_key: Optional[str], status: str, model_name: str) -> Optional[BaseChatModel]:
        """ 
        Синхронно инициализирует модель Gemini (ChatGoogleGenerativeAI).

        Args:
            api_key (Optional[str]): API ключ для Google Gemini.
            status (str): Статус активности модели ('active' для инициализации).
            model_name (str): Имя модели Gemini (например, 'gemini-pro').

        Returns:
            Optional[BaseChatModel]: Экземпляр ChatGoogleGenerativeAI или None, если инициализация не удалась.
        """
        llm: Optional[BaseChatModel] = None
        # Проверка наличия API ключа, активного статуса и имени модели
        if api_key and status.lower() == 'active' and model_name:
            logger.info(f'Инициализация Gemini: Model={model_name}')
            try: 
                # Создание экземпляра ChatGoogleGenerativeAI
                llm = ChatGoogleGenerativeAI(model=model_name, google_api_key=api_key, temperature=0.1, convert_system_message_to_human=True)
                logger.info('Gemini LLM инициализирован.')
            except Exception as ex: 
                # Логирование ошибки инициализации
                logger.error('Ошибка инициализации Gemini.', ex, exc_info=True)
        else: 
            # Логирование предупреждения, если условия для инициализации не выполнены
            logger.warning(f'Gemini LLM не инициализирован (Key={bool(api_key)}, Status={status}, Model={model_name})', exc_info=False)
        return llm

    async def _async_initialize_browser_and_controllers(self, start: bool, headless: bool, timeout: int) -> None:
        """ 
        Асинхронно инициализирует BrowserController и зависимые от него контроллеры.

        Args:
            start (bool): Флаг, указывающий, нужно ли запускать браузер.
            headless (bool): Флаг, запускать ли браузер в безголовом режиме.
            timeout (int): Таймаут для операций браузера.
        """
        # Сброс экземпляров контроллеров
        self.browser = None; self.data_extractor = None; self.form_controller = None; self.screenshot_controller = None; self.download_controller = None; self.js_executor = None; self.state_manager = None
        browser_started: bool = False # Флаг успешного запуска браузера
        # Проверка, нужно ли запускать браузер
        if not start: 
            logger.info('Иниц. браузера пропущена (start=False).'); return
        # Проверка доступности основного BrowserController
        if not BROWSER_CONTROLLER_AVAILABLE: 
            logger.warning('BrowserController недоступен.', exc_info=False); return
        try:
            logger.info('Асинхронная инициализация BrowserController...')
            # Создание экземпляра BrowserController
            self.browser = BrowserController(headless=headless, timeout=timeout)
            # Асинхронный запуск браузера
            browser_started = await self.browser.start()
            # Проверка успешности запуска
            if not browser_started: 
                logger.error('Не удалось запустить BrowserController!'); self.browser = None; return
            logger.info('BrowserController асинхронно инициализирован.')
            # Инициализация зависимых контроллеров, если браузер успешно запущен и имеет активные page/context
            if self.browser and self.browser.page and self.browser.context:
                logger.info('Инициализация зависимых контроллеров...')
                # Инициализация DataExtractionController, если BS4 доступен
                if BS4_AVAILABLE:
                    try: self.data_extractor = DataExtractionController(); logger.info('DataExtractionController иниц.')
                    except Exception as ex: logger.warning(f'Ошибка init DataExtractionController: {ex}', exc_info=False)
                else: logger.warning('BS4 недоступен, DataExtractionController не иниц.')
                # Инициализация FormController
                try: self.form_controller = FormController(page=self.browser.page); logger.info('FormController иниц.')
                except Exception as ex: logger.warning(f'Ошибка init FormController: {ex}', exc_info=False)
                # Инициализация ScreenshotController
                try: self.screenshot_controller = ScreenshotController(page=self.browser.page); logger.info('ScreenshotController иниц.')
                except Exception as ex: logger.warning(f'Ошибка init ScreenshotController: {ex}', exc_info=False)
                # Инициализация DownloadController
                try: self.download_controller = DownloadController(page=self.browser.page); logger.info('DownloadController иниц.')
                except Exception as ex: logger.warning(f'Ошибка init DownloadController: {ex}', exc_info=False)
                # Инициализация JavaScriptExecutionController
                try: self.js_executor = JavaScriptExecutionController(page=self.browser.page); logger.info('JavaScriptExecutionController иниц.')
                except Exception as ex: logger.warning(f'Ошибка init JavaScriptExecutionController: {ex}', exc_info=False)
                # Инициализация StateManager
                try: self.state_manager = StateManager(context=self.browser.context, page=self.browser.page); logger.info('StateManager иниц.')
                except Exception as ex: logger.warning(f'Ошибка init StateManager: {ex}', exc_info=False)
            else: 
                # Логирование ошибки, если page/context браузера недоступны
                logger.error('BrowserController page/context недоступны!')
        except Exception as ex:
            # Логирование ошибки при асинхронной инициализации
            logger.error('Ошибка при асинхронной инициализации BrowserController.', ex, exc_info=True)
            # Попытка закрыть браузер, если он был частично инициализирован
            if self.browser: await self.browser.close()
            self.browser = None # Сброс экземпляра браузера

    def _create_tools(self) -> None:
        """ 
        Создает инструменты LangChain для активных поисковых систем и 
        инициализированных браузерных контроллеров.
        """
        logger.info('Создание инструментов LangChain...')
        # Очистка списка инструментов
        self.tools = []
        # Функция-заглушка для синхронных вызовов асинхронных инструментов
        def _sync_error_func(*args: Any, **kwargs: Any) -> str: return 'Ошибка: асинхронный вызов (use coroutine).'

        # --- 1. Поисковые Инструменты ---
        search_tool_added: bool = False # Флаг, был ли добавлен хотя бы один поисковый инструмент
        # SerpAPI (Google)
        if self._search_provider_statuses.get("serpapi") == "active":
            if self._serpapi_key:
                try:
                    # Создание инструмента SerpAPI
                    serp_tool = Tool(name="GoogleSearch", func=SerpAPIWrapper().run, description="Поиск Google (SerpAPI). Вход: запрос.")
                    self.tools.append(serp_tool); logger.debug('Инструмент GoogleSearch (SerpAPI) добавлен.'); search_tool_added = True
                except Exception as ex: 
                    # Логирование ошибки создания инструмента SerpAPI
                    logger.error(f"Ошибка создания SerpAPI Tool: {ex}", exc_info=True)
            else: 
                # Предупреждение, если ключ SerpAPI отсутствует при активном статусе
                logger.warning("SerpAPI активен, но ключ SERPAPI_API_KEY не найден!")
        # Tavily Search
        if self._search_provider_statuses.get("tavily") == "active":
            if self._tavily_key:
                try:
                    # Создание инструмента Tavily
                    tav_tool = TavilySearchResults(max_results=5, name="TavilySearch", description="Поиск Tavily. Вход: запрос.")
                    self.tools.append(tav_tool); logger.debug('Инструмент TavilySearch добавлен.'); search_tool_added = True
                except Exception as ex: 
                    # Логирование ошибки создания инструмента Tavily
                    logger.error(f"Ошибка создания Tavily Tool: {ex}", exc_info=True)
            else: 
                # Предупреждение, если ключ Tavily отсутствует при активном статусе
                logger.warning("Tavily активен, но ключ TAVILY_API_KEY не найден!")
        # DuckDuckGo
        if self._search_provider_statuses.get("duckduckgo") == "active":
            try:
                # Создание инструмента DuckDuckGo
                ddg_tool = DuckDuckGoSearchRun(name="DuckDuckGoSearch", description="Поиск DuckDuckGo. Вход: запрос.")
                self.tools.append(ddg_tool); logger.debug('Инструмент DuckDuckGoSearch добавлен.'); search_tool_added = True
            except Exception as ex: 
                # Логирование ошибки создания инструмента DuckDuckGo
                logger.error(f"Ошибка создания DuckDuckGo Tool: {ex}", exc_info=True)
        # Предупреждение, если ни один поисковый инструмент не был добавлен
        if not search_tool_added: logger.warning("Ни один поисковый инструмент не был добавлен!")

        # --- 2. Браузерные Инструменты ---
        if self.browser:
            # Асинхронные обертки для методов BrowserController
            async def _nav(u: str) -> str: return await self.browser.navigate(u) if self.browser else 'Err:BrowserNA'
            async def _st(s: Optional[str]=None) -> str: return await self.browser.scrape_text(s) if self.browser else 'Err:BrowserNA'
            async def _sh(s: Optional[str]=None) -> str: return await self.browser.scrape_html(s) if self.browser else 'Err:BrowserNA'
            async def _ce(s: str) -> str: return await self.browser.click_element(s) if self.browser else 'Err:BrowserNA'
            # Синхронная обертка (не требует await)
            def _gu(i: Any=None) -> str: return self.browser.get_current_url() if self.browser else 'Err:BrowserNA'
            # Создание инструментов для BrowserController
            browser_tools: List[Tool] = [ 
                Tool('BrowserNavigate',_sync_error_func,coroutine=_nav,description='URL Nav'), 
                Tool('BrowserScrapeText',_sync_error_func,coroutine=_st,description='Scrape Text(sel?)'), 
                Tool('BrowserScrapeHTML',_sync_error_func,coroutine=_sh,description='Scrape HTML(sel?)'), 
                Tool('BrowserClickElement',_sync_error_func,coroutine=_ce,description='Click(sel)'), 
                Tool('GetCurrentURL',_gu,description='Get URL') 
            ]
            self.tools.extend(browser_tools); logger.debug(f'Добавлено {len(browser_tools)} инструментов BrowserController.')
        else: 
            # Предупреждение, если BrowserController не инициализирован
            logger.warning('Инструменты BrowserController не созданы.')

        # --- 3. Инструменты Извлечения Данных ---
        if self.data_extractor:
            # Обертка для find_links, обрабатывающая входной словарь
            def _fl_wrap(p: Any) -> Union[List[str], Dict[str, str]]:
                if not isinstance(p, dict): return {'error': 'Err:BadInput'}
                if 'html' not in p: return {'error': 'Err:NoHTML'}
                try: 
                    base_url_val: Optional[str] = p.get('base_url') or (self.browser.get_current_url() if self.browser else None)
                    return self.data_extractor.find_links(p['html'], base_url_val) if self.data_extractor else {'error':'Err:ExtractorNA'}
                except Exception as ex: 
                    logger.error("FindPageLinks Ошибка", ex, exc_info=True); return {'error': f'Err:{ex}'}
            # Создание инструментов для DataExtractionController
            extract_tools: List[Tool] = [ 
                Tool('ExtractProductSchema', lambda h: self.data_extractor.extract_product_details(h) if self.data_extractor else 'Err:ExtractorNA', description='Extract Product'), 
                Tool('ExtractContactInfo', lambda t: self.data_extractor.extract_contact_info(t) if self.data_extractor else 'Err:ExtractorNA', description='Extract Contact'), 
                Tool('FindPageLinks', _fl_wrap, description="Find Links {'html':...,'base_url':?}") 
            ]
            self.tools.extend(extract_tools); logger.debug(f'Добавлено {len(extract_tools)} инструментов DataExtraction.')
        else: 
            # Предупреждение, если DataExtractionController не инициализирован
            logger.warning('Инструменты DataExtractionController не созданы.')

        # --- 4. Инструменты Управления Формами ---
        if self.form_controller:
            # Асинхронные обертки для методов FormController
            async def _fff(p: Dict[str,Any]) -> str: return await self.form_controller.fill_input_field(p['selector'],p['value']) if self.form_controller and isinstance(p,dict) else 'Err:FormNA/BadInput'
            async def _sdd(p: Dict[str,Any]) -> str: return await self.form_controller.select_dropdown_option(p['selector'],value=p.get('value'),label=p.get('label')) if self.form_controller and isinstance(p,dict) else 'Err:FormNA/BadInput'
            async def _sf(p: Dict[str,Any]) -> str: return await self.form_controller.submit_form(form_selector=p.get('form_selector'),submit_button_selector=p.get('submit_button_selector')) if self.form_controller and isinstance(p,dict) else 'Err:FormNA/BadInput'
            # Создание инструментов для FormController
            form_tools: List[Tool] = [ 
                Tool('FillFormField',_sync_error_func,coroutine=_fff,description="Fill {'sel':...,'val':...}"), 
                Tool('SelectDropdown',_sync_error_func,coroutine=_sdd,description="Select {'sel':...,'val':?/'lbl':?}"), 
                Tool('SubmitForm',_sync_error_func,coroutine=_sf,description="Submit {'form_sel':?,'btn_sel':?}") 
            ]
            self.tools.extend(form_tools); logger.debug(f'Добавлено {len(form_tools)} инструментов FormController.')
        else: 
            # Предупреждение, если FormController не инициализирован
            logger.warning('Инструменты FormController не созданы.')

        # --- 5. Инструмент Скриншотов ---
        if self.screenshot_controller:
            # Асинхронная обертка для метода take_screenshot
            async def _ss(p: Dict[str,Any]) -> str: return await self.screenshot_controller.take_screenshot(p['save_path'],full_page=p.get('full_page',True),selector=p.get('selector')) if self.screenshot_controller and isinstance(p,dict) else 'Err:SSNA/BadInput'
            # Создание инструмента TakeScreenshot
            self.tools.append(Tool('TakeScreenshot',_sync_error_func,coroutine=_ss,description="Screenshot {'path':...,'full':?,'sel':?}"))
            logger.debug('Инструмент TakeScreenshot добавлен.')
        else: 
            # Предупреждение, если ScreenshotController не инициализирован
            logger.warning('Инструмент TakeScreenshot не создан.')

        # --- 6. Инструмент Загрузки ---
        if self.download_controller:
            # Асинхронная обертка для метода click_and_download
            async def _dl(p: Dict[str,Any]) -> str: return await self.download_controller.click_and_download(p['click_selector'],p['save_directory'],timeout=p.get('timeout',60000)) if self.download_controller and isinstance(p,dict) else 'Err:DLNA/BadInput'
            # Создание инструмента ClickAndDownload
            self.tools.append(Tool('ClickAndDownload',_sync_error_func,coroutine=_dl,description="Download {'clk_sel':...,'dir':...,'to':?}"))
            logger.debug('Инструмент ClickAndDownload добавлен.')
        else: 
            # Предупреждение, если DownloadController не инициализирован
            logger.warning('Инструмент ClickAndDownload не создан.')

        # --- 7. Инструмент Выполнения JS ---
        if self.js_executor:
            # Асинхронная обертка для метода execute_script
            async def _ejs(s: str) -> Union[str, Any]: return await self.js_executor.execute_script(s) if self.js_executor else 'Err:JsExecNA'
            # Создание инструмента ExecuteJavaScript
            self.tools.append(Tool('ExecuteJavaScript',_sync_error_func,coroutine=_ejs,description="JS Exec (WARN!)"))
            logger.debug('Инструмент ExecuteJavaScript добавлен.')
        else: 
            # Предупреждение, если JavaScriptExecutionController не инициализирован
            logger.warning('Инструмент ExecuteJavaScript не создан.')

        # --- 8. Инструменты Управления Состоянием ---
        if self.state_manager:
            # Асинхронные обертки для методов StateManager
            async def _gc(u: Optional[str]=None) -> Union[List[Dict[str, Any]],str]: return await self.state_manager.get_cookies(u) if self.state_manager else 'Err:StateNA'
            async def _cc() -> str: return await self.state_manager.clear_cookies() if self.state_manager else 'Err:StateNA'
            async def _cs() -> str: return await self.state_manager.clear_storage() if self.state_manager else 'Err:StateNA'
            # Синхронная обертка для login (является заглушкой)
            def _l(*a: Any, **kw: Any) -> str: return self.state_manager.login(*a, **kw) if self.state_manager else 'Err:StateNA'
            # Создание инструментов для StateManager
            state_tools: List[Tool] = [ 
                Tool('GetCookies',_sync_error_func,coroutine=_gc,description="Get Cookies(url?)"), 
                Tool('ClearCookies',_sync_error_func,coroutine=_cc,description="Clear Cookies"), 
                Tool('ClearStorage',_sync_error_func,coroutine=_cs,description="Clear Storage"), 
                Tool('Login',_l,description="Login(stub)") 
            ]
            self.tools.extend(state_tools); logger.debug(f'Добавлено {len(state_tools)} инструментов StateManager.')
        else: 
            # Предупреждение, если StateManager не инициализирован
            logger.warning('Инструменты StateManager не созданы.')

    # --- Методы run_task, stream_task, __del__, close, _get_agent_executor ---
    async def _get_agent_executor(self, llm: BaseChatModel) -> Optional[AgentExecutor]:
        """ 
        Создает и возвращает AgentExecutor на основе предоставленной LLM и доступных инструментов.

        Args:
            llm (BaseChatModel): Инициализированная модель LLM (Gemini или OpenAI).

        Returns:
            Optional[AgentExecutor]: Экземпляр AgentExecutor или None, если создание не удалось.
        """
        # Проверка инициализации Driver
        if not self._initialized: 
            logger.error('Driver не инициализирован!'); return None
        # Проверка наличия LLM
        if not llm: 
            logger.error('LLM не предоставлена.'); return None
        # Проверка наличия инструментов
        if not self.tools: 
            logger.error('Инструменты не созданы.'); return None
        
        # Переменные для хранения промпта, исполняемого агента и AgentExecutor
        prompt: Any
        agent_runnable: Any
        agent_executor: AgentExecutor
        try:
            # Загрузка стандартного ReAct промпта из LangChain Hub
            prompt = hub.pull('hwchase17/react')
            logger.debug(f'Создание агента: LLM={type(llm).__name__}, Tools={[t.name for t in self.tools]}')
            # Создание исполняемого агента (runnable)
            agent_runnable = create_react_agent(llm=llm, tools=self.tools, prompt=prompt)
            # Создание AgentExecutor
            agent_executor = AgentExecutor(
                agent=agent_runnable, 
                tools=self.tools, 
                verbose=True, # Включение подробного логирования шагов агента
                handle_parsing_errors=True, # Обработка ошибок парсинга ответа LLM
                max_iterations=30, # Максимальное количество итераций агента
                max_execution_time=300.0 # Максимальное время выполнения задачи в секундах
            )
            logger.info('AgentExecutor создан.'); return agent_executor
        except Exception as ex: 
            # Логирование ошибки создания AgentExecutor
            logger.error('Ошибка создания AgentExecutor.', ex, exc_info=True); return None

    async def run_task(self, task: str, use_gemini: bool = True) -> Optional[str]:
        """
        Запускает задачу с использованием выбранной LLM и возвращает финальный результат.
        Обрабатывает ошибки, включая ошибки квоты Google Gemini и DuckDuckGo, с логикой повторных попыток.

        Args:
            task (str): Текст задачи для выполнения агентом.
            use_gemini (bool): Флаг, использовать ли Gemini (True) или OpenAI (False).

        Returns:
            Optional[str]: Строка с финальным ответом агента или None/строка с ошибкой в случае неудачи.
        """
        # Ленивая асинхронная инициализация, если она еще не была выполнена
        if not self._initialized:
            init_ok: bool = await self.async_init()
            if not init_ok: 
                logger.error('Ошибка инициализации Driver для run_task.'); return None
            logger.info("Ленивая инициализация Driver завершена успешно.")

        # Определение имени модели и выбор LLM
        model_name: str = 'Gemini' if use_gemini else 'OpenAI'
        selected_llm: Optional[BaseChatModel] = self.gemini if use_gemini else self.openai
        # Переменные для AgentExecutor, данных результата, ответа и счетчиков
        agent_executor: Optional[AgentExecutor]
        result_data: Optional[Dict[str, Any]] = None
        final_answer_raw: Optional[str] = None
        retry_count: int = 0
        max_retries: int = 3 # Максимальное количество повторных попыток

        logger.info(f"Запуск run_task ({model_name}): '{task[:100]}...'")
        # Проверка, инициализирована ли выбранная LLM
        if not selected_llm: 
            logger.error(f'LLM ({model_name}) не инициализирована.'); return None
        # Получение AgentExecutor
        agent_executor = await self._get_agent_executor(selected_llm)
        if not agent_executor: return None

        # --- НАЧАЛО ЦИКЛА ПОВТОРНЫХ ПОПЫТОК ---
        while retry_count <= max_retries:
            try:
                logger.info(f'Вызов agent_executor.ainvoke ({model_name}) (Попытка {retry_count + 1}/{max_retries + 1})...')
                # Асинхронный вызов агента для выполнения задачи
                result_data = await agent_executor.ainvoke({'input': task})
                # Извлечение финального ответа из результата
                final_answer_raw = result_data.get('output')
                logger.info(f'Агент ({model_name}) успешно завершил run_task.')
                # Предупреждение, если финальный ответ отсутствует
                if final_answer_raw is None: 
                    logger.warning(f'Финальный ответ ("output") отсутствует ({model_name}). Result: {result_data}', exc_info=False)
                break # Успешное выполнение, выход из цикла

            except ValueError as ex_val:
                # Обработка ValueError (может быть вызвано, например, ошибкой парсинга в LangChain)
                logger.warning(f"Обработанная ошибка ValueError ({model_name}): {ex_val}", exc_info=False)
                final_answer_raw = f"Задача не выполнена: {ex_val}"; break # Выход из цикла

            except google_api_exceptions.ResourceExhausted as ex_quota:
                # Обработка ошибки квоты Google Gemini
                retry_count += 1
                logger.error(f"Ошибка квоты Google Gemini ({model_name}) (Попытка {retry_count}/{max_retries}).", ex_quota, exc_info=False)
                # Проверка превышения лимита попыток
                if retry_count > max_retries:
                    logger.error(f"Превышен лимит ({max_retries}) попыток Google."); final_answer_raw = f"Ошибка: Превышена квота Google Gemini после {max_retries} попыток."; break
                
                # Определение задержки перед повторной попыткой
                retry_delay_seconds: int = 60; delay_extracted: bool = False
                # Попытка извлечь рекомендованную задержку из метаданных исключения
                if hasattr(ex_quota, 'metadata') and ex_quota.metadata:
                     for item in ex_quota.metadata:
                         if item[0] == 'retry-delay':
                            try:
                                delay_info: Dict[str, Any] = json.loads(item[1])
                                retry_delay_seconds = max(1, int(delay_info.get('seconds', retry_delay_seconds)))
                                delay_extracted = True; break
                            except Exception as parse_ex: 
                                logger.warning(f"Не удалось распарсить retry-delay: '{item[1]}'. Ошибка: {parse_ex}", exc_info=False)
                delay_msg: str = f"Рекомендуемая задержка: {retry_delay_seconds} сек." if delay_extracted else f"Используем задержку по умолчанию: {retry_delay_seconds} сек."
                logger.info(f"{delay_msg} Ожидание перед повторной попыткой (Google)..."); await asyncio.sleep(retry_delay_seconds)

            # --- НОВЫЙ БЛОК ОБРАБОТКИ ОШИБКИ DDG ---
            except DuckDuckGoSearchException as ex_ddg:
                # Обработка исключений от DuckDuckGoSearch
                # Проверка, является ли это ошибкой Rate Limit (по ключевым словам или коду)
                if "ratelimit" in str(ex_ddg).lower() or "202" in str(ex_ddg): 
                    retry_count += 1
                    logger.error(f"Ошибка Rate Limit DuckDuckGo ({model_name}) (Попытка {retry_count}/{max_retries}).", ex_ddg, exc_info=False)
                    # Проверка превышения лимита попыток
                    if retry_count > max_retries:
                        logger.error(f"Превышен лимит ({max_retries}) попыток DDG."); final_answer_raw = f"Ошибка: Rate Limit DuckDuckGo после {max_retries} попыток."; break

                    # Установка фиксированной задержки для DDG (например, 30 секунд)
                    ddg_retry_delay_seconds: int = 30
                    logger.info(f"Ожидание {ddg_retry_delay_seconds} сек. перед повторной попыткой (DDG)...")
                    await asyncio.sleep(ddg_retry_delay_seconds)
                else:
                    # Другая ошибка от DDG - не повторяем, выходим из цикла
                    logger.error(f"Неожиданная ошибка DuckDuckGo ({model_name}).", ex_ddg, exc_info=True)
                    final_answer_raw = f"Ошибка DuckDuckGo: {ex_ddg}"; break
            # --- КОНЕЦ НОВОГО БЛОКА ---

            except LangChainException as ex_lc:
                # Обработка общих ошибок LangChain
                logger.error(f'Ошибка LangChain ({model_name}).', ex_lc, exc_info=True); final_answer_raw = f"Ошибка LangChain: {ex_lc}"; break # Выход из цикла
            except Exception as ex_other:
                # Обработка других неожиданных ошибок
                logger.error(f'Неожиданная ошибка ({model_name}).', ex_other, exc_info=True); final_answer_raw = f"Неожиданная ошибка: {ex_other}"; break # Выход из цикла
        # --- КОНЕЦ ЦИКЛА ПОВТОРНЫХ ПОПЫТОК ---

        # --- ПОСТ-ОБРАБОТКА ОТВЕТА ---
        # Проверка, что финальный ответ получен и является строкой
        if final_answer_raw and isinstance(final_answer_raw, str):
            try:
                # Попытка парсинга ответа как JSON
                parsed_data: Any = json.loads(final_answer_raw)
                # Специальная обработка для случая, когда агент вернул сводку вместо списка URL
                trigger_message: str = "provided a summary instead of a list of URLs"
                if (isinstance(parsed_data, dict) and
                        parsed_data.get("product_links") == [] and
                        isinstance(parsed_data.get("message"), str) and
                        trigger_message in parsed_data["message"]):
                    target_domain: str = parsed_data.get("target_domain", "Unknown")
                    summary_text: str = parsed_data["message"]
                    logger.info("Агент вернул сводку вместо ссылок. Переформатируем вывод.")
                    summary_output: Dict[str, str] = {"target_domain": target_domain, "summary": summary_text}
                    return json.dumps(summary_output, ensure_ascii=False, indent=2)
                else:
                    # Возврат оригинального JSON-ответа
                    return final_answer_raw
            except json.JSONDecodeError:
                # Если ответ не JSON, логируем предупреждение и возвращаем как есть
                logger.warning(f"Агент ({model_name}) вернул не JSON ответ: {final_answer_raw[:200]}...")
                return final_answer_raw
            except Exception as post_ex:
                # Логирование ошибки пост-обработки
                logger.error(f"Ошибка пост-обработки ответа агента ({model_name}): {post_ex}", None, exc_info=True)
                return final_answer_raw # Возврат сырого ответа при ошибке пост-обработки
        else:
            # Возврат None или того, что было в final_answer_raw, если это не строка
            return final_answer_raw

    async def stream_task(self, task: str, use_gemini: bool = True) -> Tuple[Optional[str], List[Dict[str, Any]]]:
        """ 
        Запускает задачу и стримит шаги выполнения агента.

        Args:
            task (str): Текст задачи для выполнения агентом.
            use_gemini (bool): Флаг, использовать ли Gemini (True) или OpenAI (False).

        Returns:
            Tuple[Optional[str], List[Dict[str, Any]]]: Кортеж, где первый элемент - финальный ответ агента,
                                                        а второй - список всех чанков, полученных во время стриминга.
        """
        # Ленивая инициализация, если необходимо
        init_ok: bool # Объявление переменной до блока if
        if not self._initialized: 
            init_ok = await self.async_init()
            if not init_ok: 
                logger.error("Ошибка инициализации Driver для stream_task."); return None, []
        
        # Определение имени модели и выбор LLM
        model_name: str = 'Gemini' if use_gemini else 'OpenAI'
        selected_llm: Optional[BaseChatModel] = self.gemini if use_gemini else self.openai
        # Переменные для AgentExecutor, ответа и чанков
        agent_executor: Optional[AgentExecutor]
        final_answer: Optional[str] = None
        all_chunks: List[Dict[str, Any]] = []
        
        logger.info(f"Запуск stream_task ({model_name}): '{task[:100]}...'")
        # Проверка инициализации LLM
        if not selected_llm: 
            logger.error(f'LLM ({model_name}) не инициализирована.'); return None, []
        # Получение AgentExecutor
        agent_executor = await self._get_agent_executor(selected_llm)
        if not agent_executor: return None, []
        
        logger.info(f'Начало стриминга ({model_name})...');
        try: 
            # Вызов функции стриминга
            final_answer, all_chunks = await stream_agent_execution(executor=agent_executor, task_input={'input': task})
        except google_api_exceptions.ResourceExhausted as ex: 
            # Обработка ошибки квоты Google
            logger.error(f"Ошибка квоты Google в stream_task ({model_name}).", ex, exc_info=False)
            final_answer = "Ошибка: Превышена квота Google."; all_chunks = [] # Установка сообщения об ошибке
        except Exception as ex: 
            # Обработка других неожиданных ошибок
            logger.error(f"Неожиданная ошибка в stream_task ({model_name}).", ex, exc_info=True)
            final_answer = f"Ошибка стриминга: {ex}" # Установка сообщения об ошибке
            all_chunks = [] # Очистка чанков при ошибке
        logger.info(f'Стриминг ({model_name}) завершен.'); return final_answer, all_chunks

    def __del__(self) -> None:
        """ 
        Деструктор для попытки асинхронного закрытия браузера.
        Примечание: Надежное асинхронное закрытие из деструктора затруднено.
        Рекомендуется явный вызов `await driver.close()`.
        """
        if self.browser:
            logger.info('Попытка закрытия BrowserController из __del__...'); 
            loop: Optional[asyncio.AbstractEventLoop]
            try: 
                # Получение текущего цикла событий
                loop = asyncio.get_event_loop_policy().get_event_loop()
            except RuntimeError: 
                # Цикл событий может быть уже закрыт или не существует
                loop = None
            # Проверка, запущен ли цикл событий
            if loop and loop.is_running(): 
                logger.warning("__del__: Невозможно надежно вызвать async close из раб. цикла.")
            else: 
                logger.warning("__del__: Нет активного цикла событий для вызова async close.")
            logger.warning("Рекомендуется явно вызывать 'await driver.close()'.")

    async def close(self) -> None:
        """ 
        Асинхронно закрывает браузер (если был инициализирован) и освобождает ресурсы Playwright.
        Сбрасывает флаг инициализации Driver.
        """
        if self.browser: 
            logger.info("Явный вызов async close()..."); 
            await self.browser.close() # Асинхронное закрытие браузера
            self.browser = None # Сброс экземпляра браузера
        # Сброс флага инициализации
        self._initialized = False

# --- Функция main для демонстрации ---
async def main() -> None:
    """ 
    Основная асинхронная функция для демонстрации работы класса Driver.
    Инициализирует Driver, проверяет доступность инструментов, формирует и запускает задачу.
    """
    # Инициализация переменных
    driver: Optional[Driver] = None
    init_success: bool = False
    search_available: bool = False
    browser_core_available: bool = False
    extraction_available: bool = False
    interaction_available: bool = False
    available_tool_names: List[str] = []
    task_to_run: Optional[str] = None
    llm_to_test_run: List[Tuple[str, bool]] = [] # Список кортежей (имя LLM, флаг use_gemini)
    # Переменные для использования внутри циклов и блоков try
    name_llm: str # Используем другое имя, чтобы не конфликтовать с name из langchain.agents.Tool
    flag_use_gemini: bool # Аналогично
    start_time: float
    end_time: float
    result: Optional[str]
    parsed_result: Any
    product_category: str
    num_links_str: str
    search_query: str
    search_tool_name_main: str # Используем другое имя

    try:
        logger.info('='*20 + ' Начало инициализации Driver ' + '='*20)
        # Создание экземпляра Driver с настройками по умолчанию (запуск браузера, безголовый режим)
        driver = Driver(start_browser=True, browser_headless=True)
        # Асинхронная инициализация Driver
        init_success = await driver.async_init()
        if not init_success: 
            logger.critical('Асинхронная инициализация Driver не удалась.'); return
        logger.info('='*20 + ' Завершение инициализации Driver ' + '='*20)
    except Exception as ex: 
        # Логирование критической ошибки инициализации
        logger.critical('Крит. ошибка инициализации Driver.', ex, exc_info=True)
        # Попытка закрыть драйвер, если он был частично инициализирован
        if driver: await driver.close() 
        return # Выход из функции main в случае ошибки
        

    try:
        # Проверка доступности инструментов после инициализации
        logger.info('Проверка доступности инструментов...')
        if driver: # Проверка, что driver не None
            available_tool_names = [tool.name for tool in driver.tools]
            logger.info(f'Инструменты: {available_tool_names}')
            # Определение доступности поисковых инструментов
            search_tools: List[str] = [name_tool for name_tool in available_tool_names if name_tool in ["GoogleSearch", "TavilySearch", "DuckDuckGoSearch"]]
            search_available = bool(search_tools)
            logger.info(f"Поиск доступен: {search_tools if search_available else 'Нет'}")
            # Определение доступности основных браузерных инструментов
            browser_core_available = all(n in available_tool_names for n in ['BrowserNavigate', 'BrowserScrapeText'])
            # Определение доступности инструмента извлечения данных о продукте
            extraction_available = 'ExtractProductSchema' in available_tool_names
            # Определение доступности инструментов взаимодействия (клик, заполнение форм)
            interaction_available = all(n in available_tool_names for n in ['BrowserClickElement', 'FillFormField'])
            logger.info(f'Статус: Поиск={search_available}, Браузер={browser_core_available}, Экстракция={extraction_available}, Взаимодействие={interaction_available}')

            # Выбор поискового инструмента по приоритету
            search_tool_name_main = "DuckDuckGoSearch" # По умолчанию
            if 'TavilySearch' in search_tools: search_tool_name_main = 'TavilySearch'
            elif 'GoogleSearch' in search_tools: search_tool_name_main = 'GoogleSearch'

            # Формирование задачи в зависимости от доступных инструментов
            if search_available and browser_core_available and extraction_available:
                logger.info('Формируем СЛОЖНУЮ задачу.'); 
                product_category = 'Электрические зубные щетки'; num_links_str = 'одну'
                task_to_run = f'''**Роль:** Веб-Агент. **Цель:** Найти {num_links_str} URL товаров ('{product_category}') через {search_tool_name_main}, перейти, извлечь JSON (Шаблон 1). **План:** 1. `{search_tool_name_main}` -> 2. `BrowserNavigate` -> 3. `BrowserScrapeHTML` -> 4. `ExtractProductSchema` -> 5. `BrowserScrapeText` -> 6. Верни JSON (Шаблон 1). **Шаблон 1:** {{..., "webpage_type": "product", "data": {{ "name": "<EN Name/N/A>", ..., "raw": "<Original Text>" }} }}'''
            elif search_available: 
                logger.info('Формируем задачу ТОЛЬКО для поиска.'); 
                search_query = 'Последние новости AI'
                task_to_run = f'Используй {search_tool_name_main} для поиска: "{search_query}".'
            else: 
                logger.warning('Ключевые инструменты недоступны.'); 
                task_to_run = 'Что такое рекурсия?' # Простая задача, не требующая инструментов

            # Оценка количества токенов для задачи (если задача сформирована)
            if task_to_run:
                print(f'\nЗадача:\n{"-"*20}\n{task_to_run}\n{"-"*20}'); print("\n--- Оценка токенов ---")
                if driver.gemini: 
                    try: 
                        print(f"Gemini ~ {driver.gemini.get_num_tokens(task_to_run)} ток.") 
                    except Exception: 
                        # Ошибки get_num_tokens игнорируются
                        ...
                if driver.openai: 
                    try: 
                        print(f"OpenAI ~ {driver.openai.get_num_tokens(task_to_run)} ток.") 
                    except Exception: 
                        # Ошибки get_num_tokens игнорируются
                        ...
                print("-" * 30)
            else: 
                logger.error('Не удалось сформировать задачу.'); return

            print('\n' + '='*15 + ' Запуск run_task ' + '='*15)
            # Формирование списка LLM для тестирования
            llm_to_test_run = []
            if driver.gemini and Config.GEMINI_STATUS.lower() == 'active': llm_to_test_run.append(('Gemini', True))
            if driver.openai and Config.OPENAI_API_STATUS.lower() == 'active': llm_to_test_run.append(('OpenAI', False))
            
            # Проверка, есть ли активные LLM для тестирования
            if not llm_to_test_run: 
                print('[!] Нет АКТИВНЫХ LLM.'); return

            # Запуск задачи с каждой активной LLM
            for name_llm, flag_use_gemini in llm_to_test_run:
                print(f'\n--- Запуск run_task с {name_llm} ---'); 
                start_time = asyncio.get_event_loop().time() # Засекаем время начала
                try:
                    # Выполнение задачи
                    result = await driver.run_task(task_to_run, use_gemini=flag_use_gemini)
                    end_time = asyncio.get_event_loop().time() # Засекаем время окончания
                    print(f'\n[Результат ({name_llm}) - {end_time - start_time:.2f} сек]:')
                    try: # Попытка красивого вывода JSON
                        if isinstance(result, str) and (result.strip().startswith('[') or result.strip().startswith('{')): 
                            parsed_result = json.loads(result); print(parsed_result)
                        elif isinstance(result, str) and result.startswith('Ошибка:'): 
                            print(f'[!] {result}') # Вывод сообщения об ошибке
                        else: 
                            print(result if result is not None else '[!] Нет ответа.')
                    except Exception: 
                        # Если не удалось распарсить как JSON или другая ошибка вывода
                        print(result if result is not None else '[!] Нет ответа.')
                        ... # Игнорирование ошибки вывода
                        
                except Exception as ex: 
                    # Обработка ошибок при выполнении run_task
                    end_time = asyncio.get_event_loop().time()
                    print(f'\n[!!!] Ошибка ({name_llm}): {ex} ({end_time - start_time:.2f} сек)')
                    logger.error(f'Ошибка run_task ({name_llm})', ex, exc_info=True)
                    ... # Игнорирование ошибки для продолжения с другими LLM, если есть
        else:
            logger.error("Экземпляр Driver не был успешно инициализирован (driver is None).")

    finally: 
        # Гарантированное закрытие драйвера в конце работы
        if driver: await driver.close() 
        logger.info('='*20 + ' Завершение работы main ' + '='*20)

if __name__ == '__main__':
    print('Запуск основной асинхронной функции main...')
    print("Напоминание: Установлены ли playwright, beautifulsoup4, lxml, langchain*, google-search-results, duckduckgo-search, python-dotenv, google-api-core, tavily-python?")
    print("Выполнен ли 'playwright install'?")
    print("-" * 40)
    # Запуск асинхронной функции main
    asyncio.run(main())
    print('Программа завершена.')
