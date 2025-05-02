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
CONTROLLERS_MODULE_PATH: str = 'src.webdriver.llm_driver.controllers'
BROWSER_CONTROLLER_AVAILABLE: bool = False # Инициализация флагов
BS4_AVAILABLE: bool = False
try:
    # pylint: disable=import-error
    from src.webdriver.llm_driver.controllers import (
        BS4_AVAILABLE, BrowserController, DataExtractionController,
        DownloadController, FormController, JavaScriptExecutionController,
        ScreenshotController, StateManager
    )
    BROWSER_CONTROLLER_AVAILABLE = True
    logger.info(f'Асинхронные контроллеры успешно импортированы из {CONTROLLERS_MODULE_PATH}.')
except ImportError as import_ex:
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
    BROWSER_CONTROLLER_AVAILABLE = False; BS4_AVAILABLE = False
# --- КОНЕЦ ИМПОРТА КОНТРОЛЛЕРОВ ---

# Загрузка переменных окружения
from dotenv import load_dotenv
dotenv_path: Path = __root__ / '.env'
if dotenv_path.exists():
    load_dotenv(dotenv_path=dotenv_path); logger.info(f'Загружены переменные окружения из: {dotenv_path}')
else: logger.warning(f'.env файл не найден по пути: {dotenv_path}.')


class Config:
    """ Класс для хранения статической конфигурации приложения. """
    ENDPOINT: Path = __root__ / 'src' / 'webdriver' / 'llm_driver'
    config: SimpleNamespace

    # --- ЗАГРУЗКА КОНФИГА ---
    try:
        config_path: Path = ENDPOINT / 'use_llm.json'
        if config_path.exists():
            config = j_loads_ns(config_path)
            if not config: logger.error(f'Файл конфигурации {config_path} пуст/некорректен!')
            else: logger.info(f'Конфигурация успешно загружена из {config_path}')
        else: logger.error(f'КРИТИЧЕСКАЯ ОШИБКА: Файл конфигурации НЕ НАЙДЕН: {config_path}!'); config = None
    except Exception as ex: logger.error(f'КРИТИЧЕСКАЯ ОШИБКА при загрузке/парсинге {config_path}.', ex, exc_info=True); config = None

    # --- ИНИЦИАЛИЗАЦИЯ АТРИБУТОВ КЛАССА ---
    # LLM
    GEMINI_API_KEY: Optional[str] = None; GEMINI_STATUS: str = 'inactive'; GEMINI_MODEL_NAME: str = ''
    OPENAI_API_KEY: Optional[str] = None; OPENAI_API_STATUS: str = 'inactive'; OPENAI_MODEL_NAME: str = ''
    # Search Providers
    SERPAPI_API_KEY: Optional[str] = None
    TAVILY_API_KEY: Optional[str] = None
    SEARCH_PROVIDERS_STATUS: Dict[str, str] = {"serpapi": "inactive", "duckduckgo": "active", "tavily": "inactive"}

    # --- Чтение настроек из Config ---
    try:
        if config:
            # LLM Модели
            if hasattr(config, 'models'):
                models_config = config.models
                gemini_conf = getattr(models_config, 'gemini', None); GEMINI_STATUS = getattr(gemini_conf, 'status', 'inactive') if gemini_conf else 'inactive'; GEMINI_MODEL_NAME = getattr(gemini_conf, 'model_name', '') if gemini_conf else ''
                openai_conf = getattr(models_config, 'openai', None); OPENAI_API_STATUS = getattr(openai_conf, 'status', 'inactive') if openai_conf else 'inactive'; OPENAI_MODEL_NAME = getattr(openai_conf, 'model_name', '') if openai_conf else ''
                # Статусы поисковиков могут быть в models (Вариант А)
                serp_m_conf = getattr(models_config, 'serpapi', None); SEARCH_PROVIDERS_STATUS["serpapi"] = getattr(serp_m_conf, 'status', SEARCH_PROVIDERS_STATUS["serpapi"]) if serp_m_conf else SEARCH_PROVIDERS_STATUS["serpapi"]
                tav_m_conf = getattr(models_config, 'tavily', None); SEARCH_PROVIDERS_STATUS["tavily"] = getattr(tav_m_conf, 'status', SEARCH_PROVIDERS_STATUS["tavily"]) if tav_m_conf else SEARCH_PROVIDERS_STATUS["tavily"]
                ddg_m_conf = getattr(models_config, 'duckduckgo', None); SEARCH_PROVIDERS_STATUS["duckduckgo"] = getattr(ddg_m_conf, 'status', SEARCH_PROVIDERS_STATUS["duckduckgo"]) if ddg_m_conf else SEARCH_PROVIDERS_STATUS["duckduckgo"]

            # Или в search_providers (Вариант Б - переопределит Вариант А)
            if hasattr(config, 'search_providers'):
                search_config = config.search_providers
                serp_s_conf = getattr(search_config, 'serpapi', None); SEARCH_PROVIDERS_STATUS["serpapi"] = getattr(serp_s_conf, 'status', SEARCH_PROVIDERS_STATUS["serpapi"]) if serp_s_conf else SEARCH_PROVIDERS_STATUS["serpapi"]
                tav_s_conf = getattr(search_config, 'tavily', None); SEARCH_PROVIDERS_STATUS["tavily"] = getattr(tav_s_conf, 'status', SEARCH_PROVIDERS_STATUS["tavily"]) if tav_s_conf else SEARCH_PROVIDERS_STATUS["tavily"]
                ddg_s_conf = getattr(search_config, 'duckduckgo', None); SEARCH_PROVIDERS_STATUS["duckduckgo"] = getattr(ddg_s_conf, 'status', SEARCH_PROVIDERS_STATUS["duckduckgo"]) if ddg_s_conf else SEARCH_PROVIDERS_STATUS["duckduckgo"]
        else: logger.warning('Config не загружен. Используются статусы по умолчанию.')
    except AttributeError as ex: logger.critical(f'Ошибка чтения структуры config: {ex}. Используются статусы по умолчанию.', exc_info=False); GEMINI_STATUS = 'inactive'; OPENAI_API_STATUS = 'inactive'; SEARCH_PROVIDERS_STATUS = {"serpapi": "inactive", "duckduckgo": "active", "tavily": "inactive"}

    # --- Установка API ключей ---
    try:
        try: GEMINI_API_KEY = gs.credentials.gemini.katia.api_key
        except AttributeError: pass
        try: OPENAI_API_KEY = gs.credentials.openai.hypotez.api_key
        except AttributeError: pass
        try: SERPAPI_API_KEY = gs.credentials.serpapi.onela.api_key
        except AttributeError: pass
        try: TAVILY_API_KEY = gs.credentials.tavily.default.api_key # <-- Укажите ваш путь
        except AttributeError: pass

        if not GEMINI_API_KEY: GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
        if not OPENAI_API_KEY: OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
        if not SERPAPI_API_KEY: SERPAPI_API_KEY = os.environ.get('SERPAPI_API_KEY')
        if not TAVILY_API_KEY: TAVILY_API_KEY = os.environ.get('TAVILY_API_KEY')

        if GEMINI_API_KEY: os.environ['GOOGLE_API_KEY'] = GEMINI_API_KEY
        if OPENAI_API_KEY: os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
        if SERPAPI_API_KEY: os.environ['SERPAPI_API_KEY'] = SERPAPI_API_KEY
        if TAVILY_API_KEY: os.environ['TAVILY_API_KEY'] = TAVILY_API_KEY

        logger.info(f'Config Gemini: Status={GEMINI_STATUS}, Model={GEMINI_MODEL_NAME}, Key Present={bool(GEMINI_API_KEY)}')
        logger.info(f'Config OpenAI: Status={OPENAI_API_STATUS}, Model={OPENAI_MODEL_NAME}, Key Present={bool(OPENAI_API_KEY)}')
        logger.info(f'Config SerpAPI: Status={SEARCH_PROVIDERS_STATUS.get("serpapi", "N/A")}, Key Present={bool(SERPAPI_API_KEY)}')
        logger.info(f'Config DuckDuckGo: Status={SEARCH_PROVIDERS_STATUS.get("duckduckgo", "N/A")}')
        logger.info(f'Config Tavily: Status={SEARCH_PROVIDERS_STATUS.get("tavily", "N/A")}, Key Present={bool(TAVILY_API_KEY)}')

    except ImportError: logger.warning("Модуль 'src.gs' не найден.")
    except NameError: logger.warning("Объект 'gs.credentials' не найден.")
    except Exception as ex: logger.error('Ошибка при установке API ключей в Config.', ex, exc_info=True)

