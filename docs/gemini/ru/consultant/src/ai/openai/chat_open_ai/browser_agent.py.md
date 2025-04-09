### **Анализ кода модуля `browser_agent.py`**

## \file /src/ai/openai/chat_openai/browser_agent.py

#### **Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код хорошо структурирован и организован в классы и функции.
  - Используются аннотации типов для параметров и возвращаемых значений.
  - Присутствует обработка исключений с логированием ошибок.
  - Использование `logger` для логирования информации и ошибок.
- **Минусы**:
  - Не все docstring переведены на русский язык.
  - Не везде используется `ex` вместо `e` в блоках обработки исключений.
  - Переменная `MODE` определена дважды, что может привести к путанице.
  - В коде используются двойные кавычки ("), хотя требуется использовать одинарные (').

#### **Рекомендации по улучшению**:

1.  **Документация**:
    *   Перевести все docstring на русский язык, следуя инструкциям.

2.  **Обработка исключений**:
    *   Использовать `ex` вместо `e` в блоках `except`.
    *   Указывать `exc_info=True` при логировании ошибок для получения полной трассировки.

3.  **Переменные**:
    *   Удалить или переименовать одну из переменных `MODE`, чтобы избежать путаницы.
    *   Присвоить переменной `MODE` значение посредством переменной окружения.

4.  **Кавычки**:
    *   Заменить все двойные кавычки (") на одинарные (') в коде.

5.  **Асинхронность**:
    *   Метод `ask` является синхронной оберткой для асинхронного метода `ask_async` и не рекомендуется к использованию. Следует рассмотреть возможность его удаления или переработки.

6.  **Использование веб-драйвера**:
    *   В коде есть закомментированные строки, касающиеся инъекции пользовательского веб-драйвера. Рассмотрена возможность использования `Driver` из `src.webdriver`.

7.  **Аннотации**:
    *   В блоке `if USE_ENV:` переменная `MODE` не аннотирована.

#### **Оптимизированный код**:

```python
                ## \file /src/ai/openai/chat_openai/browser_agent.py
# -*- coding: utf-8 -*-\
#! .pyenv/bin/python3

"""
Модуль: src.ai.openai.chat_openai.browser_agent
=================================================
    :platform: Windows, Unix
    :synopsis: Быстро настроить и запустить ИИ-агента, который сможет искать информацию в Google и анализировать веб-страницы.

    статья: https://github.com/hypo69/1001-python-ru/tree/master/articles/lang_chain_and_browser_use
"""

from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
from typing import Optional, List, Union
import urllib.parse

import header
from src import gs
from src.logger import logger


##############################################################

ENDPOINT: str = 'openai.browser_agent'
from src import USE_ENV
MODE: str = 'PRODUCTION'  # <- Определяет режим разработчика. Если MODE==\'PRODUCTION\' будет запущен kazarionaov бот, иначе тестбот
# MODE: str = 'DEV' # Дублирующая переменная, необходимо удалить
#############################################################

if USE_ENV:
    load_dotenv()


class AIBrowserAgent:
    """
    Класс для создания агента, использующего браузер для выполнения задач.
    """

    def __init__(self,
                 api_key: str,
                 model_name: str = 'gpt-4o-mini',
                 search_engine: str = 'google',
                 custom_driver: Optional[object] = None):  # Type hint: object
        """
        Инициализирует класс BrowserAgent.

        Args:
            api_key (str): Ключ API OpenAI (необязательный). Если не указан, будет использован ключ из переменных окружения.
            model_name (str): Название языковой модели OpenAI для использования (по умолчанию 'gpt-4o-mini').
            search_engine (str): Поисковая система для использования (по умолчанию 'google').
            custom_driver (Optional[object], optional): Опционально внедренный экземпляр WebDriver, по умолчанию None (браузер по умолчанию).
        """
        self.api_key: str = api_key
        self.model_name: str = model_name
        self.search_engine: str = search_engine
        self.llm = ChatOpenAI(model=self.model_name, api_key=self.api_key)  # Initialize LLM here
        self.custom_driver = custom_driver  # Save injected driver to local variable

    async def run_task(self, task_prompt: str) -> Optional[str]:
        """
        Запускает агента для выполнения заданной задачи.

        Args:
            task_prompt (str): Текст задачи для агента.

        Returns:
            Optional[str]: Результат выполнения задачи в виде строки, или None в случае ошибки.
        """
        try:
            logger.info(f'Агент начал выполнение задачи: {task_prompt}')

            # 1. Default:  browser_use managed Playwright driver (no driver needed)
            driver = None  # By default let browser_use create its own driver.

            # 2. CUSTOM:  Adapt Selenium-based driver
            # if self.custom_driver:  # if injected instance of webdriver.FireFox
            #      playwright_driver = PlaywrightFirefoxAdapter(self.custom_driver)  # Adapt.
            #      driver = playwright_driver

            # 3. Playwright driver already adapted (or pure Playwright)
            if self.custom_driver:
                driver = self.custom_driver

            agent = Agent(task=task_prompt, llm=self.llm, driver=driver)  # Pass to agent
            result = await agent.run()
            logger.info('Агент завершил выполнение задачи.')

            if hasattr(driver, 'close') and callable(getattr(driver, 'close')):\
                driver.close()  # Try closing driver, if implemented

            return result

        except Exception as ex:
            logger.error('Произошла ошибка во время выполнения задачи: ', ex, exc_info=True)
            return None

    async def find_product_alternatives(self, product_url: Optional[str] = None,
                                        sku: Optional[str] = None) -> Optional[str]:
        """
        Ищет в сети аналоги для продукта по заданному URL или SKU.

        Args:
            product_url (Optional[str], optional): URL продукта, для которого нужно найти аналоги (опционально).
            sku (Optional[str], optional): SKU продукта, для которого нужно найти аналоги (опционально).

        Returns:
            Optional[str]: Строку с описанием найденных аналогов, или None в случае ошибки.
        """

        if product_url:
            search_query = f'аналоги {product_url}'
        elif sku:
            search_query = f'аналоги товара с артикулом {sku}'
        else:
            logger.warning('Не указан ни product_url, ни sku.  Невозможно выполнить поиск аналогов.')
            return None

        encoded_search_query = urllib.parse.quote_plus(search_query)  # URL encode search query

        if self.search_engine == 'google':
            search_url = f'https://www.google.com/search?q={encoded_search_query}'
        else:  # DuckDuckGo
            search_url = f'https://duckduckgo.com/?q={encoded_search_query}'

        task_prompt = f"""Используя поисковую систему {self.search_engine}, перейди по адресу {search_url}.  
        Найди и предоставь список из 3-5 аналогов продукта.  
        Для каждого аналога укажи название и краткое описание."""

        return await self.run_task(task_prompt)

    def ask(self, q: str) -> Optional[str]:
        """
        Синхронная обертка для асинхронного метода ask_async.  Не рекомендуется к использованию.
        """
        task_prompt = f"""Ответь на следующий вопрос, используя поиск в интернете, если это необходимо: {q}"""
        return self.run_task(task_prompt)

    async def ask_async(self, q: str) -> Optional[str]:
        """
        Отвечает на заданный вопрос, используя поиск в интернете, если это необходимо.

        Args:
            question (str): Вопрос, на который нужно ответить.

        Returns:
            Optional[str]: Ответ на вопрос в виде строки, или None в случае ошибки.
        """
        task_prompt = f"""Ответь на следующий вопрос, используя поиск в интернете, если это необходимо: {q}"""
        return await self.run_task(task_prompt)


async def main():
    """
    Пример использования класса BrowserAgent.
    """
    # api_key: str = gs.credentials.openai.hypotez.api_key  # Replace with your actual method of obtaining the API key
    api_key: str = None  # Replace with your actual method of obtaining the API key
    model_name: str = 'gpt-4o-mini'  # gpt-4o-mini существует, если указан api_key

    #########################################################################
    # OPTIONAL:  Inject custom Chrome, Firefox, Edge driver
    # selenium_driver = Firefox()  # (Or with args you use in Firefox class)
    # playwright_driver = PlaywrightFirefoxAdapter(selenium_driver)
    # agent = BrowserAgent(api_key=api_key, model_name=model_name, custom_driver = playwright_driver)
    #########################################################################
    agent = AIBrowserAgent(api_key=api_key, model_name=model_name) #  Default browser_use driver

    # Пример поиска аналогов продукта
    sku: str = '1493001'
    product_url: str = None  # "https://www.apple.com/iphone-14/"  # Замените на URL интересующего вас продукта
    alternatives = await agent.find_product_alternatives(product_url=product_url, sku=sku)
    if alternatives:
        print('Найденные аналоги:')
        print(alternatives)
    else:
        print('Не удалось найти аналоги.')

    # Пример ответа на вопрос
    question = 'Какая сейчас погода в Москве?'
    answer = await agent.ask_async(question)  # Используем асинхронный метод напрямую
    if answer:
        print('Ответ на вопрос:')
        print(answer)
    else:
        print('Не удалось получить ответ на вопрос.')


if __name__ == '__main__':
    asyncio.run(main())