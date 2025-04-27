## \file src/webdriver/ai_browser/use_ai.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для запуска задач с использованием LLM через LangChain и стандартных агентов.
==================================================================================
(Использует инструменты, взаимодействующие с BrowserController и/или API поиска)

Предоставляет функциональность для:
- Конфигурирования моделей (Gemini, OpenAI).
- Установки API ключей.
- Запуска задачи с использованием LLM и доступных инструментов (веб-поиск, браузер).
- Выполнения задачи до конечного результата (`run_task`).
- Стриминга выполнения задачи (`stream_task`).

Зависимости:
    - langchain-openai, langchain-google-genai, langchain-core, langchainhub, langchain
    - langchain-community (для SerpAPIWrapper)
    - google-search-results (для SerpAPIWrapper)
    - python-dotenv
    - browser_use (или ваш модуль с BrowserController)
    - src.gs, src.logger, src.utils, header

.. module:: src.webdriver.ai_browser.use_ai
"""

import os
import asyncio
from types import SimpleNamespace
from typing import List, Dict, Any, Optional, Callable, Type, Tuple, AsyncIterator
from pathlib import Path
import logging # Стандартный logging

# LangChain компоненты
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent, Tool
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.exceptions import LangChainException
from langchain import hub
# --- Инструмент для поиска через API ---
# Убедитесь, что установлена: pip install google-search-results
from langchain_community.utilities import SerpAPIWrapper
from browser_use import Agent

# --- Внутренние модули ---
import header
from header import __root__
from src import gs
from src.logger import logger
from src.utils.jjson import j_loads, j_loads_ns
from src.utils.printer import pprint as print

try:
    from .controlers import BrowserController # Пример
    BROWSER_CONTROLLER_AVAILABLE = True
except ImportError as ex:
    logger.warning("Не удалось импортировать BrowserController. Браузерные инструменты будут недоступны.", ex, exc_info=False)
    class BrowserController: # Заглушка
        def __init__(self,*args,**kwargs): pass
        def search(self,q): return "Ошибка: Контроллер браузера недоступен."
        def navigate(self,u): return "Ошибка: Контроллер браузера недоступен."
        def scrape_text(self,s=None): return "Ошибка: Контроллер браузера недоступен."
        def click_element(self,s): return "Ошибка: Контроллер браузера недоступен."
        def close(self): pass
    BROWSER_CONTROLLER_AVAILABLE = False


from dotenv import load_dotenv
load_dotenv()

class Config:
    """ Класс для хранения статической конфигурации приложения. """
    ENDPOINT: Path = __root__ / 'src' / 'webdriver' / 'llm_driver'
    # Загрузка конфига при определении класса
    config: SimpleNamespace = j_loads_ns(ENDPOINT/'use_llm.json') # Может вызвать ошибку, если файл не найден/некорректен

    # Атрибуты класса с значениями по умолчанию
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_STATUS: str = 'inactive'
    GEMINI_MODEL_NAME: str = ''
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_API_STATUS: str = 'inactive'
    OPENAI_MODEL_NAME: str = ''

    if config: 
        try:

            os.environ['GEMINI_API_KEY']  = GEMINI_API_KEY = gs.credentials.gemini.kazarinov.api_key
            os.environ['OPENAI_API_KEY']  = OPENAI_API_KEY = gs.credentials.openai.hypotez.api_key
            os.environ['SERPAPI_API_KEY'] =  gs.credentials.serpapi.onela.api_key 

            GEMINI_STATUS = config.models.gemini.status
            GEMINI_MODEL_NAME = config.models.gemini.model_name

            OPENAI_API_STATUS = config.models.openai.status
            OPENAI_MODEL_NAME = config.models.openai.model_name

            logger.info(f"Config Gemini: Status={GEMINI_STATUS}, Model={GEMINI_MODEL_NAME}, Key Present={bool(GEMINI_API_KEY)}")
            logger.info(f"Config OpenAI: Status={OPENAI_API_STATUS}, Model={OPENAI_MODEL_NAME}, Key Present={bool(OPENAI_API_KEY)}")

        except Exception as ex:
            logger.error("Неожиданная ошибка при инициализации Config.", ex, exc_info=True)
            ...
            # Атрибуты класса останутся со значениями по умолчанию
    else:
        # Эта ветка выполнится, если j_loads_ns вернул Falsy значение
        logger.error("Ошибка загрузки конфигурации: j_loads_ns вернул некорректное значение.", None, exc_info=False)
        ...
        raise ValueError("Не удалось загрузить конфигурацию из use_ai.json")

# ===============================================================
# Функция стриминга 
# ===============================================================
async def stream_agent_execution(executor: AgentExecutor, task_input: Dict[str, Any], logger_instance) -> Tuple[Optional[str], List[Dict[str, Any]]]:
    """ Асинхронно выполняет агент через AgentExecutor и стримит шаги. """
    final_answer: Optional[str] = None; all_chunks: List[Dict[str, Any]] = []; run_id: Optional[str] = None
    logger_instance.info(f"--- Начало стриминга для входа: {task_input} ---")
    try:
        async for chunk in executor.astream(task_input):
            all_chunks.append(chunk)
            current_run_info = chunk.get("__run", {}); current_run_id = getattr(current_run_info, 'id', None)
            if current_run_id and current_run_id != run_id: run_id = current_run_id; logger_instance.debug(f"Agent Run ID: {run_id}", exc_info=False)
            if actions := chunk.get("actions"):
                for action in actions:
                    tool=getattr(action, 'tool', 'N/A'); tool_input=getattr(action, 'tool_input', 'N/A'); log_msg=getattr(action, 'log', '').strip()
                    logger_instance.info(f"Планируемое действие: Tool={tool}, Input={tool_input}")
                    if log_msg: logger_instance.debug(f"  Log (Мысли): {log_msg}", exc_info=False)
            elif steps := chunk.get("steps"):
                for step in steps:
                    observation = getattr(step, 'observation', None)
                    if observation is not None: logger_instance.info(f"Результат действия (Observation): {str(observation)[:500]}...")
                    else: logger_instance.debug(f"Получен шаг без observation: {step}", exc_info=False)
            elif output := chunk.get("output"): logger_instance.info(f"Финальный ответ: {output}"); final_answer = output
            elif messages := chunk.get("messages"):
                for msg in messages:
                    if content := getattr(msg, 'content', None): logger_instance.debug(f"Message Chunk: {content}", exc_info=False)
    except LangChainException as e: logger_instance.error("Ошибка LangChain во время стриминга.", e, exc_info=True)
    except Exception as e: logger_instance.error("Неожиданная ошибка во время стриминга.", e, exc_info=True)
    logger_instance.info(f"--- Стриминг завершен ---"); return final_answer, all_chunks
# ===============================================================


class Driver:
    """
    Класс для управления LLM и запуска агентов LangChain с веб-инструментами.
    """
    config: Config = Config
    gemini: Optional[ChatGoogleGenerativeAI] = None
    openai: Optional[ChatOpenAI] = None
    tools: List[Tool] = [] # Инициализируем пустым списком
    browser: Optional[BrowserController] = None
    search_api: SerpAPIWrapper

    def __init__(self,
                 GEMINI_API_KEY: Optional[str] = None,
                 OPENAI_API_KEY: Optional[str] = None,
                 openai_model_name: Optional[str] = None,
                 gemini_model_name: Optional[str] = None,
                 start_browser: bool = True,
                 **kwargs):
        """
        Инициализирует LLM, контроллер браузера и инструменты.
        """
        # Получение ключей и моделей
        openai_api_key = OPENAI_API_KEY or Config.OPENAI_API_KEY
        gemini_api_key = GEMINI_API_KEY or Config.GEMINI_API_KEY
        openai_model_to_use = openai_model_name or Config.OPENAI_MODEL_NAME
        gemini_model_to_use = gemini_model_name or Config.GEMINI_MODEL_NAME

        # --- Инициализация LLM ---
        if openai_api_key and Config.OPENAI_API_STATUS.lower() == 'active':
            logger.info(f"Инициализация OpenAI: Model={openai_model_to_use}")
            os.environ['OPENAI_API_KEY'] = openai_api_key
            try: self.openai = ChatOpenAI(model_name=openai_model_to_use, openai_api_key=openai_api_key)
            except Exception as ex: logger.error("Ошибка инициализации OpenAI.", ex, exc_info=True); self.openai = None
            if self.openai: logger.info("OpenAI LLM инициализирован.")
        else: logger.warning(f"OpenAI LLM не инициализирован (Key={bool(openai_api_key)}, Status={Config.OPENAI_API_STATUS})", exc_info=False); self.openai = None

        if gemini_api_key and Config.GEMINI_STATUS.lower() == 'active':
            logger.info(f"Инициализация Gemini: Model={gemini_model_to_use}")
            os.environ['GOOGLE_API_KEY'] = gemini_api_key
            logger.debug("Установлена переменная окружения GOOGLE_API_KEY.", exc_info=False)
            try: self.gemini = ChatGoogleGenerativeAI(model=gemini_model_to_use, google_api_key=gemini_api_key)
            except Exception as ex: logger.error("Ошибка инициализации Gemini.", ex, exc_info=True); self.gemini = None
            if self.gemini: logger.info("Gemini LLM инициализирован.")
        else: logger.warning(f"Gemini LLM не инициализирован (Key={bool(gemini_api_key)}, Status={Config.GEMINI_STATUS})", exc_info=False); self.gemini = None

        # --- Инициализация инструментов ---
        self.tools = [] # Начинаем с пустого списка
        self.browser = None

        # 1. Попытка добавить инструмент поиска через API (SerpApi)
        #    Требует наличия переменной окружения SERPAPI_API_KEY
        try:
            self.search_api = SerpAPIWrapper() # Попробует найти ключ в os.environ
            # Проверка, удалось ли инициализировать (может упасть, если ключ не найден или невалиден)
            # Сделаем тестовый запрос, чтобы убедиться в работоспособности ключа
            self.search_api.run("test") # Раскомментируйте для проверки ключа при инициализации (может замедлить)

            self.tools.append(Tool(
                name="WebSearchAPI",
                func=self.search_api.run,
                description="Надежный инструмент для поиска актуальной информации в интернете (новости, факты, погода и т.д.) через API. Вход - поисковый запрос. Возвращает краткую сводку результатов."
            ))
            logger.info("Добавлен инструмент WebSearchAPI (SerpApi).")
        except Exception as ex:
             # Не удалось инициализировать SerpApi (ключ не найден, невалиден, или др. ошибка)
             logger.warning(f"Не удалось инициализировать инструмент WebSearchAPI (SerpApi). Поиск через API недоступен. Ошибка: ",ex, exc_info=False)
             ...
            


        # 2. Попытка инициализировать BrowserController и добавить браузерные инструменты
        if start_browser and BROWSER_CONTROLLER_AVAILABLE:
            try:
                logger.info("Попытка инициализации BrowserController...")
                self.browser = BrowserController() # ВАША ИНИЦИАЛИЗАЦИЯ
                logger.info("BrowserController успешно инициализирован.")

                # --- Добавляем браузерные инструменты, только если BrowserController создан ---
                self.tools.extend([ # Используем extend для добавления нескольких инструментов
                    Tool(
                        name="BrowserNavigate",
                        func=lambda url: self.browser.navigate(url),
                        description="Переводит браузер на указанный URL. Входные данные - полный URL."
                    ),
                    Tool(
                        name="BrowserScrapeText",
                        func=lambda selector=None: self.browser.scrape_text(selector),
                        description="Извлекает текст с ТЕКУЩЕЙ страницы браузера (опционально по CSS селектору)."
                    ),
                    Tool(
                        name="BrowserClickElement",
                        func=lambda selector: self.browser.click_element(selector),
                        description="Кликает по элементу на ТЕКУЩЕЙ странице браузера (вход - CSS селектор)."
                    ),
                    # --- Можно добавить браузерный поиск как АЛЬТЕРНАТИВУ API ---
                    # Tool(
                    #     name="BrowserSearch",
                    #     func=lambda query: self.browser.search(query),
                    #     description="Выполняет поиск в интернете через окно браузера. Менее надежен, чем WebSearchAPI. Вход - поисковый запрос."
                    # ),
                ])
                logger.info(f"Добавлено {len(self.tools) - (1 if any(t.name == 'WebSearchAPI' for t in self.tools) else 0)} браузерных инструментов.") # Логируем количество добавленных браузерных

            except Exception as ex:
                logger.error("Ошибка при инициализации BrowserController или добавлении браузерных инструментов.", ex, exc_info=True)
                self.browser = None # Сбрасываем браузер
                # Не очищаем self.tools, т.к. там может быть WebSearchAPI
        elif not BROWSER_CONTROLLER_AVAILABLE:
            logger.warning("BrowserController недоступен, браузерные инструменты не добавлены.", exc_info=False)
        else: # start_browser is False
            logger.info("Инициализация браузера пропущена. Браузерные инструменты не добавлены.")

        logger.info(f"Итоговый список инструментов: {[tool.name for tool in self.tools]}") # Логируем финальный список

        if kwargs: logger.warning(f"Неиспользованные аргументы при инициализации Driver: {kwargs}", exc_info=False)

    def __del__(self):
        if self.browser:
            logger.info("Закрытие браузера при удалении объекта Driver...")
            try: self.browser.close()
            except Exception as ex: logger.error("Ошибка при вызове browser.close() в __del__.", ex, exc_info=True)


    # --- Методы _get_agent_executor, run_task, stream_task (без изменений) ---
    async def _get_agent_executor(self, llm: BaseChatModel) -> Optional[AgentExecutor]:
        if not llm: logger.error("LLM не инициализирована.", None, exc_info=False); return None
        # Проверка на пустой список инструментов теперь более актуальна
        if not self.tools:
             logger.error("Список инструментов пуст! Агент не сможет взаимодействовать с внешним миром.", None, exc_info=False)
             # Возможно, стоит вернуть None, если инструменты обязательны
             # return None
             logger.warning("Продолжение работы без инструментов.", exc_info=False) # Или просто предупредить

        try:
            prompt = hub.pull("hwchase17/react") # Стандартный ReAct промпт
            agent_runnable = create_react_agent(llm=llm, tools=self.tools, prompt=prompt)
            agent_executor = AgentExecutor(
                agent=agent_runnable,
                tools=self.tools, # Передаем актуальный список инструментов
                verbose=True,
                handle_parsing_errors=True
            )
            logger.info("AgentExecutor успешно создан.")
            return agent_executor
        except Exception as ex:
            logger.error("Ошибка при создании AgentExecutor.", ex, exc_info=True)
            return None

    async def run_task(self, task: str, use_gemini: bool = True) -> Optional[str]:
        model_name = 'Gemini' if use_gemini else 'OpenAI'; logger.info(f"Запуск run_task ({model_name}): '{task[:100]}...'")
        selected_llm = self.gemini if use_gemini else self.openai
        if not selected_llm: logger.error(f"LLM ({model_name}) не инициализирована.", None, exc_info=False); return None

        # Простое предупреждение, если инструментов нет ВООБЩЕ
        if not self.tools:
             logger.warning(f"Попытка выполнить задачу '{task[:50]}...' БЕЗ КАКИХ-ЛИБО инструментов!", exc_info=False)

        agent_executor = await self._get_agent_executor(selected_llm)
        if not agent_executor: logger.error(f"Не удалось создать AgentExecutor для {model_name}.", None, exc_info=False); return None
        try:
            result_data = await agent_executor.ainvoke({"input": task})
            final_answer = result_data.get('output')
            logger.info(f"Агент ({model_name}) завершил run_task.");
            if final_answer is not None: logger.info(f"Результат: {final_answer}")
            else: logger.warning(f"Финальный ответ отсутствует ({model_name}).", exc_info=False)
            return final_answer
        except LangChainException as e: logger.error(f"Ошибка LangChain ({model_name}).", e, exc_info=True); return None
        except Exception as ex: logger.error(f"Неожиданная ошибка ({model_name}).", ex, exc_info=True); return None

    async def stream_task(self, task: str, use_gemini: bool = True) -> Tuple[Optional[str], List[Dict[str, Any]]]:
        model_name = 'Gemini' if use_gemini else 'OpenAI'; logger.info(f"Запуск stream_task ({model_name}): '{task[:100]}...'")
        selected_llm = self.gemini if use_gemini else self.openai
        if not selected_llm: logger.error(f"LLM ({model_name}) не инициализирована.", None, exc_info=False); return None, []
        if not self.tools: logger.warning(f"Попытка стримить задачу '{task[:50]}...' БЕЗ КАКИХ-ЛИБО инструментов!", exc_info=False)
        agent_executor = await self._get_agent_executor(selected_llm)
        if not agent_executor: logger.error(f"Не удалось создать AgentExecutor для {model_name}.", None, exc_info=False); return None, []
        final_answer, all_chunks = await stream_agent_execution(executor=agent_executor, task_input={"input": task}, logger_instance=logger)
        return final_answer, all_chunks

# # --- Функция main для демонстрации ---
# async def main():

#     driver:Driver = None
#     try:
#         # Инициализируем Driver, который попытается создать инструменты
#         driver = Driver(start_browser=True) # Поставьте False, если браузер не нужен
#     except Exception as ex:
#         logger.error("Критическая ошибка при инициализации Driver.", ex, exc_info=True); return
#     if not driver: logger.error("Объект Driver не был создан.", None, exc_info=False); return
#     logger.info("Driver инициализирован.")

#     # Проверяем, какие инструменты реально доступны
#     if not driver.tools:
#         logger.warning("Инструменты НЕ доступны. Тестирование ограничено задачами без внешнего доступа.", exc_info=False)
#         task_to_run = "Напиши короткий стих о программировании." # Задача без инструментов
#     else:
#         logger.info(f"Доступные инструменты: {[tool.name for tool in driver.tools]}")
#         # Задача, которая, скорее всего, потребует поиска (WebSearchAPI или BrowserSearch)
#         task_to_run = "Какая столица Австралии и какая там сейчас погода?"
#         # Или задача для браузера, если он доступен
#         # task_to_run = "Найди 'LangChain python quickstart', перейди на страницу и извлеки первый пример кода."

#     print(f"\nТестовая задача: {task_to_run}")

#     # --- Тест run_task ---
#     print("\n" + "="*10 + " Тест run_task " + "="*10)
#     llm_to_test_run = []
#     if driver.gemini: llm_to_test_run.append(("Gemini", True))
#     if driver.openai: llm_to_test_run.append(("OpenAI", False)) # Можно добавить OpenAI, если настроен
#     if not llm_to_test_run: print("Нет активных LLM для запуска run_task.")
#     else:
#         for name, flag in llm_to_test_run:
#             print(f"\n--- Запуск run_task ({name}) ---")
#             result = await driver.run_task(task_to_run, use_gemini=flag)
#             print(f"[Результат run_task ({name})]: {result if result is not None else 'Ошибка или нет ответа'}")

#     # --- Тест stream_task ---
#     print("\n" + "="*10 + " Тест stream_task " + "="*10)
#     # Запустим стриминг только для Gemini для краткости примера
#     llm_to_test_stream = [("Gemini", True)] if driver.gemini else []
#     if not llm_to_test_stream: print("Нет активных LLM для запуска stream_task.")
#     else:
#         for name, flag in llm_to_test_stream:
#             print(f"\n--- Запуск stream_task ({name}) ---")
#             final_answer, chunks = await driver.stream_task(task_to_run, use_gemini=flag)
#             print(f"\nСтриминг ({name}) завершен. Чанков: {len(chunks)}")
#             print(f"[Финальный ответ ({name})]: {final_answer if final_answer is not None else 'Нет ответа или ошибка'}")

#     logger.info("="*20 + " Завершение main " + "="*20)



# --- Функция main для демонстрации сбора информации о товаре ---
async def main():
    driver: Driver = None
    BROWSER_TOOLS_AVAILABLE = False # Флаг доступности браузерных инструментов

    try:
        # Инициализируем Driver, ОБЯЗАТЕЛЬНО разрешая запуск браузера
        logger.info("Попытка инициализации Driver с start_browser=True...")
        driver = Driver(start_browser=True) # <-- Важно для браузерных инструментов
    except Exception as ex:
        logger.error("Критическая ошибка при инициализации Driver.", ex, exc_info=True)
        return

    if not driver:
        logger.error("Объект Driver не был создан.", None, exc_info=False)
        return

    logger.info("Driver инициализирован.")

    # Проверяем, были ли реально добавлены браузерные инструменты
    available_tool_names = [tool.name for tool in driver.tools]
    if "BrowserNavigate" in available_tool_names and "BrowserScrapeText" in available_tool_names:
        BROWSER_TOOLS_AVAILABLE = True
        logger.info(f"Браузерные инструменты доступны: {available_tool_names}")
    else:
        logger.warning(f"Браузерные инструменты НЕ доступны. Доступные инструменты: {available_tool_names}. Сбор информации со страницы НЕВОЗМОЖЕН.", exc_info=False)
        # Можно завершить выполнение или поставить другую задачу
        # return # Раскомментируйте, если без браузера продолжать нет смысла

    # --- Формулируем задачу для сбора информации ---

    # ВАРИАНТ 1: Если URL товара известен
    product_url = "https://www.ozon.ru/product/smartfon-apple-iphone-15-pro-max-256-gb-naturalnyy-titan-global-dual-sim-esim-sim-1262189900/" # Пример URL
    task_to_run = f"""
    Перейди по URL: {product_url}
    Внимательно изучи страницу товара.
    Извлеки следующую информацию:
    1. Полное название товара.
    2. Текущую цену (если есть скидка, укажи обе цены).
    3. Краткое описание или основные характеристики (1-2 предложения).
    4. Рейтинг товара (если есть, например, 4.5 из 5).
    5. Количество отзывов (если есть).

    Предоставь результат в виде четких пунктов или просто текстом.
    """

    # ВАРИАНТ 2: Если нужно сначала найти товар (требует рабочего WebSearchAPI или BrowserSearch)
    # product_name = "Смартфон Apple iPhone 15 Pro Max 256 ГБ натуральный титан"
    # website = "ozon.ru" # Можно указать сайт для точности
    # task_to_run = f"""
    # Используй поиск (WebSearchAPI предпочтительнее), чтобы найти страницу товара '{product_name}' на сайте {website}.
    # Перейди на найденную страницу товара.
    # Внимательно изучи страницу.
    # Извлеки следующую информацию:
    # 1. Полное название товара.
    # 2. Текущую цену (если есть скидка, укажи обе цены).
    # 3. Краткое описание или основные характеристики (1-2 предложения).
    # 4. Рейтинг товара (если есть).
    # 5. Количество отзывов (если есть).
    # Предоставь результат в виде четких пунктов или просто текстом.
    # """


    if not BROWSER_TOOLS_AVAILABLE:
         print("\nБраузерные инструменты недоступны. Запуск задачи сбора информации со страницы невозможен.")
         logger.warning("Пропуск задачи из-за отсутствия браузерных инструментов.")
         task_to_run = "Напиши короткий стих о коде." # Альтернативная задача
         # Или просто выходим
         # return

    print(f"\nТестовая задача для агента:\n--- НАЧАЛО ЗАДАЧИ ---\n{task_to_run}\n--- КОНЕЦ ЗАДАЧИ ---")

    # # --- Тест run_task ---
    # print("\n" + "="*10 + " Тест run_task для сбора данных " + "="*10)
    # llm_to_test_run = []
    # # Выбираем модель (можно проверить обе, если активны)
    # if driver.gemini: llm_to_test_run.append(("Gemini", True))
    # if driver.openai: llm_to_test_run.append(("OpenAI", False))

    # if not llm_to_test_run:
    #     print("Нет активных LLM для запуска run_task.")
    # else:
    #     for name, flag in llm_to_test_run:
    #         print(f"\n--- Запуск run_task ({name}) ---")
    #         # Увеличиваем таймаут, если нужно (по умолчанию LangChain может иметь свой)
    #         # Агент может долго думать и взаимодействовать с браузером
    #         try:
    #             result = await driver.run_task(task_to_run, use_gemini=flag)
    #             print(f"\n[Результат run_task ({name})]:\n{result if result is not None else 'Ошибка или нет ответа'}")
    #         except asyncio.TimeoutError:
    #              print(f"Выполнение задачи ({name}) превысило таймаут!")
    #              logger.error(f"Таймаут при выполнении run_task ({name})", None, exc_info=False)
    #         except Exception as e:
    #              print(f"Произошла ошибка во время run_task ({name}): {e}")
    #              logger.error(f"Ошибка во время run_task ({name})", e, exc_info=True)


    # --- Тест stream_task (для отладки) ---
    print("\n" + "="*10 + " Тест stream_task для сбора данных (отладка) " + "="*10)
    llm_to_test_stream = [("Gemini", True)] if driver.gemini else [] # Тестируем только Gemini для краткости
    if not llm_to_test_stream: print("Нет активных LLM для запуска stream_task.")
    else:
        for name, flag in llm_to_test_stream:
            if not BROWSER_TOOLS_AVAILABLE and "Перейди по URL" in task_to_run:
                 print(f"Пропуск stream_task ({name}), так как браузерные инструменты недоступны.")
                 continue
            print(f"\n--- Запуск stream_task ({name}) ---")
            final_answer, chunks = await driver.stream_task(task_to_run, use_gemini=flag)
            print(f"\nСтриминг ({name}) завершен. Чанков: {len(chunks)}")
            print(f"[Финальный ответ ({name})]: {final_answer if final_answer is not None else 'Нет ответа или ошибка'}")
            # Можно добавить вывод чанков для детальной отладки
            # print("\n--- Все чанки ---")
            # for i, chunk in enumerate(chunks):
            #     print(f"Chunk {i}: {chunk}")
            # print("--- Конец чанков ---")


    logger.info("="*20 + " Завершение main " + "="*20)
    # Важно: Driver.__del__ попытается закрыть браузер, если он был открыт

if __name__ == "__main__":
    # Убедитесь, что:
    # 1. Установлены все зависимости (langchain*, google-search-results, dotenv, ваш browser_use).
    # 2. API ключи (GEMINI, OPENAI, SERPAPI) доступны в .env или переменных окружения и gs.credentials.
    # 3. Файл конфигурации use_ai.json существует и корректен.
    # 4. Ваш BrowserController (если используется) работает корректно.
    asyncio.run(main())
