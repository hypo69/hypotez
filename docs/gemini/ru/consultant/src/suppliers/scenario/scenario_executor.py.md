### **Анализ кода модуля `scenario_executor.py`**

## \file hypotez/src/suppliers/scenario/scenario_executor.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
# Документация: https://github.com/hypo69/hypotez/blob/master/docs/ru/src/scenario/scenario_executor.py.md
"""
Модуль для работы с ассистентом программиста
=================================================

Модуль содержит класс :class:`CodeAssistant`, который используется для взаимодействия с различными AI-моделями
(например, Google Gemini и OpenAI) и выполнения задач обработки кода.

Пример использования
----------------------

>>>assistant = CodeAssistant(role='code_checker', lang='ru', model=['gemini'])
>>>assistant.process_files()
"""

import os
import sys
import requests
import asyncio
import time
import tempfile
from datetime import datetime
from math import log, prod
from pathlib import Path
from typing import Dict, List, Optional
import json

import header
from header import __root__
from src import gs
from src.utils.printer import pprint
from src.utils.jjson import j_loads, j_dumps
from src.endpoints.prestashop.product_async import PrestaProductAsync, ProductFields

from src.logger.logger import logger
from src.logger.exceptions import ProductFieldException

# Global journal for tracking scenario execution
_journal: dict = {'scenario_files': ''}
_journal['name'] = timestamp = gs.now

def dump_journal(s, journal: dict) -> None:
    """
    Сохраняет данные журнала в JSON-файл.

    Args:
        s (object): Инстанс поставщика.
        journal (dict): Словарь, содержащий данные журнала.

    Returns:
        None
    """
    _journal_file_path = Path(s.supplier_abs_path, '_journal', f"{journal['name']}.json")
    j_dumps(journal, _journal_file_path)

def run_scenario_files(s, scenario_files_list: List[Path] | Path) -> bool:
    """
    Выполняет список файлов сценариев.

    Args:
        s (object): Инстанс поставщика.
        scenario_files_list (List[Path] | Path): Список путей к файлам сценариев или одиночный путь к файлу.

    Returns:
        bool: True, если все сценарии выполнены успешно, False в противном случае.

    Raises:
        TypeError: Если scenario_files_list не является списком или объектом Path.
    """
    if isinstance(scenario_files_list, Path):
        scenario_files_list = [scenario_files_list]
    elif not isinstance(scenario_files_list, list):
        raise TypeError('scenario_files_list must be a list or a Path object.')
    scenario_files_list = scenario_files_list if scenario_files_list else s.scenario_files

    _journal['scenario_files'] = {}
    for scenario_file in scenario_files_list:
        _journal['scenario_files'][scenario_file.name] = {}
        try:
            if run_scenario_file(s, scenario_file):
                _journal['scenario_files'][scenario_file.name]['message'] = f'{scenario_file} completed successfully!'
                logger.success(f'Scenario {scenario_file} completed successfully!')
            else:
                _journal['scenario_files'][scenario_file.name]['message'] = f'{scenario_file} FAILED!'
                logger.error(f'Scenario {scenario_file} failed to execute!')
        except Exception as ex:
            logger.critical(f'An error occurred while processing {scenario_file}: {ex}')
            _journal['scenario_files'][scenario_file.name]['message'] = f'Error: {ex}'
    return True

def run_scenario_file(s, scenario_file: Path) -> bool:
    """
    Загружает и выполняет сценарии из файла.

    Args:
        s (object): Инстанс поставщика.
        scenario_file (Path): Путь к файлу сценария.

    Returns:
        bool: True, если сценарий выполнен успешно, False в противном случае.
    """
    try:
        scenarios_dict = j_loads(scenario_file)['scenarios']
        for scenario_name, scenario in scenarios_dict.items():
            s.current_scenario = scenario
            if run_scenario(s, scenario, scenario_name):
                logger.success(f'Scenario {scenario_name} completed successfully!')
            else:
                logger.error(f'Scenario {scenario_name} failed to execute!')
        return True
    except (FileNotFoundError, json.JSONDecodeError) as ex:
        logger.critical(f'Error loading or processing scenario file {scenario_file}: {ex}')
        return False

