## \file /src/suppliers/suppliers_list/morlevi/graber_via_pydoll.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для сбора данных о товарах morlevi с изпользованием библиотеки `pydoll`.
=========================================================================================
rst```
.. module:: src.suppliers.suppliers_list.morlevi.graber_via_pydoll 
```
"""
from pathlib import Path
from types import SimpleNamespace
from typing import Optional, List
from dataclasses import dataclass, field

from header import __root__
from src import gs
from src.endpoints.prestashop.product_fields import ProductFields
# from src.webdriver.driverless import use_pydoll as driver
from src.suppliers.graber_via_pydoll import Graber as GraberSupplier
# from src.utils.file import get_filenames_from_directory
from src.utils.jjson import j_loads_ns
# from src.utils.image import save_image_async, save_image_from_url_async
from src.utils.printer import pprint as print
from src.logger import logger


# --- graber.py ---
@dataclass(slots=True)
class Graber(GraberSupplier):
    """! Grabs product/category info for Morlevi supplier using pydoll. """

    def __post_init__(self):
        
        super().__post_init__(
            supplier_prefix = self.config.supplier_prefix,
            driver = self.driver,
            product_fields = self.product_fields or self.config.required_fields,
        )
