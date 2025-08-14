# # \file src/webdriver/ai_browser/use_llm.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3

"""Module for launching tasks using LLM through Langchain and standard agents.
==================================================================================================
Uses search API tools and asynchronous control tools
browser/content from the Controllers module.

Provides functionality for:
- Configuration of models (Gemini, Openai).
- installations of the API keys for LLM and search services.
- asynchronous initialization of controllers (browser, data extraction, forms, etc.).
- creating Langchain tools for controllers and active search engines.
- starting the task using LLM and available tools.
- fulfilling the task to the final result (`run_task`) with the logic of repetition when quota errors.
- Streaming of the task (`stream_task`).

Dependencies:
    -Langchain-Openai, Langchain-Google-Genai, Langchain-Core, Langchainhub, Langchain
    - Langchain-comunity (for Serpapiwrapper, Duckduckgosearchrun, TavilySearchresults)
    -Google-Search-Results (for Serpapiwrapper)
    - Duckduckgo-Search (for Duckduckgosearchrun)
    - Tavily-Python.
    -Google-Api-Core (for processing errors of the Google API quota)
    - Python-Dotenv
    - Playwright, Beautifulsoup4, LXML
    - SRC.GS, SRC.Logger, SRC.utils, Header
    - src.webdriver.llm_driver.controllers

`` `RST
.. Module :: SRC.WebDriver.AI_BROWSER.use_LLM
`` `"""

# Standard libraries
import asyncio
import json # For parsing result in Main
import logging # Standard logging
import os
from pathlib import Path
from types import SimpleNamespace
from typing import (Any, AsyncIterator, Callable, Coroutine, Dict, List, # pylint: disable=unused-import
                    Optional, Tuple, Type, TypeAlias, Union)

# Langchain components
from langchain import hub
from langchain.agents import AgentExecutor, Tool, create_react_agent
# --- search tools ---
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities import SerpAPIWrapper
# --- core Langchain ---
from langchain_core.exceptions import LangChainException
from langchain_core.language_models.chat_models import BaseChatModel
# --- Models Langchain ---
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
# --- Exceptions of Google API ---
from google.api_core import exceptions as google_api_exceptions


from google.api_core import exceptions as google_api_exceptions
from duckduckgo_search.exceptions import DuckDuckGoSearchException 
from langchain_core.exceptions import LangChainException

# --- internal modules ---
import header

from header import __root__
from src import gs
from src.logger import logger
from src.utils.jjson import j_loads_ns 
from src.utils.printer import pprint as print

# --- import of asynchronous controllers ---
# The path to the module with controllers
CONTROLLERS_MODULE_PATH: str = 'src.webdriver.llm_driver.controllers'
# The accessibility flag of the main BrowserController
BROWSER_CONTROLLER_AVAILABLE: bool = False 
# BEAUTIFULSOP accessibility flag necessary for some controllers
BS4_AVAILABLE: bool = False
try:
    # pylint: disable=import-error
    # Attempting controllers
    from src.webdriver.llm_driver.controllers import (
        BS4_AVAILABLE, BrowserController, DataExtractionController,
        DownloadController, FormController, JavaScriptExecutionController,
        ScreenshotController, StateManager
    )
    # Installation of the flag of successful import
    BROWSER_CONTROLLER_AVAILABLE = True
    logger.info(f'Асинхронные контроллеры успешно импортированы из {CONTROLLERS_MODULE_PATH}.')
except ImportError as import_ex:
    # Error logging in case of unsuccessful import
    logger.error(f'КРИТИЧЕСКАЯ ОШИБКА: Не удалось импортировать контроллеры из {CONTROLLERS_MODULE_PATH}.', import_ex, exc_info=True)
    class BrowserController: # type: ignore
        """BrowserController plug in case of import error."""
        _is_started: bool = False
        def __init__(self, *args: Any, **kwargs: Any) -> None: logger.debug('Инициализирован ЗАГЛУШКА BrowserController.', exc_info=False)
        async def start(self) -> bool: logger.error('Заглушка: start не реализован.'); return False
        async def navigate(self, u: str) -> str: return f'Ошибка: Заглушка BrowserController, navigate({u}).'
        async def scrape_text(self, s: Optional[str]=None) -> str: return 'Ошибка: Заглушка BrowserController, scrape_text.'
        async def scrape_html(self, s: Optional[str]=None) -> str: return 'Ошибка: Заглушка BrowserController, scrape_html.'
        async def click_element(self, s: str) -> str: return f'Ошибка: Заглушка BrowserController, click_element({s}).'
        def get_current_url(self) -> str: return 'Ошибка: Заглушка BrowserController.'
        async def close(self) -> None: logger.debug('Вызван close ЗАГЛУШКИ BrowserController.', exc_info=False)
    # Installation of flags of the inaccessibility of controllers
    BROWSER_CONTROLLER_AVAILABLE = False; BS4_AVAILABLE = False
# --- The end of the import of controllers ---

# Loading variables of the environment
from dotenv import load_dotenv
# Determining the path to .env file
dotenv_path: Path = __root__ / '.env'
# Checking the existence of .env file and its download
if dotenv_path.exists():
    load_dotenv(dotenv_path=dotenv_path); logger.info(f'Загружены переменные окружения из: {dotenv_path}')
else: logger.warning(f'.env файл не найден по пути: {dotenv_path}.')


