### **Анализ кода модуля `graber.py`**

#### **Качество кода:**
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Хорошая структура и организация кода.
  - Использование асинхронности для неблокирующих операций.
  - Применение декоратора `@close_pop_up` для обработки всплывающих окон.
  - Использование `logger` для логирования.
- **Минусы**:
  - Некоторые docstring на английском языке.
  - Не везде есть подробные описания в комментариях.
  - Наличие закомментированного кода.
  - Есть не все аннотации.
  - Есть `...` в коде

#### **Рекомендации по улучшению:**

1.  **Документация**:
    *   Перевести все docstring на русский язык.
    *   Добавить более подробные описания ко всем функциям и методам, включая информацию о параметрах и возвращаемых значениях.
2.  **Комментарии**:
    *   Добавить больше комментариев для пояснения логики работы кода, особенно в сложных местах.
    *   Уточнить комментарии, избегая расплывчатых формулировок, таких как "получаем" или "делаем".
    *   Использовать точные описания: "проверяем", "отправляем", "выполняем".
3.  **Использование `j_loads` или `j_loads_ns`**:
    *   Убедиться, что для чтения JSON или конфигурационных файлов используется `j_loads` или `j_loads_ns` вместо стандартных `open` и `json.load`.
4.  **Логирование**:
    *   Проверить, что все ошибки логируются с использованием `logger.error`.
5.  **Аннотации**:
    *   Добавить аннотации типов для всех переменных и параметров функций, где это необходимо.
6.  **Избегать `Union[]`**:
    *   Заменить все экземпляры `Union[]` на `|`.
7.  **Закомментированный код**:
    *   Удалить закомментированный код, если он больше не нужен.
8.  **`...` в коде**:
    *   Заменить `...` на конкретную реализацию или удалить, если это не требуется.
9.  **Стиль кода**:
    *   Проверить код на соответствие стандартам PEP8.
10. **Глобальные переменные**:
    *   Убедиться, что все глобальные переменные определены в классе `Config`.
11. **Параметр `self`**:
    *   Заменить все `self` в методах класса на `cls`.

#### **Оптимизированный код:**

```python
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
        self.fields.name = <Ваша реализация>
        )
    ```
```rst
.. module:: src.suppliers
```

Список полей: https://github.com/hypo69/hypotez/blob/master/src/endpoints/prestashop/product_fields/fields_list.txt

"""

import datetime
import os
import sys
import asyncio
import re
import importlib
from pathlib import Path
from typing import Generator, List, Optional, Dict, Any
from types import SimpleNamespace
from typing import Callable
# from langdetect import detect
from functools import wraps

import header
from header import __root__
from src import gs
from src.webdriver.driver import Driver
from src.webdriver.firefox import Firefox
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


# Глобальные настройки через объект `Config`
from dataclasses import dataclass, field

@dataclass
class Config:
    """
    Класс для хранения глобальных настроек.

    Attributes:
        driver (Optional['Driver']): Объект драйвера, используется для управления браузером или другим интерфейсом.
        locator_for_decorator (Optional[SimpleNamespace]): Если будет установлен - выполнится декоратор `@close_pop_up`.
            Устанавливается при инициализации поставщика, например: `Config.locator = self.product_locator.close_pop_up`.
        supplier_prefix (Optional[str]): Префикс поставщика.

    Example:
        >>> Config = Config()
        >>> Config.supplier_prefix = 'prefix'
        >>> print(Config.supplier_prefix)
        prefix
    """

    # Аттрибуты класса
    locator_for_decorator: Optional[SimpleNamespace] = None  # <- Если будет установлен - выполнится декоратор `@close_pop_up`. Устанавливается при инициализации поставщика, например: `Config.locator = self.product_locator.close_pop_up`
    supplier_prefix: Optional[str] = None
    driver:'Driver' = None  # <- Экземпляр класса Driver. Если не передан - создается новый экземпляр класса Driver(Firefox) по умолчанию'


# Определение декоратора для закрытия всплывающих окон
# В каждом отдельном поставщике (`Supplier`) декоратор может использоваться в индивидуальных целях
# Общее название декоратора `@close_pop_up` можно изменить
# Если декоратор не используется в поставщике - Установи `Config.locator_for_decorator = None`
def close_pop_up() -> Callable:
    """Создает декоратор для закрытия всплывающих окон перед выполнением основной логики функции.
    Функция `driver.execute_locator()` будет вызвана только если был указан `Config.locator_for_decorator` при инициализации экземляра класса.

    Args:
        value ('Driver'): Дополнительное значение для декоратора.

    Returns:
        Callable: Декоратор, оборачивающий функцию.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if Config.locator_for_decorator:
                try:
                    # Выполняет локатор для закрытия всплывающего окна
                    await Config.driver.execute_locator(Config.locator_for_decorator)
                except ExecuteLocatorException as ex:
                    logger.debug(f'Ошибка выполнения локатора:', ex, False)

                finally:
                    # Отменяет локатор после первого срабатывания
                    Config.locator_for_decorator = None

            # Выполняет основную функцию
            return await func(*args, **kwargs)
        return wrapper
    return decorator


