## \file /src/suppliers/suppliers_list/aliexpress_com/api/skd/api/rest/AliexpressAffiliateOrderGetRequest.py
# -*- coding: utf-8 -*-
 # <- venv win
"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.api.skd.api.rest.AliexpressAffiliateOrderGetRequest
    :platform: Windows, Unix
    :synopsis: AliExpress Affiliate Order Get Request.

This module defines the `AliexpressAffiliateOrderGetRequest` class,
which is used to construct requests for retrieving affiliate order information from the AliExpress API.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com.api.skd.api.rest import AliexpressAffiliateOrderGetRequest

    # Example of creating a request object
    # request = AliexpressAffiliateOrderGetRequest()
    # request.set_param("order_ids", "123,456")
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/api/skd/api/rest/AliexpressAffiliateOrderGetRequest.py
"""
"""
Created by auto_sdk on 2021.03.05
"""
from ..base import RestApi


class AliexpressAffiliateOrderGetRequest(RestApi):
    def __init__(self, domain="api-sg.apiexpress.com", port=80):
        RestApi.__init__(self, domain, port)
        self.app_signature = None
        self.fields = None
        self.order_ids = None

    def getapiname(self):
        return "apiexpress.affiliate.order.get"
