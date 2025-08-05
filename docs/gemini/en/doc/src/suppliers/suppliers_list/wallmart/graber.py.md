# Wallmart Graber - Supplier Data Extraction

## Overview

This module (`graber.py`) is part of the `hypotez` project and focuses on extracting product data from the `wallmart.com` website. It builds upon the functionality of the `src.suppliers.graber` module, extending and customizing data extraction for Wallmart-specific product pages.

## Details

The `Graber` class extends the generic `Graber` class from `src.suppliers.graber` to handle Wallmart's unique product page structure and data elements.

### Key Features:

- **Supplier-Specific Data Extraction:** The `Graber` class inherits from the `Graber` class, which defines a base set of functions for extracting common product attributes. These functions are then customized within the `Graber` class to handle specific elements and data formats found on Wallmart's website.
- **Decorator for Pre-Processing:** The module implements a decorator (`close_pop_up`) that allows for pre-processing actions before the main data extraction functions are executed. This decorator helps to handle potential pop-up windows or other interfering elements that might obstruct the data extraction process.
- **Customization and Flexibility:** The module provides a template for creating custom decorators and overriding default behavior for data extraction functions, allowing for flexibility in adapting to changes in Wallmart's website structure.

## Classes

### `Graber`

**Description**:  Extends the generic `Graber` class to extract data from Wallmart product pages.

**Inherits**: `src.suppliers.graber.Graber`

**Attributes**:

- `supplier_prefix (str)`:  Specifies the supplier prefix, which is 'wallmart' for this class.

**Methods**:

- `__init__(self, driver: Driver, lang_index: int)`: Initializes the `Graber` object with the specified `driver` instance (for interacting with the web browser) and the `lang_index` (for language-specific data extraction).

## Functions

### `close_pop_up` (Decorator)

**Purpose**: This decorator is used to close pop-up windows that might appear before the main extraction functions are executed. This ensures a cleaner and more reliable data extraction process.

**Parameters**:

- `value (Any)`: An optional parameter for the decorator. It allows for passing additional information to the decorator's logic.

**Returns**:

- `Callable`: The decorated function itself.

**Example**:

```python
@close_pop_up(value=None)  # Applying the decorator
def extract_title(self, *args, **kwargs):
    """Extracts the product title from the page."""
    # ...
```

## How it Works:

- **Inheritance**: The `Graber` class inherits from the `Graber` class, inheriting its basic data extraction functions and configuration.
- **Customization**: The `Graber` class overwrites specific functions inherited from the base `Graber` class to handle Wallmart-specific data extraction requirements.
- **Decorator**: The `close_pop_up` decorator provides a mechanism for pre-processing the data extraction process by handling potential pop-up windows or other elements that might interfere with the extraction.
- **Configuration**: The `Config.locator_for_decorator` setting allows for customizing the pop-up closing logic within the decorator.

## Examples:

```python
from src.suppliers.wallmart.graber import Graber
from src.webdriver.driver import Driver
from src.webdriver.driver import Chrome

# Creating a driver instance
driver = Driver(Chrome)

# Creating a Graber object
graber = Graber(driver, lang_index=0)

# Extracting data
product_data = graber.get_product_data(product_url='https://www.wallmart.com/product/123456789')

# Accessing extracted data
product_title = product_data['title']
``` 

This example demonstrates how to create a `Graber` object, set up a web driver, and extract product data from a Wallmart product page.