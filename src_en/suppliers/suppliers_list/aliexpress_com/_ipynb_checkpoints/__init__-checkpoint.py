## \file /src/suppliers/aliexpress_com/_ipynb_checkpoints/__init__-checkpoint.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.aliexpress_com._ipynb_checkpoints
    :platform: Windows, Unix
    :synopsis: Initialization checkpoint for AliExpress supplier.

This module serves as an initialization checkpoint for the AliExpress supplier package.
It contains version information and a detailed explanation of the module's structure and functionalities.

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com._ipynb_checkpoints.__init__-checkpoint import MODE

    print(f"Mode: {MODE}")
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/_ipynb_checkpoints/__init__-checkpoint.py
"""
MODE = 'dev'

""" supplier `aliexpress`

Here is the list of files and directories that are included in the `aliexpress` module, excluding those that start with multiple underscores or are within `_experiments`:
@rst
### Files and Directories

1. **spreadsheet.py**
2. **aliexpress/**
   - **\_\_init\_\_.py**
   - **affiliate_links_shortener_via_webdriver.py**
   - **affiliated_products_generator.py**
   - **aliapi.py**
   - **aliexpress_com.json**
   - **aliexpress_com.py**
   - **alirequests.py**
   - **category.py**
   - **desktop.ini**
   - **graber.py**
   - **version.py**
   - **_docs/**
     - affiliated_products_generator.md
   - **_dot/**
     - affiliated_products_generator.dot
     - aliapi.dot
   - **_examples/**
     - affiliated_products_generator.en.md
     - affiliated_products_generator.py
     - affiliated_products_generator.ru.md
   - **_pytests/**
     - test_affiliated_products_generator.py
   - **api/**
     - \_\_init\_\_.py
     - api.py
     - version.py
     - **_examples/iop/**
       - .DS_Store
       - \_\_init\_\_.py
       - base.py
       - test_get.py
       - test_internal.py
       - test_iop.ipynb
   - **campaign/**
     - \_\_init\_\_.py
     - campaign.py
     - gsheet.py
     - **_mermaid/**
       - AliAffiliatedProducts.mer
       - aliexpress_campaign.mer
     - **_pytest/**
       - guide_test.md
       - test_alipromo_campaign.py
       - test_campaign_integration.py
       - test_edit_campaign.py
       - test_prepare_campaigns.py
   - **gapi/**
     - \_\_init\_\_.py
     - campaign_editor.py
     - header.py
     - version.py
   - **gui/**
     - \_\_init\_\_.py
     - campaign.py
     - category.py
     - header.py
     - main.py
     - product.py
     - styles.py
     - version.py
   - **locators/**
     - affiliate_links_shortener.json
     - category.json
     - deals.json
     - from_mail.json
     - login.json
     - product.json
     - store.json
   - **utils/**
     - extract_product_id.py
     - set_full_https.py
@endrst
This structure and the explanation provide an overview of the `aliexpress` module's functionalities and organization.
"""
...

...
from packaging import version
#from .version import __version__, __doc__, __details__

from .aliexpress import Aliexpress
from .aliapi import AliApi
from .alirequests import AliRequests
from .campaign import AliCampaignEditor, AliCampaignGoogleSheet
from .campaign.html_generators import ProductHTMLGenerator, CategoryHTMLGenerator, CampaignHTMLGenerator
