## \file src/webdriver/ai_browser/use_ai.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для запуска задач с использованием LLM через LangChain и стандартных агентов.
==================================================================================
(Использует инструменты, взаимодействующие с BrowserController)

Предоставляет функциональность для:
- Конфигурирования моделей (Gemini, OpenAI).
- Установки API ключей.
- Запуска задачи с использованием LLM и браузерных инструментов.
- Выполнения задачи до конечного результата (`run_task`).
- Стриминга выполнения задачи (`stream_task`).

Зависимости:
    - langchain-openai, langchain-google-genai, langchain-core, langchainhub, langchain
    - python-dotenv
    - browser_use (или ваш модуль с BrowserController)
    - src.gs, src.logger, src.utils

.. module:: src.webdriver.ai_browser.use_ai
"""

import os
import asyncio
from types import SimpleNamespace
from typing import List, Dict, Any, Optional, Callable, Type, Tuple, AsyncIterator
from pathlib import Path
import logging # Стандартный logging все еще может быть полезен

# LangChain компоненты
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent, Tool
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.exceptions import LangChainException
from langchain import hub

# --- внутренние модули ---
import header
from header import __root__
from src import gs
from src.logger import logger
from src.utils.jjson import j_loads, j_loads_ns
from src.utils.printer import pprint as print




# --- Импорт вашего контроллера браузера ---
# Замените 'browser_use' и 'BrowserController' на ваши реальные имена
try:
    from browser_use import BrowserController # Пример
    BROWSER_CONTROLLER_AVAILABLE = True
except ImportError:
    # Заглушка, если ваш контроллер не найден
    logger.warning("Не удалось импортировать BrowserController. Браузерные инструменты будут недоступны.", exc_info=False)
    class BrowserController: # type: ignore
        def __init__(self, *args, **kwargs): logger.error("BrowserController недоступен!", None, exc_info=False)
        def search(self, q): return "Ошибка: BrowserController недоступен."
        def navigate(self, u): return "Ошибка: BrowserController недоступен."
        def scrape_text(self, s=None): return "Ошибка: BrowserController недоступен."
        def click_element(self, s): return "Ошибка: BrowserController недоступен."
        def close(self): pass
    BROWSER_CONTROLLER_AVAILABLE = False


from dotenv import load_dotenv
load_dotenv()


# --- Класс Конфигурации ---
class Config:
    """ Класс для хранения статической конфигурации приложения. """
    ENDPOINT: Path = __root__ / 'src' / 'webdriver' / 'ai_browser'
    config: SimpleNamespace = j_loads_ns(ENDPOINT/'use_ai.json')
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_STATUS: str = 'inactive'
    GEMINI_MODEL_NAME: str = ''
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_API_STATUS: str = 'inactive'
    OPENAI_MODEL_NAME: str = ''

    if config:
        try:
            GEMINI_API_KEY = gs.credentials.gemini.kazarinov
            GEMINI_STATUS = config.models.gemini.status
            GEMINI_MODEL_NAME = config.models.gemini.model_name
            OPENAI_API_KEY = gs.credentials.openai.hypotez.api_key
            OPENAI_API_STATUS = config.models.openai.status
            OPENAI_MODEL_NAME = config.models.openai.model_name

            logger.info(f"Config Gemini: Status={GEMINI_STATUS}, Model={GEMINI_MODEL_NAME}, Key Present={bool(GEMINI_API_KEY)}")
            logger.info(f"Config OpenAI: Status={OPENAI_API_STATUS}, Model={OPENAI_MODEL_NAME}, Key Present={bool(OPENAI_API_KEY)}")
    
        except AttributeError as ex: logger.error("Ошибка атрибутов при инициализации Config.", ex, exc_info=False)
        except Exception as ex: logger.error("Неожиданная ошибка при инициализации Config.", ex, exc_info=True)

    else:
        raise Exception('Ошибка! Нет файла конфигурации')

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
    Класс для управления LLM и запуска агентов LangChain с браузерными инструментами.
    """
    config: Config = Config
    gemini: Optional[ChatGoogleGenerativeAI] = None
    openai: Optional[ChatOpenAI] = None
    tools: List[Tool] = []
    browser: Optional[BrowserController] = None

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
        openai_api_key = OPENAI_API_KEY or Config.OPENAI_API_KEY
        gemini_api_key = GEMINI_API_KEY or Config.GEMINI_API_KEY
        openai_model_name = openai_model_name or Config.OPENAI_MODEL_NAME
        gemini_model_name = gemini_model_name or Config.GEMINI_MODEL_NAME

        # Инициализация LLM (OpenAI)
        if openai_api_key and Config.OPENAI_API_STATUS.lower() == 'active':
            logger.info(f"Инициализация OpenAI: Model={openai_model_name}")
            os.environ['OPENAI_API_KEY'] = openai_api_key
            try: self.openai = ChatOpenAI(model_name=openai_model_name, openai_api_key=openai_api_key)
            except Exception as ex: logger.error("Ошибка инициализации OpenAI.", ex, exc_info=True); self.openai = None
            if self.openai: logger.info("OpenAI LLM инициализирован.")
        else: logger.warning(f"OpenAI LLM не инициализирован (Key={bool(openai_api_key)}, Status={Config.OPENAI_API_STATUS})", exc_info=False); self.openai = None

        # Инициализация LLM (Gemini)
        if gemini_api_key and Config.GEMINI_STATUS.lower() == 'active':
            logger.info(f"Инициализация Gemini: Model={gemini_model_name}")
            os.environ['GOOGLE_API_KEY'] = gemini_api_key
            logger.debug("Установлена переменная окружения GOOGLE_API_KEY.", exc_info=False)
            try: self.gemini = ChatGoogleGenerativeAI(model=gemini_model_name, google_api_key=gemini_api_key)
            except Exception as ex: logger.error("Ошибка инициализации Gemini.", ex, exc_info=True); self.gemini = None
            if self.gemini: logger.info("Gemini LLM инициализирован.")
        else: logger.warning(f"Gemini LLM не инициализирован (Key={bool(gemini_api_key)}, Status={Config.GEMINI_STATUS})", exc_info=False); self.gemini = None

        # Инициализация контроллера браузера и инструментов
        self.browser = None
        if start_browser and BROWSER_CONTROLLER_AVAILABLE:
            try:
                logger.info("Попытка инициализации BrowserController...")
                self.browser = BrowserController()
                logger.info("BrowserController успешно инициализирован.")


                self.tools = [
                        Tool(
                            # 1. Имя, которое увидит LLM:
                            name="BrowserSearch",
                            # 2. Функция, которая будет вызвана:
                            #    Используем lambda, чтобы передать метод экземпляра self.browser
                            func=lambda query: self.browser.search(query),
                            # 3. Описание для LLM (ОЧЕНЬ ВАЖНО):
                            description=(
                                "Используй этот инструмент для поиска актуальной информации в интернете по заданному запросу. "
                                "Подходит для поиска новостей, фактов, ответов на вопросы, о которых у тебя нет знаний. "
                                "Входные данные (query) должны быть четким поисковым запросом (например, 'последние обновления LangChain', 'погода в Париже'). "
                                "Возвращает строку с текстовыми результатами поиска."
                            )
                        ),
                        # ... другие ваши инструменты (BrowserNavigate, BrowserScrapeText, etc.)
                    ]
                logger.info(f"Определено {len(self.tools)} инструментов.")

                self.tools = [
                    Tool(name="BrowserSearch", func=lambda query: self.browser.search(query), description="Выполняет поиск в интернете по заданному запросу."),
                    Tool(name="BrowserNavigate", func=lambda url: self.browser.navigate(url), description="Переходит по указанному URL."),
                    Tool(name="BrowserScrapeText", func=lambda selector=None: self.browser.scrape_text(selector), description="Извлекает текст с текущей страницы (опционально по CSS селектору)."),
                    Tool(name="BrowserClickElement", func=lambda selector: self.browser.click_element(selector), description="Кликает по элементу, найденному по CSS селектору."),
                ]
                logger.info(f"Определено {len(self.tools)} браузерных инструментов.")
            except Exception as e:
                logger.error("Ошибка при инициализации BrowserController или определении инструментов.", e, exc_info=True)
                self.browser = None; self.tools = []
        elif not BROWSER_CONTROLLER_AVAILABLE: logger.warning("BrowserController недоступен, инструменты не созданы.", exc_info=False); self.tools = []
        else: logger.info("Инициализация браузера пропущена. Инструменты не созданы."); self.tools = []

        if kwargs: logger.warning(f"Неиспользованные аргументы при инициализации Driver: {kwargs}", exc_info=False)

    def __del__(self):
        if self.browser:
            logger.info("Закрытие браузера при удалении объекта Driver...")
            try: self.browser.close()
            except Exception as e: logger.error("Ошибка при вызове browser.close() в __del__.", e, exc_info=True)


    async def _get_agent_executor(self, llm: BaseChatModel) -> Optional[AgentExecutor]:
        if not llm: logger.error("LLM не инициализирована.", None, exc_info=False); return None
        if not self.tools: logger.warning("Список инструментов пуст.", exc_info=False)
        try:
            prompt = hub.pull("hwchase17/react")
            agent_runnable = create_react_agent(llm=llm, tools=self.tools, prompt=prompt)
            agent_executor = AgentExecutor(agent=agent_runnable, tools=self.tools, verbose=True, handle_parsing_errors=True)
            logger.info("AgentExecutor успешно создан.")
            return agent_executor
        except Exception as e: logger.error("Ошибка при создании AgentExecutor.", e, exc_info=True); return None

    async def run_task(self, task: str, use_gemini: bool = True) -> Optional[str]:
        model_name = 'Gemini' if use_gemini else 'OpenAI'; logger.info(f"Запуск run_task ({model_name}): '{task[:100]}...'")
        selected_llm = self.gemini if use_gemini else self.openai
        if not selected_llm: logger.error(f"LLM ({model_name}) не инициализирована.", None, exc_info=False); return None
        if not self.tools and "browser" in task.lower(): logger.warning(f"Задача '{task[:50]}...' без браузерных инструментов!", exc_info=False)
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
        except Exception as e: logger.error(f"Неожиданная ошибка ({model_name}).", e, exc_info=True); return None

    async def stream_task(self, task: str, use_gemini: bool = True) -> Tuple[Optional[str], List[Dict[str, Any]]]:
        model_name = 'Gemini' if use_gemini else 'OpenAI'; logger.info(f"Запуск stream_task ({model_name}): '{task[:100]}...'")
        selected_llm = self.gemini if use_gemini else self.openai
        if not selected_llm: logger.error(f"LLM ({model_name}) не инициализирована.", None, exc_info=False); return None, []
        if not self.tools and "browser" in task.lower(): logger.warning(f"Стрим задачи '{task[:50]}...' без браузерных инструментов!", exc_info=False)
        agent_executor = await self._get_agent_executor(selected_llm)
        if not agent_executor: logger.error(f"Не удалось создать AgentExecutor для {model_name}.", None, exc_info=False); return None, []
        final_answer, all_chunks = await stream_agent_execution(executor=agent_executor, task_input={"input": task}, logger_instance=logger)
        return final_answer, all_chunks

