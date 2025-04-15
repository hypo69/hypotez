### **Анализ кода модуля `playwrid.py`**

## \file /src/webdriver/playwright/playwrid.py

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Использование `logger` для логирования.
    - Наличие docstring для большинства функций и методов.
    - Использование `j_loads_ns` для загрузки конфигурационных файлов.
    - Аннотация типов для переменных и параметров функций.
- **Минусы**:
    - Не все функции и методы имеют подробные docstring на русском языке.
    - Местами отсутствуют пробелы вокруг операторов присваивания.
    - В некоторых блоках `try-except` используется `e` вместо `ex` для исключений.
    - Отсутствует заголовок модуля с описанием.

**Рекомендации по улучшению:**

1.  **Добавить заголовок модуля**:

*   Добавить заголовок в начале файла с описанием модуля, его назначения и примером использования.

    ```python
    """
    Модуль для работы с Playwright Crawler
    =================================================

    Модуль содержит класс :class:`Playwrid`, который является подклассом `PlaywrightCrawler`
    и предоставляет дополнительные функции для настройки браузера, профилей и параметров запуска.

    Пример использования
    ----------------------

    >>> browser = Playwrid(options=["--headless"])
    >>> browser.start("https://www.example.com")
    """
    ```

2.  **Улучшить и перевести docstring**:

*   Перевести все docstring на русский язык и сделать их более подробными, следуя указанному формату.
*   Для каждой функции добавить пример использования в docstring.
*   В docstring указывать, что именно делает функция, а не просто "выполняет действие".

    ```python
    def __init__(self, user_agent: Optional[str] = None, options: Optional[List[str]] = None, *args, **kwargs) -> None:
        """
        Инициализирует Playwright Crawler с указанными параметрами запуска, настройками и User-Agent.

        Args:
            user_agent (Optional[str], optional): User-Agent, который будет использоваться. По умолчанию None.
            options (Optional[List[str]], optional): Список опций Playwright для передачи при инициализации. По умолчанию None.
            *args: Произвольные позиционные аргументы для `PlaywrightCrawler`.
            **kwargs: Произвольные именованные аргументы для `PlaywrightCrawler`.

        Returns:
            None

        Example:
            >>> browser = Playwrid(user_agent='CustomUserAgent', options=['--disable-gpu'])
        """
    ```

3.  **Исправить обработку исключений**:

*   Заменить все переменные исключений `e` на `ex` и добавить логирование ошибок с использованием `logger.error`.

    ```python
    try:
        element = self.context.page.locator(selector)
        return await element.inner_html()
    except Exception as ex:
        logger.warning(f"Element with selector '{selector}' not found or error during extraction: {ex}", exc_info=True)
        return None
    ```

4.  **Добавить пробелы вокруг операторов присваивания**:

*   Убедиться, что вокруг всех операторов присваивания (`=`) есть пробелы.

    ```python
    launch_options = {
        "headless": self.config.headless if hasattr(self.config, 'headless') else True,
        "args": self.config.options if hasattr(self.config, 'options') else []
    }
    ```

5.  **Удалить неиспользуемые импорты**:

*   Удалить закомментированные импорты:
    `#from crawlee.playwright_crawler import PlaywrightCrawler, PlaywrightCrawlingContext`

6.  **Использовать `driver.execute_locator`**:

*   Код уже использует `driver.execute_locator`, что соответствует требованиям.

**Оптимизированный код:**

