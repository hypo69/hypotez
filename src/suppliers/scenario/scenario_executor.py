# \file hypotez/src/suppliers/scenario/scenario_executor.py
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
from typing import Dict, List, Optional
import json

import header
from header import __root__
from src import gs
from src.utils.printer import pprint
from src.utils.jjson import j_loads, j_dumps
from src.endpoints.prestashop.product_async import PrestaProductAsync, ProductFields
from src.endpoints.prestashop.db import ProductCampaignsManager
from src.logger.logger import logger
from src.logger.exceptions import ProductFieldException

# Global journal for tracking scenario execution
_journal: dict = {'scenario_files': ''}
_journal['name'] = timestamp = gs.now

def dump_journal(s, journal: dict) -> None:
    """!
    Save the journal data to a JSON file.

    Args:
        s (object): Supplier instance.
        journal (dict): Dictionary containing the journal data.

    Returns:
        None
    """
    _journal_file_path = Path(s.supplier_abs_path, '_journal', f"{journal['name']}.json")
    j_dumps(journal, _journal_file_path)

def run_scenario_files(s, scenario_files_list: List[Path] | Path) -> bool:
    """!
    Executes a list of scenario files.

    Args:
        s (object): Supplier instance.
        scenario_files_list (List[Path] | Path): List of file paths for scenario files, or a single file path.

    Returns:
        bool: True if all scenarios were executed successfully, False otherwise.

    Raises:
        TypeError: If scenario_files_list is not a list or a Path object.
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
        except Exception as e:
            logger.critical(f'An error occurred while processing {scenario_file}: {e}')
            _journal['scenario_files'][scenario_file.name]['message'] = f'Error: {e}'
    return True

def run_scenario_file(s, scenario_file: Path) -> bool:
    """!
    Loads and executes scenarios from a file.

    Args:
        s (object): Supplier instance.
        scenario_file (Path): Path to the scenario file.

    Returns:
        bool: True if the scenario was executed successfully, False otherwise.
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
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.critical(f'Error loading or processing scenario file {scenario_file}: {e}')
        return False

def run_scenarios(s, scenarios: Optional[List[dict] | dict] = None, _journal=None) -> List | dict | bool:
    """!
    Executes a list of scenarios (NOT FILES).

    Args:
        s (object): Supplier instance.
        scenarios (Optional[List[dict] | dict], optional): Accepts a list of scenarios or a single scenario as a dictionary. Defaults to None.

    Returns:
        List | dict | bool: The result of executing the scenarios, or False in case of an error.

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
    """!
    Executes the received scenario.

    Args:
        supplier (object): Supplier instance.
        scenario (dict): Dictionary containing scenario details.
        scenario_name (str): Name of the scenario.

    Returns:
        List | dict | bool: The result of executing the scenario.

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
    """!
    Inserts the product into PrestaShop.

    Args:
        f (ProductFields): ProductFields instance containing the product information.
        coupon_code (Optional[str], optional): Optional coupon code. Defaults to None.
        start_date (Optional[str], optional): Optional start date for the promotion. Defaults to None.
        end_date (Optional[str], optional): Optional end date for the promotion. Defaults to None.

    Returns:
        bool: True if the insertion was successful, False otherwise.
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
