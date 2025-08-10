## \file /src/suppliers/suppliers_list/aliexpress_com/campaign/_experiments/gsheets-step-by-step.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.campaign._experiments
    :platform: Windows, Unix
    :synopsis: Step-by-step example for working with Google Sheets for AliExpress campaigns.

This module provides a detailed, step-by-step example of how to interact with Google Sheets
for managing AliExpress campaigns, including setting up worksheets, retrieving and updating campaign data.

Example usage
-------------

```python
    import asyncio
    from src.suppliers.suppliers_list.aliexpress_com.campaign._experiments.gsheets-step-by-step import AliCampaignGoogleSheet, AliCampaignEditor

    async def main():
        # Example of initializing and using the Google Sheet handler and campaign editor
        # gs = AliCampaignGoogleSheet('1nu4mNNFMzSePlggaaL_QM2vdKVP_NNBl2OG7R9MNrs0')
        # campaign_editor = AliCampaignEditor("lighting", 'EN', 'USD')
        # # ... further operations to set and get data from Google Sheets
        pass

    if __name__ == "__main__":
        asyncio.run(main())
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/campaign/_experiments/gsheets-step-by-step.py
"""



""" Experiments with Google Sheets """


import header
from types import SimpleNamespace
from gspread import Spreadsheet, Worksheet
from src.suppliers.suppliers_list.aliexpress import campaign
from src.suppliers.suppliers_list.aliexpress_com.campaign import AliCampaignGoogleSheet , AliCampaignEditor
from src.suppliers.suppliers_list.aliexpress_com.campaign.ttypes import CampaignType, CategoryType, ProductType
from src.utils.printer import pprint
from src.logger.logger import logger


gs = AliCampaignGoogleSheet('1nu4mNNFMzSePlggaaL_QM2vdKVP_NNBl2OG7R9MNrs0')
...
campaign_name = "lighting"
language = 'EN'
currency = 'USD'

campaign_editor = AliCampaignEditor(campaign_name, language, currency)
campaign_data = campaign_editor.campaign
_categories: SimpleNamespace = campaign_data.category

# Convert _categories to a dictionary
categories_dict: dict[str, CategoryType] = {category_name: getattr(_categories, category_name) for category_name in vars(_categories)}

# Convert categories to a list for Google Sheets
categories_list: list[CategoryType] = list(categories_dict.values())

# Set categories in Google Sheet
gs.set_categories(categories_list)

# Get edited categories from Google Sheet
edited_categories: list[dict] = gs.get_categories()

# Update categories_dict with edited data
for _cat in edited_categories:
    _cat_ns: SimpleNamespace = SimpleNamespace(**{
        'name':_cat['name'],
        'title':_cat['title'],
        'description':_cat['description'],
        'tags':_cat['tags'],
        'products_count':_cat['products_count']
    }
    )
    # Logging for debugging
    logger.info(f"Updating category: {_cat_ns.name}")
    categories_dict[_cat_ns.name] = _cat_ns
    products = campaign_editor.get_category_products(_cat_ns.name)
    gs.set_category_products(_cat_ns.name,products)

# Convert categories_dict back to SimpleNamespace manually
_updated_categories = SimpleNamespace(**categories_dict)

# Output data for debugging
pprint(_updated_categories)

# Create dictionary for campaign
campaign_dict: dict = {
    'name': campaign_data.campaign_name,
    'title': campaign_data.title,
    'language': language,
    'currency': currency,
    'category': _updated_categories
}

edited_campaign: SimpleNamespace = SimpleNamespace(**campaign_dict)



# Example of using pprint to output data
pprint(edited_campaign)
campaign_editor.update_campaign(edited_campaign)
