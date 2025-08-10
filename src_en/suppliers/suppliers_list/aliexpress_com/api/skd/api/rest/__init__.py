## \file /src/suppliers/suppliers_list/aliexpress_com/api/skd/api/rest/__init__.py
# -*- coding: utf-8 -*-
 # <- venv win
"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.api.skd.api.rest
    :platform: Windows, Unix
    :synopsis: Initialization module for AliExpress SDK REST API requests.

This module serves as the initialization file for the AliExpress SDK REST API requests package.
It imports various request classes for different AliExpress API functionalities.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com.api.skd.api.rest import AliexpressAffiliateProductSmartmatchRequest

    # Example of using an imported request class
    # request = AliexpressAffiliateProductSmartmatchRequest()
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/api/skd/api/rest/__init__.py
"""
from .AliexpressAffiliateProductSmartmatchRequest import AliexpressAffiliateProductSmartmatchRequest
from .AliexpressAffiliateOrderGetRequest import AliexpressAffiliateOrderGetRequest
from .AliexpressAffiliateOrderListRequest import AliexpressAffiliateOrderListRequest
from .AliexpressAffiliateHotproductDownloadRequest import AliexpressAffiliateHotproductDownloadRequest
from .AliexpressAffiliateProductdetailGetRequest import AliexpressAffiliateProductdetailGetRequest
from .AliexpressAffiliateHotproductQueryRequest import AliexpressAffiliateHotproductQueryRequest
from .AliexpressAffiliateFeaturedpromoProductsGetRequest import AliexpressAffiliateFeaturedpromoProductsGetRequest
from .AliexpressAffiliateFeaturedpromoGetRequest import AliexpressAffiliateFeaturedpromoGetRequest
from .AliexpressAffiliateProductQueryRequest import AliexpressAffiliateProductQueryRequest
from .AliexpressAffiliateCategoryGetRequest import AliexpressAffiliateCategoryGetRequest
from .AliexpressAffiliateOrderListbyindexRequest import AliexpressAffiliateOrderListbyindexRequest
from .AliexpressAffiliateLinkGenerateRequest import AliexpressAffiliateLinkGenerateRequest
