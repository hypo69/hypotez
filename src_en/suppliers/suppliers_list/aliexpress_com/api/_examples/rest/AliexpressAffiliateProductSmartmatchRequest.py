## \file /src/suppliers/suppliers_list/aliexpress_com/api/_examples/rest/AliexpressAffiliateProductSmartmatchRequest.py
# -*- coding: utf-8 -*-
 # <- venv win
"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.api._examples.rest.AliexpressAffiliateProductSmartmatchRequest
    :platform: Windows, Unix
    :synopsis: AliExpress Affiliate Product Smartmatch Request.

This module defines the `AliexpressAffiliateProductSmartmatchRequest` class,
which is used to construct requests for smart-matching products from the AliExpress API.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com.api._examples.rest import AliexpressAffiliateProductSmartmatchRequest

    # Example of creating a request object
    # request = AliexpressAffiliateProductSmartmatchRequest()
    # request.set_param("keywords", "laptop")
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/api/_examples/rest/AliexpressAffiliateProductSmartmatchRequest.py
"""
'''
Created by auto_sdk on 2021.05.17
'''
from ..base import RestApi
class AliexpressAffiliateProductSmartmatchRequest(RestApi):
	def __init__(self, domain="api-sg.apiexpress.com", port=80):
		RestApi.__init__(self,domain, port)
		self.app = None
		self.app_signature = None
		self.country = None
		self.device = None
		self.device_id = None
		self.fields = None
		self.keywords = None
		self.page_no = None
		self.product_id = None
		self.site = None
		self.target_currency = None
		self.target_language = None
		self.tracking_id = None
		self.user = None

	def getapiname(self):
		return 'apiexpress.affiliate.product.smartmatch'
