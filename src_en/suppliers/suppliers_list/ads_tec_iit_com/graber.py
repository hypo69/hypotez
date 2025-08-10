## \file /src/suppliers/suppliers_list/ads_tec_iit_com/graber.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.ads_tec_iit_com.graber
    :platform: Windows, Unix
    :synopsis: The class collects field values on the product page of `ads-tec-iit.com`.

The class collects field values on the product page of `ads-tec-iit.com`.
For each product page field, a field processing function is implemented in the parent class.
If non-standard processing is required, the function is overloaded in this class.
------------------
Before sending a request to the webdriver, preliminary actions can be performed via a decorator.
The decorator is located in the parent class by default. For the decorator to work, a value must be passed
to `Context.locator`. If you need to implement your own decorator, uncomment the lines with the decorator and override its behavior.


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
#     """Creates a decorator for closing pop-up windows before executing the main function logic.

#     Args:
#         value (Any): Additional value for the decorator.

#     Returns:
#         Callable: Decorator wrapping the function.
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
    """Class for Morlevi capture operations."""
    supplier_prefix: str

    def __init__(self, driver: Optional['Driver'] = None, lang_index:Optional[int] = None):
        """Initializes the product field collection class."""
        self.supplier_prefix = 'ads-tec-iit.com'
        super().__init__(supplier_prefix=self.supplier_prefix, driver=driver, lang_index=lang_index)
        # Set global settings via Context

        Config.locator_for_decorator = None # <- if a value is set, it will be executed in the `@close_pop_up` decorator
