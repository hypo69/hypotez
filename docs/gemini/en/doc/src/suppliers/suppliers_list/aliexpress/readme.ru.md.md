# AliExpress Supplier Integration Module

## Overview

This module provides access to data from the AliExpress supplier using HTTPS (webdriver) and API protocols. It is part of the `hypotez` project.

## Details

This module is designed to work with the AliExpress supplier. It provides tools for interacting with the AliExpress website and API, allowing you to collect product information, generate affiliate links, and manage campaigns.

## Structure

The module is structured as follows:

### `utils`

This submodule contains utility functions and classes for performing common operations in AliExpress integration. It might include tools for data formatting, error handling, logging, and other tasks that simplify interaction with the AliExpress ecosystem.

### `api`

This submodule provides methods and classes for direct interaction with the AliExpress API. It likely includes functionality for sending requests, processing responses, and managing authentication, simplifying interaction with the API for retrieving or sending data.

### `campaign`

This submodule is intended for managing marketing campaigns on AliExpress. It might include tools for creating, updating, and tracking campaigns, as well as methods for analyzing their effectiveness and optimizing them based on provided metrics.

### `gui`

This submodule provides graphical user interface elements for interacting with AliExpress functionality. It might include implementations of forms, dialogs, and other visual components that allow users to more intuitively manage AliExpress operations.

### `locators`

This submodule contains definitions for finding elements on AliExpress web pages. These locators are used together with WebDriver tools to perform automated interactions, such as collecting data or performing actions on the AliExpress platform.

### `scenarios`

This submodule defines complex scenarios or sequences of actions for interacting with AliExpress. It likely includes a combination of tasks (e.g., API requests, GUI interactions, and data processing) as part of larger operations such as product synchronization, order management, or campaign execution.

## Webdriver

The module uses `webdriver` to interact directly with AliExpress web pages. It provides the following classes for working with different browsers:

- `Driver`: Base class for WebDriver instances.
- `Chrome`: A class for using Google Chrome as the WebDriver.
- `Firefox`: A class for using Mozilla Firefox as the WebDriver.
- `Playwright`: A class for using Playwright as the WebDriver.

To create a driver instance, you can use the following code:

```python
from src.webdriver import Driver, Chrome

# Creating a driver instance (example with Chrome)
driver = Driver(Chrome)
```

The Driver, Chrome, Firefox, and Playwright modules already contain all Selenium settings. The main command used in the code is: `driver.execute_locator(l:dict)`. It returns the value of the web element by locator.

## Example

Here's an example of how to use the module to collect product information:

```python
from src.suppliers.suppliers_list.aliexpress import Aliexpress

# Create an instance of the AliExpress module
aliexpress = Aliexpress()

# Get product data using the API
product_data = aliexpress.api.get_product_data(product_id)

# Print the product data
print(product_data)

# Use webdriver to get additional information
driver = aliexpress.webdriver.Driver(Chrome)
product_description = driver.execute_locator({
    "attribute": "innerHTML",
    "by": "XPATH",
    "selector": "//div[@id='product-description']",
    "if_list": "first",
})
```