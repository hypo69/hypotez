# Module src.suppliers.hb._experiments 

## Overview

This module provides a set of functions and classes for working with suppliers, particularly within the context of the HB (House Brands) project. It focuses on tasks related to supplier initialization, scenario execution, and data processing. 

## Details

This module is used to manage and process supplier data, likely related to product information, categories, and other relevant details for the HB project.  The code initializes variables and sets up paths for working with the project's directory structure, imports key modules, and defines the `start_supplier` function.

## Functions

### `start_supplier(supplier_prefix, locale)`

**Purpose**: This function initiates the setup for a specific supplier. 

**Parameters**:
- `supplier_prefix` (str): A prefix identifying the specific supplier.
- `locale` (str): The language or region associated with the supplier.

**Returns**:
- `Supplier`: An instance of the `Supplier` class representing the initialized supplier.

**Raises Exceptions**:
- None

**How the Function Works**:
- Checks for both `supplier_prefix` and `locale` parameters. If either is missing, it returns an error message.
- Constructs a dictionary `params` with `supplier_prefix` and `locale` values.
- Uses the `Supplier` class, likely with the provided parameters, to initialize a supplier object and return it.

**Examples**:
```python
# Example 1: Starting a supplier with prefix "hb" and locale "en"
supplier = start_supplier("hb", "en")
```

```python
# Example 2: Starting a supplier without specifying prefix or locale
supplier = start_supplier(None, None) # Returns an error message
```

## Parameter Details

- `supplier_prefix` (str): A prefix used to identify the supplier, allowing for differentiation within a broader group.
- `locale` (str):  Specifies the language or regional setting for the supplier, likely used for localization or product information presentation.


## Inner Functions

- None


## Examples

- **Example 1**:
    - **Function call**: `start_supplier("hb", "en")` 
        -  This would initialize a supplier with the prefix "hb" and the locale "en".
    - **Expected result**: An initialized `Supplier` object representing the "hb" supplier in the "en" locale.
- **Example 2**:
    - **Function call**: `start_supplier(None, None)`
        - This would try to start a supplier without providing any information.
    - **Expected result**: An error message, as both `supplier_prefix` and `locale` are required to identify a supplier.