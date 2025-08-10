## \file /src/suppliers/suppliers_list/aliexpress_com/api/_examples/rest/AliexpressAffiliateHotproductDownloadRequest.py
# -*- coding: utf-8 -*-
 # <- venv win
"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.api._examples.rest.AliexpressAffiliateHotproductDownloadRequest
    :platform: Windows, Unix
    :synopsis: AliExpress Affiliate Hot Product Download Request.

This module defines the `AliexpressAffiliateHotproductDownloadRequest` class,
which is used to construct requests for downloading hot product data from the AliExpress API.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com.api._examples.rest import AliexpressAffiliateHotproductDownloadRequest

    # Example of creating a request object
    # request = AliexpressAffiliateHotproductDownloadRequest()
    # request.set_param("category_id", "12345")
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/api/_examples/rest/AliexpressAffiliateHotproductDownloadRequest.py
"""
'''
Created by auto_sdk on 2021.05.12
'''
from ..base import RestApi
class AliexpressAffiliateHotproductDownloadRequest(RestApi):
	def __init__(self, domain="api-sg.apiexpress.com", port=80):
		RestApi.__init__(self,domain, port)
		self.app_signature = None
		self.category_id = None
		self.country = None
		self.fields = None
		self.scenario_language_site = None
		self.page_no = None
		self.page_size = None
		self.target_currency = None
		self.target_language = None
		self.tracking_id = None

	def getapiname(self):
		return 'apiexpress.affiliate.hotproduct.download'