def run_scenarios(s, scenarios: Optional[List[dict] | dict] = None, _journal=None) -> List | dict | bool:
    """
    Выполняет список сценариев (НЕ ФАЙЛОВ).

    Args:
        s (object): Инстанс поставщика.
        scenarios (Optional[List[dict] | dict], optional): Принимает список сценариев или один сценарий в виде словаря. Defaults to None.

    Returns:
        List | dict | bool: Результат выполнения сценариев или False в случае ошибки.

    Todo:
        Check the option when no scenarios are specified from all sides. For example, when s.current_scenario is not specified and scenarios are not specified.
    """
    if not scenarios:
        scenarios = [s.current_scenario]

    scenarios = scenarios if isinstance(scenarios, list) else [scenarios]
    res = []
    for scenario in scenarios:
        res = run_scenario(s, scenario)
        _journal['scenario_files'][-1][scenario] = str(res)
        dump_journal(s, _journal)
    return res

def run_scenario(supplier, scenario: dict, scenario_name: str, _journal=None) -> List | dict | bool:
    """
    Выполняет полученный сценарий.

    Args:
        supplier (object): Инстанс поставщика.
        scenario (dict): Словарь, содержащий детали сценария.
        scenario_name (str): Имя сценария.

    Returns:
        List | dict | bool: Результат выполнения сценария.

    Todo:
        Check the need for the scenario_name parameter.
    """
    s = supplier
    logger.info(f'Starting scenario: {scenario_name}')
    s.current_scenario = scenario
    d = s.driver
    d.get_url(scenario['url'])

    # Get list of products in the category
    list_products_in_category: list = s.related_modules.get_list_products_in_category(s)

    # No products in the category (or they haven't loaded yet)
    if not list_products_in_category:
        logger.warning('No product list collected from the category page. Possibly an empty category - ', d.current_url)
        return False

    for url in list_products_in_category:
        if not d.get_url(url):
            logger.error(f'Error navigating to product page at: {url}')
            continue  # <- Error navigating to the page. Skip

        # Grab product page fields
        grabbed_fields = s.related_modules.grab_product_page(s)
        f: ProductFields = asyncio.run(s.related_modules.grab_page(s))
        if not f:
            logger.error('Failed to collect product fields')
            continue

        presta_fields_dict, assist_fields_dict = f.presta_fields_dict, f.assist_fields_dict
        try:
            product: Product = Product(supplier_prefix=s.supplier_prefix, presta_fields_dict=presta_fields_dict)
            insert_grabbed_data(f)
        except Exception as ex:
            logger.error(f'Product {product.fields["name"][1]} could not be saved', ex)
            continue

    return list_products_in_category

async def insert_grabbed_data_to_prestashop(
    f: ProductFields, coupon_code: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None
) -> bool:
    """
    Вставляет товар в PrestaShop.

    Args:
        f (ProductFields): Экземпляр ProductFields, содержащий информацию о товаре.
        coupon_code (Optional[str], optional): Опциональный код купона. Defaults to None.
        start_date (Optional[str], optional): Опциональная дата начала акции. Defaults to None.
        end_date (Optional[str], optional): Опциональная дата окончания акции. Defaults to None.

    Returns:
        bool: True, если вставка прошла успешно, False в противном случае.
    """
    try:
        presta = PrestaShop()
        return await presta.post_product_data(
            product_id=f.product_id,
            product_name=f.product_name,
            product_category=f.product_category,
            product_price=f.product_price,
            description=f.description,
            coupon_code=coupon_code,
            start_date=start_date,
            end_date=end_date,
        )

    except Exception as ex:
        logger.error('Failed to insert product data into PrestaShop: ', ex)
        return False
