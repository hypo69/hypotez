## \file /src/suppliers/suppliers_list/aliexpress_com/campaign/__init__.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.campaign
    :platform: Windows, Unix
    :synopsis: Modules for managing AliExpress advertising campaigns.

This module provides various functionalities for managing AliExpress advertising campaigns,
including campaign editing, processing, and HTML generation.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com.campaign import AliCampaignEditor

    # Example of using the campaign editor
    # editor = AliCampaignEditor(...)
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/campaign/__init__.py
"""



from .ali_campaign_editor import AliCampaignEditor
#from .gsheet import AliCampaignGoogleSheet
from .prepare_campaigns import  process_campaign, process_campaign_category, process_all_campaigns
#from .ali_campaign_editor_jupyter_widgets import JupyterCampaignEditorWidgets
from .html_generators import CategoryHTMLGenerator, ProductHTMLGenerator
