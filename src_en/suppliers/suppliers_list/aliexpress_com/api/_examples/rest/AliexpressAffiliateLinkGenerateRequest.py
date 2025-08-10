## \file /src/suppliers/suppliers_list/aliexpress_com/api/_examples/rest/AliexpressAffiliateLinkGenerateRequest.py
# -*- coding: utf-8 -*-
 # <- venv win
"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.api._examples.rest.AliexpressAffiliateLinkGenerateRequest
    :platform: Windows, Unix
    :synopsis: AliExpress Affiliate Link Generate Request.

This module defines the `AliexpressAffiliateLinkGenerateRequest` class,
which is used to construct requests for generating affiliate links from the AliExpress API.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com.api._examples.rest import AliexpressAffiliateLinkGenerateRequest

    # Example of creating a request object
    # request = AliexpressAffiliateLinkGenerateRequest()
    # request.set_param("source_values", "https://www.aliexpress.com/item/1005001234567890.html")
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/api/_examples/rest/AliexpressAffiliateLinkGenerateRequest.py
"""
'''
Created by auto_sdk on 2020.03.09
'''
from ..base import RestApi
class AliexpressAffiliateLinkGenerateRequest(RestApi):
	def __init__(self, domain="api-sg.apiexpress.com", port=80):
		RestApi.__init__(self,domain, port)
		self.app_signature = None
		self.promotion_link_type = None
		self.source_values = None
		self.tracking_id = None

	def getapiname(self):
		return 'apiexpress.affiliate.link.generate'