```

## **Анализ кода модуля `scenario_executor.py`**

**Качество кода:**
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Наличие docstrings для большинства функций.
  - Использование логирования через `logger`.
  - Четкая структура функций.
- **Минусы**:
  - docstrings не все на русском языке
  - Не везде указаны типы для переменных внутри функций.
  - Есть `Todo` в docstring.
  - Глобальные переменные `_journal`.
  - Использование `Union[]` вместо `|`
  - Нет обработки случая, когда `s.current_scenario` и `scenarios` не указаны.
  - В некоторых комментариях используются неточные формулировки (например, "Get list").

**Рекомендации по улучшению:**

- Перевести все docstrings на русский язык.
- Добавить аннотации типов для всех переменных, где это необходимо.
- Избавиться от `Todo` в docstring, реализовав указанные задачи или удалив их, если они больше не актуальны.
- Избегать использования глобальных переменных, таких как `_journal`. Рассмотреть возможность передачи этого словаря как аргумента в функции или использования класса для хранения состояния.
- Заменить `Union[]` на `|` для аннотации типов.
- Добавить обработку случая, когда не указаны ни `s.current_scenario`, ни `scenarios`, чтобы избежать возможных ошибок.
- Использовать более точные формулировки в комментариях, например, "Извлечение списка товаров" вместо "Get list".

**Оптимизированный код:**

```python
## \file hypotez/src/suppliers/scenario/scenario_executor.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
# Документация: https://github.com/hypo69/hypotez/blob/master/docs/ru/src/scenario/scenario_executor.py.md
"""
Исполнитель сценариев поставщиков
====================================
Модуль может исполнять различные сценарии, такие как:
- Сбор товаров в определенной каегории
- Сбор товаров по определенному фильтру
- Сбор товаров по определенному производителю
- ...
- и т.д.
```rst
.. module::  src.suppliers.scenario.scenario_executor
```
"""

import os
import sys
import requests
import asyncio
import time
import tempfile
from datetime import datetime
from math import log, prod
from pathlib import Path
from typing import Dict, List, Optional, Any
import json

import header
from header import __root__
from src import gs
from src.utils.printer import pprint
from src.utils.jjson import j_loads, j_dumps
from src.endpoints.prestashop.product_async import PrestaProductAsync, ProductFields

from src.logger.logger import logger
from src.logger.exceptions import ProductFieldException

# Global journal for tracking scenario execution
_journal: dict = {'scenario_files': ''}
_journal['name'] = timestamp = gs.now

def dump_journal(s: Any, journal: dict) -> None:
    """
    Сохраняет данные журнала в JSON-файл.

    Args:
        s (Any): Инстанс поставщика.
        journal (dict): Словарь, содержащий данные журнала.

    Returns:
        None
    """
    _journal_file_path: Path = Path(s.supplier_abs_path, '_journal', f"{journal['name']}.json")
    j_dumps(journal, _journal_file_path)

def run_scenario_files(s: Any, scenario_files_list: List[Path] | Path) -> bool:
    """
    Выполняет список файлов сценариев.

    Args:
        s (Any): Инстанс поставщика.
        scenario_files_list (List[Path] | Path): Список путей к файлам сценариев или одиночный путь к файлу.

    Returns:
        bool: True, если все сценарии выполнены успешно, False в противном случае.

    Raises:
        TypeError: Если scenario_files_list не является списком или объектом Path.
    """
    if isinstance(scenario_files_list, Path):
        scenario_files_list: List[Path] = [scenario_files_list]
    elif not isinstance(scenario_files_list, list):
        raise TypeError('scenario_files_list must be a list or a Path object.')
    scenario_files_list = scenario_files_list if scenario_files_list else s.scenario_files

    _journal['scenario_files'] = {}
    for scenario_file in scenario_files_list:
        _journal['scenario_files'][scenario_file.name] = {}
        try:
            if run_scenario_file(s, scenario_file):
                _journal['scenario_files'][scenario_file.name]['message'] = f'{scenario_file} completed successfully!'
                logger.success(f'Scenario {scenario_file} completed successfully!')
            else:
                _journal['scenario_files'][scenario_file.name]['message'] = f'{scenario_file} FAILED!'
                logger.error(f'Scenario {scenario_file} failed to execute!')
        except Exception as ex:
            logger.critical(f'An error occurred while processing {scenario_file}: {ex}')
            _journal['scenario_files'][scenario_file.name]['message'] = f'Error: {ex}'
    return True

