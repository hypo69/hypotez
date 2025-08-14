# # \file /src/suppliers/suppliers_list/aliexpress/graber_via_pydoll.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3

"""ALIEXPRESS data collection module with the library of the library `pydoll`.
======================================================================================ward

rst```
.. Module :: src.suppliers.suppliers_list.aliexpress_com.graber_via_pydoll 
`` `"""
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
    """Grabs product/category info for Aliexpress supplier using pydoll."""
    def __init__(self):
        super().__init__('opel.de')
        
