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

## \file /hypotez/src/suppliers/readme.md
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
# `webdriver` Module and Supplier Data Collection System (`graber`)

## General Overview

This set of modules is designed to automate interaction with web browsers (primarily Firefox) using Selenium WebDriver and for collecting (parsing/grabbing) structured data from product pages on supplier websites.

The main goal is to provide a flexible and extensible tool for:

1.  **WebDriver Management:** Setting up, launching, and managing an instance of the Firefox browser with support for profiles, launch options, proxies, and custom headers.
2.  **Interaction with Web Pages:** Finding elements using various strategies (locators), performing actions (clicks, typing text), getting attributes and content, executing JavaScript.
3.  **Collecting Product Data:** Extracting specific information (name, price, description, features, images, etc.) from supplier product pages using customizable locators and scripts.

## Key Components and Capabilities

*   **Extended WebDriver (`firefox.py`, `driver.py`, `js.py`):**
    *   Initializing Firefox with flexible configuration through `firefox.json`.
    *   Support for Firefox profiles (system or internal).
    *   Managing launch options (windowless, kiosk, custom arguments).
    *   Automatic User-Agent setup (random or from config).
    *   Integrated proxy support (`proxy.py`): loading a list, checking, and automatically setting a working proxy (SOCKS4/SOCKS5/HTTP) when the option is enabled.
    *   Helper methods for common tasks: `get_url` (with loading wait), `scroll`, `wait`, `fetch_html`, `locale` (page language detection).
    *   Utilities for executing JavaScript (`js.py`): `readyState`, `window_focus`, `get_referrer`, `get_page_lang`, `unhide_DOM_element`.
*   **Powerful Locator Executor (`executor.py`):**
    *   `ExecuteLocator` class for asynchronous element searching and action execution.
    *   Support for various search strategies (`By.XPATH`, `By.CSS_SELECTOR`, `By.ID`, etc.).
    *   Description of locators and actions in the form of dictionaries or `SimpleNamespace`.
    *   Performing various events: `click()`, `type(...)`, `send_keys(...)`, `clear()`, `pause(...)`, `upload_media()`, `screenshot()`.
    *   Getting attributes, text, or the WebElements themselves (`WebElement`).
    *   Flexible handling of element lists (`if_list`: "all", "first", "last", "even", "odd", index, list of indices).
    *   Setting timeouts for waiting for elements (`presence_of_element_located`, `visibility_of_all_elements_located`).
    *   Ability to take a screenshot of a specific element (`get_webelement_as_screenshot`).
    *   Method for "typing" text with a delay (`send_message`).
