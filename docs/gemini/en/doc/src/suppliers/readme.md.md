#  Module: `hypotez/src/suppliers/readme.md`

## Overview

This module serves as the core component for the `hypotez` project, specifically designed to automate data collection from product pages on supplier websites. The module seamlessly integrates with Selenium WebDriver (Firefox) to navigate, interact, and extract structured data from e-commerce platforms. 

## Details

This collection of modules automates the interaction with web browsers (primarily Firefox) using Selenium WebDriver, along with extracting structured data from product pages on supplier websites. 

The primary objective is to provide a flexible and expandable tool to:

1.  **WebDriver Management:** Setting up, launching, and managing Firefox browser instances with support for profiles, launch options, proxy settings, and custom headers.
2.  **Web Page Interaction:** Finding elements using diverse strategies (locators), performing actions (clicks, text input), retrieving attributes and content, and executing JavaScript.
3.  **Product Data Collection:** Extracting specific information (name, price, description, features, images, etc.) from product pages of suppliers using customizable locators and scripts.

## Key Components and Features

*   **Enhanced WebDriver (`firefox.py`, `driver.py`, `js.py`):**
    *   Initializes Firefox with flexible configuration through `firefox.json`.
    *   Supports Firefox profiles (system or internal).
    *   Manages launch options (windowless, kiosk, custom arguments).
    *   Automates User-Agent configuration (random or from config).
    *   Integrated proxy support (`proxy.py`): loads a list, checks, and automatically sets a working proxy (SOCKS4/SOCKS5/HTTP) when enabled.
    *   Helper methods for common tasks: `get_url` (with loading wait), `scroll`, `wait`, `fetch_html`, `locale` (detects page language).
    *   JavaScript execution utilities (`js.py`): `readyState`, `window_focus`, `get_referrer`, `get_page_lang`, `unhide_DOM_element`.
*   **Powerful Locator Executor (`executor.py`):**
    *   `ExecuteLocator` class for asynchronous element search and action execution.
    *   Supports diverse search strategies (`By.XPATH`, `By.CSS_SELECTOR`, `By.ID`, etc.).
    *   Describes locators and actions as dictionaries or `SimpleNamespace`.
    *   Performs various events: `click()`, `type(...)`, `send_keys(...)`, `clear()`, `pause(...)`, `upload_media()`, `screenshot()`.
    *   Retrieves attributes, text, or web elements (`WebElement`).
    *   Flexible handling of element lists (`if_list`: "all", "first", "last", "even", "odd", index, list of indices).
    *   Customizable element wait timeouts (`presence_of_element_located`, `visibility_of_all_elements_located`).
    *   Capability to take a screenshot of a specific element (`get_webelement_as_screenshot`).
    *   Method for "typing" text with a delay (`send_message`).
