## \file /src/suppliers/suppliers_list/aliexpress_com/api/helpers/products.py
# -*- coding: utf-8 -*-
 # <- venv win
"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.api.helpers.products
    :platform: Windows, Unix
    :synopsis: Helper functions for parsing AliExpress API product data.

This module provides utility functions for parsing product data received from the AliExpress API,
specifically handling image URLs and other product attributes.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com.api.helpers.products import parse_product
    from types import SimpleNamespace

    # Example product data (replace with actual data from API)
    # product_data = SimpleNamespace(
    #     product_small_image_urls=SimpleNamespace(string="url1,url2"),
    #     # ... other product attributes
    # )
    # parsed_product = parse_product(product_data)
    # print(parsed_product.product_small_image_urls)
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/api/helpers/products.py
"""
def parse_product(product):
    product.product_small_image_urls = product.product_small_image_urls.string
    return product


def parse_products(products):
    new_products = []

    for product in products:
        new_products.append(parse_product(product))

    return new_products
