## \file src/webdriver/pydoll/tab.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Tab class for advanced work with Pydoll browser tabs.
===============================================================
This module provides the Tab class, which acts as a proxy for the base Tab from
the pydoll library. Each Tab instance represents an extended version of a Pydoll
browser tab, running asynchronously and independently of other tabs. This class
adds the powerful `execute_locator` method to support complex, multi-step browser
automations defined by a simple configuration object.

```rst
.. module:: src.webdriver.pydoll.tab
```
"""

import asyncio
import re
from types import SimpleNamespace, TracebackType
from typing import Any, List, Optional, TYPE_CHECKING, Type, Union

from src.webdriver.pydoll.llib.browser.tab import Tab as BaseTab
from src.webdriver.pydoll.llib.constants import By, Key

if TYPE_CHECKING:
    from src.webdriver.pydoll.llib.elements.web_element import WebElement
    from src.webdriver.pydoll.options import Options

# from pydoll.browser.tab import Tab as BaseTab
# from pydoll.constants import By, Key
# # Conditional imports for type checking
# if TYPE_CHECKING:
#     from pydoll.elements.web_element import WebElement
#     from src.webdriver.pydoll.options import Options

from src.logger.logger import logger

class Tab:
    """
    An enhanced version of a browser Tab that adds the `execute_locator` method
    and acts as a proxy for the original `pydoll.browser.tab.Tab` object.
    """
    # --- Configuration Constant for Development Mode ---
    DEV_MODE: bool = True

    # Dynamically define the default timeout based on the mode
    if DEV_MODE:
        DEFAULT_TIMEOUT: int = 120 
    else:
        DEFAULT_TIMEOUT: int = 10
    
    def __init__(self, base_tab: BaseTab):
        """
        Initializes the wrapper, storing the original tab object.
        
        Args:
            base_tab (BaseTab): The original tab instance from the pydoll library.
        """
        self._base_tab: 'BaseTab' = base_tab
        logger.info(
            f"Tab created. Mode: {'DEV' if self.DEV_MODE else 'PROD'}. "
            f"Default timeout: {self.DEFAULT_TIMEOUT}s."
        )

    def __getattr__(self, name: str) -> Any:
        """
        A magic method that redirects all attribute access
        to the original _base_tab object.
        
        Args:
            name (str): The name of the attribute being accessed.
            
        Returns:
            Any: The value of the attribute from the base object.
        """
        return getattr(self._base_tab, name)

    async def __aenter__(self) -> 'Tab':
        """
        Method for entering an asynchronous context manager.
        """
        logger.debug(f"Entering context for tab: {self._base_tab._target_id}")
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ):
        """
        Method for exiting an asynchronous context manager.
        """
        logger.debug(f"Exiting context for tab: {self._base_tab._target_id}. Closing tab.")
        try:
            await self.close()
        except Exception as ex:
            logger.error(f"Failed to close tab {self._base_tab._target_id} on exit: {ex}", ex, exc_info=True)

    @staticmethod
    def _parse_keys(key_string: str) -> List[Union[Key, str]]:
        """
        Parses a string with keys into a list of Key objects and regular strings.
        
        Args:
            key_string (str): A string representing keys, e.g., "'CONTROL+A'".

        Returns:
            List[Union[Key, str]]: A list of Key enums and strings for `send_keys`.
        """
        if not key_string:
            return []
    
        if (key_string.startswith("'") and key_string.endswith("'")) or \
           (key_string.startswith('"') and key_string.endswith('"')):
            key_string = key_string[1:-1]
    
        parsed_keys: List[Union[Key, str]] = []
        key_parts = key_string.split('+')
    
        for part in key_parts:
            part_stripped = part.strip()
            if not part_stripped: continue
            try:
                key_enum = Key[part_stripped.upper()]
                parsed_keys.append(key_enum)
            except KeyError:
                parsed_keys.append(part_stripped)
        return parsed_keys

    async def _perform_action(self, event_string: str, elements: List['WebElement'], locator: SimpleNamespace, message: Optional[str] = None) -> bool:
        """
        Performs ONE action command (click, text input, etc.) on the elements.
        """
        if not event_string or not elements:
            return False

        element_to_act_on = elements[0]
        try:
            if event_string.lower().startswith('send_keys'):
                # Use a non-greedy match to find content within the first parentheses
                match = re.search(r'\((.*?)\)', event_string)
                if not match:
                    logger.warning(f"Invalid format for send_keys. Expected send_keys(...), but got: {event_string}")
                    return False

                content_to_parse = match.group(1).strip()
                keys_to_send = self._parse_keys(content_to_parse)

                if keys_to_send:
                    await element_to_act_on.press_keyboard_key(*keys_to_send)
                else:
                    logger.warning(f"Could not parse any valid keys from '{content_to_parse}' in event: {event_string}")
                    return False
                return True

            match event_string.lower().replace('()', ''):
                case 'click':
                    await element_to_act_on.click()
                case 'hover' | 'mouse_over':
                    await element_to_act_on.hover()
                case 'scroll_into_view':
                    await element_to_act_on.scroll_into_view()
                case 'send_text' | 'send_message' | 'type_text':
                    if message is None:
                        logger.warning(f"Event '{event_string}' requires a 'message' parameter for locator: {locator.locator_description}")
                        return False
                    await element_to_act_on.type_text(message)
                case 'clear':
                    await element_to_act_on.clear()
                case 'submit':
                    await element_to_act_on.submit()
                case _:
                    logger.warning(f"Unsupported event command: {event_string}")
                    return False
            return True
        except Exception as ex:
            logger.error(f"Error executing event command '{event_string}' for '{locator.locator_description}': {ex}", exc_info=True)
            return False

    async def find(
        self,
        locator: SimpleNamespace,
        raise_exc: bool = True
    ) -> Optional[Union['WebElement', List['WebElement']]]:
        """
        Finds element(s) with waiting, using the timeout from the locator or the
        default timeout for the current mode (DEV/PROD).
        """
        by_strategy: Optional[By] = None
        locator_by_str = getattr(locator, 'by', 'xpath').lower()

        try:
            by_strategy = By(locator_by_str)
        except ValueError:
            logger.error(f"Unsupported 'by' strategy: '{locator.by}'. Please use one of: {[e.value for e in By]}")
            return None

        locator_timeout = getattr(locator, 'timeout', None)
        if locator_timeout is not None and locator_timeout > 0:
            timeout_to_use = locator_timeout
        elif locator_timeout is None:
            timeout_to_use = self.DEFAULT_TIMEOUT
        else:
            timeout_to_use = 0
        
        timeout_to_use = self.DEFAULT_TIMEOUT   # <- DEBUG

        el: List['WebElement'] = await self.find_or_wait_element(
                                                                by=by_strategy,
                                                                value = locator.selector,
                                                                timeout = timeout_to_use, # <- ЭТО ВАЖНО! Это таймаут асинхронного ожидания. 
                                                                # В дебагере я сделал его большим, но в проде это приведет к зависанию при поиске
                                                                find_all=True,
                                                                raise_exc=raise_exc
                                                            )
        return el

    async def execute_locator(self, locator: SimpleNamespace, message: Optional[str] = None, raise_exc: Optional[bool]=True) -> Optional[Union[List['WebElement'], List[str], str, bool]]:
        """
        Finds elements, performs a sequence of actions, and extracts data.
        """
        # --- Stage 0: Preprocessing ---
        if not getattr(locator, 'selector', None) and str(getattr(locator, 'by', '')).upper() != 'VALUE':
            if getattr(locator, 'mandatory', False):
                logger.error(f"Empty selector in a mandatory locator: {getattr(locator, 'locator_description', 'N/A')}")
            return False
        if str(getattr(locator, 'by', '')).upper() == 'VALUE':
            return getattr(locator, 'attribute', None)

        # --- Stage 1: SEARCH ---
        elements = await self.find(locator, raise_exc=raise_exc)
        if not elements:
            log_func = logger.error if getattr(locator, 'mandatory', False) else logger.warning
            log_func(f"Locator failed: No elements found for '{locator.locator_description}' with selector '{locator.selector}'")
            return False

        # --- Stage 2: EXECUTE ACTION SEQUENCE ---
        event_sequence = getattr(locator, 'event', None)
        if event_sequence:
            commands = [cmd.strip() for cmd in event_sequence.split(';') if cmd.strip()]
            for command in commands:
                action_successful = await self._perform_action(command, elements, locator, message)
                if not action_successful and getattr(locator, 'mandatory', False):
                    logger.error(f"Mandatory event sequence failed at step '{command}' for locator: {locator.locator_description}")
                    return False

        # --- Stage 3: DATA EXTRACTION ---
        attribute_to_get = getattr(locator, 'attribute', None)
        if not attribute_to_get:
            return elements

        try:
            extracted_data: list = []
            for el in elements:
                match attribute_to_get.lower():
                    case 'innertext':
                        extracted_data.append(await el.text)
                    case 'innerhtml':
                        extracted_data.append(await el.inner_html)
                    case _:
                        extracted_data.append(await el.get_attribute(attribute_to_get))
        except Exception as ex:
            logger.error(f"Failed to get attribute '{attribute_to_get}' for locator '{locator.locator_description}': {ex}", exc_info=True)
            return False

        # --- Stage 4: RESULT FILTERING ---
        if not extracted_data:
            logger.warning(f"No data extracted for locator: {locator.locator_description}")
            return []

        match getattr(locator, 'if_list', 'all'):
            case 'first': return extracted_data[0]
            case 'last': return extracted_data[-1]
            case 'even': return extracted_data[::2]
            case 'odd': return extracted_data[1::2]
            case list() as indices: return [extracted_data[i] for i in indices if isinstance(i, int) and i < len(extracted_data)]
            case int() as index: return extracted_data[index - 1] if 0 < index <= len(extracted_data) else None
            case _: return extracted_data

    async def get_url(self, url: str) -> bool:
        """Navigates the tab to the specified URL."""
        try:
            await self.go_to(url)
            return True
        except Exception as ex:
            logger.error(f'Failed to navigate to {url}', ex, exc_info=True)
            return False

# --- Example Usage --- 
async def experiment(locator: SimpleNamespace, headless: bool = False):
    """
    Demonstrates running pydoll.Chrome with a fully configured
    Options object.
    """
    from src.webdriver.pydoll.options import Options
    from src.webdriver.pydoll.llib.browser import Chrome

    logger.info(f"Starting experiment with headless={headless}")
    options: 'Options' = Options(headless=headless)
    logger.debug(f"Generated arguments for Chrome: {options.arguments}")

    try:
        async with Chrome(options=options) as browser:
            base_tab: 'BaseTab' = await browser.start()
            async with Tab(base_tab) as tab:
                await tab.get_url("https://www.google.com")
                message = "Hello, world!"
                await tab.execute_locator(locator=locator, message=message)
                await asyncio.sleep(5)
    except Exception as ex:
        logger.error("An error occurred during the experiment: ", ex, exc_info=True)

if __name__ == "__main__":
    google_locator = SimpleNamespace(**{
        "attribute": None,
        "by": "XPATH",
        "selector": "//textarea[@name = 'q']",
        "event": "send_text();send_keys('ENTER')",
        "mandatory": True,
        "locator_description": "Google search input"
    })
    asyncio.run(experiment(locator=google_locator, headless=False))
