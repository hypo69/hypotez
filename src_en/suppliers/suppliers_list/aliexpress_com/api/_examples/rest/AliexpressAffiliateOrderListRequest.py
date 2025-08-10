## \file /src/suppliers/suppliers_list/aliexpress_com/api/_examples/rest/AliexpressAffiliateOrderListRequest.py
# -*- coding: utf-8 -*-
 # <- venv win
"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.api._examples.rest.AliexpressAffiliateOrderListRequest
    :platform: Windows, Unix
    :synopsis: AliExpress Affiliate Order List Request.

This module defines the `AliexpressAffiliateOrderListRequest` class,
which is used to construct requests for retrieving affiliate order lists from the AliExpress API.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com.api._examples.rest import AliexpressAffiliateOrderListRequest

    # Example of creating a request object
    # request = AliexpressAffiliateOrderListRequest()
    # request.set_param("start_time", "2023-01-01 00:00:00")
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/api/_examples/rest/AliexpressAffiliateOrderListRequest.py
"""
'''
Created by auto_sdk on 2021.06.02
'''
from ..base import RestApi
class AliexpressAffiliateOrderListRequest(RestApi):
	def __init__(self, domain="api-sg.apiexpress.com", port=80):
		RestApi.__init__(self,domain, port)
		self.app_signature = None
		self.end_time = None
		self.fields = None
		self.locale_site = None
		self.page_no = None
		self.page_size = None
		self.start_time = None
		self.status = None

	def getapiname(self):
		return 'apiexpress.affiliate.order.list'
