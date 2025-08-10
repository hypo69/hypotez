## \file /src/suppliers/suppliers_list/chat_gpt/graber_via_pydoll.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
.. module:: src.suppliers.suppliers_list.chat_gpt.graber_via_pydoll
    :platform: Windows, Unix
    :synopsis: Module for collecting data from ChatGPT using the `pydoll` library.

ChatGPT Data Graber via Pydoll
=========================================================================================

This module provides a `Graber` class designed to extract data from ChatGPT
using the `pydoll` library, extending the base Graber functionality.

Example usage
-------------

```python
    from src.webdriver.selenium.driver import Driver
    from src.suppliers.suppliers_list.chat_gpt.graber_via_pydoll import Graber

    # Initialize a WebDriver instance (e.g., Chrome)
    driver_instance = Driver(browser_name="Chrome")

    # Initialize the ChatGPT Graber
    chat_gpt_graber = Graber(driver=driver_instance, lang_index=0) # Assuming lang_index is needed

    # Now you can use chat_gpt_graber methods to interact with ChatGPT
    # For example, to grab conversation data:
    # conversation_data = chat_gpt_graber.grab_conversation("https://chat.openai.com/chat/...")
    # print(conversation_data)

    # Don't forget to quit the driver when done
    # driver_instance.quit()
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: suppliers/suppliers_list/chat_gpt/graber_via_pydoll.py
"""
# from pathlib import Path
# from types import SimpleNamespace
# from typing import Optional, List
# from dataclasses import dataclass, field

# from header import __root__
# from src import gs
# from src.endpoints.prestashop.product_fields import ProductFields
# from src.webdriver.driverless import use_pydoll as driver
from src.suppliers.graber_via_pydoll import Config as GraberConfig, Graber as GraberSupplier 
# from src.utils.file import get_filenames_from_directory
# from src.utils.jjson import j_loads_ns
# from src.utils.image import save_image_async, save_image_from_url_async
# from src.logger import logger




class Graber(GraberSupplier):
    """Grabs product/category info for ChatGPT supplier using pydoll."""
    def __init__(self, supplier_prefix:str = 'chat_gpt'):
        super().__init__(supplier_prefix)
        