# --- Функция main для демонстрации ---
async def main():

    logger.info("="*20 + " Инициализация Driver " + "="*20)
    driver = None
    try: driver = Driver(start_browser=True)
    except Exception as e: logger.error("Критическая ошибка при инициализации Driver.", e, exc_info=True); return
    if not driver: logger.error("Объект Driver не был создан.", None, exc_info=False); return
    logger.info("Driver инициализирован.")
    if not driver.tools: logger.warning("Инструменты не доступны. Тестирование ограничено.", exc_info=False)

    task_to_run = "Найди 'LangChain blog', перейди туда и извлеки текст заголовка страницы."
    print(f"\nТестовая задача: {task_to_run}")

    # --- Тест run_task ---
    print("\n" + "="*10 + " Тест run_task " + "="*10)
    llm_to_test_run = [("Gemini", True)] if driver.gemini else []
    if driver.openai: llm_to_test_run.append(("OpenAI", False))
    if not llm_to_test_run: print("Нет активных LLM.")
    else:
        for name, flag in llm_to_test_run:
            print(f"\n--- Запуск run_task ({name}) ---")
            result = await driver.run_task(task_to_run, use_gemini=flag)
            print(f"[Результат run_task ({name})]: {result if result is not None else 'Ошибка или нет ответа'}")

    # --- Тест stream_task ---
    print("\n" + "="*10 + " Тест stream_task " + "="*10)
    llm_to_test_stream = [("Gemini", True)] if driver.gemini else []
    # if driver.openai: llm_to_test_stream.append(("OpenAI", False))
    if not llm_to_test_stream: print("Нет активных LLM.")
    else:
        for name, flag in llm_to_test_stream:
            print(f"\n--- Запуск stream_task ({name}) ---")
            final_answer, chunks = await driver.stream_task(task_to_run, use_gemini=flag)
            print(f"\nСтриминг ({name}) завершен. Чанков: {len(chunks)}")
            print(f"[Финальный ответ ({name})]: {final_answer if final_answer is not None else 'Нет ответа или ошибка'}")

    logger.info("="*20 + " Завершение main " + "="*20)

if __name__ == "__main__":
    asyncio.run(main())