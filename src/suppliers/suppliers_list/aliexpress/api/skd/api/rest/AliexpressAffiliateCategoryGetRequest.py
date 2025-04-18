## \file /src/suppliers/aliexpress/api/skd/api/rest/AliexpressAffiliateCategoryGetRequest.py
# -*- coding: utf-8 -*-
 # <- venv win
## ~~~~~~~~~~~~~
""" module: src.suppliers.suppliers_list.aliexpress.api.skd.api.rest """
"""
Created by auto_sdk on 2020.03.09
"""
from ..base import RestApi


class AliexpressAffiliateCategoryGetRequest(RestApi):
    def __init__(self, domain="api-sg.aliexpress.com", port=80):
        RestApi.__init__(self, domain, port)
        self.app_signature = None

    def getapiname(self):
        return "aliexpress.affiliate.category.get"

