# # \file /src/suppliers/hb/_experiments/ide_experiments_grabber.py
# -*- coding: utf-8 -*-

# ! .pyenv/bin/python3

""".. module:: src.suppliers.hb._experiments 
	:platform: Windows, Unix
	:synopsis:"""


""":platform: Windows, Unix
	:synopsis:"""

""":platform: Windows, Unix
	:synopsis:"""

""":platform: Windows, Unix"""
""":platform: Windows, Unix
  :platform: Windows, Unix
  :synopsis:"""
  
"""module: src.suppliers.hb._experiments"""


"""Checking the performance of the HB scenarios.
Checks:
- Get the completed dictionary Product_fields
- Send it to the server"""



# from math import prod
import os, sys
from pathlib import Path
from typing import List, Union, Dict
from selenium.webdriver.remote.webelement import WebElement

# ############## / adding a root directory allows me to dance from the stove ############### cur###
dir_root: Path = Path(os.getcwd()[:os.getcwd().rfind('hypotez') + 7])
sys.path.append(str(dir_root))  # Adding the root folder to sys.path
dir_src = Path(dir_root, 'src')
sys.path.append(str(dir_root))
from src.webdriver import executor
"""Adding a root directory allows me to dance from the stove."""
# None


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