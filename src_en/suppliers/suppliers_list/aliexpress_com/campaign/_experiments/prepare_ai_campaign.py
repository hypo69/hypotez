## \file /src/suppliers/suppliers_list/aliexpress_com/campaign/_experiments/prepare_ai_campaign.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.campaign._experiments
    :platform: Windows, Unix
    :synopsis: Module for preparing AI-driven AliExpress campaigns.

This module provides an example of how to prepare an AI-driven AliExpress advertising campaign,
including processing campaign data with AI models.

Example usage
-------------

```python
    import asyncio
    from src.suppliers.suppliers_list.aliexpress_com.campaign._experiments.prepare_ai_campaign import AliCampaignEditor

    async def main():
        # Example of creating a campaign editor instance and processing an AI campaign
        # editor = AliCampaignEditor(campaign_name="lighting", campaign_file="EN_US.JSON")
        # editor.process_llm_campaign("lighting")
        pass

    if __name__ == "__main__":
        asyncio.run(main())
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/campaign/_experiments/prepare_ai_campaign.py
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
campaign_editor.process_llm_campaign(campaign_name)
#process_all_campaigns()
