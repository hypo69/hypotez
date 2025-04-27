# Module for String and Numeric Data Normalization

## Overview

This module provides functions for normalizing strings, boolean values, integers, and floating-point numbers. It also includes helper methods for text processing, including removing HTML tags and special characters.

## Details

This module is part of the `hypotez` project, where it plays a crucial role in ensuring data consistency and uniformity. It is used throughout the project to clean and prepare data for various tasks, such as:

- **Database interaction**: Ensuring that data stored in databases conforms to expected formats and data types.
- **Text processing**: Removing unwanted characters and formatting inconsistencies before performing text analysis or NLP tasks.
- **Data validation**: Verifying that user inputs or external data sources adhere to predefined formats and rules.

## Classes

### `None` 

This module does not contain any classes.

## Functions

### `normalize_boolean`

**Purpose**: Convert any data type into a boolean value, handling various representations of truthiness.

**Parameters**:

- `input_data (Any)`: The input data that can be a boolean, string, integer, or other type that can represent a boolean value.

**Returns**:

- `bool`: The normalized boolean value.

**Raises Exceptions**:

- `None`

**Examples**:

```python
>>> normalize_boolean('yes')
True
>>> normalize_boolean(True)
True
>>> normalize_boolean(1)
True
>>> normalize_boolean('false')
False
>>> normalize_boolean(False)
False
>>> normalize_boolean(0)
False
>>> normalize_boolean('invalid')
'invalid'  # Returns the original input if conversion fails
```

**How the Function Works**:

1. The function first checks if the input is already a boolean. If so, it returns the input directly.
2. Then, it tries to convert the input data into a string and converts it to lowercase.
3. It compares the string against a predefined set of values representing true (e.g., "true", "1", "yes") and false (e.g., "false", "0", "no").
4. If a match is found, the function returns the corresponding boolean value.
5. If the input data cannot be converted to a string or does not match any of the predefined values, the function returns the original input data.

### `normalize_string`

**Purpose**: Clean and normalize a string or a list of strings, removing unwanted characters and formatting inconsistencies.

**Parameters**:

- `input_data (str | list)`: The input data that can be either a string or a list of strings.

**Returns**:

- `str`: The normalized and cleaned string in UTF-8 encoded format.

**Raises Exceptions**:

- `TypeError`: If `input_data` is not of type `str` or `list`.

**Examples**:

```python
>>> normalize_string('Hello, World!')
'Hello World!'
>>> normalize_string(['Hello', '  World!  '])
'Hello World!'
>>> normalize_string('   This  is  a    test   string  ')
'This is a test string'
```

**How the Function Works**:

1. The function first checks if the input data is empty. If so, it returns an empty string.
2. It then checks if the input data is a list. If it is, it joins the list elements into a single string separated by spaces.
3. The function then calls three helper functions:
    - `remove_html_tags`: Removes HTML tags from the string.
    - `remove_line_breaks`: Removes line breaks from the string.
    - `remove_special_characters`: Removes specified special characters from the string.
4. Finally, it strips leading and trailing spaces from the cleaned string and converts it to UTF-8 encoding.

### `normalize_int`

**Purpose**: Convert any data type into an integer value, handling various representations of integers.

**Parameters**:

- `input_data (str | int | float | Decimal)`: The input data that can be a number or its string representation.

**Returns**:

- `int`: The integer representation of the input.

**Raises Exceptions**:

- `None`

**Examples**:

```python
>>> normalize_int('42')
42
>>> normalize_int(42)
42
>>> normalize_int(42.5)
42
>>> normalize_int('42.5')
42
```

**How the Function Works**:

1. The function first checks if the input data is already an integer. If so, it returns the input directly.
2. Then, it tries to convert the input data into a float and then into an integer.
3. If the conversion fails, the function returns the original input data.

### `normalize_float`

**Purpose**: Safely convert any data type into a floating-point number.

**Parameters**:

- `value (Any)`: The input value that can be an integer, float, string, or other data type.

**Returns**:

- `Optional[float]`: The float representation of the input, or `None` if conversion fails.

**Raises Exceptions**:

- `None`

**Examples**:

```python
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
```

