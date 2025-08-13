## \file /src/webdriver/pydoll/driver.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3


"""
This module provides a high-level asynchronous driver for controlling a browser based on `pydoll`.
======================================================================================================
This module implements the asynchronous `Driver` class, which serves as a high-level wrapper around the `pydoll` library
for automating the Chrome browser. The main goal is to simplify interaction with web pages by
using a declarative approach based on 'locators'.

Key functionality:
- **Asynchronicity:** All browser operations are performed asynchronously using `asyncio`.
- **Context Manager:** Supports `async with` for automatically opening and closing the browser.
- **Control via locators:** Instead of sequential calls to a Selenium-like API, a single `execute_locator` method is used,
  which accepts a locator object. This object describes all the steps:
  finding an element, waiting for a certain state, performing an action (click, text input), and extracting
  data (text, attributes).
- **Configuration:** Browser settings (profile path, launch mode) are loaded from the `pydoll.json` file.

Locator example:
```json
{
  "reference": {
    "attribute": "innerText",
    "by": "XPATH",
    "strategy_for_multiple_selectors": "find_first_match",
    "selector": "//span[contains(@class, 'sku-copy')]",
    "if_list": "first",
    "mandatory": true,
    "timeout": 10,
    "timeout_for_event": "presence_of_element_located",
    "event": null,
    "text_to_be_present_in_element":"","locator_description": "product reference"
  }
}

Example of use:
```python
from src.webdriver.pydoll.driver import Driver

driver = Driver(window_mode='headless')

async with driver as browser:
    await browser.get_url('https://quotes.toscrape.com')
    reference = await browser.execute_locator(browser.page.locators.reference)
    print(reference)

```
"""

import asyncio
import os
import subprocess
from http.cookies import SimpleCookie
from pathlib import Path
from tracemalloc import start
from typing import List,  Optional, Any, TYPE_CHECKING
from types import SimpleNamespace
from dataclasses import dataclass, field

from header import __root__

# from src.webdriver.pydoll.llib.browser import Chrome
# if TYPE_CHECKING:
#     from src.webdriver.pydoll.llib.elements.web_element import WebElement
#     from src.webdriver.pydoll.llib.browser.tab import Tab as Base_Tab

from pydoll.browser import Chrome
if TYPE_CHECKING:
    from pydoll.elements.web_element import WabElement
    from pydoll.browser.tab import Tab as BaseTab

from src.webdriver.pydoll.options import Options # <- DO NOT CONFUSE with src.webdriver.pydoll.llib.options.Options
from src.webdriver.pydoll.tab import Tab
from src.utils.jjson import j_loads_ns
from src.utils.printer import pprint as print
from src.logger import logger


class Browser(Chrome):
    """
    High-level asynchronous driver for the Pydoll Chrome browser.

    Args:
        window_mode (Optional[str]): Window mode ('headless', 'normal'). By default, the value from Config is used.
        options (Optional[Options]): Custom options for launching Chrome.
        user_data_dir (Optional[str]): Path to the Chrome user profile.
        binary_location (Optional[str]): Path to the browser executable.
        user_agent (Optional[str]): Custom User-Agent.
        incognito (bool): Launch in incognito mode. Defaults to False.
        disable_gpu (bool): Disable GPU hardware acceleration. Defaults to True.
    """
    pid_file: Path = __root__ / 'src' / 'webdriver' / 'pydoll' / 'process.pid'
    def __init__(self, options: Optional[Options] = None, connection_port: Optional[int] = 0, **kwargs):
        """"""

        super().__init__(options = options or Options(), connection_port = connection_port)
        ...

    def kill_previous_pid(self):
        """! Deletes the PID file of the previous browser process, if it exists. """
        try:
            probably_pid = self.pid_file.read_text().strip()
        except FileNotFoundError as ex:
            return # File not found, do nothing

        if probably_pid:
            try:
                os.kill(int(probably_pid), 9)
                logger.info(f'process {probably_pid} successfully killed')
            except Exception as ex:
                logger.error(f'process {probably_pid} not successfully killed', ex)
                ...
            finally:
                self.pid_file.unlink(missing_ok=True)

    async def save_current_pid(self):
        """! Saves the PID of the current browser process to a file. """
        if self.process and self.process.pid:
            self.pid_file.write_text(str(self.process.pid),encoding='UTF-8')
        else:
            logger.warning("Process PID is not available, cannot save.")

    async def start(self) -> Optional[Tab]:
        """! Start the browser and create the first tab.

        Returns:
            Tab: The first tab if successful, None otherwise.
        """
        # If the program crashes - delete the previous PID (of the browser)
        self.kill_previous_pid()
        try:
            base_tab: 'BaseTab' = await super().start()
            await self.save_current_pid()
            tab = Tab(base_tab)
            return tab
        except Exception as ex:
            logger.error(f"Error starting browser: ",ex)
            return None

    async def close(self):
        """! Close the driver. """
        try:
            await super().close()
        except Exception:
            ... # Ignore error when closing the browser


# ======================================================================================
# Example usage
# ======================================================================================
if __name__ == "__main__":
    import asyncio

    async def main():
        """Example of launching the Browser and using it with a locator."""
        # Create a browser instance (default: headless mode from Options config)
        browser = Browser()

        # Use it as an async context manager
        async with browser as br:
            tab = await br.start()
            if not tab:
                logger.error("Failed to start the browser")
                return

            # Open a page
            await tab.goto("https://quotes.toscrape.com")

            # Execute a locator (example: take page title text)
            title_locator = {
                "attribute": "innerText",
                "by": "XPATH",
                "selector": "//h1"
            }
            try:
                result = await tab.execute_locator(title_locator)
                print("Page title:", result)
            except Exception as ex:
                logger.error("Error executing locator", ex, exc_info=True)

    asyncio.run(main())

