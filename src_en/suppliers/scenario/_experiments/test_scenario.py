## \file /src/suppliers/scenario/_experiments/test_scenario.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.scenario._experiments
    :platform: Windows, Unix
    :synopsis: Test scenario for suppliers.

This module contains a test scenario for running supplier-specific operations.

Example usage
-------------

```python
    import asyncio
    from src.suppliers.scenario._experiments.test_scenario import scenario

    async def main():
        # Assuming 'scenario' is properly initialized
        # await scenario.run_scenarios()
        pass

    if __name__ == "__main__":
        asyncio.run(main())
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/scenario/_experiments/test_scenario.py
"""


import sys
import os
path = os.getcwd()[:os.getcwd().rfind(r'hypotez')]
sys.path.append(path)  # Add root folder to sys.path
# ----------------
from pathlib import Path
import json
import re
# ----------------
from hypotez import gs
from src.utils.printer import  pprint

from src.suppliers.scenario import Scenario


def start_supplier(supplier_prefix):
    params: dict = \
    {
        'supplier_prefix': supplier_prefix
    }

    return Supplier(**params)


supplier_prefix = 'aliexpress'
#supplier_prefix = 'amazon'
#supplier_prefix = 'kualastyle'
#supplier_prefix = 'ebay'

s = start_supplier(supplier_prefix)
""" s - throughout the code means the `Supplier` class """

print(" Can continue ")

scenario = Scenario(s)

scenario.run_scenarios()
