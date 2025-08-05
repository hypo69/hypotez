# PrestaShop Shop Endpoint Module

## Overview

This module defines the `PrestaShopShop` class, which provides an interface for interacting with PrestaShop shops through the PrestaShop API. The class inherits from the `PrestaShop` class, which provides basic API functionalities, and extends it with specific methods for managing PrestaShop shops.

## Details

The `PrestaShopShop` class is used to interact with PrestaShop shops for tasks like:

- **Retrieving shop information**: Accessing data about a specific shop, including its ID, name, and other attributes.
- **Creating new shops**: Setting up new PrestaShop shops within the PrestaShop platform.
- **Updating existing shops**: Modifying shop information like name, address, and other settings.

This module is crucial for projects that rely on PrestaShop for e-commerce operations. It provides a structured and consistent way to manage PrestaShop shops programmatically.

## Classes

### `PrestaShopShop`

**Description**: Class for interacting with PrestaShop shops through the PrestaShop API.

**Inherits**: `PrestaShop`

**Attributes**:

- `api_domain` (str): Domain of the PrestaShop API.
- `api_key` (str): API key for accessing the PrestaShop API.

**Methods**:

- `__init__(self, credentials: Optional[dict | SimpleNamespace] = None, api_domain: Optional[str] = None, api_key: Optional[str] = None, *args, **kwargs)`: Initializes the `PrestaShopShop` object.

**Principle of Operation**:

The `PrestaShopShop` class inherits the necessary API methods from the `PrestaShop` class and provides specific functionality for managing PrestaShop shops. The `__init__` method sets up the necessary connection parameters, using credentials provided through the `credentials` parameter or by directly passing `api_domain` and `api_key`. If no credentials are given, it raises a `ValueError` if both `api_domain` and `api_key` are not provided.

**How the Function Works**:

The `__init__` method performs the following actions:

1. **Retrieves API credentials**: If `credentials` are provided, it extracts `api_domain` and `api_key` from the `credentials` dictionary or SimpleNamespace object.
2. **Validates credentials**: Checks if both `api_domain` and `api_key` are present. If not, raises a `ValueError`.
3. **Initializes parent class**: Calls the `__init__` method of the parent `PrestaShop` class, passing the validated `api_domain` and `api_key` to set up the connection.

**Examples**:

```python
# Initializing a PrestaShopShop object using credentials
credentials = {
    'api_domain': 'example.prestashop.com',
    'api_key': 'your_api_key'
}
shop = PrestaShopShop(credentials=credentials)

# Initializing a PrestaShopShop object using direct parameters
shop = PrestaShopShop(api_domain='example.prestashop.com', api_key='your_api_key')
```

## Functions

### `j_loads(file_path: str | Path, namespace: bool = False, encoding: str = 'utf-8') -> dict | SimpleNamespace`

**Purpose**: Loads JSON data from a file.

**Parameters**:

- `file_path` (str | Path): Path to the JSON file.
- `namespace` (bool): If `True`, returns a `SimpleNamespace` object instead of a dictionary. Defaults to `False`.
- `encoding` (str): Encoding of the JSON file. Defaults to `utf-8`.

**Returns**:

- `dict | SimpleNamespace`: Dictionary or SimpleNamespace object containing the parsed JSON data.

**Raises Exceptions**:

- `PrestaShopException`: If an error occurs while reading or parsing the JSON file.

**How the Function Works**:

The `j_loads` function uses the `json.load` function to read and parse the JSON data from the specified file. If the `namespace` parameter is set to `True`, it converts the parsed dictionary to a `SimpleNamespace` object for easier attribute access.

**Examples**:

```python
# Loading JSON data from a file as a dictionary
data = j_loads('config.json')

# Loading JSON data from a file as a SimpleNamespace object
data = j_loads('config.json', namespace=True)
```

### `j_loads_ns(file_path: str | Path, encoding: str = 'utf-8') -> SimpleNamespace`

**Purpose**: Loads JSON data from a file and returns a `SimpleNamespace` object.

**Parameters**:

- `file_path` (str | Path): Path to the JSON file.
- `encoding` (str): Encoding of the JSON file. Defaults to `utf-8`.

**Returns**:

- `SimpleNamespace`: SimpleNamespace object containing the parsed JSON data.

**Raises Exceptions**:

- `PrestaShopException`: If an error occurs while reading or parsing the JSON file.

**How the Function Works**:

The `j_loads_ns` function is a wrapper for the `j_loads` function, setting the `namespace` parameter to `True` to ensure the function always returns a `SimpleNamespace` object.

**Examples**:

```python
# Loading JSON data from a file as a SimpleNamespace object
data = j_loads_ns('config.json')
```

## Parameter Details

- `credentials` (Optional[dict | SimpleNamespace]): Dictionary or SimpleNamespace object containing the PrestaShop API credentials, including `api_domain` and `api_key`.
- `api_domain` (Optional[str]): Domain of the PrestaShop API.
- `api_key` (Optional[str]): API key for accessing the PrestaShop API.
- `file_path` (str | Path): Path to the JSON file.
- `namespace` (bool): If `True`, returns a `SimpleNamespace` object instead of a dictionary. Defaults to `False`.
- `encoding` (str): Encoding of the JSON file. Defaults to `utf-8`.

## Examples

```python
# Initializing a PrestaShopShop object using credentials
credentials = {
    'api_domain': 'example.prestashop.com',
    'api_key': 'your_api_key'
}
shop = PrestaShopShop(credentials=credentials)

# Loading JSON data from a file as a dictionary
data = j_loads('config.json')

# Loading JSON data from a file as a SimpleNamespace object
data = j_loads_ns('config.json')
```

## Your Behavior During Code Analysis:

- Inside the code, you might encounter expressions between `<` `>`. For example: `<instruction for gemini model:Loading product descriptions into PrestaShop.>, <next, if available>. These are placeholders where you insert the relevant value.
- Always refer to the system instructions for processing code in the `hypotez` project (the first set of instructions you translated);
- Analyze the file's location within the project. This helps understand its purpose and relationship with other files. You will find the file location in the very first line of code starting with `## \\file /...`;
- Memorize the provided code and analyze its connection with other parts of the project;
- In these instructions, do not suggest code improvements. Strictly follow point 5. **Example File** when composing the response.