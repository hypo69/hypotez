## \file hypotez/src/suppliers/scenario/scenario_executor.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
Supplier Scenario Executor
====================================
This module can execute various scenarios, such as:
- Collecting products in a specific category
- Collecting products by a specific filter
- Collecting products by a specific manufacturer
- ...
- etc.
```rst
.. module::  src.suppliers.scenario.scenario_executor
```
"""

import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Any, TypeAlias
from types import SimpleNamespace

import header
from header import __root__
from src import gs
from src.utils.jjson import j_loads
from src.endpoints.prestashop.product import PrestaProduct

from src.logger.logger import logger


async def run_scenario_files(
                            s: 'Supplier',
                            d: 'Driver',
                            scenario_files_list: List[Path]|Path,
                            crawl_category_function: Any
                            ) -> bool:
    """
    The function executes a list of scenario files.

    Args:
        s (SupplierInstance): Supplier instance.
        d (d): Web driver instance.
        scenario_files_list (List[Path] | Path): List of paths to scenario files or a single file path.
        crawl_category_function (Any): Function for crawling categories, used in the scenario (e.g.,
                                      `get_list_products_in_category` from the supplier scenario).

    Returns:
        bool: `True` if all scenarios were executed successfully, otherwise `False`.

    Raises:
        TypeError: If `scenario_files_list` is not a list or a `Path` object.

    Example:
        >>> # Assuming 'supplier_instance', 'd_instance', 'my_crawl_function' are defined
        >>> # scenario_paths = [Path('path/to/scenario1.json'), Path('path/to/scenario2.json')]
        >>> # result = await run_scenario_files(supplier_instance, d_instance, scenario_paths, my_crawl_function)
        >>> # print(f'All scenarios executed successfully: {result}')
    """



    for scenario_file in scenario_files_list:
        try:
            if await run_scenario_file(s,d,scenario_file,crawl_category_function ):
                logger.success(f'Scenario {scenario_file} completed successfully.')
            else:
                logger.error(f'Scenario {scenario_file} failed to execute.')
        except Exception as ex:
            logger.critical(f'An error occurred while processing scenario {scenario_file}', ex, exc_info=True)
    return True # Return True if the loop finished (even if there were errors in individual files)


async def run_scenario_file(
                            s: 'Supplier',
                            d: 'Driver',
                            scenario_file: Path,
                            crawl_category_function: Any
                            ) -> bool:
    """
    The function loads and executes scenarios from a file.

    Args:
        s (SupplierInstance): Supplier instance.
        d (d): Web driver instance.
        scenario_file (Path): Path to the scenario file.
        crawl_category_function (Any): Function for crawling categories, used in the scenario.

    Returns:
        bool: `True` if the scenario was executed successfully, otherwise `False`.

    Example:
        >>> # Assuming 'supplier_instance', 'd_instance', 'scenario_file_path', 'my_crawl_function' are defined
        >>> # result = await run_scenario_file(supplier_instance, d_instance, scenario_file_path, my_crawl_function)
        >>> # print(f'Scenario file executed successfully: {result}')
    """
    scenarios_dict: Dict[str, Any]
    scenario_name: str
    scenario_data: Dict[str, Any]

    try:
        scenarios_dict = j_loads(scenario_file)
        if not scenarios_dict: # j_loads returns an empty dict on error
            logger.error(f'Failed to load or decode JSON from scenario file: {scenario_file}.')
            return False

        for scenario_name, scenario_data in scenarios_dict.items():
            s.current_scenario = scenario_data # Update current scenario in supplier object
            if await run_scenario(s,d,scenario_data,scenario_name,crawl_category_function):
                logger.success(f'Scenario "{scenario_name}" from file {scenario_file} completed successfully.')
            else:
                logger.error(f'Scenario "{scenario_name}" from file {scenario_file} failed to execute.')
        return True

    except Exception as ex:
        logger.critical(f'Unexpected error while executing scenario from file {scenario_file}', ex, exc_info=True)
        return False


async def run_scenarios(
                        s: 'Supplier',
                        d: 'Driver',
                        scenarios: Optional[List[dict] | dict],
                        crawl_category_function: Any
                        ) -> List | dict | bool:
    """
    The function executes a list of scenarios (NOT FILES).

    Args:
        s (SupplierInstance): Supplier instance.
        d (d): Web driver instance.
        scenarios (Optional[List[dict] | dict], optional): Accepts a list of scenarios or a single scenario as a dictionary.
                                                          Defaults to `s.current_scenario`.
        crawl_category_function (Any, optional): Function for crawling categories, used in the scenario.
                                                  Defaults to `None`.

    Returns:
        List | dict | bool: The result of executing the scenarios or `False` in case of an error.

    Todo:
        Check the option when scenarios are not specified from all sides. For example, when `s.current_scenario`
        is not specified and scenarios are not specified.

    Example:
        >>> # Assuming 'supplier_instance', 'd_instance' are defined
        >>> # my_scenario = {'url': 'http://example.com/category', 'name': 'MyCategoryScenario'}
        >>> # results = await run_scenarios(supplier_instance, d_instance, scenarios=my_scenario)
        >>> # print(f'Scenario execution results: {results}')
    """


    results: List[Any] = []
    scenarios = scenarios if isinstance(scenarios, list) else [scenarios]
    for scenario_item in scenarios:
        # Generate unique scenario name if missing

        result = await run_scenario(s, d, scenario_item,  crawl_category_function)
        results.append(result)
    return results


async def run_scenario(
                        s: 'Supplier',
                        d: 'Driver',
                        scenario: SimpleNamespace,
                        crawl_category_function: Any
                        ) -> List | dict | bool:
    """
    The function executes the given scenario.

    Args:
        s (SupplierInstance): Supplier instance.
        d (d): Web driver instance.
        scenario (Dict[str, Any]): Dictionary containing scenario details.
        scenario_name (str): Name of the scenario.
        crawl_category_function (Any, optional): Function for crawling categories, used in the scenario.
                                                  Defaults to `None`.

    Returns:
        List | dict | bool: The result of executing the scenario.

    Example:
        >>> # Assuming 'supplier_instance', 'd_instance', 'my_scenario_data', 'my_crawl_function' are defined
        >>> # result = await run_scenario(supplier_instance, d_instance, my_scenario_data, 'MyCategoryScenario', my_crawl_function)
        >>> # print(f'Scenario execution result: {result}')
    """

    list_products_in_category: List[str] | None = crawl_category_function(d, s.locator.category)
    f: ProductFields = None


    scenario_url: str = scenario.get('url')
    if not scenario_url:
        logger.error(f'Scenario "{scenario_name}" is missing a URL.')
        return False

    if not d.get_url(scenario_url):
        logger.error(f'Error navigating to scenario URL: {scenario_url} for scenario "{scenario_name}".')
        ...
        return False

    # Extract product list in category
    # If crawl_category_function is provided, use it, otherwise use the default supplier function
    if crawl_category_function:
        # Assumes crawl_category_function takes d and s.locators
        list_products_in_category = await crawl_category_function(d, s.locators)
    else:
        # Assumes s.related_modules.get_list_products_in_category expects d and s.locators
        list_products_in_category = await s.related_modules.get_list_products_in_category(d, s.locators)

    # If there are no products in the category (or they haven't loaded yet)
    if not list_products_in_category:
        logger.warning(f'Product list not collected from category page. Possibly an empty category: {d.current_url}')
        return False

    for product_url in list_products_in_category:
        if not d.get_url(product_url):
            logger.error(f'Error navigating to product page: {product_url}')
            continue  # Error navigating to page. Skip.

        # Capture product page fields
        # Assumes s.related_modules.grab_page is an asynchronous function
        f = await s.related_modules.grab_page(s)
        if not f:
            logger.error(f'Failed to collect product fields from page: {product_url}')
            continue

        presta_fields_dict, assist_fields_dict = f.presta_fields_dict, f.assist_fields_dict
        try:
            # Create ProductClass instance
            product = ProductClass(supplier_prefix=s.supplier_prefix, presta_fields_dict=presta_fields_dict)
            # Insert grabbed data into PrestaShop
            await insert_grabbed_data_to_prestashop(f)
        except Exception as ex:
            # Attempt to extract product name for logging
            product_name_for_log = ''
            if product and hasattr(product, 'fields') and 'name' in product.fields and isinstance(product.fields['name'], tuple):
                product_name_for_log = product.fields['name'][1]
            elif product and hasattr(product, 'name'): # If ProductClass has a 'name' attribute
                product_name_for_log = product.name

            logger.error(f'Product "{product_name_for_log}" cannot be saved.', ex, exc_info=True)
            continue

    return list_products_in_category # Return list of URLs that were processed


async def insert_grabbed_data_to_prestashop(
    f: ProductFields, coupon_code: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None
) -> bool:
    """
    The function adds a product to PrestaShop.

    Args:
        f (ProductFields): `ProductFields` instance containing product information.
        coupon_code (Optional[str], optional): Optional coupon code. Defaults to `None`.
        start_date (Optional[str], optional): Optional promotion start date. Defaults to `None`.
        end_date (Optional[str], optional): Optional promotion end date. Defaults to `None`.

    Returns:
        bool: `True` if the insertion was successful, otherwise `False`.

    Example:
        >>> # product_fields_instance = ProductFields(...)
        >>> # success = await insert_grabbed_data_to_prestashop(product_fields_instance, coupon_code='SAVE10')
        >>> # print(f'Product insertion into PrestaShop {"successful" if success else "failed"}.')
    """
    presta: PrestaShopClass
    try:
        # Create an instance of the class for interacting with the PrestaShop API
        presta = PrestaProductAsync() # Using PrestaProductAsync

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
        logger.error('Failed to insert product data into PrestaShop.', ex, exc_info=True)
        return False
