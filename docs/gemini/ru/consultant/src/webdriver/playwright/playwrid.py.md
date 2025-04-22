### **Анализ кода модуля `playwrid.py`**

## \file /src/webdriver/playwright/playwrid.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
.. module:: src.webdriver.playwright
    :platform: Windows, Unix
    :synopsis: Playwright Crawler

This module defines a subclass of `PlaywrightCrawler` called `Playwrid`.
It provides additional functionality such as the ability to set custom browser settings, profiles, and launch options using Playwright.

Example usage:

.. code-block:: python

    if __name__ == "__main__":
        browser = Playwrid(options=["--headless"])
        browser.start("https://www.example.com")
"""

## Качество кода:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Четкая структура класса `Playwrid`.
    - Использование асинхронности для неблокирующих операций.
    - Наличие docstring для большинства методов и классов.
    - Использование модуля `logger` для логирования.
    - Пример использования в `if __name__ == "__main__":`.
- **Минусы**:
    - Docstring написаны на английском языке.
    - Не все переменные аннотированы типами.
    - Некоторые участки кода требуют более подробных комментариев.

## Рекомендации по улучшению:

1.  **Перевод Docstring**:
    - Перевести все docstring на русский язык, чтобы соответствовать требованиям проекта.

2.  **Добавление аннотаций типов**:
    - Добавить аннотации типов для всех переменных, где это необходимо, чтобы повысить читаемость и облегчить отладку.

3.  **Улучшение комментариев**:
    - Добавить больше комментариев, объясняющих сложные участки кода, особенно в методах `_set_launch_options` и `start`.

4.  **Использование `ex` в блоках `except`**:
    - Убедиться, что все блоки `except` используют `ex` вместо `e` для обозначения исключения.

5.  **Форматирование кода**:
    - Убедиться, что весь код соответствует стандартам PEP8.

6.  **Замена устаревших терминов**:
    - Заменить термин `Product` на `товар`.

7.  **Удалить англоязычные комментарии и пояснения**

## Оптимизированный код:

```python
## \file /src/webdriver/playwright/playwrid.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.webdriver.playwright
    :platform: Windows, Unix
    :synopsis: Playwright Crawler

Этот модуль определяет подкласс `PlaywrightCrawler` под названием `Playwrid`.
Он предоставляет дополнительные функциональные возможности, такие как возможность устанавливать пользовательские настройки браузера, профили и параметры запуска с использованием Playwright.

Пример использования:

.. code-block:: python

    if __name__ == "__main__":
        browser = Playwrid(options=["--headless"])
        browser.start("https://www.example.com")
"""
import asyncio
from pathlib import Path
from typing import Optional, Dict, Any, List
from types import SimpleNamespace
#from crawlee.playwright_crawler import PlaywrightCrawler, PlaywrightCrawlingContext
from crawlee.crawlers import PlaywrightCrawler, PlaywrightCrawlingContext

import header
from header import __root__
from src import gs
from src.webdriver.playwright.executor import PlaywrightExecutor
from src.webdriver.js import JavaScript
from src.utils.jjson import j_loads_ns
from src.logger.logger import logger