*   **Data Collection System (`graber.py`, `get_graber_by_supplier.py`, `suppliers_list/*/graber.py`):**
    *   Base `Graber` class (`graber.py`) with common methods for collecting data from product pages.
    *   A separate `Graber` subclass is created for each supplier (e.g., `KspGraber`, `AliexpressGraber`) in the directory `src/suppliers/suppliers_list/<supplier_prefix>/`.
    *   Loads locators for product fields (`product.json`) and categories (`category.json`) for a specific supplier.
    *   Methods for extracting each product field (e.g., `name()`, `price()`, `description()`, `specification()`, `local_image_path()`). These methods use `driver.execute_locator` with corresponding locators.
    *   **Override capability** for data collection methods in subclasses to implement supplier-specific logic.
    *   Primary collection method `grab_page_async(*fields_to_grab)` for extracting specified fields.
    *   **Scenario execution:**
        *   Loads scenarios from JSON files in the directory `src/suppliers/suppliers_list/<supplier_prefix>/scenarios/`.
        *   `process_supplier_scenarios_async` and `process_scenarios` methods for automatically iterating through categories (according to the logic in the supplier's `scenario.py`), collecting data for each product, and (in the example) adding it through `PrestaProduct`.
    *   Factory functions (`get_graber_by_supplier.py`) for obtaining the required graber instance based on the URL or supplier prefix.
    *   `@close_pop_up()` decorator for executing an action (e.g., closing a pop-up window) before collecting a field (configured via `Config.locator_for_decorator`).

## Module Structure

*   `/src/webdriver/`: Modules for working with WebDriver.
    *   `driver.py`: General helper methods for the driver.
    *   `firefox/`: Everything for Firefox.
        *   `firefox.py`: `Firefox` class, initialization, setup, method integration.
        *   `firefox.json`: Firefox configuration file.
    *   `js.py`: JavaScript utilities.
    *   `executor.py`: `ExecuteLocator` for working with elements.
    *   `proxy.py`: Logic for working with proxies.
    *   `proxies.txt`: (Automatically generated) List of proxies.
*   `/src/suppliers/`: Modules for working with suppliers.
    *   `graber.py`: Base `Graber` class.
    *   `get_graber_by_supplier.py`: Factory for obtaining the required graber.
    *   `suppliers_list/`: Directory for each supplier.
        *   `<supplier_prefix>/`: Folder for a specific supplier (e.g., `ksp`, `aliexpress`).
            *   `graber.py`: `Graber` subclass for this supplier (with potential method overrides).
            *   `locators/`: JSON files with locators.
                *   `product.json`: Locators for fields on the product page.
                *   `category.json`: Locators for elements on the category page.
            *   `scenarios/`: JSON files with data collection scenarios (e.g., category URLs and corresponding category IDs in PrestaShop).
            *   `scenario.py`: (Optional, but used in `process_scenarios`) Python module with scenario logic, such as the `get_list_products_in_category` function for obtaining product links from the category page.

## Installing Dependencies

Make sure you have the required libraries installed:

```bash
pip install selenium requests fake-useragent # Add others if used (e.g., langdetect)
```

You also need:

1.  Install the **Mozilla Firefox** browser.
2.  Download **GeckoDriver**, compatible with your version of Firefox and OS.
3.  Specify the **correct paths** to `firefox.exe` (or Firefox binary) and `geckodriver.exe` in the file `src/webdriver/firefox/firefox.json`.

## Configuration (`firefox.json`)

The file `/src/webdriver/firefox/firefox.json` manages the configuration settings for the Firefox driver.

```json
{
  "options": [], // Additional Firefox command-line arguments (e.g., "--private")
  "disabled_options": [ "--kiosk", "--headless" ], // Example of disabled options (not used)
  "profile_directory": {
    // Path to the Firefox profile
    "os": "%LOCALAPPDATA%\\\\Mozilla\\\\Firefox\\\\Profiles\\\\xxxxx.default-release", // System profile (Windows)
    "internal": "webdriver\\\\firefox\\\\profiles\\\\xxxxx.default-release", // Profile inside the project
    "default": "os" // Use "os" or "internal" by default
  },
  "executable_path": {
    // Paths to executables (relative to the project root)
    "firefox_binary": "bin\\\\webdrivers\\\\firefox\\\\ff\\\\core-XXX\\\\firefox.exe",
    "geckodriver": "bin\\\\webdrivers\\\\firefox\\\\gecko\\\\XXX\\\\geckodriver.exe"
  },
  "headers": { // Set via preferences, not direct HTTP headers
    "User-Agent": "Mozilla/5.0 ...", // User-Agent override
    "Accept": "text/html...",
    // ... other
    "Connection": "keep-alive"
  },
  "proxy_enabled": false, // Use proxy? (true/false)
  "window_mode": null // Window mode: null (normal), "kiosk", "headless", etc.
}
```

**Important:**

*   Paths in `executable_path` and `profile_directory.internal` should be specified **relative to the project root**.
*   The environment variable `%LOCALAPPDATA%` (for `profile_directory.os`) will be automatically expanded in Windows.
*   Ensure that the specified paths and driver versions are **up-to-date** for your system.

## Usage

### 1. Initializing WebDriver

```python
import asyncio
from src.webdriver.firefox import Firefox
from src.logger.logger import logger

try:
    # Initialization with settings from firefox.json
    # Parameters can be overridden: window_mode, profile_name
    driver = Firefox(window_mode="kiosk")
    # Or use default settings:
    # driver = Firefox()
    logger.info("Firefox driver started successfully.")
except Exception as e:
    logger.critical(f"Failed to initialize Firefox driver: {e}")
    exit()

# 'driver' now contains standard Selenium methods + added ones
```

### 2. Basic Actions with WebDriver

```python
# Navigate to URL
if driver.get_url("https://www.example.com"):
    logger.info(f"Navigated to {driver.current_url}")

    # Scroll the page
    driver.scroll(scrolls=1, direction='down')

    # Wait
    driver.wait(1)

    # Get HTML
    html = driver.fetch_html()
    if html:
        logger.info("HTML obtained.")
else:
    logger.error("Failed to load the page.")

# Close the driver
# driver.quit()
```

### 3. Interacting with Elements (`ExecuteLocator`)

```python
from types import SimpleNamespace

# Define a locator (dictionary or SimpleNamespace)
login_button_locator = {
    "locator_description": "Login button",
    "by": "id",
    "selector": "login-button",
    "event": "click()", # Action - click
    "mandatory": True,
    "timeout": 10
}

input_field_locator = SimpleNamespace(
    locator_description="Name input field",
    by="css selector",
    selector="input[name=\'username\']",
    # event="type(МойЛогин)", # Enter text
    attribute="value", # Or get the 'value' attribute
    mandatory=True,
    "timeout": 5
)

async def perform_actions():
    # Perform a click
    click_success = await driver.execute_locator(login_button_locator)
    if click_success:
        logger.info("Click performed.")

    # Get the attribute value
    input_value = await driver.execute_locator(input_field_locator)
    if input_value is not None:
        logger.info(f"Value of the input field: {input_value}")

    # You can also get WebElement if event and attribute are not specified
    element = await driver.get_webelement_by_locator(input_field_locator)
    if element:
        logger.info(f"Element found: {element.tag_name}")

# Run the asynchronous function
# asyncio.run(perform_actions())

# IMPORTANT: driver.execute_locator and other methods of executor.py are asynchronous!
```

### 4. Using the Data Collection System (`Graber`)

**Scenario 1: Running Automatic Collection Based on Supplier Scenarios**

```python
from src.suppliers.get_graber_by_supplier import get_graber_by_supplier_prefix
# Assuming driver is already initialized

supplier = "ksp" # Supplier prefix
lang_id = 2 # Language ID in PrestaShop

# Get the graber instance for KSP
graber = get_graber_by_supplier_prefix(driver, supplier, lang_index=lang_id)

if graber:
    logger.info(f"Graber for '{supplier}' obtained.")

    async def run_supplier_processing():
        # Run processing of all scenarios from the scenarios/ folder for ksp
        # This function itself will iterate through categories, get product URLs,
        # call grab_page_async for each, and add the product to PrestaShop
        # (according to the logic in graber.py and scenario.py)
        results = await graber.process_supplier_scenarios_async(supplier_prefix=supplier, id_lang=lang_id)
        if results:
            logger.info(f"Scenario processing for '{supplier}' completed. Collected {len(results)} products.")
        else:
            logger.error(f"Error processing scenarios for '{supplier}'.")

    # Run
    asyncio.run(run_supplier_processing())

else:
    logger.error(f"Failed to get the graber for the supplier '{supplier}'.")

```

**Scenario 2: Manually Collecting Data from a Specific Product Page**

```python
from src.suppliers.get_graber_by_supplier import get_graber_by_supplier_url
# Assuming driver is already initialized

product_url = "https://ksp.co.il/web/item/12345" # Example product URL
lang_id = 2

# Get the graber by URL
graber = get_graber_by_supplier_url(driver, product_url, lang_index=lang_id)
# Important: get_graber_by_supplier_url already performs driver.get_url(product_url)

if graber:
    logger.info(f"Graber for URL {product_url} obtained.")

    async def grab_single_product():
        # Define which fields we want to collect
        fields_to_grab = [
            'id_product', 'name', 'price', 'description',
            'specification', 'local_image_path', 'id_supplier'
        ]
        # Call the collection method for the current page
        product_data: ProductFields = await graber.grab_page_async(*fields_to_grab, id_lang=lang_id)

        if product_data:
            logger.success(f"Data for the product collected successfully:")
            # Print or process the collected data
            print(product_data.to_dict()) # Example of printing a dictionary
            # Further actions: save to the database, send to API, etc.
            # For example, add through PrestaProduct
            # from src.endpoints.prestashop.product import PrestaProduct
            # pp = PrestaProduct()
            # pp.add_new_product(product_data)
        else:
            logger.error(f"Failed to collect data from the page {product_url}")

    # Run
    asyncio.run(grab_single_product())

else:
    logger.error(f"No suitable graber found for URL: {product_url}")

# Remember to close the driver after all operations
driver.quit()
```

### 5. Logging

The module uses a configured logger (`src/logger/logger.py`) to output information about the operation process, warnings, and errors. Configure the logging level and format in the logger file.

## Completing Work

Always close the WebDriver after finishing work to release resources:

```python
driver.quit()
```