```python
## \file /src/webdriver/playwright/playwrid.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для работы с Playwright Crawler
=================================================

Модуль содержит класс :class:`Playwrid`, который является подклассом `PlaywrightCrawler`
и предоставляет дополнительные функции для настройки браузера, профилей и параметров запуска.

Пример использования
----------------------

>>> browser = Playwrid(options=["--headless"])
>>> browser.start("https://www.example.com")
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
    Подкласс `PlaywrightCrawler`, который предоставляет дополнительные функции.

    Attributes:
        driver_name (str): Имя драйвера, по умолчанию 'playwrid'.
    """
    driver_name: str = 'playwrid'
    base_path: Path = __root__ / 'src' / 'webdriver' / 'playwright'
    config: SimpleNamespace = j_loads_ns(base_path / 'playwrid.json')
    context: PlaywrightCrawlingContext | None = None

    def __init__(self, user_agent: Optional[str] = None, options: Optional[List[str]] = None, *args, **kwargs) -> None:
        """
        Инициализирует Playwright Crawler с указанными параметрами запуска, настройками и User-Agent.

        Args:
            user_agent (Optional[str], optional): User-Agent, который будет использоваться. По умолчанию None.
            options (Optional[List[str]], optional): Список опций Playwright для передачи при инициализации. По умолчанию None.
            *args: Произвольные позиционные аргументы для `PlaywrightCrawler`.
            **kwargs: Произвольные именованные аргументы для `PlaywrightCrawler`.

        Returns:
            None

        Example:
            >>> browser = Playwrid(user_agent='CustomUserAgent', options=['--disable-gpu'])
        """
        launch_options = self._set_launch_options(user_agent, options)
        self.executor = PlaywrightExecutor()
        # Pass launch_options to PlaywrightCrawler if it accepts them
        # Otherwise, remove launch_options from the parameters
        super().__init__(
            browser_type = self.config.browser_type,
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
            user_agent (Optional[str], optional): User-Agent, который будет использоваться. По умолчанию None.
            options (Optional[List[str]], optional): Список опций Playwright для передачи при инициализации. По умолчанию None.

        Returns:
            Dict[str, Any]: Словарь с параметрами запуска для Playwright.

        Example:
            >>> launch_options = self._set_launch_options(user_agent='CustomUserAgent', options=['--disable-gpu'])
            >>> print(launch_options)
            {'headless': True, 'args': ['--disable-gpu'], 'user_agent': 'CustomUserAgent'}
        """
        launch_options = {
            "headless": self.config.headless if hasattr(self.config, 'headless') else True,
            "args": self.config.options if hasattr(self.config, 'options') else []
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

        Returns:
            None

        Raises:
            Exception: Если Playwrid Crawler завершается с ошибкой.

        Example:
            >>> browser = Playwrid(options=["--headless"])
            >>> await browser.start("https://www.example.com")
        """
        try:
            logger.info(f"Starting Playwright Crawler for {url}")
            await self.executor.start()  # Start the executor
            await self.executor.goto(url) # Goto url
            super().run(url) # run crawler
            # получаем контекст
            self.context = self.crawling_context
        except Exception as ex:
            logger.critical('Playwrid Crawler failed with an error:', ex, exc_info=True)

    @property
    def current_url(self) -> Optional[str]:
        """
        Возвращает текущий URL браузера.

        Returns:
            Optional[str]: Текущий URL.

        Example:
            >>> browser = Playwrid(options=["--headless"])
            >>> await browser.start("https://www.example.com")
            >>> current_url = browser.current_url
            >>> print(current_url)
            'https://www.example.com'
        """
        if self.context and self.context.page:
            return self.context.page.url
        return None

    def get_page_content(self) -> Optional[str]:
        """
        Возвращает HTML-контент текущей страницы.

        Returns:
            Optional[str]: HTML-контент страницы.

        Example:
            >>> browser = Playwrid(options=["--headless"])
            >>> await browser.start("https://www.example.com")
            >>> page_content = browser.get_page_content()
            >>> print(page_content[:100])
            '<!doctype html>...'
        """
        if self.context and self.context.page:
            return self.context.page.content()
        return None

    async def get_element_content(self, selector: str) -> Optional[str]:
        """
        Возвращает внутренний HTML-контент одного элемента на странице по CSS-селектору.

        Args:
            selector (str): CSS-селектор для элемента.

        Returns:
            Optional[str]: Внутренний HTML-контент элемента или None, если элемент не найден.

        Example:
            >>> browser = Playwrid(options=["--headless"])
            >>> await browser.start("https://www.example.com")
            >>> element_content = await browser.get_element_content("h1")
            >>> print(element_content)
            'Example Domain'
        """
        if self.context and self.context.page:
            try:
                element = self.context.page.locator(selector)
                return await element.inner_html()
            except Exception as ex:
                logger.warning(f"Element with selector '{selector}' not found or error during extraction: {ex}", exc_info=True)
                return None
        return None

    async def get_element_value_by_xpath(self, xpath: str) -> Optional[str]:
        """
        Возвращает текстовое значение одного элемента на странице по XPath.

        Args:
            xpath (str): XPath элемента.

        Returns:
            Optional[str]: Текстовое значение элемента или None, если элемент не найден.

        Example:
            >>> browser = Playwrid(options=["--headless"])
            >>> await browser.start("https://www.example.com")
            >>> xpath_value = await browser.get_element_value_by_xpath("//head/title")
            >>> print(xpath_value)
            'Example Domain'
        """
        if self.context and self.context.page:
            try:
                element = self.context.page.locator(f'xpath={xpath}')
                return await element.text_content()
            except Exception as ex:
                logger.warning(f"Element with XPath '{xpath}' not found or error during extraction: {ex}", exc_info=True)
                return None
        return None

    async def click_element(self, selector: str) -> None:
        """
        Кликает на один элемент на странице по CSS-селектору.

        Args:
            selector (str): CSS-селектор элемента для клика.

        Returns:
            None

        Example:
            >>> browser = Playwrid(options=["--headless"])
            >>> await browser.start("https://www.example.com")
            >>> await browser.click_element("button")
        """
        if self.context and self.context.page:
            try:
                element = self.context.page.locator(selector)
                await element.click()
            except Exception as ex:
                logger.warning(f"Element with selector '{selector}' not found or error during click: {ex}", exc_info=True)
    
    async def execute_locator(self, locator: dict | SimpleNamespace, message: Optional[str] = None, typing_speed: float = 0) -> str | List[str] | bytes | List[bytes] | bool:
        """
        Выполняет локатор через executor

        Args:
            locator (dict | SimpleNamespace): Данные локатора.
            message (Optional[str], optional): Опциональное сообщение для событий. Defaults to None.
            typing_speed (float, optional): Опциональная скорость печати для событий. Defaults to 0.

        Returns:
            str | List[str] | bytes | List[bytes] | bool: Статус выполнения.
        """
        return await self.executor.execute_locator(locator, message, typing_speed)
    

if __name__ == "__main__":
    async def main():
        browser = Playwrid(options=["--headless"])
        await browser.start("https://www.example.com")
        
        # Получение HTML всего документа
        html_content = browser.get_page_content()
        if html_content:
            print(html_content[:200])  # Выведем первые 200 символов для примера
        else:
            print("Не удалось получить HTML-контент.")
        
        # Получение HTML элемента по селектору
        element_content = await browser.get_element_content("h1")
        if element_content:
            print("\\nСодержимое элемента h1:")
            print(element_content)
        else:
            print("\\nЭлемент h1 не найден.")
        
        # Получение значения элемента по xpath
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