class Config:
    """Class for storing the static configuration of the application."""
    # The end point for configuration files associated with LLM_DRIVER
    ENDPOINT: Path = __root__ / 'src' / 'webdriver' / 'llm_driver'
    # A variable for storing a loaded configuration in the form of Simplenamespace
    config: SimpleNamespace | None # Changed to Optional [Simplenamespace] and a check has been added

    # --- Config loading ---
    try:
        # Way to the configuration file USE_LLM.JSON
        config_path: Path = ENDPOINT / 'use_llm.json'
        # Checking the existence of a configuration file
        if config_path.exists():
            # Download Configuration from JSON File in Simplenamespace
            config = j_loads_ns(config_path)
            # Check that the configuration is successfully loaded
            if not config: logger.error(f'Файл конфигурации {config_path} пуст/некорректен!')
            else: logger.info(f'Конфигурация успешно загружена из {config_path}')
        else: 
            # Logging a critical error if the configuration file was not found
            logger.error(f'КРИТИЧЕСКАЯ ОШИБКА: Файл конфигурации НЕ НАЙДЕН: {config_path}!'); config = None
    except Exception as ex: 
        # Logging a critical error when loading or parsing configuration
        logger.error(f'КРИТИЧЕСКАЯ ОШИБКА при загрузке/парсинге {config_path}.', ex, exc_info=True); config = None

    # --- initialization of class attributes ---
    # LLM API Keys and Statuses
    GEMINI_API_KEY: Optional[str] = None; GEMINI_STATUS: str = 'inactive'; GEMINI_MODEL_NAME: str = ''
    
    OPENAI_API_KEY: Optional[str] = None; OPENAI_API_STATUS: str = 'inactive'; OPENAI_MODEL_NAME: str = ''
    # Search Providers API Keys and Statuses
    SERPAPI_API_KEY: Optional[str] = None
    TAVILY_API_KEY: Optional[str] = None
    # Default search providers statuses
    SEARCH_PROVIDERS_STATUS: Dict[str, str] = {"serpapi": "inactive", "duckduckgo": "active", "tavily": "inactive"}

    # --- reading settings from config ---
    try:
        # Check that the configuration was loaded
        if config:
            # LLM models settings
            if hasattr(config, 'models'):
                models_config: SimpleNamespace = config.models
                gemini_conf: Optional[SimpleNamespace] = getattr(models_config, 'gemini', None)
                GEMINI_STATUS = getattr(gemini_conf, 'status', 'inactive') if gemini_conf else 'inactive'
                GEMINI_MODEL_NAME = getattr(gemini_conf, 'model_name', '') if gemini_conf else ''
                
                openai_conf: Optional[SimpleNamespace] = getattr(models_config, 'openai', None)
                OPENAI_API_STATUS = getattr(openai_conf, 'status', 'inactive') if openai_conf else 'inactive'
                OPENAI_MODEL_NAME = getattr(openai_conf, 'model_name', '') if openai_conf else ''
                
                # Search engines can be defined in the 'Models' section (option a)
                serp_m_conf: Optional[SimpleNamespace] = getattr(models_config, 'serpapi', None)
                SEARCH_PROVIDERS_STATUS["serpapi"] = getattr(serp_m_conf, 'status', SEARCH_PROVIDERS_STATUS["serpapi"]) if serp_m_conf else SEARCH_PROVIDERS_STATUS["serpapi"]
                
                tav_m_conf: Optional[SimpleNamespace] = getattr(models_config, 'tavily', None)
                SEARCH_PROVIDERS_STATUS["tavily"] = getattr(tav_m_conf, 'status', SEARCH_PROVIDERS_STATUS["tavily"]) if tav_m_conf else SEARCH_PROVIDERS_STATUS["tavily"]
                
                ddg_m_conf: Optional[SimpleNamespace] = getattr(models_config, 'duckduckgo', None)
                SEARCH_PROVIDERS_STATUS["duckduckgo"] = getattr(ddg_m_conf, 'status', SEARCH_PROVIDERS_STATUS["duckduckgo"]) if ddg_m_conf else SEARCH_PROVIDERS_STATUS["duckduckgo"]

            # Search activities statuses can also be defined in the `Search_providers' section (option B - redistributes option a)
            if hasattr(config, 'search_providers'):
                search_config: SimpleNamespace = config.search_providers
                serp_s_conf: Optional[SimpleNamespace] = getattr(search_config, 'serpapi', None)
                SEARCH_PROVIDERS_STATUS["serpapi"] = getattr(serp_s_conf, 'status', SEARCH_PROVIDERS_STATUS["serpapi"]) if serp_s_conf else SEARCH_PROVIDERS_STATUS["serpapi"]
                
                tav_s_conf: Optional[SimpleNamespace] = getattr(search_config, 'tavily', None)
                SEARCH_PROVIDERS_STATUS["tavily"] = getattr(tav_s_conf, 'status', SEARCH_PROVIDERS_STATUS["tavily"]) if tav_s_conf else SEARCH_PROVIDERS_STATUS["tavily"]
                
                ddg_s_conf: Optional[SimpleNamespace] = getattr(search_config, 'duckduckgo', None)
                SEARCH_PROVIDERS_STATUS["duckduckgo"] = getattr(ddg_s_conf, 'status', SEARCH_PROVIDERS_STATUS["duckduckgo"]) if ddg_s_conf else SEARCH_PROVIDERS_STATUS["duckduckgo"]
        else: 
            # Warning logistics if the configuration is not loaded
            logger.warning('Config не загружен. Используются статусы по умолчанию.')
    except AttributeError as ex: 
        # Logging a critical error when reading the structure of configuration
        logger.critical(f'Ошибка чтения структуры config: {ex}. Используются статусы по умолчанию.', None, exc_info=False)
        GEMINI_STATUS = 'inactive'; OPENAI_API_STATUS = 'inactive'
        SEARCH_PROVIDERS_STATUS = {"serpapi": "inactive", "duckduckgo": "active", "tavily": "inactive"}

    # --- Installing the API keys ---
    # Trying to install the API keys from GS.credentials, then from the encirclement variables
    try:
        # An attempt to extract Gemini from GS.credentials
        try: GEMINI_API_KEY = gs.credentials.gemini.katia.api_key
        except AttributeError: pass # The error is ignored if the key is not found
        # An attempt to extract the Openai key from GS.credentials
        try: OPENAI_API_KEY = gs.credentials.openai.hypotez.api_key
        except AttributeError: pass
        # An attempt to extract Serpapi from GS.credentials
        try: SERPAPI_API_KEY = gs.credentials.serpapi.onela.api_key
        except AttributeError: pass
        # Tavily Key Tavily from GS.credentials
        try: TAVILY_API_KEY = gs.credentials.tavily.default.api_key # <- Indicate your path
        except AttributeError: pass

        # If the keys are not found in GS.credentials, an attempt to extract from the variables
        if not GEMINI_API_KEY: GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
        if not OPENAI_API_KEY: OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
        if not SERPAPI_API_KEY: SERPAPI_API_KEY = os.environ.get('SERPAPI_API_KEY')
        if not TAVILY_API_KEY: TAVILY_API_KEY = os.environ.get('TAVILY_API_KEY')

        # Installing keys in environment variables if they were found (some SDK expect them there)
        if GEMINI_API_KEY: os.environ['GOOGLE_API_KEY'] = GEMINI_API_KEY
        if OPENAI_API_KEY: os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
        if SERPAPI_API_KEY: os.environ['SERPAPI_API_KEY'] = SERPAPI_API_KEY
        if TAVILY_API_KEY: os.environ['TAVILY_API_KEY'] = TAVILY_API_KEY

        # Logging the status of configuration and the availability of keys
        logger.info(f'Config Gemini: Status={GEMINI_STATUS}, Model={GEMINI_MODEL_NAME}, Key Present={bool(GEMINI_API_KEY)}')
        logger.info(f'Config OpenAI: Status={OPENAI_API_STATUS}, Model={OPENAI_MODEL_NAME}, Key Present={bool(OPENAI_API_KEY)}')
        logger.info(f'Config SerpAPI: Status={SEARCH_PROVIDERS_STATUS.get("serpapi", "N/A")}, Key Present={bool(SERPAPI_API_KEY)}')
        logger.info(f'Config DuckDuckGo: Status={SEARCH_PROVIDERS_STATUS.get("duckduckgo", "N/A")}')
        logger.info(f'Config Tavily: Status={SEARCH_PROVIDERS_STATUS.get("tavily", "N/A")}, Key Present={bool(TAVILY_API_KEY)}')

    except ImportError: logger.warning("Модуль 'src.gs' не найден.")
    except NameError: logger.warning("Объект 'gs.credentials' не найден.")
    except Exception as ex: 
        # Error logging when installing API keys
        logger.error('Ошибка при установке API ключей в Config.', ex, exc_info=True)

