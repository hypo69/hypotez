## \file /src/suppliers/suppliers_list/generex_de/__init__.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
.. module:: src.suppliers.suppliers_list.generex_de
    :platform: Windows, Unix
    :synopsis: Initialization file for Generex (Germany) supplier-specific functionalities.

Generex (Germany) Supplier Initialization
=========================================================================================

This module serves as the initialization file for the Generex (Germany) supplier package.
It defines the package structure and imports key components like the Graber and categories crawler.

Example usage
-------------

```python
    # No direct example usage for __init__.py, as it defines the package.
    # Components within this package would be imported and used as follows:
    # from src.suppliers.suppliers_list.generex_de.graber import Graber
    # from src.suppliers.suppliers_list.generex_de.categories_crawler import get_list_products_in_category
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: suppliers/suppliers_list/generex_de/__init__.py
"""

from .graber import Graber
from .categories_crawler import  get_list_products_in_category
