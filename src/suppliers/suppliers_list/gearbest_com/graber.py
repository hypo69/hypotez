## \file /src/suppliers/suppliers_list/gearbest_com/graber.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
.. module:: src.suppliers.suppliers_list.gearbest_com.graber
    :platform: Windows, Unix
    :synopsis: Module for collecting product data from Gearbest.

Gearbest Product Data Graber
=========================================================================================

This module provides a `Graber` class designed to extract product information from Gearbest.
It extends a base `Graber` class and includes functionality to handle pop-up windows during scraping.
It allows for custom handling of product fields by overriding methods.

Example usage
-------------

```python
    from src.webdriver.selenium.driver import Driver
    from src.suppliers.suppliers_list.gearbest_com.graber import Graber

    # Initialize a WebDriver instance (e.g., Chrome)
    driver_instance = Driver(browser_name="Chrome")

    # Initialize the Gearbest Graber
    gearbest_graber = Graber(driver=driver_instance, lang_index=0) # Assuming lang_index is needed

    # Now you can use gearbest_graber methods to interact with Gearbest
    # For example, to grab product details from a URL:
    # product_data = gearbest_graber.grab_product_details("https://www.gearbest.com/item/...")
    # print(product_data)

    # Don't forget to quit the driver when done
    # driver_instance.quit()
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: suppliers/suppliers_list/gearbest_com/graber.py
"""
from typing import Optional, Any
from types import SimpleNamespace
import header
from src.suppliers.graber import Graber as Grbr, Config, close_pop_up
from src.webdriver.selenium.driver import Driver
from src.logger.logger import logger


#
#
#           DECORATOR TEMPLATE. 
#
# def close_pop_up(value: Any = None) -> Callable:
#     """Creates a decorator to close pop-up windows before executing the main function logic.

#     Args:
#         value (Any): Additional value for the decorator.

#     Returns:
#         Callable: The decorator wrapping the function.
#     """
#     def decorator(func: Callable) -> Callable:
#         @wraps(func)
#         async def wrapper(*args, **kwargs):
#             try:
#                 # await Context.driver.execute_locator(Context.locator.close_pop_up)  # Await async pop-up close  
#                 ... 
#             except ExecuteLocatorException as e:
#                 logger.debug(f'Error executing locator: {e}')
#             return await func(*args, **kwargs)  # Await the main function
#         return wrapper
#     return decorator

class Graber(Grbr):
    """Class for Gearbest grabbing operations."""
    supplier_prefix: str

    def __init__(self, driver: Optional['Driver'] = None, lang_index:Optional[int] = None):
        """Initializes the product field collection class.

        Args:
            driver (Driver, optional): The webdriver instance for browser interaction. Defaults to None.
            lang_index (int, optional): The language index. Defaults to None.
        """
        self.supplier_prefix = 'gearbest'
        super().__init__(supplier_prefix=self.supplier_prefix, driver=driver, lang_index=lang_index)
        # Set global settings via Context
        
        Config.locator_for_decorator = None # <- if a value is set, it will be executed in the `@close_pop_up` decorator