# None
# Strying function
# None
async def stream_agent_execution( executor: AgentExecutor, task_input: Dict[str, Any]) -> Tuple[Optional[str], List[Dict[str, Any]]]:
    """Asynchronously performs an agent and stricts the steps of performing the task.

    Args:
        Executor (Agentexecutor): The initialized copy of Agentexecutor.
        Task_input (dict [str, any]): a dictionary with the input data for the task (for example, {'input': 'text of the task'}).

    Returns:
        Tuple [Optional [str], list [dict [str, ain]]: a motorcade, where the first element is the final response of the agent (if any),
                                                    And the second is a list of all the cups received during streaming."""
    # Initialization of variables for storing the result and intermediate data
    final_answer: Optional[str] = None
    all_chunks: List[Dict[str, Any]] = []
    run_id: Optional[str] = None # ID of the current launch of the agent
    logger.info(f'--- Начало стриминга для входа: {str(task_input)[:200]}... ---')
    try:
        # Asynchronous icon iteration on the agent Astream returned
        async for chunk in executor.astream(task_input):
            # Adding each cup to the list of all cans
            all_chunks.append(chunk)
            # Processing of cans type 'Actions' (planned actions of the agent)
            if actions := chunk.get('actions'):
                for action in actions:
                    tool: str = getattr(action, 'tool', 'N/A') # The name is used by this tool
                    tool_input: Any = getattr(action, 'tool_input', 'N/A') # Input data for tools
                    log_msg: str = getattr(action, 'log', '').strip() # Log/Thoughts of the Agent
                    logger.info(f"Планируемое действие: Tool=[{tool}], Input=[{str(tool_input)[:100]}...]")
                    if log_msg: logger.debug(f'  Log (Мысли): {log_msg}', exc_info=False)
            # Processing of cans type 'stps' (results of the actions performed)
            elif steps := chunk.get('steps'):
                for step in steps:
                    observation: Any = getattr(step, 'observation', None) # The result (observation) from the tool
                    action_log: str = getattr(step.action, 'log', '').strip() # LOG/Thoughts of the Agent before observation
                    tool_used: str = getattr(step.action, 'tool', 'N/A') # Tool that was used
                    if observation is not None: logger.info(f"Результат действия (Observation) от Tool=[{tool_used}]: {str(observation)[:300]}...")
                    if action_log: logger.debug(f"  Log (Мысли перед Observation): {action_log}", exc_info=False)
            # Processing a chunk type 'output' (the final response of the agent)
            elif output := chunk.get('output'): 
                logger.info(f'Финальный ответ: {output}'); final_answer = output
            # Processing of cans type 'Messages' (intermediate messages)
            elif messages := chunk.get('messages'):
                 for msg in messages:
                     if content := getattr(msg, 'content', None): logger.debug(f'Message Chunk: {content}', exc_info=False)
            # Extracting and logging of the ID launch of the agent if it has changed
            current_run_info: Dict[str, Any] = chunk.get('__run', {})
            current_run_id: Optional[str] = getattr(current_run_info, 'id', None)
            if current_run_id and current_run_id != run_id: 
                run_id = current_run_id; logger.debug(f'Agent Run ID: {run_id}', exc_info=False)
    except LangChainException as ex: 
        # Langchain error logging
        logger.error('Ошибка LangChain во время стриминга.', ex, exc_info=True)
    except Exception as ex: 
        # Logging of unexpected errors
        logger.error('Неожиданная ошибка во время стриминга.', ex, exc_info=True)
    logger.info(f'--- Стриминг завершен. Всего чанков: {len(all_chunks)}. ---')
    return final_answer, all_chunks
# None

