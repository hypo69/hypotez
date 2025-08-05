# Module src.suppliers.morlevi._experiments.JUPYTER_header

## Overview

This module provides functionality for starting a supplier using a specific prefix and locale. It also includes dependencies for working with products, categories, and utilities.

## Details

This module provides a function for starting a supplier, which is used to create a new supplier instance with specific parameters. The function takes the supplier prefix (e.g., 'aliexpress') and locale (e.g., 'en') as arguments. It then creates a dictionary with these parameters and uses it to initialize a `Supplier` instance.

## Functions

### `start_supplier`

**Purpose**: Starts a supplier with the specified prefix and locale.

**Parameters**:
- `supplier_prefix` (str): The prefix for the supplier (e.g., 'aliexpress'). Defaults to 'aliexpress'.
- `locale` (str): The language locale (e.g., 'en'). Defaults to 'en'.

**Returns**:
- `Supplier`: A `Supplier` instance with the specified parameters.

**Raises Exceptions**:
- None

**Example**:
```python
# Start a supplier with the prefix 'aliexpress' and locale 'en'
supplier = start_supplier(supplier_prefix='aliexpress', locale='en')
```

## Parameter Details
- `supplier_prefix` (str): The prefix for the supplier (e.g., 'aliexpress'). Defaults to 'aliexpress'.
- `locale` (str): The language locale (e.g., 'en'). Defaults to 'en'.

## Examples
```python
# Example 1: Start a supplier with the default prefix and locale
supplier = start_supplier()

# Example 2: Start a supplier with a custom prefix and locale
supplier = start_supplier(supplier_prefix='amazon', locale='de')