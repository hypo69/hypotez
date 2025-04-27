# AliCampaignEditor Module

## Overview

This module provides the editor for advertising campaigns. It provides functionalities to manage campaigns, such as adding, deleting, and updating products, categories, and campaign properties. The editor utilizes the `AliPromoCampaign` class to handle campaign data and the `AliCampaignGoogleSheet` class for integration with Google Sheets. The module also leverages the `j_loads` and `j_dumps` functions for working with JSON files and the `read_text_file` and `get_filenames_from_directory` functions for file operations.

## Details

The module is used to manage and edit various aspects of AliExpress campaigns. It allows for adding, deleting, and updating products, categories, and campaign properties. The editor works by reading data from JSON files and Google Sheets and updating them based on user input. The module also provides methods to check for affiliate links and rename product files if no match is found. The `AliCampaignEditor` class extends the `AliPromoCampaign` class, which handles campaign data, and utilizes the `AliCampaignGoogleSheet` class for Google Sheet integration. The module is crucial for maintaining and updating AliExpress campaign data.

## Table of Contents

### Classes

* [`AliCampaignEditor`](#alicampaigneditor)

### Functions

* [`delete_product`](#delete_product)
* [`update_product`](#update_product)
* [`update_campaign`](#update_campaign)
* [`update_category`](#update_category)
* [`get_category`](#get_category)
* [`list_categories`](#list_categories)
* [`get_category_products`](#get_category_products)

## Classes

### `AliCampaignEditor`

**Description**: This class represents an editor for AliExpress advertising campaigns. It provides functionalities to manage campaigns, such as adding, deleting, and updating products, categories, and campaign properties.

**Inherits**: `AliPromoCampaign`

**Attributes**:

* `campaign_name` (str): The name of the campaign.
* `language` (str): The language of the campaign.
* `currency` (str): The currency for the campaign.
* `campaign_file` (str | Path): Optionally load a `<lang>_<currency>.json` file from the campaign root folder. Defaults to `None`.
* `category_path` (Path): Path to the category folder.
* `base_path` (Path): Path to the base campaign directory.
* `google_sheet` (AliCampaignGoogleSheet): Instance of AliCampaignGoogleSheet for Google Sheets integration.

**Methods**:

* [`delete_product`](#delete_product)
* [`update_product`](#update_product)
* [`update_campaign`](#update_campaign)
* [`update_category`](#update_category)
* [`get_category`](#get_category)
* [`list_categories`](#list_categories)
* [`get_category_products`](#get_category_products)

#### `__init__`

**Purpose**: Initialize the `AliCampaignEditor` object with the given parameters.

**Parameters**:

* `campaign_name` (Optional[str]): The name of the campaign. Defaults to `None`.
* `language` (Optional[str | dict]): The language of the campaign. Defaults to 'EN'.
* `currency` (Optional[str]): The currency for the campaign. Defaults to 'USD'.
* `campaign_file` (Optional[str | Path]): Optionally load a `<lang>_<currency>.json` file from the campaign root folder. Defaults to `None`.

**Returns**: None

**Raises Exceptions**:

* `CriticalError`: If neither `campaign_name` nor `campaign_file` is provided.

**How the Function Works**:

The `__init__` method first checks if both `campaign_name` and `campaign_file` are `None`. If so, it raises a `CriticalError` as either parameter is required for initializing the campaign editor. If `campaign_file` is provided, the method loads the campaign data from the specified file. Otherwise, it initializes the campaign using the `campaign_name`, `language`, and `currency` parameters. After initializing the campaign, it sets up the `category_path`, `base_path`, and creates an instance of `AliCampaignGoogleSheet`.

**Examples**:

```python
# 1. by campaign parameters
>>> editor = AliCampaignEditor(campaign_name="Summer Sale", language="EN", currency="USD")

# 2. load from file
>>> editor = AliCampaignEditor(campaign_name="Summer Sale", campaign_file="EN_USD.JSON")
```

## Functions

### `delete_product`

**Purpose**: Delete a product from the campaign if it does not have an affiliate link.

**Parameters**:

* `product_id` (str): The ID of the product to be deleted.
* `exc_info` (bool): Whether to include exception information in logs. Defaults to `False`.

**Returns**: None

**Raises Exceptions**:

* `FileNotFoundError`: If the product file is not found.
* `Exception`: If an error occurs during the file renaming process.

**How the Function Works**:

The `delete_product` function first extracts the product ID from the provided `product_id` using the `extract_prod_ids` function. Then, it checks for the product in the `sources.txt` file located in the category path. If the product is found, it removes it from the list and saves the updated list back to the file. If the product is not found in the `sources.txt` file, it attempts to rename the product file from `sources/<product_id>.html` to `sources/<product_id>_.html`, indicating that the product has been removed.

**Examples**:

```python
>>> editor = AliCampaignEditor(campaign_name="Summer Sale")
>>> editor.delete_product("12345")
```

### `update_product`

**Purpose**: Update product details within a category.

**Parameters**:

* `category_name` (str): The name of the category where the product should be updated.
* `lang` (str): The language of the campaign.
* `product` (dict): A dictionary containing product details.

**Returns**: None

**How the Function Works**:

The `update_product` function calls the `dump_category_products_files` function to update the product details in the corresponding JSON file. The `dump_category_products_files` function handles the writing of product data to the JSON files.

**Examples**:

```python
>>> editor = AliCampaignEditor(campaign_name="Summer Sale")
>>> editor.update_product("Electronics", "EN", {"product_id": "12345", "title": "Smartphone"})
```

### `update_campaign`

**Purpose**: Update campaign properties such as `description`, `tags`, etc.

**Parameters**: None

**Returns**: None

**How the Function Works**:

The `update_campaign` function is a placeholder for updating campaign properties. It is not implemented in the provided code. The implementation would likely involve reading campaign properties from a JSON file or Google Sheet, updating them based on user input, and saving the updated data back to the source.

**Examples**:

```python
>>> editor = AliCampaignEditor(campaign_name="Summer Sale")
>>> editor.update_campaign()
```

### `update_category`

**Purpose**: Update the category in the JSON file.

**Parameters**:

* `json_path` (Path): Path to the JSON file.
* `category` (SimpleNamespace): Category object to be updated.

**Returns**:

* `bool`: True if update is successful, False otherwise.

**How the Function Works**:

The `update_category` function reads the JSON data from the specified file using the `j_loads` function, updates the `category` attribute in the data with the provided `category` object, and writes the updated JSON data back to the file using the `j_dumps` function. If an exception occurs during the process, it logs an error message and returns `False`. Otherwise, it returns `True`.

**Examples**:

```python
>>> category = SimpleNamespace(name="New Category", description="Updated description")
>>> editor = AliCampaignEditor(campaign_name="Summer Sale")
>>> result = editor.update_category(Path("category.json"), category)
>>> print(result)  # True if successful
```

### `get_category`

**Purpose**: Returns the `SimpleNamespace` object for a given category name.

**Parameters**:

* `category_name` (str): The name of the category to retrieve.

**Returns**:

* `Optional[SimpleNamespace]`: `SimpleNamespace` object representing the category or `None` if not found.

**How the Function Works**:

The `get_category` function first checks if the `category_name` attribute exists in the `campaign.category` object. If it exists, it retrieves the corresponding value using the `getattr` function and returns it as a `SimpleNamespace` object. If the attribute is not found, it logs a warning message and returns `None`. If an exception occurs during the process, it logs an error message and returns `None`.

**Examples**:

```python
>>> editor = AliCampaignEditor(campaign_name="Summer Sale")
>>> category = editor.get_category("Electronics")
>>> print(category)  # SimpleNamespace or None
```

### `list_categories`

**Purpose**: Retrieve a list of categories in the current campaign.

**Parameters**: None

**Returns**:

* `Optional[List[str]]`: A list of category names, or None if no categories are found.

**How the Function Works**:

The `list_categories` function first checks if the `category` attribute exists in the `campaign` object and if it is a `SimpleNamespace` object. If both conditions are met, it retrieves the keys of the `campaign.category` object using `vars` and converts them to a list. This list of keys represents the category names. If either of the conditions is not met, it logs a warning message and returns `None`. If an exception occurs during the process, it logs an error message and returns `None`.

**Examples**:

```python
>>> editor = AliCampaignEditor(campaign_name="Summer Sale")
>>> categories = editor.categories_list
>>> print(categories)  # ['Electronics', 'Fashion', 'Home']
```

### `get_category_products`

**Purpose**: Reads product data from JSON files for a specific category.

**Parameters**:

* `category_name` (str): The name of the category.

**Returns**:

* `Optional[List[SimpleNamespace]]`: List of `SimpleNamespace` objects representing products.

**How the Function Works**:

The `get_category_products` function first builds the path to the category products folder using the `base_path`, `category_name`, `language`, and `currency` attributes. It then uses the `get_filenames_from_directory` function to retrieve a list of JSON files in the category path. If JSON files are found, the function iterates through them and loads each file using the `j_loads_ns` function, converting the data to a `SimpleNamespace` object and appending it to the `products` list. Finally, it returns the list of products. If no JSON files are found, it logs an error message, calls the `process_category_products` function to prepare category products, and returns `None`.

**Examples**:

```python
>>> products = campaign.get_category_products("Electronics")
>>> print(len(products))
15
```