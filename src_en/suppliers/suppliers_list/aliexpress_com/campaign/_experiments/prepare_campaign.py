## \file /src/suppliers/suppliers_list/aliexpress_com/campaign/_experiments/prepare_campaign.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.campaign._experiments
    :platform: Windows, Unix
    :synopsis: Module for preparing AliExpress campaigns.

This module provides an example of how to prepare an AliExpress advertising campaign,
including creating a new campaign if it does not exist.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com.campaign._experiments.prepare_campaign import process_campaign

    # Example of processing a campaign
    # process_campaign(campaign_name="my_campaign", language="EN", currency="USD")
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/campaign/_experiments/prepare_campaign.py
"""



""" Checking the creation of an affiliate for an advertising campaign
If the current advertising campaign does not exist, a new one will be created"""

...
import header
from src.suppliers.suppliers_list.aliexpress_com.campaign import process_campaign

locales = {'EN': 'USD', 'HE': 'ILS', 'RU': 'ILS'}
language: str = 'EN'
currency: str = 'USD'
campaign_name:str = 'brands'
# If the current advertising campaign does not exist, a new one will be created

#process_campaign(campaign_name = campaign_name, language = language, currency = currency, campaign_file = campaign_file)
process_campaign(campaign_name = campaign_name)
