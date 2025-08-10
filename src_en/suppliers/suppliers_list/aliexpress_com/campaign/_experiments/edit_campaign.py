## \file /src/suppliers/suppliers_list/aliexpress_com/campaign/_experiments/edit_campaign.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.campaign._experiments
    :platform: Windows, Unix
    :synopsis: Module for editing AliExpress campaigns.

This module provides functionality to edit AliExpress advertising campaigns,
including loading campaign data and making modifications.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com.campaign._experiments.edit_campaign import AliCampaignEditor

    # Example of creating a campaign editor instance
    # editor = AliCampaignEditor(campaign_name="SummerSale", category_name="Electronics", language="EN", currency="USD")
    # # Now you can use the editor to modify campaign properties
    # print(editor.campaign.name)
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/campaign/_experiments/edit_campaign.py
"""



""" Advertising campaign editor """
...


import header
from pathlib import Path

from src import gs
from src.suppliers.suppliers_list.aliexpress_com.campaign import AliCampaignEditor
from src.suppliers.suppliers_list.aliexpress_com.campaign import  process_campaign, process_campaign_category, process_all_campaigns
from src.utils.file import get_filenames, get_directory_names
from src.utils.printer import pprint

locales = {'EN': 'USD', 'HE': 'ILS', 'RU': 'ILS'}


# campaign_name = "030724_men_summer_fashion"
# category_name = "men_summer_tshirts"

campaign_name = "building_bricks"
category_name = "building_bricks"
a = AliCampaignEditor(campaign_name,'EN','USD')
...
