**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use This Code Block
=========================================================================================

Description
-------------------------
[Explanation of what the code does.]

Execution Steps
-------------------------
1. [Description of the first step.]
2. [Description of the second step.]
3. [Continue as needed...]

Usage Example
-------------------------

```python
    [Code usage example]
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".
```

## webdriver Module

This module provides a unified and extended interface for working with Selenium webdrivers (in this example, focusing on Firefox), simplifying the automation of web page interactions.

### Overview
- **Initialization and Driver Configuration**: Flexible configuration of browser launch parameters (Firefox), including paths to executable files, using profiles, launch options (e.g., kiosk, headless), configuring the User-Agent, and working with proxies.
- **Element Interaction**: A powerful mechanism (`ExecuteLocator`) for finding elements on the page using various strategies (CSS selectors, XPath, ID, etc.) and performing actions on them (click, entering text, retrieving attributes, taking screenshots of the element). Supports complex scenarios with element waiting and list handling.
- **JavaScript Execution**: Utilities (`JavaScript`) for executing typical JS scripts on the page (e.g., checking `readyState`, getting the page language, changing the visibility of DOM elements, setting focus on the window).
- **Proxy Management**: Functionality (`proxy.py`) for loading proxy lists from a remote source, parsing them, and checking their functionality. Integrated with Firefox driver configuration.
- **Helper Methods**: Convenient methods for common tasks such as navigation (`get_url`), page scrolling (`scroll`), waiting (`wait`), and getting HTML code (`fetch_html`).

### Structure
- `/src/webdriver/`
    - `driver.py`: Contains the base `Driver` class (although the example uses direct inheritance from `selenium.webdriver.Firefox`), defining general methods for interacting with the driver (`get_url`, `scroll`, `wait`, `fetch_html`, `locale`, etc.).
    - `firefox/`
        - `firefox.py`: Implementation of the `Firefox` class, inheriting from `selenium.webdriver.Firefox`. Responsible for initializing GeckoDriver, configuring options, profiles, and proxies for Firefox and "injecting" (`_payload`) methods from `ExecuteLocator` and `JavaScript` into the driver instance.
        - `firefox.json`: Configuration file for the Firefox driver.
    - `js.py`: The `JavaScript` class with methods for executing JS scripts.
    - `executor.py`: The `ExecuteLocator` class for finding elements and performing actions on them based on locator dictionaries. Uses `asyncio` for some operations.
    - `proxy.py`: Functions for working with proxy servers.
    - `proxies.txt`: (Automatically created/updated) File for storing a list of proxies.

### Dependencies
Before using the `webdriver` module, ensure you have installed the required libraries:

```bash
pip install selenium requests fake-useragent
```

You also need to have the Firefox browser and the corresponding GeckoDriver installed. Paths to them are specified in the configuration file.

### Configuration (`firefox.json`)
Firefox driver configuration is done through the `/src/webdriver/firefox/firefox.json` file.

```json
{
  "options": [], // Additional command-line arguments for Firefox (e.g., "--private")
  "disabled_options": [ "--kiosk", "--headless" ], // Options that are temporarily disabled (for information)
  "profile_directory": {
    // Path to the Firefox profile
    "os": "%LOCALAPPDATA%\\\\Mozilla\\\\Firefox\\\\Profiles\\\\95c5aq3n.default-release", // Path to the system profile (Windows)
    "internal": "webdriver\\\\firefox\\\\profiles\\\\95c5aq3n.default-release", // Path to the profile inside the project
    "default": "os" // Which profile to use by default ("os" or "internal")
                     // You can also specify the name of a specific profile when creating a Firefox instance (profile_name="...")
  },
  "executable_path": {
    // Paths to executable files
    "firefox_binary": "bin\\\\webdrivers\\\\firefox\\\\ff\\\\core-127.0.2\\\\firefox.exe", // Path to firefox.exe
    "geckodriver": "bin\\\\webdrivers\\\\firefox\\\\gecko\\\\33\\\\geckodriver.exe" // Path to geckodriver.exe
  },
  "headers": {
    // Headers that will be set through preferences (not direct HTTP request headers)
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) ...", // Overriding User-Agent
    "Accept": "text/html...",
    // ... other headers
    "Connection": "keep-alive"
  },
  "proxy_enabled": false, // Enable/disable proxy usage (true/false)
                          // If true, the module will try to download, check, and set a working SOCKS4/SOCKS5 proxy
  "window_mode": null // Window mode: null (normal), "kiosk", "headless", etc.
                      // Can be overridden when creating a Firefox instance (window_mode="...")
}
```

