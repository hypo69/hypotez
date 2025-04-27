# Bangood Scenario Module

## Overview

This module is responsible for collecting product data from category pages on the Bangood.co.il website using a web driver. Each supplier has its own scenario for handling categories. This module uses a specific process for Bangood.

## Details

The module performs the following actions:

- **Collects a list of categories from supplier pages**: `get_list_categories_from_site()`.
- **Collects a list of products from a category page**: `get_list_products_in_category()`.
- **Iterates through the product list and calls `grab_product_page()` to process individual product pages**: `grab_product_page()` processes product fields and passes control to the `Product` class.

This module is designed to work in conjunction with the `Supplier` class.

## Functions

### `get_list_products_in_category(s)`

**Purpose**: Retrieves a list of product URLs from a given category page.

**Parameters**:

- `s` (Supplier): An instance of the `Supplier` class representing the supplier for which the category page is being processed.

**Returns**:

- `list[str, str, None] | None`: A list of product URLs, or `None` if no URLs are found or an error occurs.

**Raises Exceptions**:

- `None`.

**How the Function Works**:

1. The function first checks if the category page contains a banner and closes it if found.
2. The function then retrieves a list of product URLs from the category page using the `execute_locator()` method of the `Driver` object, accessing the appropriate locators from the `s.locators` dictionary.
3. If product URLs are not found, a warning message is logged.
4. The function returns the list of product URLs.

### `get_list_categories_from_site(s)`

**Purpose**: Retrieves a list of categories from the supplier's website.

**Parameters**:

- `s` (Supplier): An instance of the `Supplier` class representing the supplier for which the category pages are being processed.

**Returns**:

- `list[str, str, None] | None`: A list of category URLs, or `None` if no URLs are found or an error occurs.

**Raises Exceptions**:

- `None`.

**How the Function Works**:

1. The function retrieves a list of category URLs from the supplier's website using the `execute_locator()` method of the `Driver` object, accessing the appropriate locators from the `s.locators` dictionary.
2. The function returns the list of category URLs.

## Examples

```python
# Example of using get_list_products_in_category()
from src.suppliers.suppliers_list.bangood import scenario
from src.suppliers.suppliers_list.bangood.bangood_supplier import BangoodSupplier

# Assuming 'supplier' is an instance of BangoodSupplier
supplier = BangoodSupplier(...)

product_urls = scenario.get_list_products_in_category(supplier)

if product_urls:
    print(f'Found {len(product_urls)} product URLs.')
    for url in product_urls:
        print(url)
else:
    print('No product URLs found.')
```

```python
# Example of using get_list_categories_from_site()
from src.suppliers.suppliers_list.bangood import scenario
from src.suppliers.suppliers_list.bangood.bangood_supplier import BangoodSupplier

# Assuming 'supplier' is an instance of BangoodSupplier
supplier = BangoodSupplier(...)

category_urls = scenario.get_list_categories_from_site(supplier)

if category_urls:
    print(f'Found {len(category_urls)} category URLs.')
    for url in category_urls:
        print(url)
else:
    print('No category URLs found.')
```

## Parameter Details

- **`s` (Supplier)**: An instance of the `Supplier` class representing the supplier for which the category pages are being processed. This object contains information about the supplier, including locators for web elements on the supplier's website. The `Supplier` class is defined in the `bangood_supplier.py` file.

## How the Module Works

This module is responsible for gathering data from Bangood category pages. The `get_list_products_in_category()` function retrieves a list of product URLs from a single category page. The `get_list_categories_from_site()` function retrieves a list of all category pages for the Bangood supplier.

The module relies on the `Supplier` class to provide information about the supplier and its website structure. The `Driver` class handles the web browser interaction, using Selenium to navigate the website and retrieve data.

## Improvements

- **Implement pagination for category pages**: The current implementation assumes that all products on a category page can be retrieved on a single page. It should handle pagination scenarios for category pages with multiple pages of products.
- **Add error handling**:  The current implementation lacks robust error handling for scenarios such as network errors, invalid URLs, or unexpected website changes. Add error handling to prevent the program from crashing in these situations.
- **Improve logging**: Increase the level of detail in logging messages for debugging and monitoring purposes.
- **Optimize performance**: Investigate potential optimizations for the code to improve its performance, especially when handling a large number of categories and products.

This module demonstrates a basic approach to collecting data from supplier websites. By implementing the improvements suggested, the module can be made more robust, reliable, and performant.