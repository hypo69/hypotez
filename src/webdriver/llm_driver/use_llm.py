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
- Установки API ключей.
- Асинхронной инициализации контроллеров (браузер, извлечение данных, формы и т.д.).
- Создания инструментов LangChain для контроллеров (включая асинхронные).
- Запуска задачи с использованием LLM и доступных инструментов.
- Выполнения задачи до конечного результата (`run_task`).
- Стриминга выполнения задачи (`stream_task`).

Зависимости:
    - langchain-openai, langchain-google-genai, langchain-core, langchainhub, langchain
    - langchain-community (для SerpAPIWrapper, DuckDuckGoSearchRun)
    - google-search-results (для SerpAPIWrapper)
    - duckduckgo-search (для DuckDuckGoSearchRun)
    - google-api-core (для обработки ошибок квоты)
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
from langchain_community.utilities import SerpAPIWrapper
from langchain_core.exceptions import LangChainException
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
# --- Исключения Google API ---
from google.api_core import exceptions as google_api_exceptions

# --- Внутренние модули ---
import header # pylint: disable=unused-import # Импортируется для сайд-эффектов (sys.path)
# Импорт __root__ для корректных относительных путей проекта
from header import __root__
# from src import gs # Импортируется в Config
from src.logger import logger # Настроенный логгер проекта
from src.utils.jjson import j_loads_ns # Утилиты для работы с JSON
# Кастомная функция print для форматированного вывода
from src.utils.printer import pprint as print

# --- ИМПОРТ АСИНХРОННЫХ КОНТРОЛЛЕРОВ ---
# Важно: Проверьте правильность этого пути!
CONTROLLERS_MODULE_PATH: str = 'src.webdriver.llm_driver.controllers'
BROWSER_CONTROLLER_AVAILABLE: bool = False # Инициализация флагов
BS4_AVAILABLE: bool = False
try:
    # Импорт всех необходимых контроллеров из модуля controllers
    # pylint: disable=import-error
    from src.webdriver.llm_driver.controllers import (
        BS4_AVAILABLE,  # Импортируем флаг доступности BS4
        BrowserController,  # Async версия
        DataExtractionController,
        DownloadController,  # Async методы
        FormController,  # Async методы
        JavaScriptExecutionController,  # Async методы
        ScreenshotController,  # Async методы
        StateManager  # Async методы
    )
    # Флаг для индикации доступности ОСНОВНОГО контроллера
    BROWSER_CONTROLLER_AVAILABLE = True
    logger.info(f'Асинхронные контроллеры успешно импортированы из {CONTROLLERS_MODULE_PATH}.')
except ImportError as import_ex:
    logger.error(f'КРИТИЧЕСКАЯ ОШИБКА: Не удалось импортировать контроллеры из {CONTROLLERS_MODULE_PATH}. Браузерные инструменты НЕ БУДУТ доступны.', import_ex, exc_info=True)
    # Использование заглушки ТОЛЬКО для BrowserController
    class BrowserController: # type: ignore
        """ Заглушка BrowserController на случай ошибки импорта реального класса. """
        _is_started: bool = False # Добавляем флаг для заглушки
        def __init__(self, *args: Any, **kwargs: Any) -> None: logger.debug('Инициализирован ЗАГЛУШКА BrowserController.', exc_info=False)
        async def start(self) -> bool: logger.error('Заглушка BrowserController: start не реализован.'); return False # Async заглушка
        async def navigate(self, u: str) -> str: return f'Ошибка: Заглушка BrowserController, не могу перейти на {u}.'
        async def scrape_text(self, s: Optional[str]=None) -> str: return 'Ошибка: Заглушка BrowserController, не могу получить текст.'
        async def scrape_html(self, s: Optional[str]=None) -> str: return 'Ошибка: Заглушка BrowserController, не могу получить HTML.'
        async def click_element(self, s: str) -> str: return f'Ошибка: Заглушка BrowserController, не могу кликнуть {s}.'
        def get_current_url(self) -> str: return 'Ошибка: Заглушка BrowserController.'
        async def close(self) -> None: logger.debug('Вызван метод close ЗАГЛУШКИ BrowserController.', exc_info=False); pass
    # Устанавливаем флаги как False
    BROWSER_CONTROLLER_AVAILABLE = False
    BS4_AVAILABLE = False # Если контроллеры не импортировались, то и BS4 скорее всего тоже
# --- КОНЕЦ ИМПОРТА КОНТРОЛЛЕРОВ ---

# Загрузка переменных окружения из .env файла
from dotenv import load_dotenv
dotenv_path: Path = __root__ / '.env'
if dotenv_path.exists():
    load_dotenv(dotenv_path=dotenv_path)
    logger.info(f'Загружены переменные окружения из: {dotenv_path}')
else:
    logger.warning(f'.env файл не найден по пути: {dotenv_path}.')


# Определяем псевдоним типа для конфигурации
ConfigType: TypeAlias = Optional[SimpleNamespace]

