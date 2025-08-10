## \file /src/suppliers/suppliers_list/aliexpress_com/api/_examples/rest/AliexpressAffiliateFeaturedpromoProductsGetRequest.py
# -*- coding: utf-8 -*-
 # <- venv win
"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.api._examples.rest.AliexpressAffiliateFeaturedpromoProductsGetRequest
    :platform: Windows, Unix
    :synopsis: AliExpress Affiliate Featured Promo Products Get Request.

This module defines the `AliexpressAffiliateFeaturedpromoProductsGetRequest` class,
which is used to construct requests for retrieving featured promotional products from the AliExpress API.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com.api._examples.rest import AliexpressAffiliateFeaturedpromoProductsGetRequest

    # Example of creating a request object
    # request = AliexpressAffiliateFeaturedpromoProductsGetRequest()
    # request.set_param("promotion_name", "Summer Sale")
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/api/_examples/rest/AliexpressAffiliateFeaturedpromoProductsGetRequest.py
"""
'''
Created by auto_sdk on 2021.05.17
'''
from ..base import RestApi
class AliexpressAffiliateFeaturedpromoProductsGetRequest(RestApi):
	def __init__(self, domain="api-sg.apiexpress.com", port=80):
		RestApi.__init__(self,domain, port)
		self.app_signature = None
		self.category_id = None
		self.country = None
		self.fields = None
		self.page_no = None
		self.page_size = None
		self.promotion_end_time = None
		self.promotion_name = None
		self.promotion_start_time = None
		self.sort = None
		self.target_currency = None
		self.target_language = None
		self.tracking_id = None

	def getapiname(self):
		return 'apiexpress.affiliate.featuredpromo.products.get'
