## \file /src/suppliers/suppliers_list/aliexpress_com/api/helpers/__init__.py
# -*- coding: utf-8 -*-
 # <- venv win
"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.api.helpers
    :platform: Windows, Unix
    :synopsis: Initialization module for AliExpress API helpers.

This module serves as the initialization file for the AliExpress API helpers package.
It imports various utility functions for handling API requests, arguments, products, and categories.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com.api.helpers import api_request, get_product_ids

    # Example of using imported functions
    # response = api_request(some_request, "some_response_key")
    # product_ids = get_product_ids(["url1", "url2"])
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/api/helpers/__init__.py
"""
from .requests import api_request
from .arguments import get_list_as_string, get_product_ids
from .products import parse_products
from .categories import filter_parent_categories, filter_child_categories
