# PrestaShop Customer Endpoint

## Overview

This module provides a Python class `PrestaCustomer` for interacting with the PrestaShop customer API. It allows you to perform operations like adding, deleting, updating, and retrieving customer information in a PrestaShop instance.

## Details

The `PrestaCustomer` class inherits from the base `PrestaShop` class, which provides the basic infrastructure for communicating with the PrestaShop API. This module utilizes the PrestaShop API to manage customer data within a PrestaShop e-commerce platform.

## Classes

### `PrestaCustomer`

**Description**: This class represents a customer in PrestaShop and provides methods for interacting with the PrestaShop customer API. 

**Inherits**: `PrestaShop`

**Attributes**: None

**Methods**:
- `__init__(self, credentials: Optional[dict | SimpleNamespace] = None, api_domain: Optional[str] = None, api_key: Optional[str] = None, *args, **kwargs)`: Initializes a PrestaCustomer object.

- `add_customer_PrestaShop(self, customer_name: str, customer_email: str) -> dict | None`: Adds a new customer to PrestaShop.

- `delete_customer_PrestaShop(self, customer_id: int) -> dict | None`: Deletes a customer from PrestaShop.

- `update_customer_PrestaShop(self, customer_id: int, customer_name: str) -> dict | None`: Updates a customer's name in PrestaShop.

- `get_customer_details_PrestaShop(self, customer_id: int) -> dict | None`: Retrieves details of a specific customer from PrestaShop.

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

**Purpose**: Initializes a PrestaCustomer object, setting up necessary API credentials for interaction with PrestaShop.

**Parameters**:

- `credentials` (Optional[dict | SimpleNamespace], optional): A dictionary or SimpleNamespace object containing `api_domain` and `api_key`. Defaults to `None`.
- `api_domain` (Optional[str], optional): The API domain. Defaults to `None`.
- `api_key` (Optional[str], optional): The API key. Defaults to `None`.

**How the Function Works**:

1. The function first checks if the `credentials` parameter is provided.
2. If `credentials` are provided, it extracts `api_domain` and `api_key` from them.
3. If `api_domain` and `api_key` are not provided as part of the `credentials` parameter, it checks if they were provided directly as function arguments.
4. If neither `credentials` nor `api_domain` and `api_key` are provided, it raises a `ValueError` indicating that both parameters are required.
5. The function then calls the parent class's `__init__` method, passing along the validated `api_domain` and `api_key` to initialize the base PrestaShop API connection.

**Examples**:

```python
# Example 1: Initializing with credentials dictionary
credentials = {'api_domain': 'example.com', 'api_key': 'your_api_key'}
prestacustomer = PrestaCustomer(credentials=credentials)

# Example 2: Initializing with separate parameters
prestacustomer = PrestaCustomer(api_domain='example.com', api_key='your_api_key')
```

### `add_customer_PrestaShop`

```python
    def add_customer_PrestaShop(self, customer_name: str, customer_email: str) -> dict | None:
        """ 
        """
```

**Purpose**: Adds a new customer to PrestaShop using the provided customer name and email address.

**Parameters**:

- `customer_name` (str): The name of the new customer.
- `customer_email` (str): The email address of the new customer.

**Returns**:

- `dict | None`: Returns a dictionary containing the response from the PrestaShop API if successful, otherwise returns `None`.

**Raises Exceptions**:

- `PrestaShopException`: If an error occurs during the API request.

**How the Function Works**:

1. The function constructs a payload containing the customer name and email.
2. It sends a POST request to the PrestaShop customer endpoint using the `self.post_request` method inherited from the `PrestaShop` class.
3. The function parses the response from the API and returns the parsed data as a dictionary if the request is successful.
4. If an error occurs during the request, it logs the error using `logger.error` and returns `None`.

**Examples**:

```python
# Add a new customer
customer_details = prestacustomer.add_customer_PrestaShop(customer_name='John Doe', customer_email='johndoe@example.com')

# Check if the customer was added successfully
if customer_details:
    print(f"New customer added: {customer_details}")
else:
    print("Error adding customer.")
```

### `delete_customer_PrestaShop`

```python
    def delete_customer_PrestaShop(self, customer_id: int) -> dict | None:
        """ 
        """
```

**Purpose**: Deletes a customer from PrestaShop using the provided customer ID.

**Parameters**:

- `customer_id` (int): The ID of the customer to be deleted.

**Returns**:

- `dict | None`: Returns a dictionary containing the response from the PrestaShop API if successful, otherwise returns `None`.

**Raises Exceptions**:

- `PrestaShopException`: If an error occurs during the API request.

**How the Function Works**:

1. The function constructs a URL for the specific customer using the provided `customer_id`.
2. It sends a DELETE request to the constructed URL using the `self.delete_request` method inherited from the `PrestaShop` class.
3. The function parses the response from the API and returns the parsed data as a dictionary if the request is successful.
4. If an error occurs during the request, it logs the error using `logger.error` and returns `None`.

**Examples**:

```python
# Delete a customer with ID 3
delete_result = prestacustomer.delete_customer_PrestaShop(customer_id=3)

# Check if the customer was deleted successfully
if delete_result:
    print("Customer deleted successfully.")
else:
    print("Error deleting customer.")
```

### `update_customer_PrestaShop`

```python
    def update_customer_PrestaShop(self, customer_id: int, customer_name: str) -> dict | None:
        """ 
        """
```

**Purpose**: Updates a customer's name in PrestaShop using the provided customer ID and new name.

**Parameters**:

- `customer_id` (int): The ID of the customer to be updated.
- `customer_name` (str): The new name for the customer.

**Returns**:

- `dict | None`: Returns a dictionary containing the response from the PrestaShop API if successful, otherwise returns `None`.

**Raises Exceptions**:

- `PrestaShopException`: If an error occurs during the API request.

**How the Function Works**:

1. The function constructs a payload containing the updated customer name.
2. It constructs a URL for the specific customer using the provided `customer_id`.
3. It sends a PUT request to the constructed URL with the payload using the `self.put_request` method inherited from the `PrestaShop` class.
4. The function parses the response from the API and returns the parsed data as a dictionary if the request is successful.
5. If an error occurs during the request, it logs the error using `logger.error` and returns `None`.

**Examples**:

```python
# Update the name of the customer with ID 4
update_result = prestacustomer.update_customer_PrestaShop(customer_id=4, customer_name='Updated Customer Name')

# Check if the customer was updated successfully
if update_result:
    print("Customer name updated successfully.")
else:
    print("Error updating customer name.")
```

### `get_customer_details_PrestaShop`

```python
    def get_customer_details_PrestaShop(self, customer_id: int) -> dict | None:
        """ 
        """
```

**Purpose**: Retrieves details of a specific customer from PrestaShop using the provided customer ID.

**Parameters**:

- `customer_id` (int): The ID of the customer whose details are to be retrieved.

**Returns**:

- `dict | None`: Returns a dictionary containing the customer's details if successful, otherwise returns `None`.

**Raises Exceptions**:

- `PrestaShopException`: If an error occurs during the API request.

**How the Function Works**:

1. The function constructs a URL for the specific customer using the provided `customer_id`.
2. It sends a GET request to the constructed URL using the `self.get_request` method inherited from the `PrestaShop` class.
3. The function parses the response from the API and returns the parsed data as a dictionary if the request is successful.
4. If an error occurs during the request, it logs the error using `logger.error` and returns `None`.

**Examples**:

```python
# Get details of the customer with ID 5
customer_details = prestacustomer.get_customer_details_PrestaShop(customer_id=5)

# Check if the customer details were retrieved successfully
if customer_details:
    print(f"Customer details: {customer_details}")
else:
    print("Error retrieving customer details.")
```

## Parameter Details

- `credentials` (Optional[dict | SimpleNamespace], optional): A dictionary or SimpleNamespace object containing `api_domain` and `api_key`, used for authentication with the PrestaShop API. Defaults to `None`.
- `api_domain` (Optional[str], optional): The domain of the PrestaShop instance, used to construct API endpoints. Defaults to `None`.
- `api_key` (Optional[str], optional): The API key for accessing the PrestaShop API, used for authorization. Defaults to `None`.
- `customer_name` (str): The name of the customer, used for adding or updating customer information.
- `customer_email` (str): The email address of the customer, used for adding or updating customer information.
- `customer_id` (int): The unique identifier of a customer in PrestaShop, used for deleting, updating, or retrieving customer information.

## Examples

```python
# Example Usage:
from src.endpoints.prestashop.customer import PrestaCustomer

# API Credentials
api_domain = 'your_prestashop_domain.com'
api_key = 'your_api_key'

# Create a PrestaCustomer instance
prestacustomer = PrestaCustomer(api_domain=api_domain, api_key=api_key)

# Add a new customer
new_customer_data = prestacustomer.add_customer_PrestaShop('John Doe', 'johndoe@example.com')
if new_customer_data:
    print("New customer added:", new_customer_data)

# Delete a customer
delete_result = prestacustomer.delete_customer_PrestaShop(3)
if delete_result:
    print("Customer deleted successfully.")

# Update a customer's name
update_result = prestacustomer.update_customer_PrestaShop(4, 'Updated Customer Name')
if update_result:
    print("Customer name updated successfully.")

# Get customer details
customer_details = prestacustomer.get_customer_details_PrestaShop(5)
if customer_details:
    print("Customer details:", customer_details)
```

This example demonstrates how to use the `PrestaCustomer` class to interact with the PrestaShop customer API for various operations.

## How the Module Works

The module utilizes the PrestaShop API to perform actions related to customer management. The `PrestaCustomer` class acts as a wrapper, simplifying the interaction with the API by providing convenient methods for common operations. Each method in this class utilizes the base `PrestaShop` class's API request methods (like `get_request`, `post_request`, `put_request`, and `delete_request`) to communicate with the PrestaShop server.