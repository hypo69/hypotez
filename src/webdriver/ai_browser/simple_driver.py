## \file src/webdriver/ai_browser/simple_browser.py
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

.. module:: src.webdriver.ai_browser.simple_browser
"""

import os
import asyncio
from types import SimpleNamespace
from typing import List, Dict, Any, Optional, Callable, Type, Tuple, AsyncIterator
from pathlib import Path

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
# from src.webdriver.ai_browser import tools
# from src.webdriver.ai_browser.tools import get_tools, get_tools_by_type, get_tools_by_name
from src.webdriver.ai_browser.use_llm import Config, Driver, stream_agent_execution

from src.logger import logger
from src.utils.jjson import j_loads, j_loads_ns
from src.utils.printer import pprint as print

from dotenv import load_dotenv
load_dotenv()


class SimpleDriver(Config, Driver):
    """"""
    def __init__(self, GEMINI_API_KEY = None, OPENAI_API_KEY = None, openai_model_name = None, gemini_model_name = None, start_browser = True, **kwargs):
        Config()
        super().__init__(GEMINI_API_KEY, OPENAI_API_KEY, openai_model_name, gemini_model_name, start_browser, **kwargs) 

    async def simple_process_task_async(self, task:str = 'Hello, world!') -> Any:
        try:
            # Инициализация агента с списком моделей и задачей
            # Убедитесь, что ваш класс Agent может принимать список LLM объектов в параметре 'llm'
            agent = Agent(
                task=task,
                llm=self.gemini, # Передача инициализированнoй модели
                # Другие параметры для Agent, если они есть
            )
            logger.info(f"Агент начинает выполнение задачи: \"{task}\"")
            result: Any = await agent.run() # Ожидание результата работы агента
            result_dict:dict = result.__dict__ # Преобразование результата в словарь
            logger.info("Агент завершил выполнение задачи.")
            ...
            return result_dict 
        except Exception as agent_err:
            logger.error("Произошла ошибка во время инициализации или выполнения задачи агентом.", agent_err, exc_info=True)
            ...
            return '' # Возврат None при ошибке агента


def main():
    """
    Основная функция для запуска агента и выполнения задачи.
    """
    # Пример использования
    driver = SimpleDriver(gemini_model_name = 'gemini-2.5-flash-preview-04-17')
    task = Path(__root__ / 'src' / 'webdriver' / 'ai_browser' / 'instructions' / 'get_news_from_nocamel_site.md').read_text(encoding='utf-8')
    result = asyncio.run(driver.simple_process_task_async(task))
    print(f"Результат выполнения задачи: {result}")

if __name__ == "__main__":
    main()
