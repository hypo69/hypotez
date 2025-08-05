#  Edge WebDriver
## Overview

This module provides a custom `Edge` WebDriver class extending the standard Selenium `WebDriver` class. This class simplifies WebDriver setup and configuration for Edge by leveraging the `fake_useragent` library and the `src.logger.logger` module.

## Details
This module provides a custom Edge WebDriver class for enhanced functionality, including:

* **Simplified Initialization:**  The `__init__` method automatically sets up a user agent (using `fake_useragent`) and applies options from a configuration file (`edge.json`).
* **Custom Options:** Allows for adding custom Edge options during initialization.
* **Window Mode:**  Offers flexibility in controlling the browser window's appearance, like `kiosk`, `windowless`, or `full_window`.
* **Profile Management:**  Provides control over the user profile used for the Edge browser.
* **Logger Integration:** Includes logging capabilities using the `src.logger.logger` module for tracking WebDriver status and potential errors.
* **Executor Integration:**  The module integrates with the `ExecuteLocator` and `JavaScript` classes from `src.webdriver.executor` and `src.webdriver.js` to simplify web element interaction and JavaScript execution.

This module enhances the `Edge` WebDriver class, making it more flexible, user-friendly, and adaptable for various web automation tasks.


## Classes

### `Edge`
**Description**: Custom Edge WebDriver class for enhanced functionality.

**Inherits**: `selenium.webdriver.Edge`

**Attributes**:
- `driver_name` (str): The name of the WebDriver used, defaults to 'edge'.

**Methods**:

- `__init__(self, profile_name: Optional[str] = None, user_agent: Optional[str] = None, options: Optional[List[str]] = None, window_mode: Optional[str] = None, *args, **kwargs) -> None`: Initializes the Edge WebDriver with the specified user agent and options.
- `_payload(self) -> None`: Loads executors for locators and JavaScript scenarios.
- `set_options(self, opts: Optional[List[str]] = None) -> EdgeOptions`: Creates and configures launch options for the Edge WebDriver.

## Functions

### `__init__(self, profile_name: Optional[str] = None, user_agent: Optional[str] = None, options: Optional[List[str]] = None, window_mode: Optional[str] = None, *args, **kwargs) -> None`

**Purpose**: Initializes the Edge WebDriver with specified user agent, options, and window mode.

**Parameters**:
- `profile_name` (Optional[str], optional): The name of the Edge profile to use. Defaults to `None`.
- `user_agent` (Optional[str], optional):  The user-agent string to be used. If `None`, a random user agent is generated using `fake_useragent`. Defaults to `None`.
- `options` (Optional[List[str]], optional): A list of Edge options to be passed during initialization. Defaults to `None`.
- `window_mode` (Optional[str], optional):  The window mode for the Edge browser, such as `kiosk`, `windowless`, or `full_window`. Defaults to `None`.

**Returns**: `None`

**Raises Exceptions**:
- `WebDriverException`: If the Edge WebDriver fails to start.
- `Exception`: For general errors during WebDriver initialization.

**How the Function Works**:

1. Initializes the `user_agent` using the provided value or generates a random user agent using `fake_useragent`.
2. Loads settings from the `edge.json` configuration file located at `src/webdriver/edge/edge.json`.
3. Creates an `EdgeOptions` object and sets the user agent using the `user_agent` value.
4. Applies window mode settings based on values from both the configuration file and the provided `window_mode` parameter.
5. Adds custom options provided during initialization to the `EdgeOptions` object.
6. Appends options and headers from the configuration file to the `EdgeOptions` object.
7. Configures the user profile directory based on settings from the configuration file.
8. Starts the Edge WebDriver using the `EdgeService` and configured options.
9. Initializes the `_payload` method to set up executors.

**Examples**:

```python
# Creating an Edge WebDriver instance with default settings
driver = Edge()

# Creating an Edge WebDriver instance with a custom user agent
driver = Edge(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36')

# Creating an Edge WebDriver instance with specific options and window mode
driver = Edge(options=['--disable-gpu', '--no-sandbox'], window_mode='kiosk')

# Creating an Edge WebDriver instance with a custom profile
driver = Edge(profile_name='my_profile')
```


### `_payload(self) -> None`

**Purpose**: Loads executors for locators and JavaScript scenarios.

**Parameters**: `None`

