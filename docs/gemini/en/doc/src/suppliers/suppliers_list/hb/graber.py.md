# Module src.suppliers.hb.graber

## Overview

This module defines the `Graber` class, which is responsible for collecting product data from the hb.co.il website. It extends the `Graber` class from the `src.suppliers.graber` module and overrides specific field processing methods. 

## Details

The `Graber` class implements customized logic for fetching data from the `hb.co.il` website. It utilizes a `driver` (a WebDriver instance) to navigate the website and extract information. 

The class contains a set of methods that handle specific product fields, such as product name, description, images, and price. Each method uses a `locator` (a dictionary containing instructions on how to find and interact with the web element) to identify the corresponding field on the page.

## Classes

### `class Graber(Grbr)`

**Description**: Class for retrieving product data from the hb.co.il website.

**Inherits**: Inherits from the `Graber` class.

**Attributes**:

- `supplier_prefix`: String representing the prefix for the supplier, default is 'hb'.

**Methods**:

- `__init__(self, driver: Optional['Driver'] = None, lang_index: Optional[int] = None)`: Initializes the `Graber` instance.
    -  Sets the `supplier_prefix` to 'hb'.
    -  Calls the parent class's `__init__` method, passing the `supplier_prefix`, `driver`, and `lang_index`.
    -  Sets the `Config.locator_for_decorator` to `None`. This variable is used in the `close_pop_up` decorator.

    -  **Example:**
        ```python
        driver = Driver(Chrome) # Creating a driver instance (example with Chrome)
        graber = Graber(driver) 
        ```
- `default_image_url(self, value: Optional[Any] = None) -> bool`: Placeholder method for handling the default image URL. Always returns `True`.
- `price(self, value: Optional[Any] = None) -> bool`: Placeholder method for handling the product price. Sets the price to `150.00` and returns `True`.

## Functions

### `close_pop_up(value: Any = None) -> Callable`:

**Purpose**:  This function is a template for a decorator designed to close pop-up windows before executing the main logic of a function.

**Parameters**:

- `value (Any)`: Additional value for the decorator.

**Returns**:

- `Callable`: The decorator function.

**How the Function Works**:

- The `decorator` function wraps the original function.
- When the decorated function is called, the `wrapper` function is executed.
- The `wrapper` function first attempts to execute the `close_pop_up` locator (defined in the `Context` class) to close any pop-up windows.
- If an `ExecuteLocatorException` occurs (likely due to the pop-up not existing), a debug message is logged using `logger.debug()`.
- The `wrapper` function then calls the original function and returns the result.

**Examples**:

```python
@close_pop_up()
def my_function():
    # Main function logic here
    ...
```

## Parameter Details

- `value`: The value passed to the decorator. It can be any type, but it's intended for passing additional data to the decorator logic.
- `func`: The function to decorate.
- `*args`, `**kwargs`: Arguments and keyword arguments passed to the decorated function.
- `e`: Exception object received during the execution of the `close_pop_up` locator.

## Examples

```python
# Creating a Graber instance
driver = Driver(Chrome) # Creating a driver instance (example with Chrome)
graber = Graber(driver)

# Example of calling the price method
result = await graber.price(value=None) 

# Example of using the close_pop_up decorator
@close_pop_up()
async def my_function():
    # Function logic here
    ...
```