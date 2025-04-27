# Gearbest Data Graber

## Overview

This module provides functionality for collecting product data from the `gearbest.com` website. It inherits from the base class `src.suppliers.graber.Graber` and implements specific logic for handling product fields on the Gearbest website. 

## Details

The `Graber` class offers methods for processing various product fields on the product page. You can override these methods for customized field handling if needed.

The `Graber` class extends the base class `src.suppliers.graber.Graber`, which provides default methods for processing common product fields. If you need to modify how a specific field is handled, you can override the method in the `Graber` class.

**Decorator Usage:** 

Before sending a request to the web driver, you can execute preliminary actions using a decorator. This decorator, by default, is found in the parent class. To activate it, pass a value in `Context.locator`. If you want to implement your own decorator, uncomment the lines with the decorator and redefine its behavior. You can also implement your own decorator by uncommenting the relevant code lines.

## Classes

### `Graber`

**Description**: This class handles the process of retrieving product data from the Gearbest website.

**Inherits**:  `src.suppliers.graber.Graber`

**Attributes**:

- `supplier_prefix: str`: Specifies the prefix for the supplier.

**Methods**:

#### `__init__(self, driver: Optional['Driver'] = None, lang_index:Optional[int] = None)`

**Purpose**: Initializes the `Graber` instance with the necessary parameters.

**Parameters**:

- `driver (Optional['Driver'])`: An optional web driver instance for interacting with the browser.
- `lang_index (Optional[int])`: An optional index for the language.

**Returns**:

- `None`

**Raises**:

- `None`

**How the Function Works**:

1. Sets the `supplier_prefix` attribute to "etzmaleh".
2. Calls the parent class's `__init__` method to initialize the base Graber class, passing the supplier prefix, driver instance, and language index.
3. Sets the `Config.locator_for_decorator` to `None`. This will trigger the `@close_pop_up` decorator if a value is set.

#### `get_product_url_suffix(self, product_id: str) -> str`:
**Purpose**: Generates the URL suffix for a specific product based on the product ID.

**Parameters**:

- `product_id (str)`: The ID of the product.

**Returns**:

- `str`: The URL suffix for the product.


#### `get_product_id(self, product_url: str) -> str | None`:
**Purpose**: Extracts the product ID from a product URL.

**Parameters**:

- `product_url (str)`: The URL of the product.

**Returns**:

- `str | None`: The product ID extracted from the URL, or `None` if the ID cannot be found.


#### `get_product_title(self, response: SimpleNamespace) -> str`:
**Purpose**: Extracts the title of the product from the HTML response.

**Parameters**:

- `response (SimpleNamespace)`: The HTML response object.

**Returns**:

- `str`: The title of the product.

#### `get_product_image_url(self, response: SimpleNamespace) -> str`:
**Purpose**: Extracts the URL of the product image from the HTML response.

**Parameters**:

- `response (SimpleNamespace)`: The HTML response object.

**Returns**:

- `str`: The URL of the product image.

#### `get_product_price(self, response: SimpleNamespace) -> str`:
**Purpose**: Extracts the price of the product from the HTML response.

**Parameters**:

- `response (SimpleNamespace)`: The HTML response object.

**Returns**:

- `str`: The price of the product.

#### `get_product_price_currency(self, response: SimpleNamespace) -> str`:
**Purpose**: Extracts the currency of the product price from the HTML response.

**Parameters**:

- `response (SimpleNamespace)`: The HTML response object.

**Returns**:

- `str`: The currency of the product price.

#### `get_product_main_category(self, response: SimpleNamespace) -> str`:
**Purpose**: Extracts the main category of the product from the HTML response.

**Parameters**:

- `response (SimpleNamespace)`: The HTML response object.

**Returns**:

- `str`: The main category of the product.

#### `get_product_sub_category(self, response: SimpleNamespace) -> str`:
**Purpose**: Extracts the subcategory of the product from the HTML response.

**Parameters**:

- `response (SimpleNamespace)`: The HTML response object.

**Returns**:

- `str`: The subcategory of the product.

#### `get_product_availability(self, response: SimpleNamespace) -> str`:
**Purpose**: Extracts the availability status of the product from the HTML response.

**Parameters**:

- `response (SimpleNamespace)`: The HTML response object.

**Returns**:

- `str`: The availability status of the product.

#### `get_product_description(self, response: SimpleNamespace) -> str`:
**Purpose**: Extracts the description of the product from the HTML response.

**Parameters**:

- `response (SimpleNamespace)`: The HTML response object.

**Returns**:

- `str`: The description of the product.

#### `get_product_specification(self, response: SimpleNamespace) -> str`:
**Purpose**: Extracts the specifications of the product from the HTML response.

**Parameters**:

- `response (SimpleNamespace)`: The HTML response object.

