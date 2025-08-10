## \file /src/suppliers/aliexpress_com/__init__.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.suppliers_list.aliexpress_com
    :platform: Windows, Unix
    :synopsis: Initialization module for the AliExpress supplier.

This module serves as the initialization file for the AliExpress supplier package.
It imports various classes and functions related to AliExpress API, requests, and campaign management.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com import AliApi, AliRequests

    # Example of using the imported classes
    # api = AliApi(...)
    # requests = AliRequests(...)
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/__init__.py
"""


from .aliapi import AliApi
from .alirequests import AliRequests
from .campaign import AliCampaignEditor
from .campaign.html_generators import ProductHTMLGenerator, CategoryHTMLGenerator, CampaignHTMLGenerator