class Graber:
    """Базовый класс сбора данных со страницы для всех поставщиков."""

    def __init__(self, supplier_prefix: str,  driver: Optional['Driver'] = None,  lang_index:Optional[int] = 2, ):
        """Инициализация класса Graber.

        Args:
            supplier_prefix (str): Префикс поставщика.
            driver ('Driver'): Экземпляр класса Driver.
            lang_index (Optional[int]): Индекс языка. По умолчанию 2.
        """
        self.supplier_prefix = supplier_prefix
        # Загружает локаторы из JSON файлов
        self.product_locator: SimpleNamespace = j_loads_ns(__root__ / 'src' / 'suppliers' / 'suppliers_list' / supplier_prefix / 'locators' / 'product.json')
        self.category_locator: SimpleNamespace = j_loads_ns(__root__ / 'src' / 'suppliers' / 'suppliers_list' / supplier_prefix / 'locators' / 'category.json')
        self.driver = driver or Driver(Firefox)
        Config.driver = self.driver
        # Устанавливает базовый язык
        self.fields: ProductFields = ProductFields(lang_index ) # <- установка базового языка. Тип - `int`

        # Конфигурация для декоратора
        """Если будет установлен локатор в Config.locator_for_decorator - выполнится декоратор `@close_pop_up`"""
        Config.locator_for_decorator = None


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
                # Проверяем, что все элементы списка - словари
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
                # Используем вашу функцию для поиска файлов
                scenarios_files: List[Path | str] = recursively_get_file_path(scenarios_dir, '.json')

                if not scenarios_files:
                    logger.warning(f"Не найдено '.json' файлов сценариев в директории: {scenarios_dir}")
                    return # Завершаем генератор, если файлов нет

                logger.info(f"Найдено {len(scenarios_files)} файлов сценариев для '{supplier_prefix}'.")
                for scenario_file_path in scenarios_files:
                    try:
                        # Убедимся, что это файл
                        if not Path(scenario_file_path).is_file():
                             logger.warning(f"Пропуск не-файлового пути: {scenario_file_path}")
                             continue

                        # Загружаем JSON
                        loaded_scenario: Optional[Dict[str, Any]] = j_loads(scenario_file_path)

                        # Проверяем успешность загрузки и тип
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

    async def process_supplier_scenarios_async(self, supplier_prefix: str, input_scenarios=None, id_lang:Optional[int]=1) -> bool:
        """
        Пример метода, который использует генератор yield_scenarios_for_supplier
        и вызывает run_scenario для каждого сценария.
        """
        all_results = []
        try:
            # Получаем генератор
            scenario_generator = self.yield_scenarios_for_supplier(supplier_prefix, input_scenarios)

            # Итерируем по сценариям, которые выдает генератор
            for scenarios in scenario_generator:
                # logger.info(f"Запуск сценария для '{supplier_prefix}'...")

                result = await self.process_scenarios(supplier_prefix, scenarios['scenarios'] if hasattr(scenarios, 'scenarios') else scenarios, id_lang )
                all_results.append(result) # Собираем результаты (опционально)

            logger.info(f"Все сценарии для '{supplier_prefix}' обработаны.")
            return all_results # Возвращаем собранные результаты

        except Exception as ex:
            logger.error(f"Ошибка при обработке сценариев для '{supplier_prefix}'", ex, exc_info=True)
            return None # Или другое обозначение ошибки


    async def process_scenarios(self, supplier_prefix: str, input_scenarios: List[Dict[str, Any]] | Dict[str, Any], id_lang:Optional[int]=1) -> Optional[List[Any]]:
        """
        Выполняет один или несколько сценариев для указанного поставщика.

        Args:
            supplier_prefix (str): Префикс (идентификатор) поставщика.
            input_scenarios (List[Dict[str, Any]] | Dict[str, Any]):
                Данные сценариев: либо список словарей сценариев,
                либо словарь вида {'scenarios': {'name': dict, ...}}.
            id_lang (Optional[int]): ID языка. По умолчанию 1.

        Returns:
            Optional[List[Any]]: Список результатов выполнения каждого сценария
                                 (например, списки обработанных URL товаров)
                                 или None в случае критической ошибки.
        """
        actual_scenarios_to_process: List[Dict[str, Any]] = []

        # 1. Нормализация входных данных -> actual_scenarios_to_process (список словарей сценариев)
        if isinstance(input_scenarios, list):
            # Вход - список: валидация содержимого
            if all(isinstance(item, dict) for item in input_scenarios):
                actual_scenarios_to_process = input_scenarios
            else:
                logger.error(f"Входной список для '{supplier_prefix}' содержит не-словари.", None, False)
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
                     return None # Возврат `None` при некорректной структуре
            else:
                # Если это словарь, но не ожидаемой структуры, считаем ошибкой
                logger.error(f"Входной словарь для '{supplier_prefix}' не имеет структуры {{'scenarios': {{...}}}}.")
                # Если нужно обработать одиночный словарь как один сценарий, логика была бы здесь:
                # actual_scenarios_to_process = [input_scenarios]
                return None # Возврат `None` при некорректной структуре
        else:
            logger.error(f"Неверный тип входных данных для '{supplier_prefix}': {type(input_scenarios)}. Ожидался list или dict.")
            return None # Возврат `None` при некорректном типе

        # Проверка, есть ли сценарии после нормализации
        if not actual_scenarios_to_process:
            logger.warning(f"Нет сценариев для обработки для '{supplier_prefix}' после нормализации.")
            return [] # Возврат пустого списка

        # 2. Динамический импорт (вынесен до цикла)
        try:
            module_path_str: str = f'src.suppliers.suppliers_list.{supplier_prefix}.scenario'
            scenario_module = importlib.import_module(module_path_str)
            if not hasattr(scenario_module, 'get_list_products_in_category'):
                logger.error(f"Функция 'get_list_products_in_category' не найдена в {module_path_str}")
                return None
            get_list_func: Callable = getattr(scenario_module, 'get_list_products_in_category')
            if not callable(get_list_func):
                 logger.error(f"'get_list_products_in_category' в {module_path_str} не является функцией")
                 return None
        except (ModuleNotFoundError, ImportError, Exception) as import_err:
            logger.error(f"Ошибка импорта модуля/функции сценария для '{supplier_prefix}'", import_err, exc_info=True)
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
                continue

            scenario_url: Optional[str] = scenario_data.get('url')
            if not scenario_url:
                logger.warning(f"Сценарий для '{supplier_prefix}' не содержит ключ 'url'. Пропуск.")
                continue

            logger.info(f"Обработка сценария для '{supplier_prefix}'. URL: {scenario_url}")

            # 4. Переход по URL сценария
            if not d.get_url(scenario_url):
                logger.error(f"Не удалось перейти по URL сценария: {scenario_url}", None, False)
                continue

            # 5. Вызов функции для получения списка товаров
            list_products_in_category: Optional[List[str]] = None
            try:
                list_products_in_category = await get_list_func(d, self.category_locator)
            except Exception as func_ex:
                logger.error(f"Ошибка при выполнении get_list_products_in_category для URL {scenario_url}", func_ex, exc_info=True)
                continue

            # 6. Проверка результата функции
            if list_products_in_category is None:
                logger.warning(f'Функция get_list_products_in_category вернула None для URL {scenario_url}.')
                continue
            if not isinstance(list_products_in_category, list):
                 logger.error(f'Функция get_list_products_in_category вернула не список: {type(list_products_in_category)} для URL {scenario_url}')
                 continue
            if not list_products_in_category:
                logger.warning(f'Нет ссылок на товары для URL {scenario_url}. Возможно, пустая категория.')
                continue

            for product_url in list_products_in_category:
                # --- Начало тела внутреннего цикла ---
                if not isinstance(product_url, str) or not product_url:
                     logger.warning(f"Некорректный URL товара получен: {product_url}. Пропуск.")
                     continue

                if not d.get_url(product_url):
                    logger.error(f'Ошибка навигации на страницу товара: {product_url}')
                    continue
                required_fields:tuple = ('id_product',
                            'name',
                            'price',
                            'id_supplier',
                            'description_short',
                            'description',
                            'specification',
                            'local_image_path',
                            'default_image_url')

                f: Optional[ProductFields] = await self.grab_page_async(*required_fields, id_lang=id_lang)
                if not f:
                    logger.error(f'Не удалось собрать поля товара с {product_url}')
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
                except Exception as ex:
                    logger.error(f'Не удалось сохранить данные\n {print(f)}\n с {product_url}', ex, exc_info=True)
                product: PrestaProduct = PrestaProduct()
                product.add_new_product(f)
                all_results.append(f)
                # --- Конец тела внутреннего цикла ---

            # --- Конец тела внешнего цикла ---

        # 8. Возврат агрегированных результатов
        logger.info(f"Обработка всех сценариев для '{supplier_prefix}' завершена.")
        return all_results
        # --- Конец функции ---


    async def set_field_value(
        self,
        value: Any,
        locator_func: Callable[[], Any],
        field_name: str,
        default: Any = ''
    ) -> Any:
        """Универсальная функция для установки значений полей с обработкой ошибок.

        Args:
            value (Any): Значение для установки.
            locator_func (Callable[[], Any]): Функция для получения значения из локатора.
            field_name (str): Название поля.
            default (Any): Значение по умолчанию. По умолчанию пустая строка.

        Returns:
            Any: Установленное значение.
        """
        locator_result = await asyncio.to_thread(locator_func)
        if value:
            return value
        if locator_result:
            return locator_result
        await self.error(field_name)
        return default

    def grab_page(self, *args, **kwargs) -> ProductFields:
        """Вызывает асинхронную функцию сбора данных."""
        return asyncio.run(self.grab_page_async(*args, **kwargs))

    async def grab_page_async(self, *args, **kwargs) -> ProductFields:
        """Асинхронная функция для сбора полей товара."""
        async def fetch_all_data(*args, **kwargs):
            """Динамически вызывает функции для каждого поля."""
            # Динамическое вызовы функций для каждого поля из args
            process_fields:list = list(args) or ['id_product',
                            'name',
                            'description_short',
                            'description',
                            'specification',
                            'local_image_path',
                            'id_category_default',
                            'additional_category',
                            'default_image_url',
                            'price']
            for filed_name in process_fields:
                function = getattr(self, filed_name, None)
                if function:
                    await function(kwargs.get(filed_name, '')) # Просто вызываем с await, так как все функции асинхронные
        try:
            await fetch_all_data(*args, **kwargs)
            return self.fields
        except Exception as ex:
            logger.error(f"Ошибка в функции `fetch_all_data`", ex)
            return None


    async def error(self, field: str):
        """Обработчик ошибок для полей."""
        # Этот метод не используется в process_scenarios, оставлен как есть
        logger.debug(f"Ошибка заполнения поля {field}")


    @close_pop_up()
    async def additional_shipping_cost(self, value:Optional[Any] = None) -> bool:
        """Извлекает и устанавливает дополнительную стоимость доставки.
        Args:
        value (Any): это значение можно передать в словаре kwargs чеез ключ {additional_shipping_cost = `value`} при определении класса
        если `value` был передан - его значение подставляется в поле `ProductFields.additional_shipping_cost
        """
        try:
            # Получает значение через execute_locator
            self.fields.additional_shipping_cost = normalize_string(value or  await self.driver.execute_locator(self.product_locator.additional_shipping_cost) or '')
            return True
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `additional_shipping_cost`", ex)
            return


    @close_pop_up()
    async def delivery_in_stock(self, value:Optional[str] = None) -> bool:
        """Извлекает и устанавливает статус наличия на складе.

        Args:
        value (str): это значение можно передать в словаре kwargs через ключ {delivery_in_stock = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.delivery_in_stock`.
        """
        try:
            # Получает значение через execute_locator
            self.fields.delivery_in_stock = normalize_string( value or  await self.driver.execute_locator(self.product_locator.delivery_in_stock) or '' )
            return True
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `delivery_in_stock`", ex)
            return


    @close_pop_up()
    async def active(self, value:bool = True) -> bool:
        """Извлекает и устанавливает статус активности.

        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {active = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.active`.
        Принимаемое значениеЬ 1/0
        """
        try:
            # Получает значение через execute_locator
            self.fields.active = normalize_int( value or  await self.driver.execute_locator(self.product_locator.active) or 1)
            return True
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `active`", ex)
            return

    @close_pop_up()
    async def additional_delivery_times(self, value:Optional[str] = None) -> bool:
        """Извлекает и устанавливает дополнительное время доставки.

        Args:
        value (str): это значение можно передать в словаре kwargs через ключ {additional_delivery_times = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.additional_delivery_times`.
        """
        try:
            # Получает значение через execute_locator
            self.fields.additional_delivery_times = value or  await self.driver.execute_locator(self.product_locator.additional_delivery_times) or ''
            return True
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `additional_delivery_times`", ex)
            return


    @close_pop_up()
    async def advanced_stock_management(self, value:Optional[Any] = None) -> bool:
        """Извлекает и устанавливает статус расширенного управления запасами.
        DEPRECATED FIELD!
        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {advanced_stock_management = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.advanced_stock_management`.
        """
        return True


        # Записываем результат в поле `advanced_stock_management` объекта `ProductFields`
        self.fields.advanced_stock_management = value
        return True
    @close_pop_up()
    async def affiliate_short_link(self, value:Optional[str] = None) -> bool:
        """Извлекает и устанавливает короткую ссылку аффилиата.

        Args:
        value (str): это значение можно передать в словаре kwargs через ключ {affiliate_short_link = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.affiliate_short_link`.
        """
        try:
            # Получает значение через execute_locator
            self.fields.affiliate_short_link = value or  await self.driver.execute_locator(self.product_locator.affiliate_short_link) or ''
            return True
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `affiliate_short_link`", ex)
            return

    @close_pop_up()
    async def affiliate_summary(self, value:Optional[str] = None) -> bool:
        """Извлекает и устанавливает сводку аффилиата.

        Args:
        value (str): это значение можно передать в словаре kwargs через ключ {affiliate_summary = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.affiliate_summary`.
        """
        try:
            # Получает значение через execute_locator
            self.fields.affiliate_summary = normalize_string( value or  await self.driver.execute_locator(self.product_locator.affiliate_summary) or '' )
            return True
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `affiliate_summary`", ex)
            return


    @close_pop_up()
    async def affiliate_summary_2(self, value:Optional[Any] = None) -> bool:
        """Извлекает и устанавливает сводку аффилиата 2.

        Args:
        value (Any): это значение можно передать в словаре kwargs через ключ {affiliate_summary_2 = `value`} при определении класса.
        Если `value` был передан, его значение подставляется в поле `ProductFields.affiliate_summary_2`.
        """
        try:
            # Получает значение через execute_locator
            self.fields.affiliate_summary_2 = normalize_string(value or  await self.driver.execute_locator(self.product_locator.affiliate_summary_2) or '')
            return True
        except Exception as ex:
            logger.error(f"Ошибка получения значения в поле `affiliate_summary_2`", ex)
            return


    @close_pop_up()
    async def