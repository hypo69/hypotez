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
from typing import List, Dict, Any, Optional, Callable, Type, Tuple
from pathlib import Path

# LangChain компоненты
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
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
    config: Dict[str, Any] = j_loads_ns(ENDPOINT/ 'use_ai.json')
    models_to_use: Dict[str, Dict[str, str]] = config['models_to_use']

    # --- Установка API ключей в переменные окружения ---
    try:
        _gemini_key_source = 'gs.credentials.gemini.kazarinov' # В
        gemini_key = getattr(gs.credentials.gemini, 'kazarinov', None)
        os.environ['GEMINI_API_KEY'] = gemini_key if gemini_key else ''
        if not os.environ.get('GEMINI_API_KEY'): # Используем get для большей безопасности
            logger.warning(f"Ключ API Gemini не найден в '{_gemini_key_source}'. Переменная окружения GEMINI_API_KEY пуста.")
        else:
            logger.debug("Ключ API Gemini установлен в переменную окружения GEMINI_API_KEY.")

        _openai_key_source = 'gs.credentials.openai.hypotez.api_key'
        openai_hypotez_creds = getattr(gs.credentials.openai, 'hypotez', None)
        openai_key = getattr(openai_hypotez_creds, 'api_key', None) if openai_hypotez_creds else None
        os.environ['OPENAI_API_KEY'] = openai_key if openai_key else ''
        if not os.environ.get('OPENAI_API_KEY'): # Используем get для большей безопасности
            logger.warning(f"Ключ API OpenAI не найден в '{_openai_key_source}'. Переменная окружения OPENAI_API_KEY пуста.")
        else:
            logger.debug("Ключ API OpenAI установлен в переменную окружения OPENAI_API_KEY.")

    except AttributeError as e:
        logger.error(f"Ошибка доступа к атрибутам gs.credentials при установке ключей API: {e}. Убедитесь, что структура gs.credentials корректна.", exc_info=False)
        os.environ.setdefault('GEMINI_API_KEY', '')
        os.environ.setdefault('OPENAI_API_KEY', '')
        logger.warning("Переменные окружения GEMINI_API_KEY и OPENAI_API_KEY установлены в пустые строки из-за ошибки доступа к gs.credentials.")
    except Exception as e:
        logger.error(f"Неожиданная ошибка при установке ключей API в переменные окружения: {e}", exc_info=True)
        os.environ.setdefault('GEMINI_API_KEY', '')
        os.environ.setdefault('OPENAI_API_KEY', '')
        logger.warning("Переменные окружения GEMINI_API_KEY и OPENAI_API_KEY установлены в пустые строки из-за неожиданной ошибки.")



class Driver:
    """Класс использует `browser_use` 
    и `langchain_openai` для поиска и получения данных с веб-страниц."""

    config:Config = Config
    
    def __init__(self):
        """"""
        ...
    def _initialize_models(self):
        """"""
        ...


    async def run_task(task:str) -> str:
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
            # Выбор модели в зависимости от параметра use_google
            if 'gemini' in models_list:
                # Инициализация модели Google Gemini
                gemini = ChatGoogleGenerativeAi(
                    model="gemini-pro", 
                    google_api_key=gs.credentials.google.api_key
                )
            else:
                # Инициализация модели OpenAI
                openai = ChatOpenAI(
                    model=model_name, 
                    api_key=gs.credentials.openai.hypotez.api_key
                )

            task = f""" Найди в интернете """

            agent = Agent(
                task=task,
                llm=['openai'],
            )
            logger.info(f"Агент начал работу")
            result = await agent.run()
            logger.info(f"Агент завершил работу.")
            return result
        except Exception as e:
            logger.error(f"Произошла ошибка: {e}")
            return ''


async def main():
    """ Основная функция для выполнения задачи """
    
    # Параметр use_google позволяет выбирать между OpenAI и Google Gemini
    result = await Driver.run_task(model_name="gpt-4o")  # Пример работы с Google Gemini

    if result:
        print("Результат работы агента:")
        print(result)
    else:
        print("Не удалось получить результат.")


if __name__ == "__main__":
    asyncio.run(main())