**Returns**:

- `str`: The specifications of the product.

#### `get_product_reviews_count(self, response: SimpleNamespace) -> str`:
**Purpose**: Extracts the number of reviews for the product from the HTML response.

**Parameters**:

- `response (SimpleNamespace)`: The HTML response object.

**Returns**:

- `str`: The number of reviews for the product.

#### `get_product_rating(self, response: SimpleNamespace) -> str`:
**Purpose**: Extracts the rating of the product from the HTML response.

**Parameters**:

- `response (SimpleNamespace)`: The HTML response object.

**Returns**:

- `str`: The rating of the product.

#### `get_product_shipping_price(self, response: SimpleNamespace) -> str`:
**Purpose**: Extracts the shipping price for the product from the HTML response.

**Parameters**:

- `response (SimpleNamespace)`: The HTML response object.

**Returns**:

- `str`: The shipping price for the product.

#### `get_product_additional_info(self, response: SimpleNamespace) -> dict`:
**Purpose**: Extracts additional product information from the HTML response.

**Parameters**:

- `response (SimpleNamespace)`: The HTML response object.

**Returns**:

- `dict`: A dictionary containing additional product information.

#### `get_product_additional_info_by_locator(self, response: SimpleNamespace) -> str`:
**Purpose**: Extracts additional product information based on a provided locator.

**Parameters**:

- `response (SimpleNamespace)`: The HTML response object.

**Returns**:

- `str`: The extracted product information.

#### `get_product_all_fields(self, response: SimpleNamespace) -> dict`:
**Purpose**: Collects all product fields from the HTML response and returns them in a dictionary.

**Parameters**:

- `response (SimpleNamespace)`: The HTML response object.

**Returns**:

- `dict`: A dictionary containing all collected product fields.

## Functions

### `get_product_url_suffix(product_id: str) -> str`:

**Purpose**: Constructs the URL suffix for a product on Gearbest based on the given product ID.

**Parameters**:

- `product_id (str)`: The ID of the product.

**Returns**:

- `str`: The URL suffix for the product on Gearbest.

**How the Function Works**:

- The function directly concatenates the product ID with a fixed path string to create the URL suffix.

**Examples**:

```python
>>> get_product_url_suffix('123456789')
'/123456789.html'
```

### `get_product_id(product_url: str) -> str | None`:

**Purpose**: Extracts the product ID from a given product URL on Gearbest.

**Parameters**:

- `product_url (str)`: The URL of the product on Gearbest.

**Returns**:

- `str | None`: The extracted product ID, or `None` if the ID cannot be found.

**How the Function Works**:

- The function uses string manipulation techniques to isolate the product ID portion of the URL.

**Examples**:

```python
>>> get_product_id('https://www.gearbest.com/cell-phones/pp_123456789.html')
'123456789'

>>> get_product_id('https://www.gearbest.com/cell-phones/pp_123456789.html')
'123456789'
```

### `get_product_title(response: SimpleNamespace) -> str`:

**Purpose**: Extracts the product title from the HTML response of a Gearbest product page.

**Parameters**:

- `response (SimpleNamespace)`: The HTML response object, likely containing the product page content.

**Returns**:

- `str`: The title of the product.

**How the Function Works**:

- The function uses the web driver's methods to locate the product title element on the page and retrieves its text content.

**Examples**:

```python
>>> get_product_title(response)  # Assuming 'response' contains HTML content
'Gearbest Product Title'
```

### `get_product_image_url(response: SimpleNamespace) -> str`:

**Purpose**: Retrieves the URL of the primary product image from the HTML response of a Gearbest product page.

**Parameters**:

- `response (SimpleNamespace)`: The HTML response object containing the product page content.

**Returns**:

- `str`: The URL of the product image.

**How the Function Works**:

- The function uses the web driver's methods to locate the product image element on the page and extracts its 'src' attribute, which usually holds the image URL.

**Examples**:

```python
>>> get_product_image_url(response)  # Assuming 'response' contains HTML content
'https://www.gearbest.com/images/products/123456789/main.jpg'
```

### `get_product_price(response: SimpleNamespace) -> str`:

**Purpose**: Extracts the price of the product from the HTML response of a Gearbest product page.

**Parameters**:

- `response (SimpleNamespace)`: The HTML response object containing the product page content.

**Returns**:

- `str`: The price of the product.

**How the Function Works**:

- The function uses the web driver's methods to locate the price element on the page and retrieves its text content, typically representing the product price.

**Examples**:

```python
>>> get_product_price(response)  # Assuming 'response' contains HTML content
'$199.99'
```

### `get_product_price_currency(response: SimpleNamespace) -> str`:

**Purpose**: Extracts the currency of the product price from the HTML response of a Gearbest product page.

**Parameters**:

- `response (SimpleNamespace)`: The HTML response object containing the product page content.

