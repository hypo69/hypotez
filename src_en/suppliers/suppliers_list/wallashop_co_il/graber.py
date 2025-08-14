# # \file /src/suppliers/wallashop/graber.py
# -*- coding: utf-8 -*-

# ! .pyenv/bin/python3

""".. Module :: src.suppliers.wallashop 
	: Platform: Windows, Unix
	: synopsis: Class collects the value of the fields on the product page `Wallashop.co.il`. 
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



class Graber(GraberBase):
    """Class for capture operations Wallashop."""
    supplier_prefix: str

    def __init__(self, driver: Driver, lang_index:int):
        """Initialization of the class of collecting fields of goods."""
        self.supplier_prefix = 'wallashop'
        super().__init__(supplier_prefix=self.supplier_prefix, driver=driver, lang_index=lang_index)

        # Closer POP AP@close_pop_up`
        Config.locator_for_decorator = None # < - If the value is used, then it will be completed in the decorator `@close_pop_up`

        
