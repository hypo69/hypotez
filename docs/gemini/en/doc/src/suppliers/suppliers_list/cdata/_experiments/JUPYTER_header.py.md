# Module: src.suppliers.cdata._experiments.JUPYTER_header

## Overview

This module provides the `start_supplier` function, which initializes a supplier object with specific parameters. This module is intended to be used in conjunction with the `hypotez` project, specifically within the `suppliers` section. 

## Details

The module is designed to streamline the process of initiating a supplier for data processing tasks within the `hypotez` project. It's likely used in conjunction with a supplier-specific configuration or data pipeline to handle data ingestion, processing, and potentially, data enrichment.

## Functions

### `start_supplier`

**Purpose**:  This function initializes a supplier object with specified parameters.

**Parameters**:

- `supplier_prefix` (str): The prefix identifying the supplier. Defaults to `'aliexpress'`.
- `locale` (str): The language locale for the supplier. Defaults to `'en'`.

**Returns**:

- `Supplier`:  The initialized supplier object.

**Raises Exceptions**:

- N/A

**How the Function Works**:

- Creates a dictionary `params` containing the `supplier_prefix` and `locale` values.
- Initializes a `Supplier` object using the `params` dictionary. 
- Returns the initialized `Supplier` object.

**Example**:

```python
from src.suppliers.cdata._experiments.JUPYTER_header import start_supplier

# Initialize an AliExpress supplier with English locale
aliexpress_supplier = start_supplier(supplier_prefix='aliexpress', locale='en')

# Now you can work with the 'aliexpress_supplier' object
```

## Parameter Details

- `supplier_prefix` (str): This parameter likely identifies the supplier system or platform (e.g., `'aliexpress'`, `'amazon'`, `'ebay'`, etc.). It is used to distinguish between different supplier sources and potentially trigger specific data processing pipelines.

- `locale` (str): This parameter specifies the language locale of the supplier's data. It ensures proper data handling and processing in the correct language. For example, `'en'` signifies English, `'ru'` represents Russian, etc.

## Examples

```python
from src.suppliers.cdata._experiments.JUPYTER_header import start_supplier

# Example 1: Initializing an AliExpress supplier with the default English locale
aliexpress_supplier = start_supplier()

# Example 2: Initializing a supplier with a specific prefix and locale
ebay_supplier = start_supplier(supplier_prefix='ebay', locale='de')
```

```python
# ----------------
dir_root : Path = Path (os.getcwd()[:os.getcwd().rfind('hypotez')+7])
sys.path.append (str (dir_root) )  # Добавляю корневую папку в sys.path
dir_src = Path (dir_root, 'src')
sys.path.append (str (dir_root) ) 
# ----------------
```
- This code snippet appears to be configuring the Python path (`sys.path`). It's adding the root directory of the `hypotez` project to the path, allowing the script to import modules from within the project. 
- `dir_root`:  This variable holds the root directory path of the `hypotez` project.
- `dir_src`: This variable holds the path to the `src` directory within the `hypotez` project.
- `sys.path.append(str(dir_root))`: This line adds the root directory path to the `sys.path`, making modules in that directory accessible for import. 
- `sys.path.append(str(dir_src))`: This line adds the `src` directory path to the `sys.path`, making modules within `src` accessible for import.

```python
from src.webdriver.driver import Driver

from src.product import Product, ProductFields
from src.category import Category
from src.utils import StringFormatter, StringNormalizer
from src.utils.printer import  pprint
from src.endpoints.PrestaShop import Product as PrestaProduct
, save_text_file
# ----------------
```
- This snippet is importing various modules from the `hypotez` project.
- `src.webdriver.driver`: This imports the `Driver` class, which likely provides functionality for controlling web browsers (e.g., using Selenium).
- `src.product.Product, ProductFields`: These imports classes related to product data.  `Product` likely represents a product object, and `ProductFields` might define product attributes.
- `src.category.Category`: This imports a class for handling product categories.
- `src.utils.StringFormatter, StringNormalizer`: These imports utility classes for handling string manipulation and formatting.
- `src.utils.printer.pprint`: This imports a function for pretty-printing data to the console.
- `src.endpoints.PrestaShop.Product as PrestaProduct`: This imports a class representing products from the PrestaShop platform.
- `save_text_file`: This imports a function likely used for saving data to text files.