# ===============================================================
# Функция стриминга
# ===============================================================
async def stream_agent_execution( executor: AgentExecutor, task_input: Dict[str, Any]) -> Tuple[Optional[str], List[Dict[str, Any]]]:
    """ Асинхронно выполняет агент и стримит шаги. """
    final_answer: Optional[str] = None; all_chunks: List[Dict[str, Any]] = []; run_id: Optional[str] = None
    logger.info(f'--- Начало стриминга для входа: {str(task_input)[:200]}... ---')
    try:
        async for chunk in executor.astream(task_input):
            all_chunks.append(chunk)
            if actions := chunk.get('actions'):
                for action in actions:
                    tool: str = getattr(action, 'tool', 'N/A'); tool_input: Any = getattr(action, 'tool_input', 'N/A'); log_msg: str = getattr(action, 'log', '').strip()
                    logger.info(f"Планируемое действие: Tool=[{tool}], Input=[{str(tool_input)[:100]}...]")
                    if log_msg: logger.debug(f'  Log (Мысли): {log_msg}', exc_info=False)
            elif steps := chunk.get('steps'):
                for step in steps:
                    observation: Any = getattr(step, 'observation', None); action_log: str = getattr(step.action, 'log', '').strip(); tool_used: str = getattr(step.action, 'tool', 'N/A')
                    if observation is not None: logger.info(f"Результат действия (Observation) от Tool=[{tool_used}]: {str(observation)[:300]}...")
                    if action_log: logger.debug(f"  Log (Мысли перед Observation): {action_log}", exc_info=False)
            elif output := chunk.get('output'): logger.info(f'Финальный ответ: {output}'); final_answer = output
            elif messages := chunk.get('messages'):
                 for msg in messages:
                     if content := getattr(msg, 'content', None): logger.debug(f'Message Chunk: {content}', exc_info=False)
            current_run_info = chunk.get('__run', {}); current_run_id = getattr(current_run_info, 'id', None)
            if current_run_id and current_run_id != run_id: run_id = current_run_id; logger.debug(f'Agent Run ID: {run_id}', exc_info=False)
    except LangChainException as ex: logger.error('Ошибка LangChain во время стриминга.', ex, exc_info=True)
    except Exception as ex: logger.error('Неожиданная ошибка во время стриминга.', ex, exc_info=True)
    logger.info(f'--- Стриминг завершен. Всего чанков: {len(all_chunks)}. ---')
    return final_answer, all_chunks
