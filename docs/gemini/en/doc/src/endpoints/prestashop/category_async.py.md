# PrestaCategoryAsync Module

## Overview

This module provides an asynchronous class `PrestaCategoryAsync` for interacting with PrestaShop categories. It inherits from `PrestaShopAsync` and extends its functionality for managing categories.

## Details

This module is part of the `hypotez` project, specifically within the `src.endpoints.prestashop` package. It facilitates asynchronous interactions with the PrestaShop API to manage product categories. The `PrestaCategoryAsync` class simplifies working with categories by providing asynchronous methods for retrieving parent categories.

## Classes

### `PrestaCategoryAsync`

**Description**: An asynchronous class for managing categories in PrestaShop.

**Inherits**: `PrestaShopAsync`

**Attributes**:
- `credentials`: (Optional[Union[dict, SimpleNamespace]], optional): Credentials for accessing the PrestaShop API. Defaults to `None`.
- `api_domain`: (Optional[str], optional): The domain of the PrestaShop API. Defaults to `None`.
- `api_key`: (Optional[str], optional): The API key for accessing the PrestaShop API. Defaults to `None`.

**Methods**:

- `get_parent_categories_list_async(id_category: int|str, additional_categories_list: Optional[List[int] | int] = []) -> List[int]`: Asynchronously retrieves parent categories for a given category.

## Functions

### `get_parent_categories_list_async`

**Purpose**: Asynchronously retrieves a list of parent categories for a given category ID.

**Parameters**:

- `id_category`: (int|str): The ID of the category for which to retrieve parent categories.
- `additional_categories_list`: (Optional[List[int] | int], optional): Additional category IDs to include in the search for parent categories. Defaults to an empty list `[]`.

**Returns**:

- `List[int]`: A list of parent category IDs for the specified category.

**Raises Exceptions**:

- `Exception`: If an error occurs while retrieving parent categories.

**How the Function Works**:

- The function first attempts to convert `id_category` to an integer. If it fails, an error message is logged.
- `additional_categories_list` is also converted to a list if necessary.
- The function then iterates through each category ID in `additional_categories_list`, including the `id_category`.
- For each category, it attempts to retrieve its parent category ID using the `read` method of the `PrestaShopAsync` base class.
- If the parent category ID is less than or equal to 2, it means that the top of the category tree has been reached, and the current `out_categories_list` is returned.
- If the parent category ID is greater than 2, it is appended to the `out_categories_list`.
- Finally, the function returns the list of parent category IDs in `out_categories_list`.

**Examples**:

```python
# Example 1: Retrieve parent categories for category with ID 10
parent_categories = await PrestaCategoryAsync(credentials).get_parent_categories_list_async(10)
print(f"Parent categories for category 10: {parent_categories}")

# Example 2: Retrieve parent categories for categories with IDs 10, 15, and 20
parent_categories = await PrestaCategoryAsync(credentials).get_parent_categories_list_async(10, [15, 20])
print(f"Parent categories for categories 10, 15, and 20: {parent_categories}")
```

## Inner Functions:

This module does not contain any inner functions within `get_parent_categories_list_async`.

## `main` Function

**Purpose**: The `main` function is intended for testing and demonstration purposes. It uses placeholders (`...`) for demonstration, which should be replaced with actual code when running.

**How it Works**:

- The `main` function is primarily a placeholder for testing the functionality of the `PrestaCategoryAsync` class. It is not designed for production use.
- The `...` placeholder suggests where you would normally insert the code for testing the `get_parent_categories_list_async` method and other functionalities of the class. 

**Example**:

```python
async def main():
    """
    Example function for testing PrestaCategoryAsync.
    """
    # Replace ... with actual code for testing
    presta_category = PrestaCategoryAsync(credentials)
    parent_categories = await presta_category.get_parent_categories_list_async(10)
    print(f"Parent categories for category 10: {parent_categories}")
```

**Note**: You should replace the placeholder `...` with your own test code for the `PrestaCategoryAsync` class when using this function.

## Parameter Details

- `credentials`: (Optional[Union[dict, SimpleNamespace]], optional): Credentials for accessing the PrestaShop API. This parameter can be a dictionary or a `SimpleNamespace` object containing the `api_domain` and `api_key` for accessing the PrestaShop API. Defaults to `None`, in which case you need to provide `api_domain` and `api_key` separately.

- `api_domain`: (Optional[str], optional): The domain of the PrestaShop API. This is the base URL for the PrestaShop API endpoint. Defaults to `None`.

- `api_key`: (Optional[str], optional): The API key for accessing the PrestaShop API. This key is used to authenticate requests to the PrestaShop API. Defaults to `None`.

- `id_category`: (int|str): The ID of the category for which to retrieve parent categories. This should be a valid category ID in the PrestaShop database.

- `additional_categories_list`: (Optional[List[int] | int], optional): Additional category IDs to include in the search for parent categories. This parameter allows you to specify other category IDs along with the primary `id_category`. It can be a single category ID or a list of IDs. Defaults to an empty list `[]`, meaning only the primary `id_category` is considered.

## Examples

```python
# Example 1: Retrieve parent categories using credentials dictionary
credentials = {
    'api_domain': 'https://example.prestashop.com',
    'api_key': 'YOUR_API_KEY'
}
presta_category = PrestaCategoryAsync(credentials)
parent_categories = await presta_category.get_parent_categories_list_async(10)
print(f"Parent categories for category 10: {parent_categories}")

# Example 2: Retrieve parent categories using api_domain and api_key separately
presta_category = PrestaCategoryAsync(api_domain='https://example.prestashop.com', api_key='YOUR_API_KEY')
parent_categories = await presta_category.get_parent_categories_list_async(10)
print(f"Parent categories for category 10: {parent_categories}")

# Example 3: Retrieve parent categories for multiple categories
presta_category = PrestaCategoryAsync(credentials)
parent_categories = await presta_category.get_parent_categories_list_async(10, [15, 20])
print(f"Parent categories for categories 10, 15, and 20: {parent_categories}")
```