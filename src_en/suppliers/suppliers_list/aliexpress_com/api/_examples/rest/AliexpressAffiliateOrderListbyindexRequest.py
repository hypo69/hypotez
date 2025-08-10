## \file /src/suppliers/suppliers_list/aliexpress_com/api/_examples/rest/AliexpressAffiliateOrderListbyindexRequest.py
# -*- coding: utf-8 -*-
 # <- venv win
"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.api._examples.rest.AliexpressAffiliateOrderListbyindexRequest
    :platform: Windows, Unix
    :synopsis: AliExpress Affiliate Order List by Index Request.

This module defines the `AliexpressAffiliateOrderListbyindexRequest` class,
which is used to construct requests for retrieving affiliate order lists by index from the AliExpress API.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com.api._examples.rest import AliexpressAffiliateOrderListbyindexRequest

    # Example of creating a request object
    # request = AliexpressAffiliateOrderListbyindexRequest()
    # request.set_param("start_time", "2023-01-01 00:00:00")
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/api/_examples/rest/AliexpressAffiliateOrderListbyindexRequest.py
"""
'''
Created by auto_sdk on 2021.05.10
'''
from ..base import RestApi
class AliexpressAffiliateOrderListbyindexRequest(RestApi):
	def __init__(self, domain="api-sg.apiexpress.com", port=80):
		RestApi.__init__(self,domain, port)
		self.app_signature = None
		self.end_time = None
		self.fields = None
		self.page_size = None
		self.start_query_index_id = None
		self.start_time = None
		self.status = None

	def getapiname(self):
		return 'apiexpress.affiliate.order.listbyindex'