**Returns**:

- `str`: The currency symbol of the product price.

**How the Function Works**:

- The function uses the web driver's methods to locate the price element on the page and analyzes its text content to identify the currency symbol.

**Examples**:

```python
>>> get_product_price_currency(response)  # Assuming 'response' contains HTML content
'$'
```

### `get_product_main_category(response: SimpleNamespace) -> str`:

**Purpose**: Extracts the main category of the product from the HTML response of a Gearbest product page.

**Parameters**:

- `response (SimpleNamespace)`: The HTML response object containing the product page content.

**Returns**:

- `str`: The main category of the product.

**How the Function Works**:

- The function uses the web driver's methods to locate the category element on the page and retrieves its text content.

**Examples**:

```python
>>> get_product_main_category(response)  # Assuming 'response' contains HTML content
'Cell Phones & Telecommunications'
```

### `get_product_sub_category(response: SimpleNamespace) -> str`:

**Purpose**: Extracts the sub-category of the product from the HTML response of a Gearbest product page.

**Parameters**:

- `response (SimpleNamespace)`: The HTML response object containing the product page content.

**Returns**:

- `str`: The sub-category of the product.

**How the Function Works**:

- The function uses the web driver's methods to locate the sub-category element on the page and retrieves its text content.

**Examples**:

```python
>>> get_product_sub_category(response)  # Assuming 'response' contains HTML content
'Smartphones'
```

### `get_product_availability(response: SimpleNamespace) -> str`:

**Purpose**: Extracts the availability status of the product from the HTML response of a Gearbest product page.

**Parameters**:

- `response (SimpleNamespace)`: The HTML response object containing the product page content.

**Returns**:

- `str`: The availability status of the product.

**How the Function Works**:

- The function uses the web driver's methods to locate the availability element on the page and retrieves its text content.

**Examples**:

```python
>>> get_product_availability(response)  # Assuming 'response' contains HTML content
'In Stock'
```

### `get_product_description(response: SimpleNamespace) -> str`:

**Purpose**: Extracts the description of the product from the HTML response of a Gearbest product page.

**Parameters**:

- `response (SimpleNamespace)`: The HTML response object containing the product page content.

**Returns**:

- `str`: The description of the product.

**How the Function Works**:

- The function uses the web driver's methods to locate the description element on the page and retrieves its text content.

**Examples**:

```python
>>> get_product_description(response)  # Assuming 'response' contains HTML content
'This is the Gearbest product description.'
```

### `get_product_specification(response: SimpleNamespace) -> str`:

**Purpose**: Extracts the specifications of the product from the HTML response of a Gearbest product page.

**Parameters**:

- `response (SimpleNamespace)`: The HTML response object containing the product page content.

**Returns**:

- `str`: The specifications of the product.

**How the Function Works**:

- The function uses the web driver's methods to locate the specifications element on the page and retrieves its text content.

**Examples**:

```python
>>> get_product_specification(response)  # Assuming 'response' contains HTML content
'Specifications:\n- Brand: Apple\n- Model: iPhone 14 Pro\n-...'
```

### `get_product_reviews_count(response: SimpleNamespace) -> str`:

**Purpose**: Extracts the number of reviews for the product from the HTML response of a Gearbest product page.

**Parameters**:

- `response (SimpleNamespace)`: The HTML response object containing the product page content.

**Returns**:

- `str`: The number of reviews for the product.

**How the Function Works**:

- The function uses the web driver's methods to locate the reviews count element on the page and retrieves its text content.

**Examples**:

```python
>>> get_product_reviews_count(response)  # Assuming 'response' contains HTML content
'100 Reviews'
```

### `get_product_rating(response: SimpleNamespace) -> str`:

**Purpose**: Extracts the rating of the product from the HTML response of a Gearbest product page.

**Parameters**:

- `response (SimpleNamespace)`: The HTML response object containing the product page content.

**Returns**:

- `str`: The rating of the product.

**How the Function Works**:

- The function uses the web driver's methods to locate the rating element on the page and retrieves its text content.

**Examples**:

```python
>>> get_product_rating(response)  # Assuming 'response' contains HTML content
'4.5 Stars'
```

### `get_product_shipping_price(response: SimpleNamespace) -> str`:

**Purpose**: Extracts the shipping price for the product from the HTML response of a Gearbest product page.

**Parameters**:

- `response (SimpleNamespace)`: The HTML response object containing the product page content.

**Returns**:

- `str`: The shipping price for the product.

**How the Function Works**:

- The function uses the web driver's methods to locate the shipping price element on the page and retrieves its text content.

**Examples**:

```python
>>> get_product_shipping_price(response)  # Assuming 'response' contains HTML content
'$5.99'
```

### `get_product_additional_info(response: SimpleNamespace) -> dict`:

