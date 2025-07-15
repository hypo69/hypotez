# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
Модуль для получения информации о товарах и категориях поставщиков с использованием Pydoll.
===============================================================
```rst
.. module:: src.suppliers.graber_via_pydoll
"""

from pathlib import Path
from types import SimpleNamespace
from typing import Optional, List, AsyncGenerator
from dataclasses import dataclass, field
# from pydoll.browser.chrome import Chrome
from pydoll.browser.page import Page  

from header import __root__
from src import gs
#from src.webdriver.driverless import use_pydoll as driver # Этот импорт, похоже, не используется напрямую здесь
from src.endpoints.prestashop.product_fields import ProductFields
from src.suppliers.graber import Graber as GraberSupplier
from src.utils.convertors.ns import ns2dict
from src.utils.file import get_filenames_from_directory
from src.utils.jjson import j_loads_ns
from src.webdriver.driverless.use_pydoll import Driver 
from src.logger.logger import logger



# --- start config.py ---
@dataclass(slots=True)
class Config:
    """Configuration for a supplier."""


# --- end config.py ---

# --- graber.py ---

@dataclass(slots=True)
class Graber(GraberSupplier):
    """Grabs product/category info for a given supplier."""
    supplier_prefix: str
    config: Config = field(init=False)
                                      

    def __post_init__(self, product_locator:SimpleNamespace):
        """ """
        self.config = Config(supplier_prefix=self.supplier_prefix)
        super().__init__(
            supplier_prefix = self.supplier_prefix,  
            driver = self.driver, 
            product_fields = self.product_fields,
            lang_index = self.lang_index or 1
            )

    async def grab_product_page(self, driver: Driver, product_url: str, required_fields: Optional[List[str]] = None, ) -> ProductFields:
        """
        Grabs product information from a given URL.

        Args:
            product_url: The URL of the product page.
            driver: An optional Driver instance to use. If not provided,
                    the instance from __init__ (self.driver) will be used.
            required_fields: An optional list of fields to extract. If not provided,
                           defaults to self.config.required_fields.

        Returns:
            A ProductFields object containing the extracted information.
        """
        f: ProductFields = ProductFields()
        required_fields: list = required_fields or self.config.required_fields
        product_locators: SimpleNamespace = self.config.product_locators

        
        try:
            logger.info(f"Переход на страницу товара: {product_url}", text_color = "light_gray", bg_color = "black" )
            await driver.get_url(product_url)
        except Exception as ex:
            logger.error(f'Failed to open product page: {product_url}\n', ex, True)
            return f # Возврат пустой объект в случае ошибки навигации

        # Установка `id_supplier` Он определен в локаторе `id_supplier.attribute` и содержит значение id поставщика из Prestashop.
        # Проверка, что `product_locators` существует и имеет `атрибут id_supplier`
        if product_locators and hasattr(product_locators, 'id_supplier') and product_locators.id_supplier:
            f.id_supplier = product_locators.id_supplier.attribute # <- передача параметра через локатор
            logger.info(f"Установлен id_supplier: {f.id_supplier}" , None, False, text_color = "light_gray", bg_color = "black")

        for field_name in required_fields:
            # Пропуск id_supplier, так как он уже установлен
            if field_name == 'id_supplier':
                continue

                await function(self, field_name)


            if product_locators and hasattr(product_locators, field_name):
                locator = getattr(product_locators, field_name)
                extracted_value = await driver.execute_locator(locator)
                        
                # Установка значение, только если оно не пустое (или по другой логике)
                if extracted_value: # Можно добавить проверку на пустую строку, если нужно
                    setattr(f, field_name, extracted_value)
                    logger.info(f"""В поле '{field_name}' установлено значение: {extracted_value}""", None, False, text_color = "light_gray", bg_color = "black")

        return f

    @staticmethod
    def _normalize_url(url: str) -> str:
        """
        Приводит URL к стандартному виду https://...
        Поддерживаются форматы:
            //he.aliexpress_com.com/item/
            https://he.aliexpress_com.com/item/
            he.aliexpress_com.com/item/
        """
            
        if url.startswith('//'):
            return f'https:{url}'
        if not (url.startswith('http://') or url.startswith('https://')):
            return f'https://{url.lstrip("/")}'
        return url

    async def get_product_urls_from_category_page(self, category_url: str, locator: SimpleNamespace, page: Page) -> List[str]:
        if not page:
             logger.error("get_product_urls_from_category_page: передан пустой page (driver). Невозможно продолжить.")
             return []

        await page.go_to(category_url)
        # Проверка, что локатор существует и имеет атрибут product_links
        if not locator or not hasattr(locator, 'product_links'):
            logger.warning(f"Локатор 'product_links' не найден в category_locators для категории: {category_url}")
            return []

        uri_list: list[str] = await page.execute_locator(locator.product_links) # Вызываем на объекте page

        # Нормализуем URL-ы, используя новый статический метод
        # и отфильтровываем пустые результаты, если такие будут
        normalized_urls = [self._normalize_url(uri) for uri in uri_list if uri] # Добавлена проверка на None/пустую строку
        
        # Фильтруем на случай, если normalization сломается или вернет некорректный URL
        valid_urls = [url for url in normalized_urls if url.startswith('https://')] 
        
        if len(valid_urls) != len(normalized_urls):
            logger.warning(f"Некоторые URL были отфильтрованы после нормализации для категории: {category_url}.\n Исходно: {len(normalized_urls)}, \nВалидных: {len(valid_urls)}")
            
        return valid_urls


    async def yield_scenario(self, scenario: SimpleNamespace, page: Page) -> AsyncGenerator[ProductFields, None]:
        """Yield products for a given scenario."""
        if not page:
             logger.error("yield_scenario: передан пустой page (driver). Невозможно продолжить для сценария.")
             return # Завершаем генератор для этого сценария

        try:
            # Проверка, что scenario существует и имеет category_url
            if not scenario or not hasattr(scenario, 'category_url'):
                logger.warning("Пропущен некорректный сценарий (отсутствует category_url).")
                return

            # Получаем локаторы для категорий
            category_locators = self.config.category_locators
            if not category_locators or not hasattr(category_locators, 'product_links'):
                logger.warning(f"Локаторы категорий не настроены или отсутствует 'product_links' для сценария '{scenario.name}'. Пропуск.")
                return

            product_urls = await self.get_product_urls_from_category_page(
                scenario.category_url,
                category_locators, # Передаем весь объект локаторов, а get_product_urls_from_category_page сам выберет product_links
                page
            )

            if not product_urls:
                 logger.warning(f"Нет URL товаров, найденных для сценария: {scenario.name} на странице {scenario.category_url}")
                 return # Нет товаров для обработки в этом сценарии

            logger.info(f"Найдено {len(product_urls)} товаров для сценария '{scenario.name}'")

            for product_url in product_urls:
                logger.info(f"Обработка URL товара: {product_url}")
                # Передаем экземпляр page напрямую как driver_instance
                product_fields = await self.grab_product_page(product_url, driver_instance=page) 
                
                # Добавляем данные из сценария
                # Используется getattr с default, чтобы избежать ошибок, если атрибут отсутствует
                product_fields.id_category_default = getattr(scenario, 'id_category_default', '2') # Default value '2' if not found
                
                # Обработка дополнительных категорий
                if hasattr(scenario, 'presta_categories') and scenario.presta_categories:
                    if hasattr(scenario.presta_categories, 'additional_categories') and scenario.presta_categories.additional_categories:
                        product_fields.additional_categories = scenario.presta_categories.additional_categories

                yield product_fields

        except Exception as ex:
            # Логгируем исключение и завершаем генератор для этого сценария
            logger.error(f"Ошибка при выполнении сценария '{scenario.name}' (URL: {scenario.category_url if scenario and hasattr(scenario, 'category_url') else 'N/A'})", exc_info=ex)


    async def yield_all_scenarios(self, page: Page) -> AsyncGenerator[ProductFields, None]:
        """
        Yield products for all scenarios defined in the config.
        Итерируется по атрибутам объекта SimpleNamespace, который содержит сценарии.
        """
        if not page:
            logger.error("yield_all_scenarios: передан пустой page (driver). Невозможно продолжить.")
            return # Завершаем генератор

        for scenario_file in get_filenames_from_directory(self.config.SCENARIOS_DIR, '*.json'):
            logger.info(f"Загружаем сценарии из файла: {scenario_file}")
            try:
                scenarios_from_file = j_loads_ns(self.config.SCENARIOS_DIR / scenario_file)
            except Exception as ex:
                logger.error(f"Не удалось загрузить JSON файл сценариев: {scenario_file}", exc_info=ex)
                continue # Переходим к следующему файлу

            # Убеждаемся, что scenarios_from_file это объект с атрибутами
            if not isinstance(scenarios_from_file, SimpleNamespace) and not hasattr(scenarios_from_file, '__dict__'):
                logger.warning(f"Файл сценариев '{scenario_file}' не содержит ожидаемых данных (SimpleNamespace). Пропуск.")
                continue

            for scenario_name, scenario in scenarios_from_file.__dict__.items():

                # Проверка, что это действительно объект сценария и он имеет category_url
                if not isinstance(scenario, SimpleNamespace) or not hasattr(scenario, 'category_url'):
                    logger.debug(f"Пропуск атрибут '{scenario_name}' из файла '{scenario_file}', так как это не является валидным сценарием.")
                    continue

                logger.info(f"Запуск сценария: '{scenario_name}' из файла '{scenario_file}'")

                # Передаем экземпляр page как драйвер для каждого сценария
                async for product in self.yield_scenario(scenario, page):
                    yield product