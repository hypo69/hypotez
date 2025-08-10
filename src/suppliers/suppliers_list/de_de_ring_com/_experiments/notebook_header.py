## \file /src/suppliers/suppliers_list/de_de_ring_com/_experiments/notebook_header.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
.. module:: src.suppliers.suppliers_list.de_de_ring_com._experiments.notebook_header
    :platform: Windows, Unix
    :synopsis: Header for Jupyter notebooks related to De-De-Ring supplier experiments.

De-De-Ring Notebook Header
=========================================================================================

This module provides a standardized header for Jupyter notebooks used in experiments
related to the De-De-Ring supplier. It sets up the project root and imports common utilities.

Example usage
-------------

```python
    # This module is typically imported at the beginning of a Jupyter notebook
    # to set up the environment for De-De-Ring supplier experiments.
    # import src.suppliers.suppliers_list.de_de_ring_com._experiments.notebook_header
    # from src.suppliers.suppliers_list.de_de_ring_com._experiments.notebook_header import start_supplier

    # supplier = start_supplier(supplier_prefix='de_de_ring', locale='de')
    # print(f"Supplier started: {supplier.supplier_prefix}")
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: suppliers/suppliers_list/de_de_ring_com/_experiments/notebook_header.py
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



from src import gs
from src.webdriver.selenium.driver import Driver, executor

from src.product import Product, ProductFields
from src.category import Category
from src.utils import StringFormatter, StringNormalizer
from src.utils.printer import  pprint
, save_text_file
from src.scenario import run_scenarios
# ----------------

def start_supplier(supplier_prefix, locale):
    """ Start the supplier.

    Args:
        supplier_prefix (str): The prefix of the supplier.
        locale (str): The locale for the supplier.

    Returns:
        Supplier: An instance of the Supplier class.
    """
    if not supplier_prefix and not locale: return "Scenario and language not set"
    
    params: dict = \
    {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }
    
    return Supplier(**params)