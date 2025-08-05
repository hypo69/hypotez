# Module: src.suppliers.kualastyle.via_webdriver

## Overview

This module contains functions for parsing product information from the Kualastyle website using Selenium WebDriver.

## Details

This module provides functionalities for retrieving product information from the Kualastyle website, specifically targeting product URLs within a given category. The code utilizes Selenium WebDriver to navigate and interact with the website, extracting relevant data. 

## Functions

### `get_list_products_in_category`

**Purpose**:  This function retrieves a list of product URLs from a specific category page on the Kualastyle website.

**Parameters**:
- `s` (Supplier):  An instance of the `Supplier` class representing the Kualastyle supplier.

**Returns**:
- `list[str, str, None]`: Returns a list of product URLs, where each item is a tuple containing the product URL, product name, and potentially None.

**Raises Exceptions**:
- None

**How the Function Works**:

1.  The function retrieves the Selenium WebDriver instance (`d`) from the `Supplier` object (`s`).
2.  It accesses the locator dictionary (`l`) for the "category" section, which contains the specific locators to identify product links.
3.  The WebDriver scrolls the page (using `d.scroll`) to ensure all product links are loaded within the viewport.
4.  It executes the `product_links` locator (using `d.execute_locator`) to retrieve a list of product URLs.

**Examples**:

```python
# Assuming 's' is a Supplier object representing Kualastyle
product_urls = get_list_products_in_category(s)
if product_urls:
    for url, name, _ in product_urls:
        print(f"Product URL: {url}")
        print(f"Product Name: {name}")
```

## Parameter Details

- `s` (Supplier): An instance of the `Supplier` class, providing access to the Selenium WebDriver and locators used for web scraping.
- `l` (dict): A dictionary containing locators for identifying specific web elements on the Kualastyle website.
- `d` (Driver): An instance of the `Driver` class (a wrapper for Selenium WebDriver) used for interacting with the website.

## Examples

```python
from src.suppliers.kualastyle.via_webdriver import get_list_products_in_category

# Assuming 's' is a Supplier object representing Kualastyle
product_urls = get_list_products_in_category(s)
if product_urls:
    for url, name, _ in product_urls:
        print(f"Product URL: {url}")
        print(f"Product Name: {name}")
```
```python