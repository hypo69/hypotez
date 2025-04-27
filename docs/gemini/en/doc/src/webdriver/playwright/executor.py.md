# PlaywrightExecutor Module

## Overview

This module (`src/webdriver/playwright/executor.py`) provides functionalities to interact with web elements using Playwright based on provided locators. It handles parsing locators, interacting with elements, and error handling.

## Details

The `PlaywrightExecutor` class is the core component of this module. It uses Playwright to launch a browser instance (Chromium, Firefox, or Webkit) and provides methods for interacting with web elements.

## Classes

### `PlaywrightExecutor`

**Description**: This class executes commands based on executor-style locator commands using Playwright. It handles parsing locators, interacting with elements, and error handling.

**Inherits**: None

**Attributes**:

- `driver`: The Playwright driver instance (e.g., `async_playwright().start()`).
- `browser_type`: The type of browser to launch (e.g., `'chromium'`, `'firefox'`, `'webkit'`).
- `page`: The Playwright page instance.
- `config`: A SimpleNamespace object containing Playwright configuration settings from `playwrid.json`.

**Methods**:

#### `start()`

**Purpose**: Initializes Playwright and launches a browser instance.

**Parameters**: None

**Returns**: None

**Raises Exceptions**:

- `Exception`: If Playwright fails to start the browser.

**How the Function Works**: 

- Starts the Playwright driver using `async_playwright().start()`.
- Launches a browser instance based on `self.browser_type` with specified options from the `config`.
- Creates a new page using `browser.new_page()`.

**Example**: 

```python
executor = PlaywrightExecutor(browser_type='chromium')
await executor.start()
```

#### `stop()`

**Purpose**: Closes Playwright browser and stops its instance.

**Parameters**: None

**Returns**: None

**Raises Exceptions**:

- `Exception`: If Playwright fails to close the browser.

**How the Function Works**:

- If `self.page` exists, closes the page.
- If `self.driver` exists, stops the driver and sets it to `None`.

**Example**:

```python
await executor.stop()
```

#### `execute_locator()`

**Purpose**: Executes actions on a web element based on the provided locator.

**Parameters**:

- `locator`: Locator data (dict or SimpleNamespace).
- `message`: Optional message for events.
- `typing_speed`: Optional typing speed for events.
- `timeout`: Timeout for locating the element (seconds).
- `timeout_for_event`: Wait condition ('presence_of_element_located', 'visibility_of_all_elements_located').

**Returns**: 
The result of the operation, which can be a string, list, dict, Locator, bool, or None.

**Raises Exceptions**: None

**How the Function Works**:

- Parses the locator data.
- If the locator has an `event` and `attribute`, but lacks a `mandatory` flag, it skips execution.
- If the locator has an `attribute` and `by`, it retrieves the attribute value or executes the event.
- If the locator has `selector` and `by` lists and is sorted by "pairs", it iterates through each pair of locators and executes them.
- If the locator doesn't contain valid `selector` and `by` lists or an invalid `sorted` value, it logs a warning.

**Inner Functions**:

- `_parse_locator()`: Parses and executes locator instructions.

**Examples**:

```python
# Example 1: Click on a button
locator = {
    "by": "XPATH",
    "selector": "//button[@id='submit-button']",
    "event": "click()",
}

result = await executor.execute_locator(locator)

# Example 2: Get the text content of an element
locator = {
    "by": "CSS_SELECTOR",
    "selector": ".product-title",
    "attribute": "textContent",
}

text_content = await executor.execute_locator(locator)

# Example 3: Upload a file
locator = {
    "by": "CSS_SELECTOR",
    "selector": "#upload-input",
    "event": "upload_media()",
}

await executor.execute_locator(locator, message="path/to/file.pdf")
```

#### `evaluate_locator()`

**Purpose**: Evaluates and processes locator attributes.

**Parameters**:

- `attribute`: Attribute to evaluate (can be a string, list of strings, or a dictionary).

**Returns**:
The evaluated attribute, which can be a string, list of strings, or dictionary.

**Raises Exceptions**: None

**How the Function Works**: 

- If the attribute is a list, it evaluates each item in the list.
- Otherwise, it directly returns the attribute as a string.

**Inner Functions**:

- `_evaluate()`: Evaluates a single attribute.

**Examples**:

```python
attribute_string = "text_content"
evaluated_attribute = await executor.evaluate_locator(attribute_string)

attribute_list = ["text_content", "href", "id"]
evaluated_attributes = await executor.evaluate_locator(attribute_list)

attribute_dict = {"title": "product-title", "price": ".product-price"}
evaluated_attribute_dict = await executor.evaluate_locator(attribute_dict)
```

#### `get_attribute_by_locator()`

**Purpose**: Gets the specified attribute from the web element.

**Parameters**:

- `locator`: Locator data (dict or SimpleNamespace).

**Returns**:
Attribute or None.

**Raises Exceptions**: None

**How the Function Works**:

- Gets the web element using `get_webelement_by_locator()`.
- If the element is found, it retrieves the specified attribute.
- If the attribute is a dictionary, it retrieves multiple attributes based on the dictionary keys.

**Inner Functions**:

- `_parse_dict_string()`: Parses a string like '{attr1:attr2}' into a dictionary.
- `_get_attribute()`: Retrieves a single attribute from a Locator.
- `_get_attributes_from_dict()`: Retrieves multiple attributes based on a dictionary.

**Examples**:

```python
# Example 1: Get a single attribute
locator = {
    "by": "XPATH",
    "selector": "//h1",
    "attribute": "textContent",
}

text_content = await executor.get_attribute_by_locator(locator)

# Example 2: Get multiple attributes from a dictionary
locator = {
    "by": "XPATH",
    "selector": "//div[@class='product-details']",
    "attribute": "{title:product-title, price:product-price}",
}

attributes = await executor.get_attribute_by_locator(locator)
```

#### `get_webelement_by_locator()`

**Purpose**: Gets a web element using the locator.

**Parameters**:

- `locator`: Locator data (dict or SimpleNamespace).

**Returns**: 
Playwright Locator

**Raises Exceptions**: None

**How the Function Works**:

- If the `by` is "XPATH", it uses the `page.locator(f'xpath={locator.selector}')`.
- Otherwise, it uses `page.locator(locator.selector)`.
- It then filters the elements based on the `if_list` parameter:
    - `'all'`: Returns all elements.
    - `'first'`: Returns the first element.
    - `'last'`: Returns the last element.
    - `'even'`: Returns even-indexed elements.
    - `'odd'`: Returns odd-indexed elements.
    - List of integers: Returns elements at specified indexes.
    - Integer: Returns the element at the specified index.

**Examples**:

```python
# Example 1: Get the first element
locator = {
    "by": "CSS_SELECTOR",
    "selector": ".product-item",
    "if_list": "first",
}

first_element = await executor.get_webelement_by_locator(locator)

# Example 2: Get all elements
locator = {
    "by": "XPATH",
    "selector": "//div[@class='product-list']//a",
    "if_list": "all",
}

all_elements = await executor.get_webelement_by_locator(locator)
```

#### `get_webelement_as_screenshot()`

**Purpose**: Takes a screenshot of the located web element.

**Parameters**:

- `locator`: Locator data (dict or SimpleNamespace).
- `webelement`: The web element Locator.

**Returns**:
Screenshot in bytes or None.

**Raises Exceptions**: None

**How the Function Works**:

- If `webelement` is not provided, it gets the element using `get_webelement_by_locator()`.
- If the element is found, it takes a screenshot using `webelement.screenshot()`.

**Examples**:

```python
# Example 1: Take a screenshot of an element using locator
locator = {
    "by": "XPATH",
    "selector": "//img[@alt='product-image']",
}

screenshot = await executor.get_webelement_as_screenshot(locator)

# Example 2: Take a screenshot of a previously located element
element = await executor.get_webelement_by_locator(locator)
screenshot = await executor.get_webelement_as_screenshot(locator, webelement=element)
```

#### `execute_event()`

**Purpose**: Executes the event associated with the locator.

**Parameters**:

- `locator`: Locator data (dict or SimpleNamespace).
- `message`: Optional message for events.
- `typing_speed`: Optional typing speed for events.

**Returns**:
Execution status.

**Raises Exceptions**: None

**How the Function Works**:

- Gets the web element using `get_webelement_by_locator()`.
- Iterates through the events in the `locator.event` string, separated by semicolons:
    - `click()`: Clicks the element.
    - `pause(duration)`: Pauses for the specified duration.
    - `upload_media()`: Uploads a file.
    - `screenshot()`: Takes a screenshot of the element.
    - `clear()`: Clears the input field.
    - `send_keys(keys)`: Sends keys to the input field.
    - `type(text)`: Types text into the input field with optional typing speed.

