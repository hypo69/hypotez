## \file /src/suppliers/suppliers_list/aliexpress_com/campaign/_examples/_examle_prepare_campains.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.campaign._examples
    :platform: Windows, Unix
    :synopsis: Example of preparing AliExpress campaigns.

This module provides examples of how to use the campaign preparation functions
for AliExpress, including processing single categories, specific campaigns, and all campaigns.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com.campaign._examples._examle_prepare_campains import process_campaign_category, process_campaign, process_all_campaigns

    # Example 1: Process a Single Campaign Category
    # process_campaign_category("SummerSale", "Electronics", "EN", "USD", force=True)

    # Example 2: Process a Specific Campaign
    # process_campaign("WinterSale", categories=["Clothing", "Toys"], language="EN", currency="USD", force=False)

    # Example 3: Process All Campaigns
    # process_all_campaigns(language="EN", currency="USD", force=True)
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/campaign/_examples/_examle_prepare_campains.py
"""


from ..prepare_campaigns import *

# Example 1: Process a Single Campaign Category
process_campaign_category("SummerSale", "Electronics", "EN", "USD", force=True)

# Example 2: Process a Specific Campaign
process_campaign("WinterSale", categories=["Clothing", "Toys"], language="EN", currency="USD", force=False)

# Example 3: Process All Campaigns
process_all_campaigns(language="EN", currency="USD", force=True)


campaigns_directory = Path(gs.path.google_drive,'aliexpress','campaigns')
campaign_names = get_directory_names(campaigns_directory)
languages = {'EN': 'USD', 'HE': 'ILS', 'RU': 'ILS'}
