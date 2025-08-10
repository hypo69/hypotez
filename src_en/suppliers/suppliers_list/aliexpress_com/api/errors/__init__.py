## \file /src/suppliers/suppliers_list/aliexpress_com/api/errors/__init__.py
# -*- coding: utf-8 -*-
 # <- venv win
"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.api.errors
    :platform: Windows, Unix
    :synopsis: Initialization module for AliExpress API errors.

This module serves as the initialization file for the AliExpress API errors package.
It imports all custom exception classes defined in the `exceptions` submodule,
making them directly accessible when this package is imported.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com.api.errors import ApiRequestException

    # Example of using an imported exception
    # try:
    #     raise ApiRequestException("An API request error occurred.")
    # except ApiRequestException as e:
    #     print(e)
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/api/errors/__init__.py
"""
from .exceptions import *
