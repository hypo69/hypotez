# # \file /src/suppliers/suppliers_list/apple_com/graber.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3
""".. module:: src.suppliers.suppliers_list.apple_com.graber
    :platform: Windows, Unix
    :synopsis: Module for collecting product data from Apple.

Apple Product Data Graber
=========================================================================================

This module provides a `Graber` class designed to extract product information from Apple.
It extends a base `Graber` class and includes functionality to handle pop-up windows during scraping.
It allows for custom handling of product fields by overriding methods.

Example usage
-------------

```python
    from src.webdriver.selenium.driver import Driver
    from src.suppliers.suppliers_list.apple_com.graber import Graber

    # Initialize a WebDriver instance (e.g., Chrome)
    driver_instance = Driver(browser_name="Chrome")

    # Initialize the Apple Graber
    apple_graber = Graber(driver=driver_instance, lang_index=0) # Assuming lang_index is needed

    # Now you can use apple_graber methods to interact with Apple
    # For example, to grab product details from a URL:
    # product_data = apple_graber.grab_product_details("https://www.apple.com/shop/product/...")
    # print(product_data)

    # Don't forget to quit the driver when done
    # driver_instance.quit()
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: suppliers/suppliers_list/apple_com/graber.py"""
from typing import Optional, Any
from types import SimpleNamespace
import header
from src.suppliers.graber import GraberBase, Config, close_pop_up
from src.webdriver.selenium.driver import Driver
from src.logger.logger import logger


# None
# DECORATOR TEMPLATE.
# # def close_pop_up(value: Any = None) -> Callable:
# """Creates a decorator to close pop-up windows before executing the main function logic.

# Args:
# value (Any): Additional value for the decorator.

# Returns:
# Callable: The decorator wrapping the function.
# None
# def decorator(func: Callable) -> Callable:
# @wraps(func)
# async def wrapper(*args, **kwargs):
# try:
# # await Context.driver.execute_locator(Context.locator.close_pop_up)  # Await async pop-up close
# None
# except ExecuteLocatorException as e:
# logger.debug(f'Error executing locator: {e}')
# return await func(*args, **kwargs)  # Await the main function
# return wrapper
# return decorator


class Graber(GraberBase):
    """Class for Apple grabbing operations."""
    supplier_prefix: str

    def __init__(self, driver: Optional['Driver'] = None, lang_index:Optional[int] = None):
        """Initializes the product field collection class.

        Args:
            driver (Driver, optional): The webdriver instance for browser interaction. Defaults to None.
            lang_index (int, optional): The language index. Defaults to None."""
        self.supplier_prefix = 'apple'
        super().__init__(supplier_prefix=self.supplier_prefix, driver=driver, lang_index=lang_index)
        # Set global settings via Context
        
        Config.locator_for_decorator = None # <- if a value is set, it will be executed in the `@close_pop_up` decorator

    # async def description_short(self, value:Optional[Any] = None) -> bool:
    # """Fetch and set short description.
        
    # Args:
    # value (Any): This value can be passed in the kwargs dictionary via the key {description_short = `value`} when defining the class.
    # If `value` is passed, its value is substituted into the `ProductFields.description_short` field.
    # None
    # try:
    # # Get value via execute_locator
    # #path = self.driver.current_url + '/#tab-description'
    # #await self.driver.get_url(path)
    # raw_data = await self.driver.execute_locator(self.product_locator.description_short)

    # self.fields.description_short = value or normalize_string(raw_data) or ''
    # None
    # return
    # except Exception as ex:
    # Logger.error (f "Error obtaining a value in the field` description_short` ", ex)
    # None
    # return

    # self.fields.description_short = value
    # return True

    async def default_image_url(self, value:Optional[Any] = None) -> bool:
        return True

    async def price(self, value:Optional[Any] = None) -> bool:
        """Placeholder for price."""
        self.fields.price = 150.00
        return True


        

from typing import Optional, Any
from types import SimpleNamespace
import header
from src.suppliers.graber import GraberBase, Config, close_pop_up
from src.webdriver.selenium.driver import Driver
from src.logger.logger import logger


# None
# DECORATOR TEMPLATE.
# # def close_pop_up(value: Any = None) -> Callable:
# """Creates a decorator to close pop -ups before performing the main logic of the function.

# Args:
# Value (Any): additional value for the decorator.

# Returns:
# Callable: a decorator wrapping a function.
# None
# def decorator(func: Callable) -> Callable:
# @wraps(func)
# async def wrapper(*args, **kwargs):
# try:
# # await Context.driver.execute_locator(Context.locator.close_pop_up)  # Await async pop-up close
# None
# except ExecuteLocatorException as e:
# Logger.debug (f'hoshka of the locator: {e} ')
# return await func(*args, **kwargs)  # Await the main function
# return wrapper
# return decorator


class Graber(GraberBase):
    """Class for capture operations Morlevi."""
    supplier_prefix: str

    def __init__(self, driver: Optional['Driver'] = None, lang_index:Optional[int] = None):
        """Initialization of the class of collecting fields of goods."""
        self.supplier_prefix = 'hb'
        super().__init__(supplier_prefix=self.supplier_prefix, driver=driver, lang_index=lang_index)
        # Installation Global Settings via CONTEXT
        
        Config.locator_for_decorator = None # < - If the value is used, then it will be completed in the decorator `@close_pop_up`

    # async def description_short(self, value:Optional[Any] = None) -> bool:
    # """Fetch and Set Short Description.
        
    # Args:
    # Value (Any): This value can be transmitted in the Kwargs dictionary through the key {description_short = `value`} when determining the class.
    # If `Value` was transmitted, its value is substituted in the field` Productfields.Description_Short`.
    # None
    # try:
    # # We get a value through execute_locator
    # #path = self.driver.current_url + '/#tab-description'
    # #await self.driver.get_url(path)
    # raw_data = await self.driver.execute_locator(self.product_locator.description_short)

    # self.fields.description_short = value or normalize_string(raw_data) or ''
    # None
    # return
    # except Exception as ex:
    # Logger.error (f "Error obtaining a value in the field` description_short` ", ex)
    # None
    # return

    # self.fields.description_short = value
    # return True

    async def default_image_url(self, value:Optional[Any] = None) -> bool:
        return True

    async def price(self, value:Optional[Any] = None) -> bool:
        """The plug is for the price"""
        self.fields.price = 150.00
        return True


        