*   **Data Collection System (`graber.py`, `get_graber_by_supplier.py`, `suppliers_list/*/graber.py`):**
    *   Base `Graber` class (`graber.py`) with common methods for collecting data from a product page.
    *   A separate `Graber` subclass is created for each supplier (e.g., `KspGraber`, `AliexpressGraber`) in the `src/suppliers/suppliers_list/<supplier_prefix>/` directory.
    *   Loading locators for product fields (`product.json`) and categories (`category.json`) for a specific supplier.
    *   Methods for extracting each product field (e.g., `name()`, `price()`, `description()`, `specification()`, `local_image_path()`). These methods use `driver.execute_locator` with the appropriate locators.
    *   **Ability to override** field collection methods in subclasses to implement specific supplier logic.
    *   The main collection method `grab_page_async(*fields_to_grab)` for extracting the specified fields.
    *   **Scenario Execution:**
        *   Loading scenarios from JSON files in the `src/suppliers/suppliers_list/<supplier_prefix>/scenarios/` directory.
        *   `process_supplier_scenarios_async` and `process_scenarios` methods for automatically traversing categories (according to the logic in the supplier's `scenario.py`), collecting data for each product, and (in the example) adding it through `PrestaProduct`.
    *   Factory functions (`get_graber_by_supplier.py`) for getting the correct graber instance by URL or supplier prefix.
    *   The `@close_pop_up()` decorator for performing an action (e.g., closing a pop-up window) before collecting a field (configurable via `Config.locator_for_decorator`).

## Module Structure

*   `/src/webdriver/`: Modules for working with WebDriver.
    *   `driver.py`: General helper methods for the driver.
    *   `firefox/`: Everything for Firefox.
        *   `firefox.py`: `Firefox` class, initialization, configuration, implementation of methods.
        *   `firefox.json`: Firefox configuration file.
    *   `js.py`: JavaScript utilities.
    *   `executor.py`: `ExecuteLocator` for working with elements.
    *   `proxy.py`: Proxy logic.
    *   `proxies.txt`: (Automatically created) Proxy list.
*   `/src/suppliers/`: Modules for working with suppliers.
    *   `graber.py`: Base `Graber` class.
    *   `get_graber_by_supplier.py`: Factory for getting the right graber.
    *   `suppliers_list/`: Directory for each supplier.
        *   `<supplier_prefix>/`: Folder for a specific supplier (e.g., `ksp`, `aliexpress`).
            *   `graber.py`: `Graber` subclass for this supplier (with potential method overrides).
            *   `locators/`: JSON files with locators.
                *   `product.json`: Locators for fields on the product page.
                *   `category.json`: Locators for elements on the category page.
            *   `scenarios/`: JSON files with data collection scenarios (e.g., category URLs and corresponding category IDs in PrestaShop).
            *   `scenario.py`: (Optional, but used in `process_scenarios`) Python module with scenario logic, e.g., the `get_list_products_in_category` function for getting product links from a category page.

## Installing Dependencies

Make sure the necessary libraries are installed:

```bash
pip install selenium requests fake-useragent # Add others if used (e.g., langdetect)
```

You also need to:

1.  Install the **Mozilla Firefox** browser.
2.  Download **GeckoDriver**, compatible with your version of Firefox and OS.
3.  Specify the **correct paths** to `firefox.exe` (or the Firefox binary) and `geckodriver.exe` in the `src/webdriver/firefox/firefox.json` file.

## Configuration (`firefox.json`)

The `/src/webdriver/firefox/firefox.json` file manages Firefox driver settings.

```json
{
  "options": [], // Additional Firefox command-line arguments (e.g., "--private")
  "disabled_options": [ "--kiosk", "--headless" ], // Example of disabled options (not used)
  "profile_directory": {
    // Path to the Firefox profile
    "os": "%LOCALAPPDATA%\\\\Mozilla\\\\Firefox\\\\Profiles\\\\xxxxx.default-release", // System profile (Windows)
    "internal": "webdriver\\\\firefox\\\\profiles\\\\xxxxx.default-release", // Profile within the project
    "default": "os" // Use "os" or "internal" by default
  },
  "executable_path": {
    // Paths to executables (relative to project root)
    "firefox_binary": "bin\\\\webdrivers\\\\firefox\\\\ff\\\\core-XXX\\\\firefox.exe",
    "geckodriver": "bin\\\\webdrivers\\\\firefox\\\\gecko\\\\XXX\\\\geckodriver.exe"
  },
  "headers": { // Set through preferences, not direct HTTP headers
    "User-Agent": "Mozilla/5.0 ...", // User-Agent override
    "Accept": "text/html...",
    // ... others
    "Connection": "keep-alive"
  },
  "proxy_enabled": false, // Use a proxy? (true/false)
  "window_mode": null // Window mode: null (normal), "kiosk", "headless", etc.
}
```

**Important:**

*   Paths in `executable_path` and `profile_directory.internal` should be specified **relative to the project root**.
*   The `%LOCALAPPDATA%` environment variable (for `profile_directory.os`) will be automatically expanded in Windows.
*   Make sure the specified paths and driver versions are **current** for your system.

## Usage

### 1. Initializing WebDriver

```python
import asyncio
from src.webdriver.firefox import Firefox
from src.logger.logger import logger

try:
    # Initialization with settings from firefox.json
    # You can override parameters: window_mode, profile_name
    driver = Firefox(window_mode="kiosk")
    # Or use the default settings:
    # driver = Firefox()
    logger.info("Firefox driver successfully launched.")
except Exception as e:
    logger.critical(f"Failed to initialize Firefox driver: {e}")
    exit()

# 'driver' now contains standard Selenium methods + added ones
```

### 2. Basic Actions with WebDriver

```python
# Go to the URL
if driver.get_url("https://www.example.com"):
    logger.info(f"Went to {driver.current_url}")

    # Scroll the page
    driver.scroll(scrolls=1, direction='down')

    # Waiting
    driver.wait(1)

    # Get HTML
    html = driver.fetch_html()
    if html:
        logger.info("HTML received.")
else:
    logger.error("Failed to load the page.")

# Close the driver
# driver.quit()
```

### 3. Interaction with Elements (`ExecuteLocator`)

```python
from types import SimpleNamespace

# Define the locator (dictionary or SimpleNamespace)
login_button_locator = {
    "locator_description": "Login Button",
    "by": "id",
    "selector": "login-button",
    "event": "click()", # Action - click
    "mandatory": True,
    "timeout": 10
}

input_field_locator = SimpleNamespace(
    locator_description="Username input field",
    by="css selector",
    selector="input[name='username']",
    # event="type(MyLogin)", # Enter text
    attribute="value", # Or get the 'value' attribute
    mandatory=True,
    timeout=5
)

async def perform_actions():
    # Perform a click
    click_success = await driver.execute_locator(login_button_locator)
    if click_success:
        logger.info("Click performed.")

    # Get the value of the attribute
    input_value = await driver.execute_locator(input_field_locator)
    if input_value is not None:
        logger.info(f"Value of the input field: {input_value}")

    # You can also get WebElement if event and attribute are not specified
    element = await driver.get_webelement_by_locator(input_field_locator)
    if element:
        logger.info(f"Element found: {element.tag_name}")

# Run the asynchronous function
# asyncio.run(perform_actions())

# IMPORTANT: driver.execute_locator and other methods in executor.py are asynchronous!
```

### 4. Using the Data Collection System (`Graber`)

**Scenario 1: Running automatic collection according to supplier scenarios**

```python
from src.suppliers.get_graber_by_supplier import get_graber_by_supplier_prefix
# Assuming the driver is already initialized

supplier = "ksp" # Supplier prefix
lang_id = 2 # Language ID in PrestaShop

# Get a graber instance for KSP
graber = get_graber_by_supplier_prefix(driver, supplier, lang_index=lang_id)

if graber:
    logger.info(f"Graber for '{supplier}' obtained.")

    async def run_supplier_processing():
        # Run processing of all scenarios from the scenarios/ folder for ksp
        # This function will automatically traverse categories, get product URLs,
        # call grab_page_async for each, and add the product to PrestaShop
        # (according to the logic in graber.py and scenario.py)
        results = await graber.process_supplier_scenarios_async(supplier_prefix=supplier, id_lang=lang_id)
        if results:
            logger.info(f"Processing scenarios for '{supplier}' completed. {len(results)} products collected.")
        else:
            logger.error(f"Error processing scenarios for '{supplier}'.")

    # Launch
    asyncio.run(run_supplier_processing())

else:
    logger.error(f"Failed to get graber for supplier '{supplier}'.")

```

**Scenario 2: Manual data collection from a specific product page**

```python
from src.suppliers.get_graber_by_supplier import get_graber_by_supplier_url
# Assuming the driver is already initialized

product_url = "https://ksp.co.il/web/item/12345" # Example product URL
lang_id = 2

# Get the graber by URL
graber = get_graber_by_supplier_url(driver, product_url, lang_index=lang_id)
# Important: get_graber_by_supplier_url already executes driver.get_url(product_url)

if graber:
    logger.info(f"Graber for URL {product_url} obtained.")

    async def grab_single_product():
        # Determine which fields we want to collect
        fields_to_grab = [
            'id_product', 'name', 'price', 'description',
            'specification', 'local_image_path', 'id_supplier'
        ]
        # Call the collection method for the current page
        product_data: ProductFields = await graber.grab_page_async(*fields_to_grab, id_lang=lang_id)

        if product_data:
            logger.success(f"Data for product successfully collected:")
            # Display or process the collected data
            print(product_data.to_dict()) # Example of dictionary output
            # Further actions: saving to the database, sending to the API, etc.
            # For example, adding through PrestaProduct
            # from src.endpoints.prestashop.product import PrestaProduct
            # pp = PrestaProduct()
            # pp.add_new_product(product_data)
        else:
            logger.error(f"Failed to collect data from page {product_url}")

    # Launch
    asyncio.run(grab_single_product())

else:
    logger.error(f"No suitable graber found for URL: {product_url}")

# Don't forget to close the driver after all operations
driver.quit()
```

### 5. Logging

The module uses a configured logger (`src/logger/logger.py`) to output information about the operation process, warnings, and errors. Set the logging level and format in the logger file.

## Completing Work

Always close WebDriver after finishing work to free up resources:

```python
driver.quit()
```
"""