class Config:
    """
    Класс для хранения статической конфигурации приложения.

    Загружает конфигурацию из JSON-файла, определяет API ключи,
    статусы и имена моделей для LLM и API поиска.
    Использует безопасный доступ к полям конфигурации с fallback-значениями.
    """
    # Путь к директории с файлом конфигурации
    ENDPOINT: Path = __root__ / 'src' / 'webdriver' / 'llm_driver'
    # Переменная для хранения загруженной конфигурации
    config: ConfigType = None

    # --- ЗАГРУЗКА КОНФИГА ---
    try:
        config_path: Path = ENDPOINT / 'use_llm.json'
        if config_path.exists():
            config = j_loads_ns(config_path) # Используем вашу функцию
            if not config: logger.error(f'Файл конфигурации {config_path} загружен, но пуст или некорректен!')
            else: logger.info(f'Конфигурация успешно загружена из {config_path}')
        else: logger.error(f'КРИТИЧЕСКАЯ ОШИБКА: Файл конфигурации НЕ НАЙДЕН: {config_path}!'); config = None
    except Exception as ex: logger.error(f'КРИТИЧЕСКАЯ ОШИБКА при загрузке/парсинге {config_path}.', ex, exc_info=True); config = None

    # --- ИНИЦИАЛИЗАЦИЯ АТРИБУТОВ КЛАССА ---
    GEMINI_API_KEY: Optional[str] = None; OPENAI_API_KEY: Optional[str] = None; SERPAPI_API_KEY: Optional[str] = None
    GEMINI_STATUS: str = 'inactive'; GEMINI_MODEL_NAME: str = ''
    OPENAI_API_STATUS: str = 'inactive'; OPENAI_MODEL_NAME: str = ''

    # Попытка чтения статусов и моделей из config с fallback
    try:
        if config and hasattr(config, 'models'):
            gemini_config = getattr(config.models, 'gemini', None); GEMINI_STATUS = getattr(gemini_config, 'status', 'inactive') if gemini_config else 'inactive'; GEMINI_MODEL_NAME = getattr(gemini_config, 'model_name', '') if gemini_config else ''
            openai_config = getattr(config.models, 'openai', None); OPENAI_API_STATUS = getattr(openai_config, 'status', 'inactive') if openai_config else 'inactive'; OPENAI_MODEL_NAME = getattr(openai_config, 'model_name', '') if openai_config else ''
        else: logger.warning('Config не загружен или нет секции "models". Используются статусы "inactive".')
    except AttributeError as ex: logger.critical(f'Ошибка чтения статуса/модели из config: {ex}', exc_info=False)
    # --- КОНЕЦ ИНИЦИАЛИЗАЦИИ АТРИБУТОВ ---

    # --- Установка API ключей ---
    try:
        from src import gs as project_gs # Импорт gs
        try: GEMINI_API_KEY = project_gs.credentials.gemini.katia.api_key # ПРОВЕРЬТЕ ИМЯ ПОЛЬЗОВАТЕЛЯ!
        except AttributeError: logger.warning('GEMINI_API_KEY не найден в gs', exc_info=False)
        try: OPENAI_API_KEY = project_gs.credentials.openai.hypotez.api_key
        except AttributeError: logger.warning('OPENAI_API_KEY не найден в gs', exc_info=False)
        try: SERPAPI_API_KEY = project_gs.credentials.serpapi.onela.api_key
        except AttributeError: logger.warning('SERPAPI_API_KEY не найден в gs', exc_info=False)
        if not GEMINI_API_KEY: GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
        if not OPENAI_API_KEY: OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
        if not SERPAPI_API_KEY: SERPAPI_API_KEY = os.environ.get('SERPAPI_API_KEY')
        if GEMINI_API_KEY: os.environ['GOOGLE_API_KEY'] = GEMINI_API_KEY
        if OPENAI_API_KEY: os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
        if SERPAPI_API_KEY: os.environ['SERPAPI_API_KEY'] = SERPAPI_API_KEY
        logger.info(f'Config Gemini: Status={GEMINI_STATUS}, Model={GEMINI_MODEL_NAME}, Key Present={bool(GEMINI_API_KEY)}')
        logger.info(f'Config OpenAI: Status={OPENAI_API_STATUS}, Model={OPENAI_MODEL_NAME}, Key Present={bool(OPENAI_API_KEY)}')
        logger.info(f'Config SerpAPI: Key Present={bool(SERPAPI_API_KEY)}')
    except ImportError: logger.warning("Модуль 'src.gs' не найден.")
    except NameError: logger.warning("Объект 'gs.credentials' не найден.")
    except Exception as ex: logger.error('Ошибка при установке API ключей в Config.', ex, exc_info=True)

# ===============================================================
# Функция стриминга
# ===============================================================
async def stream_agent_execution( executor: AgentExecutor, task_input: Dict[str, Any]) -> Tuple[Optional[str], List[Dict[str, Any]]]:
    """
    Асинхронно выполняет агент через AgentExecutor и стримит шаги выполнения.

    Args:
        executor (AgentExecutor): Исполнитель агента LangChain.
        task_input (Dict[str, Any]): Входные данные для задачи агента (обычно {'input': '...'}).

    Returns:
        Tuple[Optional[str], List[Dict[str, Any]]]: Кортеж, содержащий:
            - Финальный ответ агента (строка) или None.
            - Список всех чанков (словарей), полученных во время стриминга.
    """
    # Объявление переменных
    final_answer: Optional[str] = None
    all_chunks: List[Dict[str, Any]] = []
    run_id: Optional[str] = None
    current_run_info: Dict[str, Any]
    current_run_id: Optional[str]
    chunk: Dict[str, Any]
    actions: Optional[List[Any]]; action: Any; tool: str; tool_input: Any; log_msg: str
    steps: Optional[List[Any]]; step: Any; observation: Any; action_log: str; tool_used: str
    output: Optional[str]; messages: Optional[List[Any]]; msg: Any; content: Optional[str]

    logger.info(f'--- Начало стриминга для входа: {str(task_input)[:200]}... ---')
    try:
        # Асинхронный цикл по чанкам
        async for chunk in executor.astream(task_input):
            all_chunks.append(chunk)
            # Обработка планируемых действий
            if actions := chunk.get('actions'):
                for action in actions:
                    tool = getattr(action, 'tool', 'N/A')
                    tool_input = getattr(action, 'tool_input', 'N/A')
                    log_msg = getattr(action, 'log', '').strip()
                    logger.info(f"Планируемое действие: Tool=[{tool}], Input=[{str(tool_input)[:100]}...]")
                    if log_msg: logger.debug(f'  Log (Мысли): {log_msg}', exc_info=False)
            # Обработка выполненных шагов
            elif steps := chunk.get('steps'):
                for step in steps:
                    observation = getattr(step, 'observation', None)
                    action_log = getattr(step.action, 'log', '').strip()
                    tool_used = getattr(step.action, 'tool', 'N/A')
                    if observation is not None:
                        logger.info(f"Результат действия (Observation) от Tool=[{tool_used}]: {str(observation)[:300]}...")
                        if action_log: logger.debug(f"  Log (Мысли перед Observation): {action_log}", exc_info=False)
                    else: logger.debug(f'Получен шаг от Tool=[{tool_used}] без observation: {step}', exc_info=False)
            # Обработка финального ответа
            elif output := chunk.get('output'):
                logger.info(f'Финальный ответ: {output}')
                final_answer = output
            # Обработка сообщений (менее релевантно для ReAct)
            elif messages := chunk.get('messages'):
                 for msg in messages:
                     if content := getattr(msg, 'content', None):
                         logger.debug(f'Message Chunk: {content}', exc_info=False)
            # Обновление ID запуска
            current_run_info = chunk.get('__run', {})
            current_run_id = getattr(current_run_info, 'id', None)
            if current_run_id and current_run_id != run_id:
                run_id = current_run_id; logger.debug(f'Agent Run ID: {run_id}', exc_info=False)
    # Обработка исключений
    except LangChainException as ex: logger.error('Ошибка LangChain во время стриминга.', ex, exc_info=True)
    except Exception as ex: logger.error('Неожиданная ошибка во время стриминга.', ex, exc_info=True)
    logger.info(f'--- Стриминг завершен. Всего чанков: {len(all_chunks)}. ---')
    return final_answer, all_chunks
