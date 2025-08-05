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

## Documentation for the `normalizer` Module
=========================================

The `normalizer` module provides functionality to normalize various data types, including strings, booleans, integers, and floats. It also includes utility functions for text processing.

---

## Contents

1. [Overview](#overview)
2. [Module Functions](#module-functions)
   - [normalize_boolean](#normalize_boolean)
   - [normalize_string](#normalize_string)
   - [normalize_int](#normalize_int)
   - [normalize_float](#normalize_float)
   - [remove_line_breaks](#remove_line_breaks)
   - [remove_html_tags](#remove_html_tags)
   - [remove_special_characters](#remove_special_characters)
   - [normalize_sql_date](#normalize_sql_date)
3. [Usage Example](#usage-example)
4. [Requirements](#requirements)

---

## Overview

The module provides convenient utilities for data normalization and processing. It can be used to:
- Remove HTML tags from strings.
- Convert strings to numeric or boolean values.
- Clean strings from special characters.
- Transform lists of strings into a single normalized string.

---

## Module Functions

### `normalize_boolean`

**Description:**  
Converts the input value to a boolean.

**Arguments:**  
- `input_data (Any)`: Data that might represent a boolean (string, number, boolean).

**Returns:**  
- `bool`: The converted boolean value.

**Example:**  
```python
normalize_boolean('yes')  # Result: True
normalize_boolean(0)      # Result: False
```

---

### `normalize_string`

**Description:**  
Converts a string or a list of strings to a normalized string, removing extra spaces, HTML tags, and special characters.

**Arguments:**  
- `input_data (str | list)`: A string or a list of strings.

**Returns:**  
- `str`: The cleaned string in UTF-8 encoding.

**Example:**  
```python
normalize_string(['  Example string  ', '<b>with HTML</b>'])  # Result: 'Example string with HTML'
```

---

### `normalize_int`

**Description:**  
Converts the input value to an integer.

**Arguments:**  
- `input_data (str | int | float | Decimal)`: A number or its string representation.

**Returns:**  
- `int`: The converted integer.

**Example:**  
```python
normalize_int('42')  # Result: 42
normalize_int(3.14)  # Result: 3
```

---

### `normalize_float`

**Description:**  
Converts the input value to a float.

**Arguments:**  
- `value (Any)`: A number, string, or a list of numbers.

**Returns:**  
- `float | List[float] | None`: A float, a list of floats, or `None` in case of an error.

**Example:**  
```python
normalize_float('3.14')         # Result: 3.14
normalize_float([1, '2.5', 3])  # Result: [1.0, 2.5, 3.0]
```

---

### `remove_line_breaks`

**Description:**  
Removes newline characters from a string.

**Arguments:**  
- `input_str (str)`: The input string.

**Returns:**  
- `str`: The string without newline characters.

**Example:**  
```python
remove_line_breaks('String\\nwith line breaks\\r')  # Result: 'String with line breaks'
```

---

### `remove_html_tags`

**Description:**  
Removes HTML tags from a string.

**Arguments:**  
- `input_html (str)`: The input string containing HTML tags.

**Returns:**  
- `str`: The string without HTML tags.

**Example:**  
```python
remove_html_tags('<p>Example text</p>')  # Result: 'Example text'
```

---

### `remove_special_characters`

**Description:**  
Removes special characters from a string or a list of strings.

**Arguments:**  
- `input_str (str | list)`: A string or a list of strings.

**Returns:**  
- `str | list`: The string or list of strings without special characters.

**Example:**  
```python
remove_special_characters('Hello@World!')  # Result: 'HelloWorld'
```

---

### `normalize_sql_date`

**Description:**  
Converts a string or a `datetime` object to the standard SQL date format (`YYYY-MM-DD`).

**Arguments:**  
- `input_data (str | datetime)`: A string or `datetime` object representing a date.

**Returns:**  
- `str`: The normalized date in the `YYYY-MM-DD` string format.

**Example:**  
```python
normalize_sql_date('2024-12-06')  # Result: '2024-12-06'
normalize_sql_date(datetime(2024, 12, 6))  # Result: '2024-12-06'
```

---

## Usage Example

```python
from src.utils.string.normalizer import normalize_string, normalize_boolean, normalize_int, normalize_float, normalize_sql_date

# Normalize string
clean_str = normalize_string(['<h1>Header</h1>', '  text with spaces  '])
print(clean_str)  # 'Header text with spaces'

# Normalize boolean
is_active = normalize_boolean('Yes')
print(is_active)  # True

# Normalize integer
integer_value = normalize_int('42')
print(integer_value)  # 42

# Normalize float
float_value = normalize_float('3.14159')
print(float_value)  # 3.14159

# Normalize SQL date
sql_date = normalize_sql_date('2024-12-06')
print(sql_date)  # '2024-12-06'
```

---

## Requirements

- Python 3.10 or higher.
- The `src.logger` module for logging.
- The module is used in development mode (``).

---

## Logging

All errors and warnings are logged through `logger`:
- Errors are logged using `logger.error`.
- Unexpected values are logged using `logger.debug` or `logger.warning`.