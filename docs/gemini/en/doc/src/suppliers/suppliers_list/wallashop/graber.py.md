# Wallashop Graber Module

## Overview

This module implements a `Graber` class for extracting product data from the Wallashop website (`wallashop.co.il`). It inherits functionalities from the generic `Graber` class and overrides specific methods for handling Wallashop-specific scenarios.

## Details

The `Graber` class extends the functionality of the generic `Graber` class by defining specific behaviors for Wallashop, including:

- **Overriding Field Extraction Functions**:  It provides customized functions for extracting individual product fields from the Wallashop page.

- **Decorator for Pre-Request Actions**: The module allows defining a decorator to perform actions before sending a request to the web driver. This decorator is defined in the parent `Graber` class.

- **Customized Decorator Behavior**:  If the `Context.locator` value is set, the decorator will execute.  Developers can override the default decorator behavior by uncommenting the decorator lines and implementing custom logic.

## Classes

### `Graber`

**Description**: This class handles the extraction of product data from the Wallashop website.

**Inherits**: `src.suppliers.graber.Graber` 

**Attributes**:

- `supplier_prefix (str)`: A prefix identifying Wallashop as the supplier.

**Methods**:

- `__init__(self, driver: Driver, lang_index: int)`: Initializes the `Graber` class.

    - **Parameters**:

        - `driver (Driver)`: Instance of the `Driver` class responsible for interacting with the web browser.
        - `lang_index (int)`: Index of the language to be used for data extraction.

    - **Purpose**: Initializes the `Graber` instance, sets the `supplier_prefix` attribute, and calls the parent class constructor to set up basic configuration.

    - **Inner Functions**: 
        - `None`

    - **How the Function Works**: 
        - The function initializes the `supplier_prefix` attribute with 'wallashop'.
        - It then calls the parent class constructor (`__init__` of `Graber`), passing the `supplier_prefix`, `driver`, and `lang_index` as arguments. 
        - This sets up the base configuration of the `Graber` object, including loading default configuration and settings. 
        - The `Config.locator_for_decorator` attribute is set to `None` in this version of the class. This means that the default decorator behavior will not be executed unless a specific value is assigned to `Config.locator_for_decorator`.


## Code Example

```python
                ## \\file /src/suppliers/wallashop/graber.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.wallashop 
	:platform: Windows, Unix
	:synopsis: Класс собирает значение полей на странице  товара `wallashop.co.il`. 
    Для каждого поля страницы товара сделана функция обработки поля в родительском классе.
    Если нужна нестандертная обработка, функция перегружается в этом классе.
    ------------------
    Перед отправкой запроса к вебдрайверу можно совершить предварительные действия через декоратор. 
    Декоратор по умолчанию находится в родительском классе. Для того, чтобы декоратор сработал надо передать значение 
    в `Context.locator`, Если надо реализовать свой декоратор - раскоментируйте строки с декоратором и переопределите его поведение


"""

from typing import Optional, Any
from types import SimpleNamespace
import header
from src.suppliers.graber import Graber as Grbr, Config, close_pop_up
from src.webdriver.driver import Driver
from src.logger.logger import logger



class Graber(Grbr):
    """Класс для операций захвата Wallashop."""
    supplier_prefix: str

    def __init__(self, driver: Driver, lang_index:int):
        """Инициализация класса сбора полей товара."""
        self.supplier_prefix = 'wallashop'
        super().__init__(supplier_prefix=self.supplier_prefix, driver=driver, lang_index=lang_index)

        # Закрыватель поп ап `@close_pop_up`
        Config.locator_for_decorator = None # <- если будет уастановлено значение - то оно выполнится в декораторе `@close_pop_up`
```