def run_scenario_file(s: Any, scenario_file: Path) -> bool:
    """
    Загружает и выполняет сценарии из файла.

    Args:
        s (Any): Инстанс поставщика.
        scenario_file (Path): Путь к файлу сценария.

    Returns:
        bool: True, если сценарий выполнен успешно, False в противном случае.
    """
    try:
        scenarios_dict: dict = j_loads(scenario_file)['scenarios']
        for scenario_name, scenario in scenarios_dict.items():
            s.current_scenario = scenario
            if run_scenario(s, scenario, scenario_name):
                logger.success(f'Scenario {scenario_name} completed successfully!')
            else:
                logger.error(f'Scenario {scenario_name} failed to execute!')
        return True
    except (FileNotFoundError, json.JSONDecodeError) as ex:
        logger.critical(f'Error loading or processing scenario file {scenario_file}: {ex}')
        return False

def run_scenarios(s: Any, scenarios: Optional[List[dict] | dict] = None, _journal: dict = None) -> List | dict | bool:
    """
    Выполняет список сценариев (НЕ ФАЙЛОВ).

    Args:
        s (Any): Инстанс поставщика.
        scenarios (Optional[List[dict] | dict], optional): Принимает список сценариев или один сценарий в виде словаря. Defaults to None.

    Returns:
        List | dict | bool: Результат выполнения сценариев или False в случае ошибки.
    """
    if scenarios is None and s.current_scenario is None:
        logger.warning('No scenarios specified.')
        return False

    if not scenarios:
        scenarios: list = [s.current_scenario]

    scenarios = scenarios if isinstance(scenarios, list) else [scenarios]
    res: list = []
    for scenario in scenarios:
        res = run_scenario(s, scenario)
        _journal['scenario_files'][-1][scenario] = str(res)
        dump_journal(s, _journal)
    return res

def run_scenario(supplier: Any, scenario: dict, scenario_name: str, _journal: dict = None) -> List | dict | bool:
    """
    Выполняет полученный сценарий.

    Args:
        supplier (Any): Инстанс поставщика.
        scenario (dict): Словарь, содержащий детали сценария.
        scenario_name (str): Имя сценария.

    Returns:
        List | dict | bool: Результат выполнения сценария.
    """
    s: Any = supplier
    logger.info(f'Starting scenario: {scenario_name}')
    s.current_scenario = scenario
    d = s.driver
    d.get_url(scenario['url'])

    # Извлечение списка товаров в категории
    list_products_in_category: list = s.related_modules.get_list_products_in_category(s)

    # Нет товаров в категории (или они еще не загружены)
    if not list_products_in_category:
        logger.warning('No product list collected from the category page. Possibly an empty category - ', d.current_url)
        return False

    for url in list_products_in_category:
        if not d.get_url(url):
            logger.error(f'Error navigating to product page at: {url}')
            continue  # <- Error navigating to the page. Skip

        # Получение полей страницы товара
        grabbed_fields = s.related_modules.grab_product_page(s)
        f: ProductFields = asyncio.run(s.related_modules.grab_page(s))
        if not f:
            logger.error('Failed to collect product fields')
            continue

        presta_fields_dict: dict = f.presta_fields_dict
        assist_fields_dict: dict = f.assist_fields_dict
        try:
            product = Product(supplier_prefix=s.supplier_prefix, presta_fields_dict=presta_fields_dict)
            insert_grabbed_data(f)
        except Exception as ex:
            logger.error(f'Product {product.fields["name"][1]} could not be saved', ex)
            continue

    return list_products_in_category

async def insert_grabbed_data_to_prestashop(
    f: ProductFields, coupon_code: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None
) -> bool:
    """
    Вставляет товар в PrestaShop.

    Args:
        f (ProductFields): Экземпляр ProductFields, содержащий информацию о товаре.
        coupon_code (Optional[str], optional): Опциональный код купона. Defaults to None.
        start_date (Optional[str], optional): Опциональная дата начала акции. Defaults to None.
        end_date (Optional[str], optional): Опциональная дата окончания акции. Defaults to None.

    Returns:
        bool: True, если вставка прошла успешно, False в противном случае.
    """
    try:
        presta = PrestaShop()
        return await presta.post_product_data(
            product_id=f.product_id,
            product_name=f.product_name,
            product_category=f.product_category,
            product_price=f.product_price,
            description=f.description,
            coupon_code=coupon_code,
            start_date=start_date,
            end_date=end_date,
        )

    except Exception as ex:
        logger.error('Failed to insert product data into PrestaShop: ', ex)
        return False