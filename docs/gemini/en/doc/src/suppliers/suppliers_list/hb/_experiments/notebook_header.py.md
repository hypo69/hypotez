# Module: src.suppliers.hb._experiments.notebook_header

## Overview

This module provides a function for starting a supplier based on specified parameters, including supplier prefix and locale. It utilizes various utility functions and classes from other modules in the `hypotez` project.

## Details

The `start_supplier` function is used to initiate the process for a specific supplier. It takes the `supplier_prefix` and `locale` as input and creates a `Supplier` object based on these parameters. If either of these parameters is missing, an informative message is returned.

This module primarily serves as a starting point for executing supplier-specific scenarios. It utilizes external modules for common functionality like:

- **`src.gs`**: Google Sheets integration.
- **`src.webdriver`**: Webdriver management.
- **`src.product`**: Product data handling.
- **`src.category`**: Category data handling.
- **`src.utils`**: Utility functions for string formatting and normalization.
- **`src.scenario`**: Scenario execution.

## Functions

### `start_supplier`

**Purpose**: Initializes the supplier process based on provided parameters.

**Parameters**:

- `supplier_prefix` (str): The prefix identifying the supplier.
- `locale` (str): The language or region associated with the supplier.

**Returns**:

- str: An informative message if either `supplier_prefix` or `locale` is missing.
- Supplier: A `Supplier` object initialized with the provided parameters.

**Raises Exceptions**:

- None

**How the Function Works**:

1. It checks if both `supplier_prefix` and `locale` are provided. If not, it returns a message indicating that the script requires both parameters.
2. If both parameters are present, it creates a dictionary (`params`) containing the values for `supplier_prefix` and `locale`.
3. It creates a `Supplier` object using the `**params` syntax, which expands the dictionary into keyword arguments for the `Supplier` constructor.
4. The function returns the initialized `Supplier` object.

**Examples**:

```python
# Example 1: Both parameters provided
start_supplier('hb', 'en')  # Initializes a supplier with prefix 'hb' and locale 'en'

# Example 2: Missing locale
start_supplier('hb', None)  # Returns "Не задан сценарий и язык"

# Example 3: Missing supplier_prefix
start_supplier(None, 'en')  # Returns "Не задан сценарий и язык"
```