**Returns**: `None`

**How the Function Works**:

1. Initializes instances of `JavaScript` and `ExecuteLocator` classes.
2. Assigns methods from the `JavaScript` instance (e.g., `get_page_lang`, `ready_state`, `get_referrer`, `unhide_DOM_element`, `window_focus`) to the `Edge` object.
3. Assigns methods from the `ExecuteLocator` instance (e.g., `execute_locator`, `get_webelement_as_screenshot`, `get_webelement_by_locator`, `get_attribute_by_locator`, `send_message`, `send_key_to_webelement`) to the `Edge` object.

**Examples**:

```python
driver = Edge()
# Accessing the JavaScript executors
driver.get_page_lang()
driver.ready_state()

# Accessing the ExecuteLocator executors
driver.execute_locator({'by': 'XPATH', 'selector': "//button[@id = 'closeXButton']"})
driver.get_webelement_by_locator({'by': 'XPATH', 'selector': "//button[@id = 'closeXButton']"})
```

### `set_options(self, opts: Optional[List[str]] = None) -> EdgeOptions`

**Purpose**: Creates and configures launch options for the Edge WebDriver.

**Parameters**:
- `opts` (Optional[List[str]], optional): A list of options to add to the Edge WebDriver. Defaults to `None`.

**Returns**:  `EdgeOptions`: A configured `EdgeOptions` object.

**How the Function Works**:

1. Creates an `EdgeOptions` object.
2. If `opts` is provided, it adds each option from the `opts` list to the `EdgeOptions` object.
3. Returns the configured `EdgeOptions` object.

**Examples**:

```python
driver = Edge()
# Creating a custom EdgeOptions object
options = driver.set_options(['--disable-gpu', '--no-sandbox'])
# Using the custom options object to start the Edge WebDriver
driver = Edge(options=options)

# Creating a custom EdgeOptions object with specific options
options = driver.set_options(['--disable-gpu', '--no-sandbox', '--headless'])
# Using the custom options object to start the Edge WebDriver
driver = Edge(options=options)
```


## Parameter Details
- `profile_name` (Optional[str], optional): The name of the Edge profile to use. Defaults to `None`. If not provided, the default profile from the configuration file is used.
- `user_agent` (Optional[str], optional): The user-agent string to be used. If `None`, a random user agent is generated using `fake_useragent`. Defaults to `None`. You can specify a specific user agent for better control over browser identification.
- `options` (Optional[List[str]], optional): A list of Edge options to be passed during initialization. Defaults to `None`. This parameter allows for adding specific Edge options, like disabling certain features or enabling specific functionalities.
- `window_mode` (Optional[str], optional): The window mode for the Edge browser, such as `kiosk`, `windowless`, or `full_window`. Defaults to `None`. This parameter gives flexibility in controlling the browser window's appearance.
- `opts` (Optional[List[str]], optional): A list of options to add to the Edge WebDriver. Defaults to `None`. This parameter allows for adding specific Edge options when creating a custom `EdgeOptions` object.

## Examples

```python
# Creating an Edge WebDriver instance with default settings
driver = Edge()

# Creating an Edge WebDriver instance with a custom user agent
driver = Edge(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36')

# Creating an Edge WebDriver instance with specific options and window mode
driver = Edge(options=['--disable-gpu', '--no-sandbox'], window_mode='kiosk')

# Creating an Edge WebDriver instance with a custom profile
driver = Edge(profile_name='my_profile')

# Accessing the JavaScript executors
driver.get_page_lang()
driver.ready_state()

# Accessing the ExecuteLocator executors
driver.execute_locator({'by': 'XPATH', 'selector': "//button[@id = 'closeXButton']"})
driver.get_webelement_by_locator({'by': 'XPATH', 'selector': "//button[@id = 'closeXButton']"})

# Creating a custom EdgeOptions object
options = driver.set_options(['--disable-gpu', '--no-sandbox'])
# Using the custom options object to start the Edge WebDriver
driver = Edge(options=options)

# Creating a custom EdgeOptions object with specific options
options = driver.set_options(['--disable-gpu', '--no-sandbox', '--headless'])
# Using the custom options object to start the Edge WebDriver
driver = Edge(options=options)

# Navigating to a website
driver.get("https://www.example.com")

# Closing the WebDriver instance
driver.quit()
```