# ===============================================================


class Driver:
    """
    Класс для управления LLM, асинхронными контроллерами и агентами LangChain.
    """
    # Ссылка на класс конфигурации
    config_class: Type[Config] = Config

    # Экземпляры LLM
    gemini: Optional[BaseChatModel] = None
    openai: Optional[BaseChatModel] = None

    # Список инструментов LangChain
    tools: List[Tool] = []

    # Экземпляры контроллеров
    browser: Optional[BrowserController] = None
    # Экземпляр SerpAPIWrapper создается внутри инструмента
    data_extractor: Optional[DataExtractionController] = None
    form_controller: Optional[FormController] = None
    screenshot_controller: Optional[ScreenshotController] = None
    download_controller: Optional[DownloadController] = None
    js_executor: Optional[JavaScriptExecutionController] = None
    state_manager: Optional[StateManager] = None

    # Флаг для отслеживания асинхронной инициализации
    _initialized: bool = False
    # Сохраняем ключ SerpAPI для использования в инструменте
    _serpapi_key: Optional[str] = None
    # Параметры для инициализации браузера
    _start_browser: bool
    _browser_headless: bool
    _browser_timeout: int

    def __init__(self,
                 GEMINI_API_KEY: Optional[str] = None,
                 OPENAI_API_KEY: Optional[str] = None,
                 SERPAPI_API_KEY: Optional[str] = None,
                 openai_model_name: Optional[str] = None,
                 gemini_model_name: Optional[str] = None,
                 start_browser: bool = True,
                 browser_headless: bool = True,
                 browser_timeout: int = 30000,
                 **kwargs: Any) -> None:
        """
        Синхронно инициализирует LLM и сохраняет параметры для асинхронной инициализации.
        Для полной инициализации необходимо вызвать `await driver.async_init()`.

        Args:
            GEMINI_API_KEY (Optional[str]): Ключ API для Google Gemini. По умолчанию None.
            OPENAI_API_KEY (Optional[str]): Ключ API для OpenAI. По умолчанию None.
            SERPAPI_API_KEY (Optional[str]): Ключ API для SerpAPI. По умолчанию None.
            openai_model_name (Optional[str]): Имя модели OpenAI. По умолчанию None.
            gemini_model_name (Optional[str]): Имя модели Gemini. По умолчанию None.
            start_browser (bool): Пытаться ли инициализировать браузер. По умолчанию True.
            browser_headless (bool): Режим запуска браузера. По умолчанию True.
            browser_timeout (int): Таймаут браузера в мс. По умолчанию 30000.
            **kwargs (Any): Дополнительные неиспользуемые аргументы.
        """
        # Объявление локальных переменных __init__
        openai_api_key_to_use: Optional[str]
        gemini_api_key_to_use: Optional[str]
        openai_model_to_use: str
        gemini_model_to_use: str
        openai_status: str
        gemini_status: str

        logger.info('--- Начало СИНХРОННОЙ инициализации Driver ---')
        # Сохранение параметров для асинхронной инициализации
        self._start_browser = start_browser
        self._browser_headless = browser_headless
        self._browser_timeout = browser_timeout
        self._serpapi_key = SERPAPI_API_KEY or self.config_class.SERPAPI_API_KEY
        self._initialized = False # Флаг инициализации

        # Обнуление атрибутов при создании экземпляра
        self.openai = None; self.gemini = None; self.tools = []
        self.browser = None; self.data_extractor = None; self.form_controller = None
        self.screenshot_controller = None; self.download_controller = None
        self.js_executor = None; self.state_manager = None

        # --- Получение ключей, моделей, статусов из Config ---
        openai_api_key_to_use = OPENAI_API_KEY or self.config_class.OPENAI_API_KEY
        gemini_api_key_to_use = GEMINI_API_KEY or self.config_class.GEMINI_API_KEY
        openai_model_to_use = openai_model_name or self.config_class.OPENAI_MODEL_NAME
        gemini_model_to_use = gemini_model_name or self.config_class.GEMINI_MODEL_NAME
        openai_status = self.config_class.OPENAI_API_STATUS
        gemini_status = self.config_class.GEMINI_STATUS

        # --- Обновление переменных окружения ---
        if gemini_api_key_to_use: os.environ['GOOGLE_API_KEY'] = gemini_api_key_to_use
        if openai_api_key_to_use: os.environ['OPENAI_API_KEY'] = openai_api_key_to_use
        if self._serpapi_key: os.environ['SERPAPI_API_KEY'] = self._serpapi_key

        # --- Синхронная инициализация LLM ---
        self.openai = self._initialize_openai(openai_api_key_to_use, openai_status, openai_model_to_use)
        self.gemini = self._initialize_gemini(gemini_api_key_to_use, gemini_status, gemini_model_to_use)

        if kwargs: logger.warning(f'Неиспользованные аргументы: {kwargs}', exc_info=False)
        logger.info('--- Синхронная инициализация Driver завершена. Вызовите async_init() ---')

    async def async_init(self) -> bool:
        """
        Асинхронно инициализирует BrowserController, зависимые контроллеры и инструменты.
        Должен быть вызван с `await` после создания экземпляра Driver.

        Returns:
            bool: True если инициализация прошла успешно, иначе False.
        """
        # Предотвращение повторной инициализации
        if self._initialized:
             logger.info('Driver уже инициализирован асинхронно.')
             return True

        logger.info('--- Начало АСИНХРОННОЙ инициализации Driver ---')
        self.tools = [] # Очистка списка инструментов перед заполнением

        # Асинхронная инициализация браузера и контроллеров
        await self._async_initialize_browser_and_controllers(
            start=self._start_browser,
            headless=self._browser_headless,
            timeout=self._browser_timeout
        )

        # Создание инструментов (теперь использует self._serpapi_key)
        self._create_tools()

        logger.info(f'Итоговый список доступных инструментов Driver: {[tool.name for tool in self.tools]}')
        self._initialized = True # Установка флага успешной инициализации
        logger.info('--- Асинхронная инициализация Driver завершена ---')
        return True

    # --- Вспомогательные методы для инициализации ---
    def _initialize_openai(self, api_key: Optional[str], status: str, model_name: str) -> Optional[BaseChatModel]:
        """ Синхронно инициализирует модель OpenAI. """
        llm: Optional[BaseChatModel] = None
        if api_key and status.lower() == 'active' and model_name:
            logger.info(f'Инициализация OpenAI: Model={model_name}')
            try: llm = ChatOpenAI(model_name=model_name, openai_api_key=api_key, temperature=0.1); logger.info('OpenAI LLM инициализирован.')
            except Exception as ex: logger.error('Ошибка инициализации OpenAI.', ex, exc_info=True)
        else: logger.warning(f'OpenAI LLM не инициализирован (Key={bool(api_key)}, Status={status}, Model={model_name})', exc_info=False)
        return llm

    def _initialize_gemini(self, api_key: Optional[str], status: str, model_name: str) -> Optional[BaseChatModel]:
        """ Синхронно инициализирует модель Gemini. """
        llm: Optional[BaseChatModel] = None
        if api_key and status.lower() == 'active' and model_name:
            logger.info(f'Инициализация Gemini: Model={model_name}')
            os.environ['GOOGLE_API_KEY'] = api_key
            try: llm = ChatGoogleGenerativeAI(model=model_name, google_api_key=api_key, temperature=0.1, convert_system_message_to_human=True); logger.info('Gemini LLM инициализирован.')
            except Exception as ex: logger.error('Ошибка инициализации Gemini.', ex, exc_info=True)
        else: logger.warning(f'Gemini LLM не инициализирован (Key={bool(api_key)}, Status={status}, Model={model_name})', exc_info=False)
        return llm

    async def _async_initialize_browser_and_controllers(self, start: bool, headless: bool, timeout: int) -> None:
        """ Асинхронно инициализирует BrowserController и зависимые контроллеры. """
        # Обнуление контроллеров
        self.browser = None; self.data_extractor = None; self.form_controller = None; self.screenshot_controller = None; self.download_controller = None; self.js_executor = None; self.state_manager = None
        browser_started: bool = False

        if not start: logger.info('Инициализация браузера пропущена (start=False).'); return
        if not BROWSER_CONTROLLER_AVAILABLE: logger.warning('BrowserController недоступен.', exc_info=False); return

        try:
            logger.info('Асинхронная инициализация BrowserController...')
            self.browser = BrowserController(headless=headless, timeout=timeout)
            browser_started = await self.browser.start() # Асинхронный запуск
            if not browser_started: logger.error('Не удалось запустить BrowserController!'); self.browser = None; return
            logger.info('BrowserController асинхронно инициализирован.')

            # Инициализация зависимых контроллеров
            if self.browser and self.browser.page and self.browser.context:
                logger.info('Инициализация зависимых контроллеров...')
                if BS4_AVAILABLE:
                    try: self.data_extractor = DataExtractionController(); logger.info('DataExtractionController иниц.')
                    except Exception as ex: logger.warning(f'Ошибка init DataExtractionController: {ex}', exc_info=False)
                else: logger.warning('BS4 недоступен, DataExtractionController не иниц.')
                try: self.form_controller = FormController(page=self.browser.page); logger.info('FormController иниц.')
                except Exception as ex: logger.warning(f'Ошибка init FormController: {ex}', exc_info=False)
                try: self.screenshot_controller = ScreenshotController(page=self.browser.page); logger.info('ScreenshotController иниц.')
                except Exception as ex: logger.warning(f'Ошибка init ScreenshotController: {ex}', exc_info=False)
                try: self.download_controller = DownloadController(page=self.browser.page); logger.info('DownloadController иниц.')
                except Exception as ex: logger.warning(f'Ошибка init DownloadController: {ex}', exc_info=False)
                try: self.js_executor = JavaScriptExecutionController(page=self.browser.page); logger.info('JavaScriptExecutionController иниц.')
                except Exception as ex: logger.warning(f'Ошибка init JavaScriptExecutionController: {ex}', exc_info=False)
                try: self.state_manager = StateManager(context=self.browser.context, page=self.browser.page); logger.info('StateManager иниц.')
                except Exception as ex: logger.warning(f'Ошибка init StateManager: {ex}', exc_info=False)
            else: logger.error('BrowserController page/context недоступны!')
        except Exception as ex:
            logger.error('Ошибка при асинхронной инициализации BrowserController.', ex, exc_info=True)
            if self.browser: await self.browser.close()
            self.browser = None

    def _create_tools(self) -> None:
        """
        Создает инструменты LangChain для всех инициализированных контроллеров.
        Для асинхронных методов используется `coroutine`.
        """
        logger.info('Создание инструментов LangChain...')
        self.tools = [] # Начинаем с чистого списка

        # Общая функция-заглушка
        def _sync_error_func(*args: Any, **kwargs: Any) -> str:
            return 'Ошибка: Этот инструмент требует асинхронного выполнения (use coroutine).'

        # 1. Инструмент "Умный Поиск"
        if self._serpapi_key:
            # Асинхронная функция поиска с fallback
            async def _smart_search_async(query: str) -> str:
                search_result: str = ''; loop: asyncio.AbstractEventLoop
                serp_error_text: str = 'Got error from SerpAPI'; no_results_text: str = 'returned any results'
                try: # Попытка SerpAPI
                    logger.debug(f"SmartSearch: Попытка SerpAPI: '{query[:100]}...'")
                    serp_api_wrapper = SerpAPIWrapper(); loop = asyncio.get_running_loop()
                    search_result = await loop.run_in_executor(None, serp_api_wrapper.run, query)
                    logger.debug("SmartSearch: Успех SerpAPI."); return search_result
                except ValueError as ex_val:
                    if serp_error_text in str(ex_val) and no_results_text in str(ex_val): logger.warning(f"SmartSearch: Google не вернул рез-тов для '{query[:100]}...'. Fallback DDG.");
                    else: logger.error(f"SmartSearch: ValueError от SerpAPI: {ex_val}", exc_info=False); return f"Ошибка Google: {ex_val}"
                except Exception as ex_serp: logger.error("SmartSearch: Ошибка SerpAPI.", ex_serp, exc_info=True); return f"Ошибка Google: {ex_serp}"
                # Попытка DuckDuckGo
                try:
                    logger.debug(f"SmartSearch: Попытка DuckDuckGo: '{query[:100]}...'")
                    ddg_search = DuckDuckGoSearchRun(); loop = asyncio.get_running_loop()
                    search_result = await loop.run_in_executor(None, ddg_search.run, query)
                    logger.debug("SmartSearch: Успех DuckDuckGo."); return search_result
                except Exception as ex_ddg: logger.error("SmartSearch: Ошибка DuckDuckGo.", ex_ddg, exc_info=True); return f"Ошибка: Поиск не дал результатов. Ошибка DDG: {ex_ddg}"

            smart_search_tool = Tool( name='SmartSearch', func=_sync_error_func, coroutine=_smart_search_async, description='Поиск в интернете (Google с fallback на DuckDuckGo). Вход: запрос. Выход: сводка.')
            self.tools.append(smart_search_tool); logger.debug('Инструмент SmartSearch создан.')
        else: # Fallback только на DuckDuckGo
            logger.warning('SERPAPI_API_KEY не найден. Используем только DuckDuckGo.')
            try:
                ddg_search = DuckDuckGoSearchRun()
                ddg_tool = Tool(name="DuckDuckGoSearch", func=ddg_search.run, description="Поиск в интернете (DuckDuckGo). Вход: запрос. Выход: сводка.")
                self.tools.append(ddg_tool); logger.debug('Инструмент DuckDuckGoSearch создан.')
            except Exception as ex_ddg_only: logger.error(f"Не удалось создать DuckDuckGoSearch: {ex_ddg_only}", exc_info=True)

        # 2. BrowserController Tools
        if self.browser:
            async def _nav_async(url: str) -> str: return await self.browser.navigate(url) if self.browser else 'Err:BrowserNA'
            async def _st_async(s: Optional[str]=None) -> str: return await self.browser.scrape_text(s) if self.browser else 'Err:BrowserNA'
            async def _sh_async(s: Optional[str]=None) -> str: return await self.browser.scrape_html(s) if self.browser else 'Err:BrowserNA'
            async def _ce_async(s: str) -> str: return await self.browser.click_element(s) if self.browser else 'Err:BrowserNA'
            def _gu_sync(tool_input: Any = None) -> str: return self.browser.get_current_url() if self.browser else 'Err:BrowserNA' # ИЗМЕНЕНО: добавлен tool_input
            browser_tools: List[Tool] = [ Tool(name='BrowserNavigate', func=_sync_error_func, coroutine=_nav_async, description='Переход по URL. Вход: URL.'), Tool(name='BrowserScrapeText', func=_sync_error_func, coroutine=_st_async, description='Извлечение текста (опц. селектор).'), Tool(name='BrowserScrapeHTML', func=_sync_error_func, coroutine=_sh_async, description='Извлечение HTML (опц. селектор).'), Tool(name='BrowserClickElement', func=_sync_error_func, coroutine=_ce_async, description='Клик по элементу (селектор).'), Tool(name='GetCurrentURL', func=_gu_sync, description='Получить текущий URL.') ]
            self.tools.extend(browser_tools); logger.debug(f'Добавлено {len(browser_tools)} инструментов BrowserController.')
        else: logger.warning('Инструменты BrowserController не созданы.')

        # 3. DataExtractionController Tools (Синхронные)
        if self.data_extractor:
            # Обертка для _fl_sync с обработкой ошибок аргументов
            def _find_links_wrapper(p: Any) -> Union[List[str], Dict[str, str]]:
                if not isinstance(p, dict):
                    logger.error("FindPageLinks: Ошибка ввода - ожидался словарь.", exc_info=False)
                    return {'error': 'Err:BadInput - Expected a dictionary.'}
                if 'html' not in p:
                    logger.error("FindPageLinks: Ошибка ввода - отсутствует ключ 'html'.", exc_info=False)
                    return {'error': 'Err:NoHTML - Missing "html" key.'}
                # base_url необязателен, но лучше его передать
                if 'base_url' not in p:
                     logger.warning("FindPageLinks: Ключ 'base_url' отсутствует, будут использоваться относительные URL из HTML или текущий URL браузера.", exc_info=False)

                try:
                    base_url = p.get('base_url') or (self.browser.get_current_url() if self.browser else None)
                    # Убедимся, что data_extractor существует перед вызовом
                    if self.data_extractor:
                         return self.data_extractor.find_links(p['html'], base_url)
                    else:
                         logger.error("FindPageLinks: Экземпляр DataExtractionController отсутствует.")
                         return {'error': 'Err:ExtractorNA - DataExtractor not initialized.'}
                except Exception as ex:
                    logger.error(f"FindPageLinks: Неожиданная ошибка при извлечении ссылок.", ex, exc_info=True)
                    return {'error': f'Err:Exception - {str(ex)}'}

            extraction_tools: List[Tool] = [
                Tool(name='ExtractProductSchema', func=lambda html: self.data_extractor.extract_product_details(html) if self.data_extractor else 'Err:ExtractorNA', description='Извлечение схемы товара из HTML.'),
                Tool(name='ExtractContactInfo', func=lambda text: self.data_extractor.extract_contact_info(text) if self.data_extractor else 'Err:ExtractorNA', description='Извлечение контактов из текста.'),
                Tool(name='FindPageLinks', func=_find_links_wrapper, description="Поиск ссылок в HTML. Вход: {'html': '...', 'base_url': 'url'(opt)}."), # Используем обертку
            ]
            self.tools.extend(extraction_tools); logger.debug(f'Добавлено {len(extraction_tools)} инструментов DataExtraction.')
        else: logger.warning('Инструменты DataExtractionController не созданы.')

        # 4. FormController Tools (Асинхронные)
        if self.form_controller:
            async def _fff_async(p: Dict[str, Any]) -> str: return await self.form_controller.fill_input_field(p['selector'], p['value']) if self.form_controller and isinstance(p, dict) else 'Err:FormNA/BadInput'
            async def _sdd_async(p: Dict[str, Any]) -> str: return await self.form_controller.select_dropdown_option(p['selector'], value=p.get('value'), label=p.get('label')) if self.form_controller and isinstance(p, dict) else 'Err:FormNA/BadInput'
            async def _sf_async(p: Dict[str, Any]) -> str: return await self.form_controller.submit_form(form_selector=p.get('form_selector'), submit_button_selector=p.get('submit_button_selector')) if self.form_controller and isinstance(p, dict) else 'Err:FormNA/BadInput'
            form_tools: List[Tool] = [ Tool(name='FillFormField', func=_sync_error_func, coroutine=_fff_async, description="Заполнение поля. Вход: {'selector': 'css', 'value': 'text'}."), Tool(name='SelectDropdown', func=_sync_error_func, coroutine=_sdd_async, description="Выбор опции. Вход: {'selector': 'css', 'value': 'v'}/{'label': 'l'}."), Tool(name='SubmitForm', func=_sync_error_func, coroutine=_sf_async, description="Отправка формы. Вход: {'form_selector': 'css'} / {'submit_button_selector': 'css'}."), ]
            self.tools.extend(form_tools); logger.debug(f'Добавлено {len(form_tools)} инструментов FormController.')
        else: logger.warning('Инструменты FormController не созданы.')

        # 5. ScreenshotController Tools (Асинхронные)
        if self.screenshot_controller:
            async def _ss_async(p: Dict[str, Any]) -> str: return await self.screenshot_controller.take_screenshot(p['save_path'], full_page=p.get('full_page', True), selector=p.get('selector')) if self.screenshot_controller and isinstance(p, dict) else 'Err:ScreenshotNA/BadInput'
            self.tools.append(Tool(name='TakeScreenshot', func=_sync_error_func, coroutine=_ss_async, description="Скриншот. Вход: {'save_path': 'path', 'full_page': bool(opt), 'selector': 'css'(opt)}."))
            logger.debug('Инструмент TakeScreenshot добавлен.')
        else: logger.warning('Инструмент TakeScreenshot не создан.')

        # 6. DownloadController Tools (Асинхронные)
        if self.download_controller:
            async def _dl_async(p: Dict[str, Any]) -> str: return await self.download_controller.click_and_download(p['click_selector'], p['save_directory'], timeout=p.get('timeout', 60000)) if self.download_controller and isinstance(p, dict) else 'Err:DownloadNA/BadInput'
            self.tools.append(Tool(name='ClickAndDownload', func=_sync_error_func, coroutine=_dl_async, description="Клик для скачивания. Вход: {'click_selector': 'css', 'save_directory': 'path', 'timeout': ms(opt)}."))
            logger.debug('Инструмент ClickAndDownload добавлен.')
        else: logger.warning('Инструмент ClickAndDownload не создан.')

        # 7. JavaScriptExecutionController Tools (Асинхронные)
        if self.js_executor:
            async def _ejs_async(s: str) -> Union[str, Any]: return await self.js_executor.execute_script(s) if self.js_executor else 'Err:JsExecNA'
            self.tools.append(Tool(name='ExecuteJavaScript', func=_sync_error_func, coroutine=_ejs_async, description="Выполнение JS (ОСТОРОЖНО!). Вход: строка JS кода."))
            logger.debug('Инструмент ExecuteJavaScript добавлен.')
        else: logger.warning('Инструмент ExecuteJavaScript не создан.')

        # 8. StateManager Tools (Асинхронные/Синхронные)
        if self.state_manager:
            async def _gc_async(u: Optional[str]=None) -> Union[List[Dict[str, Any]], str]: return await self.state_manager.get_cookies(u) if self.state_manager else 'Err:StateNA'
            async def _cc_async() -> str: return await self.state_manager.clear_cookies() if self.state_manager else 'Err:StateNA'
            async def _cs_async() -> str: return await self.state_manager.clear_storage() if self.state_manager else 'Err:StateNA'
            def _l_sync(*a: Any, **kw: Any) -> str: return self.state_manager.login(*a, **kw) if self.state_manager else 'Err:StateNA'
            state_tools: List[Tool] = [ Tool(name='GetCookies', func=_sync_error_func, coroutine=_gc_async, description="Получение cookies. Вход: опц. URL."), Tool(name='ClearCookies', func=_sync_error_func, coroutine=_cc_async, description="Очистка cookies."), Tool(name='ClearStorage', func=_sync_error_func, coroutine=_cs_async, description="Очистка localStorage/sessionStorage."), Tool(name='Login', func=_l_sync, description="Вход на сайт (заглушка)."), ]
            self.tools.extend(state_tools); logger.debug(f'Добавлено {len(state_tools)} инструментов StateManager.')
        else: logger.warning('Инструменты StateManager не созданы.')


    # --- Методы _get_agent_executor, run_task, stream_task, __del__, close ---
    async def _get_agent_executor(self, llm: BaseChatModel) -> Optional[AgentExecutor]:
        """ Создает и возвращает AgentExecutor. """
        if not self._initialized: logger.error('Driver не инициализирован!'); return None
        if not llm: logger.error('LLM не предоставлена.'); return None
        if not self.tools: logger.error('Инструменты не созданы.'); return None
        prompt: Any; agent_runnable: Any; agent_executor: AgentExecutor
        try:
            prompt = hub.pull('hwchase17/react'); logger.debug(f'Создание агента: LLM={type(llm).__name__}, Tools={[t.name for t in self.tools]}')
            agent_runnable = create_react_agent(llm=llm, tools=self.tools, prompt=prompt)
            agent_executor = AgentExecutor(agent=agent_runnable, tools=self.tools, verbose=True, handle_parsing_errors=True, max_iterations=30, max_execution_time=300.0)
            logger.info('AgentExecutor создан.'); return agent_executor
        except Exception as ex: logger.error('Ошибка создания AgentExecutor.', ex, exc_info=True); return None

    async def run_task(self, task: str, use_gemini: bool = True) -> Optional[str]:
        """
        Запускает задачу и возвращает результат, обрабатывая ошибки.
        Включает логику повторных попыток при ошибке квоты Google Gemini.
        """
        # Ленивая асинхронная инициализация
        if not self._initialized:
            init_ok = await self.async_init()
            if not init_ok: logger.error('Ошибка инициализации Driver для run_task.'); return None

        model_name: str = 'Gemini' if use_gemini else 'OpenAI'
        selected_llm: Optional[BaseChatModel] = self.gemini if use_gemini else self.openai
        agent_executor: Optional[AgentExecutor]
        result_data: Optional[Dict[str, Any]] = None
        final_answer: Optional[str] = None
        retry_count: int = 0
        max_retries: int = 3 # Максимальное количество повторных попыток при ошибке квоты

        logger.info(f"Запуск run_task ({model_name}): '{task[:100]}...'")
        if not selected_llm: logger.error(f'LLM ({model_name}) не инициализирована.'); return None
        agent_executor = await self._get_agent_executor(selected_llm)
        if not agent_executor: return None

        # --- НАЧАЛО ЦИКЛА ПОВТОРНЫХ ПОПЫТОК ---
        while retry_count <= max_retries:
            try:
                # Логируем номер попытки (начиная с 1)
                logger.info(f'\n ++++++++++++++++++++++++++++++++++++++ \n Вызов agent_executor.ainvoke ({model_name}) (Попытка {retry_count + 1}/{max_retries + 1})...\n +++++++++++++++++++++++++++++++++++')
                result_data = await agent_executor.ainvoke({'input': task})
                final_answer = result_data.get('output')
                logger.info(f'\n +++++++++++++++++++++++++++++++++++ Агент ({model_name}) завершил run_task.\n +++++++++++++++++++++++++++++++++')
                if final_answer is None: logger.warning(f'Финальный ответ ("output") отсутствует ({model_name}). Результат: {result_data}', exc_info=False)
                return  final_answer 

            except ValueError as ex_val: # Обработка ValueError (не подлежит повтору)
                logger.warning(f"Обработанная ошибка ValueError ({model_name}): {ex_val}", exc_info=False)
                final_answer = f"Задача не выполнена: {ex_val}"
                break # Выходим из цикла

            except google_api_exceptions.ResourceExhausted as ex_quota: # Обработка ошибки квоты Google
                retry_count += 1 # Увеличиваем счетчик попыток
                logger.error(f"Ошибка квоты Google Gemini ({model_name}) (Попытка {retry_count}/{max_retries}).", ex_quota, exc_info=False)

                if retry_count > max_retries:
                    logger.error(f"Превышено максимальное количество ({max_retries}) попыток для ошибки квоты Google.")
                    final_answer = f"Ошибка: Превышена квота Google Gemini после {max_retries} попыток."
                    break # Выходим из цикла после превышения лимита

                # Извлечение задержки из метаданных
                retry_delay_seconds: int = 60 # Значение по умолчанию (60 секунд)
                delay_extracted: bool = False
                if hasattr(ex_quota, 'metadata') and ex_quota.metadata:
                     for item in ex_quota.metadata:
                         if item[0] == 'retry-delay':
                             try:
                                 delay_info = json.loads(item[1])
                                 # Берем значение 'seconds', минимум 1 секунда, иначе дефолт
                                 retry_delay_seconds = max(1, int(delay_info.get('seconds', retry_delay_seconds)))
                                 delay_extracted = True
                                 break
                             except (json.JSONDecodeError, ValueError, TypeError, KeyError):
                                 logger.warning(f"Не удалось распарсить retry-delay: {item[1]}", exc_info=False)

                delay_msg: str = f"Рекомендуемая задержка: {retry_delay_seconds} сек." if delay_extracted else f"Используем задержку по умолчанию: {retry_delay_seconds} сек."
                logger.info(f"{delay_msg} Ожидание перед повторной попыткой... URL лимитов: https://ai.google.dev/gemini-api/docs/rate-limits")

                # Асинхронное ожидание
                await asyncio.sleep(retry_delay_seconds)
                # Цикл продолжится для следующей попытки

            except LangChainException as ex_lc: # Обработка ошибок LangChain (не подлежит повтору)
                logger.error(f'Ошибка LangChain ({model_name}).', ex_lc, exc_info=True); final_answer = f"Ошибка LangChain: {ex_lc}"
                break # Выходим из цикла

            except Exception as ex_other: # Обработка других неожиданных ошибок (не подлежит повтору)
                logger.error(f'Неожиданная ошибка ({model_name}).', ex_other, exc_info=True); final_answer = f"Неожиданная ошибка: {ex_other}"
                break # Выходим из цикла
        # --- КОНЕЦ ЦИКЛА ПОВТОРНЫХ ПОПЫТОК ---

        return final_answer # Возврат результата или сообщения об ошибке


    async def stream_task(self, task: str, use_gemini: bool = True) -> Tuple[Optional[str], List[Dict[str, Any]]]:
        """ Запускает задачу и стримит шаги выполнения. """
        # Ленивая асинхронная инициализация
        if not self._initialized: init_ok = await self.async_init();
        if not init_ok: logger.error("Ошибка инициализации Driver для stream_task."); return None, []
        model_name: str = 'Gemini' if use_gemini else 'OpenAI'; selected_llm: Optional[BaseChatModel] = self.gemini if use_gemini else self.openai
        agent_executor: Optional[AgentExecutor]; final_answer: Optional[str] = None; all_chunks: List[Dict[str, Any]] = []
        logger.info(f"Запуск stream_task ({model_name}): '{task[:100]}...'")
        if not selected_llm: logger.error(f'LLM ({model_name}) не инициализирована.'); return None, []
        agent_executor = await self._get_agent_executor(selected_llm)
        if not agent_executor: return None, []
        logger.info(f'Начало стриминга ({model_name})...');
        # ПРИМЕЧАНИЕ: Логика повторных попыток для стриминга сложнее.
        # Оставим обработку ошибки квоты для стриминга как есть.
        try: final_answer, all_chunks = await stream_agent_execution(executor=agent_executor, task_input={'input': task})
        except google_api_exceptions.ResourceExhausted as ex:
             logger.error(f"Ошибка квоты Google Gemini во время stream_task ({model_name}).", ex, exc_info=False);
             final_answer = "Ошибка: Превышена квота Google Gemini во время стриминга."
             all_chunks = [] # Возвращаем пустой список чанков
        except Exception as ex:
             logger.error(f"Неожиданная ошибка во время stream_task ({model_name}).", ex, exc_info=True);
             final_answer = f"Ошибка стриминга: {ex}"
             all_chunks = []
        logger.info(f'Стриминг ({model_name}) завершен.'); return final_answer, all_chunks


    def __del__(self) -> None:
        """ Деструктор для попытки асинхронного закрытия браузера. """
        if self.browser:
            logger.info('Попытка закрытия BrowserController из __del__...'); loop: Optional[asyncio.AbstractEventLoop]
            try: loop = asyncio.get_event_loop_policy().get_event_loop()
            except RuntimeError: loop = None
            if loop and loop.is_running(): logger.warning("__del__: Невозможно надежно вызвать async close из работающего цикла.")
            else: logger.warning("__del__: Нет активного цикла событий для вызова async close.")
            logger.warning("Рекомендуется явно вызывать 'await driver.close()'.")

    async def close(self) -> None:
        """ Асинхронно закрывает браузер и освобождает ресурсы Playwright. """
        if self.browser: logger.info("Явный вызов async close()..."); await self.browser.close(); self.browser = None
        self._initialized = False


