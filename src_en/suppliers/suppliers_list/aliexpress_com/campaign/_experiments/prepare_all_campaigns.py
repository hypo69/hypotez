## \file /src/suppliers/suppliers_list/aliexpress_com/campaign/_experiments/prepare_all_campaigns.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.campaign._experiments
    :platform: Windows, Unix
    :synopsis: Module for preparing all AliExpress campaigns.

This module provides functionality to process all AliExpress advertising campaigns
for all languages, by searching for category names from directories.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com.campaign._experiments.prepare_all_campaigns import process_all_campaigns

    # Example of processing all campaigns
    # process_all_campaigns(language="EN", currency="USD", force=True)
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/campaign/_experiments/prepare_all_campaigns.py
"""



""" Runs all advertising campaigns for all languages by searching for category names from directories """
...
import header
from src.suppliers.suppliers_list.aliexpress_com.campaign.prepare_campaigns import process_all_campaigns, main_process

# locales = {'EN': 'USD', 'HE': 'ILS', 'RU': 'ILS'}
# campaign_name:str = 'rc'
# language: str = 'EN'
# currency: str = 'USD'
# campaign_file:str = None
# # If the current advertising campaign does not exist, a new one will be created

process_campaign(campaign_name = campaign_name, language = language, currency = currency, campaign_file = campaign_file)
main_process('brands',['mrgreen'])
#process_all_campaigns()
