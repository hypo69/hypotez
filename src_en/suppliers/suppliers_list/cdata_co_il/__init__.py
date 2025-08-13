## \file /src/suppliers/suppliers_list/cdata_co_il/__init__.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
.. module:: src.suppliers.suppliers_list.cdata_co_il
    :platform: Windows, Unix
    :synopsis: Initialization file for Cdata (Israel) supplier-specific functionalities.

Cdata (Israel) Supplier Initialization
=========================================================================================

This module serves as the initialization file for the Cdata (Israel) supplier package.
It defines the package structure and imports key components like the Graber and categories crawler.

Example usage
-------------

```python
    # No direct example usage for __init__.py, as it defines the package.
    # Components within this package would be imported and used as follows:
    # from src.suppliers.suppliers_list.cdata_co_il.graber import Graber
    # from src.suppliers.suppliers_list.cdata_co_il.categories_crawler import get_list_products_in_category
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: suppliers/suppliers_list/cdata_co_il/__init__.py
"""

from .graber import Graber
from .categories_crawler import  get_list_products_in_category