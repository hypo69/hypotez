## \file /src/suppliers/suppliers_list/ebay_com/_experiments/JUPYTER_header.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
.. module:: src.suppliers.suppliers_list.ebay_com._experiments.JUPYTER_header
    :platform: Windows, Unix
    :synopsis: Header for Jupyter notebooks related to eBay supplier experiments.

eBay Jupyter Header
=========================================================================================

This module provides a standardized header for Jupyter notebooks used in experiments
related to the eBay supplier. It sets up the project root and imports common utilities.

Example usage
-------------

```python
    # This module is typically imported at the beginning of a Jupyter notebook
    # to set up the environment for eBay supplier experiments.
    # import src.suppliers.suppliers_list.ebay_com._experiments.JUPYTER_header
    # from src.suppliers.suppliers_list.ebay_com._experiments.JUPYTER_header import start_supplier

    # supplier = start_supplier(supplier_prefix='ebay', locale='en')
    # print(f"Supplier started: {supplier.supplier_prefix}")
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: suppliers/suppliers_list/ebay_com/_experiments/JUPYTER_header.py
"""

import sys
import os
from pathlib import Path

# ----------------
dir_root : Path = Path (os.getcwd()[:os.getcwd().rfind('hypotez')+7])
sys.path.append (str (dir_root) )  # Add root folder to sys.path
dir_src = Path (dir_root, 'src')
sys.path.append (str (dir_root) ) 
# ----------------

from pathlib import Path
import json
import re


#from settings import gs
from src.webdriver.selenium.driver import Driver

from src.product import Product, ProductFields
from src.category import Category
from src.utils import StringFormatter, StringNormalizer
from src.utils.printer import  pprint
from src.endpoints.PrestaShop import Product as PrestaProduct
, save_text_file
# ----------------

def start_supplier(supplier_prefix: str = 'aliexpress', locale: str = 'en' ):
    """ Start the supplier.

    Args:
        supplier_prefix (str, optional): The prefix of the supplier. Defaults to 'aliexpress'.
        locale (str, optional): The locale for the supplier. Defaults to 'en'.

    Returns:
        Supplier: An instance of the Supplier class.
    """
    params: dict = \
    {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }
    
    return Supplier(**params))