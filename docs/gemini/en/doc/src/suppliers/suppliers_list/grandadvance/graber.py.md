# Grandadvance Data Graber

## Overview

This module is responsible for collecting product data from the Grandadvance website. It implements the `Graber` class, which inherits from the base `src.suppliers.graber.Graber` class. 

The `Graber` class provides methods for processing various product fields on the product page. If a field requires custom handling, its method can be overridden.

For each product page field, a processing function is defined in the parent `Graber` class. If a field requires non-standard processing, you can override the method in this class.

## Details

This module inherits from the base `Graber` class, responsible for collecting product data from a specific online marketplace. It's designed to work with Grandadvance specifically, customizing field processing and incorporating specific behavior. 

### Pre-processing with Decorators

Before sending a request to the webdriver, you can perform pre-processing steps through a decorator. The default decorator resides in the parent class. To activate the decorator, you need to pass the value to `Context.locator`. If you need to implement your own decorator, uncomment the decorator lines and redefine its behavior. You can also implement your own custom decorator by uncommenting the relevant code lines. 

### Configuration and Locators

This module utilizes configuration files to define the specific behaviors for this supplier. The configuration data is loaded from JSON files, including:

- `grandadvance.json`:  Contains overall configuration settings for the Grandadvance supplier.
- `product.json`:  Contains locators for elements on the product page.

These files are loaded using the `j_loads_ns` function from `src.utils.jjson`.

### Driver Management

The module interacts with the webdriver through the `Driver` object, which handles browser interactions, locators, and execution of tasks. It's instantiated using the `Driver` class from `src.webdriver.driver`. The `Driver.execute_locator` method is used to find and manipulate web elements based on the provided locators.

## Classes

### `Graber`

**Description**:  This class inherits from the `Graber` base class and specializes in collecting data from Grandadvance. It overrides methods for specific fields, handles pre-processing, and interacts with the webdriver.

**Inherits**:  `src.suppliers.graber.Graber`

**Attributes**:
- `driver`:  An instance of the `Driver` class used to interact with the browser. 
- `lang_index`:  The index of the language for which the product data is being collected.

**Methods**:

- `__init__(self, driver: Driver, lang_index:int)`:  
    - Initializes the `Graber` object, loading configuration and locators from JSON files.
    - Calls the parent class's `__init__` method, setting the supplier prefix and initializing the `Graber` object.

## Examples

### Example of Graber Instantiation

```python
# Creating a Graber instance (example with Firefox)
from src.webdriver import Driver, Firefox
from src.suppliers.suppliers_list.grandadvance.graber import Graber

driver = Driver(Firefox)
graber = Graber(driver, lang_index=0)
```
This example demonstrates how to create a Graber instance, setting up the driver and specifying the language index.

### Example of Using execute_locator

```python
# Example of using driver.execute_locator
close_banner = {
  "attribute": null,
  "by": "XPATH",
  "selector": "//button[@id = 'closeXButton']",
  "if_list": "first",
  "use_mouse": false,
  "mandatory": false,
  "timeout": 0,
  "timeout_for_event": "presence_of_element_located",
  "event": "click()",
  "locator_description": "Закрываю pop-up окно, если оно не появилось - не страшно (`mandatory`:`false`)"
}

result = driver.execute_locator(close_banner)
```
This example demonstrates the use of the `driver.execute_locator` method to interact with a web element identified by the provided locator.

## Parameter Details

### `Config.locator_for_decorator` 

This attribute is used to define the locator for the decorator used in pre-processing. It's set to `self.product_locator.click_to_specifications` in the code, indicating that the decorator will apply to the `click_to_specifications` locator. 

### `driver`

- `driver`:  A `Driver` object responsible for web browser interactions. It inherits from `Driver`, `Chrome`, `Firefox`, and `Playwright`, providing a unified interface for browser automation.

### `lang_index`

- `lang_index`:  An integer representing the index of the language used for collecting data.

### `Config`

- `Config`:  A class representing the configuration for the supplier. It's used to store settings and parameters.

### `locator`

- `locator`:  A `SimpleNamespace` object containing locators for web elements on the product page.

### `product_locator`

- `product_locator`:  An attribute within the `Graber` class representing the locators for the product page.

### `click_to_specifications`

- `click_to_specifications`:  A locator for the "Click to specifications" button on the product page. It's used by the decorator to perform pre-processing before sending the request to the webdriver.