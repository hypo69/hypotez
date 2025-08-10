## \file /src/suppliers/suppliers_list/aliexpress_com/api/_examples/rest/AliexpressAffiliateFeaturedpromoGetRequest.py
# -*- coding: utf-8 -*-
 # <- venv win
"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.api._examples.rest.AliexpressAffiliateFeaturedpromoGetRequest
    :platform: Windows, Unix
    :synopsis: AliExpress Affiliate Featured Promo Get Request.

This module defines the `AliexpressAffiliateFeaturedpromoGetRequest` class,
which is used to construct requests for retrieving featured promotional information from the AliExpress API.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com.api._examples.rest import AliexpressAffiliateFeaturedpromoGetRequest

    # Example of creating a request object
    # request = AliexpressAffiliateFeaturedpromoGetRequest()
    # request.set_param("fields", "promo_id,promo_name")
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/api/_examples/rest/AliexpressAffiliateFeaturedpromoGetRequest.py
"""
'''
Created by auto_sdk on 2020.09.25
'''
from ..base import RestApi
class AliexpressAffiliateFeaturedpromoGetRequest(RestApi):
	def __init__(self, domain="api-sg.apiexpress.com", port=80):
		RestApi.__init__(self,domain, port)
		self.app_signature = None
		self.fields = None

	def getapiname(self):
		return 'apiexpress.affiliate.featuredpromo.get'
