# Test AliExpress Scenario
## Overview

This module contains a script for testing the AliExpress supplier integration within the Hypotez project. It demonstrates a workflow for fetching product data from AliExpress and adding it to the PrestaShop database.

## Details

This script defines a test scenario for a specific product category (`iPhone 13 & 13 MINI`). It includes essential product details such as the AliExpress category ID, brand, URL, active status, condition, PrestaShop category mapping, and product combination attributes. The script then fetches and processes product data from AliExpress, extracts relevant information, and attempts to add the product to the PrestaShop database.

## Functions

### `start_supplier(supplier_prefix)`

**Purpose**: Initializes an instance of the `Supplier` class based on a given supplier prefix. 

**Parameters**:
- `supplier_prefix` (str): The unique prefix for the AliExpress supplier, e.g., 'aliexpress'.

**Returns**:
- `Supplier`: An instance of the `Supplier` class initialized with the provided prefix.

**Example**:

```python
supplier_prefix = 'aliexpress'
s = start_supplier(supplier_prefix)
```

### `start_product()`

**Purpose**: Initializes an instance of the `Product` class based on a predefined test scenario and supplier data. 

**Parameters**: None

**Returns**:
- `Product`: An instance of the `Product` class initialized with the predefined test scenario and supplier data.

**Example**:

```python
p = start_product()
```

## Class Methods

### `Product`

**Description**: Represents a product on AliExpress. It provides methods for retrieving product data, validating the product's presence in the PrestaShop database, and adding the product to PrestaShop.

**Inherits**: `object`

**Attributes**:

- `supplier` (`Supplier`): The supplier object associated with the product.
- `webelements_locators` (`dict`): A dictionary containing web element locators for extracting product information.
- `product_categories` (`dict`): A dictionary defining the PrestaShop categories associated with the product.
- `product_fields` (`dict`): A dictionary containing the extracted product fields.

**Methods**:

- `check_if_product_in_presta_db(reference: str) -> bool`: Checks if the product with the given `reference` exists in the PrestaShop database.
- `add_2_PrestaShop(product_fields: dict) -> None`: Attempts to add the product with the provided `product_fields` to the PrestaShop database.

**Example**:

```python
from src import gs
from src.product import Product
from categories import Category
from src.logger.logger import logger

# ... (Previous code)

# Example usage of the Product class
p = start_product()
d = s.driver
_ = d.execute_locator
f = p.fields
l = p.webelements_locators

d.get_url(test_products_list[0])
f.reference = d.current_url.split('/')[-1].split('.')[0]
f.price = _(l['price'])

if not p.check_if_product_in_presta_db(f.reference):
    p.add_2_PrestaShop(f)
```

## Parameter Details

- `supplier_prefix` (str): The unique prefix for the AliExpress supplier, e.g., 'aliexpress'.
- `test_scenario` (dict): A dictionary containing the test scenario for a specific product category.
- `test_products_list` (list): A list of URLs for the test products.
- `s` (`Supplier`): An instance of the `Supplier` class representing the AliExpress supplier.
- `p` (`Product`): An instance of the `Product` class representing the AliExpress product.
- `d` (`Driver`): An instance of the `Driver` class for interacting with the web browser.
- `_` (`Callable`): A reference to the `driver.execute_locator` method.
- `f` (`dict`): A reference to the `product_fields` dictionary.
- `l` (`dict`): A reference to the `webelements_locators` dictionary.

## Examples

```python
# Example 1: Initializing a Supplier
supplier_prefix = 'aliexpress'
s = start_supplier(supplier_prefix)

# Example 2: Initializing a Product
p = start_product()

# Example 3: Extracting and Adding Product Data
d = s.driver
_ = d.execute_locator
f = p.fields
l = p.webelements_locators

d.get_url(test_products_list[0])
f.reference = d.current_url.split('/')[-1].split('.')[0]
f.price = _(l['price'])

if not p.check_if_product_in_presta_db(f.reference):
    p.add_2_PrestaShop(f)
```

## How the Function Works

The script first initializes the `Supplier` and `Product` classes using the `start_supplier` and `start_product` functions. It then extracts product data from AliExpress using web element locators defined in the `webelements_locators` dictionary. The script then attempts to add the product to the PrestaShop database using the `check_if_product_in_presta_db` and `add_2_PrestaShop` methods of the `Product` class. 

This script demonstrates a basic workflow for fetching product data from AliExpress and adding it to the PrestaShop database. It is important to note that this is a simplified example and may require further customization depending on the specific requirements of the Hypotez project.