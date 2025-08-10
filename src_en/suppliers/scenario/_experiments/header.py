## \file /src/suppliers/scenario/_experiments/header.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.scenario._experiments
    :platform: Windows, Unix
    :synopsis: Header for scenario experiments.

This module provides a common header for various scenario experiments, including
path configurations and imports for necessary modules.

Example usage
-------------

```python
    from src.suppliers.scenario._experiments.header import start_supplier

    # Example of starting a supplier
    # supplier_instance = start_supplier("my_supplier")
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/scenario/_experiments/header.py
"""


import sys
import os
path = os.getcwd()[:os.getcwd().rfind(r'hypotez')+7]
sys.path.append(path)  # Add root folder to sys.path
# ----------------


from pathlib import Path
import json
import re
# ----------------
#from hypotez import gs, Supplier, Product
from src import gs

from src.endpoints.prestashop.product import PrestaProduct
from src.endpoints.prestashop.category import PrestaCategory
from src.logger.logger import logger,log_decorator, pprint


def start_supplier(supplier_prefix):
    params: dict = \
    {
        'supplier_prefix': supplier_prefix
    }

    return Supplier(**params)

