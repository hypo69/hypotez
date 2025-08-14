# # \file /src/suppliers/grandadvance/graber.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3

"""Module for collecting goods about Grandadvance.
======================================================================================ward

The module contains the class: class: `Graber`, which is used to collect goods
from the website `Bangood.com`. It is inherited from the base class: class: `src.suppliers.graber.graber`.

The `Graber Class provides methods for processing various fields of goods on the page.
If it is necessary to non -standard processing of the field, the method may be redefined.

For each field of the product page, the field processing function in the parental `Graber` is made.
If non -standard processing is needed, you can overload the method here in this class.
-----------------
Before sending a request to the webdraper, you can take preliminary actions through the decorator. 
The default decorator is in the parent class. In order for the decorator to work, you need to transmit the value 
In `CONTEXT.LOCATOR`, if you need to realize your decorator, replace the lines with the decorator and reduce its behavior.
You can also realize your own decorator by dividing the corresponding lines of the code

`` `RST
.. Module :: src.suppliers.suppliers_list.grandadvance
`` `"""

from typing import Optional, Any
from types import SimpleNamespace
import header
from header import __root__
from src import gs
from src.suppliers.graber import GraberBase, Config, close_pop_up
from src.utils.jjson import j_loads_ns
from src.webdriver.selenium.driver import Driver
from types import SimpleNamespace
from src.logger.logger import logger


ENDPOINT = 'grandadvance'

# None

class Graber(GraberBase):
    """The class will be inhabited by Graber."""

    def __init__(self, driver: Driver, lang_index:int):
        config:SimpleNamespace = j_loads_ns(gs.path.src / 'suppliers' / ENDPOINT / f'{ENDPOINT}.json')
        locator: SimpleNamespace = j_loads_ns(gs.path.src / 'suppliers' / ENDPOINT / 'locators' / 'product.json')
        super().__init__(supplier_prefix=ENDPOINT, driver=driver, lang_index=lang_index)
        Config.locator_for_decorator = self.product_locator.click_to_specifications # <- if locator not definded decorator

