# Playwrid - Playwright Crawler

## Overview

This module defines a subclass of `PlaywrightCrawler` called `Playwrid`. It provides additional functionality such as the ability to set custom browser settings, profiles, and launch options using Playwright. It is a useful tool for web scraping and automated testing. 

## Details

The module utilizes Playwright to interact with web pages and performs tasks such as browsing, extracting data, clicking elements, and executing custom code. It leverages features like custom user agents and headless browsing to enhance functionality and flexibility. This class is specifically designed for projects where you need a controlled and reliable way to interact with websites.

## Classes

### `Playwrid`

**Description**:  A subclass of `PlaywrightCrawler` that extends its functionality to work with Playwright, a popular web automation library. This subclass allows for custom browser settings, profiles, and launch options.
**Inherits**: `PlaywrightCrawler` 

**Attributes**:

 - `driver_name (str)`: Name of the driver, defaults to 'playwrid'.
 - `base_path (Path)`:  The base path for the Playwright configuration file, set to the directory of the Playwright configuration file.
 - `config (SimpleNamespace)`: A `SimpleNamespace` object that loads and holds the configuration data from the `playwrid.json` file. It provides an easy and structured way to access the configuration properties.
 - `context`: An object that represents the current Playwright browsing context, which includes the browser page and other related information. This allows for managing the browsing environment and interacting with the active page. 

**Methods**:

 - `__init__(self, user_agent: Optional[str] = None, options: Optional[List[str]] = None, *args, **kwargs) -> None`
   - **Purpose**: This method initializes the Playwright Crawler with the specified launch options, settings, and user agent. 
   - **Parameters**:
     - `user_agent (Optional[str])`: The user agent string to be used, it is set in the `playwrid.json` configuration file. 
     - `options (Optional[List[str]])`: A list of Playwright options to be passed during initialization, they are set in the `playwrid.json` configuration file.
 - `_set_launch_options(self, user_agent: Optional[str] = None, options: Optional[List[str]] = None) -> Dict[str, Any]`
   - **Purpose**: This method configures the launch options for the Playwright Crawler. 
   - **Parameters**: 
     - `settings (SimpleNamespace)`: A `SimpleNamespace` object containing launch settings from the `playwrid.json` configuration file. 
     - `user_agent (Optional[str])`: The user agent string to be used. 
     - `options (Optional[List[str]])`: A list of Playwright options to be passed during initialization.
   - **Returns**: A dictionary with launch options for Playwright.
 - `async def start(self, url: str) -> None`
   - **Purpose**: This method starts the Playwrid Crawler and navigates to the specified URL. 
   - **Parameters**:
     - `url (str)`: The URL to navigate to. 
   - **Exceptions**:
     - `Exception`: If there is an error starting or running the crawler, it will log a critical error message and raise an exception. 
 - `@property\ndef current_url(self) -> Optional[str]`
   - **Purpose**: Returns the current URL of the browser. 
   - **Returns**: The current URL.
 - `def get_page_content(self) -> Optional[str]`
   - **Purpose**: Returns the HTML content of the current page. 
   - **Returns**: HTML content of the page. 
 - `async def get_element_content(self, selector: str) -> Optional[str]`
   - **Purpose**: Returns the inner HTML content of a single element on the page by CSS selector.
   - **Parameters**:
     - `selector (str)`: CSS selector for the element.
   - **Returns**: Inner HTML content of the element, or None if not found.
 - `async def get_element_value_by_xpath(self, xpath: str) -> Optional[str]`
   - **Purpose**: Returns the text value of a single element on the page by XPath.
   - **Parameters**:
     - `xpath (str)`: XPath of the element.
   - **Returns**: The text value of the element, or None if not found. 
 - `async def click_element(self, selector: str) -> None`
   - **Purpose**: Clicks a single element on the page by CSS selector. 
   - **Parameters**:
     - `selector (str)`: CSS selector of the element to click. 
 - `async def execute_locator(self, locator: dict | SimpleNamespace, message: Optional[str] = None, typing_speed: float = 0) -> str | List[str] | bytes | List[bytes] | bool`
   - **Purpose**: Executes a locator through the executor.
   - **Parameters**: 
     - `locator (dict | SimpleNamespace)`: Locator data (dict or SimpleNamespace). 
     - `message (Optional[str])`: Optional message for events. 
     - `typing_speed (float)`: Optional typing speed for events.
   - **Returns**: Execution status. 

