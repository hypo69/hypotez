**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use This Code Block
=========================================================================================

Description
-------------------------
[Explanation of what the code does.]

Execution Steps
-------------------------
1. [Description of the first step.]
2. [Description of the second step.]
3. [Continue as needed...]

Usage Example
-------------------------

```python
    [Code usage example]
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".
```

## PrestaShop Endpoint Module Documentation

This document provides an overview of the `prestashop` module (`src/endpoints/prestashop/`) and its functionalities for interacting with the PrestaShop Web Service API.

## Purpose

The `prestashop` module provides a Python toolkit for interacting with the **PrestaShop Web Service API**. It encapsulates the logic for sending requests, handling responses, authentication, and data formatting, allowing developers to programmatically manage various resources of a PrestaShop store, with a particular focus on **products**.

**Key tasks addressed by the module:**

1.  **Unified API interaction:** Providing a convenient interface for performing standard CRUD operations (Create, Read, Update, Delete) and searching across various PrestaShop resources (products, categories, taxes, images, etc.).
2.  **Product management:** Specialized functions for creating and retrieving product data, including handling multilingual fields and associations (categories, features, images).
3.  **Data structuring:** Using the `ProductFields` class as a standardized container for product data, which is then transformed into a format understood by the PrestaShop API.
4.  **Data processing and formats:** Supporting working with XML and JSON formats, including automatic conversion between Python dictionaries and XML when necessary.
5.  **Image uploading:** Functions for uploading product images from both local files and URLs.
6.  **Configuration and flexibility:** Ability to easily switch between different PrestaShop instances (dev, prod) and data sources (environment variables, configuration files).

The module is tightly integrated with other parts of the system: it receives data prepared by the `graber` module as a `ProductFields` object, and uses the base `PrestaShop` class for actual API request sending.

## Key Components and Capabilities

*   **`PrestaShop` (`api.py`):**
    *   **Base class** for interacting with any PrestaShop API resource.
    *   Uses `requests.Session` for managing HTTP connections and authentication (Basic Auth with API key).
    *   `_exec` method: Central method for performing HTTP requests (GET, POST, PUT, DELETE) to the API, handling parameters (filters, sorting, limits, output format, language, etc.).
    *   Wrapper methods for standard operations: `create`, `read`, `write`, `unlink`, `search`.
    *   `ping` method: Checks API availability.
    *   `get_schema` method: Retrieves the data schema (fields and their types) for any API resource (useful for understanding the structure).
    *   `create_binary` method: Uploads binary data (e.g., images) via POST request (`multipart/form-data`).
    *   `upload_image_from_url` method: Utility for downloading an image from a URL and then uploading it through `create_binary`.
    *   Response handling: `_check_response` (checks HTTP status) and `_parse_response` (converts JSON/XML response to Python dictionary).
    *   Error handling: `_parse_response_error` (logs API errors).
    *   Configuration support through the nested `Config` class.
*   **`ProductFields` (`product_fields.py`):**
    *   **Data Transfer Object (DTO)** / **Data Container** for the product.
    *   Represents the product data structure, closely aligned with the requirements of the PrestaShop API.
    *   Initialized with default values from `product_fields_default_values.json` (through `_payload`).
    *   Provides properties (`@property`) for accessing and setting values of product fields (from `fields_list.txt`). Setters include basic data normalization.
    *   Supports **multilingual fields** (name, description, etc.) through the `_set_multilang_value` method, which stores data for different languages.
    *   Manages **associations**: Contains methods for adding (`..._append`) and clearing (`..._clear`) associations with categories, images, features, combinations, tags, etc.
    *   `to_dict()` method: Key method that transforms a `ProductFields` object into a Python dictionary ready for sending to the API. It filters empty values, converts all values to strings, and properly formats multilingual fields and associations.
*   **`PrestaProduct` (`product.py`):**
    *   **Class specializing in the `products` resource** of the API. Inherits from `PrestaShop`.
    *   `add_new_product(f: ProductFields)` method:
        *   Accepts a filled `ProductFields` object.
        *   Calls `_add_parent_categories` to automatically add all parent categories of the product.
        *   Calls `f.to_dict()` to get the data dictionary.
        *   Converts the dictionary to **XML** (`dict2xml`) for sending (PrestaShop API often requires XML for creating/updating complex resources like products).
        *   Calls the inherited method `self.create(\'products\', ...)` to send the POST request.
        *   Handles the response, and if successful, tries to upload the product image (using `f.local_image_path` or `f.default_image_url`).
        *   Returns data about the added product or an empty dictionary in case of an error.
    *   `get_product(id_product)` method: Retrieves data for a specific product by ID.
    *   `get_product_schema` method: Retrieves the schema for the `products` resource.
    *   `get_parent_category` method: Helper method for retrieving the parent category.
    *   `_add_parent_categories` method: Internal logic for building the category tree.

## Module Structure

