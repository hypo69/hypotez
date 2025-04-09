### **Анализ кода модуля `playwrid.py`**

## \\file /src/webdriver/playwright/playwrid.py

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Использование `j_loads_ns` для загрузки конфигурации.
    - Логирование с использованием `logger` из `src.logger`.
    - Четкое разделение на методы для выполнения различных действий (например, `_set_launch_options`, `start`, `get_element_content`).
    - Применение `SimpleNamespace` для конфигурации.
- **Минусы**:
    - Не все функции и методы имеют подробные docstring, особенно внутренние функции.
    - Некоторые комментарии на английском языке.
    - Использование `hasattr` для проверки наличия атрибутов в `_set_launch_options` может быть упрощено.
    - Нет обработки ошибок при запуске `super().run(url)` в методе `start`.
    - В примере использования в `if __name__ == "__main__":` много `print` вместо `logger.info`

**Рекомендации по улучшению:**

1.  **Документация**:
    - Добавить docstring для класса `Playwrid`, указав основные методы и их назначение.
    - Перевести все docstring и комментарии на русский язык.
    - Добавить примеры использования в docstring для основных методов.
    - Улучшить описание параметров и возвращаемых значений в docstring.
    - Добавить обработку возможных исключений в методе `start` при вызове `super().run(url)`.
    - Использовать `logger.info` вместо `print` в примере использования для единообразия логирования.

2.  **Улучшение кода**:
    - Избегать использования `hasattr` в `_set_launch_options`. Вместо этого можно использовать `getattr` с указанием значения по умолчанию.
    - Добавить обработку ошибок при вызове `super().run(url)` в методе `start`.
    - Улучшить обработку исключений в методах `get_element_content` и `get_element_value_by_xpath`, добавив более конкретные сообщения об ошибках.

3. **Безопасность**:
    - Удостовериться, что все используемые сторонние библиотеки и зависимости актуальны и не содержат известных уязвимостей.

**Оптимизированный код:**

