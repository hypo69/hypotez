# JUPYTER_header Module

## Overview

This module provides the starting point for handling Etzmaleh supplier tasks. It sets up the project environment and imports necessary modules for working with products, categories, and other relevant components. 

## Details

The module is primarily designed to manage Etzmaleh-specific tasks, such as processing product information, handling category assignments, and leveraging the Etzmaleh API. It imports and utilizes key classes like `Product`, `Category`, and utilities like `StringFormatter` and `StringNormalizer` for manipulating data. It also establishes a connection with PrestaShop using the `PrestaProduct` class, allowing for the creation and management of products within PrestaShop. 

## Functions

### `start_supplier`

**Purpose**: Initializes and starts the supplier workflow for Etzmaleh, based on the provided supplier prefix and locale.

**Parameters**:

- `supplier_prefix` (str):  The prefix identifying the specific supplier. Defaults to "aliexpress."
- `locale` (str): The language locale for the supplier. Defaults to "en."

**Returns**:

- `Supplier`: Returns an instance of the `Supplier` class, representing the initialized Etzmaleh supplier object.

**Example**:

```python
# Starting the AliExpress supplier with English locale
supplier = start_supplier(supplier_prefix='aliexpress', locale='en')
```

**How the Function Works**:

1. The function first creates a dictionary called `params` to hold the `supplier_prefix` and `locale` values. 
2. Then, it utilizes the `Supplier` class (not shown in the code snippet) to create a new `Supplier` instance using the provided `params`.
3. Finally, the `Supplier` instance is returned, allowing for further interaction and processing related to the specified Etzmaleh supplier.

## Parameter Details

- `supplier_prefix` (str):  Identifies the specific supplier, such as "aliexpress."
- `locale` (str): The language locale for the supplier, such as "en."

## Examples

```python
# Example 1: Starting AliExpress supplier
supplier = start_supplier('aliexpress', 'en')

# Example 2: Starting the Etzmaleh supplier with Spanish locale
supplier = start_supplier('etzmaleh', 'es')