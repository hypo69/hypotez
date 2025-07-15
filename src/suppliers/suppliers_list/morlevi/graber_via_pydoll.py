## \file /src/suppliers/suppliers_list/aliexpress/graber_via_pydoll.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для сбора данных о товарах с Aliexpress с изпользованием библиотеки `pydoll`.
=========================================================================================
rst```
.. module:: src.suppliers.suppliers_list.aliexpress.graber_via_pydoll 
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
from src.suppliers.graber_via_pydoll import Config as GraberConfig, Graber as GraberSupplier
# from src.utils.file import get_filenames_from_directory
from src.utils.jjson import j_loads_ns
# from src.utils.image import save_image_async, save_image_from_url_async
from src.utils.printer import pprint as print
from src.logger import logger

# --- start config.py ---
@dataclass(slots=True)
class Config:
    """Configuration for a supplier."""
    supplier_prefix: str 
    supplier_alias: str = field(init=False)
    ENDPOINT: Path = field(init=False)
    SCENARIOS_DIR: Path = field(init=False)

    required_fields: list[str] = field(default_factory=lambda: [
        'id_supplier',
        'name',
        'price',
        'reference',
        'description',
        'description_short',
        'default_image_url',
        'local_image_path',
    ])

    def __post_init__(self):
        self.supplier_alias = self.supplier_prefix.replace('.', '_').replace('-', '_')
        self.ENDPOINT = __root__ / 'src' / 'suppliers' / 'suppliers_list' / self.supplier_alias
        self.SCENARIOS_DIR = self.ENDPOINT / 'scenarios'
        ...

    @property
    def product_locators(self) -> SimpleNamespace:
        # Убедитесь, что этот путь верен и файл существует
        try:
            return j_loads_ns(self.ENDPOINT / 'locators' / 'product.json')
        except FileNotFoundError:
            logger.error(f"Файл локаторов товара не найден для поставщика {self.supplier_prefix}: {self.ENDPOINT / 'locators' / 'product.json'}")
            return SimpleNamespace() # Возврат пустой объект, чтобы избежать ошибок дальше

    @property
    def category_locators(self) -> SimpleNamespace:
        # Убедитесь, что этот путь верен и файл существует
        try:
            return j_loads_ns(self.ENDPOINT / 'locators' / 'category.json')
        except FileNotFoundError:
            logger.error(f"Файл локаторов категории не найден для поставщика {self.supplier_prefix}: {self.ENDPOINT / 'locators' / 'category.json'}")
            return SimpleNamespace() # Возврат пустой объект

# --- end config.py ---

# --- graber.py ---
@dataclass(slots=True)
class Graber(GraberSupplier):
    """! Grabs product/category info for Morlevi supplier using pydoll. """

    config: Config = field(init=False)

    def __post_init__(self):
        self.config = Config(supplier_prefix='morlevi')

        super().__post_init__(
            supplier_prefix=self.config.supplier_prefix,
            product_locator=self.config.product_locators,
            category_locator=self.config.category_locators,
            driver=self.driver,
            fields=self.fields
        )
