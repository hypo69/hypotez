# Module for Validating Strings
## Overview

This module provides functions for validating strings against specific criteria or formats. Validation may involve checking for the presence of certain characters, string length, email format, URL, etc.

## Details

The module defines a class called `ProductFieldsValidator` which provides methods for validating various fields related to products. It uses regular expressions and other string manipulation techniques to ensure that the input strings meet the specified requirements.

## Classes

### `ProductFieldsValidator`

**Description**: This class provides methods for validating product-related strings.

**Methods**:

- `validate_price(price: str) -> bool`: Validates if the given price is a valid number. 
- `validate_weight(weight: str) -> bool`: Validates if the given weight is a valid number.
- `validate_sku(sku: str) -> bool`: Validates if the given SKU (stock keeping unit) is valid.
- `validate_url(url: str) -> bool`: Validates if the given URL is valid.
- `isint(s: str) -> bool`: Checks if the given string can be converted to an integer.


## Functions

### `validate_price(price: str) -> bool`

**Purpose**: Validates if the given price is a valid number.

**Parameters**:

- `price` (str): The price string to be validated.

**Returns**:

- `bool`: Returns `True` if the price is valid, `False` otherwise.

**How the Function Works**:

- The function first checks if the `price` is empty. If it is, the function returns `None`.
- Then it removes any non-numeric characters from the price string using a regular expression.
- Finally, it tries to convert the price string to a float. If the conversion is successful, it returns `True`, otherwise it returns `None`.

**Examples**:

- `validate_price('10.99')` returns `True`
- `validate_price('10,99')` returns `True`
- `validate_price('10.99 USD')` returns `True`
- `validate_price('abc')` returns `None`


### `validate_weight(weight: str) -> bool`

**Purpose**: Validates if the given weight is a valid number.

**Parameters**:

- `weight` (str): The weight string to be validated.

**Returns**:

- `bool`: Returns `True` if the weight is valid, `False` otherwise.

**How the Function Works**:

- The function first checks if the `weight` is empty. If it is, the function returns `None`.
- Then it removes any non-numeric characters from the weight string using a regular expression.
- Finally, it tries to convert the weight string to a float. If the conversion is successful, it returns `True`, otherwise it returns `None`.

**Examples**:

- `validate_weight('10.5')` returns `True`
- `validate_weight('10,5')` returns `True`
- `validate_weight('10.5 kg')` returns `True`
- `validate_weight('abc')` returns `None`


### `validate_sku(sku: str) -> bool`

**Purpose**: Validates if the given SKU (stock keeping unit) is valid.

**Parameters**:

- `sku` (str): The SKU string to be validated.

**Returns**:

- `bool`: Returns `True` if the SKU is valid, `False` otherwise.

**How the Function Works**:

- The function first checks if the `sku` is empty. If it is, the function returns `None`.
- Then it removes any special characters and line breaks from the SKU string.
- Finally, it checks if the length of the SKU string is at least 3 characters. If it is, it returns `True`, otherwise it returns `None`.

**Examples**:

- `validate_sku('SKU123')` returns `True`
- `validate_sku('SKU-123')` returns `True`
- `validate_sku('SKU1234567890')` returns `True`
- `validate_sku('SKU')` returns `None`
- `validate_sku('')` returns `None`


### `validate_url(url: str) -> bool`

**Purpose**: Validates if the given URL is valid.

**Parameters**:

- `url` (str): The URL string to be validated.

**Returns**:

- `bool`: Returns `True` if the URL is valid, `False` otherwise.

**How the Function Works**:

- The function first checks if the `url` is empty. If it is, the function returns `None`.
- Then it trims any leading or trailing whitespace from the `url`.
- If the `url` doesn't start with "http", it adds "http://" to the beginning of the `url`.
- Finally, it parses the `url` using `urllib.parse.urlparse` and checks if the netloc and scheme components are not empty. If they are not empty, it returns `True`, otherwise it returns `None`.

**Examples**:

- `validate_url('https://www.google.com')` returns `True`
- `validate_url('google.com')` returns `True`
- `validate_url('www.google.com')` returns `True`
- `validate_url('http://www.google.com/')` returns `True`
- `validate_url('')` returns `None`
- `validate_url('abc')` returns `None`


### `isint(s: str) -> bool`

**Purpose**: Checks if the given string can be converted to an integer.

**Parameters**:

- `s` (str): The string to be checked.

**Returns**:

- `bool`: Returns `True` if the string can be converted to an integer, `False` otherwise.

**How the Function Works**:

- The function tries to convert the string `s` to an integer using `int(s)`.
- If the conversion is successful, it returns `True`.
- If the conversion fails, it catches the `Exception` and returns `False`.

**Examples**:

- `isint('123')` returns `True`
- `isint('12.3')` returns `False`
- `isint('abc')` returns `False`


## Parameter Details

- `price` (str): Represents the price of a product, which should be a valid number.
- `weight` (str): Represents the weight of a product, which should be a valid number.
- `sku` (str): Represents the stock keeping unit of a product, which should be a valid string with a minimum length of 3 characters.
- `url` (str): Represents a web address (URL), which should be a valid URL according to the standard format.
- `s` (str): Represents a string that needs to be checked for its convertibility to an integer.


## Examples

```python
from src.utils.string.validator import ProductFieldsValidator

# Validating a price
price = '10.99'
is_valid_price = ProductFieldsValidator.validate_price(price)
print(f'Price "{price}" is valid: {is_valid_price}') # Output: Price "10.99" is valid: True

# Validating a weight
weight = '10.5 kg'
is_valid_weight = ProductFieldsValidator.validate_weight(weight)
print(f'Weight "{weight}" is valid: {is_valid_weight}') # Output: Weight "10.5 kg" is valid: True

# Validating a SKU
sku = 'SKU12345'
is_valid_sku = ProductFieldsValidator.validate_sku(sku)
print(f'SKU "{sku}" is valid: {is_valid_sku}') # Output: SKU "SKU12345" is valid: True

# Validating a URL
url = 'https://www.google.com'
is_valid_url = ProductFieldsValidator.validate_url(url)
print(f'URL "{url}" is valid: {is_valid_url}') # Output: URL "https://www.google.com" is valid: True

# Checking if a string is an integer
s = '123'
is_int = ProductFieldsValidator.isint(s)
print(f'String "{s}" is an integer: {is_int}') # Output: String "123" is an integer: True

# Checking if a string is not an integer
s = '12.3'
is_int = ProductFieldsValidator.isint(s)
print(f'String "{s}" is an integer: {is_int}') # Output: String "12.3" is an integer: False
```