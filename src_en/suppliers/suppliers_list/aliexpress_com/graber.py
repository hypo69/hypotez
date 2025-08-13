# # \file /src/suppliers/suppliers_list/aliexpress_com/graber.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3
""".. module:: src.suppliers.suppliers_list.aliexpress_com.graber
    :platform: Windows, Unix
    :synopsis: Module for collecting product data from Aliexpress.

Module for collecting product data from Aliexpress
=========================================================================================

This module provides a `Graber` class designed to extract product information from Aliexpress.
It extends a base `Graber` class and includes functionality to handle pop-up windows during scraping.

Example usage
-------------

```python
    from src.webdriver.selenium.driver import Driver
    from src.suppliers.suppliers_list.aliexpress_com.graber import Graber

    # Initialize a WebDriver instance (e.g., Chrome)
    driver_instance = Driver(browser_name="Chrome")

    # Initialize the Aliexpress Graber
    aliexpress_graber = Graber(driver=driver_instance, lang_index=0)

    # Now you can use aliexpress_graber methods to interact with Aliexpress
    # For example, to grab product details from a URL:
    # product_data = aliexpress_graber.grab_product_details("https://www.aliexpress.com/item/...")
    # print(product_data)

    # Don't forget to quit the driver when done
    # driver_instance.quit()
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: suppliers/suppliers_list/aliexpress_com/graber.py"""
from typing import Optional, Any
from types import SimpleNamespace
from typing import Any, Callable
from functools import wraps
# from src.utils.jjson import j_loads, j_loads_ns
from src.suppliers.graber import GraberBase, Config, close_pop_up
from src.webdriver.selenium.driver import Driver
from src.logger.logger import logger
from src.logger.exceptions import ExecuteLocatorException

# None
# DECORATOR TEMPLATE.
# # def close_pop_up(value: Any = None) -> Callable:
# """# Creates a decorator to close pop -ups before performing the main logic of the function.
    
# : Param Value: additional value for the decorator.
# : Type Value: Any
# : Return: a decorator wrapping a function.
# : Rtype: Callable
    
# None
# def decorator(func: Callable) -> Callable:
# @wraps(func)
# async def wrapper(*args, **kwargs):
# try:
# # checks the presence of a locator for closing a pop -up window
# if Config.locator_for_decorator and Config.locator_for_decorator.close_pop_up:
# # executes the closing locator of a pop -up window
# await Context.driver.execute_locator(Config.locator_for_decorator.close_pop_up)
# None
# except ExecuteLocatorException as ex:
# # logs the error of the locator
# Logger.debug (F'Oshitka of the locator: ', ex)
# # expects the main function
# return await func(*args, **kwargs)
# return wrapper
# return decorator


class Graber(GraberBase):
    """Class for collecting goods about goods with AliExpress."""
    supplier_prefix: str

    def __init__(self, driver: Driver, lang_index:int):
        """Initialization of the class of collecting fields of goods.

        : Param Driver: A copy of the web drive for interacting with the browser.
        : Type Driver: Driver"""
        self.supplier_prefix = 'aliexpress_com.com'
        # Call of the parent class designer
        super().__init__(supplier_prefix=self.supplier_prefix, driver=driver, lang_index=lang_index)

        # sets the locator value for the decorator in `none`
        # If the value is set, then it will be completed in the decorator `@close_pop_up`
        Config.locator_for_decorator = None
