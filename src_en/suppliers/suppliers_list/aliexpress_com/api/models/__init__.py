## \file /src/suppliers/suppliers_list/aliexpress_com/api/models/__init__.py
# -*- coding: utf-8 -*-
 # <- venv win
"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.api.models
    :platform: Windows, Unix
    :synopsis: Initialization module for AliExpress API models.

This module serves as the initialization file for the AliExpress API models package.
It imports various data models used for representing AliExpress entities such as
languages, currencies, products, categories, and affiliate links.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com.api.models import Product

    # Example of using a model
    # product = Product(product_id="123", product_title="Example Product")
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/api/models/__init__.py
"""
from .languages import Language
from .currencies import Currency
from .request_parameters import ProductType, SortBy, LinkType
from .affiliate_link import AffiliateLink
from .hotproducts import HotProductsResponse
from .product import Product
from .category import Category, ChildCategory
