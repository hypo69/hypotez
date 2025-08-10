## \file /src/suppliers/suppliers_list/aliexpress_com/api/tools/__init__.py
# -*- coding: utf-8 -*-
 # <- venv win
"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.api.tools
    :platform: Windows, Unix
    :synopsis: Initialization module for AliExpress API tools.

This module serves as the initialization file for the AliExpress API tools package.
It imports the `get_product_id` function, making it directly accessible when this package is imported.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com.api.tools import get_product_id

    # Example of using the get_product_id function
    # product_id = get_product_id("https://www.aliexpress.com/item/123.html")
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/api/tools/__init__.py
"""
from .get_product_id import get_product_id
