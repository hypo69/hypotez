## \file src/webdriver/llm_driver/simple_browser.py
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

```rst
.. module:: src.webdriver.llm_driver.simple_browser
```
"""

# Стандартные библиотеки
import os
import sys
import io
import asyncio
import time
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
# Импорт агента из локального модуля browser_use
from browser_use import Agent # type: ignore # Предполагается, что Agent имеет определенный интерфейс

# --- Внутренние модули ---
import header
from header import __root__
from src import gs
# from src.webdriver.ai_browser import tools
# from src.webdriver.ai_browser.tools import get_tools, get_tools_by_type, get_tools_by_name
# Импорт Config, Driver и stream_agent_execution из вышестоящего модуля
from src.webdriver.llm_driver.use_llm import Config as BaseDriverConfig, Driver, stream_agent_execution

from src.logger import logger
from src.utils.jjson import j_loads, j_loads_ns, j_dumps
from src.utils.printer import pprint as print

# Загрузка переменных окружения из .env файла
from dotenv import load_dotenv
load_dotenv()

class Config:
    """
    Класс конфигурации для SimpleDriver.
    Определяет базовую точку для связанных файлов.
    """
    # Определение пути к директории для файлов, связанных с этим модулем (SANDBOX/davidka)
    ENDPOINT:Path = Path(__root__/'SANDBOX'/'davidka')

class SimpleDriver(Driver):
    """
    Упрощенный драйвер, наследующий от основного класса Driver.
    Предназначен для выполнения специфических задач с использованием LLM и агента `browser_use.Agent`.
    """
    def __init__(self, 
                 GEMINI_API_KEY:str = None, 
                 OPENAI_API_KEY:str = None, 
                 openai_model_name:str = None, 
                 gemini_model_name:str = None, 
                 start_browser:bool = True, # Изменен тип на bool для соответствия родительскому классу
                **kwargs: Any) -> None:
        """
        Инициализирует экземпляр SimpleDriver.

        Args:
            GEMINI_API_KEY (Optional[str]): API ключ для Gemini. По умолчанию `None`.
            OPENAI_API_KEY (Optional[str]): API ключ для OpenAI. По умолчанию `None`.
            openai_model_name (Optional[str]): Имя модели OpenAI. По умолчанию `None`.
            gemini_model_name (Optional[str]): Имя модели Gemini. По умолчанию `None`.
            start_browser (bool): Флаг, указывающий, нужно ли запускать браузер. По умолчанию `True`.
            **kwargs (Any): Дополнительные именованные аргументы, передаваемые в родительский конструктор.
        """
        # Вызов конструктора родительского класса Driver
        super().__init__(
            GEMINI_API_KEY=GEMINI_API_KEY, # Явная передача аргументов
            OPENAI_API_KEY=OPENAI_API_KEY,
            openai_model_name=openai_model_name,
            gemini_model_name=gemini_model_name,
            start_browser=start_browser,
            **kwargs
        ) 

    async def simple_process_task_async(self, task:str = 'Hello, world!') -> Any:
        """
        Асинхронно обрабатывает задачу с использованием агента `browser_use.Agent`.
        Функция извлекает и очищает JSON-подобные данные из результатов работы агента.

        Args:
            task (str): Текст задачи для агента. По умолчанию 'Hello, world!'.

        Returns:
            Any: Словарь с агрегированными результатами извлечения данных или пустая строка в случае критической ошибки.
                 Тип возвращаемого значения зависит от содержимого `result_dict`.
        
        Example:
            >>> driver = SimpleDriver()
            >>> # asyncio.run(driver.async_init()) # Необходим для инициализации LLM в Driver, если не сделано ранее
            >>> # result = asyncio.run(driver.simple_process_task_async("Найди информацию о Python"))
            >>> # print(result)
            # Ожидаемый результат зависит от реализации browser_use.Agent и задачи
        """
        # Инициализация словаря для хранения результатов
        result_dict:dict = {}

        def clean_json(raw_text: str) -> str:
            """
            Функция очищает строку, пытаясь извлечь из неё валидный JSON-фрагмент.
            1. Удаляет всё до первой открывающей фигурной скобки `{`.
            2. Удаляет обрамляющие символы ```, переносы строк и пробелы.

            Args:
                raw_text (str): Исходная строка с потенциальным JSON.

            Returns:
                str: Очищенная строка, готовая к парсингу как JSON, или исходная строка, если очистка не удалась.
            """
            json_start_index: int = -1 # Инициализация индекса начала JSON
            # 1. Попытка найти первую открывающую фигурную скобку
            try:
                json_start_index = raw_text.index('{')
            except ValueError: # ValueError возникает, если символ не найден
                logger.warning(f"Первая фигурная скобка '{{' не найдена в тексте: '{raw_text[:100]}...'")
                return raw_text # Если скобка не найдена, возвращается исходный текст
            
            # Извлечение текста, начиная с первой фигурной скобки
            json_cleaned: str = raw_text[json_start_index:]
    
            # 2. Удаление обрамляющих тройных кавычек (markdown code block) и лишних пробельных символов
            json_cleaned = json_cleaned.strip('`\n ')
            
            return json_cleaned

        try:
            # Инициализация агента `browser_use.Agent`
            # Передача задачи и инициализированной LLM-модели (предпочтительно Gemini)
            agent = Agent(
                task=task,
                llm=self.gemini, # Используется self.gemini, который должен быть инициализирован в Driver
            )
            logger.info(f"Агент начинает выполнение задачи: \"{task}\"")
            # Асинхронный запуск выполнения задачи агентом
            answer: Any = await agent.run() # Тип `answer` зависит от реализации `Agent.run()`

            # Проверка, вернулся ли результат от агента
            if not answer:
                logger.error('Не вернулся результат действий агента. Попытка перезапуска задачи через 5 минут.')
                # Ожидание перед повторной попыткой
                await asyncio.sleep(300) # Используется asyncio.sleep для асинхронной задержки
                # Рекурсивный вызов для повторной обработки задачи
                return await self.simple_process_task_async(task)

            # Получение текущей временной метки (используется для логирования или именования файлов, если потребуется)
            # timestamp:str = gs.now # Закомментировано, так как не используется далее

            # Обработка истории действий агента для извлечения результатов
            if hasattr(answer, 'history') and isinstance(answer.history, list):
                for action_result_item in answer.history:
                    # Предполагается, что `action_result` содержит атрибут `result` (список)
                    result_list: Optional[list] = getattr(action_result_item, 'result', None)
                    if not result_list or not isinstance(result_list, list) or not result_list:
                        continue # Пропуск, если result отсутствует, не список или пуст

                    # Предполагается, что первый элемент списка `result` является объектом `ActionResult`
                    # и содержит атрибут `extracted_content`
                    result_obj: Any = result_list[0] # Тип `ActionResult` не определен, используется Any
                    extracted_content: Optional[str] =	getattr(result_obj, 'extracted_content', None)

                    if not extracted_content or not isinstance(extracted_content, str):
                        continue # Пропуск, если извлеченный контент отсутствует или не строка

                    # Очистка извлеченного контента для получения JSON-подобной строки
                    cleaned_json_text: str = clean_json(extracted_content)
                    try:
                        # Попытка парсинга очищенной строки как JSON
                        data: Optional[Dict[str, Any]] = j_loads(cleaned_json_text)
                        # Если парсинг не удался или вернул пустой результат, но строка не пустая,
                        # то сохраняется исходная очищенная строка под ключом 'data'
                        if not data and cleaned_json_text: 
                            data = {'data': cleaned_json_text}
                        
                        if not data: 
                            continue # Пропуск, если данных нет
                    except Exception as ex_json: # Более общее исключение для j_loads
                        logger.error(f"Ошибка разбора JSON из текста: '{cleaned_json_text[:100]}...'", ex_json, exc_info=True)
                        # Если JSON не распарсился, можно сохранить очищенный текст
                        data = {'raw_cleaned_text': cleaned_json_text}
                        # continue # Решение о продолжении зависит от требований

                    # Обновление общего словаря результатов данными из текущего шага
                    if isinstance(data, dict): # Убедимся, что data - это словарь
                        result_dict.update(data)
            else:
                logger.warning("Атрибут 'history' отсутствует или не является списком в ответе агента.")

            logger.info("Агент завершил выполнение задачи.")
            ...
            return result_dict # Возврат агрегированных результатов
        except Exception as agent_err:
            # Логирование критической ошибки во время работы агента
            logger.error(f"\n\n !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\nПроизошла ошибка во время инициализации или выполнения задачи агентом.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n", agent_err, exc_info=True)
            ...
            return '' # Возврат пустой строки в случае критической ошибки агента


