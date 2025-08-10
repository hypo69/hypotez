## \file /src/suppliers/suppliers_list/aliexpress_com/utils/__init__.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.utils
    :platform: Windows, Unix
    :synopsis: Utility functions for AliExpress supplier-specific operations.

AliExpress Utility Functions
=========================================================================================

This module provides various utility functions specifically designed for interacting with
AliExpress data, including product ID extraction, URL normalization, and locale management.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com.utils import extract_prod_ids, ensure_https, locales

    # Example of using extract_prod_ids
    product_url = "https://www.aliexpress.com/item/10050012345.html"
    product_id = extract_prod_ids(product_url)
    print(f"Extracted Product ID: {product_id}")

    # Example of using ensure_https
    http_url = "http://example.com"
    https_url = ensure_https(http_url)
    print(f"Converted to HTTPS: {https_url}")

    # Example of accessing locales
    print(f"Available Locales: {locales}")
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: suppliers/suppliers_list/aliexpress_com/utils/__init__.py
"""


from .extract_product_id import extract_prod_ids
from .ensure_https import ensure_https
from .locales import locales