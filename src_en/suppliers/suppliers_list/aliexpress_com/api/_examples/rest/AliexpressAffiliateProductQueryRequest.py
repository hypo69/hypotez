## \file /src/suppliers/suppliers_list/aliexpress_com/api/_examples/rest/AliexpressAffiliateProductQueryRequest.py
# -*- coding: utf-8 -*-
 # <- venv win
"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.api._examples.rest.AliexpressAffiliateProductQueryRequest
    :platform: Windows, Unix
    :synopsis: AliExpress Affiliate Product Query Request.

This module defines the `AliexpressAffiliateProductQueryRequest` class,
which is used to construct requests for querying product data from the AliExpress API.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com.api._examples.rest import AliexpressAffiliateProductQueryRequest

    # Example of creating a request object
    # request = AliexpressAffiliateProductQueryRequest()
    # request.set_param("keywords", "shoes")
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/api/_examples/rest/AliexpressAffiliateProductQueryRequest.py
"""
'''
Created by auto_sdk on 2021.05.20
'''
from ..base import RestApi
class AliexpressAffiliateProductQueryRequest(RestApi):
	def __init__(self, domain="api-sg.apiexpress.com", port=80):
		RestApi.__init__(self,domain, port)
		self.app_signature = None
		self.category_ids = None
		self.delivery_days = None
		self.fields = None
		self.keywords = None
		self.max_sale_price = None
		self.min_sale_price = None
		self.page_no = None
		self.page_size = None
		self.platform_product_type = None
		self.ship_to_country = None
		self.sort = None
		self.target_currency = None
		self.target_language = None
		self.tracking_id = None

	def getapiname(self):
		return 'apiexpress.affiliate.product.query'
