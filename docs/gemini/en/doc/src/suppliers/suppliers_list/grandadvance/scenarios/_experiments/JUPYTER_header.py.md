# Module: src.suppliers.grandadvance.scenarios._experiments.JUPYTER_header

## Overview

This module defines a function for starting a specific supplier.

## Details

This module appears to be part of the `hypotez` project, which likely involves working with suppliers and product data. It utilizes libraries and classes related to supplier integration, product management, and web driver functionality.

The module contains one main function: `start_supplier()`.

## Functions

### `start_supplier(supplier_prefix: str = 'aliexpress', locale: str = 'en')`

**Purpose**: This function initiates a supplier based on provided parameters.

**Parameters**:

- `supplier_prefix` (str, optional): The prefix identifying the supplier. Defaults to 'aliexpress'.
- `locale` (str, optional): The language locale for the supplier. Defaults to 'en'.

**Returns**:

- `Supplier`: An instance of the `Supplier` class, representing the initialized supplier.

**How the Function Works**:

1. **Parameter Gathering**: The function creates a dictionary `params` with the `supplier_prefix` and `locale` values.
2. **Supplier Initialization**: It instantiates a `Supplier` object using the `params` dictionary.
3. **Return**: The initialized `Supplier` instance is returned.

**Examples**:

```python
# Starting AliExpress supplier with default locale ('en')
supplier = start_supplier()

# Starting AliExpress supplier with a specific locale ('ru')
supplier = start_supplier(locale='ru')

# Starting a different supplier (e.g., 'grandadvance')
supplier = start_supplier(supplier_prefix='grandadvance')