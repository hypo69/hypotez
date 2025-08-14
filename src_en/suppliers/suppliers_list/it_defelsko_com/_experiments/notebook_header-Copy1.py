# # \file /src/suppliers/hb/_experiments/notebook_header-Copy1.py
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


import sys
import os
from pathlib import Path

# None
dir_root : Path = Path (os.getcwd()[:os.getcwd().rfind('hypotez')+7])
sys.path.append (str (dir_root) )  # Add the root folder to sys.path
dir_src = Path (dir_root, 'src')
sys.path.append (str (dir_root) ) 
# None

from pathlib import Path
import json
import re



from src import gs
from src.webdriver.selenium.driver import Driver, executor

from src.product import Product, ProductFields
from src.category import Category
from src.utils import StringFormatter, StringNormalizer
from src.utils.printer import  pprint
, save_text_file
from src.scenario import run_scenarios
# None

def start_supplier(supplier_prefix, locale):
    """The start of the supplier"""
    if not supplier_prefix and not locale: return "Не задан сценарий и язык"
    
    params: dict = \
    {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }
    
    return Supplier(**params))