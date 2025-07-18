## \file /src/suppliers/graber.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
 Модуль грабера. Собирает информацию с вестраницы товара
 =========================================================
 Базовый класс сбора данных со старницы HTML поставщиков.
    Целевые поля страницы (`название`,`описание`,`спецификация`,`артикул`,`цена`,...) собирает вебдрйвер (class: [`Driver`](../webdriver))
    Местополжение поля определяется его локатором. Локаторы хранятся в словарях JSON в директории `locators` каждого поставщика.
    ([подробно о локаторах](locators.ru.md))
     Таблица поставщиков:
              https://docs.google.com/spreadsheets/d/14f0PyQa32pur-sW2MBvA5faIVghnsA0hWClYoKpkFBQ/edit?gid=1778506526#gid=1778506526

 

## Для нестендартной обработки полей товара просто переопределите функцию в своем классе.
Пример:
```python
s = `suppler_prefix`
from src.suppliers imoprt Graber
locator = j_loads(gs.path.src.suppliers / f{s} / 'locators' / 'product.json`)

class G(Graber):

    @close_pop_up()
    async def name(self, value:Optional[Any] = None) -> bool:
        self.product_fields.name = <Ваша реализация>
        )
    ```
```rst
.. module:: src.suppliers 
``` 

Список полей: https://github.com/hypo69/hypotez/blob/master/src/endpoints/prestashop/product_fields/fields_list.txt
Модуль `graber`: https://github.com/hypo69/hypotez/blob/master/docs/ru/src/suppliers/graber.py.md
Локатор https://github.com/hypo69/hypotez/blob/master/docs/ru/src/suppliers/locator.md
Подробно о локаторе https://github.com/hypo69/hypotez/blob/master/src/webdriver/locator.md

"""


import datetime
import os
import sys
import asyncio
import re
import importlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Generator, List, Optional, Dict, Any
from types import SimpleNamespace
from typing import Callable
# from langdetect import detect
from functools import wraps

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.webdriver.driverless.use_pydoll import Driver

import header
from header import __root__
from src import gs
# from src.webdriver.driver import Driver
# from src.webdriver.firefox import Firefox
from src.endpoints.prestashop.product_fields import ProductFields
# from src.endpoints.prestashop.category_async import PrestaCategoryAsync
# from src.suppliers.scenario.scenario_executor import run_scenario as _runscenario, run_scenarios as _runscenarios, run_scenario_file as _run_scenario_file, run_scenario_files as _run_scenario_files
from src.endpoints.prestashop.product import PrestaProduct
from src.utils.jjson import j_loads, j_loads_ns, j_dumps
from src.utils.image import save_image, save_image_async, save_image_from_url_async
from src.utils.file import read_text_file, get_directory_names, get_filenames_from_directory, read_text_file_generator, recursively_get_file_path, save_text_file
from src.utils.string.normalizer import( normalize_string, 
                                        normalize_int, 
                                        normalize_float, 
                                        normalize_boolean, 
                                        normalize_sql_date, 
                                        normalize_sku )
from src.logger.exceptions import ExecuteLocatorException
from src.utils.printer import pprint as print
from src.logger.logger import logger


# Определение декоратора для закрытия всплывающих окон
# В каждом отдельном поставщике (`Supplier`) декоратор может использоваться в индивидуальных целях
# Общее название декоратора `@close_pop_up` можно изменить 
# Если декоратор не используется в поставщике - Установи `Config.locator_for_decorator = None` 

# --- decorator.py ---

def close_pop_up() -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            instance = args[0]
            
            # Получаем локатор напрямую из экземпляра
            locator = instance.locator_for_decorator
            
            if locator:
                try:
                    await instance.driver.execute_locator(locator)
                except Exception as ex:
                    print(f'Ошибка выполнения локатора в декораторе: {ex}')
                finally:
                    # Очищаем локатор в экземпляре, а не в глобальном Config
                    instance.locator_for_decorator = None 

            return await func(*args, **kwargs)
        return wrapper
    return decorator

# --- decorator.py end ---

# --- config.py ---

@dataclass(slots=True, kw_only=True)
class Config:
    """! Класс конфигурации поставщика."""

    supplier_prefix: str
    locator_for_decorator: Optional[SimpleNamespace] = None

    ENDPOINT: Path = field(init=False)
    SCENARIOS_DIR: Path = field(init=False)

    required_fields: list[str] = field(default_factory=lambda: [
        'id_supplier', 'name', 'price', 'reference', 'description',
        'description_short', 'specification', 'default_image_url', 'local_image_path',
    ])

    def __post_init__(self):
        supplier_alias = self.supplier_prefix.replace('.', '_').replace('-', '_')
        self.ENDPOINT = __root__ / 'src' / 'suppliers' / 'suppliers_list' / supplier_alias
        self.SCENARIOS_DIR = self.ENDPOINT / 'scenarios'


    @property
    def product_locators(self) -> SimpleNamespace:
        try:
            return j_loads_ns(self.ENDPOINT / 'locators' / 'product.json')
        except FileNotFoundError:
            logger.error(f"Локаторы товара не найдены: {self.ENDPOINT / 'locators' / 'product.json'}")
            return SimpleNamespace()

    @property
    def category_locators(self) -> SimpleNamespace:
        try:
            return j_loads_ns(self.ENDPOINT / 'locators' / 'category.json')
        except FileNotFoundError:
            logger.error(f"Локаторы категории не найдены: {self.ENDPOINT / 'locators' / 'category.json'}")
            return SimpleNamespace()

# --- config.py end ---

# --- graber.py ---
@dataclass(slots=True, kw_only=True)
class GraberBase:
    """! Базовый класс грабера поставщика.

    Attrs:
        supplier_prefix (str): Префикс поставщика.
        driver (Driver): Экземпляр драйвера браузера.
        locator_for_decorator (Optional[SimpleNamespace]): Локаторы для использования в декораторах.
        lang_index (int): Индекс языка.
        config (Config): Конфигурация, загружаемая по префиксу.
        product_locator (SimpleNamespace): Локаторы для товара.
        product_fields (ProductFields): Поля, собираемые с карточки товара.
    """

    supplier_prefix: str
    driver: 'Driver'
    locator_for_decorator: Optional[SimpleNamespace] = None
    lang_index: int = 1

    config: 'Config' = field(init=False)
    product_locator: SimpleNamespace = field(init=False)
    product_fields: ProductFields = field(default_factory=lambda: ProductFields())

    def __post_init__(self):
        self.config = Config(supplier_prefix=self.supplier_prefix)
        #self.config.locator_for_decorator = self.locator_for_decorator
        self.product_locator = self.config.product_locators


    def grab_page(self, required_fields, page_url, *args, **kwargs) -> ProductFields | bool:
        return asyncio.run(self.grab_page_async(required_fields, page_url, *args, **kwargs))

    async def grab_page_async(
        self,
        required_fields: Optional[list] = None,
        page_url: Optional[str] = '',
        *args,
        **kwargs
    ) -> Optional[ProductFields]:

        async def call_field_func(field_name: str) -> None:
            function = getattr(self, field_name, None)
            if function:
                try:
                    await function(kwargs.get(field_name, ''))
                except Exception as ex:
                    logger.error(f"Ошибка при вызове функции '{field_name}'", ex, exc_info=True)

        try:
            required_fields = required_fields or self.config.required_fields
            if page_url:
                await asyncio.to_thread(self.driver.get_url, page_url)

            await asyncio.gather(*[
                call_field_func(field_name)
                for field_name in required_fields
                if hasattr(self, field_name)
            ])

            return self.product_fields

        except Exception as ex:
            logger.error("Ошибка в `grab_page_async`", ex, exc_info=True)
            return None


    
    def yield_scenarios_for_supplier(self, supplier_prefix: str, input_scenarios: Optional[List[Dict[str, Any]] | Dict[str, Any]] = None) -> Generator[Dict[str, Any], None, None]:
        """
        Генератор, который выдает (yields) словари сценариев для поставщика.

        Сначала обрабатывает сценарии, переданные в `input_scenarios`.
        Если `input_scenarios` пуст или None, ищет и загружает .json файлы
        из директории сценариев поставщика.

        Args:
            supplier_prefix (str): Префикс (идентификатор) поставщика.
            input_scenarios (Optional[List[Dict] | Dict]): Непосредственно переданные
                сценарии (один словарь или список словарей).

        Yields:
            Generator[Dict[str, Any], None, None]: Генератор, возвращающий
                словари сценариев по одному.
        """
        processed_input = False # Флаг, указывающий, обработали ли мы входные данные

        # 1. Обработка напрямую переданных сценариев
        if input_scenarios:
            scenario_list: List[Dict[str, Any]] = []
            if isinstance(input_scenarios, list):
                # Проверка, что все элементы списка - словари
                if all(isinstance(item, dict) for item in input_scenarios):
                    scenario_list = input_scenarios
                else:
                    logger.warning(f"Не все элементы в списке input_scenarios для '{supplier_prefix}' являются словарями.")
            elif isinstance(input_scenarios, dict):
                scenario_list = [input_scenarios]
            else:
                logger.warning(f"Неверный тип для input_scenarios для '{supplier_prefix}': {type(input_scenarios)}. Ожидался dict или list[dict].")

            if scenario_list: # Если после проверок список не пуст
                logger.info(f"Обработка {len(scenario_list)} сценариев, переданных напрямую для '{supplier_prefix}'.")
                for scenario_dict in scenario_list:
                     yield scenario_dict
                     processed_input = True # Отмечаем, что обработали входные данные

        # 2. Загрузка из файлов, если входные данные не были обработаны
        if not processed_input:
            scenarios_dir: Path = __root__ / 'src' / 'suppliers' / 'suppliers_list' / supplier_prefix / 'scenarios'
            logger.info(f"Входные сценарии не предоставлены/обработаны для '{supplier_prefix}', поиск в: {scenarios_dir}")
            try:
                # Используется вашу функцию для поиска файлов
                scenarios_files: List[Path | str] = recursively_get_file_path(scenarios_dir, '.json')

                if not scenarios_files:
                    logger.warning(f"Не найдено '.json' файлов сценариев в директории: {scenarios_dir}")
                    return # Завершаем генератор, если файлов нет

                logger.info(f"Найдено {len(scenarios_files)} файлов сценариев для '{supplier_prefix}'.")
                for scenario_file_path in scenarios_files:
                    try:
                        # Провера, что это файл
                        if not Path(scenario_file_path).is_file():
                             logger.warning(f"Пропуск не-файлового пути: {scenario_file_path}")
                             continue

                        # Загружаем JSON
                        loaded_scenario: Optional[Dict[str, Any]] = j_loads(scenario_file_path)

                        # Проверка успешность загрузки и тип
                        if loaded_scenario is not None and isinstance(loaded_scenario, dict):
                            logger.debug(f"Yield сценария из файла: {scenario_file_path}")
                            yield loaded_scenario # Отдаем загруженный словарь сценария
                        else:
                            logger.error(f"Не удалось загрузить или результат не словарь: {scenario_file_path}")

                    except Exception as file_load_ex:
                        logger.error(f"Ошибка при обработке файла сценария {scenario_file_path}", file_load_ex, exc_info=True)

            except FileNotFoundError:
                logger.error(f"Директория сценариев не найдена: {scenarios_dir}")
            except Exception as e:
                logger.error(f"Ошибка при поиске файлов сценариев для '{supplier_prefix}'", e, exc_info=True)

    async def process_supplier_scenarios_async(self, input_scenarios:list = [], id_lang:Optional[int]=1) -> bool:
        """
        Пример метода, который использует генератор yield_scenarios_for_supplier
        и вызывает run_scenario для каждого сценария.
        """
        all_results = []
        try:
            # Получаем генератор
            scenario_generator = self.yield_scenarios_for_supplier(input_scenarios)

            # Итерируем по сценариям, которые выдает генератор
            for scenarios in scenario_generator:
                # logger.info(f"Запуск сценария для '{supplier_prefix}'...")

                result = await self.process_scenarios(self.supplier_prefix, scenarios['scenarios'] if hasattr(scenarios, 'scenarios') else scenarios, id_lang )
                all_results.append(result) # Собираем результаты (опционально)

            logger.info(f"Все сценарии для '{self.supplier_prefix}' обработаны.")
            return all_results # Возврат собранные результаты

        except Exception as ex:
            logger.error(f"Ошибка при обработке сценариев для '{self.supplier_prefix}'", ex, exc_info=True)
            return None # Или другое обозначение ошибки


    async def process_scenarios(self, input_scenarios: List[Dict[str, Any]] | Dict[str, Any], id_lang:Optional[int]=1) -> Optional[List[Any]]:
        """
        Выполняет один или несколько сценариев для указанного поставщика.

        Args:
            supplier_prefix (str): Префикс (идентификатор) поставщика.
            input_scenarios (List[Dict[str, Any]] | Dict[str, Any]):
                Данные сценариев: либо список словарей сценариев,
                либо словарь вида {'scenarios': {'name': dict, ...}}.

        Returns:
            Optional[List[Any]]: Список результатов выполнения каждого сценария
                                 (например, списки обработанных URL товаров)
                                 или None в случае критической ошибки.
        """
        actual_scenarios_to_process: List[Dict[str, Any]] = []
        supplier_prefix = self.supplier_prefix
        # 1. Нормализация входных данных -> actual_scenarios_to_process (список словарей сценариев)
        if isinstance(input_scenarios, list):
            # Вход - список: валидация содержимого
            if all(isinstance(item, dict) for item in input_scenarios):
                actual_scenarios_to_process = input_scenarios
            else:
                logger.error(f"""Входной список для '{supplier_prefix}' содержит не-словари.
                {print(input_scenarios)}
                """, None, False)
                ...
                return None # Возврат `None` при некорректном вводе
        elif isinstance(input_scenarios, dict):
            # Вход - словарь: проверка структуры {'scenarios': {name: dict, ...}}
            if 'scenarios' in input_scenarios and isinstance(input_scenarios.get('scenarios'), dict):
                inner_scenarios_dict = input_scenarios['scenarios']
                # Проверка, что все значения во вложенном словаре - тоже словари
                if all(isinstance(item, dict) for item in inner_scenarios_dict.values()):
                    # Извлечение словарей сценариев из значений вложенного словаря
                    actual_scenarios_to_process = list(inner_scenarios_dict.values())
                    logger.debug(f"Извлечено {len(actual_scenarios_to_process)} сценариев из ключа 'scenarios' для '{supplier_prefix}'.")
                else:
                     logger.error(f"Внутренний словарь 'scenarios' для '{supplier_prefix}' содержит не-словари в значениях.", None, False)
                     ...
                     return None # Возврат `None` при некорректной структуре
            else:
                # Если это словарь, но не ожидаемой структуры, считаем ошибкой
                logger.error(f"Входной словарь для '{supplier_prefix}' не имеет структуры {{'scenarios': {{...}}}}.")
                ...
                # Если нужно обработать одиночный словарь как один сценарий, логика была бы здесь:
                # actual_scenarios_to_process = [input_scenarios]
                return None # Возврат `None` при некорректной структуре
        else:
            logger.error(f"Неверный тип входных данных для '{supplier_prefix}': {type(input_scenarios)}. Ожидался list или dict.")
            ...
            return None # Возврат `None` при некорректном типе

        # Проверка, есть ли сценарии после нормализации
        if not actual_scenarios_to_process:
            logger.warning(f"Нет сценариев для обработки для '{supplier_prefix}' после нормализации.")
            ...
            return [] # Возврат пустого списка

        # 2. Динамический импорт (вынесен до цикла)
        try:
            module_path_str: str = f'src.suppliers.suppliers_list.{supplier_prefix}.scenario'
            scenario_module = importlib.import_module(module_path_str)
            if not hasattr(scenario_module, 'get_list_products_in_category'):
                logger.error(f"Функция 'get_list_products_in_category' не найдена в {module_path_str}")
                ...
                return None
            get_list_func: Callable = getattr(scenario_module, 'get_list_products_in_category')
            if not callable(get_list_func):
                 logger.error(f"'get_list_products_in_category' в {module_path_str} не является функцией")
                 ...
                 return None
        except (ModuleNotFoundError, ImportError, Exception) as import_err:
            logger.error(f"Ошибка импорта модуля/функции сценария для '{supplier_prefix}'", import_err, exc_info=True)
            ...
            return None

        # --- Основной цикл обработки сценариев ---
        all_results: List[Any] = []
        d = self.driver # Предполагается, что self.driver инициализирован

        # Итерация по подготовленному списку словарей сценариев
        for scenario_data in actual_scenarios_to_process:
            # --- Начало тела внешнего цикла ---
            # 3. Получение URL из текущего словаря сценария
            if not isinstance(scenario_data, dict): # Дополнительная проверка типа
                logger.warning(f"Пропуск не-словаря в списке сценариев: {scenario_data}")
                ...
                continue

            scenario_url: Optional[str] = scenario_data.get('url')
            if not scenario_url:
                logger.warning(f"Сценарий для '{supplier_prefix}' не содержит ключ 'url'. Пропуск.")
                ...
                continue

            logger.info(f"Обработка сценария для '{supplier_prefix}'. URL: {scenario_url}")

            # 4. Переход по URL сценария
            if not d.get_url(scenario_url):
                logger.error(f"Не удалось перейти по URL сценария: {scenario_url}", None, False)
                ...
                continue

            # 5. Вызов функции для получения списка товаров
            list_products_in_category: Optional[List[str]] = None
            try:
                list_products_in_category = await get_list_func(d, self.category_locator)
            except Exception as func_ex:
                logger.error(f"Ошибка при выполнении get_list_products_in_category для URL {scenario_url}", func_ex, exc_info=True)
                ...
                continue

            # 6. Проверка результата функции
            if list_products_in_category is None:
                logger.warning(f'Функция get_list_products_in_category вернула None для URL {scenario_url}.')
                ...
                continue
            if not isinstance(list_products_in_category, list):
                 logger.error(f'Функция get_list_products_in_category вернула не список: {type(list_products_in_category)} для URL {scenario_url}')
                 ...
                 continue
            if not list_products_in_category:
                logger.warning(f'Нет ссылок на товары для URL {scenario_url}. Возможно, пустая категория.')
                ...
                continue

            for product_url in list_products_in_category:
                # --- Начало тела внутреннего цикла ---
                if not isinstance(product_url, str) or not product_url:
                     logger.warning(f"Некорректный URL товара получен: {product_url}. Пропуск.")
                     ...
                     continue

                if not d.get_url(product_url):
                    logger.error(f'Ошибка навигации на страницу товара: {product_url}')
                    ...
                    continue


                f: Optional[ProductFields] = await self.grab_page_async(*self.required_fields, id_lang=id_lang)
                if not f:
                    logger.error(f'Не удалось собрать поля товара со страницы {product_url}')
                    ...
                    continue

                try:
                    f.id_category_default = scenario_data.get('presta_categories')['default_category']
                    f.additional_category_append(f.id_category_default)
                    additional_categories = scenario_data.get('presta_categories')['additional_categories']
                    if additional_categories:
                        for category in additional_categories:
                            if category:
                                f.additional_category_append(category)
                except Exception as ex:
                    logger.error(f'Ошибка добавления дополнительных категорий{print(f)}')
                    ...
                except Exception as ex:
                    logger.error(f'Не удалось сохранить данные\n {print(f)}\n с {product_url}', ex, exc_info=True)
                    ...
                product: PrestaProduct = PrestaProduct()
                product.add_new_product(f)
                all_results.append(f)
                # --- Конец тела внутреннего цикла ---
            
            # --- Конец тела внешнего цикла ---

        # 8. Возврат агрегированных результатов
        logger.info(f"Обработка всех сценариев для '{supplier_prefix}' завершена.")
        return all_results
        # --- Конец функции ---


    @close_pop_up()
    async def additional_shipping_cost(self, value:Optional[Any] = None) -> bool:
        """Fetch and set additional shipping cost.
        Args:
        value (Any): это значение можно передать в словаре kwargs чеез ключ {additional_shipping_cost = `value`} при определении класса
        если `value` был передан - его значение подставляется в поле `ProductFields.additional_shipping_cost
        """
        try:           
            self.product_fields.additional_shipping_cost = normalize_string(value or  await self.driver.execute_locator(self.product_locator.additional_shipping_cost) or '')
            return True
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `additional_shipping_cost`", ex)
            ...
            return


    @close_pop_up()
    async def delivery_in_stock(self, value:Optional[str] = None) -> bool:
        """Fetch and set delivery in stock status.
        
        Args:
        value (str): это значение можно передать в словаре kwargs через ключ {delivery_in_stock = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.delivery_in_stock`.
        """
        try:            
            self.product_fields.delivery_in_stock = normalize_string( value or  await self.driver.execute_locator(self.product_locator.delivery_in_stock) or '' )
            return True
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `delivery_in_stock`", ex)
            ...
            return


    @close_pop_up()
    async def active(self, value:bool = True) -> bool:
        """Fetch and set active status.
        
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {active = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.active`.
        Принимаемое значениеЬ 1/0
        """
        try:            
            self.product_fields.active = normalize_int( value or  await self.driver.execute_locator(self.product_locator.active) or 1)
            return True
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `active`", ex)
            ...
            return

    @close_pop_up()
    async def additional_delivery_times(self, value:Optional[str] = None) -> bool:
        """Fetch and set additional delivery times.
        
        Args:
        value (str): это значение можно передать в словаре kwargs через ключ {additional_delivery_times = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.additional_delivery_times`.
        """
        try:            
            self.product_fields.additional_delivery_times = value or  await self.driver.execute_locator(self.product_locator.additional_delivery_times) or ''
            return True
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `additional_delivery_times`", ex)
            ...
            return


    @close_pop_up()
    async def advanced_stock_management(self, value:Optional[Any] = None) -> bool:
        """ -** DEPRECATED FIELD! **- Не используется в престашоп 1.7.8 и выше.
        Args:
            value (Any): это значение можно передать в словаре kwargs через ключ {advanced_stock_management = `value`} при определении класса.
            Если `value` был передан, его значение подставляется в поле `ProductFields.advanced_stock_management`.
        """
        return False


    @close_pop_up()
    async def affiliate_short_link(self, value:Optional[str] = None) -> bool:
        """Fetch and set affiliate short link.
        
        Args:
        value (str): это значение можно передать в словаре kwargs через ключ {affiliate_short_link = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.affiliate_short_link`.
        """
        try:            
            self.product_fields.affiliate_short_link = value or  await self.driver.execute_locator(self.product_locator.affiliate_short_link) or ''
            
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `affiliate_short_link`", ex)
            ...
            return
        return True

    @close_pop_up()
    async def affiliate_summary(self, value:Optional[str] = None) -> bool:
        """Fetch and set affiliate summary.
        
        Args:
        value (str): это значение можно передать в словаре kwargs через ключ {affiliate_summary = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.affiliate_summary`.
        """
        try:            
            self.product_fields.affiliate_summary = normalize_string( value or  await self.driver.execute_locator(self.product_locator.affiliate_summary) or '' )
            return True
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `affiliate_summary`", ex)
            ...
            return


    @close_pop_up()
    async def affiliate_summary_2(self, value:Optional[Any] = None) -> bool:
        """Fetch and set affiliate summary 2.
        
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {affiliate_summary_2 = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.affiliate_summary_2`.
        """
        try:            
            self.product_fields.affiliate_summary_2 = normalize_string(value or  await self.driver.execute_locator(self.product_locator.affiliate_summary_2) or '')
            return True
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `affiliate_summary_2`", ex)
            ...
            return


    @close_pop_up()
    async def affiliate_text(self, value:Optional[str] = None) -> bool:
        """Fetch and set affiliate text.
        
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {affiliate_text = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.affiliate_text`.
        """
        try:            
            self.product_fields.affiliate_text = normalize_string( value or  await self.driver.execute_locator(self.product_locator.affiliate_text) or '')
            return True
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `affiliate_text`", ex)
            ...
            return
        
    @close_pop_up()
    async def affiliate_image_large(self, value:Optional[str] = None) -> bool:
        """Fetch and set affiliate large image.
        
        Args:
        value (str): это значение можно передать в словаре kwargs через ключ {affiliate_image_large = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.affiliate_image_large`.
        """
        try:            
            self.product_fields.affiliate_image_large  = value or  await self.driver.execute_locator(self.product_locator.affiliate_image_large) or ''
            return True
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `affiliate_image_large`", ex)
            ...
            return

    @close_pop_up()
    async def affiliate_image_medium(self, value:Optional[str] = None) -> bool:
        """Fetch and set affiliate medium image.
        
        Args:
        value (str): это значение можно передать в словаре kwargs через ключ {affiliate_image_medium = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.affiliate_image_medium`.
        """
        try:            
            self.product_fields.affiliate_image_medium = value or  await self.driver.execute_locator(self.product_locator.affiliate_image_medium) or ''
            return True
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `affiliate_image_medium`", ex)
            ...
            return

    @close_pop_up()
    async def affiliate_image_small(self, value:Optional[str] = None) -> bool:
        """Fetch and set affiliate small image.
        
        Args:
        value (str): это значение можно передать в словаре kwargs через ключ {affiliate_image_small = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.affiliate_image_small`.
        """
        try:            
            self.product_fields.affiliate_image_small = value or  await self.driver.execute_locator(self.product_locator.affiliate_image_small) or ''
            return True
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `affiliate_image_small`", ex)
            ...
            return

    @close_pop_up()
    async def available_date(self, value:Optional[Any] = None) -> bool:
        """Fetch and set available date.
        
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {available_date = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.available_date`.
        """
        try:            
            self.product_fields.available_date = value or  await self.driver.execute_locator(self.product_locator.available_date) or ''
            return True
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `available_date`", ex)
            ...
            return

    @close_pop_up()
    async def available_for_order(self, value:Optional[str] = None) -> bool:
        """Fetch and set available for order status.

        Args:
        value (str): это значение можно передать в словаре kwargs через ключ {available_for_order = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.available_for_order`.
        """
        try:            
            self.product_fields.available_for_order = value or  await self.driver.execute_locator(self.product_locator.available_for_order) or ''
            return True
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `available_for_order`", ex)
            ...
            return


    @close_pop_up()
    async def available_later(self, value:Optional[str] = None) -> bool:
        """Fetch and set available later status.

        Args:
        value (str): это значение можно передать в словаре kwargs через ключ {available_later = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.available_later`.
        """
        try:            
            self.product_fields.available_later = value or  await self.driver.execute_locator(self.product_locator.available_later) or ''
            return True
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `available_later`", ex)
            ...
            return

    @close_pop_up()
    async def available_now(self, value:Optional[str] = 1) -> bool:
        """Fetch and set available now status.

        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {available_now = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.available_now`.
        """
        try:            
            self.product_fields.available_now = normalize_int(value or  await self.driver.execute_locator(self.product_locator.available_now) or 1)
            return True
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `available_now`", ex)
            ...
            return


    @close_pop_up()
    async def additional_categories(self, value: str | list = None) -> dict:
        """Set additional categories.

        Это значение можно передать в словаре kwargs через ключ {additional_categories = `value`} при определении класса.
        Если `value` было передано, оно подставляется в поле `ProductFields.additional_categories`.

        Args:
        value (str | list, optional): Строка или список категорий. Если не передано, используется пустое значение.

        Returns:
        dict: Словарь с ID категорий.
        """
        self.product_fields.additional_categories = value 
        return True if value else False
        

    @close_pop_up()
    async def cache_default_attribute(self, value:Optional[Any] = None) -> bool:
        """Fetch and set cache default attribute.

        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {cache_default_attribute = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.cache_default_attribute`.
        """
        try:
            self.product_fields.cache_default_attribute = value or  await self.driver.execute_locator(self.product_locator.cache_default_attribute) or ''
            return True
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `cache_default_attribute`", ex)
            ...
            return

    @close_pop_up()
    async def cache_has_attachments(self, value:Optional[int] = 0) -> bool:
        """Fetch and set cache has attachments status.

        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {cache_has_attachments = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.cache_has_attachments`.
        """
        try:            
            self.product_fields.cache_has_attachments = normalize_int(value or  await self.driver.execute_locator(self.product_locator.cache_has_attachments) or 0)
           
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `cache_has_attachments`", ex)
            ...
            return
        return True

    @close_pop_up()
    async def cache_is_pack(self, value:Optional[str] = None) -> bool:
        """Fetch and set cache is pack status.

        Args:
        value (str): это значение можно передать в словаре kwargs через ключ {cache_is_pack = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.cache_is_pack`.
        """
        try:            
            self.product_fields.cache_is_pack = normalize_string(value or  await self.driver.execute_locator(self.product_locator.cache_is_pack) or '')
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `cache_is_pack`", ex)
            ...
            return
        return True

    @close_pop_up()
    async def condition(self, value:Optional[Any] = None) -> bool:
        """Fetch and set product condition.

        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {condition = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.condition`.
        """
        try:            
            self.product_fields.condition = normalize_string(value or  await self.driver.execute_locator(self.product_locator.condition) or 'new')
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `condition`", ex)
            ...
            return
        return True


    @close_pop_up()
    async def customizable(self, value:Optional[Any] = None) -> bool:
        """Fetch and set customizable status.

        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {customizable = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.customizable`.
        """
        try:            
            self.product_fields.customizable = value or  await self.driver.execute_locator(self.product_locator.customizable) or ''
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `customizable`", ex)
            ...
            return
        return True

    @close_pop_up()
    async def date_add(self, value:Optional[str | datetime.date] = None) -> bool:
        """Fetch and set date added.

        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {date_add = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.date_add`.
        """
        try:            
            self.product_fields.date_add = normalize_sql_date( value or  await self.driver.execute_locator(self.product_locator.date_add) or gs.now)
            
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `date_add`", ex)
            ...
            return
        return True

    @close_pop_up()
    async def date_upd(self, value:Optional[str | datetime.date] = None) -> bool:
        """Fetch and set date updated.

        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {date_upd = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.date_upd`.
        """
        try:            
            self.product_fields.date_upd = normalize_sql_date( value or  await self.driver.execute_locator(self.product_locator.date_upd) or gs.now )
            
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `date_upd`", ex)
            ...
            return
        return True

    @close_pop_up()
    async def delivery_out_stock(self, value:Optional[str] = None) -> bool:
        """Fetch and set delivery out of stock.

        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {delivery_out_stock = `value`} при определении класса.
        Если `value` было передано, его значение подставляется в поле `ProductFields.delivery_out_stock`.
        """
        try:            
            self.product_fields.delivery_out_stock = normalize_string( value or  await self.driver.execute_locator(self.product_locator.delivery_out_stock) or '')
           
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `delivery_out_stock`", ex)
            ...
            return
        return True

    @close_pop_up()
    async def depth(self, value:Optional[float] = None) -> bool:
        """Fetch and set depth.

        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {depth = `value`} при определении класса.
        Если `value` было передано, его значение подставляется в поле `ProductFields.depth`.
        """
        try:            
            self.product_fields.depth = normalize_float( value or  await self.driver.execute_locator(self.product_locator.depth) or None )
            return True
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `depth`", ex)
            ...
            return

    @close_pop_up()
    async def description(self, value:Optional[str] = None) -> bool:
        """Fetch and set description.
        
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {description = `value`} при определении класса.
        Если `value` было передано, его значение подставляется в поле `ProductFields.description`.
        """
        try:
            self.product_fields.description = normalize_string(value or  await self.driver.execute_locator(self.product_locator.description) or None)
            return True
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `description` \n ", ex)
            ...
            return
        return True

    @close_pop_up()
    async def description_short(self, value:Optional[str] = '') -> bool:
        """Fetch and set short description.
    
        Args:
        value (atr): это значение можно передать в словаре kwargs через ключ {description_short = `value`} при определении класса.
        Если `value` было передано, его значение подставляется в поле `ProductFields.description_short`.
        """
        try:
            self.product_fields.description_short = normalize_string(value or await self.driver.execute_locator(self.product_locator.description_short) or '')
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `description_short`", ex)
            ...
            return
        return True



    @close_pop_up()
    async def id_category_default(self, value:int) -> bool:
        """Fetch and set default category ID.
        
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {id_category_default = `value`} при определении класса.
        Если `value` было передано, его значение подставляется в поле `ProductFields.id_category_default`.
        """
        try:
            self.product_fields.id_category_default = normalize_int(value or await self.driver.execute_locator(self.product_locator.id_category_default) or None)
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `id_category_default`", ex)
            ...
            return False
        return True

    @close_pop_up()
    async def id_default_combination(self, value:Optional[int] = None) -> bool:
        """Fetch and set default combination ID.
        
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {id_default_combination = `value`} при определении класса.
        Если `value` было передано, его значение подставляется в поле `ProductFields.id_default_combination`.
        """
        try:
            self.product_fields.id_default_combination = normalize_int(value or await self.driver.execute_locator(self.product_locator.id_default_combination) or 0)
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `id_default_combination`", ex)
            ...
            return False
        return True

    @close_pop_up()
    async def id_product(self, value:Optional[int] = None) -> bool:
        """Fetch and set product ID.
        
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {id_product = `value`} при определении класса.
        Если `value` было передано, его значение подставляется в поле `ProductFields.id_product`.
        """
        try:
            # Получаем значение id_supplier, если оно не передано
            self.product_fields.id_product = normalize_int(await self.driver.execute_locator(self.product_locator.id_product), None)
        except Exception as ex:
            logger.error(f"Ошибка значения поля `id_product`", ex)
            ...
            return
    


    @close_pop_up()
    async def locale(self, value:Optional[Any] = None) -> bool:
        """Fetch and set locale.
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {locale = `value`} при определении класса.
        Если `value` не было передано, оно определяется автоматически.
        """

        # Если value не передано, Определение locale автоматически
        try:
            i18n = value or d.locale
            if not i18n and self.product_fields.name['language'][0]['value']:
                text = self.product_fields.name['language'][0]['value']
                i18n = detect(text)

            # Записываем результат в поле `locale` объекта `ProductFields`
            self.product_fields.locale = i18n

        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `locale`", ex)
            ...
            return
        return True


    @close_pop_up()
    async def id_default_image(self, value:Optional[int] = None) -> bool:
        """Fetch and set default image ID.
        Args:
            Значение   определается из престашопа автоматически, если не передано.
        """

        try:            
            self.product_fields.id_default_image = value or  await self.driver.execute_locator(self.product_locator.id_default_image) or 0
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `id_default_image`", ex)
            ...
            return
        return True


    @close_pop_up()
    async def ean13(self, value:Optional[str] = None) -> bool:
        """Fetch and set EAN13 code.
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {ean13 = `value`} при определении класса.
        Если `value` было передано, его значение подставляется в поле `ProductFields.ean13`.
        """

        try:            
            self.product_fields.ean13 = value or  await self.driver.execute_locator(self.product_locator.ean13) or ''
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `ean13`", ex)
            ...
            return
        return True


    @close_pop_up()
    async def ecotax(self, value:Optional[int] = None) -> bool:
        """Fetch and set ecotax.
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {ecotax = `value`} при определении класса.
        Если `value` было передано, его значение подставляется в поле `ProductFields.ecotax`.
        """

        try:

            self.product_fields.ecotax = value or  await self.driver.execute_locator(self.product_locator.ecotax) or 0
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `ecotax`", ex)
            ...
        return True


    @close_pop_up()
    async def height(self, value:Optional[float] = None) -> bool:
        """Fetch and set height.
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {height = `value`} при определении класса.
        Если `value` было передано, его значение подставляется в поле `ProductFields.height`.
        """

        try:            
            self.product_fields.height = value or  await self.driver.execute_locator(self.product_locator.height) or 0.0
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `height`", ex)
            ...
            return
        return True

    @close_pop_up()
    async def how_to_use(self, value:Optional[str] = None) -> bool:
        """Fetch and set how to use.
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {how_to_use = `value`} при определении класса.
        Если `value` было передано, его значение подставляется в поле `ProductFields.how_to_use`.
        """
        try:            
            self.product_fields.how_to_use = normalize_string(value or  await self.driver.execute_locator(self.product_locator.how_to_use) or '')
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `how_to_use`", ex)
            ...
            return
        return True

    @close_pop_up()
    async def id_manufacturer(self, value:Optional[int] = None) -> bool:
        """Fetch and set manufacturer ID.
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {id_manufacturer = `value`} при определении класса.
        Если `value` было передано, его значение подставляется в поле `ProductFields.id_manufacturer`.
        """
        try:            
            self.product_fields.id_manufacturer = normalize_int(value or  await self.driver.execute_locator(self.product_locator.id_manufacturer) or None)
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `id_manufacturer`", ex)
            ...
            return
        return True


    @close_pop_up()
    async def id_supplier(self, value:Optional[Any] = None) -> bool:
        """Fetch and set supplier ID.
        Код поставщика из таблицы `suppliers`
        Обычно подставлятся в локакор
              "id_supplier": {
                "attribute": "1234",
                "by": "VALUE",
                "strategy_for_multiple_selectors": "find_first_match",
                "selector": "none",
                "if_list": "first",
                "mandatory": true,
                "timeout": 2,
                "timeout_for_event": "presence_of_element_located",
                "event": null,
                "locator_description": "SKU ksp"
              },

              Таблица поставщиков:
              https://docs.google.com/spreadsheets/d/14f0PyQa32pur-sW2MBvA5faIVghnsA0hWClYoKpkFBQ/edit?gid=1778506526#gid=1778506526
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {id_supplier = `value`} при определении класса.
        Если `value` было передано, его значение подставляется в поле `ProductFields.id_supplier`.
        """
        try:            
            self.product_fields.id_supplier = normalize_int(value or  self.product_locator.id_supplier.attribute)
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `id_supplier`", ex)
            ...
            return
        return True


    @close_pop_up()
    async def id_tax_rules_group (self, value:Optional[Any] = None) -> bool:
        """Fetch and set tax ID.
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {id_tax_rules_group = `value`} при определении класса.
        Если `value` было передано, его значение подставляется в поле `ProductFields.id_tax_rules_group`.
        """
        try:            
            self.product_fields.id_tax_rules_group = normalize_int(value or  await self.driver.execute_locator(self.product_locator.id_tax_rules_group ) or 1)
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `id_tax_rules_group `", ex)
            ...
            return
        return True

    @close_pop_up()
    async def id_type_redirected(self, value:Optional[Any] = None) -> bool:
        """Fetch and set redirected type ID.
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {id_type_redirected = `value`} при определении класса.
        Если `value` было передано, его значение подставляется в поле `ProductFields.id_type_redirected`.
        """
        try:            
            self.product_fields.id_type_redirected = normalize_int(value or  await self.driver.execute_locator(self.product_locator.id_type_redirected) or 0)
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `id_type_redirected`", ex)
            ...
            return
        return True


    @close_pop_up()
    async def images_urls(self, value:Optional[Any] = None) -> bool:
        """Fetch and set image URLs.
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {images_urls = `value`} при определении класса.
        Если `value` было передано, его значение подставляется в поле `ProductFields.images_urls`.
        """
        try:            
            self.product_fields.images_urls = normalize_string(value or  await self.driver.execute_locator(self.product_locator.images_urls) or '')
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `images_urls`", ex)
            ...
            return
        return True    


    @close_pop_up()
    async def indexed(self, value:Optional[Any] = None) -> bool:
        """Fetch and set indexed status.
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {indexed = `value`} при определении класса.
        Если `value` было передано, его значение подставляется в поле `ProductFields.indexed`.
        """
        try:            
            self.product_fields.indexed = normalize_string(value or  await self.driver.execute_locator(self.product_locator.indexed) or '')
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `indexed`", ex)
            ...
            return
        return True


    @close_pop_up()
    async def ingredients(self, value:Optional[Any] = None) -> bool:
        """Fetch and set ingredients.
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {ingredients = `value`} при определении класса.
        Если `value` было передано, его значение подставляется в поле `ProductFields.ingredients`.
        """
        try:            
            self.product_fields.ingredients = normalize_string(value or  await self.driver.execute_locator(self.product_locator.ingredients) or '')
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `ingredients`", ex)
            ...
            return
        return True


    @close_pop_up()
    async def meta_description(self, value:Optional[Any] = None) -> bool:
        """Fetch and set meta description.
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {meta_description = `value`} при определении класса.
        Если `value` было передано, его значение подставляется в поле `ProductFields.meta_description`.
        """
        try:            
            self.product_fields.meta_description = normalize_string(value or  await self.driver.execute_locator(self.product_locator.meta_description) or '')
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `meta_description`", ex)
            ...
            return
        return True


    @close_pop_up()
    async def meta_keywords(self, value:Optional[Any] = None) -> bool:
        """Fetch and set meta keywords.
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {meta_keywords = `value`} при определении класса.
        Если `value` было передано, его значение подставляется в поле `ProductFields.meta_keywords`.
        """
        try:
            self.product_fields.meta_keywords = normalize_string(value or  await self.driver.execute_locator(self.product_locator.meta_keywords) or '')
            return True
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `meta_keywords`", ex)
            ...
            return


    @close_pop_up()
    async def meta_title(self, value:Optional[Any] = None) -> bool:
        """Fetch and set meta title.
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {meta_title = `value`} при определении класса.
        Если `value` было передано, его значение подставляется в поле `ProductFields.meta_title`.
        """
        try:
            self.product_fields.meta_title = normalize_string(value or  await self.driver.execute_locator(self.product_locator.meta_title) or '')
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `meta_title`", ex)
            return
        return True

    @close_pop_up()
    async def is_virtual(self, value:Optional[Any] = None) -> bool:
        """Fetch and set virtual status.
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {is_virtual = `value`} при определении класса.
        Если `value` было передано, его значение подставляется в поле `ProductFields.is_virtual`.
        """
        try:            
            self.product_fields.is_virtual = normalize_int(value or  await self.driver.execute_locator(self.product_locator.is_virtual) or 0)  
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `is_virtual`", ex)
            ...
            return
        return True


        
    @close_pop_up()
    async def isbn(self, value:Optional[Any] = None) -> bool:
        """Fetch and set ISBN.
        
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {isbn = `value`} при определении класса.
        Если `value` было передано, его значение подставляется в поле `ProductFields.isbn`.
        """
        try:            
            self.product_fields.isbn = normalize_string(value or  await self.driver.execute_locator(self.product_locator.isbn) or '')
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `isbn`", ex)
            ...
            return
        return True

    @close_pop_up()
    async def link_rewrite(self, value:Optional[Any] = None) -> bool:
        """Fetch and set link rewrite.
        
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {link_rewrite = `value`} при определении класса.
        Если `value` было передано, его значение подставляется в поле `ProductFields.link_rewrite`.
        """
        try:            
            self.product_fields.link_rewrite = normalize_string(value or  await self.driver.execute_locator(self.product_locator.link_rewrite) or '')
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `link_rewrite`", ex)
            ...
            return
        return True

    @close_pop_up()
    async def location(self, value:Optional[Any] = None) -> bool:
        """Fetch and set location.
        
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {location = `value`} при определении класса.
        Если `value` было передано, его значение подставляется в поле `ProductFields.location`.
        """
        try:            
            self.product_fields.location = normalize_string(value or  await self.driver.execute_locator(self.product_locator.location) or '')
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `location`", ex)
            ...
            return
        return True

    @close_pop_up()
    async def low_stock_alert(self, value:Optional[Any] = None) -> bool:
        """Fetch and set low stock alert.
        
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {low_stock_alert = `value`} при определении класса.
        Если `value` было передано, его значение подставляется в поле `ProductFields.low_stock_alert`.
        """
        try:
            self.product_fields.low_stock_alert = normalize_string(value or  await self.driver.execute_locator(self.product_locator.low_stock_alert) or '') 
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `low_stock_alert`", ex)
            ...
            return
        return True

    @close_pop_up()
    async def low_stock_threshold(self, value:Optional[Any] = None) -> bool:
        """Fetch and set low stock threshold.
        
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {low_stock_threshold = `value`} при определении класса.
        Если `value` было передано, его значение подставляется в поле `ProductFields.low_stock_threshold`.
        """
        try:
            self.product_fields.low_stock_threshold = normalize_string( value or  await self.driver.execute_locator(self.product_locator.low_stock_threshold) or '' )
            
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `low_stock_threshold`", ex)
            ...
            return
        return True

    @close_pop_up()
    async def minimal_quantity(self, value:Optional[Any] = None) -> bool:
        """Fetch and set minimal quantity.
        
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {minimal_quantity = `value`} при определении класса.
        Если `value` было передано, его значение подставляется в поле `ProductFields.minimal_quantity`.
        """
        try:
            
            self.product_fields.minimal_quantity = normalize_int( value or  await self.driver.execute_locator(self.product_locator.minimal_quantity) or 1)

        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `minimal_quantity`", ex)
            ...
            return
        return True

    @close_pop_up()
    async def mpn(self, value:Optional[Any] = None) -> bool:
        """Fetch and set MPN (Manufacturer Part Number).
        
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {mpn = `value`} при определении класса.
        Если `value` было передано, его значение подставляется в поле `ProductFields.mpn`.
        """
        try:
            
            self.product_fields.mpn = normalize_string( value or  await self.driver.execute_locator(self.product_locator.mpn) or '')
            
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `mpn`", ex)
            ...
            return
        return True

    @close_pop_up()
    async def name(self, value:Optional[str] = '') -> bool:
        """Fetch and set product name.
        
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {name = `value`} при определении класса.
        Если `value` было передано, его значение подставляется в поле `ProductFields.name`.
        """
        value = value if value else await self.driver.execute_locator(self.product_locator.name)
        if value:
            self.product_fields.name = normalize_string(value)[:127]
            return True       
        return False


    @close_pop_up()
    async def online_only(self, value:Optional[Any] = None) -> bool:
        """Fetch and set online-only status.
        
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {online_only = `value`} при определении класса.
        Если `value` было передано, его значение подставляется в поле `ProductFields.online_only`.
        """
        try:
            
            self.product_fields.online_only = normalize_int( value or  await self.driver.execute_locator(self.product_locator.online_only) or 0 )
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `online_only`", ex)
            ...
            return
        return True

    @close_pop_up()
    async def on_sale(self, value:Optional[Any] = None) -> bool:
        """Fetch and set on sale status.
        
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {on_sale = `value`} при определении класса.
        Если `value` было передано, его значение подставляется в поле `ProductFields.on_sale`.
        """
        try:
            
            self.product_fields.on_sale = value or  await self.driver.execute_locator(self.product_locator.on_sale) or ''
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `on_sale`", ex)
            ...
            return
        return True


    @close_pop_up()
    async def out_of_stock(self, value:Optional[Any] = None) -> bool:
        """Fetch and set out of stock status.
        
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {out_of_stock = `value`} при определении класса.
        Если `value` было передано, его значение подставляется в поле `ProductFields.out_of_stock`.
        """
        try:
            
            self.product_fields.out_of_stock = normalize_string( value or  await self.driver.execute_locator(self.product_locator.out_of_stock) or '' )
            
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `out_of_stock`", ex)
            ...
            return
        return True

    @close_pop_up()
    async def pack_stock_type(self, value:Optional[Any] = None) -> bool:
        """Fetch and set pack stock type.

        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {pack_stock_type = `value`} при определении класса.
        Если `value` было передано, его значение подставляется в поле `ProductFields.pack_stock_type`.
        """
        try:
            
            self.product_fields.pack_stock_type = normalize_string( value or  await self.driver.execute_locator(self.product_locator.pack_stock_type) or '')
            
        except Exception as ex:
            logger.error(f'Ошибка получения значения в поле `pack_stock_type`', ex)
            ...
            return
        return True


    @close_pop_up()
    async def price(self, value:Optional[Any] = None) -> bool:
        """Fetch and set price.

        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {price = `value`} при определении класса.
        Если `value` было передано, его значение подставляется в поле `ProductFields.price`.
        """
        try:
            self.product_fields.price = normalize_float( value if value else await self.driver.execute_locator(self.product_locator.price))
            
        except Exception as ex:
            logger.error(f'Ошибка получения значения в поле `price`', ex)
            ...
            return
        return True

    @close_pop_up()
    async def product_type(self, value:Optional[Any] = None) -> bool:
        """Fetch and set product type.

        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {product_type = `value`} при определении класса.
        Если `value` был передан - его значение подставляется в поле `ProductFields.product_type`.
        """
        try:
            
            self.product_fields.product_type = value or  await self.driver.execute_locator(self.product_locator.product_type) or ''
        except Exception as ex:
            logger.error(f'Ошибка получения значения в поле `product_type`', ex)
            ...
            return
        return True


    @close_pop_up()
    async def quantity(self, value:Optional[Any] = None) -> bool:
        """Fetch and set quantity.

        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {quantity = `value`} при определении класса.
        Если `value` был передан - его значение подставляется в поле `ProductFields.quantity`.
        """
        try:
            self.product_fields.quantity = normalize_int( value or  await self.driver.execute_locator(self.product_locator.quantity) or 1 )
        except Exception as ex:
            logger.error(f'Ошибка получения значения в поле `quantity`', ex)
            ...
            return
        return True

    @close_pop_up()
    async def quantity_discount(self, value:Optional[Any] = None) -> bool:
        """Fetch and set quantity discount.

        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {quantity_discount = `value`} при определении класса.
        Если `value` был передан - его значение подставляется в поле `ProductFields.quantity_discount`.
        """
        try:
            self.product_fields.quantity_discount = normalize_string( value or  await self.driver.execute_locator(self.product_locator.quantity_discount) or '' )
            self.product_fields.quantity_discount = normalize_string( value or  await self.driver.execute_locator(self.product_locator.quantity_discount) or '' )
            
        except Exception as ex:
            logger.error(f'Ошибка получения значения в поле `quantity_discount`', ex)
            ...
            return
        return True

    @close_pop_up()
    async def redirect_type(self, value:Optional[Any] = None) -> bool:
        """Fetch and set redirect type.

        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {redirect_type = `value`} при определении класса.
        Если `value` был передан - его значение подставляется в поле `ProductFields.redirect_type`.
        """
        try:            
            self.product_fields.redirect_type = value or  await self.driver.execute_locator(self.product_locator.redirect_type) or ''
        except Exception as ex:
            logger.error(f'Ошибка получения значения в поле `redirect_type`', ex)
            ...
            return
        return True


    @close_pop_up()
    async def reference(self, value:Optional[Any] = None) -> bool:
        """Fetch and set reference.

        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {reference = `value`} при определении класса.
        Если `value` был передан - его значение подставляется в поле `ProductFields.reference`.
        """
        try:            
            self.product_fields.reference = normalize_string( value or  await self.driver.execute_locator(self.product_locator.reference) or '')

        except Exception as ex:
            logger.error(f'Ошибка получения значения в поле `reference`', ex)
            ...
            return
        return True

    @close_pop_up()
    async def show_condition(self, value:Optional[int] = None) -> bool:
        """Fetch and set show condition.
    
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {show_condition = `value`} при определении класса.
        Если `value` был передан - его значение подставляется в поле `ProductFields.show_condition`.
        """
        try:
            self.product_fields.show_condition = normalize_int( value or  await self.driver.execute_locator(self.product_locator.show_condition) or 1 )
            
        except Exception as ex:
            logger.error('Ошибка получения значения в поле `show_condition`', ex)
            ...
            return
        return True

    @close_pop_up()
    async def show_price(self, value:Optional[int] = None) -> bool:
        """Fetch and set show price.
    
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {show_price = `value`} при определении класса.
        Если `value` был передан - его значение подставляется в поле `ProductFields.show_price`.
        """
        try:
            self.product_fields.show_price = normalize_int( value or  await self.driver.execute_locator(self.product_locator.show_price) or 1 )
            
        except Exception as ex:
            logger.error('Ошибка получения значения в поле `show_price`', ex)
            ...
            return
        return True


    @close_pop_up()
    async def state(self, value:Optional[str] = None) -> bool:
        """Fetch and set state.
    
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {state = `value`} при определении класса.
        Если `value` был передан - его значение подставляется в поле `ProductFields.state`.
        """
        try:
            
            self.product_fields.state = normalize_string( value or  await self.driver.execute_locator(self.product_locator.state))
        except Exception as ex:
            logger.error('Ошибка получения значения в поле `state`', ex)
            ...
            return
        return True

    @close_pop_up()
    async def text_fields(self, value:Optional[Any] = None) -> bool:
        """Fetch and set text fields.
    
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {text_fields = `value`} при определении класса.
        Если `value` был передан - его значение подставляется в поле `ProductFields.text_fields`.
        """
        try:
            self.product_fields.text_fields = value or  await self.driver.execute_locator(self.product_locator.text_fields) or ''
        except Exception as ex:
            logger.error('Ошибка получения значения в поле `text_fields`', ex)
            ...
            return
        return True

    @close_pop_up()
    async def unit_price_ratio(self, value:Optional[Any] = None) -> bool:
        """Fetch and set unit price ratio.
    
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {unit_price_ratio = `value`} при определении класса.
        Если `value` был передан - его значение подставляется в поле `ProductFields.unit_price_ratio`.
        """
        try:
            
            self.product_fields.unit_price_ratio = value or  await self.driver.execute_locator(self.product_locator.unit_price_ratio) or ''
        except Exception as ex:
            logger.error('Ошибка получения значения в поле `unit_price_ratio`', ex)
            ...
            return
        return True


    @close_pop_up()
    async def unity(self, value:Optional[str] = None) -> bool:
        """Fetch and set unity.

        Args:
            value (Any): это значение можно передать в словаре kwargs через ключ {unity = `value`} при определении класса.
            Если `value` был передан - его значение подставляется в поле `ProductFields.unity`.
        """
        try:
            self.product_fields.unity = normalize_string( value or  await self.driver.execute_locator(self.product_locator.unity) or '')
            
        except Exception as ex:
            logger.error(f'Ошибка получения значения в поле `unity`', ex)
            ...
            return
        return True

    @close_pop_up()
    async def upc(self, value:Optional[str] = None) -> bool:
        """Fetch and set UPC.

        Args:
            value (Any): это значение можно передать в словаре kwargs через ключ {upc = `value`} при определении класса.
            Если `value` был передан - его значение подставляется в поле `ProductFields.upc`.
        """
        try:
            self.product_fields.upc = normalize_string( value or  await self.driver.execute_locator(self.product_locator.upc) or '')
            
        except Exception as ex:
            logger.error(f'Ошибка получения значения в поле `upc`', ex)
            ...
            return
        return True

    @close_pop_up()
    async def uploadable_files(self, value:Optional[Any] = None) -> bool:
        """Fetch and set uploadable files.

        Args:
            value (Any): это значение можно передать в словаре kwargs через ключ {uploadable_files = `value`} при определении класса.
            Если `value` был передан - его значение подставляется в поле `ProductFields.uploadable_files`.
        """
        try:
            
            self.uploadable_files.upc = value or  await self.driver.execute_locator(self.product_locator.uploadable_files) or ''
            
        except Exception as ex:
            logger.error(f'Ошибка получения значения в поле `uploadable_files`', ex)
            ...
            return
        return True

    @close_pop_up()
    async def default_image_url(self, value:Optional[str] = None) -> bool:
        """Fetch and set default image URL.

        Args:
            value (Any): это значение можно передать в словаре kwargs через ключ {default_image_url = `value`} при определении класса.
            Если `value` был передан - его значение подставляется в поле `ProductFields.default_image_url`.
        """
        try:
            self.product_fields.default_image_url = value or  await self.driver.execute_locator(self.product_locator.default_image_url) or ''

        except Exception as ex:
            logger.error(f'Ошибка получения значения в поле `default_image_url`', ex)
            ...
            return
        return True

    @close_pop_up()
    async def visibility(self, value:Optional[str] = None) -> bool:
        """Fetch and set visibility.
          
        Args:
            value (Any): это значение можно передать в словаре kwargs через ключ {visibility = `value`} при определении класса.
              В таблице ps_products  поле visibility определяет, 
            как товар будет виден на сайте. Возможные значения этого поля обычно следующие:

            `both`: Товар будет виден как в каталоге, так и в результатах поиска.  
            `catalog`: Товар будет виден только в каталоге, но не будет отображаться в результатах поиска.
            `search`: Товар будет виден только в результатах поиска, но не будет отображаться в каталоге.
            `none`: Товар будет скрыт от всех пользователей и не будет виден ни в каталоге, ни в результатах поиска.
            Эти значения позволяют управлять видимостью товаров на сайте, что может быть полезно для различных маркетинговых стратегий или временного скрытия товаров.
            Если `value` был передан - его значение подставляется в поле `ProductFields.visibility`.
        """
        try:
            self.product_fields.visibility = value or  await self.driver.execute_locator(self.product_locator.visibility) or 'both'
        except Exception as ex:
            logger.error(f'Ошибка получения значения в поле `visibility`', ex)
            ...
            return
        return True


    @close_pop_up()
    async def weight(self, value:Optional[float] = None) -> bool:
        """Fetch and set weight.
    
        Args:
            value (Any): это значение можно передать в словаре kwargs через ключ {weight = `value`} при определении класса.
            Если `value` был передан, его значение подставляется в поле `ProductFields.weight`.
        """
        try:           
            self.product_fields.weight = normalize_int( value or  await self.driver.execute_locator(self.product_locator.weight) or 0  )
            
        except Exception as ex:
            logger.error('Ошибка получения значения в поле `weight`', ex)
            ...
            return
        return True


    @close_pop_up()
    async def wholesale_price(self, value:Optional[float] = None) -> bool:
        """Fetch and set wholesale price.
    
        Args:
            value (Any): это значение можно передать в словаре kwargs через ключ {wholesale_price = `value`} при определении класса.
            Если `value` был передан, его значение подставляется в поле `ProductFields.wholesale_price`.
        """
        try:
            self.product_fields.wholesale_price = normalize_float( value or  await self.driver.execute_locator(self.product_locator.wholesale_price) or 0)

        except Exception as ex:
            logger.error('Ошибка получения значения в поле `wholesale_price`', ex)
            ...
            return
        return True

    @close_pop_up()
    async def width(self, value:Optional[float] = None) -> bool:
        """Fetch and set width.
    
        Args:
            value (Any): это значение можно передать в словаре kwargs через ключ {width = `value`} при определении класса.
            Если `value` был передан, его значение подставляется в поле `ProductFields.width`.
        """
        try:
           self.product_fields.width = normalize_float( value or  await self.driver.execute_locator(self.product_locator.width) or 0)
            
        except Exception as ex:
            logger.error('Ошибка получения значения в поле `width`', ex)
            ...
            return
        return True


    @close_pop_up()
    async def specification(self, value:Optional[str|list] = None) -> bool:
        """Fetch and set specification.
    
        Args:
            value (Any): это значение можно передать в словаре kwargs через ключ {specification = `value`} при определении класса.
            Если `value` был передан, его значение подставляется в поле `ProductFields.specification`.
        """
        try:
            
            self.product_fields.specification = normalize_string( value or  await self.driver.execute_locator(self.product_locator.specification) or '')
            
        except Exception as ex:
            logger.error('Ошибка получения значения в поле `specification`', ex)
            ...
            return
        return True

    @close_pop_up()
    async def link(self, value:Optional[str] = None) -> bool:
        """Fetch and set link.
    
        Args:
            value (Any): это значение можно передать в словаре kwargs через ключ {link = `value`} при определении класса.
            Если `value` был передан, его значение подставляется в поле `ProductFields.link`.
        """
        try:            
            self.product_fields.link = value or  await self.driver.execute_locator(self.product_locator.link) or ''

        except Exception as ex:
            logger.error('Ошибка получения значения в поле `link`', ex)
            ...
            return
        return True

    @close_pop_up()
    async def byer_protection(self, value:Optional[str] = None) -> bool:
        """Fetch and set buyer protection.
        
        Args:
        value (str): это значение можно передать в словаре kwargs через ключ {byer_protection = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.byer_protection`.
        """
        try:
            self.product_fields.byer_protection = normalize_string( value or  await self.driver.execute_locator(self.product_locator.byer_protection) or '' )
            
        except Exception as ex:
            logger.error(f'Ошибка получения значения в поле `byer_protection`', ex)
            ...
            return
        return True

    @close_pop_up()
    async def customer_reviews(self, value:Optional[Any] = None) -> bool:
        """Fetch and set customer reviews.
        
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {customer_reviews = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.customer_reviews`.
        """
        try:
            self.product_fields.customer_reviews = normalize_string( value or  await self.driver.execute_locator(self.product_locator.customer_reviews) or ''  )
            
        except Exception as ex:
            logger.error(f'Ошибка получения значения в поле `customer_reviews`', ex)
            ...
            return
        return True

    @close_pop_up()
    async def link_to_video(self, value:Optional[Any] = None) -> bool:
        """Fetch and set link to video.
        
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {link_to_video = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.link_to_video`.
        """
        try:
            self.product_fields.link_to_video = value or  await self.driver.execute_locator(self.product_locator.link_to_video) or ''
            
        except Exception as ex:
            logger.error(f'Ошибка получения значения в поле `link_to_video`', ex)
            ...
            return
        return True

    @close_pop_up()
    async def local_image_path(self, value: Optional[str] = None) -> bool:
        """Fetch and save an image locally.

        Функция получает `URL` картинки или байты изображения, сохраняет изображение в формате `PNG` в директории `tmp` 
        и устанавливает путь к сохранённой картинке в поле `local_image_path`. Если передано значение в параметре `value`,
        оно записывается в поле без изменений.

        Args:
            value (Optional[str], optional): URL изображения, который можно передать в классе через ключ `{local_image_path = value}`.
                Если `value` было передано, его значение подставляется в поле `ProductFields.local_image_path`.

        .. note:
            Путь к изображению ведёт в директорию `tmp`.

        .. todo:
            - Как передать значение из `**kwargs` функции `grab_product_page(**kwargs)`?
            - Как передать путь к файлу без жесткой привязки?

        """
        if value:
            self.product_fields.local_image_path = value
            return True

        img_path:str = Path(gs.path.tmp / f'{self.product_fields.id_supplier}_{self.product_fields.id_product}.png')

        self.product_fields.local_image_path = img_path  # <- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DEBUG

        try:
            if not self.product_fields.id_supplier:
                await self.id_supplier()
            # Получаем результат из локатора как `bytes` или `str`(url)
            raw_image = await self.driver.execute_locator(self.product_locator.default_image_url)
            if not raw_image:
                logger.error(f"Not image grabed. locator: {print(self.product_locator.default_image_url)}")
                return False

            raw_image = raw_image[0] if isinstance(raw_image, list) else raw_image

            if isinstance(raw_image, bytes):
                # Если это байты, они передаются в save_image для сохранения изображения
                await save_image_async(raw_image, img_path)
                #save_image(raw_image, img_path)  # <- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  DEBUG

            elif isinstance(raw_image, str):
                # если это строка, предполагаем, что это URL изображения
                await save_image_from_url_async(raw_image,img_path)
            else:
                logger.debug("Неизвестный тип данных для изображения", None, False)
                ...
                return

        except Exception as ex:
            logger.error(f'Ошибка сохранения изображения в поле `local_image_path`', ex)
            ...
            return
        return True

    @close_pop_up()
    async def local_video_path(self, value:Optional[Any] = None) -> bool:
        """Fetch and save video locally.
        
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {local_video_path = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.local_video_path`.
        """
        try:
            value = value or  await self.driver.execute_locator(self.product_locator.local_video_path) or ''
            
        except Exception as ex:
            logger.error(f'Ошибка сохранения видео в поле `local_video_path`', ex)
            ...
            return
        return True

# --- graber.py end ---