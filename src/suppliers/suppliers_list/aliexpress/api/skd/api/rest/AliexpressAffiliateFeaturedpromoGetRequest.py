## \file /src/suppliers/aliexpress/api/skd/api/rest/AliexpressAffiliateFeaturedpromoGetRequest.py
# -*- coding: utf-8 -*-
 # <- venv win
## ~~~~~~~~~~~~~
""" module: src.suppliers.suppliers_list.aliexpress.api.skd.api.rest """
"""
Created by auto_sdk on 2020.09.25
"""
from ..base import RestApi


class AliexpressAffiliateFeaturedpromoGetRequest(RestApi):
    def __init__(self, domain="api-sg.aliexpress.com", port=80):
        RestApi.__init__(self, domain, port)
        self.app_signature = None
        self.fields = None

    def getapiname(self):
        return "aliexpress.affiliate.featuredpromo.get"