```python
                ## \file /src/webdriver/playwright/playwrid.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для работы с Playwright Crawler
========================================

Этот модуль определяет подкласс `PlaywrightCrawler` под названием `Playwrid`.
Он предоставляет дополнительные функциональные возможности, такие как возможность установки пользовательских настроек браузера,
профилей и параметров запуска с использованием Playwright.

Пример использования:
----------------------

.. code-block:: python

    if __name__ == "__main__":
        browser = Playwrid(options=["--headless"])
        await browser.start("https://www.example.com")
"""
import asyncio
from pathlib import Path
from typing import Optional, Dict, Any, List
from types import SimpleNamespace

# from crawlee.playwright_crawler import PlaywrightCrawler, PlaywrightCrawlingContext
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
    Подкласс `PlaywrightCrawler`, предоставляющий дополнительные функции.

    Этот класс позволяет настраивать параметры запуска браузера, такие как user-agent и опции командной строки.

    Attributes:
        driver_name (str): Имя драйвера, по умолчанию 'playwrid'.
        base_path (Path): Базовый путь к файлам конфигурации.
        config (SimpleNamespace): Объект конфигурации, загруженный из playwrid.json.
        context (Optional[PlaywrightCrawlingContext]): Контекст выполнения Playwright.
    """

    driver_name: str = 'playwrid'
    base_path: Path = __root__ / 'src' / 'webdriver' / 'playwright'
    config: SimpleNamespace = j_loads_ns(base_path / 'playwrid.json')
    context: Optional[PlaywrightCrawlingContext] = None

    def __init__(self, user_agent: Optional[str] = None, options: Optional[List[str]] = None, *args, **kwargs) -> None:
        """
        Инициализирует Playwright Crawler с указанными параметрами запуска, настройками и user-agent.

        Args:
            user_agent (Optional[str]): User-agent для использования в браузере.
            options (Optional[List[str]]): Список опций Playwright для передачи при инициализации.
            *args: Дополнительные аргументы, передаваемые в `PlaywrightCrawler.__init__`.
            **kwargs: Дополнительные именованные аргументы, передаваемые в `PlaywrightCrawler.__init__`.
        """
        launch_options = self._set_launch_options(user_agent, options)
        self.executor = PlaywrightExecutor()
        # Pass launch_options to PlaywrightCrawler if it accepts them
        # Otherwise, remove launch_options from the parameters
        super().__init__(
            browser_type=self.config.browser_type,
            # launch_options=launch_options,  # Remove or adjust if not accepted
            **kwargs
        )
        # If PlaywrightCrawler does not accept launch_options, set them separately
        if hasattr(self, 'set_launch_options'):
            self.set_launch_options(launch_options)
        else:
            # Handle launch options differently if needed
            pass

    def _set_launch_options(self, user_agent: Optional[str] = None, options: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Конфигурирует параметры запуска для Playwright Crawler.

        Args:
            user_agent (Optional[str]): User-agent для использования.
            options (Optional[List[str]]): Список опций Playwright для передачи при инициализации.

        Returns:
            Dict[str, Any]: Словарь с параметрами запуска для Playwright.
        """
        launch_options = {
            'headless': getattr(self.config, 'headless', True),
            'args': getattr(self.config, 'options', [])
        }

        # Add custom user-agent if provided
        if user_agent:
            launch_options['user_agent'] = user_agent

        # Merge custom options with default options
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
            logger.info(f'Starting Playwright Crawler for {url}')
            await self.executor.start()  # Start the executor
            await self.executor.goto(url)  # Goto url
            super().run(url)  # run crawler
            # получаем контекст
            self.context = self.crawling_context
        except Exception as ex:
            logger.error('Playwrid Crawler failed with an error:', ex, exc_info=True)

    @property
    def current_url(self) -> Optional[str]:
        """
        Возвращает текущий URL браузера.

        Returns:
            Optional[str]: Текущий URL или None, если URL недоступен.
        """
        if self.context and self.context.page:
            return self.context.page.url
        return None

    def get_page_content(self) -> Optional[str]:
        """
        Возвращает HTML-содержимое текущей страницы.

        Returns:
            Optional[str]: HTML-содержимое страницы или None, если содержимое недоступно.
        """
        if self.context and self.context.page:
            return self.context.page.content()
        return None

    async def get_element_content(self, selector: str) -> Optional[str]:
        """
        Возвращает внутреннее HTML-содержимое элемента по CSS-селектору.

        Args:
            selector (str): CSS-селектор элемента.

        Returns:
            Optional[str]: Внутреннее HTML-содержимое элемента или None, если элемент не найден.
        """
        if self.context and self.context.page:
            try:
                element = self.context.page.locator(selector)
                return await element.inner_html()
            except Exception as ex:
                logger.warning(f"Element with selector '{selector}' not found or error during extraction: {ex}")
                return None
        return None

    async def get_element_value_by_xpath(self, xpath: str) -> Optional[str]:
        """
        Возвращает текстовое значение элемента по XPath.

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
                logger.warning(f"Element with XPath '{xpath}' not found or error during extraction: {ex}")
                return None
        return None

    async def click_element(self, selector: str) -> None:
        """
        Кликает на элемент по CSS-селектору.

        Args:
            selector (str): CSS-селектор элемента.
        """
        if self.context and self.context.page:
            try:
                element = self.context.page.locator(selector)
                await element.click()
            except Exception as ex:
                logger.warning(f"Element with selector '{selector}' not found or error during click: {ex}")

    async def execute_locator(self, locator: dict | SimpleNamespace, message: Optional[str] = None, typing_speed: float = 0) -> str | List[str] | bytes | List[bytes] | bool:
        """
        Выполняет локатор через executor

        Args:
            locator (dict | SimpleNamespace): Данные локатора.
            message (Optional[str]): Опциональное сообщение для событий.
            typing_speed (float): Опциональная скорость печати для событий.

        Returns:
            str | List[str] | bytes | List[bytes] | bool: Статус выполнения.
        """
        return await self.executor.execute_locator(locator, message, typing_speed)


if __name__ == "__main__":

    async def main():
        """
        Пример использования Playwrid Crawler.
        """
        browser = Playwrid(options=["--headless"])
        await browser.start("https://www.example.com")

        # Получение HTML всего документа
        html_content = browser.get_page_content()
        if html_content:
            logger.info(html_content[:200])  # Выведем первые 200 символов для примера
        else:
            logger.info("Не удалось получить HTML-контент.")

        # Получение HTML элемента по селектору
        element_content = await browser.get_element_content("h1")
        if element_content:
            logger.info("\nСодержимое элемента h1:")
            logger.info(element_content)
        else:
            logger.info("\nЭлемент h1 не найден.")

        # Получение значения элемента по xpath
        xpath_value = await browser.get_element_value_by_xpath("//head/title")
        if xpath_value:
            logger.info(f"\nЗначение элемента по XPATH //head/title: {xpath_value}")
        else:
            logger.info("\nЭлемент по XPATH //head/title не найден")

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
        logger.info(f"Name: {name}")

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