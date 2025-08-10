## \file /src/suppliers/graber.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Graber Module: Collects information from product web pages.
=========================================================
Base class for collecting data from supplier HTML pages.
    Target page fields (`name`, `description`, `specification`, `reference`, `price`,...) are collected by the webdriver (class: [`Driver`](../webdriver)).
    The location of the field is determined by its locator. Locators are stored in JSON dictionaries in the `locators` directory of each supplier.
    ([details about locators](locators.ru.md))
     Supplier table:
              https://docs.google.com/spreadsheets/d/14f0PyQa32pur-sW2MBvA5faIVghnsA0hWClYoKpkFBQ/edit?gid=1778506526#gid=1778506526


## For non-standard field processing, simply override the function in your class.
Example:
```python
s = `suppler_prefix`
from src.suppliers import Graber
locator = j_loads(gs.path.src.suppliers / f{s} / 'locators' / 'product.json`)

class G(Graber):

    @close_pop_up()
    async def name(self, value:Optional[Any] = None) -> bool:
        self.product_fields.name = <Your implementation>
        )
    ```
```rst
.. module:: src.suppliers
```

List of fields: https://github.com/hypo69/hypotez/blob/master/src/endpoints/prestashop/product_fields/fields_list.txt
Locator: https://github.com/hypo69/hypotez/blob/master/docs/ru/src/suppliers/locator.md
Details about the locator: https://github.com/hypo69/hypotez/blob/master/src/webdriver/locator.md

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
    from src.webdriver.pydoll import Driver

from header import __root__
from src import gs
# from src.webdriver.selenium.driver import Driver
# from src.webdriver.firefox import Firefox
from src.endpoints.prestashop.product_fields import ProductFields
# from src.endpoints.prestashop.category_async import PrestaCategoryAsync
# from src.suppliers.scenario.scenario_executor import run_scenario as _runscenario, run_scenarios as _runscenarios, run_scenario_file as _run_scenario_file, run_scenario_files as _run_scenario_files
from src.endpoints.prestashop.product import PrestaProduct
from src.utils.jjson import j_loads, j_loads_ns, j_dumps
from src.utils.image import save_image, save_image_async, save_image_from_url_async
from src.utils.file import read_text_file, get_directory_names, get_filenames_from_directory, read_text_file_generator, recursively_get_file_path, save_text_file
from src.utils.string.normalizer import(
    normalize_string,
    normalize_int,
    normalize_float,
    normalize_boolean,
    normalize_sql_date,
    normalize_sku )
from src.logger.exceptions import ExecuteLocatorException
from src.utils.printer import pprint as print
from src.logger.logger import logger



# --- decorator.py ---

def close_pop_up() -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            instance = args[0]

            # Get the locator directly from the instance
            locator = instance.locator_for_decorator

            if locator:
                try:
                    await instance.driver.execute_locator(locator)
                except Exception as ex:
                    print(f'Error executing locator in decorator: {ex}')
                finally:
                    # Clear the locator in the instance, not in the global Config
                    instance.locator_for_decorator = None

            return await func(*args, **kwargs)
        return wrapper
    return decorator

# --- decorator.py end ---

# --- config.py ---

class Config:
    """! Supplier configuration class."""

    # Memory optimization provided by slots=True in dataclass
    __slots__ = ('supplier_prefix', 'locator_for_decorator', 'required_fields', 'ENDPOINT', 'SCENARIOS_DIR')

    def __init__(self, *, supplier_prefix: str, locator_for_decorator: Optional[SimpleNamespace] = None):
        """
        Class initializer.
        The asterisk (*) in the arguments makes all subsequent parameters keyword-only,
        which is analogous to kw_only=True in dataclass.
        """
        # 1. Assign attributes that dataclass used to generate
        self.supplier_prefix: str = supplier_prefix
        self.locator_for_decorator: Optional[SimpleNamespace] = locator_for_decorator

        # 2. Initialize field with default value (analogous to default_factory)
        self.required_fields: List[str] = [
            'id_supplier', 'name', 'price', 'reference', 'description',
            'description_short', 'specification', 'default_image_url', 'local_image_path',
        ]

        _supplier_alias = self.supplier_prefix.replace('.', '_').replace('-', '_')
        # Assumes __root__ is globally defined
        self.ENDPOINT: Path = __root__ / 'src' / 'suppliers' / 'suppliers_list' / _supplier_alias
        self.SCENARIOS_DIR: Path = self.ENDPOINT / 'scenarios'

    @property
    def product_locators(self) -> SimpleNamespace:
        """Property for lazy loading product locators."""
        try:
            return j_loads_ns(self.ENDPOINT / 'locators' / 'product.json')
        except FileNotFoundError:
            # logger.error(f"Product locators not found: {self.ENDPOINT / 'locators' / 'product.json'}")
            print(f"ERROR: Product locators not found: {self.ENDPOINT / 'locators' / 'product.json'}")
            return SimpleNamespace()

    @property
    def category_locators(self) -> SimpleNamespace:
        """Property for lazy loading category locators."""
        try:
            return j_loads_ns(self.ENDPOINT / 'locators' / 'category.json')
        except FileNotFoundError:
            # logger.error(f"Category locators not found: {self.ENDPOINT / 'locators' / 'category.json'}")
            print(f"ERROR: Category locators not found: {self.ENDPOINT / 'locators' / 'category.json'}")
            return SimpleNamespace()
# --- config.py end ---

# --- graber.py ---
@dataclass(slots=True, kw_only=True)
class GraberBase:
    """! Base class for supplier grabber.

    Attrs:
        supplier_prefix (str): Supplier prefix.
        driver (Driver): Browser driver instance.
        locator_for_decorator (Optional[SimpleNamespace]): Locators for use in decorators.
        lang_index (int): Language index.
        config (Config): Configuration loaded by prefix.
        product_locator (SimpleNamespace): Locators for the product.
        product_fields (ProductFields): Fields collected from the product card.
    """

    supplier_prefix: str
    driver: 'Driver'
    locator_for_decorator: Optional[SimpleNamespace] = None
    lang_index: int = 1

    config: Config = field(init=False)
    product_locator: SimpleNamespace = field(init=False)
    product_fields: ProductFields = field(default_factory=lambda: ProductFields())

    def __post_init__(self):
        self.config = Config(supplier_prefix=self.supplier_prefix, locator_for_decorator=self.locator_for_decorator or None)
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
                    logger.error(f"Error calling function '{field_name}'", ex, exc_info=True)

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
            logger.error("Error in `grab_page_async`", ex, exc_info=True)
            return None



    def yield_scenarios_for_supplier(self, supplier_prefix: str, input_scenarios: Optional[List[Dict[str, Any]] | Dict[str, Any]] = None) -> Generator[Dict[str, Any], None, None]:
        """
        Generator that yields scenario dictionaries for a supplier.

        First processes scenarios passed in `input_scenarios`.
        If `input_scenarios` is empty or None, it searches and loads .json files
        from the supplier's scenarios directory.

        Args:
            supplier_prefix (str): Supplier prefix (identifier).
            input_scenarios (Optional[List[Dict] | Dict]): Directly passed
                scenarios (a single dictionary or a list of dictionaries).

        Yields:
            Generator[Dict[str, Any], None, None]: A generator that returns
                scenario dictionaries one by one.
        """
        processed_input = False # Flag indicating whether we have processed input data

        # 1. Processing directly passed scenarios
        if input_scenarios:
            scenario_list: List[Dict[str, Any]] = []
            if isinstance(input_scenarios, list):
                # Check that all list elements are dictionaries
                if all(isinstance(item, dict) for item in input_scenarios):
                    scenario_list = input_scenarios
                else:
                    logger.warning(f"Not all elements in input_scenarios list for '{supplier_prefix}' are dictionaries.")
            elif isinstance(input_scenarios, dict):
                scenario_list = [input_scenarios]
            else:
                logger.warning(f"Invalid type for input_scenarios for '{supplier_prefix}': {type(input_scenarios)}. Expected dict or list[dict].")

            if scenario_list: # If the list is not empty after checks
                logger.info(f"Processing {len(scenario_list)} scenarios passed directly for '{supplier_prefix}'.")
                for scenario_dict in scenario_list:
                     yield scenario_dict
                     processed_input = True # Mark that input data has been processed

        # 2. Loading from files if input data was not processed
        if not processed_input:
            scenarios_dir: Path = __root__ / 'src' / 'suppliers' / 'suppliers_list' / supplier_prefix / 'scenarios'
            logger.info(f"Input scenarios not provided/processed for '{supplier_prefix}', searching in: {scenarios_dir}")
            try:
                # Use your function to find files
                scenarios_files: List[Path | str] = recursively_get_file_path(scenarios_dir, '.json')

                if not scenarios_files:
                    logger.warning(f"No '.json' scenario files found in directory: {scenarios_dir}")
                    return # End the generator if no files

                logger.info(f"Found {len(scenarios_files)} scenario files for '{supplier_prefix}'.")
                for scenario_file_path in scenarios_files:
                    try:
                        # Check that it is a file
                        if not Path(scenario_file_path).is_file():
                             logger.warning(f"Skipping non-file path: {scenario_file_path}")
                             continue

                        # Load JSON
                        loaded_scenario: Optional[Dict[str, Any]] = j_loads(scenario_file_path)

                        # Check for successful loading and type
                        if loaded_scenario is not None and isinstance(loaded_scenario, dict):
                            logger.debug(f"Yielding scenario from file: {scenario_file_path}")
                            yield loaded_scenario # Yield the loaded scenario dictionary
                        else:
                            logger.error(f"Failed to load or result is not a dictionary: {scenario_file_path}")

                    except Exception as file_load_ex:
                        logger.error(f"Error processing scenario file {scenario_file_path}", file_load_ex, exc_info=True)

            except FileNotFoundError:
                logger.error(f"Scenario directory not found: {scenarios_dir}")
            except Exception as e:
                logger.error(f"Error searching for scenario files for '{supplier_prefix}'", e, exc_info=True)

    async def process_supplier_scenarios_async(self, input_scenarios:list = [], id_lang:Optional[int]=1) -> bool:
        """
        Example method that uses the yield_scenarios_for_supplier generator
        and calls run_scenario for each scenario.
        """
        all_results = []
        try:
            # Get the generator
            scenario_generator = self.yield_scenarios_for_supplier(self.supplier_prefix, input_scenarios)

            # Iterate through the scenarios yielded by the generator
            for scenarios in scenario_generator:
                # logger.info(f"Running scenario for '{supplier_prefix}'...")

                result = await self.process_scenarios(scenarios['scenarios'] if hasattr(scenarios, 'scenarios') else scenarios, id_lang )
                all_results.append(result) # Collect results (optional)

            logger.info(f"All scenarios for '{self.supplier_prefix}' processed.")
            return all_results # Return collected results

        except Exception as ex:
            logger.error(f"Error processing scenarios for '{self.supplier_prefix}'", ex, exc_info=True)
            return None # Or another error indication


    async def process_scenarios(self, input_scenarios: List[Dict[str, Any]] | Dict[str, Any], id_lang:Optional[int]=1) -> Optional[List[Any]]:
        """
        Executes one or more scenarios for the specified supplier.

        Args:
            input_scenarios (List[Dict[str, Any]] | Dict[str, Any]):
                Scenario data: either a list of scenario dictionaries,
                or a dictionary of the form {'scenarios': {'name': dict, ...}}.

        Returns:
            Optional[List[Any]]: A list of results from each scenario execution
                                 (e.g., lists of processed product URLs)
                                 or None in case of a critical error.
        """
        actual_scenarios_to_process: List[Dict[str, Any]] = []
        supplier_prefix = self.supplier_prefix
        # 1. Normalize input data -> actual_scenarios_to_process (list of scenario dictionaries)
        if isinstance(input_scenarios, list):
            # Input - list: validate content
            if all(isinstance(item, dict) for item in input_scenarios):
                actual_scenarios_to_process = input_scenarios
            else:
                logger.error(f"""Input list for '{supplier_prefix}' contains non-dictionaries.
                {print(input_scenarios)}
                """, None, False)
                ...
                return None # Return `None` for invalid input
        elif isinstance(input_scenarios, dict):
            # Input - dictionary: check structure {'scenarios': {'name': dict, ...}}
            if 'scenarios' in input_scenarios and isinstance(input_scenarios.get('scenarios'), dict):
                inner_scenarios_dict = input_scenarios['scenarios']
                # Check that all values in the nested dictionary are also dictionaries
                if all(isinstance(item, dict) for item in inner_scenarios_dict.values()):
                    # Extract scenario dictionaries from the values of the nested dictionary
                    actual_scenarios_to_process = list(inner_scenarios_dict.values())
                    logger.debug(f"Extracted {len(actual_scenarios_to_process)} scenarios from 'scenarios' key for '{supplier_prefix}'.")
                else:
                     logger.error(f"Inner 'scenarios' dictionary for '{supplier_prefix}' contains non-dictionaries in values.", None, False)
                     ...
                     return None # Return `None` for invalid structure
            else:
                # If it's a dictionary, but not of the expected structure, consider it an error
                logger.error(f"Input dictionary for '{supplier_prefix}' does not have the structure {{'scenarios': {{...}}}}.")
                ...
                # If a single dictionary needs to be processed as a single scenario, the logic would be here:
                # actual_scenarios_to_process = [input_scenarios]
                return None # Return `None` for invalid structure
        else:
            logger.error(f"Invalid input type for '{supplier_prefix}': {type(input_scenarios)}. Expected list or dict.")
            ...
            return None # Return `None` for invalid type

        # Check if there are scenarios after normalization
        if not actual_scenarios_to_process:
            logger.warning(f"No scenarios to process for '{supplier_prefix}' after normalization.")
            ...
            return [] # Return empty list

        # 2. Dynamic import (moved before the loop)
        try:
            module_path_str: str = f'src.suppliers.suppliers_list.{supplier_prefix}.scenario'
            scenario_module = importlib.import_module(module_path_str)
            if not hasattr(scenario_module, 'get_list_products_in_category'):
                logger.error(f"Function 'get_list_products_in_category' not found in {module_path_str}")
                ...
                return None
            get_list_func: Callable = getattr(scenario_module, 'get_list_products_in_category')
            if not callable(get_list_func):
                 logger.error(f"'get_list_products_in_category' in {module_path_str} is not a function")
                 ...
                 return None
        except (ModuleNotFoundError, ImportError, Exception) as import_err:
            logger.error(f"Error importing scenario module/function for '{supplier_prefix}'", import_err, exc_info=True)
            ...
            return None

        # --- Main scenario processing loop ---
        all_results: List[Any] = []
        d = self.driver # Assumes self.driver is initialized

        # Iterate over the prepared list of scenario dictionaries
        for scenario_data in actual_scenarios_to_process:
            # --- Start of outer loop body ---
            # 3. Get URL from current scenario dictionary
            if not isinstance(scenario_data, dict): # Additional type check
                logger.warning(f"Skipping non-dictionary in scenario list: {scenario_data}")
                ...
                continue

            scenario_url: Optional[str] = scenario_data.get('url')
            if not scenario_url:
                logger.warning(f"Scenario for '{supplier_prefix}' does not contain 'url' key. Skipping.")
                ...
                continue

            logger.info(f"Processing scenario for '{supplier_prefix}'. URL: {scenario_url}")

            # 4. Navigate to scenario URL
            if not d.get_url(scenario_url):
                logger.error(f"Failed to navigate to scenario URL: {scenario_url}", None, False)
                ...
                continue

            # 5. Call function to get product list
            list_products_in_category: Optional[List[str]] = None
            try:
                list_products_in_category = await get_list_func(d, self.category_locators)
            except Exception as func_ex:
                logger.error(f"Error executing get_list_products_in_category for URL {scenario_url}", func_ex, exc_info=True)
                ...
                continue

            # 6. Check function result
            if list_products_in_category is None:
                logger.warning(f'Function get_list_products_in_category returned None for URL {scenario_url}.')
                ...
                continue
            if not isinstance(list_products_in_category, list):
                 logger.error(f'Function get_list_products_in_category returned non-list: {type(list_products_in_category)} for URL {scenario_url}')
                 ...
                 continue
            if not list_products_in_category:
                logger.warning(f'No product links for URL {scenario_url}. Possibly an empty category.')
                ...
                continue

            for product_url in list_products_in_category:
                # --- Start of inner loop body ---
                if not isinstance(product_url, str) or not product_url:
                     logger.warning(f"Invalid product URL received: {product_url}. Skipping.")
                     ...
                     continue

                if not d.get_url(product_url):
                    logger.error(f'Error navigating to product page: {product_url}')
                    ...
                    continue


                f: Optional[ProductFields] = await self.grab_page_async(required_fields=self.config.required_fields, page_url=product_url)
                if not f:
                    logger.error(f'Failed to collect product fields from page {product_url}')
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
                    logger.error(f"Error adding additional categories{print(f)}")
                    ...
                except Exception as ex:
                    logger.error(f'Failed to save data\n {print(f)}\n from {product_url}', ex, exc_info=True)
                    ...
                product: PrestaProduct = PrestaProduct()
                product.add_new_product(f)
                all_results.append(f)
                # --- End of inner loop body ---

            # --- End of outer loop body ---

        # 8. Return aggregated results
        logger.info(f"Processing of all scenarios for '{supplier_prefix}' completed.")
        return all_results
        # --- End of function ---


    @close_pop_up()
    async def additional_shipping_cost(self, value:Optional[Any] = None) -> bool:
        """Fetch and set additional shipping cost.
        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {additional_shipping_cost = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.additional_shipping_cost` field.
        """
        try:
            self.product_fields.additional_shipping_cost = normalize_string(value or  await self.driver.execute_locator(self.product_locator.additional_shipping_cost) or '')
            return True if self.product_fields.additional_shipping_cost else False
        except Exception as ex:
            logger.error(f"Error getting value in `additional_shipping_cost` field", ex)
            ...
            return False


    @close_pop_up()
    async def delivery_in_stock(self, value:Optional[str] = None) -> bool:
        """Fetch and set delivery in stock status.

        Args:
        value (str): This value can be passed in the kwargs dictionary via the key {delivery_in_stock = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.delivery_in_stock` field.
        """
        try:
            self.product_fields.delivery_in_stock = normalize_string( value or  await self.driver.execute_locator(self.product_locator.delivery_in_stock) or '' )
            return True if self.product_fields.delivery_in_stock else False
        except Exception as ex:
            logger.error(f"Error getting value in `delivery_in_stock` field", ex)
            ...
            return False


    @close_pop_up()
    async def active(self, value:bool = True) -> bool:
        """Fetch and set active status.

        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {active = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.active` field.
        Accepted values: 1/0
        """
        try:
            self.product_fields.active = normalize_int( value or  await self.driver.execute_locator(self.product_locator.active) or 1)
            return True if self.product_fields.active in (1, True) else False
        except Exception as ex:
            logger.error(f"Error getting value in `active` field", ex)
            ...
            return False

    @close_pop_up()
    async def additional_delivery_times(self, value:Optional[str] = None) -> bool:
        """Fetch and set additional delivery times.

        Args:
        value (str): This value can be passed in the kwargs dictionary via the key {additional_delivery_times = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.additional_delivery_times` field.
        """
        try:
            self.product_fields.additional_delivery_times = value or  await self.driver.execute_locator(self.product_locator.additional_delivery_times) or ''
            return True if self.product_fields.additional_delivery_times else False
        except Exception as ex:
            logger.error(f"Error getting value in `additional_delivery_times` field", ex)
            ...
            return False


    @close_pop_up()
    async def advanced_stock_management(self, value:Optional[Any] = None) -> bool:
        """ -** DEPRECATED FIELD! **- Not used in Prestashop 1.7.8 and above.
        Args:
            value (Any): This value can be passed in the kwargs dictionary via the key {advanced_stock_management = `value`} when defining the class.
            If `value` was passed, its value is substituted into the `ProductFields.advanced_stock_management` field.
        """
        return False


    @close_pop_up()
    async def affiliate_short_link(self, value:Optional[str] = None) -> bool:
        """Fetch and set affiliate short link.

        Args:
        value (str): This value can be passed in the kwargs dictionary via the key {affiliate_short_link = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.affiliate_short_link` field.
        """
        try:
            self.product_fields.affiliate_short_link = value or  await self.driver.execute_locator(self.product_locator.affiliate_short_link) or ''
            return True if self.product_fields.affiliate_short_link else False
        except Exception as ex:
            logger.error(f"Error getting value in `affiliate_short_link` field", ex)
            ...
            return False

    @close_pop_up()
    async def affiliate_summary(self, value:Optional[str] = None) -> bool:
        """Fetch and set affiliate summary.

        Args:
        value (str): This value can be passed in the kwargs dictionary via the key {affiliate_summary = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.affiliate_summary` field.
        """
        try:
            self.product_fields.affiliate_summary = normalize_string( value or  await self.driver.execute_locator(self.product_locator.affiliate_summary) or '' )
            return True if self.product_fields.affiliate_summary else False
        except Exception as ex:
            logger.error(f"Error getting value in `affiliate_summary` field", ex)
            ...
            return False


    @close_pop_up()
    async def affiliate_summary_2(self, value:Optional[Any] = None) -> bool:
        """Fetch and set affiliate summary 2.

        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {affiliate_summary_2 = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.affiliate_summary_2` field.
        """
        try:
            self.product_fields.affiliate_summary_2 = normalize_string(value or  await self.driver.execute_locator(self.product_locator.affiliate_summary_2) or '')
            return True if self.product_fields.affiliate_summary_2 else False
        except Exception as ex:
            logger.error(f"Error getting value in `affiliate_summary_2` field", ex)
            ...
            return False


    @close_pop_up()
    async def affiliate_text(self, value:Optional[str] = None) -> bool:
        """Fetch and set affiliate text.

        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {affiliate_text = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.affiliate_text` field.
        """
        try:
            self.product_fields.affiliate_text = normalize_string( value or  await self.driver.execute_locator(self.product_locator.affiliate_text) or '')
            return True if self.product_fields.affiliate_text else False
        except Exception as ex:
            logger.error(f"Error getting value in `affiliate_text` field", ex)
            ...
            return False

    @close_pop_up()
    async def affiliate_image_large(self, value:Optional[str] = None) -> bool:
        """Fetch and set affiliate large image.

        Args:
        value (str): This value can be passed in the kwargs dictionary via the key {affiliate_image_large = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.affiliate_image_large` field.
        """
        try:
            self.product_fields.affiliate_image_large  = value or  await self.driver.execute_locator(self.product_locator.affiliate_image_large) or ''
            return True if self.product_fields.affiliate_image_large else False
        except Exception as ex:
            logger.error(f"Error getting value in `affiliate_image_large` field", ex)
            ...
            return False

    @close_pop_up()
    async def affiliate_image_medium(self, value:Optional[str] = None) -> bool:
        """Fetch and set affiliate medium image.

        Args:
        value (str): This value can be passed in the kwargs dictionary via the key {affiliate_image_medium = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.affiliate_image_medium` field.
        """
        try:
            self.product_fields.affiliate_image_medium = value or  await self.driver.execute_locator(self.product_locator.affiliate_image_medium) or ''
            return True if self.product_fields.affiliate_image_medium else False
        except Exception as ex:
            logger.error(f"Error getting value in `affiliate_image_medium` field", ex)
            ...
            return False

    @close_pop_up()
    async def affiliate_image_small(self, value:Optional[str] = None) -> bool:
        """Fetch and set affiliate small image.

        Args:
        value (str): This value can be passed in the kwargs dictionary via the key {affiliate_image_small = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.affiliate_image_small` field.
        """
        try:
            self.product_fields.affiliate_image_small = value or  await self.driver.execute_locator(self.product_locator.affiliate_image_small) or ''
            return True if self.product_fields.affiliate_image_small else False
        except Exception as ex:
            logger.error(f"Error getting value in `affiliate_image_small` field", ex)
            ...
            return False

    @close_pop_up()
    async def available_date(self, value:Optional[Any] = None) -> bool:
        """Fetch and set available date.

        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {available_date = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.available_date` field.
        """
        try:
            self.product_fields.available_date = value or  await self.driver.execute_locator(self.product_locator.available_date) or ''
            return True if self.product_fields.available_date else False
        except Exception as ex:
            logger.error(f"Error getting value in `available_date` field", ex)
            ...
            return False

    @close_pop_up()
    async def available_for_order(self, value:Optional[str] = None) -> bool:
        """Fetch and set available for order status.

        Args:
        value (str): This value can be passed in the kwargs dictionary via the key {available_for_order = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.available_for_order` field.
        """
        try:
            self.product_fields.available_for_order = value or  await self.driver.execute_locator(self.product_locator.available_for_order) or ''
            return True if self.product_fields.available_for_order else False
        except Exception as ex:
            logger.error(f"Error getting value in `available_for_order` field", ex)
            ...
            return False


    @close_pop_up()
    async def available_later(self, value:Optional[str] = None) -> bool:
        """Fetch and set available later status.

        Args:
        value (str): This value can be passed in the kwargs dictionary via the key {available_later = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.available_later` field.
        """
        try:
            self.product_fields.available_later = value or  await self.driver.execute_locator(self.product_locator.available_later) or ''
            return True  if self.product_fields.available_later else False
        except Exception as ex:
            logger.error(f"Error getting value in `available_later` field", ex)
            ...
            return False

    @close_pop_up()
    async def available_now(self, value:Optional[str] = 1) -> bool:
        """Fetch and set available now status.

        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {available_now = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.available_now` field.
        """
        try:
            self.product_fields.available_now = normalize_int(value or  await self.driver.execute_locator(self.product_locator.available_now) or 1)
            return True if self.product_fields.available_now else False
        except Exception as ex:
            logger.error(f"Error getting value in `available_now` field", ex)
            ...
            return False


    @close_pop_up()
    async def additional_categories(self, value: str | list = None) -> dict:
        """Set additional categories.

        This value can be passed in the kwargs dictionary via the key {additional_categories = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.additional_categories` field.

        Args:
        value (str | list, optional): String or list of categories. If not passed, an empty value is used.

        Returns:
        dict: Dictionary with category IDs.
        """
        self.product_fields.additional_categories = value
        return True if value else False


    @close_pop_up()
    async def cache_default_attribute(self, value:Optional[Any] = None) -> bool:
        """Fetch and set cache default attribute.

        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {cache_default_attribute = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.cache_default_attribute` field.
        """
        try:
            self.product_fields.cache_default_attribute = value or  await self.driver.execute_locator(self.product_locator.cache_default_attribute) or ''
            return True if self.product_fields.cache_default_attribute else False
        except Exception as ex:
            logger.error(f"Error getting value in `cache_default_attribute` field", ex)
            ...
            return False

    @close_pop_up()
    async def cache_has_attachments(self, value:Optional[int] = 0) -> bool:
        """Fetch and set cache has attachments status.

        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {cache_has_attachments = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.cache_has_attachments` field.
        """
        try:
            self.product_fields.cache_has_attachments = normalize_int(value or  await self.driver.execute_locator(self.product_locator.cache_has_attachments) or 0)
            return True if self.product_fields.cache_has_attachments else False
        except Exception as ex:
            logger.error(f"Error getting value in `cache_has_attachments` field", ex)
            ...
            return False


    @close_pop_up()
    async def cache_is_pack(self, value:Optional[str] = None) -> bool:
        """Fetch and set cache is pack status.

        Args:
        value (str): This value can be passed in the kwargs dictionary via the key {cache_is_pack = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.cache_is_pack` field.
        """
        try:
            self.product_fields.cache_is_pack = normalize_string(value or  await self.driver.execute_locator(self.product_locator.cache_is_pack) or '')
            return True if self.product_fields.cache_is_pack else False
        except Exception as ex:
            logger.error(f"Error getting value in `cache_is_pack` field", ex)
            ...
            return False

    @close_pop_up()
    async def condition(self, value:Optional[Any] = None) -> bool:
        """Fetch and set product condition.

        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {condition = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.condition` field.
        """
        try:
            self.product_fields.condition = normalize_string(value or  await self.driver.execute_locator(self.product_locator.condition) or 'new')
            return True if self.product_fields.condition else False
        except Exception as ex:
            logger.error(f"Error getting value in `condition` field", ex)
            ...
            return False


    @close_pop_up()
    async def customizable(self, value:Optional[Any] = None) -> bool:
        """Fetch and set customizable status.

        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {customizable = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.customizable` field.
        """
        try:
            self.product_fields.customizable = value or  await self.driver.execute_locator(self.product_locator.customizable) or ''
            return True if self.product_fields.customizable else False
        except Exception as ex:
            logger.error(f"Error getting value in `customizable` field", ex)
            ...
            return False


    @close_pop_up()
    async def date_add(self, value:Optional[str | datetime.date] = None) -> bool:
        """Fetch and set date added.

        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {date_add = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.date_add` field.
        """
        try:
            self.product_fields.date_add = normalize_sql_date( value or  await self.driver.execute_locator(self.product_locator.date_add) or gs.now)
            return True if self.product_fields.date_add else False
        except Exception as ex:
            logger.error(f"Error getting value in `date_add` field", ex)
            ...
            return False

    @close_pop_up()
    async def date_upd(self, value:Optional[str | datetime.date] = None) -> bool:
        """Fetch and set date updated.

        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {date_upd = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.date_upd` field.
        """
        try:
            self.product_fields.date_upd = normalize_sql_date( value or  await self.driver.execute_locator(self.product_locator.date_upd) or gs.now )
            return True if self.product_fields.date_upd else False
        except Exception as ex:
            logger.error(f"Error getting value in `date_upd` field", ex)
            ...
            return False

    @close_pop_up()
    async def delivery_out_stock(self, value:Optional[str] = None) -> bool:
        """Fetch and set delivery out of stock.

        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {delivery_out_stock = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.delivery_out_stock` field.
        """
        try:
            self.product_fields.delivery_out_stock = normalize_string( value or  await self.driver.execute_locator(self.product_locator.delivery_out_stock) or '')
            return True if self.product_fields.delivery_out_stock else False
        except Exception as ex:
            logger.error(f"Error getting value in `delivery_out_stock` field", ex)
            ...
            return False
        return True

    @close_pop_up()
    async def depth(self, value:Optional[float] = None) -> bool:
        """Fetch and set depth.

        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {depth = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.depth` field.
        """
        try:
            self.product_fields.depth = normalize_float( value or  await self.driver.execute_locator(self.product_locator.depth) or None )
            return True if self.product_fields.depth else False
        except Exception as ex:
            logger.error(f"Error getting value in `depth` field", ex)
            ...
            return False

    @close_pop_up()
    async def description(self, value:Optional[str] = None) -> bool:
        """Fetch and set description.

        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {description = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.description` field.
        """
        try:
            self.product_fields.description = normalize_string(value or  await self.driver.execute_locator(self.product_locator.description) or None)
            return True if self.product_fields.description else False
        except Exception as ex:
            logger.error(f"Error getting value in `description` \n ", ex)
            ...
            return False

    @close_pop_up()
    async def description_short(self, value:Optional[str] = '') -> bool:
        """Fetch and set short description.

        Args:
        value (atr): This value can be passed in the kwargs dictionary via the key {description_short = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.description_short` field.
        """
        try:
            self.product_fields.description_short = normalize_string(value or await self.driver.execute_locator(self.product_locator.description_short) or '')
            return True if self.product_fields.description_short else False
        except Exception as ex:
            logger.error(f"Error getting value in `description_short` field", ex)
            ...
            return False
        return True



    @close_pop_up()
    async def id_category_default(self, value:int) -> bool:
        """Fetch and set default category ID.

        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {id_category_default = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.id_category_default` field.
        """
        try:
            self.product_fields.id_category_default = normalize_int(value or await self.driver.execute_locator(self.product_locator.id_category_default) or None)
            return True if self.product_fields.id_category_default else False
        except Exception as ex:
            logger.error(f"Error getting value in `id_category_default` field", ex)
            ...
            return False
        return True

    @close_pop_up()
    async def id_default_combination(self, value:Optional[int] = None) -> bool:
        """Fetch and set default combination ID.

        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {id_default_combination = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.id_default_combination` field.
        """
        try:
            self.product_fields.id_default_combination = normalize_int(value or await self.driver.execute_locator(self.product_locator.id_default_combination) or 0)
            return True if self.product_fields.id_default_combination else False
        except Exception as ex:
            logger.error(f"Error getting value in `id_default_combination` field", ex)
            ...
            return False
        return True

    @close_pop_up()
    async def id_product(self, value:Optional[int] = None) -> bool:
        """Fetch and set product ID.

        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {id_product = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.id_product` field.
        """
        try:
            # Get the value of id_supplier, if not passed
            self.product_fields.id_product = normalize_int(await self.driver.execute_locator(self.product_locator.id_product), None)
            return True if self.product_fields.id_product else False
        except Exception as ex:
            logger.error(f"Error getting value in `id_product` field", ex)
            ...
            return False



    @close_pop_up()
    async def locale(self, value:Optional[Any] = None) -> bool:
        """Fetch and set locale.
        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {locale = `value`} when defining the class.
        If `value` was not passed, it is determined automatically.
        """

        # If value is not passed, determine locale automatically
        try:
            i18n = value or self.driver.locale
            # if not i18n and self.product_fields.name['language'][0]['value']:
            #     text = self.product_fields.name['language'][0]['value']
            #     i18n = detect(text)

            # Write the result to the `locale` field of the `ProductFields` object
            self.product_fields.locale = i18n
            return True if self.product_fields.locale else False
        except Exception as ex:
            logger.error(f"Error getting value in `locale` field", ex)
            ...
            return False



    @close_pop_up()
    async def id_default_image(self, value:Optional[int] = None) -> bool:
        """Fetch and set default image ID.
        Args:
            The value is automatically determined from Prestashop if not passed.
        """

        try:
            self.product_fields.id_default_image = value or  await self.driver.execute_locator(self.product_locator.id_default_image) or 0
            return True if self.product_fields.id_default_image else False
        except Exception as ex:
            logger.error(f"Error getting value in `id_default_image` field", ex)
            ...
            return False

    @close_pop_up()
    async def ean13(self, value:Optional[str] = None) -> bool:
        """Fetch and set EAN13 code.
        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {ean13 = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.ean13` field.
        """

        try:
            self.product_fields.ean13 = value or  await self.driver.execute_locator(self.product_locator.ean13) or ''
            return True if self.product_fields.ean13 else False
        except Exception as ex:
            logger.error(f"Error getting value in `ean13` field", ex)
            ...
            return False

    @close_pop_up()
    async def ecotax(self, value:Optional[int] = None) -> bool:
        """Fetch and set ecotax.
        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {ecotax = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.ecotax` field.
        """

        try:

            self.product_fields.ecotax = value or  await self.driver.execute_locator(self.product_locator.ecotax) or 0
            return True if self.product_fields.ecotax else False
        except Exception as ex:
            logger.error(f"Error getting value in `ecotax` field", ex)
            ...
            return False


    @close_pop_up()
    async def height(self, value:Optional[float] = None) -> bool:
        """Fetch and set height.
        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {height = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.height` field.
        """

        try:
            self.product_fields.height = value or  await self.driver.execute_locator(self.product_locator.height) or 0.0
            return True if self.product_fields.height else False
        except Exception as ex:
            logger.error(f"Error getting value in `height` field", ex)
            ...
            return  False

    @close_pop_up()
    async def how_to_use(self, value:Optional[str] = None) -> bool:
        """Fetch and set how to use.
        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {how_to_use = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.how_to_use` field.
        """
        try:
            self.product_fields.how_to_use = normalize_string(value or  await self.driver.execute_locator(self.product_locator.how_to_use) or '')
            return True if self.product_fields.how_to_use else False
        except Exception as ex:
            logger.error(f"Error getting value in `how_to_use` field", ex)
            ...
            return False

    @close_pop_up()
    async def id_manufacturer(self, value:Optional[int] = None) -> bool:
        """Fetch and set manufacturer ID.
        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {id_manufacturer = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.id_manufacturer` field.
        """
        try:
            self.product_fields.id_manufacturer = normalize_int(value or  await self.driver.execute_locator(self.product_locator.id_manufacturer) or None)
            return True if self.product_fields.id_manufacturer else False
        except Exception as ex:
            logger.error(f"Error getting value in `id_manufacturer` field", ex)
            ...
            return False


    @close_pop_up()
    async def id_supplier(self, value:Optional[Any] = None) -> bool:
        """Fetch and set supplier ID.
        Supplier code from the `suppliers` table
        Usually substituted into the locator
              "id_supplier": {
                "attribute": "1234",
                "by": "VALUE",
                "strategy_for_multiple_selectors": "find_first_match",
                "selector": null,
                "if_list": "first",
                "mandatory": true,
                "timeout": 2,
                "timeout_for_event": "presence_of_element_located",
                "event": null,
                "text_to_be_present_in_element":"","locator_description": "SKU ksp"
              },

              Supplier table:
              https://docs.google.com/spreadsheets/d/14f0PyQa32pur-sW2MBvA5faIVghnsA0hWClYoKpkFBQ/edit?gid=1778506526#gid=1778506526
        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {id_supplier = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.id_supplier` field.
        """
        try:
            self.product_fields.id_supplier = normalize_int(value or  self.product_locator.id_supplier.attribute)
            return True if self.product_fields.id_supplier else False
        except Exception as ex:
            logger.error(f"Error getting value in `id_supplier` field", ex)
            ...
            return False

    @close_pop_up()
    async def id_tax_rules_group (self, value:Optional[Any] = None) -> bool:
        """Fetch and set tax ID.
        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {id_tax_rules_group = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.id_tax_rules_group` field.
        """
        try:
            self.product_fields.id_tax_rules_group = normalize_int(value or  await self.driver.execute_locator(self.product_locator.id_tax_rules_group) or 1)
            return True if self.product_fields.id_tax_rules_group else False
        except Exception as ex:
            logger.error(f"Error getting value in `id_tax_rules_group ` field", ex)
            ...
            return False

    @close_pop_up()
    async def id_type_redirected(self, value:Optional[Any] = None) -> bool:
        """Fetch and set redirected type ID.
        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {id_type_redirected = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.id_type_redirected` field.
        """
        try:
            self.product_fields.id_type_redirected = normalize_int(value or  await self.driver.execute_locator(self.product_locator.id_type_redirected) or 0)
            return True if self.product_fields.id_type_redirected else False
        except Exception as ex:
            logger.error(f"Error getting value in `id_type_redirected` field", ex)
            ...
            return  False


    @close_pop_up()
    async def images_urls(self, value:Optional[Any] = None) -> bool:
        """Fetch and set image URLs.
        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {images_urls = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.images_urls` field.
        """
        try:
            self.product_fields.images_urls = normalize_string(value or  await self.driver.execute_locator(self.product_locator.images_urls) or '')
            return True if self.product_fields.images_urls else False
        except Exception as ex:
            logger.error(f"Error getting value in `images_urls` field", ex)
            ...
            return False

    @close_pop_up()
    async def indexed(self, value:Optional[Any] = None) -> bool:
        """Fetch and set indexed status.
        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {indexed = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.indexed` field.
        """
        try:
            self.product_fields.indexed = normalize_string(value or  await self.driver.execute_locator(self.product_locator.indexed) or '')
            return True if self.product_fields.indexed else False
        except Exception as ex:
            logger.error(f"Error getting value in `indexed` field", ex)
            ...
            return False


    @close_pop_up()
    async def ingredients(self, value:Optional[Any] = None) -> bool:
        """Fetch and set ingredients.
        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {ingredients = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.ingredients` field.
        """
        try:
            self.product_fields.ingredients = normalize_string(value or  await self.driver.execute_locator(self.product_locator.ingredients) or '')
            return True if self.product_fields.ingredients else False
        except Exception as ex:
            logger.error(f"Error getting value in `ingredients` field", ex)
            ...
            return False

    @close_pop_up()
    async def meta_description(self, value:Optional[Any] = None) -> bool:
        """Fetch and set meta description.
        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {meta_description = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.meta_description` field.
        """
        try:
            self.product_fields.meta_description = normalize_string(value or  await self.driver.execute_locator(self.product_locator.meta_description) or '')
            return True if self.product_fields.meta_description else False
        except Exception as ex:
            logger.error(f"Error getting value in `meta_description` field", ex)
            ...
            return  False


    @close_pop_up()
    async def meta_keywords(self, value:Optional[Any] = None) -> bool:
        """Fetch and set meta keywords.
        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {meta_keywords = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.meta_keywords` field.
        """
        try:
            self.product_fields.meta_keywords = normalize_string(value or  await self.driver.execute_locator(self.product_locator.meta_keywords) or '')
            return True if self.product_fields.meta_keywords else False
        except Exception as ex:
            logger.error(f"Error getting value in `meta_keywords` field", ex)
            ...
            return False


    @close_pop_up()
    async def meta_title(self, value:Optional[Any] = None) -> bool:
        """Fetch and set meta title.
        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {meta_title = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.meta_title` field.
        """
        try:
            self.product_fields.meta_title = normalize_string(value or  await self.driver.execute_locator(self.product_locator.meta_title) or '')
            return True if self.product_fields.meta_title else False
        except Exception as ex:
            logger.error(f"Error getting value in `meta_title` field", ex)
            return False

    @close_pop_up()
    async def is_virtual(self, value:Optional[Any] = None) -> bool:
        """Fetch and set virtual status.
        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {is_virtual = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.is_virtual` field.
        """
        try:
            self.product_fields.is_virtual = normalize_int(value or  await self.driver.execute_locator(self.product_locator.is_virtual) or 0)
            return True if self.product_fields.is_virtual else False
        except Exception as ex:
            logger.error(f"Error getting value in `is_virtual` field", ex)
            ...
            return False

    @close_pop_up()
    async def isbn(self, value:Optional[Any] = None) -> bool:
        """Fetch and set ISBN.

        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {isbn = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.isbn` field.
        """
        try:
            self.product_fields.isbn = normalize_string(value or  await self.driver.execute_locator(self.product_locator.isbn) or '')
            return True if self.product_fields.isbn else False
        except Exception as ex:
            logger.error(f"Error getting value in `isbn` field", ex)
            ...
            return False

    @close_pop_up()
    async def link_rewrite(self, value:Optional[Any] = None) -> bool:
        """Fetch and set link rewrite.

        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {link_rewrite = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.link_rewrite` field.
        """
        try:
            self.product_fields.link_rewrite = normalize_string(value or  await self.driver.execute_locator(self.product_locator.link_rewrite) or '')
            return True if self.product_fields.link_rewrite else False
        except Exception as ex:
            logger.error(f"Error getting value in `link_rewrite` field", ex)
            ...
            return False

    @close_pop_up()
    async def location(self, value:Optional[Any] = None) -> bool:
        """Fetch and set location.

        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {location = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.location` field.
        """
        try:
            self.product_fields.location = normalize_string(value or  await self.driver.execute_locator(self.product_locator.location) or '')
            return True if self.product_fields.location else False
        except Exception as ex:
            logger.error(f"Error getting value in `location` field", ex)
            ...
            return False

    @close_pop_up()
    async def low_stock_alert(self, value:Optional[Any] = None) -> bool:
        """Fetch and set low stock alert.

        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {low_stock_alert = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.low_stock_alert` field.
        """
        try:
            self.product_fields.low_stock_alert = normalize_string(value or  await self.driver.execute_locator(self.product_locator.low_stock_alert) or '')
            return True if self.product_fields.low_stock_alert else False
        except Exception as ex:
            logger.error(f"Error getting value in `low_stock_alert` field", ex)
            ...
            return False

    @close_pop_up()
    async def low_stock_threshold(self, value:Optional[Any] = None) -> bool:
        """Fetch and set low stock threshold.

        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {low_stock_threshold = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.low_stock_threshold` field.
        """
        try:
            self.product_fields.low_stock_threshold = normalize_string( value or  await self.driver.execute_locator(self.product_locator.low_stock_threshold) or '' )
            return True if self.product_fields.low_stock_threshold else False
        except Exception as ex:
            logger.error(f"Error getting value in `low_stock_threshold` field", ex)
            ...
            return False

    @close_pop_up()
    async def minimal_quantity(self, value:Optional[Any] = None) -> bool:
        """Fetch and set minimal quantity.

        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {minimal_quantity = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.minimal_quantity` field.
        """
        try:
            self.product_fields.minimal_quantity = normalize_int( value or  await self.driver.execute_locator(self.product_locator.minimal_quantity) or 1)
            return True if self.product_fields.minimal_quantity else False
        except Exception as ex:
            logger.error(f"Error getting value in `minimal_quantity` field", ex)
            ...
            return False

    @close_pop_up()
    async def mpn(self, value:Optional[Any] = None) -> bool:
        """Fetch and set MPN (Manufacturer Part Number).

        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {mpn = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.mpn` field.
        """
        try:

            self.product_fields.mpn = normalize_string( value or  await self.driver.execute_locator(self.product_locator.mpn) or '')
            return True if self.product_fields.mpn else False
        except Exception as ex:
            logger.error(f"Error getting value in `mpn` field", ex)
            ...
            return False

    @close_pop_up()
    async def name(self, value:Optional[str] = '') -> bool:
        """Fetch and set product name.

        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {name = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.name` field.
        """
        try:
            self.product_fields.name = normalize_string(value if value else await self.driver.execute_locator(self.product_locator.name))
            return True if self.product_fields.name else False
        except Exception as ex:
            logger.error(f"Error getting value in `name` field", ex)
            ...
            return False

    @close_pop_up()
    async def online_only(self, value:Optional[Any] = None) -> bool:
        """Fetch and set online-only status.

        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {online_only = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.online_only` field.
        """
        try:

            self.product_fields.online_only = normalize_int( value or  await self.driver.execute_locator(self.product_locator.online_only) or 0 )
            return True if self.product_fields.online_only else False
        except Exception as ex:
            logger.error(f"Error getting value in `online_only` field", ex)
            ...
            return False

    @close_pop_up()
    async def on_sale(self, value:Optional[Any] = None) -> bool:
        """Fetch and set on sale status.

        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {on_sale = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.on_sale` field.
        """
        try:
            self.product_fields.on_sale = value or  await self.driver.execute_locator(self.product_locator.on_sale) or ''
            return True if self.product_fields.on_sale else False
        except Exception as ex:
            logger.error(f"Error getting value in `on_sale` field", ex)
            ...
            return False

    @close_pop_up()
    async def out_of_stock(self, value:Optional[Any] = None) -> bool:
        """Fetch and set out of stock status.

        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {out_of_stock = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.out_of_stock` field.
        """
        try:

            self.product_fields.out_of_stock = normalize_string( value or  await self.driver.execute_locator(self.product_locator.out_of_stock) or '' )
            return True if self.product_fields.out_of_stock else False
        except Exception as ex:
            logger.error(f"Error getting value in `out_of_stock` field", ex)
            ...
            return  False

    @close_pop_up()
    async def pack_stock_type(self, value:Optional[Any] = None) -> bool:
        """Fetch and set pack stock type.

        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {pack_stock_type = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.pack_stock_type` field.
        """
        try:

            self.product_fields.pack_stock_type = normalize_string( value or  await self.driver.execute_locator(self.product_locator.pack_stock_type) or '')
            return True if self.product_fields.pack_stock_type else False
        except Exception as ex:
            logger.error(f'Error getting value in `pack_stock_type`', ex)
            ...
            return False

    @close_pop_up()
    async def price(self, value:Optional[Any] = None) -> bool:
        """Fetch and set price.

        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {price = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.price` field.
        """
        try:
            self.product_fields.price = normalize_float( value if value else await self.driver.execute_locator(self.product_locator.price))
            return True if self.product_fields.price else False
        except Exception as ex:
            logger.error(f'Error getting value in `price`', ex)
            ...
            return False

    @close_pop_up()
    async def product_type(self, value:Optional[Any] = None) -> bool:
        """Fetch and set product type.

        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {product_type = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.product_type` field.
        """
        try:

            self.product_fields.product_type = value or  await self.driver.execute_locator(self.product_locator.product_type) or ''
            return True if self.product_fields.product_type else False
        except Exception as ex:
            logger.error(f'Error getting value in `product_type`', ex)
            ...
            return False

    @close_pop_up()
    async def quantity(self, value:Optional[Any] = None) -> bool:
        """Fetch and set quantity.

        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {quantity = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.quantity` field.
        """
        try:
            self.product_fields.quantity = normalize_int( value or  await self.driver.execute_locator(self.product_locator.quantity) or 1 )
            return True if self.product_fields.quantity else False
        except Exception as ex:
            logger.error(f'Error getting value in `quantity`', ex)
            ...
            return False

    @close_pop_up()
    async def quantity_discount(self, value:Optional[Any] = None) -> bool:
        """Fetch and set quantity discount.

        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {quantity_discount = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.quantity_discount` field.
        """
        try:
            self.product_fields.quantity_discount = normalize_string( value or  await self.driver.execute_locator(self.product_locator.quantity_discount) or '' )
            return True if self.product_fields.quantity_discount else False
        except Exception as ex:
            logger.error(f'Error getting value in `quantity_discount`', ex)
            ...
            return False

    @close_pop_up()
    async def redirect_type(self, value:Optional[Any] = None) -> bool:
        """Fetch and set redirect type.

        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {redirect_type = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.redirect_type` field.
        """
        try:
            self.product_fields.redirect_type = value or  await self.driver.execute_locator(self.product_locator.redirect_type) or ''
            return True if self.product_fields.redirect_type else False
        except Exception as ex:
            logger.error(f'Error getting value in `redirect_type`', ex)
            ...
            return False

    @close_pop_up()
    async def reference(self, value:Optional[Any] = None) -> bool:
        """Fetch and set reference.

        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {reference = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.reference` field.
        """
        try:
            self.product_fields.reference = normalize_string( value or  await self.driver.execute_locator(self.product_locator.reference) or '')
            return True if self.product_fields.reference else False
        except Exception as ex:
            logger.error(f'Error getting value in `reference`', ex)
            ...
            return False

    @close_pop_up()
    async def show_condition(self, value:Optional[int] = None) -> bool:
        """Fetch and set show condition.

        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {show_condition = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.show_condition` field.
        """
        try:
            self.product_fields.show_condition = normalize_int( value or  await self.driver.execute_locator(self.product_locator.show_condition) or 1 )
            return True if self.product_fields.show_condition else False
        except Exception as ex:
            logger.error('Error getting value in `show_condition`', ex)
            ...
            return False

    @close_pop_up()
    async def show_price(self, value:Optional[int] = None) -> bool:
        """Fetch and set show price.

        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {show_price = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.show_price` field.
        """
        try:
            self.product_fields.show_price = normalize_int( value or  await self.driver.execute_locator(self.product_locator.show_price) or 1 )
            return True if self.product_fields.show_price else False
        except Exception as ex:
            logger.error('Error getting value in `show_price`', ex)
            ...
            return False

    @close_pop_up()
    async def state(self, value:Optional[str] = None) -> bool:
        """Fetch and set state.

        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {state = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.state` field.
        """
        try:
            self.product_fields.state = normalize_string( value or  await self.driver.execute_locator(self.product_locator.state))
            return True if self.product_fields.state else False
        except Exception as ex:
            logger.error('Error getting value in `state`', ex)
            ...
            return False


    @close_pop_up()
    async def text_fields(self, value:Optional[Any] = None) -> bool:
        """Fetch and set text fields.

        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {text_fields = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.text_fields` field.
        """
        try:
            self.product_fields.text_fields = value or  await self.driver.execute_locator(self.product_locator.text_fields) or ''
            return True if self.product_fields.text_fields else False
        except Exception as ex:
            logger.error('Error getting value in `text_fields`', ex)
            ...
            return False

    @close_pop_up()
    async def unit_price_ratio(self, value:Optional[Any] = None) -> bool:
        """Fetch and set unit price ratio.

        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {unit_price_ratio = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.unit_price_ratio` field.
        """
        try:

            self.product_fields.unit_price_ratio = value or  await self.driver.execute_locator(self.product_locator.unit_price_ratio) or ''
            return True if self.product_fields.unit_price_ratio else False
        except Exception as ex:
            logger.error('Error getting value in `unit_price_ratio`', ex)
            ...
            return False

    @close_pop_up()
    async def unity(self, value:Optional[str] = None) -> bool:
        """Fetch and set unity.

        Args:
            value (Any): This value can be passed in the kwargs dictionary via the key {unity = `value`} when defining the class.
            If `value` was passed, its value is substituted into the `ProductFields.unity` field.
        """
        try:
            self.product_fields.unity = normalize_string( value or  await self.driver.execute_locator(self.product_locator.unity) or '')
            return True if self.product_fields.unity else False
        except Exception as ex:
            logger.error(f'Error getting value in `unity`', ex)
            ...
            return False

    @close_pop_up()
    async def upc(self, value:Optional[str] = None) -> bool:
        """Fetch and set UPC.

        Args:
            value (Any): This value can be passed in the kwargs dictionary via the key {upc = `value`} when defining the class.
            If `value` was passed, its value is substituted into the `ProductFields.upc` field.
        """
        try:
            self.product_fields.upc = normalize_string( value or  await self.driver.execute_locator(self.product_locator.upc) or '')
            return True if self.product_fields.upc else False
        except Exception as ex:
            logger.error(f'Error getting value in `upc`', ex)
            ...
            return False

    @close_pop_up()
    async def uploadable_files(self, value:Optional[Any] = None) -> bool:
        """Fetch and set uploadable files.

        Args:
            value (Any): This value can be passed in the kwargs dictionary via the key {uploadable_files = `value`} when defining the class.
            If `value` was passed, its value is substituted into the `ProductFields.uploadable_files` field.
        """
        try:

            self.uploadable_files.upc = value or  await self.driver.execute_locator(self.product_locator.uploadable_files) or ''
            return True if self.uploadable_files.upc else False
        except Exception as ex:
            logger.error(f'Error getting value in `uploadable_files`', ex)
            ...
            return False

    @close_pop_up()
    async def default_image_url(self, value:Optional[str] = None) -> bool:
        """Fetch and set default image URL.

        Args:
            value (Any): This value can be passed in the kwargs dictionary via the key {default_image_url = `value`} when defining the class.
            If `value` was passed, its value is substituted into the `ProductFields.default_image_url` field.
        """
        try:
            self.product_fields.default_image_url = value or  await self.driver.execute_locator(self.product_locator.default_image_url) or ''
            return True if self.product_fields.default_image_url else False
        except Exception as ex:
            logger.error(f'Error getting value in `default_image_url`', ex)
            ...
            return False

    @close_pop_up()
    async def visibility(self, value:Optional[str] = None) -> bool:
        """Fetch and set visibility.

        Args:
            value (Any): This value can be passed in the kwargs dictionary via the key {visibility = `value`} when defining the class.
              In the ps_products table, the visibility field determines how the product will be visible on the site. Possible values for this field are usually:

            `both`: The product will be visible both in the catalog and in search results.
            `catalog`: The product will be visible only in the catalog, but will not appear in search results.
            `search`: The product will be visible only in search results, but will not appear in the catalog.
            `none`: The product will be hidden from all users and will not be visible in either the catalog or search results.
            These values allow you to control the visibility of products on the site, which can be useful for various marketing strategies or temporary hiding of products.
            If `value` was passed, its value is substituted into the `ProductFields.visibility` field.
        """
        try:
            self.product_fields.visibility = value or  await self.driver.execute_locator(self.product_locator.visibility) or 'both'
            return True if self.product_fields.visibility else False
        except Exception as ex:
            logger.error(f'Error getting value in `visibility`', ex)
            ...
            return False



    @close_pop_up()
    async def weight(self, value:Optional[float] = None) -> bool:
        """Fetch and set weight.

        Args:
            value (Any): This value can be passed in the kwargs dictionary via the key {weight = `value`} when defining the class.
            If `value` was passed, its value is substituted into the `ProductFields.weight` field.
        """
        try:
            self.product_fields.weight = normalize_int( value or  await self.driver.execute_locator(self.product_locator.weight) or 0  )
            return True if self.product_fields.weight else False
        except Exception as ex:
            logger.error('Error getting value in `weight`', ex)
            ...
            return False


    @close_pop_up()
    async def wholesale_price(self, value:Optional[float] = None) -> bool:
        """Fetch and set wholesale price.

        Args:
            value (Any): This value can be passed in the kwargs dictionary via the key {wholesale_price = `value`} when defining the class.
            If `value` was passed, its value is substituted into the `ProductFields.wholesale_price` field.
        """
        try:
            self.product_fields.wholesale_price = normalize_float( value or  await self.driver.execute_locator(self.product_locator.wholesale_price) or 0)
            return True if self.product_fields.wholesale_price else False
        except Exception as ex:
            logger.error('Error getting value in `wholesale_price`', ex)
            ...
            return False


    @close_pop_up()
    async def width(self, value:Optional[float] = None) -> bool:
        """Fetch and set width.

        Args:
            value (Any): This value can be passed in the kwargs dictionary via the key {width = `value`} when defining the class.
            If `value` was passed, its value is substituted into the `ProductFields.width` field.
        """
        try:
           self.product_fields.width = normalize_float( value or  await self.driver.execute_locator(self.product_locator.width) or 0)
           return True if self.product_fields.width else False
        except Exception as ex:
            logger.error('Error getting value in `width`', ex)
            ...
            return False


    @close_pop_up()
    async def specification(self, value:Optional[str|list] = None) -> bool:
        """Fetch and set specification.

        Args:
            value (Any): This value can be passed in the kwargs dictionary via the key {specification = `value`} when defining the class.
            If `value` was passed, its value is substituted into the `ProductFields.specification` field.
        """
        try:

            self.product_fields.specification = normalize_string( value or  await self.driver.execute_locator(self.product_locator.specification) or '')
            return True if self.product_fields.specification else False
        except Exception as ex:
            logger.error('Error getting value in `specification`', ex)
            ...
            return False


    @close_pop_up()
    async def link(self, value:Optional[str] = None) -> bool:
        """Fetch and set link.

        Args:
            value (Any): This value can be passed in the kwargs dictionary via the key {link = `value`} when defining the class.
            If `value` was passed, its value is substituted into the `ProductFields.link` field.
        """
        try:
            self.product_fields.link = value or  await self.driver.execute_locator(self.product_locator.link) or ''
            return True if self.product_fields.link else False
        except Exception as ex:
            logger.error('Error getting value in `link`', ex)
            ...
            return False


    @close_pop_up()
    async def byer_protection(self, value:Optional[str] = None) -> bool:
        """Fetch and set buyer protection.

        Args:
        value (str): This value can be passed in the kwargs dictionary via the key {byer_protection = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.byer_protection` field.
        """
        try:
            self.product_fields.byer_protection = normalize_string( value or  await self.driver.execute_locator(self.product_locator.byer_protection) or '' )
            return True if self.product_fields.byer_protection else False
        except Exception as ex:
            logger.error(f'Error getting value in `byer_protection`', ex)
            ...
            return False

    @close_pop_up()
    async def customer_reviews(self, value:Optional[Any] = None) -> bool:
        """Fetch and set customer reviews.

        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {customer_reviews = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.customer_reviews` field.
        """
        try:
            self.product_fields.customer_reviews = normalize_string( value or  await self.driver.execute_locator(self.product_locator.customer_reviews) or ''  )
            return True if self.product_fields.customer_reviews else False
        except Exception as ex:
            logger.error(f'Error getting value in `customer_reviews`', ex)
            ...
            return False


    @close_pop_up()
    async def link_to_video(self, value:Optional[Any] = None) -> bool:
        """Fetch and set link to video.
        """
        try:
            self.product_fields.link_to_video = value or  await self.driver.execute_locator(self.product_locator.link_to_video) or ''
            return True if self.product_fields.link_to_video else False
        except Exception as ex:
            logger.error(f'Error getting value in `link_to_video`', ex)
            ...
            return False

    @close_pop_up()
    async def local_image_path(self, value: Optional[str] = None) -> bool:
        """Fetch and save an image locally.

        The function gets the image `URL` or image bytes, saves the image in `PNG` format in the `tmp` directory
        and sets the path to the saved image in the `local_image_path` field. If a value is passed in the `value` parameter,
        it is written to the field without changes.

        Args:
            value (Optional[str], optional): Image URL, which can be passed in the class via the key `{local_image_path = value}`.
                If `value` was passed, its value is substituted into the `ProductFields.local_image_path` field.

        .. note::
            The image path leads to the `tmp` directory.

        .. todo::
            - How to pass a value from `**kwargs` to the `grab_product_page(**kwargs)` function?
            - How to pass a file path without hardcoding?

        """
        if value:
            self.product_fields.local_image_path = value
            return True

        img_path:str = Path(gs.path.tmp / f'{self.product_fields.id_supplier}_{self.product_fields.id_product}.png')

        self.product_fields.local_image_path = img_path  # <- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DEBUG

        try:
            if not self.product_fields.id_supplier:
                await self.id_supplier()
            # Get the result from the locator as `bytes` or `str`(url)
            raw_image = await self.driver.execute_locator(self.product_locator.default_image_url)
            if not raw_image:
                logger.error(f"Not image grabed. locator: {print(self.product_locator.default_image_url)}")
                return False

            raw_image = raw_image[0] if isinstance(raw_image, list) else raw_image

            if isinstance(raw_image, bytes):
                # If it's bytes, they are passed to save_image to save the image
                await save_image_async(raw_image, img_path)
                #save_image(raw_image, img_path)  # <- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  DEBUG

            elif isinstance(raw_image, str):
                # if it's a string, assume it's an image URL
                await save_image_from_url_async(raw_image,img_path)
            else:
                logger.debug("Unknown image data type", None, False)
                ...
                return False

        except Exception as ex:
            logger.error(f'Error saving image to `local_image_path` field', ex)
            ...
            return False
        return True if self.product_fields.local_image_path else False

    @close_pop_up()
    async def local_video_path(self, value:Optional[Any] = None) -> bool:
        """Fetch and save video locally.

        Args:
        value (Any): This value can be passed in the kwargs dictionary via the key {local_video_path = `value`} when defining the class.
        If `value` was passed, its value is substituted into the `ProductFields.local_video_path` field.
        """
        try:
            value = value or  await self.driver.execute_locator(self.product_locator.local_video_path) or ''

        except Exception as ex:
            logger.error(f'Error saving video to `local_video_path` field', ex)
            ...
            return
        return True

# --- graber.py end ---
