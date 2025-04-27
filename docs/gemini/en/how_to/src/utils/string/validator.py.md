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

## \file /src/utils/string/validator.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
String Validator
===============

This module provides functions to validate strings against specific criteria or formats.
Validation may include checking for specific characters, string length, email format, URL, etc.

.. module:: src.utils.string.validator 

"""
...

import re, html
from urllib.parse import urlparse, parse_qs
from typing import Union
from urllib.parse import urlparse, parse_qs

from src.logger.logger import logger

class ProductFieldsValidator:
    """
    ProductFieldsValidator:
    @details 
    - Purpose: Validates string fields related to product data.
    - Actions: Performs various checks, such as validating price, weight, SKU, and URLs. 
    - Usage Example: Ensures the integrity and consistency of product information by validating individual fields.
    """

    @staticmethod
    def validate_price(price: str) -> bool:
        """
        Validates a price string.

        Args:
            price (str): The price string to be validated.

        Returns:
            bool: True if the price is valid, False otherwise.

        Example:
            >>> ProductFieldsValidator.validate_price('12.99')
            True
            >>> ProductFieldsValidator.validate_price('12,99')
            True
            >>> ProductFieldsValidator.validate_price('12.99a')
            False
        """
        """
        Price validation
        """
        if not price:
            return False
        price = Ptrn.clear_price.sub('', price)
        price = price.replace(',', '.')
        try:
            float(price)
        except:
            return False
        return True


    @staticmethod
    def validate_weight(weight: str) -> bool:
        """
        Validates a weight string.

        Args:
            weight (str): The weight string to be validated.

        Returns:
            bool: True if the weight is valid, False otherwise.

        Example:
            >>> ProductFieldsValidator.validate_weight('1.5 kg')
            True
            >>> ProductFieldsValidator.validate_weight('1,5 kg')
            True
            >>> ProductFieldsValidator.validate_weight('1.5 kg a')
            False
        """
        """
        Weight validation
        """
        if not weight:
            return False
        weight = Ptrn.clear_number.sub('', weight)
        weight = weight.replace(',', '.')
        try:
            float(weight)
        except:
            return False
        return True


    @staticmethod
    def validate_sku(sku: str) -> bool:
        """
        Validates a SKU (Stock Keeping Unit) string.

        Args:
            sku (str): The SKU string to be validated.

        Returns:
            bool: True if the SKU is valid, False otherwise.

        Example:
            >>> ProductFieldsValidator.validate_sku('ABC123')
            True
            >>> ProductFieldsValidator.validate_sku('ABC1234567890')
            True
            >>> ProductFieldsValidator.validate_sku('ABC 123')
            True
            >>> ProductFieldsValidator.validate_sku('ABC')
            False
        """
        """
        SKU validation
        """
        if not sku:
            return False
        sku = StringFormatter.remove_special_characters(sku)
        sku = StringFormatter.remove_line_breaks(sku)
        sku = sku.strip()
        if len(sku) < 3:
            return False
        return True


    @staticmethod
    def validate_url(url: str) -> bool:
        """
        Validates a URL string.

        Args:
            url (str): The URL string to be validated.

        Returns:
            bool: True if the URL is valid, False otherwise.

        Example:
            >>> ProductFieldsValidator.validate_url('https://www.example.com')
            True
            >>> ProductFieldsValidator.validate_url('www.example.com')
            True
            >>> ProductFieldsValidator.validate_url('example.com')
            True
            >>> ProductFieldsValidator.validate_url('http://example.com')
            True
            >>> ProductFieldsValidator.validate_url('http://')
            False
            >>> ProductFieldsValidator.validate_url('example.com/')
            True
        """
        """
        URL validation
        """
        if not url:
            return False

        url = url.strip()

        if not url.startswith('http'):
            url = 'http://' + url

        parsed_url = urlparse(url)

        if not parsed_url.netloc or not parsed_url.scheme:
            return False

        return True

    @staticmethod
    def isint(s: str) -> bool:
        """
        Checks if a string can be converted to an integer.

        Args:
            s (str): The string to be checked.

        Returns:
            bool: True if the string can be converted to an integer, False otherwise.

        Example:
            >>> ProductFieldsValidator.isint('123')
            True
            >>> ProductFieldsValidator.isint('123.45')
            False
            >>> ProductFieldsValidator.isint('abc')
            False
        """
        try:
            s = int(s)
            return True
        except Exception as ex:
            return False