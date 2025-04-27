# Module: src.suppliers.visualdg._experiments.JUPYTER_header

## Overview

This module provides a Jupyter notebook-like header for VisualDG experiments. It defines a `start_supplier` function for initializing a supplier based on the provided parameters.

## Details

This file defines a Jupyter notebook-like header for VisualDG experiments, which sets up the environment for working with suppliers. It imports necessary modules, defines a root directory path, and provides the `start_supplier` function for supplier initialization.

The code is organized as follows:

1. **Imports:** Imports required modules, including `sys`, `os`, `Path`, `json`, `re`, `Driver`, `Product`, `Category`, `StringFormatter`, `StringNormalizer`, `pprint`, `PrestaProduct`, and `save_text_file`.
2. **Root Directory Setup:** Sets up the root directory path using `os.getcwd()` and adds it to `sys.path` to ensure correct module imports.
3. **`start_supplier` Function:** This function initiates a supplier instance with the provided parameters, including the `supplier_prefix` and `locale`.

## Functions

### `start_supplier`

**Purpose:** This function initializes a supplier instance based on the given parameters.

**Parameters:**

- `supplier_prefix` (str, optional): The prefix for the supplier, such as `aliexpress`. Defaults to `'aliexpress'`.
- `locale` (str, optional): The language locale, such as `en`. Defaults to `'en'`.

**Returns:**

- `Supplier`: A supplier instance initialized with the specified parameters.

**How the Function Works:**

- The function creates a `params` dictionary containing the `supplier_prefix` and `locale` values.
- It then constructs a `Supplier` instance using the `params` dictionary.
- Finally, the initialized `Supplier` instance is returned.

**Example:**

```python
# Start an Aliexpress supplier with the English locale
supplier = start_supplier(supplier_prefix='aliexpress', locale='en')