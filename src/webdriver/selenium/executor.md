# Executor Module Documentation

## Introduction

The `executor.py` module is a core component for automated interaction with web pages. It allows finding elements on a page using various locators (e.g., ID, class, XPath), performing actions on them (e.g., click, text input), and retrieving their attribute values. The module also includes mechanisms for waiting for elements to appear and handling potential errors such as timeouts and click interceptions.

This document provides a detailed description of the `executor.py` module, its integration with drivers like `use_pydoll.py`, and how to use it effectively.

## Key Classes and Methods

### `ExecuteLocator` Class

This is the main class in the `executor.py` module. It handles all interactions with web elements based on the provided locators.

**Initialization:**

```python
from selenium.webdriver.remote.webdriver import WebDriver
from src.webdriver.executor import ExecuteLocator

# driver: An instance of a Selenium-compatible WebDriver
driver = ... 
executor = ExecuteLocator(driver=driver)
```

The `ExecuteLocator` class is initialized with a `driver` object that conforms to the `WebDriver` interface. This can be a standard Selenium driver or a custom driver like the one in `use_pydoll.py`.

### Core Methods

#### `execute_locator(...)`

This is the primary method for executing actions on web elements. It orchestrates the process of finding elements, performing events, and retrieving attributes.

**Signature:**

```python
async def execute_locator(
    self,
    locator:  dict | SimpleNamespace,
    timeout: Optional[float] = 0,
    timeout_for_event: Optional[str] = "presence_of_element_located",
    message: Optional[str] = None,
    typing_speed: Optional[float] = 0,
) ->  Optional[str | list | dict | WebElement | bool]:
```

**Parameters:**

*   `locator`: A dictionary or `SimpleNamespace` containing the locator information.
*   `timeout`: The time to wait for the element to be found.
*   `timeout_for_event`: The condition to wait for (e.g., `presence_of_element_located`).
*   `message`: A message to be used for actions like `send_keys`.
*   `typing_speed`: The speed at which to type for `send_keys` events.

**Returns:**

The result of the operation, which can be a string, list, dictionary, `WebElement`, boolean, or `None`.

#### `get_webelement_by_locator(...)`

This method retrieves one or more web elements based on the provided locator.

**Signature:**

```python
async def get_webelement_by_locator(
    self,
    locator: dict | SimpleNamespace,
    timeout: Optional[float] = 0,
    timeout_for_event: Optional[str] = "presence_of_element_located",
) -> Optional[WebElement | List[WebElement]]:
```

This method supports filtering the list of found elements using the `if_list` attribute in the locator.

#### `get_attribute_by_locator(...)`

This method retrieves attributes from a web element or a list of web elements.

**Signature:**

```python
async def get_attribute_by_locator(
    self,
    locator: SimpleNamespace | dict,
    timeout: Optional[float] = 0,
    timeout_for_event: str = "presence_of_element_located",
    message: Optional[str] = None,
    typing_speed: float = 0,
) -> Optional[WebElement | list[WebElement]]:
```

#### `execute_event(...)`

This method executes an event associated with a locator, such as a click or sending keys.

**Signature:**

```python
async def execute_event(
    self,
    locator: SimpleNamespace | dict,
    timeout: float = 5,
    timeout_for_event: str = "presence_of_element_located",
    message: str = None,
    typing_speed: float = 0,
) -> Optional[str | list[str] | bytes | list[bytes] | bool]:
```

## Driver Integration: `use_pydoll.py`

The `executor.py` module is designed to work with any Selenium-compatible WebDriver. The `driverless/use_pydoll.py` file provides an example of such a driver, using the `pydoll` library to control a Chrome browser.

The `Driver` class in `use_pydoll.py` initializes a `pydoll` browser instance and provides methods for interacting with it. The `execute_locator` method in this class serves as a bridge to the `executor.py` module, preparing the locator and calling the appropriate methods.

### Usage Example

Here is a complete workflow demonstrating how to use `executor.py` with the `use_pydoll.py` driver:

1.  **Initialize the Driver:**

    ```python
    from src.webdriver.driverless.use_pydoll import Driver

    # Initialize the driver
    driver = Driver(window_mode='headless')
    await driver.async_init_page()
    ```

2.  **Define a Locator:**

    The `locator` object is a key part of using the executor. It defines how to find an element, what to do with it, and what to return.

    ```python
    from types import SimpleNamespace

    locator = SimpleNamespace(
        attribute="innerText",
        by="XPATH",
        strategy_for_multiple_selectors="find_first_match",
        selector="//span[contains(@class, 'sku-copy')]",
        if_list="first",
        mandatory=True,
        timeout=0,
        timeout_for_event="presence_of_element_located",
        event=None,
        locator_description="product reference"
    )
    ```

3.  **Execute the Locator:**

    ```python
    # The 'execute_locator' method in 'use_pydoll.py' will internally
    # use the 'executor.py' module's logic.
    result = await driver.execute_locator(locator)
    ```

4.  **Process the Result:**

    ```python
    if result:
        print(f"Found product reference: {result}")
    else:
        print("Could not find product reference.")
    ```

## Locator Structure

The `locator` object is a `SimpleNamespace` or dictionary that can contain the following fields:

*   `by`: The method for finding the element (e.g., `XPATH`, `CSS_SELECTOR`, `ID`).
*   `selector`: The selector string for finding the element.
*   `attribute`: The attribute to retrieve from the element (e.g., `innerText`, `href`, `src`). If `None`, the `WebElement` itself is returned.
*   `event`: The event to perform on the element (e.g., `click()`, `send_keys(...)`).
*   `if_list`: A strategy for filtering a list of found elements. Can be `all`, `first`, `last`, `even`, `odd`, an integer index, or a list of indices.
*   `mandatory`: A boolean indicating whether the locator is mandatory. If `True` and the element is not found, an error will be logged.
*   `timeout`: The time to wait for the element to be found.
*   `timeout_for_event`: The condition to wait for.
*   `strategy_for_multiple_selectors`: How to handle multiple selectors in the `selector` field (e.g., `find_first_match`).
*   `locator_description`: A description of the locator for logging purposes.

By combining these fields, you can create complex and powerful interactions with web pages in a structured and reusable way.
