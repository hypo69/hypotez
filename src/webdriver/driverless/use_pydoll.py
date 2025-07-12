import asyncio
from typing import List, Any, Optional
from types import SimpleNamespace
from pydoll.browser import Chrome 
from pydoll.browser.options import ChromeOptions as Options
from pydoll.browser.page import Page
from pydoll.constants import By
from pydoll.element import WebElement

from header import __root__
from src.credentials import j_loads_ns
from src.utils.printer import pprint as print
from src.logger import logger

class Config:
        """! Configuration class for Pydoll Chrome browser. """
        # Default configuration values can be set here if needed
        # For example, you can set default user agent, window size, etc.
        config: SimpleNamespace = j_loads_ns(__root__ / 'src' / 'webdriver' / 'driverless' / 'use_pydoll.json')
        user_profile_path: str = config.user_profile_path
        WINDOW_MODE:str =  config.WINDOW_MODE

class Driver(Chrome):
    """! Driver class for Pydoll Chrome browser. """

    page: Page = None

    def __init__(self, 
                    window_mode: Optional[str] = 'headless', 
                    enable_user_profile: Optional[bool] = True,
                    user_profile_path: Optional[str] = None,
                    **kwargs
                    
                ):
        """! Synchronous constructor; 
        Use `await async_init_page()` for full setup!

        Args:
            profile_path (str, optional): Path to Chrome user profile directory
            **kwargs: Arbitrary keyword arguments passed to Chrome constructor.
        """
        # Configure browser options
        options = Options()
        
        # Настройка пользовательского профиля
        if enable_user_profile:
            # Способ 1: Указать директорию пользовательских данных
            options.add_argument(f'--user-data-dir={user_profile_path or Config.profile_path}')
            
            # Способ 2: Указать конкретный профиль (если нужен определенный профиль)
            # options.add_argument(f'--profile-directory=Profile 1')  # или Default, Profile 2, etc.
        
        # Дополнительные опции для работы с профилем
        if enable_user_profile:
            # Отключить первый запуск и восстановление
            options.add_argument('--no-first-run')
            options.add_argument('--no-default-browser-check')
            options.add_argument('--disable-default-apps')
            
        #options.add_argument('--proxy-server=username:password@ip:port')
        #options.add_argument('--window-size=1920,1080')
        #options.add_argument('--start-maximized')
        #options.binary_location = fr'C:\Program Files\Google\Chrome\Application\chrome.exe'
        
        if kwargs.get('window_mode', 'headless') == 'headless':
            options.add_argument('--headless=new')

        #options.add_argument('--disable-notifications')

        super().__init__(options = options)
        
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

    async def execute_locator(self, locator: SimpleNamespace) -> str |  list | WebElement | bool :
        """! Locate and return content from the element based on locator info.

        Args:
            locator (SimpleNamespace): Locator configuration object.

        Returns:
            Any: The data extracted or list of elements depending on locator and strategy.

        Raises:
            ValueError: If an unsupported attribute is requested.

        locator exmaple:
          "reference": {
                        "attribute": "innerText",
                        "by": "XPATH",
                        "strategy_for_multiple_selectors": "find_first_match","selector": "//span[ contains( @class, 'sku-copy')]",
                        "strategy_for_multiple_selectors": "find_first_match",
                        "if_list": "first",
                        "mandatory": true,
                        "timeout": 0,
                        "timeout_for_event": "presence_of_element_located",
                        "event": null,
                        "locator_description": "product reference"
                  }
        """
        # Ensure page is initialized
        if not self.page:
            await self.async_init()

        res: list = []
        elements: WebElement | list[WebElement] = None
        selectors: list = []

        if not locator.selector or locator.selector == '':
            ...
            if locator.mandatory: 
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
                        ...
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
                if isinstance(_result, list) and len(_result) == 0:
                    return False
                ...

            case 'innerhtml':
                if len(elements) == 1:
                    return await elements[0].inner_html
                _result= [await el.inner_html for el in elements]
                if isinstance(_result, list) and len(_result) == 0:
                    return False
                ...

            case 'src' | 'href':
                if len(elements) == 1:
                    return await elements[0].get_attribute(locator.attribute)
                _result= [await el.get_attribute(locator.attribute) for el in elements]
                if isinstance(_result, list) and len(_result) == 0:
                    return False
                ...

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
                return _result[0] if isinstance(_result, list) else _result 
            case 'last':
                return _result[-1] if isinstance(_result, list) else _result 
            case 'even':
                return [_result[i] for i in range(0, len(_result), 2)]  if isinstance(_result, list) else _result 
            case 'odd':
                return [_result[i] for i in range(1, len(_result), 2)]  if isinstance(_result, list) else _result 
            case list() if isinstance(if_list, list): # <- список полей по номерам. Например [1,6,8]
                return [_result[i] for i in if_list if isinstance(i, int)] if isinstance(_result, list) else _result 
            case int() if isinstance(if_list, int): # <-  полей по номеру. Например 4
                return _result[if_list - 1]  if isinstance(_result, list) else _result 
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

