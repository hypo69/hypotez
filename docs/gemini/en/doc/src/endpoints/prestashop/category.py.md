# PrestaShop Category Management

## Overview

This module provides functionality for managing categories within PrestaShop. It contains the `PrestaCategory` class, which allows for retrieving information about parent categories.

## Details

The module utilizes the PrestaShop API to interact with the platform. The `PrestaCategory` class extends the `PrestaShop` base class, providing specific methods for category management.

The module's primary function is to obtain the list of parent categories for a given category ID. This information is crucial for navigating the category tree and understanding the hierarchy of products within PrestaShop.

## Classes

### `PrestaCategory`

**Description**: Class for managing categories in PrestaShop.

**Inherits**: `PrestaShop`

**Attributes**:
- `api_key` (str): API key for accessing PrestaShop.
- `api_domain` (str): Domain name of the PrestaShop instance.

**Methods**:
- `get_parent_categories_list(id_category: str | int, parent_categories_list: Optional[List[int | str]] = None) -> List[int | str]`: Retrieves parent categories from PrestaShop for a given category.

## Functions

### `get_parent_categories_list`

**Purpose**: Retrieves parent categories for a given category ID from PrestaShop.

**Parameters**:
- `id_category` (str | int): ID of the category to retrieve parent categories for.
- `parent_categories_list` (Optional[List[int | str]], optional): List of parent category IDs. Defaults to `None`.

**Returns**:
- `List[int | str]`: List of parent category IDs.

**Raises Exceptions**:
- `ValueError`: If the category ID is missing.
- `Exception`: If an error occurs while retrieving category data.

**How the Function Works**:
1. Verifies if the `id_category` is provided. If not, logs an error message and returns an empty list.
2. Calls the `get` method of the `PrestaShop` class to retrieve the category information from PrestaShop.
3. Extracts the `id_parent` value from the retrieved category data.
4. Appends the `id_parent` to the `parent_categories_list`.
5. Recursively calls itself with the `id_parent` as the `id_category` if the `id_parent` is greater than 2. Otherwise, returns the `parent_categories_list`.

**Examples**:
```python
>>> category = PrestaCategory(api_key='your_api_key', api_domain='your_domain')
>>> parent_categories = category.get_parent_categories_list(id_category='10')
>>> print(parent_categories)
[2, 10]
```

## Parameter Details

- `id_category` (str | int): The ID of the category for which to retrieve parent categories. It can be either a string or an integer.
- `parent_categories_list` (Optional[List[int | str]], optional): A list of parent category IDs that are already known. This is used for recursive calls to the function and should be left as `None` for the initial call.


## Examples

```python
>>> category = PrestaCategory(api_key='your_api_key', api_domain='your_domain')
>>> parent_categories = category.get_parent_categories_list(id_category=10)
>>> print(parent_categories)
[2, 10]

>>> category = PrestaCategory(api_key='your_api_key', api_domain='your_domain')
>>> parent_categories = category.get_parent_categories_list(id_category='10')
>>> print(parent_categories)
[2, 10]
```