# Module src.endpoints.prestashop.category_async

## Overview

This module defines an asynchronous class `PrestaCategoryAsync` for managing categories in PrestaShop. It allows retrieving parent categories for a given category asynchronously.

## More details

This module provides an asynchronous interface for interacting with the PrestaShop API to manage categories. It uses the `PrestaShopAsync` class from the `src.endpoints.prestashop.api` module as a base class. The `PrestaCategoryAsync` class allows retrieving parent categories for a given category asynchronously, which can be useful for building category trees or breadcrumbs.

## Classes

### `PrestaCategoryAsync`

**Description**: Asynchronous class for managing categories in PrestaShop.

**Inherits**:
- `PrestaShopAsync`: Inherits asynchronous API interaction functionality from the `PrestaShopAsync` class.

**Attributes**:
- `api_domain` (str): The domain of the PrestaShop API.
- `api_key` (str): The API key for accessing the PrestaShop API.

**Working principle**:
The class initializes with the PrestaShop API domain and key. It provides an asynchronous method, `get_parent_categories_list_async`, to retrieve the parent categories of a given category. This method sends requests to the PrestaShop API and returns a list of parent category IDs.

#### `__init__`

```python
def __init__(self, credentials: Optional[Union[dict, SimpleNamespace]] = None, api_domain: Optional[str] = None, api_key: Optional[str] = None):
    """Инициализирует экземпляр класса PrestaCategoryAsync.

    Args:
        credentials (Optional[Union[dict, SimpleNamespace]], optional): Словарь или SimpleNamespace, содержащий учетные данные API (api_domain и api_key). Defaults to None.
        api_domain (Optional[str], optional): Домен API PrestaShop. Defaults to None.
        api_key (Optional[str], optional): Ключ API для доступа к PrestaShop API. Defaults to None.

    Raises:
        ValueError: Если параметры api_domain или api_key не предоставлены.
    """
```

#### `get_parent_categories_list_async`

```python
async def get_parent_categories_list_async(self, id_category: int|str , additional_categories_list: Optional[List[int] | int] = []) -> List[int]:
    """Асинхронно извлекает родительские категории для данной категории.

    Args:
        id_category (int | str): Идентификатор категории, для которой требуется получить родительские категории.
        additional_categories_list (Optional[List[int] | int], optional): Список дополнительных категорий для добавления в поиск. Defaults to [].

    Returns:
        List[int]: Список идентификаторов родительских категорий.
    """
```

## Functions

### `main`

```python
async def main():
    """

    """
```

**Purpose**: Placeholder function for asynchronous execution.

**Parameters**: None

**Returns**: None

**How the function works**:
This function is a placeholder for asynchronous execution. It currently does nothing.

**Examples**:
```python
async def main():
    ...
```