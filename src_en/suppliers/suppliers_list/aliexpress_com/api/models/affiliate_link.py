## \file /src/suppliers/suppliers_list/aliexpress_com/api/models/affiliate_link.py
# -*- coding: utf-8 -*-
 # <- venv win
"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.api.models.affiliate_link
    :platform: Windows, Unix
    :synopsis: Data model for AliExpress affiliate links.

This module defines the `AffiliateLink` class, which represents the structure
of an affiliate link returned by the AliExpress API.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com.api.models import AffiliateLink

    # Example of creating an AffiliateLink object
    # link = AffiliateLink()
    # link.promotion_link = "https://ali.ski/example"
    # link.source_value = "https://www.aliexpress.com/item/123.html"
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/api/models/affiliate_link.py
"""
class AffiliateLink:
    promotion_link: str
    source_value: str
