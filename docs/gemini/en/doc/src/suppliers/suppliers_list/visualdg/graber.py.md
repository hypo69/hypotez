# VisualDG Graber Module

## Overview

This module is a part of the `hypotez` project and is responsible for collecting data from product pages on the `visualdg.co.il` website. 

The `Graber` class extends the `Graber` class from the `src.suppliers.graber` module, providing specific field handling for VisualDG products. 

It leverages the `Driver` class from the `src.webdriver` module for interaction with the web browser and employs a decorator pattern for handling pop-up windows. 

## Details

The `Graber` class is designed to retrieve specific data points from individual product pages on the `visualdg.co.il` website. The module's structure is based on the following:

- **Inherited Base Class**: The `Graber` class inherits from the `src.suppliers.graber.Graber` class, which provides a general framework for collecting product data from various suppliers.

- **Field-Specific Functions**: The `Graber` class overrides certain field handling functions from its parent class, providing custom logic for extracting data from the VisualDG website.

- **Decorator Pattern**: The module implements a decorator pattern for handling pop-up windows that might appear on the product pages. This ensures that the main logic for retrieving data executes correctly even if pop-ups obstruct the process.

## Classes

### `Graber`

**Description**: The `Graber` class represents a VisualDG data collector, inheriting from the `Grbr` (short for `Graber`) class and implementing custom functionality for VisualDG product pages.

**Inherits**:
- `src.suppliers.graber.Graber`

**Attributes**:
- `supplier_prefix`: A string identifying the supplier prefix for VisualDG (value: 'visualdg').

**Methods**:
- `__init__(self, driver: Optional[\'Driver\'] = None, lang_index:Optional[int] = None)`: Initializes the `Graber` instance, setting the `supplier_prefix` and calling the parent class's `__init__` method to set up the base Graber functionality.

**How the Class Works**:

- **Initialization**:
    - The `__init__` method initializes the `supplier_prefix` attribute with 'visualdg' and calls the parent class's `__init__` method, passing the `supplier_prefix`, an optional `driver` instance (for web browser control), and an optional `lang_index` for language-specific data processing.
    - The method sets the `locator_for_decorator` attribute to `None`. This attribute controls the execution of the pop-up window handling decorator.

- **Decorator Handling**:
    - The module uses a decorator pattern for closing pop-up windows. The decorator is defined in the parent class (`src.suppliers.graber.Graber`) and can be overridden in this class. 
    - If the `locator_for_decorator` attribute is not `None`, the decorator will be executed before each field-specific function call.

- **Field-Specific Functions**:
    - The class overrides certain field-specific functions from its parent class. This allows it to handle data extraction from VisualDG product pages in a way that is specific to the site's structure.

- **Example**:
    ```python
    from src.suppliers.visualdg.graber import Graber
    from src.webdriver.driver import Driver
    from src.webdriver.driver import Chrome

    # Creating a driver instance (example with Chrome)
    driver = Driver(Chrome)

    # Creating an instance of the VisualDG Graber
    visualdg_graber = Graber(driver=driver) 
    ```

## Inner Functions
  
  - There are no inner functions in this code.  

## Examples

```python
from src.suppliers.visualdg.graber import Graber
from src.webdriver.driver import Driver
from src.webdriver.driver import Chrome

# Creating a driver instance (example with Chrome)
driver = Driver(Chrome)

# Creating an instance of the VisualDG Graber
visualdg_graber = Graber(driver=driver) 
``` 

## Parameter Details

- `driver`: An optional instance of the `Driver` class from the `src.webdriver` module. This driver is used for interacting with the web browser.
- `lang_index`: An optional integer representing the index of the language to be used for data extraction. This parameter is passed to the parent class's `__init__` method. 
- `locator_for_decorator`: An optional value that controls the execution of the pop-up window handling decorator. It can be used to specify a locator for the pop-up window that should be closed.