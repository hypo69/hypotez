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


## \file /src/utils/string/normalizer.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Module for normalizing strings and numeric data
=========================================================================================

The module provides functions for normalizing strings, booleans, integers, and floating-point numbers. 
It also includes helper methods for text processing, including removing HTML tags and special characters.

Example Usage
--------------------
```python

    from src.utils.string.normalizer import normalize_string, normalize_boolean

    normalized_str = normalize_string(" Пример строки <b>с HTML</b> ")
    normalized_bool = normalize_boolean("yes")
```
.. module:: src.utils.string.normalizer
"""

import re
import html
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Any, List, Optional
from src.logger.logger import logger



def normalize_boolean(input_data: Any) -> bool:
    """Normalizes data into a boolean.

    Args:
        input_data (Any): Data that can represent a boolean (e.g., bool, string, integer).

    Returns:
        bool: Boolean representation of the input.

    Example:
        >>> normalize_boolean('yes')
        True
    """
    original_input = input_data  # Saves the original value
    if isinstance(input_data, bool):
        return input_data

    try:
        input_str = str(input_data).strip().lower()
        if input_str in {'true', '1', 'yes', 'y', 'on', True, 1}:
            return True
        if input_str in {'false', '0', 'no', 'n', 'off', False, 0}:
            return False
    except Exception as ex:
        logger.error('Error in normalize_boolean: ', ex)

    logger.debug(f'Unexpected value for boolean conversion: {input_data}')
    return original_input  # Returns the original value


def normalize_string(input_data: str | list) -> str:
    """Normalizes a string or a list of strings.

    Args:
        input_data (str | list): Input data that can be either a string or a list of strings.

    Returns:
        str: Cleaned and normalized string in UTF-8 encoded format.

    Example:
        >>> normalize_string(['Hello', '  World!  '])
        'Hello World!'

    Raises:
        TypeError: If `input_data` is not of type `str` or `list`.
    """
    if not input_data:
        return ''

    original_input = input_data  # Saves the original value. In case of parsing errors, this value will be returned.

    if not isinstance(input_data, (str, list)):
        raise TypeError('Data must be a string or a list of strings.')

    if isinstance(input_data, list):
        input_data = ' '.join(map(str, input_data))

    try:
        cleaned_str = remove_html_tags(input_data)
        cleaned_str = remove_line_breaks(cleaned_str)
        cleaned_str = remove_special_characters(cleaned_str)
        normalized_str = ' '.join(cleaned_str.split())

        return normalized_str.strip().encode('utf-8').decode('utf-8')
    except Exception as ex:
        logger.error('Error in normalize_string: ', ex)
        return str(original_input).encode('utf-8').decode('utf-8')


def normalize_int(input_data: str | int | float | Decimal) -> int:
    """Normalizes data into an integer.

    Args:
        input_data (str | int | float | Decimal): Input data that can be a number or its string representation.

    Returns:
        int: Integer representation of the input.

    Example:
        >>> normalize_int('42')
        42
    """
    original_input = input_data  # Saves the original value
    try:
        if isinstance(input_data, Decimal):
            return int(input_data)
        return int(float(input_data))
    except (ValueError, TypeError, InvalidOperation) as ex:
        logger.error('Error in normalize_int: ', ex)
        return original_input  # Returns the original value



def normalize_float(value: Any) -> Optional[float]:
    """
    Safely converts the input value to float or returns None,
    if the conversion failed. Removes common currency symbols
    and thousand separators before conversion.

    Args:
        value (Any): Input value (int, float, str, etc.).

    Returns:
        Optional[float]: Float number or None if conversion failed.

    Examples:
        >>> normalize_float(5)
        5.0
        >>> normalize_float("5")
        5.0
        >>> normalize_float("3.14")
        3.14
        >>> normalize_float("abc")
        None
        >>> normalize_float("₪0.00")
        0.0
        >>> normalize_float("$1,234.56")
        1234.56
        >>> normalize_float("  - 7.5 € ")
        -7.5
        >>> normalize_float(None)
        None
        >>> normalize_float(['1'])
        None
        >>> normalize_float('')
        None

    Important! Check after calling this function that it did not return None
    """
    if value is None:
        return None

    # If it's already a number, just convert to float
    if isinstance(value, (int, float)):
        return float(value)

    # If it's a list/tuple - error
    if isinstance(value, (list, tuple)):
        logger.warning(f'Expected a single value, received an iterable object: {value}')
        return None

    # Attempt to convert the value to a string for cleaning
    try:
        value_str = str(value)
    except Exception as e:
        logger.warning(f'Unable to convert value to string: {value} ({type(value)}). Error: {e}')
        return None

    # Cleaning the string from known non-numeric characters
    # 1. Remove common currency symbols (can be extended list)
    cleaned_str: str = re.sub(r'[₪$€£¥₽]', '', value_str)
    # 2. Remove thousand separators (commas)
    cleaned_str = cleaned_str.replace(',', '')
    # 3. Remove leading/trailing spaces
    cleaned_str = cleaned_str.strip()

    # If the string is empty after cleaning
    if not cleaned_str:
        logger.warning(f'The value became empty after cleaning: "{value}" -> "{cleaned_str}"')
        return None

    # Attempt to convert the cleaned string
    try:
        # Use float() for conversion
        float_value = float(cleaned_str)
        # Rounding to 3 digits is no longer required by the code, we return as is
        return float_value
    except (ValueError, TypeError):
        logger.warning(f'Failed to convert the cleaned string "{cleaned_str}" (from "{value}") to float')
        return None



def normalize_sql_date(input_data: str) -> str:
    """Normalizes data into SQL date format (YYYY-MM-DD).

    Args:
        input_data (str): Data that can represent a date (e.g., string, datetime object).

    Returns:
        str: Normalized date in SQL format (YYYY-MM-DD) or original value if conversion fails.

    Example:
        >>> normalize_sql_date('2024-12-06')
        '2024-12-06'
        >>> normalize_sql_date('12/06/2024')
        '2024-12-06'
    """
    original_input = input_data  # Saves the original value

    try:
        # Checking and converting the string to a date format
        if isinstance(input_data, str):
            # Attempt to parse the date from the string
            for date_format in ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y']:
                try:
                    normalized_date = datetime.strptime(input_data, date_format).date()
                    return normalized_date.isoformat()  # Returns the date in 'YYYY-MM-DD' format
                except ValueError:
                    continue
        # If the input data is already a datetime object
        if isinstance(input_data, datetime):
            return input_data.date().isoformat()

    except Exception as ex:
        logger.error('Error in normalize_sql_date: ', ex)

    logger.debug(f'Failed to convert to SQL date: {input_data}')
    return original_input  # Returns the original value
def simplify_string(input_str: str) -> str:
    """ Simplifies the input string by keeping only letters, digits, and replacing spaces with underscores.

    @param input_str: The string to be simplified.
    @return: The simplified string.
    @code
        example_str = "It's a test string with 'single quotes', numbers 123 and symbols!"
        simplified_str = StringNormalizer.simplify_string(example_str)
        print(simplified_str)  # Output: Its_a_test_string_with_single_quotes_numbers_123_and_symbols
    @endcode
    """
    try:
        # Remove all characters except letters, digits, and spaces
        cleaned_str = re.sub(r'[^a-zA-Z0-9\s]', '', input_str)
        # Replace spaces with underscores
        cleaned_str = cleaned_str.replace(' ', '_')
        # Remove consecutive underscores
        cleaned_str = re.sub(r'_+', '_', cleaned_str)
        return cleaned_str
    except Exception as ex:
        logger.error("Error simplifying the string", ex)
        return input_str

def remove_line_breaks(input_str: str) -> str:
    """Removes line breaks from the input string.

    Args:
        input_str (str): Input string.

    Returns:
        str: String without line breaks.
    """
    return input_str.replace('\n', ' ').replace('\r', ' ').strip()


def remove_html_tags(input_html: str) -> str:
    """Removes HTML tags from the input string.

    Args:
        input_html (str): Input HTML string.

    Returns:
        str: String without HTML tags.
    """
    return re.sub(r'<.*?>', '', input_html).strip()



def remove_special_characters(input_str: str | list, chars: list[str] = None) -> str | list:
    """Removes specified special characters from a string or list of strings.

    Args:
        input_str (str | list): Input string or list of strings.
        chars (list[str], optional): List of characters to remove. Defaults to None.

    Returns:
        str | list: Processed string or list with specified characters removed.
    """
    if chars is None:
        chars = ['#']  # Default list of characters to remove

    pattern = '[' + re.escape(''.join(chars)) + ']'

    if isinstance(input_str, list):
        return [re.sub(pattern, '', s) for s in input_str]
    return re.sub(pattern, '', input_str)

def normalize_sku(input_str: str) -> str:
    """
    Normalizes the SKU by removing specific Hebrew keywords and any non-alphanumeric characters, 
    except for hyphens.

    Args:
        input_str (str): The input string containing the SKU.

    Returns:
        str: The normalized SKU string.

    Example:
        >>> normalize_sku("מקט: 303235-A")
        '303235-A'
        >>> normalize_sku("מק\'\'ט: 12345-B")
        '12345-B'
        >>> normalize_sku("Some text מקט: 123-456-789 other text")
        'Some text 123-456-789 other text' # Important: It now keeps the hyphens and spaces between texts
    """
    try:
        # Remove Hebrew keywords
        _str = re.sub(r'מקט|מק\'\'ט', '', input_str, flags=re.IGNORECASE)

        # Remove non-alphanumeric characters, except for hyphens
        normalized_sku = re.sub(r'[^\\w-]+\', \'\', _str)

        return normalized_sku
    except Exception as ex:
        logger.error(f"Error normalizing SKU: ", exc_info=True)  # Include exception details
        return input_str