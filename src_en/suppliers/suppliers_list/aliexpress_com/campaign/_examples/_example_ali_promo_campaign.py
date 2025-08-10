## \file /src/suppliers/suppliers_list/aliexpress_com/campaign/_examples/_example_ali_promo_campaign.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.campaign._examples
    :platform: Windows, Unix
    :synopsis: Example of AliExpress promotional campaign creation.

This module provides examples of how to create and manage AliExpress promotional campaigns,
including setting up campaign parameters and accessing product data.

Example usage
-------------

```python
    import asyncio
    from src.suppliers.suppliers_list.aliexpress_com.campaign._examples._example_ali_promo_campaign import AliPromoCampaign

    async def main():
        # Example of creating a promotional campaign
        # campaign_instance = AliPromoCampaign(campaign_name="SummerSale", category_name="Electronics", language="EN", currency="USD")
        # print(campaign_instance.campaign.name)
        pass

    if __name__ == "__main__":
        asyncio.run(main())
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/campaign/_examples/_example_ali_promo_campaign.py
"""


""" Examples of creating an advertising campaign """



...
import header
from pathlib import Path
from types import SimpleNamespace
from src import gs
from src.suppliers.suppliers_list.aliexpress.ali_promo_campaign import AliPromoCampaign
from src.suppliers.suppliers_list.aliexpress import AliAffiliatedProducts
from src.utils import get_filenames, get_directory_names, read_text_file, csv2dict
from src.utils.jjson import j_loads_ns
from src.utils.printer import pprint
from src.logger.logger import logger

campaigns_directory = Path(gs.path.google_drive, 'aliexpress', 'campaigns')
campaign_names = get_directory_names(campaigns_directory)

campaign_name = '280624_cleararanse'
category_name = 'gaming_comuter_accessories'
language = 'EN'
currency = 'USD'

a:SimpleNamespace = AliPromoCampaign(campaign_name = campaign_name,
                     category_name = category_name,
                     language = language,
                     currency = currency)

campaign = a.campaign
category = a.category
products = a.category.products

# dict
a = AliPromoCampaign(campaign_name,category_name,{'EN':'USD'})
# string
a = AliPromoCampaign(campaign_name,category_name, 'EN','USD')
