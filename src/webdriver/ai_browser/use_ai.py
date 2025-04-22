## \file src/webdriver/ai_browser/use_ai.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для запуска задач с использованием LLM через LangChain и кастомного Agent.

Предоставляет функциональность для:
- Конфигурирования моделей (Gemini, OpenAI) через словарь.
- Установки API ключей в переменные окружения при старте из gs.credentials.
- Запуска задачи на ВСЕХ активных моделях.
- Сбора и возврата результатов от каждой активной модели.

Зависимости:
    - langchain-openai
    - langchain-google-genai
    - langchain-core
    - python-dotenv
    - browser_use (кастомный модуль Agent)
    - src.gs (кастомный модуль)
    - src.logger (кастомный модуль)

.. module:: src.webdriver.ai_browser.use_ai
"""

import os
import asyncio
from types import SimpleNamespace
from typing import List, Dict, Any, Optional, Callable, Type, Tuple
from pathlib import Path

# LangChain компоненты
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor 
from langchain_core.language_models.chat_models import BaseChatModel # Базовый класс для type hinting
from langchain_core.exceptions import LangChainException # Для обработки ошибок LangChain

# Ваш класс Agent (убедитесь, что он импортирован правильно)
from browser_use import Agent # Пример: если browser_use находится в корне src

from dotenv import load_dotenv

from src.credentials import j_loads_ns
load_dotenv() # Функция загружает переменные окружения из .env файла

# Ваши внутренние модули
import header # type: ignore
from header import __root__ # type: ignore
from src import gs # type: ignore
from src.utils.jjson import j_loads # type: ignore
from src.utils.printer import pprint as print
from src.logger import logger


# --- Класс Конфигурации (API ключи устанавливаются в env) ---
class Config:
    """
    Класс для хранения статической конфигурации приложения.

    Содержит словарь доступных моделей, список URL для обработки,
    и шаблон задачи. API КЛЮЧИ УСТАНАВЛИВАЮТСЯ В ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ
    ПРИ ОПРЕДЕЛЕНИИ КЛАССА из `gs.credentials`.
    """
    ENDPOINT:Path = __root__/ 'src'/ 'webdriver'/ 'ai_browser'
    config: SimpleNamespace 
    GEMINI_API_KEY:str 
    GEMINI_STATUS:str
    GEMINI_MODEL_NAME:str
    OPENAI_API_KEY:str 
    OPENAI_API_STATUS:str
    OPENAI_MODEL_NAME:str

    # --- Установка API ключей в переменные окружения ---
    try:
        config: SimpleNamespace = j_loads_ns(ENDPOINT/ 'use_ai.json')
        if config: 
            GEMINI_API_KEY = getattr(gs.credentials.gemini, 'kazarinov', None)
            GEMINI_STATUS = config.models.gemini.status
            GEMINI_MODEL_NAME =  config.models.gemini.model_name
            OPENAI_API_KEY = getattr(gs.credentials.openai.hypotez, 'api_key', None)
            OPENAI_API_STATUS = config.models.openai.status
            OPENAI_MODEL_NAME =  config.models.openai.model_name
        else:
            raise Exception("Ошибка загрузки файла конфигурации")
            ...

    except AttributeError as ex:
        logger.error(f"Ошибка доступа к атрибутам gs.credentials при установке ключей API:. Убедитесь, что структура gs.credentials корректна.",ex, exc_info=False)
        os.environ.setdefault('GEMINI_API_KEY', '')
        os.environ.setdefault('OPENAI_API_KEY', '')
        logger.warning("Переменные окружения GEMINI_API_KEY и OPENAI_API_KEY установлены в пустые строки из-за ошибки доступа к gs.credentials.")
    except Exception as ex:
        logger.error(f"Неожиданная ошибка при установке ключей API в переменные окружения:",ex, exc_info=True)
        os.environ.setdefault('GEMINI_API_KEY', '')
        os.environ.setdefault('OPENAI_API_KEY', '')
        logger.warning("Переменные окружения GEMINI_API_KEY и OPENAI_API_KEY установлены в пустые строки из-за неожиданной ошибки.")



class Driver:
    """Класс использует `browser_use` 
    и `langchain_openai` для поиска и получения данных с веб-страниц."""

    config:Config = Config
    gemini:'ChatGoogleGenerativeAI'
    openai:'ChatOpenAI'
    
    def __init__(self,
                 GEMINI_API_KEY: str = '',
                 OPENAI_API_KEY: str = '',
                 openai_model_name: Optional[str] = '', 
                 gemini_model_name: Optional[str] = '', 
                 **kwargs): # kwargs для других возможных аргументов (например, для суперкласса)
        """
        Инициализирует класс, настраивая клиентов OpenAI и Gemini.

        Args:
            GEMINI_API_KEY (str, optional): API ключ для Gemini. По умолчанию ''.
                                           Будет использован Config.GEMINI_API_KEY если не предоставлен.
            OPENAI_API_KEY (str, optional): API ключ для OpenAI. По умолчанию ''.
                                           Будет использован Config.OPENAI_API_KEY если не предоставлен.
            openai_model_name (str, optional): Имя модели OpenAI для использования.
                                               Если None или '', используется Config.OPENAI_MODEL_NAME.
            gemini_model_name (str, optional): Имя модели Gemini для использования.
                                               Если None или '', используется Config.GEMINI_MODEL_NAME.
            **kwargs: Дополнительные именованные аргументы (например, для передачи суперклассу).
        """

        openai_api_key = OPENAI_API_KEY or Config.OPENAI_API_KEY or ''
        gemini_api_key = GEMINI_API_KEY or Config.GEMINI_API_KEY or ''


        openai_model_name = openai_model_name or Config.OPENAI_MODEL_NAME
        gemini_model_name = gemini_model_name or Config.GEMINI_MODEL_NAME

        # Обрати внимание, как  определяются ключи api
        if openai_api_key and Config.OPENAI_API_STATUS.lower() == 'active':
            print(f"Initializing OpenAI with model: {openai_model_name}")
            os.environ['OPENAI_API_KEY'] = openai_api_key
            try:
                self.openai = ChatOpenAI(
                    model_name=openai_model_name
                    # Если ChatOpenAI может принимать доп. аргументы, можно передать **kwargs
                    # **kwargs
                )
            except Exception as ex:
                print(f"Error initializing OpenAI: ",ex)

        if gemini_api_key and Config.GEMINI_STATUS.lower() == 'active':
            print(f"Initializing Gemini with model: {gemini_model_name}")
            os.environ['GEMINI_API_KEY'] = gemini_api_key # Уточните необходимость
            try:
                self.gemini = ChatGoogleGenerativeAI(
                    model=gemini_model_name,
                    api_key=gemini_api_key
                     # Если ChatGoogleGenerativeAI может принимать доп. аргументы, можно передать **kwargs
                    # **kwargs
                )
            except Exception as ex:
                print(f"Error initializing Gemini: ",ex)
                ...

        # Если нужно передать оставшиеся kwargs дальше (например, в super().__init__):
        # super().__init__(**kwargs)
        # Или если нужно проверить, что не осталось неиспользованных kwargs:
        if kwargs:
             print(f"Warning: Unused keyword arguments passed to YourClass.__init__: {kwargs}")
             # raise TypeError(f"__init__() got unexpected keyword arguments: {list(kwargs.keys())}")



    async def run_task(self, task:str) -> str:
        """
        Исполяет сценарий 

        Args:
            model_name: Название языковой модели для использования (по умолчанию gpt-4o).
            use_google: Если True, используется Google Gemini. Если False, используется OpenAI.

        Returns:
            Строку с результатом работы агента, содержащую название статьи и сгенерированный комментарий.
            Возвращает None, если произошла ошибка.
        """
         
        try:
            if self.gemini:
                agent = Agent(
                    task=task,
                    llm=self.gemini, # <- Сюда отправляется модель
                )
                logger.info(f"Агент начал работу")
                agent_executor = AgentExecutor(agent=agent, tools=None, verbose=True)
                await agent_executor.ainvoke({"input": task}) 
                #result = await agent.run()
                logger.info(f"Агент завершил работу\nрезультат:\n{print(result)}")
                return result
        except Exception as e:
            logger.error(f"Произошла ошибка: {e}")
            return ''

        #----------------------------------------------------------
        #                                                          |
        #              Аналогично для других моделей               |
        #                                                          |
        # ---------------------------------------------------------


async def main():
    """ Основная функция для выполнения задачи """
    
    # Параметр use_google позволяет выбирать между OpenAI и Google Gemini
    result = await Driver.run_task("Hello!")  # Пример работы с Google Gemini

    if result:
        print("Результат работы агента:")
        print(result)
    else:
        print("Не удалось получить результат.")


if __name__ == "__main__":
    asyncio.run(main())
