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

# --- end config.py ---


class Graber:
    """Grabs product/category info for a given supplier."""

    def __init__(self, page:Page, supplier_prefix: str):
        self.config = Config(supplier_prefix=supplier_prefix)
        self.page = page

    async def grab_product_page(self, product_url: str, page: Optional[Page] = None, actual_fields: Optional[List[str]] = None) -> ProductFields:
        actual_fields = actual_fields or self.config.actual_fields
        page = page or self.page
        locator = self.config.product_locators
        f = ProductFields()

        try:
            await page.go_to(product_url)
        except Exception as e:
            logger.error(f'Failed to open product page: {product_url}', e)
            return f

        # Устанавливаем id_supplier в любом случае, если он определен в локаторах
        if hasattr(locator, 'id_supplier'):
            f.id_supplier = locator.id_supplier

        for field_name in actual_fields:
            # Пропускаем id_supplier, так как он уже установлен
            if field_name == 'id_supplier':
                continue
            
            try:
                # Убедимся, что локатор для поля существует
                if hasattr(locator, field_name):
                    setattr(f, field_name, await driver.execute_locator(page, getattr(locator, field_name)))
            except Exception as e:
                logger.error(f'Failed to extract {field_name} from {product_url}', e)

        return f

    @staticmethod
    def _normalize_url(url: str) -> str:
        """
        Приводит URL к стандартному виду https://...
        Поддерживаются форматы:
            //he.aliexpress.com/item/
            https://he.aliexpress.com/item/
            he.aliexpress.com/item/
        """
            
        if url.startswith('//'):
            return f'https:{url}'
        if not (url.startswith('http://') or url.startswith('https://')):
            return f'https://{url.lstrip("/")}'
        return url

    async def get_product_urls_from_category_page(self, category_url: str, locator: SimpleNamespace, page: Page) -> List[str]:
        await page.go_to(category_url)
        uri_list: list[str] = await driver.execute_locator(page, locator)

        # Нормализуем URL-ы, используя новый статический метод
        # и отфильтровываем пустые результаты, если такие будут
        normalized_urls = [self._normalize_url(uri) for uri in uri_list]
        return [url for url in normalized_urls if url]


    async def yield_scenario(self, scenario: SimpleNamespace, page) -> AsyncGenerator[ProductFields, None]:
        """Yield products for a given scenario."""
        try:
            product_urls = await self.get_product_urls_from_category_page(
                scenario.category_url,
                self.config.category_locators.product_links,
                page
            )

            if not product_urls:
                 logger.warning(f"No product URLs found for scenario: {scenario.name} on page {scenario.category_url}")


            for product_url in product_urls:
                product_fields = await self.grab_product_page(product_url, page)
                
                # Добавляем данные из сценария
                product_fields.id_category_default = scenario.id_category_default or '2'
                if getattr(scenario, 'presta_categories', None) and getattr(scenario.presta_categories, 'additional_categories', None):
                    product_fields.additional_categories = scenario.presta_categories.additional_categories

                yield product_fields

        except Exception as ex:
            logger.error(f"Ошибка при выполнении сценария '{scenario.name}'", exc_info=ex)
            # В случае ошибки генератор просто прекратит работу для этого сценария

    async def yield_all_scenarios(self, page) -> AsyncGenerator[ProductFields, None]:
        """
        Yield products for all scenarios defined in the config.
        Итерируется по атрибутам объекта SimpleNamespace, который содержит сценарии.
        """

        for scenario_file in get_filenames_from_directory(self.config.SCENARIOS_DIR, '*.json'):
            logger.info(f"Загружаем сценарии из файла: {scenario_file}")
            scenarios_from_file = j_loads_ns(self.config.SCENARIOS_DIR / scenario_file)

            for scenario_name, scenario in scenarios_from_file.__dict__.items():

                # ВАЖНО: Пропускаем служебные поля, которые не являются сценариями.
                # Лучше проверять наличие ключевого атрибута, например 'category_url'.
                if not hasattr(scenario, 'category_url'):
                    logger.debug(f"Пропускаем атрибут '{scenario_name}', так как это не сценарий.")
                    continue

                logger.info(f"Запускаем сценарий: '{scenario_name}'")

                async for product in self.yield_scenario(scenario, page):
                    yield product