**Important:** The paths in `executable_path` and `profile_directory` are specified relative to the project root (defined by `header.__root__` or `gs.path.root`). The `%LOCALAPPDATA%` variable will be automatically replaced with the corresponding path in Windows.

### Usage

#### 1. Initializing the Firefox Driver

```python
import asyncio
from pathlib import Path
from types import SimpleNamespace

# It is assumed that the project structure is set up and gs/header are available
# import header
# from src import gs
from src.webdriver.firefox import Firefox
from src.logger.logger import logger # Used for logging

# Initialize the driver using settings from firefox.json
# You can override some parameters during initialization:
try:
    # Example with kiosk mode
    driver = Firefox(window_mode="kiosk", profile_name="my_custom_profile")
    # Or simply use the default settings from JSON
    # driver = Firefox()
    logger.info("Firefox driver successfully launched.")
except Exception as e:
    logger.critical(f"Failed to initialize Firefox driver: {e}")
    # Exit or further error handling
    exit()

# Now the 'driver' instance contains both standard Selenium methods
# as well as added methods from JavaScript and ExecuteLocator.
```

#### 2. Navigation and Basic Actions

```python
# Navigate to a URL
if driver.get_url("https://www.google.com"):
    logger.info(f"Successfully navigated to {driver.current_url}")
    # Waiting for loading (checking document.readyState) is already built into get_url

    # Explicit waiting (if necessary)
    driver.wait(1.5) # Wait for 1.5 seconds

    # Scrolling the page
    driver.scroll(scrolls=2, direction='down', delay=0.5) # Scroll down twice with a 0.5s delay

    # Getting the page language
    lang = driver.get_page_lang()
    logger.info(f"Page language: {lang}") # Uses JavaScript

    # Getting the referrer
    referrer = driver.get_referrer()
    logger.info(f"Referrer: {referrer}") # Uses JavaScript

else:
    logger.error("Failed to load the page.")

# Getting the HTML code of the current page
html = driver.fetch_html() # Returns driver.page_source after successful get_url
if html:
    logger.info(f"Received {len(html)} bytes of HTML.")

# Getting HTML from a local file
# local_file_path = Path("path/to/your/file.html").absolute()
# file_uri = local_file_path.as_uri() # Converts the path to file:///...
# html_local = driver.fetch_html(file_uri)
# if html_local:
#    logger.info(f"HTML from file: {html_local[:100]}...")

```

#### 3. Interaction with Elements using `ExecuteLocator`

`ExecuteLocator` allows you to perform actions on elements using dictionaries or `SimpleNamespace` to describe the locator and action.

