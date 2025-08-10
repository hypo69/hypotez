## \file /src/suppliers/suppliers_list/aliexpress_com/campaign/_examples/_example_edit_campaign.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.campaign._examples
    :platform: Windows, Unix
    :synopsis: Example of editing an AliExpress campaign.

This module provides an example of how to edit an AliExpress advertising campaign,
including loading campaign data and making modifications.

Example usage
-------------

```python
    import asyncio
    from src.suppliers.suppliers_list.aliexpress_com.campaign._examples._example_edit_campaign import AliCampaignEditor

    async def main():
        # Example of creating a campaign editor instance
        # editor = AliCampaignEditor(campaign_name="SummerSale", category_name="Electronics", language="EN", currency="USD")
        # # Now you can use the editor to modify campaign properties
        # print(editor.campaign.name)
        pass

    if __name__ == "__main__":
        asyncio.run(main())
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/campaign/_examples/_example_edit_campaign.py
"""



""" Advertising campaign editor """
...
import re
import shutilrom pathlib import Path
from typing import List, Optional, Union
from types import SimpleNamespace
from src import gs
from src.suppliers.suppliers_list.aliexpress_com.campaign.ali_promo_campaign import AliPromoCampaign
from src.suppliers.suppliers_list.aliexpress_com.affiliated_products_generator import AliAffiliatedProducts
from src.suppliers.suppliers_list.aliexpress_com.utils.extract_product_id import extract_prod_ids
from src.suppliers.suppliers_list.aliexpress_com.utils.ensure_https import ensure_https
from src.utils.jjson import j_loads_ns, j_loads
from src.utils.convertors import list2string, csv2dict
from src.utils.printer import pprint
from src.utils.jjson import j_dumps, j_loads, j_loads_ns
from src.utils.file import read_text_file, get_filenames
from src.logger.logger import logger

class AliCampaignEditor(AliPromoCampaign):
    """ Advertising campaign editor """
    ...

    def __init__(self, campaign_name: str, category_name: str, language: str = 'EN', currency: str = 'USD'):
        """"""
        ...
        super().__init__(campaign_name, category_name, language, currency)