# ===============================================================

class Driver:
    """ Класс для управления LLM, контроллерами и агентами LangChain. """
    config_class: Type[Config] = Config
    gemini: Optional[BaseChatModel] = None; openai: Optional[BaseChatModel] = None
    tools: List[Tool] = []
    browser: Optional[BrowserController] = None
    data_extractor: Optional[DataExtractionController] = None
    form_controller: Optional[FormController] = None
    screenshot_controller: Optional[ScreenshotController] = None
    download_controller: Optional[DownloadController] = None
    js_executor: Optional[JavaScriptExecutionController] = None
    state_manager: Optional[StateManager] = None
    _initialized: bool = False
    _serpapi_key: Optional[str] = None
    _tavily_key: Optional[str] = None
    _search_provider_statuses: Dict[str, str] = {} # Инициализируем здесь
    _start_browser: bool; _browser_headless: bool; _browser_timeout: int

    def __init__(self,
                 GEMINI_API_KEY: Optional[str] = None, OPENAI_API_KEY: Optional[str] = None,
                 SERPAPI_API_KEY: Optional[str] = None, TAVILY_API_KEY: Optional[str] = None,
                 openai_model_name: Optional[str] = None, gemini_model_name: Optional[str] = None,
                 start_browser: bool = True, browser_headless: bool = True, browser_timeout: int = 30000,
                 **kwargs: Any) -> None:
        """ Синхронно инициализирует LLM и сохраняет параметры. """
        openai_api_key: Optional[str]; gemini_api_key: Optional[str]
        openai_model_name: str; gemini_model_model_name: str
        openai_status: str; gemini_status: str

        logger.info('--- Начало СИНХРОННОЙ инициализации Driver ---')
        self._start_browser = start_browser; self._browser_headless = browser_headless; self._browser_timeout = browser_timeout
        self._serpapi_key = SERPAPI_API_KEY or self.config_class.SERPAPI_API_KEY
        self._tavily_key = TAVILY_API_KEY or self.config_class.TAVILY_API_KEY
        self._search_provider_statuses = self.config_class.SEARCH_PROVIDERS_STATUS.copy()
        self._initialized = False

        self.openai = None; self.gemini = None; self.tools = []; self.browser = None; self.data_extractor = None; self.form_controller = None
        self.screenshot_controller = None; self.download_controller = None; self.js_executor = None; self.state_manager = None

        openai_api_key = OPENAI_API_KEY or self.config_class.OPENAI_API_KEY
        gemini_api_key = GEMINI_API_KEY or self.config_class.GEMINI_API_KEY
        openai_model = openai_model_name or self.config_class.OPENAI_MODEL_NAME
        gemini_model = gemini_model_name or self.config_class.GEMINI_MODEL_NAME
        openai_status = self.config_class.OPENAI_API_STATUS
        gemini_status = self.config_class.GEMINI_STATUS

        if gemini_api_key: os.environ['GEMINI_API_KEY'] = gemini_api_key
        if openai_api_key: os.environ['OPENAI_API_KEY'] = openai_api_key
        if self._serpapi_key: os.environ['SERPAPI_API_KEY'] = self._serpapi_key
        if self._tavily_key: os.environ['TAVILY_API_KEY'] = self._tavily_key

        self.openai = self._initialize_openai(openai_api_key, openai_status, openai_model)
        self.gemini = self._initialize_gemini(gemini_api_key, gemini_status, gemini_model)

        if kwargs: logger.warning(f'Неиспользованные аргументы: {kwargs}', exc_info=False)
        logger.info('--- Синхронная инициализация Driver завершена. Вызовите async_init() ---')

    async def async_init(self) -> bool:
        """ Асинхронно инициализирует BrowserController и инструменты. """
        if self._initialized: logger.info('Driver уже инициализирован.'); return True
        logger.info('--- Начало АСИНХРОННОЙ инициализации Driver ---')
        self.tools = []
        await self._async_initialize_browser_and_controllers(self._start_browser, self._browser_headless, self._browser_timeout)
        self._create_tools()
        logger.info(f'Итоговый список доступных инструментов Driver: {[tool.name for tool in self.tools]}')
        self._initialized = True
        logger.info('--- Асинхронная инициализация Driver завершена ---')
        return True

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
            try: llm = ChatGoogleGenerativeAI(model=model_name, google_api_key=api_key, temperature=0.1, convert_system_message_to_human=True); logger.info('Gemini LLM инициализирован.')
            except Exception as ex: logger.error('Ошибка инициализации Gemini.', ex, exc_info=True)
        else: logger.warning(f'Gemini LLM не инициализирован (Key={bool(api_key)}, Status={status}, Model={model_name})', exc_info=False)
        return llm

    async def _async_initialize_browser_and_controllers(self, start: bool, headless: bool, timeout: int) -> None:
        """ Асинхронно инициализирует BrowserController и зависимые контроллеры. """
        self.browser = None; self.data_extractor = None; self.form_controller = None; self.screenshot_controller = None; self.download_controller = None; self.js_executor = None; self.state_manager = None
        browser_started: bool = False
        if not start: logger.info('Иниц. браузера пропущена (start=False).'); return
        if not BROWSER_CONTROLLER_AVAILABLE: logger.warning('BrowserController недоступен.', exc_info=False); return
        try:
            logger.info('Асинхронная инициализация BrowserController...')
            self.browser = BrowserController(headless=headless, timeout=timeout)
            browser_started = await self.browser.start()
            if not browser_started: logger.error('Не удалось запустить BrowserController!'); self.browser = None; return
            logger.info('BrowserController асинхронно инициализирован.')
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
        """ Создает инструменты LangChain для активных поисковиков и контроллеров. """
        logger.info('Создание инструментов LangChain...')
        self.tools = []
        def _sync_error_func(*args: Any, **kwargs: Any) -> str: return 'Ошибка: асинхронный вызов (use coroutine).'

        # --- 1. Поисковые Инструменты ---
        search_tool_added: bool = False
        # SerpAPI (Google)
        if self._search_provider_statuses.get("serpapi") == "active":
            if self._serpapi_key:
                try:
                    serp_tool = Tool(name="GoogleSearch", func=SerpAPIWrapper().run, description="Поиск Google (SerpAPI). Вход: запрос.")
                    self.tools.append(serp_tool); logger.debug('Инструмент GoogleSearch (SerpAPI) добавлен.'); search_tool_added = True
                except Exception as ex: logger.error(f"Ошибка создания SerpAPI Tool: {ex}", exc_info=True)
            else: logger.warning("SerpAPI активен, но ключ SERPAPI_API_KEY не найден!")
        # Tavily Search
        if self._search_provider_statuses.get("tavily") == "active":
            if self._tavily_key:
                try:
                    tav_tool = TavilySearchResults(max_results=5, name="TavilySearch", description="Поиск Tavily. Вход: запрос.")
                    self.tools.append(tav_tool); logger.debug('Инструмент TavilySearch добавлен.'); search_tool_added = True
                except Exception as ex: logger.error(f"Ошибка создания Tavily Tool: {ex}", exc_info=True)
            else: logger.warning("Tavily активен, но ключ TAVILY_API_KEY не найден!")
        # DuckDuckGo
        if self._search_provider_statuses.get("duckduckgo") == "active":
            try:
                ddg_tool = DuckDuckGoSearchRun(name="DuckDuckGoSearch", description="Поиск DuckDuckGo. Вход: запрос.")
                self.tools.append(ddg_tool); logger.debug('Инструмент DuckDuckGoSearch добавлен.'); search_tool_added = True
            except Exception as ex: logger.error(f"Ошибка создания DuckDuckGo Tool: {ex}", exc_info=True)
        if not search_tool_added: logger.warning("Ни один поисковый инструмент не был добавлен!")

        # --- 2. Браузерные Инструменты ---
        if self.browser:
            async def _nav(u: str) -> str: return await self.browser.navigate(u) if self.browser else 'Err:BrowserNA'
            async def _st(s: Optional[str]=None) -> str: return await self.browser.scrape_text(s) if self.browser else 'Err:BrowserNA'
            async def _sh(s: Optional[str]=None) -> str: return await self.browser.scrape_html(s) if self.browser else 'Err:BrowserNA'
            async def _ce(s: str) -> str: return await self.browser.click_element(s) if self.browser else 'Err:BrowserNA'
            def _gu(i: Any=None) -> str: return self.browser.get_current_url() if self.browser else 'Err:BrowserNA'
            browser_tools = [ Tool('BrowserNavigate',_sync_error_func,coroutine=_nav,description='URL Nav'), Tool('BrowserScrapeText',_sync_error_func,coroutine=_st,description='Scrape Text(sel?)'), Tool('BrowserScrapeHTML',_sync_error_func,coroutine=_sh,description='Scrape HTML(sel?)'), Tool('BrowserClickElement',_sync_error_func,coroutine=_ce,description='Click(sel)'), Tool('GetCurrentURL',_gu,description='Get URL') ]
            self.tools.extend(browser_tools); logger.debug(f'Добавлено {len(browser_tools)} инструментов BrowserController.')
        else: logger.warning('Инструменты BrowserController не созданы.')

        # --- 3. Инструменты Извлечения Данных ---
        if self.data_extractor:
            def _fl_wrap(p: Any) -> Union[List[str], Dict[str, str]]:
                if not isinstance(p, dict): return {'error': 'Err:BadInput'};
                if 'html' not in p: return {'error': 'Err:NoHTML'};
                try: base = p.get('base_url') or (self.browser.get_current_url() if self.browser else None); return self.data_extractor.find_links(p['html'], base) if self.data_extractor else {'error':'Err:ExtractorNA'}
                except Exception as ex: logger.error("FindPageLinks Ошибка", ex, exc_info=True); return {'error': f'Err:{ex}'}
            extract_tools = [ Tool('ExtractProductSchema', lambda h: self.data_extractor.extract_product_details(h) if self.data_extractor else 'Err:ExtractorNA', description='Extract Product'), Tool('ExtractContactInfo', lambda t: self.data_extractor.extract_contact_info(t) if self.data_extractor else 'Err:ExtractorNA', description='Extract Contact'), Tool('FindPageLinks', _fl_wrap, description="Find Links {'html':...,'base_url':?}") ]
            self.tools.extend(extract_tools); logger.debug(f'Добавлено {len(extract_tools)} инструментов DataExtraction.')
        else: logger.warning('Инструменты DataExtractionController не созданы.')

        # --- 4. Инструменты Управления Формами ---
        if self.form_controller:
            async def _fff(p: Dict[str,Any]) -> str: return await self.form_controller.fill_input_field(p['selector'],p['value']) if self.form_controller and isinstance(p,dict) else 'Err:FormNA/BadInput'
            async def _sdd(p: Dict[str,Any]) -> str: return await self.form_controller.select_dropdown_option(p['selector'],value=p.get('value'),label=p.get('label')) if self.form_controller and isinstance(p,dict) else 'Err:FormNA/BadInput'
            async def _sf(p: Dict[str,Any]) -> str: return await self.form_controller.submit_form(form_selector=p.get('form_selector'),submit_button_selector=p.get('submit_button_selector')) if self.form_controller and isinstance(p,dict) else 'Err:FormNA/BadInput'
            form_tools = [ Tool('FillFormField',_sync_error_func,coroutine=_fff,description="Fill {'sel':...,'val':...}"), Tool('SelectDropdown',_sync_error_func,coroutine=_sdd,description="Select {'sel':...,'val':?/'lbl':?}"), Tool('SubmitForm',_sync_error_func,coroutine=_sf,description="Submit {'form_sel':?,'btn_sel':?}") ]
            self.tools.extend(form_tools); logger.debug(f'Добавлено {len(form_tools)} инструментов FormController.')
        else: logger.warning('Инструменты FormController не созданы.')

        # --- 5. Инструмент Скриншотов ---
        if self.screenshot_controller:
            async def _ss(p: Dict[str,Any]) -> str: return await self.screenshot_controller.take_screenshot(p['save_path'],full_page=p.get('full_page',True),selector=p.get('selector')) if self.screenshot_controller and isinstance(p,dict) else 'Err:SSNA/BadInput'
            self.tools.append(Tool('TakeScreenshot',_sync_error_func,coroutine=_ss,description="Screenshot {'path':...,'full':?,'sel':?}"))
            logger.debug('Инструмент TakeScreenshot добавлен.')
        else: logger.warning('Инструмент TakeScreenshot не создан.')

        # --- 6. Инструмент Загрузки ---
        if self.download_controller:
            async def _dl(p: Dict[str,Any]) -> str: return await self.download_controller.click_and_download(p['click_selector'],p['save_directory'],timeout=p.get('timeout',60000)) if self.download_controller and isinstance(p,dict) else 'Err:DLNA/BadInput'
            self.tools.append(Tool('ClickAndDownload',_sync_error_func,coroutine=_dl,description="Download {'clk_sel':...,'dir':...,'to':?}"))
            logger.debug('Инструмент ClickAndDownload добавлен.')
        else: logger.warning('Инструмент ClickAndDownload не создан.')

        # --- 7. Инструмент Выполнения JS ---
        if self.js_executor:
            async def _ejs(s: str) -> Union[str, Any]: return await self.js_executor.execute_script(s) if self.js_executor else 'Err:JsExecNA'
            self.tools.append(Tool('ExecuteJavaScript',_sync_error_func,coroutine=_ejs,description="JS Exec (WARN!)"))
            logger.debug('Инструмент ExecuteJavaScript добавлен.')
        else: logger.warning('Инструмент ExecuteJavaScript не создан.')

        # --- 8. Инструменты Управления Состоянием ---
        if self.state_manager:
            async def _gc(u: Optional[str]=None) -> Union[List[Dict[str, Any]],str]: return await self.state_manager.get_cookies(u) if self.state_manager else 'Err:StateNA'
            async def _cc() -> str: return await self.state_manager.clear_cookies() if self.state_manager else 'Err:StateNA'
            async def _cs() -> str: return await self.state_manager.clear_storage() if self.state_manager else 'Err:StateNA'
            def _l(*a: Any, **kw: Any) -> str: return self.state_manager.login(*a, **kw) if self.state_manager else 'Err:StateNA'
            state_tools = [ Tool('GetCookies',_sync_error_func,coroutine=_gc,description="Get Cookies(url?)"), Tool('ClearCookies',_sync_error_func,coroutine=_cc,description="Clear Cookies"), Tool('ClearStorage',_sync_error_func,coroutine=_cs,description="Clear Storage"), Tool('Login',_l,description="Login(stub)") ]
            self.tools.extend(state_tools); logger.debug(f'Добавлено {len(state_tools)} инструментов StateManager.')
        else: logger.warning('Инструменты StateManager не созданы.')

    # --- Методы run_task, stream_task, __del__, close, _get_agent_executor ---
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
        Запускает задачу и возвращает результат, обрабатывая ошибки и квоты.
        Включает логику повторных попыток при ошибках квоты Google Gemini и DDG.
        """
        # ... (Начало метода run_task без изменений: инициализация, получение llm/executor) ...
        if not self._initialized:
            init_ok = await self.async_init()
            if not init_ok: logger.error('Ошибка инициализации Driver для run_task.'); return None
            logger.info("Ленивая инициализация Driver завершена успешно.")

        model_name: str = 'Gemini' if use_gemini else 'OpenAI'
        selected_llm: Optional[BaseChatModel] = self.gemini if use_gemini else self.openai
        agent_executor: Optional[AgentExecutor]; result_data: Optional[Dict[str, Any]] = None
        final_answer_raw: Optional[str] = None; retry_count: int = 0; max_retries: int = 3

        logger.info(f"Запуск run_task ({model_name}): '{task[:100]}...'")
        if not selected_llm: logger.error(f'LLM ({model_name}) не инициализирована.'); return None
        agent_executor = await self._get_agent_executor(selected_llm)
        if not agent_executor: return None

        # --- НАЧАЛО ЦИКЛА ПОВТОРНЫХ ПОПЫТОК ---
        while retry_count <= max_retries:
            try:
                logger.info(f'Вызов agent_executor.ainvoke ({model_name}) (Попытка {retry_count + 1}/{max_retries + 1})...')
                result_data = await agent_executor.ainvoke({'input': task})
                final_answer_raw = result_data.get('output')
                logger.info(f'Агент ({model_name}) успешно завершил run_task.')
                if final_answer_raw is None: logger.warning(f'Финальный ответ ("output") отсутствует ({model_name}). Result: {result_data}', exc_info=False)
                break # Успех

            except ValueError as ex_val:
                logger.warning(f"Обработанная ошибка ValueError ({model_name}): {ex_val}", exc_info=False)
                final_answer_raw = f"Задача не выполнена: {ex_val}"; break

            except google_api_exceptions.ResourceExhausted as ex_quota:
                retry_count += 1
                logger.error(f"Ошибка квоты Google Gemini ({model_name}) (Попытка {retry_count}/{max_retries}).", ex_quota, exc_info=False)
                if retry_count > max_retries:
                    logger.error(f"Превышен лимит ({max_retries}) попыток Google."); final_answer_raw = f"Ошибка: Превышена квота Google Gemini после {max_retries} попыток."; break
                retry_delay_seconds: int = 60; delay_extracted: bool = False
                if hasattr(ex_quota, 'metadata') and ex_quota.metadata:
                     for item in ex_quota.metadata:
                         if item[0] == 'retry-delay':
                            try:
                                delay_info = json.loads(item[1]); retry_delay_seconds = max(1, int(delay_info.get('seconds', retry_delay_seconds))); delay_extracted = True; break
                            except Exception as parse_ex: logger.warning(f"Не удалось распарсить retry-delay: '{item[1]}'. Ошибка: {parse_ex}", exc_info=False)
                delay_msg: str = f"Рекомендуемая задержка: {retry_delay_seconds} сек." if delay_extracted else f"Используем задержку по умолчанию: {retry_delay_seconds} сек."
                logger.info(f"{delay_msg} Ожидание перед повторной попыткой (Google)..."); await asyncio.sleep(retry_delay_seconds)

            # --- НОВЫЙ БЛОК ОБРАБОТКИ ОШИБКИ DDG ---
            except DuckDuckGoSearchException as ex_ddg:
                # Проверяем, является ли это ошибкой Rate Limit
                if "ratelimit" in str(ex_ddg).lower() or "202" in str(ex_ddg): # Ищем по тексту ошибки
                    retry_count += 1
                    logger.error(f"Ошибка Rate Limit DuckDuckGo ({model_name}) (Попытка {retry_count}/{max_retries}).", ex_ddg, exc_info=False)
                    if retry_count > max_retries:
                        logger.error(f"Превышен лимит ({max_retries}) попыток DDG."); final_answer_raw = f"Ошибка: Rate Limit DuckDuckGo после {max_retries} попыток."; break

                    # Устанавливаем фиксированную задержку для DDG (например, 30 секунд)
                    ddg_retry_delay_seconds = 30
                    logger.info(f"Ожидание {ddg_retry_delay_seconds} сек. перед повторной попыткой (DDG)...")
                    await asyncio.sleep(ddg_retry_delay_seconds)
                else:
                    # Другая ошибка от DDG - не повторяем
                    logger.error(f"Неожиданная ошибка DuckDuckGo ({model_name}).", ex_ddg, exc_info=True)
                    final_answer_raw = f"Ошибка DuckDuckGo: {ex_ddg}"; break
            # --- КОНЕЦ НОВОГО БЛОКА ---

            except LangChainException as ex_lc:
                logger.error(f'Ошибка LangChain ({model_name}).', ex_lc, exc_info=True); final_answer_raw = f"Ошибка LangChain: {ex_lc}"; break
            except Exception as ex_other:
                logger.error(f'Неожиданная ошибка ({model_name}).', ex_other, exc_info=True); final_answer_raw = f"Неожиданная ошибка: {ex_other}"; break
        # --- КОНЕЦ ЦИКЛА ПОВТОРНЫХ ПОПЫТОК ---

        # --- ПОСТ-ОБРАБОТКА ОТВЕТА (без изменений) ---
        if final_answer_raw and isinstance(final_answer_raw, str):
             # ... (код пост-обработки как раньше) ...
            try:
                parsed_data = json.loads(final_answer_raw)
                trigger_message = "provided a summary instead of a list of URLs"
                if (isinstance(parsed_data, dict) and
                        parsed_data.get("product_links") == [] and
                        isinstance(parsed_data.get("message"), str) and
                        trigger_message in parsed_data["message"]):
                    target_domain = parsed_data.get("target_domain", "Unknown")
                    summary_text = parsed_data["message"]
                    logger.info("Агент вернул сводку вместо ссылок. Переформатируем вывод.")
                    summary_output = {"target_domain": target_domain, "summary": summary_text}
                    return json.dumps(summary_output, ensure_ascii=False, indent=2)
                else:
                    return final_answer_raw
            except json.JSONDecodeError:
                logger.warning(f"Агент ({model_name}) вернул не JSON ответ: {final_answer_raw[:200]}...")
                return final_answer_raw
            except Exception as post_ex:
                logger.error(f"Ошибка пост-обработки ответа агента ({model_name}): {post_ex}", exc_info=True)
                return final_answer_raw
        else:
            return final_answer_raw




    async def stream_task(self, task: str, use_gemini: bool = True) -> Tuple[Optional[str], List[Dict[str, Any]]]:
        """ Запускает задачу и стримит шаги выполнения. """
        if not self._initialized: init_ok = await self.async_init();
        if not init_ok: logger.error("Ошибка инициализации Driver для stream_task."); return None, []
        model_name: str = 'Gemini' if use_gemini else 'OpenAI'; selected_llm: Optional[BaseChatModel] = self.gemini if use_gemini else self.openai
        agent_executor: Optional[AgentExecutor]; final_answer: Optional[str] = None; all_chunks: List[Dict[str, Any]] = []
        logger.info(f"Запуск stream_task ({model_name}): '{task[:100]}...'")
        if not selected_llm: logger.error(f'LLM ({model_name}) не инициализирована.'); return None, []
        agent_executor = await self._get_agent_executor(selected_llm)
        if not agent_executor: return None, []
        logger.info(f'Начало стриминга ({model_name})...');
        try: 
            final_answer, all_chunks = await stream_agent_execution(executor=agent_executor, task_input={'input': task})
        except google_api_exceptions.ResourceExhausted as ex: 
            logger.error(f"Ошибка квоты Google в stream_task ({model_name}).", ex, exc_info=False)
            final_answer = "Ошибка: Превышена квота Google."; all_chunks = []
        except Exception as ex: 
            logger.error(f"Неожиданная ошибка в stream_task ({model_name}).", ex, exc_info=True)
            final_answer = f"Ошибка стриминга: {ex}"
            all_chunks = []
        logger.info(f'Стриминг ({model_name}) завершен.'); return final_answer, all_chunks

    def __del__(self) -> None:
        """ Деструктор для попытки асинхронного закрытия браузера. """
        if self.browser:
            logger.info('Попытка закрытия BrowserController из __del__...'); loop: Optional[asyncio.AbstractEventLoop]
            try: loop = asyncio.get_event_loop_policy().get_event_loop()
            except RuntimeError: loop = None
            if loop and loop.is_running(): logger.warning("__del__: Невозможно надежно вызвать async close из раб. цикла.")
            else: logger.warning("__del__: Нет активного цикла событий для вызова async close.")
            logger.warning("Рекомендуется явно вызывать 'await driver.close()'.")

    async def close(self) -> None:
        """ Асинхронно закрывает браузер и освобождает ресурсы Playwright. """
        if self.browser: logger.info("Явный вызов async close()..."); await self.browser.close(); self.browser = None
        self._initialized = False

# --- Функция main для демонстрации ---
async def main() -> None:
    """ Основная асинхронная функция для демонстрации работы Driver. """
    driver: Optional[Driver] = None; init_success: bool = False
    search_available: bool = False; browser_core_available: bool = False; extraction_available: bool = False; interaction_available: bool = False
    available_tool_names: List[str] = []; task_to_run: Optional[str] = None; llm_to_test_run: List[Tuple[str, bool]] = []
    name: str; flag: bool; start_time: float; end_time: float; result: Optional[str]; parsed_result: Any
    product_category: str; num_links_str: str; search_query: str; search_tool_name: str

    try:
        logger.info('='*20 + ' Начало инициализации Driver ' + '='*20)
        driver = Driver(start_browser=True, browser_headless=True)
        init_success = await driver.async_init()
        if not init_success: logger.critical('Асинхронная инициализация Driver не удалась.'); return
        logger.info('='*20 + ' Завершение инициализации Driver ' + '='*20)
    except Exception as ex: 
        logger.critical('Крит. ошибка инициализации Driver.', ex, exc_info=True)
        await driver.close() 
        return driver or None; 
        

    try:
        logger.info('Проверка доступности инструментов...')
        available_tool_names = [tool.name for tool in driver.tools]
        logger.info(f'Инструменты: {available_tool_names}')
        search_tools = [name for name in available_tool_names if name in ["GoogleSearch", "TavilySearch", "DuckDuckGoSearch"]]
        search_available = bool(search_tools); logger.info(f"Поиск доступен: {search_tools if search_available else 'Нет'}")
        browser_core_available = all(n in available_tool_names for n in ['BrowserNavigate', 'BrowserScrapeText'])
        extraction_available = 'ExtractProductSchema' in available_tool_names
        interaction_available = all(n in available_tool_names for n in ['BrowserClickElement', 'FillFormField'])
        logger.info(f'Статус: Поиск={search_available}, Браузер={browser_core_available}, Экстракция={extraction_available}, Взаимодействие={interaction_available}')

        search_tool_name = "DuckDuckGoSearch" # Default
        if 'TavilySearch' in search_tools: search_tool_name = 'TavilySearch'
        elif 'GoogleSearch' in search_tools: search_tool_name = 'GoogleSearch'

        if search_available and browser_core_available and extraction_available:
            logger.info('Формируем СЛОЖНУЮ задачу.'); product_category = 'Электрические зубные щетки'; num_links_str = 'одну'
            task_to_run = f'''**Роль:** Веб-Агент. **Цель:** Найти {num_links_str} URL товаров ('{product_category}') через {search_tool_name}, перейти, извлечь JSON (Шаблон 1). **План:** 1. `{search_tool_name}` -> 2. `BrowserNavigate` -> 3. `BrowserScrapeHTML` -> 4. `ExtractProductSchema` -> 5. `BrowserScrapeText` -> 6. Верни JSON (Шаблон 1). **Шаблон 1:** {{..., "webpage_type": "product", "data": {{ "name": "<EN Name/N/A>", ..., "raw": "<Original Text>" }} }}'''
        elif search_available: logger.info('Формируем задачу ТОЛЬКО для поиска.'); search_query = 'Последние новости AI'; task_to_run = f'Используй {search_tool_name} для поиска: "{search_query}".'
        else: logger.warning('Ключевые инструменты недоступны.'); task_to_run = 'Что такое рекурсия?'

        if task_to_run:
            print(f'\nЗадача:\n{"-"*20}\n{task_to_run}\n{"-"*20}'); print("\n--- Оценка токенов ---")
            if driver.gemini: 
                try: 
                    print(f"Gemini ~ {driver.gemini.get_num_tokens(task_to_run)} ток.") 
                except Exception: 
                    ...
            if driver.openai: 
                try: print(f"OpenAI ~ {driver.openai.get_num_tokens(task_to_run)} ток.") 
                except Exception: 
                    ...
            print("-" * 30)
        else: logger.error('Не удалось сформировать задачу.'); return

        print('\n' + '='*15 + ' Запуск run_task ' + '='*15)
        llm_to_test_run = []
        if driver.gemini and Config.GEMINI_STATUS.lower() == 'active': llm_to_test_run.append(('Gemini', True))
        if driver.openai and Config.OPENAI_API_STATUS.lower() == 'active': llm_to_test_run.append(('OpenAI', False))
        if not llm_to_test_run: print('[!] Нет АКТИВНЫХ LLM.'); return

        for name, flag in llm_to_test_run:
            print(f'\n--- Запуск run_task с {name} ---'); start_time = asyncio.get_event_loop().time()
            try:
                result = await driver.run_task(task_to_run, use_gemini=flag); end_time = asyncio.get_event_loop().time()
                print(f'\n[Результат ({name}) - {end_time - start_time:.2f} сек]:')
                try: # Красивый вывод
                    if isinstance(result, str) and (result.strip().startswith('[') or result.strip().startswith('{')): parsed_result = json.loads(result); print(parsed_result)
                    elif isinstance(result, str) and result.startswith('Ошибка:'): print(f'[!] {result}')
                    else: print(result if result is not None else '[!] Нет ответа.')
                except Exception: 
                    print(result if result is not None else '[!] Нет ответа.')
                    ...
                    
            except Exception as ex: 
                end_time = asyncio.get_event_loop().time()
                print(f'\n[!!!] Ошибка ({name}): {ex} ({end_time - start_time:.2f} сек)')
                logger.error(f'Ошибка run_task ({name})', ex, exc_info=True)
                ...

    finally: await driver.close() if driver else None; logger.info('='*20 + ' Завершение работы main ' + '='*20)

if __name__ == '__main__':
    print('Запуск основной асинхронной функции main...')
    print("Напоминание: Установлены ли playwright, beautifulsoup4, lxml, langchain*, google-search-results, duckduckgo-search, python-dotenv, google-api-core, tavily-python?")
    print("Выполнен ли 'playwright install'?")
    print("-" * 40)
    asyncio.run(main())
    print('Программа завершена.')