```python
# Example locator dictionary for the Google search button
search_button_locator = {
    "locator_description": "Search button 'Google Search'", # Description for logs
    "by": "xpath",
    "selector": "(//input[@name=\'btnK\'])[2]", # Element selector
    "event": "click()", # Action: click
    "attribute": None, # Attribute not retrieved
    "if_list": "first", # If multiple found, take the first
    "mandatory": True, # Locator is required, error if not found
    "timeout": 5 # Timeout for waiting for the element (seconds)
}

# Locator for the input field
search_input_locator = SimpleNamespace(
    locator_description="Search input field",
    by="css selector",
    selector="textarea[name=\'q\']",
    event="type(My search query)", # Action: enter text
    # event="clear();type(My query);send_keys(ENTER)", # You can combine events using ';'
    attribute=None,
    if_list="first",
    mandatory=True,
    timeout=5
)

# Locator for getting an attribute (e.g., the value)
some_value_locator = {
    "locator_description": "Get the value of the button",
    "by": "xpath",
    "selector": "(//input[@name=\'btnK\'])[2]",
    "event": None, # No action
    "attribute": "value", # Get the value of the 'value' attribute
    "if_list": "first",
    "mandatory": False, # Optional locator
    "timeout": 3
}

# Locator for getting the text of all links in the results
# (example is hypothetical, the selector may be different)
results_links_locator = {
    "locator_description": "Search results links",
    "by": "css selector",
    "selector": "div.g a h3", # Approximate selector for link titles
    "event": None,
    "attribute": "textContent", # Get the text content
    "if_list": "all", # Get all found elements
    "mandatory": False,
    "timeout": 10,
    "timeout_for_event": "visibility_of_all_elements_located" # Wait for all elements to be visible
}

# --- Executing Locators ---
# Use asyncio.run or an existing event loop for async functions

async def main_interaction():
    try:
        # 1. Enter text in the search field
        success_input = await driver.execute_locator(search_input_locator, typing_speed=0.05) # Slow typing
        if success_input:
            logger.info("Text entered successfully.")
            await asyncio.sleep(1) # Short pause

            # 2. Click the search button
            success_click = await driver.execute_locator(search_button_locator)
            if success_click:
                logger.info("Click on the button executed.")
                await asyncio.sleep(2) # Pause for results to load

                # 3. Get the attribute value
                button_value = await driver.execute_locator(some_value_locator)
                if button_value:
                    logger.info(f"Value of the 'value' attribute of the button: {button_value}")

                # 4. Get the text of all links
                link_texts = await driver.execute_locator(results_links_locator)
                if link_texts:
                    logger.info("Found link texts:")
                    for i, text in enumerate(link_texts):
                        logger.info(f"  {i+1}: {text}")
                else:
                    logger.warning("Search result links not found.")

            else:
                logger.error("Failed to click the button.")
        else:
            logger.error("Failed to enter text.")

    except Exception as e:
        logger.error(f"Error during interaction: {e}")

# Running the asynchronous function
# asyncio.run(main_interaction()) # In real code

# --- Additional Capabilities of ExecuteLocator ---

# Getting WebElement (if event and attribute are not specified)
async def get_element():
     element = await driver.get_webelement_by_locator(search_input_locator)
     if element:
         logger.info(f"WebElement found: {element.tag_name}")
         # Make the element visible (if it is hidden by styles)
         driver.unhide_DOM_element(element)
         logger.info("Attempting to make the element visible (JS).")

         # Screenshot of a specific element
         screenshot_bytes = await driver.get_webelement_as_screenshot(search_input_locator)
         if screenshot_bytes:
             with open("element_screenshot.png", "wb") as f:
                 f.write(screenshot_bytes)
             logger.info("Element screenshot saved to element_screenshot.png")

# asyncio.run(get_element()) # In real code

# Sending a message with Shift+Enter emulation (if necessary)
message_locator = search_input_locator # Using the same input field locator
# message_locator.event = None # Remove the previous type event
async def send_complex_message():
    message = "First line;Second line after carriage return"
    success = await driver.send_message(message_locator, message=message, typing_speed=0.02)
    if success:
        logger.info("Message with carriage return sent.")

# asyncio.run(send_complex_message()) # In real code

```

#### 4. Closing

```python
# Close the browser and end the WebDriver session
driver.quit()
logger.info("Firefox driver closed.")
```

### Logging
The module actively uses a logger configured in `/src/logger/logger.py`. The logging level and output format can be adjusted there. Execution errors, timeouts, and important steps are logged to facilitate debugging.

### Working with Proxies
If `"proxy_enabled": true` is set in `firefox.json`, then when initializing `Firefox()`:

1. `download_proxies_list()` is called to download/update `proxies.txt` from the URL specified in `proxy.py`.
2. `get_proxies_dict()` is called to parse `proxies.txt`.
3. The module iterates through random SOCKS4/SOCKS5 proxies from the list.
4. `check_proxy()` is called for each proxy, which attempts to make a request through it.
5. The first successfully verified proxy is set in Firefox settings through `options.set_preference`.
6. If a working proxy is not found, a warning is output to the log.

```python