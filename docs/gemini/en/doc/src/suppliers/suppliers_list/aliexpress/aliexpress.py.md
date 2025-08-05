# Module: AliExpress

## Overview

This module provides the `Aliexpress` class, which integrates functionality from `Supplier`, `AliRequests`, and `AliApi` for working with AliExpress. It facilitates interaction with the AliExpress platform, enabling operations like fetching product details, handling requests, and utilizing the AliExpress API.

## Details

The `Aliexpress` class acts as a central hub for interacting with the AliExpress platform. It leverages the `AliRequests` class to manage HTTP requests, the `AliApi` class to interact with the AliExpress API, and the `Supplier` class to provide a general framework for supplier-related operations. 

## Classes

### `Aliexpress`

**Description:** Base class for interacting with AliExpress. Combines functionality from `Supplier`, `AliRequests`, and `AliApi` classes.

**Inherits:**
 - `AliRequests`: Handles HTTP requests for interacting with AliExpress.
 - `AliApi`: Provides methods for utilizing the AliExpress API.

**Attributes:**
 - `supplier_prefix (str):` Prefix identifying the AliExpress supplier. Default: 'aliexpress'.
 - `locale (str | dict):` Language and currency settings. Default: `{'EN': 'USD'}`.
 - `webdriver (bool | str):` Indicates whether to use a webdriver and which browser to use. Default: `False` (no webdriver).
 
**Methods:**

#### `__init__`

```python
    def __init__(self, 
                 webdriver: bool | str = False, 
                 locale: str | dict = {'EN': 'USD'},
                 *args, **kwargs):
        """
        Initialize the Aliexpress class.

        :param webdriver: Webdriver mode. Supported values are:
            - `False` (default): No webdriver.
            - `'chrome'`: Use the Chrome webdriver.
            - `'mozilla'`: Use the Mozilla webdriver.
            - `'edge'`: Use the Edge webdriver.
            - `'default'`: Use the system's default webdriver.
        :type webdriver: bool | str

        :param locale: The language and currency settings for the script.
        :type locale: str | dict

        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.

        **Examples:**

        .. code-block:: python

            # Run without a webdriver
            a = Aliexpress()

            # Webdriver `Chrome`
            a = Aliexpress('chrome')

        """
        ...
        super().__init__(supplier_prefix = 'aliexpress', 
                         locale = locale, 
                         webdriver = webdriver, 
                         *args, **kwargs)

```

**Purpose:** Initializes the `Aliexpress` class with the specified webdriver mode, locale settings, and additional arguments.

**Parameters:**

 - `webdriver (bool | str):`  Specifies the webdriver mode. Supported values are `False` (no webdriver), `'chrome'`, `'mozilla'`, `'edge'`, and `'default'`. 
 - `locale (str | dict):`  Sets the language and currency preferences for the script. Accepts a string or a dictionary.
 - `args:` Additional positional arguments.
 - `kwargs:` Additional keyword arguments.

**Returns:** None.

**Raises Exceptions:** None.

**How the Function Works:** 
- The `__init__` method initializes the `Aliexpress` class.
- It calls the `__init__` method of the superclass (`AliRequests`) using the `super()` function, passing in the `supplier_prefix`, `locale`, `webdriver`, and any additional arguments. This inheritance structure allows for reuse of code from the superclass and the `AliApi` class.

**Examples:**

```python
# Run without a webdriver
a = Aliexpress()

# Webdriver `Chrome`
a = Aliexpress('chrome')

```

## Parameter Details

### `webdriver`

**Description:** 
 - `False`: Disables the use of a webdriver.
 - `'chrome'`: Uses the Chrome webdriver.
 - `'mozilla'`: Uses the Mozilla webdriver.
 - `'edge'`: Uses the Edge webdriver.
 - `'default'`: Uses the system's default webdriver.

### `locale`

**Description:** The language and currency settings for the script. Accepts a string or a dictionary.

## Examples

```python
# Run without a webdriver
a = Aliexpress()

# Webdriver `Chrome`
a = Aliexpress('chrome')