```
src/endpoints/prestashop/
├── api.py                 # Base PrestaShop class for API
├── product.py             # PrestaProduct class for working with products
├── product_fields.py      # ProductFields class (DTO for product)
├── category.py            # (Presumably) Class for working with categories
├── utils/                 # Helper utilities
│   ├── dict2xml.py        # Python dict -> XML converter
│   └── xml2dict.py        # XML -> Python dict converter
├── product_fields/
│   ├── fields_list.txt    # List of all product fields
│   └── product_fields_default_values.json # Default values for fields
└── ...                    # Other possible modules (for orders, customers, etc.)
```

## Dependencies

*   `requests`: For performing HTTP requests.
*   `httpx`: (Imported `Response`, but not actively used in the code shown, `requests` dependency may be sufficient).
*   Standard Python libraries (`os`, `json`, `xml.etree.ElementTree`, `pathlib`, `typing`, etc.).

## Configuration

API configuration (store address and key) is set through the `Config` class inside `api.py` and `product.py`.

*   **`MODE`**: Determines which set of credentials to use ('dev', 'dev8', 'prod').
*   **`USE_ENV`**: If `True`, the `API_DOMAIN` and `API_KEY` keys are taken from the environment variables `HOST` and `API_KEY`.
*   **`API_DOMAIN`**, **`API_KEY`**: If `USE_ENV` is `False`, these values are taken from the `gs.credentials.presta.client...` object depending on the selected `MODE`.
*   **`POST_FORMAT`**: Determines the data format for sending (in `api.py`, but `PrestaProduct` always uses XML for creating products).

## Usage

### 1. Initialization

```python
from src.endpoints.prestashop.api import PrestaShop
from src.endpoints.prestashop.product import PrestaProduct

# Initialize the basic API client (if you need to work with different resources)
# Credentials will be taken from Config based on MODE
api = PrestaShop(api_domain=Config.API_DOMAIN, api_key=Config.API_KEY)

# Initialize the client for working with products
pp = PrestaProduct(api_domain=Config.API_DOMAIN, api_key=Config.API_KEY)

# Check connection
if api.ping():
    print("API is available!")
```

### 2. Working with ProductFields

```python
from src.endpoints.prestashop.product_fields import ProductFields

# Create a ProductFields object for the language with ID=2 (Hebrew)
pf = ProductFields(id_lang=2)

# Fill in the fields (many already have default values)
pf.id_supplier = 10 # Supplier ID
pf.reference = "TEST-SKU-123" # SKU
pf.price = 199.99
pf.name = "מוצר בדיקה" # Hebrew name
pf.description = "<p>תיאור מוצר כאן.</p>" # Hebrew description
pf.active = 1
pf.id_category_default = 5 # Main category

# Add associations
pf.additional_category_append(5) # Add the main category to associations
pf.additional_category_append(8) # Add another category

# Specify the path to the local image (if it was downloaded by the graber)
pf.local_image_path = "/path/to/downloaded/image.png"

# Get the dictionary for sending to the API
api_data_dict = pf.to_dict()
```

### 3. Adding a Product

```python
# Use the PrestaProduct instance (pp) and ProductFields (pf) from previous steps

try:
    added_product_info = pp.add_new_product(pf)
    if added_product_info:
        print(f"Product successfully added! ID: {added_product_info.id}")
        # Here added_product_info is a SimpleNamespace with the response from the API
    else:
        print("Error adding product.")
except Exception as e:
    print(f"An error occurred: {e}")

```

### 4. Retrieving Product Data

```python
try:
    product_id_to_get = 123 # ID of the product to retrieve
    product_data = pp.get_product(product_id_to_get)

    if product_data and 'products' in product_data:
        print("Product data:")
        # print(product_data['products'][0]) # Print the product dictionary
    else:
        print(f"Product with ID {product_id_to_get} not found or an error occurred.")
except Exception as e:
    print(f"An error occurred while getting the product: {e}")
```

### 5. Retrieving Resource Schema

```python
# Get the empty schema for products
blank_schema = pp.get_product_schema(schema='blank')
# print(blank_schema)

# Get the full schema for categories
full_category_schema = api.get_schema(resource='categories')
# print(full_category_schema)
```

## Data Format and XML

Although the PrestaShop API supports JSON for many operations (especially GET), for creating and updating complex resources, such as products (`products`), **XML format is often required**.

*   The `ProductFields` class, using the `to_dict()` method, creates a **Python dictionary**.
*   In the `PrestaProduct.add_new_product` method, this dictionary is **converted to XML** using the `dict2xml` utility.
*   This **XML is sent** to the API when creating a product (`POST /api/products`).
*   API responses (including errors) can come in both JSON and XML. The `_parse_response` method first attempts to parse the response as JSON, and then (if unsuccessful or the format is XML) uses `xml2dict` to convert it to a dictionary.

## Error Handling

*   The base `PrestaShop` class checks the HTTP status of the response (`_check_response`).
*   For statuses other than 200/201, `_parse_response_error` is called, which attempts to extract the error code and message from the response body (JSON or XML) and logs them.
*   Custom exceptions (`PrestaShopAuthenticationError`, `PrestaShopException`) are defined, but not actively generated in the code shown (they are logged through `logger.error`). The main error handling consists of logging and returning `None`, `False`, or `{}` from methods in case of failure.