class Driver:
    """LLM control class, controllers and agents of Langchain.
    Orchens the initialization of models, browser controllers and Langchain tools,
    as well as starting tasks using LLM."""
    # Reference to the configuration class
    config_class: Type[Config] = Config
    # Copies of LLM models
    gemini: Optional[BaseChatModel] = None
    openai: Optional[BaseChatModel] = None
    # List of available Langchain tools
    tools: List[Tool] = []
    # Copies of browser controllers
    browser: Optional[BrowserController] = None
    data_extractor: Optional[DataExtractionController] = None
    form_controller: Optional[FormController] = None
    screenshot_controller: Optional[ScreenshotController] = None
    download_controller: Optional[DownloadController] = None
    js_executor: Optional[JavaScriptExecutionController] = None
    state_manager: Optional[StateManager] = None
    # The flag indicating whether Driver was completely initialized (including the asynchronous part)
    _initialized: bool = False
    # API Keys for Search Services
    _serpapi_key: Optional[str] = None
    _tavily_key: Optional[str] = None
    # Search providers activity statuses
    _search_provider_statuses: Dict[str, str] = {} 
    # Parameters for initializing the browser
    _start_browser: bool
    _browser_headless: bool
    _browser_timeout: int

    def __init__(self,
                 GEMINI_API_KEY: Optional[str] = None, OPENAI_API_KEY: Optional[str] = None,
                 SERPAPI_API_KEY: Optional[str] = None, TAVILY_API_KEY: Optional[str] = None,
                 openai_model_name: Optional[str] = None, gemini_model_name: Optional[str] = None,
                 start_browser: bool = True, browser_headless: bool = True, browser_timeout: int = 30000,
                 **kwargs: Any) -> None:
        """Synchronously initializes LLM and retains parameters for asynchronous initialization.

        Args:
            Gemini_api_key (Optional [str]): API key for gemini.
            Openai_api_key (Optional [str]): API key for Openai.
            Serpapi_api_key (Optional [str]): API key for Serpapi.
            Tavily_api_key (Optional [Str]): API key for Tavily.
            Opena_Model_name (Optional [Str]): name of the Openai model.
            gemini_model_name (Optional [str]): name of the model Gemini.
            Start_browSer (Bool): flag, whether to start a browser during initialization.
            Browser_Headless (Bool): Flag, whether to start a browser in a headless mode.
            Browser_Timeout (int): Timesout for browser operations in milliseconds.
            ** KWARGS (ANY): Additional inconsistent arguments."""
        # Variables for storing keys and names of models
        openai_api_key_local: Optional[str] # Local area of visibility
        gemini_api_key_local: Optional[str] # Local area of visibility
        openai_model_name_local: str # Local area of visibility
        gemini_model_name_local: str # Local area of visibility
        openai_status_local: str # Local area of visibility
        gemini_status_local: str # Local area of visibility

        logger.info('--- Начало СИНХРОННОЙ инициализации Driver ---')
        # Parameters preservation to initialize the browser
        self._start_browser = start_browser
        self._browser_headless = browser_headless
        self._browser_timeout = browser_timeout
        # Obtaining API keys for search services from arguments or from config
        self._serpapi_key = SERPAPI_API_KEY or self.config_class.SERPAPI_API_KEY
        self._tavily_key = TAVILY_API_KEY or self.config_class.TAVILY_API_KEY
        # Copying the statuses of search providers from Config
        self._search_provider_statuses = self.config_class.SEARCH_PROVIDERS_STATUS.copy()
        # Installation of the FALSE initialization flag
        self._initialized = False

        # Initialization of the attributes of a default value
        self.openai = None; self.gemini = None; self.tools = []; self.browser = None; self.data_extractor = None; self.form_controller = None
        self.screenshot_controller = None; self.download_controller = None; self.js_executor = None; self.state_manager = None

        # Determining the API keys and names of models for Openai and Gemini
        openai_api_key_local = OPENAI_API_KEY or self.config_class.OPENAI_API_KEY
        gemini_api_key_local = GEMINI_API_KEY or self.config_class.GEMINI_API_KEY
        openai_model_name_local = openai_model_name or self.config_class.OPENAI_MODEL_NAME
        gemini_model_name_local = gemini_model_name or self.config_class.GEMINI_MODEL_NAME
        openai_status_local = self.config_class.OPENAI_API_STATUS
        gemini_status_local = self.config_class.GEMINI_STATUS

        # Installation of API keys in environment variables (for some SDK)
        if gemini_api_key_local: os.environ['GEMINI_API_KEY'] = gemini_api_key_local
        logger.info(f'Ключ джемини {os.environ['GEMINI_API_KEY']=}')
        if openai_api_key_local: os.environ['OPENAI_API_KEY'] = openai_api_key_local
        if self._serpapi_key: os.environ['SERPAPI_API_KEY'] = self._serpapi_key
        if self._tavily_key: os.environ['TAVILY_API_KEY'] = self._tavily_key

        # Initialization of LLM models
        self.openai = self._initialize_openai(openai_api_key_local, openai_status_local, openai_model_name_local)
        self.gemini = self._initialize_gemini(gemini_api_key_local, gemini_status_local, gemini_model_name_local)

        # Logging unused arguments if they are
        if kwargs: logger.warning(f'Неиспользованные аргументы: {kwargs}', exc_info=False)
        logger.info('--- Синхронная инициализация Driver завершена. Вызовите async_init() ---')

    async def async_init(self) -> bool:
        """Asynchronously initializes BrowserController, dependent controllers and Langchain tools.
        This method should be caused after synchronous __init__.

        Returns:
            Bool: True, if asynchronous initialization was successful, otherwise FALSE."""
        # Check if Driver has already been initialized
        if self._initialized: 
            logger.info('Driver уже инициализирован.'); return True
        logger.info('--- Начало АСИНХРОННОЙ инициализации Driver ---')
        # Cleaning the list of tools before new initialization
        self.tools = []
        # Asynchronous initialization of the browser and related controllers
        await self._async_initialize_browser_and_controllers(self._start_browser, self._browser_headless, self._browser_timeout)
        # Creation of Langchain tools based on initialized controllers
        self._create_tools()
        logger.info(f'Итоговый список доступных инструментов Driver: {[tool.name for tool in self.tools]}')
        # Installation of the flag of successful initialization
        self._initialized = True
        logger.info('--- Асинхронная инициализация Driver завершена ---')
        return True

    def _initialize_openai(self, api_key: Optional[str], status: str, model_name: str) -> Optional[BaseChatModel]:
        """Synchronously initializes the Openai (Chatopenai) model.

        Args:
            API_KEY (Optional [str]): API key for Openai.
            Status (str): the status of model activity ('Active' for initialization).
            Model_name (str): the name of the Openai model (for example, 'GPT-3.5-Turbo').

        Returns:
            Optional [BaseChatmodel]: Chatopenai or None copy, if initialization has failed."""
        llm: Optional[BaseChatModel] = None
        # Checking the presence of API key, active status and model name
        if api_key and status.lower() == 'active' and model_name:
            logger.info(f'Инициализация OpenAI: Model={model_name}')
            try: 
                # Creating a copy of Chatopenai
                llm = ChatOpenAI(model_name=model_name, openai_api_key=api_key, temperature=0.1)
                logger.info('OpenAI LLM инициализирован.')
            except Exception as ex: 
                # Logging the error of initialization
                logger.error('Ошибка инициализации OpenAI.', ex, exc_info=True)
        else: 
            # Warning logistics if the conditions for initialization are not fulfilled
            logger.warning(f'OpenAI LLM не инициализирован (Key={bool(api_key)}, Status={status}, Model={model_name})', exc_info=False)
        return llm

    def _initialize_gemini(self, api_key: Optional[str], status: str, model_name: str) -> Optional[BaseChatModel]:
        """Synchronously initializes the Gemini model (Chatooglegenerativeai).

        Args:
            API_KEY (Optional [str]): API Key for Google Gemini.
            Status (str): the status of model activity ('Active' for initialization).
            Model_name (str): the name of the Gemini model (for example, 'gemini-Pro').

        Returns:
            Optional [BaseChatmodel]: Chatgooglegneeratei or None copy, if initialization has failed."""
        llm: Optional[BaseChatModel] = None
        # Checking the presence of API key, active status and model name
        if api_key and status.lower() == 'active' and model_name:
            logger.info(f'Инициализация Gemini: Model={model_name}')
            try: 
                # Creation of a copy of Chatooglegnerativeai
                llm = ChatGoogleGenerativeAI(model=model_name, google_api_key=api_key, temperature=0.1, convert_system_message_to_human=True)
                logger.info('Gemini LLM инициализирован.')
            except Exception as ex: 
                # Logging the error of initialization
                logger.error('Ошибка инициализации Gemini.', ex, exc_info=True)
        else: 
            # Warning logistics if the conditions for initialization are not fulfilled
            logger.warning(f'Gemini LLM не инициализирован (Key={bool(api_key)}, Status={status}, Model={model_name})', exc_info=False)
        return llm

    async def _async_initialize_browser_and_controllers(self, start: bool, headless: bool, timeout: int) -> None:
        """Asynchronically initializes BrowserController and controllers dependent on it.

        Args:
            Start (Bool): A flag indicating whether the browser needs to be launched.
            Headless (Bool): Flag, whether to start a browser in a headless mode.
            Timeout (int): Timesout for browser operations."""
        # Reset of copies of controllers
        self.browser = None; self.data_extractor = None; self.form_controller = None; self.screenshot_controller = None; self.download_controller = None; self.js_executor = None; self.state_manager = None
        browser_started: bool = False # The flag of the successful launch of the browser
        # Check if the browser needs to run
        if not start: 
            logger.info('Иниц. браузера пропущена (start=False).'); return
        # Verification of the main BrowserController
        if not BROWSER_CONTROLLER_AVAILABLE: 
            logger.warning('BrowserController недоступен.', exc_info=False); return
        try:
            logger.info('Асинхронная инициализация BrowserController...')
            # Creating a copy of BrowserController
            self.browser = BrowserController(headless=headless, timeout=timeout)
            # Asynchronous launch of the browser
            browser_started = await self.browser.start()
            # Checking the success of the launch
            if not browser_started: 
                logger.error('Не удалось запустить BrowserController!'); self.browser = None; return
            logger.info('BrowserController асинхронно инициализирован.')
            # Initialization of dependent controllers, if the browser is successfully launched and has active Page/Context
            if self.browser and self.browser.page and self.browser.context:
                logger.info('Инициализация зависимых контроллеров...')
                # Initialization of DataextRactionController if BS4 is available
                if BS4_AVAILABLE:
                    try: self.data_extractor = DataExtractionController(); logger.info('DataExtractionController иниц.')
                    except Exception as ex: logger.warning(f'Ошибка init DataExtractionController: {ex}', exc_info=False)
                else: logger.warning('BS4 недоступен, DataExtractionController не иниц.')
                # FormController initialization
                try: self.form_controller = FormController(page=self.browser.page); logger.info('FormController иниц.')
                except Exception as ex: logger.warning(f'Ошибка init FormController: {ex}', exc_info=False)
                # Initialization ScreenshotController
                try: self.screenshot_controller = ScreenshotController(page=self.browser.page); logger.info('ScreenshotController иниц.')
                except Exception as ex: logger.warning(f'Ошибка init ScreenshotController: {ex}', exc_info=False)
                # Initialization DownloadController
                try: self.download_controller = DownloadController(page=self.browser.page); logger.info('DownloadController иниц.')
                except Exception as ex: logger.warning(f'Ошибка init DownloadController: {ex}', exc_info=False)
                # Initialization JavascriptexecutionController
                try: self.js_executor = JavaScriptExecutionController(page=self.browser.page); logger.info('JavaScriptExecutionController иниц.')
                except Exception as ex: logger.warning(f'Ошибка init JavaScriptExecutionController: {ex}', exc_info=False)
                # Initialization Statemanager
                try: self.state_manager = StateManager(context=self.browser.context, page=self.browser.page); logger.info('StateManager иниц.')
                except Exception as ex: logger.warning(f'Ошибка init StateManager: {ex}', exc_info=False)
            else: 
                # Error logging if Page/Context is not available to the browser
                logger.error('BrowserController page/context недоступны!')
        except Exception as ex:
            # Logging error with asynchronous initialization
            logger.error('Ошибка при асинхронной инициализации BrowserController.', ex, exc_info=True)
            # An attempt to close the browser if it was partially initialized
            if self.browser: await self.browser.close()
            self.browser = None # Resetting a copy of the browser

    def _create_tools(self) -> None:
        """Creates Langchain tools for active search engines and 
        Initialized browser controllers."""
        logger.info('Создание инструментов LangChain...')
        # Cleaning the list of tools
        self.tools = []
        # Synchronized calls of asynchronous tools
        def _sync_error_func(*args: Any, **kwargs: Any) -> str: return 'Ошибка: асинхронный вызов (use coroutine).'

        # --- 1. Search tools ---
        search_tool_added: bool = False # Flag, whether at least one search tool was added
        # SerpAPI (Google)
        if self._search_provider_statuses.get("serpapi") == "active":
            if self._serpapi_key:
                try:
                    # Creating a Serpapi tool
                    serp_tool = Tool(name="GoogleSearch", func=SerpAPIWrapper().run, description="Поиск Google (SerpAPI). Вход: запрос.")
                    self.tools.append(serp_tool); logger.debug('Инструмент GoogleSearch (SerpAPI) добавлен.'); search_tool_added = True
                except Exception as ex: 
                    # Logging error creating a serpapi tool
                    logger.error(f"Ошибка создания SerpAPI Tool: {ex}", exc_info=True)
            else: 
                # Warning if the serpapi key is absent with active status
                logger.warning("SerpAPI активен, но ключ SERPAPI_API_KEY не найден!")
        # Tavily Search
        if self._search_provider_statuses.get("tavily") == "active":
            if self._tavily_key:
                try:
                    # Creating a Tavily tool
                    tav_tool = TavilySearchResults(max_results=5, name="TavilySearch", description="Поиск Tavily. Вход: запрос.")
                    self.tools.append(tav_tool); logger.debug('Инструмент TavilySearch добавлен.'); search_tool_added = True
                except Exception as ex: 
                    # Logging error creating a Tavily tool
                    logger.error(f"Ошибка создания Tavily Tool: {ex}", exc_info=True)
            else: 
                # Warning if the Tavily key is absent with active status
                logger.warning("Tavily активен, но ключ TAVILY_API_KEY не найден!")
        # DuckDuckGo
        if self._search_provider_statuses.get("duckduckgo") == "active":
            try:
                # Creating the Duckduckgo tool
                ddg_tool = DuckDuckGoSearchRun(name="DuckDuckGoSearch", description="Поиск DuckDuckGo. Вход: запрос.")
                self.tools.append(ddg_tool); logger.debug('Инструмент DuckDuckGoSearch добавлен.'); search_tool_added = True
            except Exception as ex: 
                # Logging error creating the Duckduckgo tool
                logger.error(f"Ошибка создания DuckDuckGo Tool: {ex}", exc_info=True)
        # Warning if no search tool has been added
        if not search_tool_added: logger.warning("Ни один поисковый инструмент не был добавлен!")

        # --- 2. Browser tools ---
        if self.browser:
            # Asynchronous wrappers for BrowserController methods
            async def _nav(u: str) -> str: return await self.browser.navigate(u) if self.browser else 'Err:BrowserNA'
            async def _st(s: Optional[str]=None) -> str: return await self.browser.scrape_text(s) if self.browser else 'Err:BrowserNA'
            async def _sh(s: Optional[str]=None) -> str: return await self.browser.scrape_html(s) if self.browser else 'Err:BrowserNA'
            async def _ce(s: str) -> str: return await self.browser.click_element(s) if self.browser else 'Err:BrowserNA'
            # Synchronous wrapper (does not require AWAIT)
            def _gu(i: Any=None) -> str: return self.browser.get_current_url() if self.browser else 'Err:BrowserNA'
            # Creating tools for BrowserController
            browser_tools: List[Tool] = [ 
                Tool('BrowserNavigate',_sync_error_func,coroutine=_nav,description='URL Nav'), 
                Tool('BrowserScrapeText',_sync_error_func,coroutine=_st,description='Scrape Text(sel?)'), 
                Tool('BrowserScrapeHTML',_sync_error_func,coroutine=_sh,description='Scrape HTML(sel?)'), 
                Tool('BrowserClickElement',_sync_error_func,coroutine=_ce,description='Click(sel)'), 
                Tool('GetCurrentURL',_gu,description='Get URL') 
            ]
            self.tools.extend(browser_tools); logger.debug(f'Добавлено {len(browser_tools)} инструментов BrowserController.')
        else: 
            # Warning if BrowserController is not initialized
            logger.warning('Инструменты BrowserController не созданы.')

        # --- 3. Data extraction tools ---
        if self.data_extractor:
            # Wrapping for find_Links, processing input dictionary
            def _fl_wrap(p: Any) -> Union[List[str], Dict[str, str]]:
                if not isinstance(p, dict): return {'error': 'Err:BadInput'}
                if 'html' not in p: return {'error': 'Err:NoHTML'}
                try: 
                    base_url_val: Optional[str] = p.get('base_url') or (self.browser.get_current_url() if self.browser else None)
                    return self.data_extractor.find_links(p['html'], base_url_val) if self.data_extractor else {'error':'Err:ExtractorNA'}
                except Exception as ex: 
                    logger.error("FindPageLinks Ошибка", ex, exc_info=True); return {'error': f'Err:{ex}'}
            # Creation of tools for DataextractionController
            extract_tools: List[Tool] = [ 
                Tool('ExtractProductSchema', lambda h: self.data_extractor.extract_product_details(h) if self.data_extractor else 'Err:ExtractorNA', description='Extract Product'), 
                Tool('ExtractContactInfo', lambda t: self.data_extractor.extract_contact_info(t) if self.data_extractor else 'Err:ExtractorNA', description='Extract Contact'), 
                Tool('FindPageLinks', _fl_wrap, description="Find Links {'html':...,'base_url':?}") 
            ]
            self.tools.extend(extract_tools); logger.debug(f'Добавлено {len(extract_tools)} инструментов DataExtraction.')
        else: 
            # Warning if DataEXTRACTRACTROLLER is not initialized
            logger.warning('Инструменты DataExtractionController не созданы.')

        # --- 4. Form control tools ---
        if self.form_controller:
            # Asynchronous wrappers for FormController methods
            async def _fff(p: Dict[str,Any]) -> str: return await self.form_controller.fill_input_field(p['selector'],p['value']) if self.form_controller and isinstance(p,dict) else 'Err:FormNA/BadInput'
            async def _sdd(p: Dict[str,Any]) -> str: return await self.form_controller.select_dropdown_option(p['selector'],value=p.get('value'),label=p.get('label')) if self.form_controller and isinstance(p,dict) else 'Err:FormNA/BadInput'
            async def _sf(p: Dict[str,Any]) -> str: return await self.form_controller.submit_form(form_selector=p.get('form_selector'),submit_button_selector=p.get('submit_button_selector')) if self.form_controller and isinstance(p,dict) else 'Err:FormNA/BadInput'
            # Creating tools for FormController
            form_tools: List[Tool] = [ 
                Tool('FillFormField',_sync_error_func,coroutine=_fff,description="Fill {'sel':...,'val':...}"), 
                Tool('SelectDropdown',_sync_error_func,coroutine=_sdd,description="Select {'sel':...,'val':?/'lbl':?}"), 
                Tool('SubmitForm',_sync_error_func,coroutine=_sf,description="Submit {'form_sel':?,'btn_sel':?}") 
            ]
            self.tools.extend(form_tools); logger.debug(f'Добавлено {len(form_tools)} инструментов FormController.')
        else: 
            # Warning if FormController is not initialized
            logger.warning('Инструменты FormController не созданы.')

        # --- 5. Screenshots tool ---
        if self.screenshot_controller:
            # Asynchronous wrapper for the Take_Scrence
            async def _ss(p: Dict[str,Any]) -> str: return await self.screenshot_controller.take_screenshot(p['save_path'],full_page=p.get('full_page',True),selector=p.get('selector')) if self.screenshot_controller and isinstance(p,dict) else 'Err:SSNA/BadInput'
            # Creating a TakeScrenceenShot tool
            self.tools.append(Tool('TakeScreenshot',_sync_error_func,coroutine=_ss,description="Screenshot {'path':...,'full':?,'sel':?}"))
            logger.debug('Инструмент TakeScreenshot добавлен.')
        else: 
            # Warning if ScreenshotController is not initialized
            logger.warning('Инструмент TakeScreenshot не создан.')

        # --- 6. Loading tool ---
        if self.download_controller:
            # Asynchronous rotation for the click_and_download method
            async def _dl(p: Dict[str,Any]) -> str: return await self.download_controller.click_and_download(p['click_selector'],p['save_directory'],timeout=p.get('timeout',60000)) if self.download_controller and isinstance(p,dict) else 'Err:DLNA/BadInput'
            # Creating the Clickanddownload tool
            self.tools.append(Tool('ClickAndDownload',_sync_error_func,coroutine=_dl,description="Download {'clk_sel':...,'dir':...,'to':?}"))
            logger.debug('Инструмент ClickAndDownload добавлен.')
        else: 
            # Warning if downloadController is not initialized
            logger.warning('Инструмент ClickAndDownload не создан.')

        # --- 7.
        if self.js_executor:
            # Asynchronous rotation for the Execute_Script method
            async def _ejs(s: str) -> Union[str, Any]: return await self.js_executor.execute_script(s) if self.js_executor else 'Err:JsExecNA'
            # Creating an ExecuteJavascript tool
            self.tools.append(Tool('ExecuteJavaScript',_sync_error_func,coroutine=_ejs,description="JS Exec (WARN!)"))
            logger.debug('Инструмент ExecuteJavaScript добавлен.')
        else: 
            # Warning if JavaScriptexecitationController is not initialized
            logger.warning('Инструмент ExecuteJavaScript не создан.')

        # --- 8. Status management tools ---
        if self.state_manager:
            # Asynchronous wrapper for Statemanager methods
            async def _gc(u: Optional[str]=None) -> Union[List[Dict[str, Any]],str]: return await self.state_manager.get_cookies(u) if self.state_manager else 'Err:StateNA'
            async def _cc() -> str: return await self.state_manager.clear_cookies() if self.state_manager else 'Err:StateNA'
            async def _cs() -> str: return await self.state_manager.clear_storage() if self.state_manager else 'Err:StateNA'
            # Synchronous wrapper for login (is a plug)
            def _l(*a: Any, **kw: Any) -> str: return self.state_manager.login(*a, **kw) if self.state_manager else 'Err:StateNA'
            # Creating tools for Statemanager
            state_tools: List[Tool] = [ 
                Tool('GetCookies',_sync_error_func,coroutine=_gc,description="Get Cookies(url?)"), 
                Tool('ClearCookies',_sync_error_func,coroutine=_cc,description="Clear Cookies"), 
                Tool('ClearStorage',_sync_error_func,coroutine=_cs,description="Clear Storage"), 
                Tool('Login',_l,description="Login(stub)") 
            ]
            self.tools.extend(state_tools); logger.debug(f'Добавлено {len(state_tools)} инструментов StateManager.')
        else: 
            # Warning if Statemanager is not initialized
            logger.warning('Инструменты StateManager не созданы.')

    # --- Методы run_task, stream_task, __del__, close, _get_agent_executor ---
    async def _get_agent_executor(self, llm: BaseChatModel) -> Optional[AgentExecutor]:
        """Creates and returns Agentexecutor based on LLM provided and affordable tools.

        Args:
            LLM (BaseChatmodel): Initialized LLM (Gemini or Openai) model.

        Returns:
            Optional [Agentexecutor]: Agentexecutor or None copy, if the creation failed."""
        # Driver initialization verification
        if not self._initialized: 
            logger.error('Driver не инициализирован!'); return None
        # Checking the availability of LLM
        if not llm: 
            logger.error('LLM не предоставлена.'); return None
        # Checking the availability of tools
        if not self.tools: 
            logger.error('Инструменты не созданы.'); return None
        
        # Variables for storage of industrial executive agent and agentexecutor
        prompt: Any
        agent_runnable: Any
        agent_executor: AgentExecutor
        try:
            # Loading standard Prompt from Langchain Hub
            prompt = hub.pull('hwchase17/react')
            logger.debug(f'Создание агента: LLM={type(llm).__name__}, Tools={[t.name for t in self.tools]}')
            # Creation of a performed agent (Runnable)
            agent_runnable = create_react_agent(llm=llm, tools=self.tools, prompt=prompt)
            # Creating Agentexecutor
            agent_executor = AgentExecutor(
                agent=agent_runnable, 
                tools=self.tools, 
                verbose=True, # Inclusion of detailed logging of agent steps
                handle_parsing_errors=True, # Parsing error processing llm response
                max_iterations=30, # The maximum number of agent iterations
                max_execution_time=300.0 # The maximum time of the task in seconds
            )
            logger.info('AgentExecutor создан.'); return agent_executor
        except Exception as ex: 
            # Logging errors of creating agentexecutor
            logger.error('Ошибка создания AgentExecutor.', ex, exc_info=True); return None

    async def run_task(self, task: str, use_gemini: bool = True) -> Optional[str]:
        """It launches the task using the selected LLM and returns the final result.
        It processes errors, including Google Gemini and Duckduckgo quota errors, with repeated attempts logic.

        Args:
            TASK (str): the text of the task for performing an agent.
            Use_Gemini (Bool): flag, use Gemini (True) or Openai (False).

        Returns:
            Optional [str]: a string with the final response of an agent or None/line with an error in case of failure."""
        # Lazy asynchronous initialization if it has not yet been completed
        if not self._initialized:
            init_ok: bool = await self.async_init()
            if not init_ok: 
                logger.error('Ошибка инициализации Driver для run_task.'); return None
            logger.info("Ленивая инициализация Driver завершена успешно.")

        # Determining the name of the model and the choice of LLM
        model_name: str = 'Gemini' if use_gemini else 'OpenAI'
        selected_llm: Optional[BaseChatModel] = self.gemini if use_gemini else self.openai
        # Variables for Agentexecutor, data of the result, response and meters
        agent_executor: Optional[AgentExecutor]
        result_data: Optional[Dict[str, Any]] = None
        final_answer_raw: Optional[str] = None
        retry_count: int = 0
        max_retries: int = 3 # The maximum number of repeated attempts

        logger.info(f"Запуск run_task ({model_name}): '{task[:100]}...'")
        # Check, whether the selected LLM is initialized
        if not selected_llm: 
            logger.error(f'LLM ({model_name}) не инициализирована.'); return None
        # Obtaining Agentexecutor
        agent_executor = await self._get_agent_executor(selected_llm)
        if not agent_executor: return None

        # --- The beginning of the cycle of repeated attempts ---
        while retry_count <= max_retries:
            try:
                logger.info(f'Вызов agent_executor.ainvoke ({model_name}) (Попытка {retry_count + 1}/{max_retries + 1})...')
                # Asynchronous challenge of an agent to complete the task
                result_data = await agent_executor.ainvoke({'input': task})
                # Extracting the final response from the result
                final_answer_raw = result_data.get('output')
                logger.info(f'Агент ({model_name}) успешно завершил run_task.')
                # Warning if the final answer is absent
                if final_answer_raw is None: 
                    logger.warning(f'Финальный ответ ("output") отсутствует ({model_name}). Result: {result_data}', exc_info=False)
                break # Successful execution, exit from the cycle

            except ValueError as ex_val:
                # Valuerror processing (can be caused, for example, by the parsing error in Langchain)
                logger.warning(f"Обработанная ошибка ValueError ({model_name}): {ex_val}", exc_info=False)
                final_answer_raw = f"Задача не выполнена: {ex_val}"; break # Exit from the cycle

            except google_api_exceptions.ResourceExhausted as ex_quota:
                # Google Gemini quota processing
                retry_count += 1
                logger.error(f"Ошибка квоты Google Gemini ({model_name}) (Попытка {retry_count}/{max_retries}).", ex_quota, exc_info=False)
                # Verification of the exceeding the limit of attempts
                if retry_count > max_retries:
                    logger.error(f"Превышен лимит ({max_retries}) попыток Google."); final_answer_raw = f"Ошибка: Превышена квота Google Gemini после {max_retries} попыток."; break
                
                # Determination of delay before re -attempt
                retry_delay_seconds: int = 60; delay_extracted: bool = False
                # An attempt to extract a recommended delay from metadata exclusion
                if hasattr(ex_quota, 'metadata') and ex_quota.metadata:
                     for item in ex_quota.metadata:
                         if item[0] == 'retry-delay':
                            try:
                                delay_info: Dict[str, Any] = json.loads(item[1])
                                retry_delay_seconds = max(1, int(delay_info.get('seconds', retry_delay_seconds)))
                                delay_extracted = True; break
                            except Exception as parse_ex: 
                                logger.warning(f"Не удалось распарсить retry-delay: '{item[1]}'. Ошибка: {parse_ex}", exc_info=False)
                delay_msg: str = f"Рекомендуемая задержка: {retry_delay_seconds} сек." if delay_extracted else f"Используется задержку по умолчанию: {retry_delay_seconds} сек."
                logger.info(f"{delay_msg} Ожидание перед повторной попыткой (Google)..."); await asyncio.sleep(retry_delay_seconds)

            # --- a new error processing unit DDG ---
            except DuckDuckGoSearchException as ex_ddg:
                # Exception processing from Duckducgosearch
                # Checking whether this is a Rate Limit error (by keywords or code)
                if "ratelimit" in str(ex_ddg).lower() or "202" in str(ex_ddg): 
                    retry_count += 1
                    logger.error(f"Ошибка Rate Limit DuckDuckGo ({model_name}) (Попытка {retry_count}/{max_retries}).", ex_ddg, exc_info=False)
                    # Verification of the exceeding the limit of attempts
                    if retry_count > max_retries:
                        logger.error(f"Превышен лимит ({max_retries}) попыток DDG."); final_answer_raw = f"Ошибка: Rate Limit DuckDuckGo после {max_retries} попыток."; break

                    # Installation of a fixed delay for DDG (for example, 30 seconds)
                    ddg_retry_delay_seconds: int = 30
                    logger.info(f"Ожидание {ddg_retry_delay_seconds} сек. перед повторной попыткой (DDG)...")
                    await asyncio.sleep(ddg_retry_delay_seconds)
                else:
                    # Another error from DDG - do not repeat, leave the cycle
                    logger.error(f"Неожиданная ошибка DuckDuckGo ({model_name}).", ex_ddg, exc_info=True)
                    final_answer_raw = f"Ошибка DuckDuckGo: {ex_ddg}"; break
            # --- The end of the new block ---

            except LangChainException as ex_lc:
                # Langchain common errors processing
                logger.error(f'Ошибка LangChain ({model_name}).', ex_lc, exc_info=True); final_answer_raw = f"Ошибка LangChain: {ex_lc}"; break # Exit from the cycle
            except Exception as ex_other:
                # Processing other unexpected errors
                logger.error(f'Неожиданная ошибка ({model_name}).', ex_other, exc_info=True); final_answer_raw = f"Неожиданная ошибка: {ex_other}"; break # Exit from the cycle
        # --- The end of the cycle of repeated attempts ---

        # --- post-processing an answer ---
        # Check that the final answer is obtained and is a line
        if final_answer_raw and isinstance(final_answer_raw, str):
            try:
                # Parsing to answer as json
                parsed_data: Any = json.loads(final_answer_raw)
                # Special processing for the case when the agent returned the summary instead of the URL list
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
                    # Return of the original Json answer
                    return final_answer_raw
            except json.JSONDecodeError:
                # If the answer is not json, we log in the warning and return as is
                logger.warning(f"Агент ({model_name}) вернул не JSON ответ: {final_answer_raw[:200]}...")
                return final_answer_raw
            except Exception as post_ex:
                # Logging the post-processing error
                logger.error(f"Ошибка пост-обработки ответа агента ({model_name}): {post_ex}", None, exc_info=True)
                return final_answer_raw # Return of a raw response with a post-processing error
        else:
            # None return or what was in Final_answer_RaW, if this is not a line
            return final_answer_raw

    async def stream_task(self, task: str, use_gemini: bool = True) -> Tuple[Optional[str], List[Dict[str, Any]]]:
        """It launches the task and strip steps of the agent.

        Args:
            TASK (str): the text of the task for performing an agent.
            Use_Gemini (Bool): flag, use Gemini (True) or Openai (False).

        Returns:
            Tuple [Optional [Str], List [dict [str, a ain]]: a motorcade, where the first element is the final response of the agent,
                                                        And the second is a list of all the cups received during streaming."""
        # Lazy initialization, if necessary
        init_ok: bool # Variable announcement to IF block
        if not self._initialized: 
            init_ok = await self.async_init()
            if not init_ok: 
                logger.error("Ошибка инициализации Driver для stream_task."); return None, []
        
        # Determining the name of the model and the choice of LLM
        model_name: str = 'Gemini' if use_gemini else 'OpenAI'
        selected_llm: Optional[BaseChatModel] = self.gemini if use_gemini else self.openai
        # Variables for Agentexecutor, response and chaank
        agent_executor: Optional[AgentExecutor]
        final_answer: Optional[str] = None
        all_chunks: List[Dict[str, Any]] = []
        
        logger.info(f"Запуск stream_task ({model_name}): '{task[:100]}...'")
        # Verification of LLM initialization
        if not selected_llm: 
            logger.error(f'LLM ({model_name}) не инициализирована.'); return None, []
        # Obtaining Agentexecutor
        agent_executor = await self._get_agent_executor(selected_llm)
        if not agent_executor: return None, []
        
        logger.info(f'Начало стриминга ({model_name})...');
        try: 
            # Calling the streaming function
            final_answer, all_chunks = await stream_agent_execution(executor=agent_executor, task_input={'input': task})
        except google_api_exceptions.ResourceExhausted as ex: 
            # Google quota error processing
            logger.error(f"Ошибка квоты Google в stream_task ({model_name}).", ex, exc_info=False)
            final_answer = "Ошибка: Превышена квота Google."; all_chunks = [] # Installation of error messages
        except Exception as ex: 
            # Processing other unexpected errors
            logger.error(f"Неожиданная ошибка в stream_task ({model_name}).", ex, exc_info=True)
            final_answer = f"Ошибка стриминга: {ex}" # Installation of error messages
            all_chunks = [] # Cleaning of cups with an error
        logger.info(f'Стриминг ({model_name}) завершен.'); return final_answer, all_chunks

    def __del__(self) -> None:
        """Destructor to attempt the asynchronous closure of the browser.
        Note: Reliable asynchronous closure from the destructor is difficult.
        A clear call is recommended `aWAIT DRIVER.Close ()`."""
        if self.browser:
            logger.info('Попытка закрытия BrowserController из __del__...'); 
            loop: Optional[asyncio.AbstractEventLoop]
            try: 
                # Obtaining the current event cycle
                loop = asyncio.get_event_loop_policy().get_event_loop()
            except RuntimeError: 
                # The cycle of events may already be closed or not existing
                loop = None
            # Check whether the event cycle has been launched
            if loop and loop.is_running(): 
                logger.warning("__del__: Невозможно надежно вызвать async close из раб. цикла.")
            else: 
                logger.warning("__del__: Нет активного цикла событий для вызова async close.")
            logger.warning("Рекомендуется явно вызывать 'await driver.close()'.")

    async def close(self) -> None:
        """Asynchronously closes the browser (if it was initialized) and releases the resources of Playwright.
        Drops the Driver initialization flag."""
        if self.browser: 
            logger.info("Явный вызов async close()..."); 
            await self.browser.close() # Asynchronous closing of the browser
            self.browser = None # Resetting a copy of the browser
        # Reset of the flag of initialization
        self._initialized = False

