## \file /src/suppliers/ads_tec_iit_com/__init__.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
.. module:: src.suppliers.ads_tec_iit_com
    :platform: Windows, Unix
    :synopsis: Initialization module for the Ads-Tec IIT supplier.

This module serves as the initialization file for the Ads-Tec IIT supplier package.
It imports the `Graber` class and the `get_list_products_in_category` function,
making them accessible when the package is imported.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.ads_tec_iit_com import Graber, get_list_products_in_category

    # Example of using the imported classes/functions
    # graber_instance = Graber(...)
    # product_list = get_list_products_in_category(...)
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/ads_tec_iit_com/__init__.py
"""

from .graber import Graber
from .categories_crawler import  get_list_products_in_category
