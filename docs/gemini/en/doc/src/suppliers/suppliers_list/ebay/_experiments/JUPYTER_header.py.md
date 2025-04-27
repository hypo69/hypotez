# JUPYTER_header Module

## Overview

This module contains the `start_supplier` function which is used to start a supplier.

## Details

This file is responsible for initializing and starting a supplier based on provided parameters. It imports necessary libraries for handling various aspects of the supplier, including product and category management, data processing, and web interaction.

## Functions

### `start_supplier`

**Purpose**: Initializes and starts a supplier with the specified prefix and locale.

**Parameters**:

- `supplier_prefix` (str): The prefix of the supplier. Defaults to 'aliexpress'.
- `locale` (str): The locale of the supplier. Defaults to 'en'.

**Returns**:

- `Supplier`: An instance of the `Supplier` class, initialized with the provided parameters.

**Raises Exceptions**:

- None

**How the Function Works**:

The function creates a dictionary containing the supplier prefix and locale, and then passes it to the `Supplier` class constructor to create a new instance of the supplier.

**Examples**:

```python
# Start an AliExpress supplier with English locale
aliexpress_supplier = start_supplier(supplier_prefix='aliexpress', locale='en')

# Start a generic supplier with English locale
generic_supplier = start_supplier(locale='en')
```

**Inner Functions**:

None


## Parameter Details

- `supplier_prefix` (str): Specifies the prefix of the supplier, which is used to identify the supplier within the system. For example, 'aliexpress', 'ebay', 'amazon'.
- `locale` (str): Represents the language and regional settings for the supplier.  This parameter is important for handling product descriptions, currency formats, and other locale-specific aspects of the supplier. 

## Examples

```python
# Example 1: Start an AliExpress supplier with English locale
aliexpress_supplier = start_supplier(supplier_prefix='aliexpress', locale='en')
print(aliexpress_supplier)  # Output: <Supplier: supplier_prefix='aliexpress', locale='en'>

# Example 2: Start a generic supplier with English locale
generic_supplier = start_supplier(locale='en')
print(generic_supplier)  # Output: <Supplier: supplier_prefix='aliexpress', locale='en'>

```

## Code Breakdown

```python
                ## \\file /src/suppliers/ebay/_experiments/JUPYTER_header.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.ebay._experiments 
	:platform: Windows, Unix
	:synopsis:

"""


"""
	:platform: Windows, Unix
	:synopsis:

"""


"""
	:platform: Windows, Unix
	:synopsis:

"""


"""
  :platform: Windows, Unix

"""
"""
  :platform: Windows, Unix
  :platform: Windows, Unix
  :synopsis:
"""
  
""" module: src.suppliers.ebay._experiments """


import sys
import os
from pathlib import Path

# ----------------
dir_root : Path = Path (os.getcwd()[:os.getcwd().rfind('hypotez')+7])
sys.path.append (str (dir_root) )  # Добавляю корневую папку в sys.path
dir_src = Path (dir_root, 'src')
sys.path.append (str (dir_root) ) 
# ----------------

from pathlib import Path
import json
import re


#from settings import gs
from src.webdriver.driver import Driver

from src.product import Product, ProductFields
from src.category import Category
from src.utils import StringFormatter, StringNormalizer
from src.utils.printer import  pprint
from src.endpoints.PrestaShop import Product as PrestaProduct
, save_text_file
# ----------------

def start_supplier(supplier_prefix: str = 'aliexpress', locale: str = 'en' ):
    """ Старт поставщика """
    params: dict = \
    {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }
    
    return Supplier(**params)