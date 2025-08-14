# # \file /src/suppliers/kualastyle/graber.py
# -*- coding: utf-8 -*-

# ! .pyenv/bin/python3

""".. Module :: src.suppliers.kualastyle 
	: Platform: Windows, Unix
	: synopsis: Class collects the value of the fields on the product page `kualastyle.co.il`. 
    For each field of the product page, the field processing function in the parental class is made.
    If non -standard processing is needed, the function is overloaded in this class.
    -----------------
    Before sending a request to the webdraper, you can take preliminary actions through the decorator. 
    The default decorator is in the parent class. In order for the decorator to work, you need to transmit the value 
    in `context.locator`, if you need to realize your decorator, replace the lines with the decorator and reduce its behavior"""


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

    def __init__(self, driver: Driver, lang_index:int):
        """Initialization of the class of collecting fields of goods."""
        self.supplier_prefix = 'kualastyle'
        super().__init__(supplier_prefix=self.supplier_prefix, driver=driver, lang_index=lang_index)
        # Installation Global Settings via CONTEXT
        
        Config.locator_for_decorator = None # < - If the value is used, then it will be completed in the decorator `@close_pop_up`

        
 