# --- Функция main для демонстрации ---
async def main() -> None:
    """ Основная асинхронная функция для демонстрации работы Driver. """
    # Объявление переменных
    driver: Optional[Driver] = None; init_success: bool = False
    search_available: bool = False; browser_core_available: bool = False; extraction_available: bool = False; interaction_available: bool = False
    available_tool_names: List[str] = []; task_to_run: Optional[str] = None; llm_to_test_run: List[Tuple[str, bool]] = []
    name: str; flag: bool; start_time: float; end_time: float; result: Optional[str]; parsed_result: Any
    product_category: str; num_links_str: str; search_query: str; search_tool_name: str

    try:
        logger.info('='*20 + ' Начало инициализации Driver ' + '='*20)
        driver = Driver(start_browser=True, browser_headless=True) # browser_headless=False для видимого окна
        init_success = await driver.async_init() # Асинхронная инициализация
        if not init_success: logger.critical('Асинхронная инициализация Driver не удалась.'); return # Выход, если не удалось
        logger.info('='*20 + ' Завершение инициализации Driver ' + '='*20)
    except Exception as ex:
        logger.critical('Критическая ошибка при инициализации Driver.', ex, exc_info=True);
        if driver: await driver.close(); # Попытка закрыть, если драйвер частично создался
        return # Выход при критической ошибке инициализации
    # Убрана лишняя проверка if not driver, так как она покрывается try/except выше

    # Основная логика работы с драйвером
    try:
        logger.info('Проверка доступности ключевых инструментов...')
        available_tool_names = [tool.name for tool in driver.tools]
        logger.info(f'Все доступные инструменты: {available_tool_names}')

        # Проверка наличия групп инструментов
        if 'SmartSearch' in available_tool_names or 'DuckDuckGoSearch' in available_tool_names: search_available = True
        if 'BrowserNavigate' in available_tool_names and 'BrowserScrapeText' in available_tool_names: browser_core_available = True
        if 'ExtractProductSchema' in available_tool_names: extraction_available = True
        if 'BrowserClickElement' in available_tool_names and 'FillFormField' in available_tool_names: interaction_available = True
        logger.info(f'Статус доступности:\n Поиск={search_available},\n Браузер(Core)={browser_core_available},\n Экстракция={extraction_available},\n Взаимодействие={interaction_available}')

        # --- Оценка токенов начального промпта ---
        # Перенесем формирование задачи сюда, чтобы оценить токены
        if search_available and browser_core_available and extraction_available:
            logger.info('Формируем СЛОЖНУЮ задачу.')
            product_category = 'Электрические чайники с терморегулятором'; num_links_str = 'две'
            search_tool_name = 'SmartSearch' if 'SmartSearch' in available_tool_names else 'DuckDuckGoSearch'
            task_to_run = f'''
**Роль:** Веб-Агент. **Цель:** Найти {num_links_str} URL товаров ('{product_category}') и извлечь инфо в список JSON.
**План:**
1. Найди URL через `{search_tool_name}` (категория: {product_category}).
2. Для каждого URL: `BrowserNavigate` -> Проверка логина (`BrowserScrapeText`) -> `BrowserClickElement` (попап) -> `BrowserScrapeHTML` -> `ExtractProductSchema` -> `BrowserScrapeText` (`raw_data`) -> Определи тип -> Сформируй JSON (Шаблон 1-5). Переведи текст на EN (кроме raw_data). Добавь в список.
3. Верни список JSON.
**Шаблоны:** Шаблон 1: {{..., "webpage_type": "product", "data": {{ "name": "<EN Name/N/A>", ..., "raw": "<Original Text>" }} }}; Шаблон 5: {{..., "status": "error", "webpage_type": "other/error", "data": {{...}} }}
'''
        elif search_available:
            logger.info('Формируем задачу ТОЛЬКО для поиска.'); search_query = 'Погода в Берлине на завтра'
            search_tool_name = 'SmartSearch' if 'SmartSearch' in available_tool_names else 'DuckDuckGoSearch'
            task_to_run = f'Используй {search_tool_name} для поиска: "{search_query}".'
        else:
            logger.warning('Ключевые инструменты недоступны. Базовая задача.')
            task_to_run = 'Каковы основные принципы объектно-ориентированного программирования?'

        if task_to_run:
            print(f'\nИтоговая задача:\n{"-"*20}\n{task_to_run}\n{"-"*20}')
            print("\n--- Оценка токенов начального промпта ---")
            if driver.gemini:
                try: num_tokens_gemini = driver.gemini.get_num_tokens(task_to_run); print(f"Gemini: Токены задачи ~ {num_tokens_gemini}")
                except Exception as ex_token_g: logger.warning(f"Не удалось оценить токены Gemini: {ex_token_g}", exc_info=False)
            if driver.openai:
                try: num_tokens_openai = driver.openai.get_num_tokens(task_to_run); print(f"OpenAI: Токены задачи ~ {num_tokens_openai}")
                except Exception as ex_token_o: logger.warning(f"Не удалось оценить токены OpenAI: {ex_token_o}", exc_info=False)
            print("-" * 30)
        else:
            logger.error('Не удалось сформировать задачу.'); return

        # --- Тест run_task ---
        print('\n' + '='*15 + ' Запуск run_task ' + '='*15)
        llm_to_test_run = []
        if driver.gemini and Config.GEMINI_STATUS.lower() == 'active': logger.info('Добавляем Gemini.'); llm_to_test_run.append(('Gemini', True))
        else: logger.warning('Gemini не активен/недоступен.')
        if driver.openai and Config.OPENAI_API_STATUS.lower() == 'active': logger.info('Добавляем OpenAI.'); llm_to_test_run.append(('OpenAI', False))
        else: logger.warning('OpenAI не активен/недоступен.')

        if not llm_to_test_run: print('\n[!] Нет АКТИВНЫХ LLM.'); logger.error('Нет активных LLM.'); return
        else:
            for name, flag in llm_to_test_run:
                print(f'\n--- Запуск run_task с {name} ---')
                start_time = asyncio.get_event_loop().time()
                try:
                    result = await driver.run_task(task_to_run, use_gemini=flag)
                    end_time = asyncio.get_event_loop().time()
                    print(f'\n[Результат run_task ({name}) - Заняло {end_time - start_time:.2f} сек]:')
                    try: # Красивый вывод JSON
                        if isinstance(result, str) and (result.strip().startswith('[') or result.strip().startswith('{')): parsed_result = json.loads(result); print(parsed_result)
                        elif isinstance(result, str) and result.startswith('Ошибка:'): print(f'[!] {result}') # Вывод сообщения об ошибке
                        else: print(result if result is not None else '[!] Нет ответа или неизвестная ошибка.')
                    except (json.JSONDecodeError, TypeError): print(result if result is not None else '[!] Нет ответа или неизвестная ошибка.')
                except asyncio.TimeoutError: end_time = asyncio.get_event_loop().time(); print(f'\n[!!!] ТАЙМАУТ ({name})! ({end_time - start_time:.2f} сек)'); logger.error(f'Таймаут run_task ({name})', exc_info=False)
                except Exception as ex: end_time = asyncio.get_event_loop().time(); print(f'\n[!!!] Ошибка ({name}): {ex} ({end_time - start_time:.2f} сек)'); logger.error(f'Ошибка run_task ({name})', ex, exc_info=True)

    finally:
        # --- Явное закрытие браузера в блоке finally ---
        if driver: logger.info("Явное закрытие браузера в блоке finally..."); await driver.close()

    logger.info('='*20 + ' Завершение работы main ' + '='*20)

if __name__ == '__main__':
    print('Запуск основной асинхронной функции main...')
    # Напоминание о зависимостях
    # pip install playwright beautifulsoup4 lxml langchain langchain-openai langchain-google-genai langchain-community google-search-results duckduckgo-search python-dotenv google-api-core
    # playwright install
    asyncio.run(main())
    print('Программа завершена.')
