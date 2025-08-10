## \file /src/suppliers/suppliers_list/aliexpress_com/campaign/_experiments/gsheets-quick.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.campaign._experiments
    :platform: Windows, Unix
    :synopsis: Quick example for working with Google Sheets for AliExpress campaigns.

This module provides a quick example of how to interact with Google Sheets
for managing AliExpress campaigns, including setting up worksheets and saving campaign data.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com.campaign._experiments.gsheets-quick import AliCampaignGoogleSheet

    # Example of initializing and using the Google Sheet handler
    # gs = AliCampaignGoogleSheet(campaign_name="lighting", language='EN', currency='USD')
    # gs.set_products_worksheet("chandeliers")
    # gs.save_campaign_from_worksheet()
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/campaign/_experiments/gsheets-quick.py
"""



""" Working with Google Sheets """


from unicodedata import category
import header
from types import SimpleNamespace
from gspread import Worksheet, Spreadsheet
from src.suppliers.suppliers_list.aliexpress_com.campaign import AliCampaignGoogleSheet
from src.suppliers.suppliers_list.aliexpress_com.campaign.ttypes import CampaignType, CategoryType, ProductType
from src.utils.printer import pprint
from src.logger.logger import logger


campaign_name = "lighting"
category_name = "chandeliers"
language = 'EN'
currency = 'USD'

gs = AliCampaignGoogleSheet(campaign_name=campaign_name, language=language, currency=currency)

gs.set_products_worksheet(category_name)
#gs.save_categories_from_worksheet(False)
gs.save_campaign_from_worksheet()
...
