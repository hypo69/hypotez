## \file /src/suppliers/suppliers_list/de_de_ring_com/_experiments/ide_experiments_grabber.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
.. module:: src.suppliers.suppliers_list.de_de_ring_com._experiments.ide_experiments_grabber
    :platform: Windows, Unix
    :synopsis: Experiment file for testing grabber scenarios for De-De-Ring.

De-De-Ring Grabber Experiment File
=========================================================================================

This module contains experimental code for testing the execution of grabber scenarios
for the De-De-Ring supplier. It includes checks for populating product fields and sending data to the server.

Example usage
-------------

```python
    # This module is intended for direct execution during development and testing.
    # It initializes a supplier, product, and driver, then runs a scenario.
    # Example of running the script:
    # python src/suppliers/suppliers_list/de_de_ring_com/_experiments/ide_experiments_grabber.py
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: suppliers/suppliers_list/de_de_ring_com/_experiments/ide_experiments_grabber.py
"""


"""  Checks for scenario execution for HB.
Checks:
- get populated product_fields dictionary
- send it to the server
"""



#from math import prod
import os, sys
from pathlib import Path
from typing import List, Union, Dict
from selenium.webdriver.remote.webelement import WebElement

################# Adding the root directory allows me to start from the base ###################
dir_root: Path = Path(os.getcwd()[:os.getcwd().rfind('hypotez') + 7])
sys.path.append(str(dir_root))  # Adding the root folder to sys.path
dir_src = Path(dir_root, 'src')
sys.path.append(str(dir_root))
from src.webdriver import executor
"""  Adding the root directory allows me to start from the base. """
####################################################################################################


from src import gs

from src.product import Product, ProductFields
from src.scenario import run_scenarios

from src.logger.logger import logger, ExecuteLocatorException
from src.webdriver.selenium.driver import Driver
from src.utils import StringFormatter, StringNormalizer




s: Supplier = Supplier(supplier_prefix = 'hb')
p: Product = Product(s)
l: Dict = s.locators["product"]
d: Driver = s.driver
f: ProductFields = ProductFields(s)

s.current_scenario: Dict =  {
      "url": "https://hbdeadsea.co.il/product-category/bodyspa/feet-hand-treatment/",
      "name": "טיפוח כפות ידיים ורגליים",
      "condition": "new",
      "presta_categories": {
        "default_category": 11259,
        "additional_categories": []
      }
    }

d.get_url(s.current_scenario['url'])
ret = run_scenarios(s, s.current_scenario)
s.related_modules.grab_product_page(s))