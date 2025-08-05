# Module: `src.goog.spreadsheet.bberyakov.helpers`

## Overview

This module provides utility functions for converting color formats, specifically:

- Hexadecimal to decimal
- Decimal to hexadecimal
- Hexadecimal to RGB

## Details

This module is designed to facilitate the conversion of color representations between different formats, which are often used in spreadsheets and other applications. It offers functions for transforming hexadecimal color codes, decimal representations, and RGB color values.

## Functions

### `hex_color_to_decimal(letters: str) -> int`

**Purpose**: Converts a hexadecimal color code (e.g., "A" or "AA") to its decimal equivalent.

**Parameters**:
- `letters` (str): The hexadecimal color code to convert. 

**Returns**:
- `int`: The decimal equivalent of the hexadecimal color code.

**Example**:

```python
>>> print(hex_color_to_decimal("A"))  # Output: 1
>>> print(hex_color_to_decimal("AA"))  # Output: 27
```

**How the Function Works**:

This function uses a helper function `letter_to_number` to translate individual hexadecimal characters into decimal values. For single-letter hexadecimal codes, it directly converts the letter to its decimal equivalent. For two-letter hexadecimal codes, it multiplies the decimal value of the first letter by 26 and adds the decimal value of the second letter.

**Inner Functions**:

- `letter_to_number(letter: str) -> int`:

    **Purpose**: Converts a single hexadecimal character to its decimal equivalent.

    **Parameters**:
    - `letter` (str): The hexadecimal character to convert.

    **Returns**:
    - `int`: The decimal equivalent of the hexadecimal character.

    **How the Function Works**:

    This function uses the `ord()` function to get the Unicode code point of the input character and then adjusts it based on the starting Unicode code point of lowercase letters (97). It then returns the adjusted code point as a string.

### `decimal_color_to_hex(number: int) -> str`

**Purpose**: Converts a decimal number to its hexadecimal color code representation.

**Parameters**:
- `number` (int): The decimal number to convert.

**Returns**:
- `str`: The hexadecimal color code equivalent of the decimal number.

**Example**:

```python
>>> print(decimal_color_to_hex(1))  # Output: 'A'
>>> print(decimal_color_to_hex(27))  # Output: 'AA'
```

**How the Function Works**:

This function uses the `divmod()` function to calculate the quotient and remainder when dividing the decimal number (minus 1) by 26. If the number is less than or equal to 26, it directly converts the number to its corresponding hexadecimal character using the `chr()` function. If the number is greater than 26, it recursively calls the `decimal_color_to_hex()` function with the quotient and concatenates the result with the character corresponding to the remainder.

### `hex_to_rgb(hex: str) -> tuple`

**Purpose**: Converts a hexadecimal color code to its RGB (Red, Green, Blue) color representation.

**Parameters**:
- `hex` (str): The hexadecimal color code to convert.

**Returns**:
- `tuple`: A tuple containing three integers representing the red, green, and blue components of the RGB color.

**Example**:

```python
>>> print(hex_to_rgb("#FFFFFF"))  # Output: (255, 255, 255)
>>> print(hex_to_rgb("FFFFFF"))  # Output: (255, 255, 255)
```

**How the Function Works**:

This function first removes the '#' symbol from the hexadecimal color code if present. It then extracts the red, green, and blue components by slicing the hexadecimal string into two-character chunks and converts each chunk to an integer using the `int()` function with base 16. It then returns these integer values as a tuple.