# Module: src.suppliers.ksp._experiments.JUPYTER_header

## Overview

This module provides a basic framework for starting a supplier in the `hypotez` project. It defines the `start_supplier` function and imports relevant modules for interacting with products, categories, web drivers, and other project utilities.

## Details

The code initializes the `sys.path` variable to include the project's root directory and relevant subdirectories. This allows for the import of modules from the `hypotez` project.

The `start_supplier` function takes the supplier prefix and locale as parameters. It initializes a dictionary with these parameters and returns a `Supplier` object. The specific actions taken by the `Supplier` class are not defined in this file.

## Functions

### `start_supplier`

**Purpose**: Starts a supplier based on the given prefix and locale.

**Parameters**:

- `supplier_prefix` (str): The prefix for the supplier (e.g., `aliexpress`). Defaults to `aliexpress`.
- `locale` (str): The locale for the supplier (e.g., `en`). Defaults to `en`.

**Returns**:

- `Supplier`: A `Supplier` object initialized with the provided parameters.

**How the Function Works**:

1. Initializes a dictionary `params` with the given `supplier_prefix` and `locale`.
2. Creates a `Supplier` object using the `params` dictionary.
3. Returns the created `Supplier` object.

**Examples**:

```python
# Start a supplier with the default prefix 'aliexpress' and locale 'en'
supplier = start_supplier()

# Start a supplier with a custom prefix 'amazon' and locale 'de'
supplier = start_supplier(supplier_prefix='amazon', locale='de')
```

## Inner Functions:

None.

## Parameter Details:

- `supplier_prefix` (str): The prefix for the supplier. It is used to identify the specific supplier (e.g., `aliexpress`, `amazon`).
- `locale` (str): The locale for the supplier. It specifies the language and region settings for the supplier's data (e.g., `en` for English, `de` for German).

## Examples:

```python
# Example 1: Start the default supplier
supplier = start_supplier()

# Example 2: Start a supplier with a specific prefix and locale
supplier = start_supplier(supplier_prefix='amazon', locale='de')
```