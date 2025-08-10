## \file /src/suppliers/suppliers_list/aliexpress_com/api/skd/api/__init__.py
# -*- coding: utf-8 -*-
 # <- venv win
"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.api.skd.api
    :platform: Windows, Unix
    :synopsis: Initialization module for AliExpress SDK API.

This module serves as the initialization file for the AliExpress SDK API package.
It imports all components from the `rest` submodule and `FileItem` from the `base` submodule,
making them directly accessible when this package is imported.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com.api.skd.api import AliexpressAffiliateCategoryGetRequest

    # Example of using an imported request class
    # request = AliexpressAffiliateCategoryGetRequest()
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/api/skd/api/__init__.py
"""
from .rest import *
from .base import FileItem
