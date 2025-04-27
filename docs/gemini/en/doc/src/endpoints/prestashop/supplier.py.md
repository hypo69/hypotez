# Module for working with PrestaShop suppliers
## Overview
The module contains the `PrestaSupplier` class for working with suppliers in PrestaShop. This class provides functionality to interact with PrestaShop's API, handling various operations related to suppliers, including:
-  Retrieving information about suppliers, including their name, address, contact details, and more.
-  Creating new suppliers.
-  Updating existing suppliers.
-  Deleting suppliers.
-  Managing supplier products.
-  Additional operations depending on the specific PrestaShop API version and features.

## Details
The `PrestaSupplier` class inherits from the `PrestaShop` class, which defines the core API interaction logic. This allows for a consistent way of handling API requests and responses. The module's purpose is to provide a simplified and more convenient way to manage suppliers within PrestaShop. 
This class provides a higher level of abstraction for the API interaction, handling the details of the API requests and responses. This approach makes the code more readable and maintainable.
## Classes
### `PrestaSupplier`
**Description**: This class is responsible for interacting with PrestaShop's API regarding suppliers.
**Inherits**: The class inherits from `PrestaShop`, which provides basic API interaction capabilities.

**Attributes**:
-  `credentials` (Optional[dict | SimpleNamespace], optional): A dictionary or SimpleNamespace object containing the `api_domain` and `api_key`. Defaults to None.
-  `api_domain` (Optional[str], optional): The API domain. Defaults to None.
-  `api_key` (Optional[str], optional): The API key. Defaults to None.

**Methods**:
-  `__init__`: Initializes the PrestaShop supplier instance.
-  **`get_suppliers`**: Retrieves a list of suppliers from the PrestaShop store.
-  **`get_supplier_by_id`**: Retrieves information about a specific supplier by its ID.
-  **`create_supplier`**: Creates a new supplier in the PrestaShop store.
-  **`update_supplier`**: Updates the information of an existing supplier.
-  **`delete_supplier`**: Deletes a supplier from the PrestaShop store.
-  **`get_supplier_products`**: Retrieves a list of products associated with a specific supplier.
-  **`add_product_to_supplier`**: Associates a product with a specific supplier.
-  **`remove_product_from_supplier`**: Disassociates a product from a specific supplier.
-  **`search_suppliers`**: Searches for suppliers based on specific criteria.
-  **`get_supplier_orders`**: Retrieves a list of orders associated with a specific supplier.
-  **`get_supplier_invoices`**: Retrieves a list of invoices associated with a specific supplier.
-  **`get_supplier_credits`**: Retrieves a list of credits associated with a specific supplier.
-  **`get_supplier_payments`**: Retrieves a list of payments associated with a specific supplier.
-  **`get_supplier_shipping_labels`**: Retrieves a list of shipping labels associated with a specific supplier.
-  **`get_supplier_shipping_tracking_numbers`**: Retrieves a list of shipping tracking numbers associated with a specific supplier.

## Functions

### `__init__`
**Purpose**: Initializes the `PrestaSupplier` object.
**Parameters**:
-  `credentials` (Optional[dict | SimpleNamespace], optional): A dictionary or SimpleNamespace object containing the `api_domain` and `api_key`. Defaults to None.
-  `api_domain` (Optional[str], optional): The API domain. Defaults to None.
-  `api_key` (Optional[str], optional): The API key. Defaults to None.

**Returns**: None
**Raises Exceptions**:
-  `ValueError`: If both `api_domain` and `api_key` are not provided.

**How the Function Works**:
- The function first checks if `credentials` are provided. If they are, it extracts the `api_domain` and `api_key` from the `credentials` dictionary or SimpleNamespace object.
- If `credentials` are not provided, it uses the `api_domain` and `api_key` parameters.
- If both `api_domain` and `api_key` are missing, it raises a `ValueError`.
- Finally, it calls the parent class's `__init__` method to initialize the API connection.

**Examples**:
```python
# Using credentials dictionary
credentials = {'api_domain': 'example.com', 'api_key': 'your_api_key'}
supplier = PrestaSupplier(credentials=credentials)

# Using api_domain and api_key parameters
supplier = PrestaSupplier(api_domain='example.com', api_key='your_api_key')
```