**How the Function Works**:

1. The function first checks if the input value is `None`. If so, it returns `None`.
2. It then checks if the input value is already a number (integer or float). If so, it converts it to a float and returns it.
3. If the input value is a list or tuple, it logs a warning and returns `None`.
4. The function then tries to convert the input value to a string. If this fails, it logs a warning and returns `None`.
5. The function then cleans the string by removing known non-numeric characters, including currency symbols and thousands separators.
6. If the cleaned string is empty, it logs a warning and returns `None`.
7. Finally, it tries to convert the cleaned string to a float. If this fails, it logs a warning and returns `None`.

### `normalize_sql_date`

**Purpose**: Convert any data type into a SQL date format (YYYY-MM-DD).

**Parameters**:

- `input_data (str)`: The input data that can be a string or a datetime object representing a date.

**Returns**:

- `str`: The normalized date in SQL format (YYYY-MM-DD), or the original input if conversion fails.

**Raises Exceptions**:

- `None`

**Examples**:

```python
>>> normalize_sql_date('2024-12-06')
'2024-12-06'
>>> normalize_sql_date('12/06/2024')
'2024-12-06'
>>> normalize_sql_date(datetime(2024, 12, 6))
'2024-12-06'
```

**How the Function Works**:

1. The function first checks if the input data is already a string. If so, it tries to parse the date from the string using different date formats (YYYY-MM-DD, MM/DD/YYYY, DD/MM/YYYY). If parsing is successful, it returns the normalized date in SQL format.
2. If the input data is a datetime object, it returns the date component in SQL format.
3. If conversion fails, the function returns the original input data.

### `simplify_string`

**Purpose**: Simplify an input string by removing special characters and replacing spaces with underscores.

**Parameters**:

- `input_str (str)`: The input string to be simplified.

**Returns**:

- `str`: The simplified string.

**Raises Exceptions**:

- `None`

**Examples**:

```python
>>> simplify_string("It's a test string with 'single quotes', numbers 123 and symbols!")
'Its_a_test_string_with_single_quotes_numbers_123_and_symbols'
```

**How the Function Works**:

1. The function first removes all characters except letters, digits, and spaces.
2. It then replaces spaces with underscores.
3. Finally, it removes consecutive underscores.

### `remove_line_breaks`

**Purpose**: Remove line breaks from an input string.

**Parameters**:

- `input_str (str)`: The input string.

**Returns**:

- `str`: The string without line breaks.

**Raises Exceptions**:

- `None`

**Examples**:

```python
>>> remove_line_breaks('This is a string\nwith line breaks.\rAnd some more.')
'This is a string with line breaks. And some more.'
```

**How the Function Works**:

1. The function replaces all newline characters (`\n`) with spaces.
2. It then replaces all carriage return characters (`\r`) with spaces.
3. Finally, it strips leading and trailing spaces from the string.

### `remove_html_tags`

**Purpose**: Remove HTML tags from an input string.

**Parameters**:

- `input_html (str)`: The input HTML string.

**Returns**:

- `str`: The string without HTML tags.

**Raises Exceptions**:

- `None`

**Examples**:

```python
>>> remove_html_tags('<p>This is a string with <b>HTML tags</b>.</p>')
'This is a string with HTML tags.'
```

**How the Function Works**:

1. The function uses a regular expression to match all HTML tags (including opening and closing tags) and replaces them with empty strings.
2. Finally, it strips leading and trailing spaces from the string.

### `remove_special_characters`

**Purpose**: Remove specified special characters from a string or list of strings.

**Parameters**:

- `input_str (str | list)`: The input string or list of strings.
- `chars (list[str], optional)`: The list of characters to remove. Defaults to `None`.

**Returns**:

- `str | list`: The processed string or list with specified characters removed.

**Raises Exceptions**:

- `None`

**Examples**:

```python
>>> remove_special_characters('This is a string with #special characters.')
'This is a string with special characters.'
>>> remove_special_characters(['This is a string with #special characters.', 'Another string with $special characters.'], chars=['#', '$'])
['This is a string with special characters.', 'Another string with special characters.']
```

**How the Function Works**:

