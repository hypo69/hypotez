import asyncio
from typing import List, Any
from types import SimpleNamespace
from pydoll.browser import Chrome
from pydoll.browser.options import ChromeOptions as Options
from pydoll.browser.page import Page
from pydoll.constants import By
from pydoll.element import WebElement

from header import __root__
from src.utils.printer import pprint as print
from src.logger import logger

class Driver(Chrome):
    """! Driver class for Pydoll Chrome browser. """

    page: Page = None

    def __init__(self,  **kwargs):
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
        
    async def async_init_page(self):
        """! Asynchronous initialization to set up the page.
        
        This method should be called after creating the Driver instance.
        
        Returns:
        Driver: Self reference for method chaining.
        """
        if self.page is None:
            self.page = await self.get_page()
        return self

    async def close(self):
        """! Close the driver. """
        if self.page:
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
        # Ensure page is initialized
        if not self.page:
            await self.async_init()

        res: list = []
        elements: WebElement | list[WebElement] = None
        selectors: list = []

        if not locator.selector or locator.selector == '':
            ...
            logger.error(f"Locator selector is empty: {print(locator.__dict__)}")
            return False

        if ';' in locator.selector:
            selectors = locator.selector.split(';')
        else:
            selectors = [locator.selector]

        # Special case for 'value' in starteg `BY` returned value from locator.attribute
        # f.e. supplier_id = locator.attribute
        if str(locator.by).upper() == 'VALUE':  
            return locator.attribute

        # Strategy for multiple selectors (XPATH не умеет в ленивые операторы)
        match getattr(locator, 'strategy_for_multiple_selectors', 'find_first_match').lower():
            case 'find_first_match':
                for selector in selectors:
                    try:
                        elements = await self.page.find_elements(By[locator.by.upper()], selector)

                    except Exception as ex:
                        logger.warning(f"Error executing locator: {locator}", ex, exc_info=True)
                        return False
        ...
        match getattr(locator, 'attribute', '').lower():
            case '':
                # If no attribute is provided, return WebElement object(s)
                _result = elements

            case 'innertext':
                if len(elements) == 1:
                    return await elements[0].get_element_text()
                _result= [await el.get_element_text() for el in elements]
                ...

            case 'innerhtml':
                if len(elements) == 1:
                    return await elements[0].inner_html
                _result= [await el.inner_html for el in elements]

            case 'src' | 'href':
                if len(elements) == 1:
                    return await elements[0].get_attribute(locator.attribute)
                _result= [await el.get_attribute(locator.attribute) for el in elements]

            case _:
                raise ValueError(f"Unsupported attribute: {locator=}")
        ...
        # List filtering strategy
        if_list = getattr(locator, 'if_list', '')
        match if_list:
            case '':
                return _result
            case 'all':
                return _result
            case 'first':
                return _result[0]
            case 'last':
                return _result[-1]
            case 'even':
                return [_result[i] for i in range(0, len(_result), 2)]
            case 'odd':
                return [_result[i] for i in range(1, len(_result), 2)]
            case list() if isinstance(if_list, list):
                return [_result[i] for i in if_list if isinstance(i, int)]
            case int() if isinstance(if_list, int):
                return _result[if_list - 1]
            case _:
                return _result
        return None

    async def get_url(self, url: str) -> bool:
        """! Navigate to the given URL.

        Args:
        url (str): The target URL.

        Returns:
        bool: `True` if navigation was successful, else `False`.
        """
        # Ensure page is initialized
        if self.page is None:
            await self.async_init()
            
        try:
            await self.page.go_to(url)
            return True
        except Exception as ex:
            logger.error(f"Failed to navigate to URL: {url}", ex)
            return False