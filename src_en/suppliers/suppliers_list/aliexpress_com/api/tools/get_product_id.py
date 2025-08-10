## \file /src/suppliers/suppliers_list/aliexpress_com/api/tools/get_product_id.py
# -*- coding: utf-8 -*-

"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.api.tools.get_product_id
    :platform: Windows, Unix
    :synopsis: Tool for extracting product IDs from AliExpress URLs or strings.

This module provides a function to extract the product ID from a given string,
which can be a direct product ID or a URL containing the product ID.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com.api.tools import get_product_id

    # Example of extracting product ID from a URL
    # product_id = get_product_id("https://www.aliexpress.com/item/12345.html")
    # print(product_id) # Output: 12345

    # Example of extracting product ID from a string
    # product_id = get_product_id("98765")
    # print(product_id) # Output: 98765
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/api/tools/get_product_id.py
"""
"""Some useful tools."""

from ..errors import ProductIdNotFoundException
from src.suppliers.suppliers_list.aliexpress_com.utils.extract_product_id import extract_prod_ids
import re


def get_product_id(raw_product_id: str) -> str:
    """Returns the product ID from a given text. Raises ProductIdNotFoundException on fail."""
    return extract_prod_ids(raw_product_id)
    # if re.search(r'^[0-9]*$', text):
    #     return text

    # # Extract product ID from URL
    # asin = re.search(r'(\/)([0-9]*)(\.)', text)
    # if asin:
    #     return asin.group(2)
    # else:
    #     raise ProductIdNotFoundException('Product id not found: ' + text)