# --- function of Main for demonstration ---
async def main() -> None:
    """The main asynchronous function for demonstrating the work of the Driver class.
    It initializes Driver, checks the availability of tools, forms and starts the task."""
    # Initialization of variables
    driver: Optional[Driver] = None
    init_success: bool = False
    search_available: bool = False
    browser_core_available: bool = False
    extraction_available: bool = False
    interaction_available: bool = False
    available_tool_names: List[str] = []
    task_to_run: Optional[str] = None
    llm_to_test_run: List[Tuple[str, bool]] = [] # List of motorcies (LLM name, Use_Gemini flag)
    # Variables for use inside cycles and blocks Try
    name_llm: str # Another name is used so as not to conflict with NAME from Langchain.agents.Tool
    flag_use_gemini: bool # Similarly
    start_time: float
    end_time: float
    result: Optional[str]
    parsed_result: Any
    product_category: str
    num_links_str: str
    search_query: str
    search_tool_name_main: str # Another name is used

    try:
        logger.info('='*20 + ' Начало инициализации Driver ' + '='*20)
        # Creating a Driver copy with default settings (launching a browser, headless mode)
        driver = Driver(start_browser=True, browser_headless=True)
        # Asynchronous initialization of Driver
        init_success = await driver.async_init()
        if not init_success: 
            logger.critical('Асинхронная инициализация Driver не удалась.'); return
        logger.info('='*20 + ' Завершение инициализации Driver ' + '='*20)
    except Exception as ex: 
        # Logging a critical error of initialization
        logger.critical('Крит. ошибка инициализации Driver.', ex, exc_info=True)
        # An attempt to close the driver if he was partially initialized
        if driver: await driver.close() 
        return # Exit from the Main function in case of error
        

    try:
        # Checking the accessibility of tools after initialization
        logger.info('Проверка доступности инструментов...')
        if driver: # Check that Driver is not none
            available_tool_names = [tool.name for tool in driver.tools]
            logger.info(f'Инструменты: {available_tool_names}')
            # Determining the availability of search tools
            search_tools: List[str] = [name_tool for name_tool in available_tool_names if name_tool in ["GoogleSearch", "TavilySearch", "DuckDuckGoSearch"]]
            search_available = bool(search_tools)
            logger.info(f"Поиск доступен: {search_tools if search_available else 'Нет'}")
            # Determining the availability of basic browser tools
            browser_core_available = all(n in available_tool_names for n in ['BrowserNavigate', 'BrowserScrapeText'])
            # Determining the availability of the product extraction tool
            extraction_available = 'ExtractProductSchema' in available_tool_names
            # Determining the availability of interaction tools (click, filling out forms)
            interaction_available = all(n in available_tool_names for n in ['BrowserClickElement', 'FillFormField'])
            logger.info(f'Статус: Поиск={search_available}, Браузер={browser_core_available}, Экстракция={extraction_available}, Взаимодействие={interaction_available}')

            # Choosing a search tool for priority
            search_tool_name_main = "DuckDuckGoSearch" # at default
            if 'TavilySearch' in search_tools: search_tool_name_main = 'TavilySearch'
            elif 'GoogleSearch' in search_tools: search_tool_name_main = 'GoogleSearch'

            # The formation of the task depending on the available tools
            if search_available and browser_core_available and extraction_available:
                logger.info('Формируем СЛОЖНУЮ задачу.'); 
                product_category = 'Электрические зубные щетки'; num_links_str = 'одну'
                task_to_run = f'''** Role: ** web-agent. ** Purpose: ** Find {num_links_str} URL of goods ('{Product_category}') through {search_tool_name_main}, go, extract json (template 1). ** Plan: ** 1. `{Search_tool_name_main}` -> 2. `Browsernavigate` -> 3.` Browserscrapehtml` -> 4. `Extractproductschema` -> 5.` Browserscraftext` -> 6. Return Json (template 1). ** Template 1: ** {..., "webpage_type": "product", "data": {{"name": "<en name/n/a>", ..., "raw": "<Original Text>"}}}}}}}}}}}}}}}}}}}}}}}}}}}'''
            elif search_available: 
                logger.info('Формируем задачу ТОЛЬКО для поиска.'); 
                search_query = 'Последние новости AI'
                task_to_run = f'Используй {search_tool_name_main} для поиска: "{search_query}".'
            else: 
                logger.warning('Ключевые инструменты недоступны.'); 
                task_to_run = 'Что такое рекурсия?' # A simple task that does not require tools

            # Assessment of the number of tokens for the task (if the task is formed)
            if task_to_run:
                print(f'\nЗадача:\n{"-"*20}\n{task_to_run}\n{"-"*20}'); print("\n--- Оценка токенов ---")
                if driver.gemini: 
                    try: 
                        print(f"Gemini ~ {driver.gemini.get_num_tokens(task_to_run)} ток.") 
                    except Exception: 
                        # Get_num_tokens errors are ignored
                        ...
                if driver.openai: 
                    try: 
                        print(f"OpenAI ~ {driver.openai.get_num_tokens(task_to_run)} ток.") 
                    except Exception: 
                        # Get_num_tokens errors are ignored
                        ...
                print("-" * 30)
            else: 
                logger.error('Не удалось сформировать задачу.'); return

            print('\n' + '='*15 + ' Запуск run_task ' + '='*15)
            # LLM List Formation for Testing
            llm_to_test_run = []
            if driver.gemini and Config.GEMINI_STATUS.lower() == 'active': llm_to_test_run.append(('Gemini', True))
            if driver.openai and Config.OPENAI_API_STATUS.lower() == 'active': llm_to_test_run.append(('OpenAI', False))
            
            # Check if there are active LLM for testing
            if not llm_to_test_run: 
                print('[!] Нет АКТИВНЫХ LLM.'); return

            # Starting the task with each active LLM
            for name_llm, flag_use_gemini in llm_to_test_run:
                print(f'\n--- Запуск run_task с {name_llm} ---'); 
                start_time = asyncio.get_event_loop().time() # We cut out the start time
                try:
                    # Performing the task
                    result = await driver.run_task(task_to_run, use_gemini=flag_use_gemini)
                    end_time = asyncio.get_event_loop().time() # We cut the end time
                    print(f'\n[Результат ({name_llm}) - {end_time - start_time:.2f} сек]:')
                    try: # An attempt to a beautiful output json
                        if isinstance(result, str) and (result.strip().startswith('[') or result.strip().startswith('{')): 
                            parsed_result = json.loads(result); print(parsed_result)
                        elif isinstance(result, str) and result.startswith('Ошибка:'): 
                            print(f'[!] {result}') # Error output
                        else: 
                            print(result if result is not None else '[!] Нет ответа.')
                    except Exception: 
                        # If it was not possible to paple a json or other output error
                        print(result if result is not None else '[!] Нет ответа.')
                        ... # Ignoring the output error
                        
                except Exception as ex: 
                    # Error processing when performing run_task
                    end_time = asyncio.get_event_loop().time()
                    print(f'\n[!!!] Ошибка ({name_llm}): {ex} ({end_time - start_time:.2f} сек)')
                    logger.error(f'Ошибка run_task ({name_llm})', ex, exc_info=True)
                    ... # Ignoring error to continue with other LLM, if there is
        else:
            logger.error("Экземпляр Driver не был успешно инициализирован (driver is None).")

    finally: 
        # Guaranteed closure of the driver at the end of the work
        if driver: await driver.close() 
        logger.info('='*20 + ' Завершение работы main ' + '='*20)

if __name__ == '__main__':
    print('Запуск основной асинхронной функции main...')
    print("Напоминание: Установлены ли playwright, beautifulsoup4, lxml, langchain*, google-search-results, duckduckgo-search, python-dotenv, google-api-core, tavily-python?")
    print("Выполнен ли 'playwright install'?")
    print("-" * 40)
    # Launch of asynchronous function Main
    asyncio.run(main())
    print('Программа завершена.')
