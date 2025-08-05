# PrestaProduct Module

## Overview

The `PrestaProduct` module (`src/endpoints/prestashop/product.py`) provides direct interaction with **products** via the PrestaShop Web Service API. It inherits from the base `PrestaShop` class (from `api.py`), which provides general functionality for working with the API (CRUD methods, request and response handling).

The `PrestaProduct` class adds specific logic for working with the `products` resource of the PrestaShop API, simplifying tasks such as:

1. **Getting the product schema:** Requesting the data structure for the `products` resource.
2. **Adding a new product:** Receiving product data in the format of a `ProductFields` object, preparing it (including category handling), and sending a request to create the product (`POST /api/products`).
3. **Getting information about the product:** Requesting data for a specific product by its ID (`GET /api/products/{id}`).
4. **Handling category hierarchy:** Automatically identifying and adding all parent categories for a product when it is created.
5. **Uploading images:** (Implicitly through `PrestaShop.create_binary` and `upload_image_from_url`) The ability to upload the main image for a newly created product.

The main usage scenario: after the `Graber` collects data from the supplier's page and fills the `ProductFields` object, this object is passed to the `add_new_product` method of the `PrestaProduct` class to create the corresponding product in the PrestaShop store.

## Key Features and Methods

* **Inheritance from `PrestaShop`:** Receives all basic functionality for interacting with the API (authentication, `_exec` request execution, basic CRUD methods, ping, etc.).
* **Configuration (`Config`):**
    * Uses the nested `Config` class to define `API_DOMAIN` and `API_KEY`.
    * Supports several modes (`MODE`): 'dev', 'dev8', 'prod', allowing easy switching between different PrestaShop instances.
    * Can read credentials from environment variables (`USE_ENV=True`) or from the configuration object `gs.credentials` (depending on `MODE`).
* **`__init__(self, api_key, api_domain, ...)`:**
    * Initializes the object, passing `api_key` and `api_domain` to the constructor of the parent class `PrestaShop`. If they are not explicitly passed, the values from `Config` are used.
* **`get_product_schema(self, resource_id=None, schema=None)`:**
    * Requests the data schema for the `products` resource from the PrestaShop API.
    * Allows you to get an empty schema (`schema='blank'`) for creating a new product or a full schema (by default).
* **`get_parent_category(self, id_category)`:**
    * Helper method to get the ID of the parent category for the specified `id_category`. Uses `self.read('categories', ...)` .
* **`_add_parent_categories(self, f: ProductFields)`:**
    * **Important internal method.** Accepts a `ProductFields` object.
    * Analyzes the list of categories already added to `f.additional_categories` (including `id_category_default`).
    * Recursively (through `get_parent_category`) finds **all** parent categories for each of the initial categories, going up the hierarchy to root categories (ID <= 2).
    * Adds **unique** found parent IDs back to `f.additional_categories`, ensuring that the product is linked to the entire category branch.
* **`get_product(self, id_product, **kwargs)`:**
    * Gets data for a specific product from PrestaShop by its ID.
    * Uses `self.read('products', resource_id=id_product)`.
    * Returns a dictionary with product data.
* **`add_new_product(self, f: ProductFields)`:**
    * **The main method for creating a product.**
    * Accepts a filled `ProductFields` object.
    * Calls `_add_parent_categories(f)` to add parent categories.
    * Calls `f.to_dict()` to convert product data into a dictionary compatible with the API.
    * Forms the request body (including the wrapper `{'prestashop': {'products': [...]}}`).
    * Converts the dictionary to XML using `dict2xml`.
    * Sends a `POST` request to `/api/products` with XML data using `self.create('products', data=presta_product_xml)`.
    * If successful:
        * Parses the response, gets the ID of the created product.
        * Attempts to upload the image:
            * If there is a path to a local file in `f.local_image_path`, use `self.create_binary` to upload it.
            * If there is a URL in `f.default_image_url`, use `self.upload_image_from_url` to download and upload it.
        * Logs success and returns `SimpleNamespace` with data of the added product (from the API response).
    * In case of an error (when creating a product or uploading an image), logs the error and returns an empty dictionary `{}`.

## Typical Workflow

1. **Data Collection:** An instance of `Graber` (or its descendant) collects data from the supplier's product page and fills the `ProductFields` object (`f`).
2. **Initialization of `PrestaProduct`:** An instance of `PrestaProduct` is created with the necessary API credentials.
    ```python
    from src.endpoints.prestashop.product import PrestaProduct
    from src.endpoints.prestashop.product_fields import ProductFields

    # pf - это объект ProductFields, заполненный грабером
    pf: ProductFields = get_product_data_from_supplier()

    # Инициализация PrestaProduct (API ключи возьмутся из Config)
    pp = PrestaProduct()
    ```
3. **Adding a product:** The `add_new_product` method is called.
    ```python
    # Добавление товара в PrestaShop
    result = pp.add_new_product(pf)

    if result:
        print(f"Товар успешно добавлен. ID: {result.id}")
    else:
        print("Не удалось добавить товар.")
    ```
4. **Inside `add_new_product`:**
    * Parent categories are defined and added (`_add_parent_categories`).
    * `ProductFields` data is converted to a dictionary (`pf.to_dict()`).
    * The dictionary is converted to XML (`dict2xml`).
    * A POST request is sent to the API (`self.create`).
    * The image is uploaded (if available) (`self.create_binary` or `self.upload_image_from_url`).

## Usage Examples

At the end of the `product.py` file, there are example functions:

* **`example_add_new_product()`:** Demonstrates how you can manually create a data dictionary (or load it from a JSON schema) and send it to create a product, using the `_exec` method directly (for more flexibility) or `create`. This example is useful for debugging the data structure being sent to the API.
* **`example_get_product(id_product)`:** Shows how to get data for an existing product by its ID and save it to a JSON file for analysis.

These examples can be run if the `product.py` file is executed as the main script (`if __name__ == '__main__':`).

```python
if __name__ == '__main__':
    # Получить данные товара с ID 2191 и сохранить в JSON
    example_get_product(2191)

    # Попытаться добавить новый товар на основе данных из файла схемы
    # (предварительно нужно создать или скачать файл 'product_schema.2191_....json')
    # example_add_new_product()

```