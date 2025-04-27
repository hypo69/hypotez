# Kualastyle Graber Module

## Overview

This module implements the `Graber` class, which is responsible for extracting data from product pages on the kualastyle.co.il website. It inherits functionality from the generic `Graber` class, but overrides certain methods to handle specific data extraction requirements for Kualastyle. 

## Details

The `Graber` class utilizes the `driver.execute_locator()` method to fetch data from specific web elements on the product pages. It also defines a custom decorator, `close_pop_up`, to handle potentially interfering pop-up windows before extracting data. This ensures a clean data extraction process.

## Classes

### `Graber`

**Description**: This class extends the generic `Graber` class to handle product page data extraction for Kualastyle.

**Inherits**: `Graber` (from `src.suppliers.graber`)

**Attributes**:

- `supplier_prefix` (str): A unique prefix identifier for this supplier. 

**Methods**:

- `__init__(self, driver: Driver, lang_index:int)`: Initializes the `Graber` instance by setting the `supplier_prefix` and calling the parent class's `__init__` method. It also sets the `locator_for_decorator` attribute in the `Config` class, which is used to specify the locator for the `close_pop_up` decorator.

## Parameter Details

- `driver` (Driver): An instance of the `Driver` class from `src.webdriver.driver`, used for web interaction.
- `lang_index` (int): An index representing the language of the product page.
- `locator_for_decorator` (None): Defines the locator for the `close_pop_up` decorator. 

## Examples

```python
from src.suppliers.kualastyle.graber import Graber
from src.webdriver.driver import Driver
from src.webdriver.driver import Chrome

# Creating a driver instance (example with Chrome)
driver = Driver(Chrome)

# Initialize the Graber class with the driver and language index
graber = Graber(driver, lang_index=0)

# Use the graber instance to extract data from product pages
# Example: 
product_data = graber.extract_data(product_url='https://www.kualastyle.co.il/product-url')