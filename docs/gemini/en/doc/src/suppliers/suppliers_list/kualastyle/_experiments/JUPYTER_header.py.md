# JUPYTER_header Module

## Overview

This module provides a basic structure for setting up a supplier in the `hypotez` project. 

## Details

The code in this file is intended to be a header for Jupyter notebooks used in experiments related to suppliers. The main functions include:

- **`start_supplier(supplier_prefix: str = 'aliexpress', locale: str = 'en')`**: This function initializes a supplier object with a specific prefix and locale.

## Functions

### `start_supplier(supplier_prefix: str = 'aliexpress', locale: str = 'en')`

**Purpose**: Initializes a supplier object based on the provided `supplier_prefix` and `locale`.

**Parameters**:

- `supplier_prefix` (str): The prefix for the supplier (e.g., 'aliexpress'). Defaults to 'aliexpress'.
- `locale` (str): The language locale for the supplier (e.g., 'en'). Defaults to 'en'.

**Returns**:

- `Supplier`: A `Supplier` object representing the initialized supplier.

**How the Function Works**:

1. The function creates a dictionary named `params` to hold the supplier's prefix and locale.
2. It returns an instance of the `Supplier` class, using the `params` dictionary as input.

**Examples**:

```python
# Initializing an AliExpress supplier in English
aliexpress_supplier = start_supplier(supplier_prefix='aliexpress', locale='en')

# Initializing a supplier with a custom prefix in Russian
custom_supplier = start_supplier(supplier_prefix='custom_supplier', locale='ru')
```

**Inner Functions**: None

**Note**: The `Supplier` class is assumed to be defined elsewhere in the project. This header file primarily provides a setup structure for using suppliers within Jupyter notebooks.