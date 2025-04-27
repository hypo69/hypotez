# Module: Amazon Supplier Category Page Crawler

## Overview

This module is responsible for collecting product information from category pages of the Amazon supplier. It utilizes a web driver to navigate through the pages and extract relevant data. The module implements a specific scenario for processing Amazon categories, ensuring consistent and reliable data collection.

## Details

This module is designed to interact with Amazon's category pages and retrieve product information, contributing to the overall process of collecting and processing supplier data. 

The module implements the following functionalities:

- **Retrieving the list of categories from the supplier's website:**  `get_list_categories_from_site()` function (not shown in the provided code) is responsible for extracting a list of available categories from the Amazon seller's website.
- **Collecting product URLs from a category page:** `get_list_products_in_category()` function collects a list of product URLs from a given category page, ensuring that all products within the category are captured.
- **Iterating through products and delegating processing:** The module iterates through the list of product URLs and sends each URL to the `grab_product_page()` function. This function handles the retrieval and processing of individual product data, ultimately sending it to the `Product` class for further analysis.

## Functions

### `get_list_products_in_category(d: 'Driver', l: dict) -> list[str, str, None]`

**Purpose**: This function retrieves a list of product URLs from a category page on the Amazon website using the provided web driver (`d`) and locator (`l`).

**Parameters**:

- `d` (`Driver`): An instance of the web driver (Chrome, Firefox, or Playwright).
- `l` (`dict`): A dictionary containing the locator for product links on the category page.

**Returns**:

- `list[str, str, None]`: A list of product URLs, or `None` if no product URLs are found.

**Raises Exceptions**:

- N/A

**How the Function Works**:

- Scrolls the page to ensure that all product links are loaded.
- Uses the `execute_locator()` method of the web driver to find all elements matching the provided locator.
- Collects the href attribute values (product URLs) from the identified elements.
- Logs information about the number of products found.
- Returns the collected list of product URLs.

**Examples**:

```python
# Example usage of get_list_products_in_category
driver = Driver(Chrome)  # Create a driver instance
locator = {  # Define locator for product links
    'by': 'XPATH', 
    'selector': "//a[@class='a-link-normal a-text-normal']" 
}
category_url = "https://www.amazon.com/s?k=books&i=stripbooks&hvadid=241900109007&hvdev=c&hvlocphy=9003703&hvnetw=g&hvqmt=e&hvrand=13497670745158468853&hvtargid=kwd-2249426090&hydadcr=8482_10383262&tag=googhydr-20&ref=pd_sl_6wzk659dtw_e" 

product_urls = get_list_products_in_category(driver, locator, category_url)

if product_urls:
    for url in product_urls:
        print(url)  # Print each product URL found
```

## Class Methods

### `Product`

**Description**: The `Product` class represents a product retrieved from the Amazon website. It contains attributes and methods for handling and processing product data.

**Inherits**: 

**Attributes**:

- `product_id` (str): Unique identifier of the product, typically an Amazon Standard Identification Number (ASIN).
- `name` (str): Name of the product.
- `description` (str): Description of the product.
- `price` (float): Price of the product.
- `category` (str): Category of the product.
- `images` (list[str]): List of URLs for images associated with the product.
- `url` (str): URL of the product page.
- `availability` (str): Availability status of the product.
- `attributes` (dict): Dictionary containing additional product attributes.

**Methods**:

- `get_details()`: This method retrieves and updates product details from the Amazon website, including the name, description, price, category, images, availability, and other relevant attributes.
- `save()`: This method saves the product information to a database or a file.

**Principle of Operation**:

- The `Product` class acts as a container for storing product information.
- It provides methods for retrieving and updating product details from the Amazon website.
- The `save()` method ensures that the collected product data is stored in a persistent manner for future reference.

**Examples**:

```python
product = Product(product_id='B01LXF395G', url='https://www.amazon.com/dp/B01LXF395G')
product.get_details()
print(f'Product Name: {product.name}')
print(f'Product Price: {product.price}')
product.save()  # Save product data to a database or file
```

## Parameter Details

- `d` (`Driver`): An instance of the web driver (Chrome, Firefox, or Playwright). The driver is used for browsing and interacting with Amazon's website.
- `l` (`dict`): A dictionary representing a locator for specific elements on the web page. The locator defines how to find a particular web element using various methods like XPath, CSS Selectors, or tag names. 
- `list_products_in_category` (list): A list containing product URLs found on the Amazon category page.
- `asin` (str): Amazon Standard Identification Number (ASIN). This is a unique identifier for each product on Amazon.
- `_asin` (str): A modified ASIN that includes additional information or formatting for specific purposes.
- `_sku` (str): A unique identifier for a product within the store's database. The `_sku` is typically composed of the supplier's identifier and the ASIN.

## Examples

```python
# Example code snippet using the get_list_products_in_category function
driver = Driver(Chrome)
locator = {
    'by': 'XPATH',
    'selector': "//a[@class='a-link-normal a-text-normal']" 
}
product_urls = get_list_products_in_category(driver, locator)

if product_urls:
    for url in product_urls:
        print(url)  # Print each product URL found

# Example code snippet showing how to use the Product class
product = Product(product_id='B01LXF395G', url='https://www.amazon.com/dp/B01LXF395G')
product.get_details()
print(f'Product Name: {product.name}')
print(f'Product Price: {product.price}')
product.save()  # Save product data to a database or file
```

## Additional Notes

- The code utilizes a web driver to interact with the Amazon website.
- The module implements specific logic for processing Amazon categories.
- The `get_list_categories_from_site()` function (not shown in the provided code) is responsible for retrieving a list of categories from the Amazon seller's website.
- The module uses logging to provide information about the process.
- The code includes comments and docstrings for better understanding and documentation.
- The code example demonstrates how to use the `get_list_products_in_category()` function and the `Product` class.

This module serves as a critical component for extracting product information from Amazon supplier category pages, contributing to the overall data collection and processing pipeline.