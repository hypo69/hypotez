# Module src.suppliers.ivory.graber
## Overview

This module contains the `Graber` class for scraping product data from the website `ivory.co.il`. The class inherits from the `Graber` class defined in `src.suppliers.graber.py` and implements specific logic for extracting information from Ivory's website. 

## Details

The `Graber` class leverages Selenium through the `Driver` class from `src.webdriver.driver.py` to interact with the website and retrieve product data. The class uses a decorator (`close_pop_up`) to handle potential pop-up windows that may appear on the website.

## Classes

### `Graber`

**Description**: Класс для операций захвата данных с сайта `ivory.co.il`.

**Inherits**: `Graber` from `src.suppliers.graber.py`.

**Attributes**:

- `supplier_prefix`: Префикс поставщика (`ivory`).

**Methods**:

- `__init__(self, driver: Optional['Driver'] = None, lang_index:Optional[int] = None)`: Инициализирует класс сбора полей товара. Устанавливает префикс поставщика (`supplier_prefix`) и инициализирует родительский класс `Graber`.

## Functions

### `close_pop_up` 

**Purpose**: Создает декоратор для закрытия всплывающих окон перед выполнением основной логики функции.

**Parameters**:

- `value (Any)`: Дополнительное значение для декоратора.

**Returns**:

- `Callable`: Декоратор, оборачивающий функцию.

**How the Function Works**:

- The function creates a decorator that can be applied to other functions.
- The decorator attempts to close any pop-up windows using the `Driver.execute_locator` method with the `close_pop_up` locator.
- If an exception occurs during the pop-up closing process, the decorator logs the error using the `logger.debug` method.
- The decorated function is then executed, and its return value is returned.

**Examples**:

```python
@close_pop_up()
def my_function():
    # Code to be executed after closing pop-ups
    ...
```


## Parameter Details

- `value (Any)`: Дополнительное значение, которое может быть передано декоратору. 

## Examples

```python
# Creating a Graber instance with a Chrome driver
driver = Driver(Chrome)
graber = Graber(driver=driver)

# Accessing the supplier prefix
supplier_prefix = graber.supplier_prefix 

# Using the close_pop_up decorator on a function
@close_pop_up()
def my_function():
    # Code to be executed after closing pop-ups
    ...