**Examples**:

```python
# Example 1: Click a button and then take a screenshot
locator = {
    "by": "XPATH",
    "selector": "//button[@id='submit-button']",
    "event": "click();pause(2);screenshot()",
}

result = await executor.execute_event(locator)

# Example 2: Type text into a field with typing speed
locator = {
    "by": "CSS_SELECTOR",
    "selector": "#search-input",
    "event": "type('Hello World!')",
}

await executor.execute_event(locator, typing_speed=0.1)
```

#### `send_message()`

**Purpose**: Sends a message to a web element.

**Parameters**:

- `locator`: Information about the element's location on the page.
- `message`: The message to be sent to the web element.
- `typing_speed`: Speed of typing the message in seconds.

**Returns**:
Returns `True` if the message was sent successfully, `False` otherwise.

**Raises Exceptions**: None

**How the Function Works**:

- Gets the web element using `get_webelement_by_locator()`.
- Types the message into the element with optional typing speed.

**Examples**:

```python
# Example 1: Send a message with typing speed
locator = {
    "by": "XPATH",
    "selector": "//textarea[@id='message-box']",
}

await executor.send_message(locator, message="Hello there!", typing_speed=0.1)

# Example 2: Send a message without typing speed
locator = {
    "by": "CSS_SELECTOR",
    "selector": "#comment-field",
}

await executor.send_message(locator, message="This is a comment.")
```

#### `goto()`

**Purpose**: Navigates to a specified URL.

**Parameters**:

- `url`: URL to navigate to.

**Returns**: None

**Raises Exceptions**: None

**How the Function Works**:

- Uses `self.page.goto(url)` to navigate to the specified URL.

**Example**:

```python
await executor.goto("https://www.example.com")
```


## Parameter Details

- `locator` (dict | SimpleNamespace): A dictionary or SimpleNamespace object containing information about the web element's location on the page. It typically includes the following keys:
    - `by`: The type of locator (e.g., "XPATH", "CSS_SELECTOR", "VALUE").
    - `selector`: The selector string that uniquely identifies the web element.
    - `attribute`: The attribute to retrieve (e.g., "textContent", "href", "value").
    - `event`: The action to perform on the web element (e.g., "click()", "type('text')", "send_keys('Enter')").
    - `if_list`: Specifies how to handle multiple elements: "first", "last", "all", "even", "odd", list of indexes, or an integer index.
    - `mandatory`: Whether the element is mandatory.
    - `timeout`: Timeout for locating the element in seconds.
    - `timeout_for_event`: The wait condition for the element.
    - `locator_description`: A brief description of the locator for debugging purposes.

- `message` (str): The message to send to the web element (e.g., for typing into a field or uploading a file).

- `typing_speed` (float): The typing speed in seconds for events like "type()" and "send_message()".

- `timeout` (float): The timeout in seconds for locating the web element.

- `timeout_for_event` (str): The wait condition for the element (e.g., "presence_of_element_located", "visibility_of_all_elements_located").

## Examples

```python
from src.webdriver.playwright.executor import PlaywrightExecutor
import asyncio

async def main():
    # Initialize the PlaywrightExecutor
    executor = PlaywrightExecutor(browser_type='chromium')

    # Start the browser
    await executor.start()

    # Navigate to a website
    await executor.goto("https://www.example.com")

    # Click a button
    button_locator = {
        "by": "XPATH",
        "selector": "//button[@id='submit-button']",
        "event": "click()",
    }
    await executor.execute_locator(button_locator)

    # Type text into a field
    text_field_locator = {
        "by": "CSS_SELECTOR",
        "selector": "#search-input",
        "event": "type('Hello World!')",
    }
    await executor.execute_locator(text_field_locator, typing_speed=0.1)

    # Get the text content of an element
    title_locator = {
        "by": "CSS_SELECTOR",
        "selector": "h1",
        "attribute": "textContent",
    }
    title_text = await executor.execute_locator(title_locator)
    print(f"Page title: {title_text}")

    # Take a screenshot of an element
    image_locator = {
        "by": "XPATH",
        "selector": "//img[@alt='product-image']",
    }
    screenshot = await executor.get_webelement_as_screenshot(image_locator)
    with open("screenshot.png", "wb") as f:
        f.write(screenshot)

    # Stop the browser
    await executor.stop()

if __name__ == "__main__":
    asyncio.run(main())