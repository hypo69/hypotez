## \file /src/suppliers/suppliers_list/aliexpress_com/api/skd/api/rest/AliexpressAffiliateProductdetailGetRequest.py
# -*- coding: utf-8 -*-
 # <- venv win
"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.api.skd.api.rest.AliexpressAffiliateProductdetailGetRequest
    :platform: Windows, Unix
    :synopsis: AliExpress Affiliate Product Detail Get Request.

This module defines the `AliexpressAffiliateProductdetailGetRequest` class,
which is used to construct requests for retrieving detailed product information from the AliExpress API.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com.api.skd.api.rest import AliexpressAffiliateProductdetailGetRequest

    # Example of creating a request object
    # request = AliexpressAffiliateProductdetailGetRequest()
    # request.set_param("product_ids", "12345")
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/api/skd/api/rest/AliexpressAffiliateProductdetailGetRequest.py
"""
"""
Created by auto_sdk on 2021.05.17
"""
from ..base import RestApi


class AliexpressAffiliateProductdetailGetRequest(RestApi):
    def __init__(self, domain="api-sg.apiexpress.com", port=80):
        RestApi.__init__(self, domain, port)
        self.app_signature = None
        self.country = None
        self.fields = None
        self.product_ids = None
        self.target_currency = None
        self.target_language = None
        self.tracking_id = None

    def getapiname(self):
        return "apiexpress.affiliate.productdetail.get"
