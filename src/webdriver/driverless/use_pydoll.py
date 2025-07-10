import asyncio
from typing import List, Any
from types import SimpleNamespace
from pydoll.browser import Chrome
from pydoll.browser.options import ChromeOptions as Options
from pydoll.browser.page import Page
from pydoll.constants import By

from header import __root__
from src.logger import logger

class Driver(Chrome):
    """! Driver class for Pydoll Chrome browser. """

    page: Page = None

    def __init__(self, **kwargs):
        """! Synchronous constructor; use `await async_init()` for full setup.

        Args:
        **kwargs: Arbitrary keyword arguments passed to Chrome constructor.
        """
            # Configure browser options
        options = Options()
        #options.add_argument('--proxy-server=username:password@ip:port')
        #options.add_argument('--window-size=1920,1080')
        #options.add_argument('--start-maximized')
        #options.binary_location = '/path/to/your/browser'
        #options.headless = kwargs.get('headless', True)  # Default to headless mode

        options.add_argument('--headless=new')
        options.add_argument('--disable-notifications')

        

        super().__init__(options = options, **kwargs, )
        self.page: Page = self.get_page()

    async def close(self):
        """! Close the driver. """
        await self.page.close()
        await super().close()

    async def execute_locator(self, locator: SimpleNamespace) -> Any:
        """! Locate and return content from the element based on locator info.

        Args:
        locator (SimpleNamespace): Locator configuration object.

        Returns:
        Any: The data extracted or list of elements depending on locator and strategy.

        Raises:
        ValueError: If an unsupported attribute is requested.
        """

        if locator.by.upper() == 'VALUE':
            return locator.attribute

        res: list = []
        elements: 'WebElement' | list['WebElement'] = None

        # Strategy for multiple selectors (XPATH не умеет в жадные операторы)
        match getattr(locator, 'strategy_for_multiple_selectors', 'find_first_match').lower():
            case 'find_first_match':
                selectors: list = locator.selector.split(';')
                for selector in selectors:
                    try:
                        elements = await self.page.find_elements(By[locator.by.upper()], selector)
                        if elements:
                            break
                    except Exception as ex:
                        logger.warning(f"Error executing locator: {locator}", ex, exc_info=True)
                        return None

        match getattr(locator, 'attribute', '').lower():
            case '':
                # If no attribute is provided, return WebElement object(s)
                res = elements

            case 'innertext':
                if len(elements) == 1:
                    return await elements[0].get_element_text()
                res = [await el.get_element_text() for el in elements]

            case 'innerhtml':
                if len(elements) == 1:
                    return await elements[0].inner_html
                res = [await el.inner_html for el in elements]

            case 'src' | 'href':
                if len(elements) == 1:
                    return await elements[0].get_attribute(locator.attribute)
                res = [await el.get_attribute(locator.attribute) for el in elements]

            case _:
                raise ValueError(f"Unsupported attribute: {locator=}")

        # List filtering strategy
        if_list = getattr(locator, 'if_list', '')
        match if_list:
            case '':
                return res
            case 'all':
                return res
            case 'first':
                return res[0]
            case 'last':
                return res[-1]
            case 'even':
                return [res[i] for i in range(0, len(res), 2)]
            case 'odd':
                return [res[i] for i in range(1, len(res), 2)]
            case list() if isinstance(if_list, list):
                return [res[i] for i in if_list if isinstance(i, int)]
            case int() if isinstance(if_list, int):
                return res[if_list - 1]

        return None

    async def get_url(self, url: str) -> bool:
        """! Navigate to the given URL.

        Args:
        url (str): The target URL.

        Returns:
        bool: `True` if navigation was successful, else `False`.
        """
        try:
            await self.page.go_to(url)
            return True
        except Exception as ex:
            logger.error(f"Failed to navigate to URL: {url}", ex)
            return False
