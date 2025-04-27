# Module: src.suppliers.aliexpress.api.tools.get_product_id

## Overview

This module provides a function to extract product IDs from given text. It utilizes the `extract_prod_ids` function from the `src.suppliers.suppliers_list.aliexpress.utils.extract_product_id` module to perform the extraction.

## Details

The `get_product_id` function takes a raw product ID as input and returns a product ID extracted from the text. If no product ID can be extracted, a `ProductIdNotFoundException` is raised.

## Functions

### `get_product_id`

**Purpose**: This function extracts a product ID from a given text.

**Parameters**:

- `raw_product_id` (str): The raw product ID text to extract from.

**Returns**:

- `str`: The extracted product ID.

**Raises Exceptions**:

- `ProductIdNotFoundException`: If a product ID cannot be extracted from the provided text.

**How the Function Works**:

- The function delegates the extraction process to the `extract_prod_ids` function from the `src.suppliers.suppliers_list.aliexpress.utils.extract_product_id` module. 

**Examples**:

```python
from src.suppliers.aliexpress.api.tools.get_product_id import get_product_id

# Example 1: Successful extraction
raw_product_id = "Product ID: 1234567890"
product_id = get_product_id(raw_product_id)
print(f"Product ID: {product_id}")  # Output: Product ID: 1234567890

# Example 2: Product ID not found
raw_product_id = "This text does not contain a product ID."
try:
    product_id = get_product_id(raw_product_id)
    print(f"Product ID: {product_id}")
except ProductIdNotFoundException as ex:
    print(f"Error: {ex}")  # Output: Error: Product id not found: This text does not contain a product ID.
```