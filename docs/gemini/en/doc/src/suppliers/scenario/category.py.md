# Module: Category

## Overview

This module provides classes for working with product categories, primarily for PrestaShop. It focuses on handling and processing category data, including crawling and building a hierarchical dictionary of categories.

## Details

This module utilizes the `PrestaCategoryAsync` class from the `src.endpoints.prestashop` module to interact with PrestaShop's category data. It leverages Selenium WebDriver for webpage navigation and data extraction, and relies on `j_loads` and `j_dumps` from the `src.utils.jjson` module for safe JSON handling. The module also utilizes the `logger` from the `src.logger` module for logging events and errors during execution.

## Classes

### `Category`

**Description**: This class represents a category handler, specifically designed for product categories within PrestaShop. It inherits functionality from the `PrestaCategoryAsync` class, providing extended capabilities for category management.

**Inherits**: `PrestaCategoryAsync`

**Attributes**:

- `credentials` (Dict): A dictionary containing the API credentials for accessing category data.

**Methods**:

#### `__init__(self, api_credentials, *args, **kwargs)`

**Purpose**: Initializes a `Category` object, configuring it with the provided API credentials and inheriting functionality from the parent class.

**Parameters**:

- `api_credentials` (Dict): The API credentials for accessing category data.
- `*args`: Variable length argument list (unused).
- `**kwargs`: Keyword arguments (unused).

**Returns**: None.

**Raises Exceptions**: None.

#### `crawl_categories_async(self, url, depth, driver, locator, dump_file, default_category_id, category=None)`

**Purpose**: Asynchronously crawls categories recursively, building a hierarchical dictionary of categories and their associated information. 

**Parameters**:

- `url` (str): The URL of the category page to begin crawling.
- `depth` (int): The depth of the recursion.
- `driver` (Selenium WebDriver instance): The Selenium WebDriver instance for navigating the web pages.
- `locator` (str): The XPath locator for finding category links on the web pages.
- `dump_file` (str): The path to the JSON file where the results of the crawling will be saved.
- `default_category_id` (int): The default category ID associated with the current crawl.
- `category` (Dict, optional): An existing category dictionary to update or expand upon. Defaults to `None`.

**Returns**: Dict: The updated or new category dictionary, containing the hierarchical structure of categories and their information.

**Raises Exceptions**: Exception: If an error occurs during category crawling.

#### `crawl_categories(self, url, depth, driver, locator, dump_file, default_category_id, category={})`

**Purpose**: Recursively crawls categories, building a hierarchical dictionary of categories and their associated information. 

**Parameters**:

- `url` (str): The URL of the category page to begin crawling.
- `depth` (int): The depth of the recursion.
- `driver` (Selenium WebDriver instance): The Selenium WebDriver instance for navigating the web pages.
- `locator` (str): The XPath locator for finding category links on the web pages.
- `dump_file` (str): The path to the JSON file where the results of the crawling will be saved.
- `id_category_default` (int): The default category ID associated with the current crawl.
- `category` (Dict, optional): An existing category dictionary to update or expand upon. Defaults to an empty dictionary.

**Returns**: Dict: The updated or new category dictionary, containing the hierarchical structure of categories and their information.

**Raises Exceptions**: Exception: If an error occurs during category crawling.

#### `_is_duplicate_url(self, category, url)`

**Purpose**: Checks if a given URL already exists in the category dictionary.

**Parameters**:

- `category` (Dict): The category dictionary to check.
- `url` (str): The URL to check for duplicates.

**Returns**: bool: `True` if the URL is a duplicate, `False` otherwise.

**Raises Exceptions**: None.

## Functions

### `compare_and_print_missing_keys(current_dict, file_path)`

**Purpose**: Compares a provided dictionary with data loaded from a file and prints any missing keys.

**Parameters**:

- `current_dict` (Dict): The current dictionary to compare against the file data.
- `file_path` (str): The path to the file containing the data.

**Returns**: None.

**Raises Exceptions**: Exception: If an error occurs while loading data from the file.

**How the Function Works**:

1. The function attempts to load data from the specified `file_path` using `j_loads`.
2. If successful, it iterates through the keys in the data loaded from the file.
3. For each key, it checks if it exists in the `current_dict`.
4. If a key is not found in the `current_dict`, it is printed to the console.
5. If an error occurs during data loading, an error message is logged using the `logger` and the function returns.

**Examples**:

```python
current_dict = {'key1': 'value1', 'key2': 'value2'}
file_path = 'data.json'
compare_and_print_missing_keys(current_dict, file_path)
```

**Output**:

```
key3
key4
```

**Note**: This function is designed to be used for comparing two sets of data, for example, during testing or validation. 
It provides a way to identify any missing keys in the `current_dict` compared to the data loaded from the file.