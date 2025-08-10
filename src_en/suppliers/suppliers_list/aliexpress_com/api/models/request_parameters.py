## \file /src/suppliers/suppliers_list/aliexpress_com/api/models/request_parameters.py
# -*- coding: utf-8 -*-
 # <- venv win
"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.api.models.request_parameters
    :platform: Windows, Unix
    :synopsis: Data models for AliExpress API request parameters.

This module defines various classes representing parameters used in AliExpress API requests,
such as product types, sorting options, and link types.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com.api.models import ProductType, SortBy, LinkType

    # Example of using ProductType
    # product_type = ProductType.ALL

    # Example of using SortBy
    # sort_option = SortBy.SALE_PRICE_ASC

    # Example of using LinkType
    # link_type = LinkType.NORMAL
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/api/models/request_parameters.py
"""
class ProductType:
    ALL = 'ALL'
    PLAZA = 'PLAZA'
    TMALL = 'TMALL'

class SortBy:
    SALE_PRICE_ASC = 'SALE_PRICE_ASC'
    SALE_PRICE_DESC = 'SALE_PRICE_DESC'
    LAST_VOLUME_ASC = 'LAST_VOLUME_ASC'
    LAST_VOLUME_DESC = 'LAST_VOLUME_DESC'

class LinkType:
    NORMAL = 0
    HOTLINK = 2