def main() -> None:
    """
    Основная функция для демонстрации запуска агента `SimpleDriver` и выполнения задачи.
    Функция инициализирует `SimpleDriver`, определяет задачу и запускает ее асинхронную обработку.
    """
    # Пример использования SimpleDriver
    # Инициализация драйвера с указанием модели Gemini
    # Предполагается, что API ключ Gemini будет подхвачен из Config или переменных окружения
    driver = SimpleDriver(gemini_model_name='gemini-1.5-flash-preview-0514') # Обновлено имя модели

    # Определение задачи из файла инструкций
    # Формирование пути к файлу с инструкциями
    instruction_file_path: Path = __root__ / 'src' / 'webdriver' / 'ai_browser' / 'instructions' / 'get_supplier_categories.md'
    task_text: str
    # Чтение текста задачи из файла
    if instruction_file_path.exists():
        task_text = instruction_file_path.read_text(encoding='utf-8')
    else:
        logger.error(f"Файл с инструкциями не найден: {instruction_file_path}")
        task_text = "Найди основные категории товаров на сайте example.com" # Задача по умолчанию

    # Запуск асинхронной обработки задачи
    # asyncio.run используется для выполнения асинхронной функции из синхронного контекста
    # Сначала необходимо асинхронно инициализировать родительский Driver, если он использует async_init
    async def run_driver_task():
        # Асинхронная инициализация родительского драйвера (LLM, инструменты и т.д.)
        # Это важно, так как SimpleDriver наследуется от Driver, который может требовать async_init
        if not driver._initialized: # Проверка флага инициализации
             await driver.async_init()
        # Выполнение основной задачи
        return await driver.simple_process_task_async(task_text)

    result: Any = asyncio.run(run_driver_task())
    
    # Вывод результата выполнения задачи
    print(f"Результат выполнения задачи: {result}")

if __name__ == "__main__":
    # Вызов основной функции при запуске скрипта
    main()