1. The function first defines a default list of characters to remove (`['#']`) if no `chars` argument is provided.
2. It then creates a regular expression pattern that matches any of the specified characters.
3. If the input is a list, the function iterates through each string in the list and applies the pattern to remove the specified characters.
4. If the input is a string, the function applies the pattern to remove the specified characters from the string.

### `normalize_sku`

**Purpose**: Normalize the SKU by removing Hebrew keywords and non-alphanumeric characters, except for hyphens.

**Parameters**:

- `input_str (str)`: The input string containing the SKU.

**Returns**:

- `str`: The normalized SKU string.

**Raises Exceptions**:

- `None`

**Examples**:

```python
>>> normalize_sku("מקט: 303235-A")
'303235-A'
>>> normalize_sku("מק\'\'ט: 12345-B")
'12345-B'
>>> normalize_sku("Some text מקט: 123-456-789 other text")
'Some text 123-456-789 other text'
```

**How the Function Works**:

1. The function first removes Hebrew keywords like "מקט" and "מק\'\'ט" (case-insensitive) from the input string.
2. Then, it removes all non-alphanumeric characters except for hyphens (`-`).
3. Finally, it returns the normalized SKU string.

## Parameter Details

- `input_data (Any)`: Input data that can be a boolean, string, integer, or other data type representing a boolean value.
- `input_data (str | list)`: Input data that can be either a string or a list of strings.
- `input_data (str | int | float | Decimal)`: Input data that can be a number or its string representation.
- `value (Any)`: Input value that can be an integer, float, string, or other data type.
- `input_data (str)`: Input data that can be a string or a datetime object representing a date.
- `input_str (str)`: The input string to be simplified or processed.
- `input_html (str)`: The input HTML string.
- `input_str (str | list)`: The input string or list of strings.
- `chars (list[str], optional)`: The list of characters to remove. Defaults to `None`.
- `input_str (str)`: The input string containing the SKU.

## Examples

```python
# Examples of using normalize_boolean:
>>> normalize_boolean('yes')
True
>>> normalize_boolean(True)
True
>>> normalize_boolean(1)
True
>>> normalize_boolean('false')
False
>>> normalize_boolean(False)
False
>>> normalize_boolean(0)
False
>>> normalize_boolean('invalid')
'invalid'

# Examples of using normalize_string:
>>> normalize_string('Hello, World!')
'Hello World!'
>>> normalize_string(['Hello', '  World!  '])
'Hello World!'
>>> normalize_string('   This  is  a    test   string  ')
'This is a test string'

# Examples of using normalize_int:
>>> normalize_int('42')
42
>>> normalize_int(42)
42
>>> normalize_int(42.5)
42
>>> normalize_int('42.5')
42

# Examples of using normalize_float:
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

# Examples of using normalize_sql_date:
>>> normalize_sql_date('2024-12-06')
'2024-12-06'
>>> normalize_sql_date('12/06/2024')
'2024-12-06'
>>> normalize_sql_date(datetime(2024, 12, 6))
'2024-12-06'

# Examples of using simplify_string:
>>> simplify_string("It's a test string with 'single quotes', numbers 123 and symbols!")
'Its_a_test_string_with_single_quotes_numbers_123_and_symbols'

# Examples of using remove_line_breaks:
>>> remove_line_breaks('This is a string\nwith line breaks.\rAnd some more.')
'This is a string with line breaks. And some more.'

# Examples of using remove_html_tags:
>>> remove_html_tags('<p>This is a string with <b>HTML tags</b>.</p>')
'This is a string with HTML tags.'

# Examples of using remove_special_characters:
>>> remove_special_characters('This is a string with #special characters.')
'This is a string with special characters.'
>>> remove_special_characters(['This is a string with #special characters.', 'Another string with $special characters.'], chars=['#', '$'])
['This is a string with special characters.', 'Another string with special characters.']

# Examples of using normalize_sku:
>>> normalize_sku("מקט: 303235-A")
'303235-A'
>>> normalize_sku("מק\'\'ט: 12345-B")
'12345-B'
>>> normalize_sku("Some text מקט: 123-456-789 other text")
'Some text 123-456-789 other text'
```