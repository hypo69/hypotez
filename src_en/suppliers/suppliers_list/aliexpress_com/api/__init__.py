## \file /src/suppliers/suppliers_list/aliexpress_com/api/__init__.py
# -*- coding: utf-8 -*-
 # <- venv win
"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.api
    :platform: Windows, Unix
    :synopsis: AliExpress API wrapper.

This module provides a Python wrapper for the AliExpress API, allowing interaction
with various AliExpress services such as product information retrieval and affiliate link generation.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com.api import AliexpressApi

    # Example of initializing the API client
    # api_client = AliexpressApi(api_key="YOUR_API_KEY", secret="YOUR_SECRET")
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/api/__init__.py
"""

from .version import __version__, __doc__, __details__

from .api import AliexpressApi
from . import models
