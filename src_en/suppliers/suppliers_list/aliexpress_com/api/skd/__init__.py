## \file /src/suppliers/suppliers_list/aliexpress_com/api/skd/__init__.py
# -*- coding: utf-8 -*-
 # <- venv win
"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.api.skd
    :platform: Windows, Unix
    :synopsis: Initialization module for AliExpress SDK.

This module serves as the initialization file for the AliExpress SDK package.
It provides functions for setting and retrieving default application information,
including API key and secret.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com.api.skd import setDefaultAppInfo, getDefaultAppInfo

    # Example of setting default app info
    # setDefaultAppInfo("your_app_key", "your_app_secret")

    # Example of getting default app info
    # app_info = getDefaultAppInfo()
    # print(app_info.appkey)
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/api/skd/__init__.py
"""
'''
Created on 2012-6-29

@author: lihao
'''
from .api.base import sign



class appinfo(object):
    def __init__(self,appkey,secret):
        self.appkey = appkey
        self.secret = secret

def getDefaultAppInfo():
    pass


def setDefaultAppInfo(appkey,secret):
    default = appinfo(appkey,secret)
    global getDefaultAppInfo
    getDefaultAppInfo = lambda: default
