## \file /src/suppliers/suppliers_list/ebay_com/graber_via_pydoll.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
.. module:: src.suppliers.suppliers_list.ebay_com.graber_via_pydoll
    :platform: Windows, Unix
    :synopsis: Module for collecting data from eBay using the `pydoll` library.

eBay Data Graber via Pydoll
=========================================================================================

This module provides a `Graber` class designed to extract product and category information from eBay
using the `pydoll` library, extending the base Graber functionality.

Example usage
-------------

```python
    from src.webdriver.selenium.driver import Driver
    from src.suppliers.suppliers_list.ebay_com.graber_via_pydoll import Graber

    # Initialize a WebDriver instance (e.g., Chrome)
    driver_instance = Driver(browser_name="Chrome")

    # Initialize the eBay Graber
    ebay_graber = Graber(driver=driver_instance, lang_index=0) # Assuming lang_index is needed

    # Now you can use ebay_graber methods to interact with eBay
    # For example, to grab product details from a URL:
    # product_data = ebay_graber.grab_product_details("https://www.ebay.com/itm/...")
    # print(product_data)

    # Don't forget to quit the driver when done
    # driver_instance.quit()
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: suppliers/suppliers_list/ebay_com/graber_via_pydoll.py
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
    """Grabs product/category info for eBay supplier using pydoll."""
    def __init__(self):
        super().__init__('ebay.com')
        
