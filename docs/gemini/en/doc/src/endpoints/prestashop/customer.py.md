# Module `src.endpoints.prestashop.customer`

## Overview

The module `src.endpoints.prestashop.customer` provides a class for interacting with customers in PrestaShop. It includes functionalities for adding, deleting, updating, and retrieving customer details using the PrestaShop API.

## More details

This module simplifies customer management in PrestaShop by encapsulating API calls within a Python class. It handles authentication and provides methods for common customer-related operations. The code is designed to be modular and reusable, making it easier to integrate with other parts of the project that require customer management capabilities.

## Classes

### `PrestaCustomer`

**Description**: This class is designed to manage customer-related operations in PrestaShop. It inherits from the `PrestaShop` class, providing the basic API interaction capabilities.

**Inherits**: `PrestaShop`

**Attributes**:
- None

**Parameters**:
- `credentials` (Optional[dict | SimpleNamespace], optional): A dictionary or SimpleNamespace object containing the `api_domain` and `api_key`. Defaults to `None`.
- `api_domain` (Optional[str], optional): The API domain. Defaults to `None`.
- `api_key` (Optional[str], optional): The API key. Defaults to `None`.

**Working principle**:
The class initializes with API credentials and provides methods to perform CRUD (Create, Read, Update, Delete) operations on PrestaShop customers. It uses the `PrestaShop` class to handle the underlying API requests.

**Methods**: 
- `__init__`: Initializes the `PrestaCustomer` object.

## Class Methods

### `__init__`

```python
def __init__(self, 
                 credentials: Optional[dict | SimpleNamespace] = None, 
                 api_domain: Optional[str] = None, 
                 api_key: Optional[str] = None, 
                 *args, **kwargs):
    """Инициализация клиента PrestaShop.

    Args:
        credentials (Optional[dict | SimpleNamespace], optional): Словарь или объект SimpleNamespace с параметрами `api_domain` и `api_key`. Defaults to None.
        api_domain (Optional[str], optional): Домен API. Defaults to None.
        api_key (Optional[str], optional): Ключ API. Defaults to None.
    """
```

**Purpose**: Initializes the `PrestaCustomer` class with the necessary API credentials.

**Parameters**:
- `credentials` (Optional[dict | SimpleNamespace], optional): A dictionary or `SimpleNamespace` object containing `api_domain` and `api_key`. Defaults to `None`.
- `api_domain` (Optional[str], optional): The API domain. Defaults to `None`.
- `api_key` (Optional[str], optional): The API key. Defaults to `None`.

**How the function works**:
- The method first checks if credentials are provided as a dictionary or `SimpleNamespace`.
- If credentials are provided, it extracts `api_domain` and `api_key` from the credentials object.
- It raises a `ValueError` if both `api_domain` and `api_key` are not provided.
- Finally, it calls the `__init__` method of the superclass (`PrestaShop`) to initialize the API client.

**Examples**:
```python
# Example 1: Using api_domain and api_key directly
prestacustomer = PrestaCustomer(api_domain="your_api_domain", api_key="your_api_key")

# Example 2: Using a credentials dictionary
credentials = {"api_domain": "your_api_domain", "api_key": "your_api_key"}
prestacustomer = PrestaCustomer(credentials=credentials)

# Example 3: Using a SimpleNamespace object for credentials
credentials = SimpleNamespace(api_domain="your_api_domain", api_key="your_api_key")
prestacustomer = PrestaCustomer(credentials=credentials)
```