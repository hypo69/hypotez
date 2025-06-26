## \file /src/suppliers/graber_via_pydoll.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
Модуль для получения информации о товарах и категориях поставщиков с использованием Pydoll.
===============================================================
```rst
.. module:: src.suppliers.graber_via_pydoll
```
"""

from pathlib import Path
from types import SimpleNamespace
from typing import Optional, List, AsyncGenerator
from dataclasses import dataclass, field
from pydoll.browser.chrome import Chrome
from pydoll.browser.page import Page

from header import __root__
from src import gs
from src.webdriver.driverless import use_pydoll as driver
from src.utils.file import get_filenames_from_directory
from src.utils.jjson import j_loads_ns
from src.endpoints.prestashop.product_fields import ProductFields
from src.logger.logger import logger


# --- start config.py ---
@dataclass
class Config:
    """Configuration for a supplier."""
    supplier_prefix: str
    supplier_alias: str = field(init=False)
    ENDPOINT: Path = field(init=False)
    SCENARIOS_DIR: Path = field(init=False)

    actual_fields: list[str] = field(default_factory=lambda: [
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

    @property
    def product_locators(self) -> SimpleNamespace:
        return j_loads_ns(self.ENDPOINT / 'locators' / 'product.json')

    @property
    def category_locators(self) -> SimpleNamespace:
        return j_loads_ns(self.ENDPOINT / 'locators' / 'category.json')

    @property
    def scenarios(self) -> List[SimpleNamespace]:
        result = j_loads_ns(self.SCENARIOS_DIR)
        return result if isinstance(result, list) else [result]
# --- end config.py ---


class Graber:
    """Grabs product/category info for a given supplier."""

    def __init__(self, supplier_prefix: str):
        self.config = Config(supplier_prefix)
        self.browser = Chrome()

    async def grab_product_page(self, product_url: str, page: Page, actual_fields: Optional[List[str]] = None) -> ProductFields:
        actual_fields = actual_fields or self.config.actual_fields
        locator = self.config.product_locators
        f = ProductFields()

        try:
            await page.go_to(product_url)
        except Exception as e:
            logger.error(f'Failed to open product page: {product_url}', e)
            return f

        f.id_supplier = locator.id_supplier

        for field_name in actual_fields:
            try:
                setattr(f, field_name, await driver.execute_locator(page, getattr(locator, field_name)))
            except Exception as e:
                logger.error(f'Failed to extract {field_name} from {product_url}', e)

        return f

    async def get_product_urls_from_category_page(self, category_url: str, locator: SimpleNamespace, page: Page) -> List[str]:
        await page.go_to(category_url)
        uri_list:list[str] = await driver.execute_locator(page, locator)

        def normalize_url(self,  product_url: str,) -> str:
            """
            Поддерживаются входные URL формата:
                //he.aliexpress.com/item/
                https://he.aliexpress.com/item/
                he.aliexpress.com/item/
            """

            if product_url.startswith('//'):
                url = f'https:{product_url}'
            elif product_url.startswith('http://') or product_url.startswith('https://'):
                url = product_url
            else:
                url = f'https://{product_url.lstrip("/")}'

            return url

        for i, uri in enumerate(uri_list):
            uri_list[i] = normalize_url(self, uri)

        return uri_list


    async def yield_scenario(self, scenario: SimpleNamespace) -> AsyncGenerator[ProductFields, None]:
        try:
            async with self.browser:
                await self.browser.start()
                page = await self.browser.get_page()

                product_urls = await self.get_product_urls_from_category_page(
                    scenario.category_url,
                    self.config.category_locators.product_links,
                    page
                )

                for product_url in product_urls:
                    product_fields = await self.grab_product_page(product_url, page)
                    product_fields.id_category_default = scenario.id_category_default or '2'
                    if getattr(scenario.presta_categories, 'additional_categories', None):
                        product_fields.additional_categories = scenario.presta_categories.additional_categories

                    yield product_fields

        except Exception as ex:
            logger.error("Ошибка при выполнении сценария", ex)

    async def yield_all_scenarios(self) -> AsyncGenerator[ProductFields, None]:
        for scenario in self.config.scenarios:
            async for product in self.yield_scenario(scenario):
                yield product
