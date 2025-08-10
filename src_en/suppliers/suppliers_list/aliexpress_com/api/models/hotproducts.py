## \file /src/suppliers/suppliers_list/aliexpress_com/api/models/hotproducts.py
# -*- coding: utf-8 -*-
 # <- venv win
"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.api.models.hotproducts
    :platform: Windows, Unix
    :synopsis: Data model for AliExpress hot products response.

This module defines the `HotProductsResponse` class, which represents the structure
of the response when querying for hot products from the AliExpress API.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com.api.models import HotProductsResponse

    # Example of creating a HotProductsResponse object
    # response = HotProductsResponse()
    # response.current_page_no = 1
    # response.current_record_count = 10
    # response.total_record_count = 100
    # response.products = [] # List of Product objects
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/api/models/hotproducts.py
"""
from .product import Product
from typing import List


class HotProductsResponse:
    current_page_no: int
    current_record_count: int
    total_record_count: int
    products: List[Product]
