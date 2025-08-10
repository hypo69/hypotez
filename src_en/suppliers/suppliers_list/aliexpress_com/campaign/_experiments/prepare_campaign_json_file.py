## \file /src/suppliers/suppliers_list/aliexpress_com/campaign/_experiments/prepare_campaign_json_file.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.campaign._experiments
    :platform: Windows, Unix
    :synopsis: Module for preparing AliExpress campaign JSON files.

This module provides an example of how to prepare a JSON file for an AliExpress advertising campaign,
including creating a campaign editor instance and accessing campaign data.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com.campaign._experiments.prepare_campaign_json_file import AliCampaignEditor

    # Example of creating a campaign editor instance
    # editor = AliCampaignEditor(campaign_name="lighting", campaign_file="EN_US.JSON")
    # print(editor.campaign_file)
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/campaign/_experiments/prepare_campaign_json_file.py
"""



""" Checking campaign creation """



import header
from pathlib import Path
from src.suppliers.suppliers_list.aliexpress_com.campaign import AliCampaignEditor
from src import gs
from src.suppliers.suppliers_list.aliexpress_com.campaign import process_campaign_category, process_campaign,  process_all_campaigns
from src.utils.file import get_filenames, get_directory_names
from src.utils.printer import pprint
from src.logger.logger import logger

#locales = {'EN': 'USD', 'HE': 'ILS', 'RU': 'ILS'}
campaign_name = 'lighting'
campaign_file = 'EN_US.JSON'
campaign_editor = AliCampaignEditor(campaign_name = campaign_name, campaign_file = campaign_file )
campaign_file
#process_campaign(campaign_name)
#process_all_campaigns()
