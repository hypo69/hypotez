# # \file /src/suppliers/morlevi/graber.py
# -*- coding: utf-8 -*-

# ! .pyenv/bin/python3



"""Module for working with morlevi.co.il
===========================================
The class collects the value of the fields on the product page `Morlevi.co.il`. 
    For each field of the product page, the field processing function in the parental class is made.
    If non -standard processing is needed, the function is overloaded in this class.
    -----------------
    Before sending a request to the webdraper, you can take preliminary actions through the decorator. 
    The default decorator is in the parent class. In order for the decorator to work, you need to transmit the value 
    in `context.locator`, if you need to realize your decorator, replace the lines with the decorator and reduce its behavior

`` `RST
.. Module :: src.suppliers.morlevi 
	: Platform: Windows, Unix
	: synopsis: 
`` `"""

from typing import Optional, TypeVar, Any
from types import SimpleNamespace

from header import __root__
from src.suppliers.graber import GraberBase, Config, close_pop_up

T = TypeVar('T')

# #                             DECORATOR TEMPLATE.


# def close_pop_up(value: Any = None) -> Callable:
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
    supplier_prefix: str  = 'morlevi.co.il'

    def __init__(self, driver: T, locator_for_decorator:Optional[SimpleNamespace] = None, lang_index:Optional[int] = None):
        """Initialization of the class of collecting fields of goods."""

        Config.locator_for_decorator = locator_for_decorator # < - If the value is set, then it will be completed in the decorator `@close_pop_up`
        super().__init__(supplier_prefix=self.supplier_prefix, driver=driver, lang_index=lang_index)