**Purpose**: Extracts additional product information from the HTML response of a Gearbest product page, returning it as a dictionary.

**Parameters**:

- `response (SimpleNamespace)`: The HTML response object containing the product page content.

**Returns**:

- `dict`: A dictionary containing additional product information, where keys are the names of the information and values are the corresponding data.

**How the Function Works**:

- The function uses the web driver's methods to locate specific elements on the page that contain additional product information. 
- It then extracts the text content from those elements and stores it in a dictionary with appropriate keys.

**Examples**:

```python
>>> get_product_additional_info(response)  # Assuming 'response' contains HTML content
{'Brand': 'Apple', 'Model': 'iPhone 14 Pro', 'Color': 'Space Black', 'Storage': '256GB'}
```

### `get_product_additional_info_by_locator(response: SimpleNamespace) -> str`:

**Purpose**: Extracts additional product information from the HTML response based on a provided locator.

**Parameters**:

- `response (SimpleNamespace)`: The HTML response object containing the product page content.

**Returns**:

- `str`: The extracted product information, potentially containing text, attributes, or other data from the located element.

**How the Function Works**:

- The function uses the provided locator (which specifies the method of finding the element, such as XPath or CSS selector) to locate a specific element on the page.
- It then extracts the data from the located element, which could be the text content, an attribute value, or other information based on the locator's purpose.

**Examples**:

```python
>>> get_product_additional_info_by_locator(response)  # Assuming 'response' contains HTML content
'256GB'
```

### `get_product_all_fields(response: SimpleNamespace) -> dict`:

**Purpose**:  Collects all product fields from the HTML response of a Gearbest product page and organizes them into a dictionary.

**Parameters**:

- `response (SimpleNamespace)`: The HTML response object containing the product page content.

**Returns**:

- `dict`: A comprehensive dictionary containing all extracted product fields.

**How the Function Works**:

- The function uses the web driver's methods to locate elements on the page that contain information about various product fields, such as the title, price, description, specifications, reviews, ratings, and other details. 
- It then extracts the text content from these elements and stores them in a dictionary with appropriate keys.
- It also utilizes the previously defined functions, such as `get_product_title`, `get_product_price`, `get_product_description`, etc., to retrieve specific fields from the response.

**Examples**:

```python
>>> get_product_all_fields(response)  # Assuming 'response' contains HTML content
{
'product_id': '123456789',
'product_url': 'https://www.gearbest.com/cell-phones/pp_123456789.html',
'product_title': 'Gearbest Product Title',
'product_image_url': 'https://www.gearbest.com/images/products/123456789/main.jpg',
'product_price': '$199.99',
'product_price_currency': '$',
'product_main_category': 'Cell Phones & Telecommunications',
'product_sub_category': 'Smartphones',
'product_availability': 'In Stock',
'product_description': 'This is the Gearbest product description.',
'product_specification': 'Specifications:\n- Brand: Apple\n- Model: iPhone 14 Pro\n-...',
'product_reviews_count': '100 Reviews',
'product_rating': '4.5 Stars',
'product_shipping_price': '$5.99',
'product_additional_info': {'Brand': 'Apple', 'Model': 'iPhone 14 Pro', 'Color': 'Space Black', 'Storage': '256GB'}
}
```

## Parameter Details

- `driver (Optional['Driver'])`: An instance of the `Driver` class from `src.webdriver.driver`. It's used to control the web browser and interact with the Gearbest website.
- `lang_index (Optional[int])`: An index representing the language. If specified, it indicates the language in which the product data should be retrieved.
- `product_id (str)`: The unique identifier for the product on Gearbest.
- `product_url (str)`: The complete URL of the product page on Gearbest.
- `response (SimpleNamespace)`: A Python object representing the HTML content of the product page.
- `locator (dict)`: A dictionary defining the locator to use when finding elements on the product page. For example, a locator may specify an XPath or CSS selector.

## Examples

```python
# Example 1: Retrieving product information from a URL.
from src.suppliers.suppliers_list.gearbest.graber import Graber
from src.webdriver.driver import Driver
from src.webdriver.driver import Chrome

driver = Driver(Chrome)
graber = Graber(driver=driver)
product_url = 'https://www.gearbest.com/cell-phones/pp_123456789.html'
product_data = graber.get_product_all_fields(product_url)
print(product_data)

# Example 2: Getting all product fields.
from src.suppliers.suppliers_list.gearbest.graber import get_product_all_fields
from src.webdriver.driver import Driver
from src.webdriver.driver import Chrome
from src.suppliers.graber import Config
from src.logger.logger import logger

# Assuming `response` is an object containing the HTML response of the product page.
driver = Driver(Chrome)
graber = Graber(driver=driver)
product_data = graber.get_product_all_fields(response)
print(product_data)