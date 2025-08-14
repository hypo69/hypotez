# # \file /src/webdriver/pydoll/driver.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3


"""This module provides a high-level asynchronous driver for controlling a browser based on `pydoll`.
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
    await browser.get_url('https://toscrape.com/')
    reference = await browser.execute_locator(browser.page.locators.reference)
    print(reference)

```"""

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

from src.webdriver.pydoll.llib.browser import Chrome
if TYPE_CHECKING:
    from src.webdriver.pydoll.llib.elements.web_element import WebElement
    from src.webdriver.pydoll.llib.browser.tab import Tab as Base_Tab

# from pydoll.browser import Chrome
# if TYPE_CHECKING:
# from pydoll.elements.web_element import WabElement
# from pydoll.browser.tab import Tab as BaseTab

from src.webdriver.pydoll.options import Options # <- DO NOT CONFUSE with src.webdriver.pydoll.llib.options.Options
from src.webdriver.pydoll.tab import Tab
from src.utils.jjson import j_loads_ns
from src.utils.printer import pprint as print
from src.logger import logger


class Browser(Chrome):
    """High-level asynchronous driver for the Pydoll Chrome browser.

    Args:
        window_mode (Optional[str]): Window mode ('headless', 'normal'). By default, the value from Config is used.
        options (Optional[Options]): Custom options for launching Chrome.
        user_data_dir (Optional[str]): Path to the Chrome user profile.
        binary_location (Optional[str]): Path to the browser executable.
        user_agent (Optional[str]): Custom User-Agent.
        incognito (bool): Launch in incognito mode. Defaults to False.
        disable_gpu (bool): Disable GPU hardware acceleration. Defaults to True."""
    pid_file: Path = __root__ / 'src' / 'webdriver' / 'pydoll' / 'process.pid'
    def __init__(self, options: Optional[Options] = None, connection_port: Optional[int] = 0, **kwargs):
        """"""
        super().__init__(options = options or Options(), connection_port = connection_port, **kwargs)
        ...

    def _kill_previous_pid(self) -> None:
        """.. method:: _kill_previous_pid()
           :platform: Linux, Windows, macOS
           :synopsis: Deletes the PID file of the previous browser process, if it exists.

        Reads the PID from the stored PID file, attempts to terminate the process,
        and deletes the PID file afterward. All operations are performed with
        safe attribute checks to avoid unexpected exceptions.

        Returns:
            None

        Example:
            ```python
            obj._kill_previous_pid()
            ```"""
        pid_file = getattr(self, "pid_file", None)
        if not pid_file:
            ... # logger.error("pid_file attribute is missing, cannot kill previous PID.", exc_info=True)
            return

        saved_pid: Optional[str] = pid_file.read_text().strip() if pid_file.exists() else None

        try:
            if saved_pid:
                os.kill(int(saved_pid), 9)
                logger.info(f"Process {saved_pid} killed.")
        except Exception as ex:
            logger.error(f"Failed to kill process {saved_pid}.", ex, exc_info=True)
        finally:
            pid_file.unlink(missing_ok=True)


    async def _save_current_pid(self) -> bool:
        """Saves the process ID (PID) of the current browser process into the predefined PID file. 


        Returns:
            bool: ``True`` if PID was successfully saved, ``False`` otherwise.

        Example:
            ```python
            success = await obj.save_current_pid()
            if success:
                logger.info("PID saved successfully.")
            else:
                logger.warning("Failed to save PID.")
            ```"""
        try:

            _process_manager = getattr(self, '_browser_process_manager', None)
            _process = getattr(_process_manager, '_process', None)
            if _process:
                pid = getattr(_process, 'pid', None)
                pid_file = getattr(self, "pid_file", None)
                pid_file.write_text(str(pid), encoding="UTF-8")
                self._pid = pid
                return True
        except Exception as ex:
            logger.error(f'Ошибка сохранения PID' , ex)
            return False



    async def start(self) -> Optional[Tab]:
        """Starts the browser, creates the first tab, and saves the PID
        of the running browser process. If a previous PID exists,
        it is killed before starting the new browser process.

        Returns:
            Optional[Tab]: The first browser tab if successful, ``None`` otherwise.

        Example:
            ```python
            tab = await obj.start()
            if not tab:
                logger.error("Browser failed to start.")
            ```"""
        # Delete the previous PID if it exists
        if not self._kill_previous_pid():
            ... # <- MB error in the file, but not critical

        try:
            base_tab: BaseTab = await super().start()
            if not base_tab:
                logger.error("BaseTab is None after starting browser.", exc_info=True)
                return None

            # Save the current PID
            if not await self._save_current_pid():
                logger.error("Failed to save current PID before starting browser.", exc_info=True)

            return Tab(base_tab)
        except Exception as ex:
            logger.error("Error starting browser:", ex, exc_info=True)
            return None


    async def close(self):
        """! Close the driver."""
        try:
            await super().close()
        except Exception:
            ... # Ignore error when closing the browser


# None
# Example usage
# None
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
            await tab.goto("https://toscrape.com/")

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