## Example File

```python
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
    Subclass of `PlaywrightCrawler` that provides additional functionality.

    Attributes:
        driver_name (str): Name of the driver, defaults to 'playwrid'.
    """
    driver_name: str = 'playwrid'
    base_path: Path = __root__ / 'src' / 'webdriver' / 'playwright'
    config: SimpleNamespace = j_loads_ns(base_path / 'playwrid.json')
    context = None

    def __init__(self, user_agent: Optional[str] = None, options: Optional[List[str]] = None, *args, **kwargs) -> None:
        """
        Initializes the Playwright Crawler with the specified launch options, settings, and user agent.
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
        Configures the launch options for the Playwright Crawler.

        :param settings: A SimpleNamespace object containing launch settings.
        :type settings: SimpleNamespace
        :param user_agent: The user-agent string to be used.
        :type user_agent: Optional[str]
        :param options: A list of Playwright options to be passed during initialization.
        :type options: Optional[List[str]]
        :returns: A dictionary with launch options for Playwright.
        :rtype: Dict[str, Any]
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
        Starts the Playwrid Crawler and navigates to the specified URL.

        :param url: The URL to navigate to.
        :type url: str
        """
        try:
            logger.info(f"Starting Playwright Crawler for {url}")
            await self.executor.start()  # Start the executor
            await self.executor.goto(url) # Goto url
            super().run(url) # run crawler
            # получаем контекст
            self.context = self.crawling_context
        except Exception as ex:
            logger.critical('Playwrid Crawler failed with an error:', ex)

    @property
    def current_url(self) -> Optional[str]:
        """
        Returns the current URL of the browser.

        :returns: The current URL.
        :rtype: Optional[str]
        """
        if self.context and self.context.page:
            return self.context.page.url
        return None

    def get_page_content(self) -> Optional[str]:
        """
        Returns the HTML content of the current page.

        :returns: HTML content of the page.
        :rtype: Optional[str]
        """
        if self.context and self.context.page:
            return self.context.page.content()
        return None

    async def get_element_content(self, selector: str) -> Optional[str]:
        """
        Returns the inner HTML content of a single element on the page by CSS selector.

        :param selector: CSS selector for the element.
        :type selector: str
        :returns: Inner HTML content of the element, or None if not found.
        :rtype: Optional[str]
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
        Returns the text value of a single element on the page by XPath.

        :param xpath: XPath of the element.
        :type xpath: str
        :returns: The text value of the element, or None if not found.
        :rtype: Optional[str]
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
        Clicks a single element on the page by CSS selector.

        :param selector: CSS selector of the element to click.
        :type selector: str
        """
        if self.context and self.context.page:
            try:
                element = self.context.page.locator(selector)
                await element.click()
            except Exception as ex:
                logger.warning(f"Element with selector '{selector}' not found or error during click: {ex}")
    
    async def execute_locator(self, locator: dict | SimpleNamespace, message: Optional[str] = None, typing_speed: float = 0) -> str | List[str] | bytes | List[bytes] | bool:
        """
        Executes locator through executor

        :param locator: Locator data (dict or SimpleNamespace).
        :type locator: dict | SimpleNamespace
        :param message: Optional message for events.
        :type message: Optional[str]
        :param typing_speed: Optional typing speed for events.
        :type typing_speed: float
        :returns: Execution status.
        :rtype: str | List[str] | bytes | List[bytes] | bool
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
            print("\nСодержимое элемента h1:")
            print(element_content)
        else:
            print("\nЭлемент h1 не найден.")
        
        # Получение значения элемента по xpath
        xpath_value = await browser.get_element_value_by_xpath("//head/title")
        if xpath_value:
             print(f"\nЗначение элемента по XPATH //head/title: {xpath_value}")
        else:
             print("\nЭлемент по XPATH //head/title не найден")

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
```