## \file /src/suppliers/suppliers_list/aliexpress_com/api/_examples/rest/AliexpressAffiliateCategoryGetRequest.py
# -*- coding: utf-8 -*-
 # <- venv win
"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.api._examples.rest.AliexpressAffiliateCategoryGetRequest
    :platform: Windows, Unix
    :synopsis: AliExpress Affiliate Category Get Request.

This module defines the `AliexpressAffiliateCategoryGetRequest` class,
which is used to construct requests for retrieving affiliate category information from the AliExpress API.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com.api._examples.rest import AliexpressAffiliateCategoryGetRequest

    # Example of creating a request object
    # request = AliexpressAffiliateCategoryGetRequest()
    # request.set_param("fields", "category_id,category_name")
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/api/_examples/rest/AliexpressAffiliateCategoryGetRequest.py
"""
'''
Created by auto_sdk on 2020.03.09
'''
from ..base import RestApi
class AliexpressAffiliateCategoryGetRequest(RestApi):
	def __init__(self, domain="api-sg.apiexpress.com", port=80):
		RestApi.__init__(self,domain, port)
		self.app_signature = None

	def getapiname(self):
		return 'apiexpress.affiliate.category.get'