class Playwrid(PlaywrightCrawler):
    """
    Подкласс `PlaywrightCrawler`, который предоставляет дополнительные функциональные возможности.

    Attributes:
        driver_name (str): Имя драйвера, по умолчанию 'playwrid'.
    """
    driver_name: str = 'playwrid'
    base_path: Path = __root__ / 'src' / 'webdriver' / 'playwright'
    config: SimpleNamespace = j_loads_ns(base_path / 'playwrid.json')
    context = None

    def __init__(self, user_agent: Optional[str] = None, options: Optional[List[str]] = None, *args, **kwargs) -> None:
        """
        Инициализирует Playwright Crawler с указанными параметрами запуска, настройками и user agent.

        Args:
            user_agent (Optional[str], optional): User-agent для использования. По умолчанию None.
            options (Optional[List[str]], optional): Список опций Playwright. По умолчанию None.
        """
        launch_options = self._set_launch_options(user_agent, options)
        self.executor = PlaywrightExecutor()
        # Передача launch_options в PlaywrightCrawler, если он их принимает
        # В противном случае, удаляем launch_options из параметров
        super().__init__(
            browser_type=self.config.browser_type,
            # launch_options=launch_options,  # Удалите или настройте, если не принимается
            **kwargs
        )
        # Если PlaywrightCrawler не принимает launch_options, устанавливаем их отдельно
        if hasattr(self, 'set_launch_options'):
            self.set_launch_options(launch_options)
        else:
            # Обработка launch_options другим способом при необходимости
            pass

    def _set_launch_options(self, user_agent: Optional[str] = None, options: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Конфигурирует параметры запуска для Playwright Crawler.

        Args:
            user_agent (Optional[str], optional): User-agent для использования. По умолчанию None.
            options (Optional[List[str]], optional): Список опций Playwright для передачи во время инициализации. По умолчанию None.

        Returns:
            Dict[str, Any]: Словарь с параметрами запуска для Playwright.
        """
        launch_options = {
            "headless": self.config.headless if hasattr(self.config, 'headless') else True,
            "args": self.config.options if hasattr(self.config, 'options') else []
        }

        # Добавление пользовательского user-agent, если он предоставлен
        if user_agent:
            launch_options['user_agent'] = user_agent

        # Объединение пользовательских опций с опциями по умолчанию
        if options:
            launch_options['args'].extend(options)

        return launch_options

    async def start(self, url: str) -> None:
        """
        Запускает Playwrid Crawler и переходит по указанному URL.

        Args:
            url (str): URL для перехода.
        """
        try:
            logger.info(f"Запуск Playwright Crawler для {url}")
            await self.executor.start()  # Запуск executor
            await self.executor.goto(url) # Переход по URL
            super().run(url) # Запуск crawler
            # Функция извлекает контекст
            self.context = self.crawling_context
        except Exception as ex:
            logger.critical('Playwrid Crawler завершился с ошибкой:', ex)

    @property
    def current_url(self) -> Optional[str]:
        """
        Возвращает текущий URL браузера.

        Returns:
            Optional[str]: Текущий URL.
        """
        if self.context and self.context.page:
            return self.context.page.url
        return None

    def get_page_content(self) -> Optional[str]:
        """
        Возвращает HTML-содержимое текущей страницы.

        Returns:
            Optional[str]: HTML-содержимое страницы.
        """
        if self.context and self.context.page:
            return self.context.page.content()
        return None

    async def get_element_content(self, selector: str) -> Optional[str]:
        """
        Возвращает внутреннее HTML-содержимое одного элемента на странице по CSS-селектору.

        Args:
            selector (str): CSS-селектор для элемента.

        Returns:
            Optional[str]: Внутреннее HTML-содержимое элемента или None, если элемент не найден.
        """
        if self.context and self.context.page:
            try:
                element = self.context.page.locator(selector)
                return await element.inner_html()
            except Exception as ex:
                logger.warning(f"Элемент с селектором '{selector}' не найден или произошла ошибка во время извлечения: {ex}")
                return None
        return None

    async def get_element_value_by_xpath(self, xpath: str) -> Optional[str]:
        """
        Возвращает текстовое значение одного элемента на странице по XPath.

        Args:
            xpath (str): XPath элемента.

        Returns:
            Optional[str]: Текстовое значение элемента или None, если элемент не найден.
        """
        if self.context and self.context.page:
            try:
                element = self.context.page.locator(f'xpath={xpath}')
                return await element.text_content()
            except Exception as ex:
                logger.warning(f"Элемент с XPath '{xpath}' не найден или произошла ошибка во время извлечения: {ex}")
                return None
        return None

    async def click_element(self, selector: str) -> None:
        """
        Кликает на один элемент на странице по CSS-селектору.

        Args:
            selector (str): CSS-селектор элемента для клика.
        """
        if self.context and self.context.page:
            try:
                element = self.context.page.locator(selector)
                await element.click()
            except Exception as ex:
                logger.warning(f"Элемент с селектором '{selector}' не найден или произошла ошибка во время клика: {ex}")
    
    async def execute_locator(self, locator: dict | SimpleNamespace, message: Optional[str] = None, typing_speed: float = 0) -> str | List[str] | bytes | List[bytes] | bool:
        """
        Выполняет локатор через executor.

        Args:
            locator (dict | SimpleNamespace): Данные локатора.
            message (Optional[str], optional): Опциональное сообщение для событий. По умолчанию None.
            typing_speed (float, optional): Опциональная скорость печати для событий. По умолчанию 0.

        Returns:
            str | List[str] | bytes | List[bytes] | bool: Статус выполнения.
        """
        return await self.executor.execute_locator(locator, message, typing_speed)


if __name__ == "__main__":
    async def main():
        browser = Playwrid(options=["--headless"])
        await browser.start("https://www.example.com")
        
        # Функция извлекает HTML всего документа
        html_content = browser.get_page_content()
        if html_content:
            print(html_content[:200])  # Выведем первые 200 символов для примера
        else:
            print("Не удалось получить HTML-контент.")
        
        # Функция извлекает HTML элемента по селектору
        element_content = await browser.get_element_content("h1")
        if element_content:
            print("\\nСодержимое элемента h1:")
            print(element_content)
        else:
            print("\\nЭлемент h1 не найден.")
        
        # Функция извлекает значение элемента по xpath
        xpath_value = await browser.get_element_value_by_xpath("//head/title")
        if xpath_value:
             print(f"\\nЗначение элемента по XPATH //head/title: {xpath_value}")
        else:
             print("\\nЭлемент по XPATH //head/title не найден")

        # Нажатие на кнопку (при наличии)
        await browser.click_element("button")

        locator_name = {
        "attribute": "innerText",
        "by": "XPATH",
        "selector": "//h1",
        "if_list": "first",
        "use_mouse": False,
        "timeout": 0,
        "timeout_for_event": "presence_of_element_located",
        "event": None,
        "mandatory": True,
        "locator_description": "Название товара"
        }

        name = await browser.execute_locator(locator_name)
        print("Name:", name)

        locator_click = {
        "attribute": None,
        "by": "CSS",
        "selector": "button",
        "if_list": "first",
        "use_mouse": False,
        "timeout": 0,
        "timeout_for_event": "presence_of_element_located",
        "event": "click()",
        "mandatory": True,
        "locator_description": "название товара"
        }
        await browser.execute_locator(locator_click)
        await asyncio.sleep(3)
    asyncio.run(main())