## \file /src/suppliers/suppliers_list/aliexpress_com/campaign/_experiments/prepare_new_campaign.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.campaign._experiments
    :platform: Windows, Unix
    :synopsis: Module for preparing new AliExpress campaigns.

This module provides an example of how to prepare a new AliExpress advertising campaign,
including creating a campaign editor instance and processing the new campaign.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com.campaign._experiments.prepare_new_campaign import AliCampaignEditor

    # Example of creating a campaign editor instance and processing a new campaign
    # editor = AliCampaignEditor(campaign_name="my_new_campaign")
    # editor.process_new_campaign("my_new_campaign")
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/campaign/_experiments/prepare_new_campaign.py
"""




""" Experiments on the new advertising campaign scenario """

...
import header

from pathlib import Path

from src import gs

from src.suppliers.suppliers_list.aliexpress_com.campaign import AliCampaignEditor
from src.utils.file import get_filenames, get_directory_names
from src.utils.printer import pprint
from src.logger.logger import logger

campaign_name = 'rc'
aliexpress_editor =  AliCampaignEditor(campaign_name)
aliexpress_editor.process_new_campaign(campaign_name)
