# Module: `ksp`

## Overview

This module provides the `Graber` class for extracting product data from the `ksp.co.il` website. It inherits from the base `Graber` class and overrides functions for specific data fields.

## Details

The `Graber` class is responsible for collecting and processing product information from the `ksp.co.il` website. 

**Key Features:**

- **Overridden Functions:** Overrides field processing functions inherited from the parent class to handle specific requirements of the `ksp.co.il` website. 
- **Decorator Functionality:** Enables the use of a decorator (available in the parent class) to perform actions before accessing the web driver.
- **Mobile Version Support:**  Detects if the website is loading in a mobile version and applies appropriate locators for those fields.
- **Configurability:** Allows for adjusting locators and decorator behavior based on specific needs.

## Classes

### `Graber`

**Description:** Class for collecting product data from the `ksp.co.il` website.

**Inherits:** `Grbr`

**Attributes:**

- `supplier_prefix (str):` Defines the supplier prefix for the `ksp` website.

**Methods:**

#### `__init__(self, driver: Optional['Driver'] = None, lang_index:Optional[int] = None)`

**Purpose:** Initializes the `Graber` class and sets up the driver and language index.

**Parameters:**

- `driver (Optional['Driver'], optional):`  The web driver instance. Defaults to `None`.
- `lang_index (Optional[int], optional):`  The language index for data collection. Defaults to `None`.

**How the Function Works:**

- Initializes the `supplier_prefix` with the value `"ksp"`.
- Calls the `__init__` method of the parent class (`Grbr`) to inherit its setup.
- Waits for 3 seconds to allow the website to load.
- Checks if the current URL contains `/mob/`. If so, sets the locators based on the mobile version of the website.

**Examples:**

```python
# Creating a `Graber` instance 
graber = Graber(driver=driver, lang_index=1) 

# Accessing the `supplier_prefix`
print(graber.supplier_prefix)  # Output: ksp
```

## Functions

### `close_pop_up(value: Any = None) -> Callable`

**Purpose:**  (Template for Decorator) - This function serves as a template for a decorator to close pop-up windows before executing the main function's logic.

**Parameters:**

- `value (Any, optional):`  An optional additional value for the decorator. Defaults to `None`.

**Returns:**

- `Callable`:  A decorator function.

**How the Function Works:**

-  This function is a decorator template designed to close pop-up windows before executing the main function. It defines a wrapper function that attempts to close the pop-up using `Context.driver.execute_locator(Context.locator.close_pop_up)`. It uses `@wraps(func)` to preserve the original function's metadata.

**Example:**

```python
# (Not implemented, example only)

@close_pop_up() 
def my_function():
    # Function logic
    ...
```
**Note:** This function is commented out in the provided code. It is a template for a decorator. You can uncomment and implement this function as needed.

## Inner Functions

**Inner Functions:**  This file does not contain any inner functions.

## Parameter Details

- `driver (Optional['Driver'], optional):`  The web driver instance. Defaults to `None`.
- `lang_index (Optional[int], optional):`  The language index for data collection. Defaults to `None`.

## Examples

```python
#  Creating an instance with a specific language index
graber = Graber(lang_index=1)
```

## How the File Works

The `graber.py` file provides a `Graber` class for extracting product information from `ksp.co.il`. It's designed to override specific field processing functions and apply a decorator for pre-execution actions. It also includes support for the mobile version of the `ksp.co.il` website. The file relies on:

- **Webdriver:** To interact with the `ksp.co.il` website.
- **Locators:** To identify elements on the web page.
- **Decorator:** To perform actions before accessing the web driver.

## Additional Notes:

- The code includes the import of the `close_pop_up` function from the `src.suppliers.graber` module. This suggests the presence of a decorator pattern for handling pop-up windows.
- The logic includes checking for the `/mob/` string in the current URL to identify the mobile version of the website.
- `Config.locator_for_decorator` is set to `None` and might indicate a configurable parameter for the `close_pop_up` decorator. 
- There are `...` placeholders in the code, implying additional logic or implementation may be needed for specific scenarios.
- The code relies on the `src.utils.jjson` module for loading JSON data and the `src.logger.logger` module for logging purposes.

```python
                ```