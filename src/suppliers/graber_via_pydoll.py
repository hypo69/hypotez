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
from pydoll.browser.chrome import Chrome
from pydoll.browser.page import Page  # Предполагается, что Page - это тип драйвера

from header import __root__
from src import gs
#from src.webdriver.driverless import use_pydoll as driver # Этот импорт, похоже, не используется напрямую здесь
from src.endpoints.advertisement.facebook.scenarios import locator
from src.endpoints.prestashop.product_fields import ProductFields
from src.utils.convertors.ns import ns2dict
from src.utils.file import get_filenames_from_directory
from src.utils.jjson import j_loads_ns
from src.webdriver.driverless.use_pydoll import Driver  # Импортируем класс Driver из use_pydoll
from src.logger.logger import logger



# --- start config.py ---
@dataclass
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


class Graber:
    """Grabs product/category info for a given supplier."""
    config: Config = None
    driver: Driver = None

    def __init__(self, supplier_prefix: str, driver: Optional[Driver] = None):
        self.config = Config(supplier_prefix=supplier_prefix)
        self.driver = driver or Driver()

    async def grab_product_page(self, product_url: str, driver: Optional[Driver] = None, required_fields: Optional[List[str]] = None) -> ProductFields:
        """
        Grabs product information from a given URL.

        Args:
            product_url: The URL of the product page.
            page: An optional Page instance to use. If not provided,
                             the instance from __init__ (self.driver) will be used.
            required_fields: An optional list of fields to extract. If not provided,
                           defaults to self.config.required_fields.

        Returns:
            A ProductFields object containing the extracted information.
        """
        required_fields = required_fields or self.config.required_fields
        f = ProductFields()
        locator = self.config.product_locators
        driver = driver or self.driver
        if not driver:
            _m = "No driver instance provided or available in Graber instance"
            #raise ValueError(_m)
            logger.error(f'{_m}:{self.config.supplier_prefix}\n',None,)
            ...
            return f

        try:
            logger.info(f"Переход на страницу товара: {product_url}")
            await driver.page.go_to(product_url)
        except Exception as ex:
            logger.error(f'Failed to open product page: {product_url}', exc_info=ex) # Используется exc_info для стека
            return f # Возврат пустой объект в случае ошибки навигации

        # Установка `id_supplier` если он определен в локаторах
        # Проверка, что `locator` существует и имеет `атрибут id_supplier`
        if locator and hasattr(locator, 'id_supplier') and locator.id_supplier:
            f.id_supplier = locator.id_supplier
            logger.debug(f"\nУстановлен id_supplier: {f.id_supplier}\n")

        for field_name in required_fields:
            # Пропуск id_supplier, так как он уже установлен
            if field_name == 'id_supplier':
                continue

            if locator and hasattr(locator, field_name):
                _locator = getattr(locator, field_name)
                    
                extracted_value = await driver.execute_locator(_locator)
                        
                # Установка значение, только если оно не пустое (или по другой логике)
                if extracted_value is not None: # Можно добавить проверку на пустую строку, если нужно
                    setattr(f, field_name, extracted_value)
                    logger.debug(f"Поле '{field_name}' извлечено: '{extracted_value}'")
                else:
                    logger.warning(f"Локатор для поля '{field_name}' не найден в конфигурации поставщика {self.config.supplier_prefix}. Пропуск.")
                    ...

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
            logger.warning(f"Некоторые URL были отфильтрованы после нормализации для категории: {category_url}. Исходно: {len(normalized_urls)}, Валидных: {len(valid_urls)}")
            
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