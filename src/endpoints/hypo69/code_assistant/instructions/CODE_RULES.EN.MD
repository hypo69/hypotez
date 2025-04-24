
### **System Instructions for Processing Code in the `hypotez` Project**

=========================================================================================

Description of functionality and rules for generating, analyzing, and improving code. Aimed at ensuring a consistent and readable coding style that meets requirements.

---

### **Basic Principles**

#### **1. General Guidelines**:
- Adhere to a clear and understandable coding style.
- All changes must be justified and comply with established requirements.

#### **2. Comments**:
- Use `#` for internal comments.
- In comments, avoid using first-person plural verbs like *"we do"*, *"we go"*, *"we return"*, *"we send"*, etc. Instead, use precise impersonal or third-person terms such as *"extraction"*, *"check"*, *"execution"*, *"replacement"*, *"call"*, *"Function performs"*, *"Function changes value"*, *"Function calls"*, *"sending"*.
Example:
```python
# Incorrect:
def function(param: str, param1: Optional[str | dict | str] = None) -> dict | None:
    # We get the parameter value
    ...
# Correct:

def function(param: str, param1: Optional[str | dict | str] = None) -> dict | None:
    # Function extracts the parameter value
    ...
# Incorrect:
if not process_directory.exists():
    logger.error(f"Directory does not exist: {process_directory}")
    continue  # We move to the next directory if the current one does not exist

if not process_directory.is_dir():
    logger.error(f"This is not a directory: {process_directory}", None, False)
    continue  # We move to the next directory if the current one is not a directory
# Correct:

if not process_directory.exists():
    logger.error(f"Directory does not exist: {process_directory}")
    continue  # Proceeding to the next directory if the current one does not exist
if not process_directory.is_dir():
    logger.error(f"This is not a directory: {process_directory}", None, False)
    continue  # Proceeding to the next directory if the current one is not a directory

```
- Documentation for all functions, methods, and classes must follow this format:
    ```python
        def function(param: str, param1: Optional[str | dict | str] = None) -> dict | None:
            """
            Args:
                param (str): Description of the `param` parameter.
                param1 (Optional[str | dict | str], optional): Description of the `param1` parameter. Defaults to `None`.

            Returns:
                dict | None: Description of the return value. Returns a dictionary or `None`.

            Raises:
                SomeError: Description of the situation where the `SomeError` exception is raised.

            Example:
                >>> function('param', 'param1')
                {'param': 'param1'}
            """
    ```
- Comments and documentation must be clear, concise, and accurate.


### **3. File Header**:
Mandatory: Keep the lines
```python
## \file path/to/file
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
```
and
```
"""
...
```rst
 .. module:: src.utils.string.html_simplification
 ```
"""
```
if they exist. If not, add them.
Example:
```python
## \file /src/utils/string/html_simplification.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Module for cleaning HTML tags from text and simplifying HTML code.
===============================================================
The module minimizes HTML code, removes tags and attributes, and also handles
special cases such as scripts, styles, and comments.
Uses BeautifulSoup for reliable HTML parsing.

Dependencies:
    - beautifulsoup4 (pip install beautifulsoup4)
    - lxml (optional, for faster parsing: pip install lxml)

 .. module:: src.utils.string.html_simplification
"""
```

#### **4. Code Formatting**:
- Use single quotes. `a:str = 'value'`, `print('Hello World!')`;
- Add spaces around operators. For example, `x = 5`;
- All parameters must be type-annotated. `def function(param: str, param1: Optional[str | dict | str] = None) -> dict | None:`;
- Do not use `Union`. Use `|` instead.
- Do not use the term `Product`, only `товар`. (Note: This rule specifies using the Russian word 'товар'.)

#### **5. Logging**:
- For logging, always use the `logger` module from `src.logger.logger`.
- Errors must be logged using `logger.error`.
Example:
    ```python
        try:
            ...
        except Exception as ex:
            logger.error('Error while processing data', ex, exc_info=True)
    ```
#### **6. Do not use `Union[]` in the code. Use `|` instead.
For example:
```python
x: str | int ...
```

#### **7. Do not use global variables. If necessary, define them in the `Config` class.**
Example:

- Incorrect:
```python

state:int = 'global'

def func():
    print(state)

```
- Correct:
```python

class Config:
    state:int = 'global'

def func():
    print(Config.state)

```

#### **8. Do not use `self` in class methods. Use `cls` instead.** (Note: Standard Python practice is to use `self` for instance methods and `cls` for class methods. This rule might be project-specific.)
#### **9. Always declare variables at the beginning of the function. Do not declare them in the middle of the function.**
Example:
```python
def func():
    # Incorrect
    if condition:
        x = 5
        y = 10
    else:
        x = 20
        y = 30
    # Correct
    x = None
    y = None
    if condition:
        x = 5
        y = 10
    else:
        x = 20
        y = 30
```
---

### **Main Requirements**:

#### **1. Response Format in Markdown**:
- All responses must be provided in **Markdown** format.

#### **2. Comment Format**:
- Use the specified style for comments and documentation in the code.
- Example:

```python
from typing import Generator, Optional, List
from pathlib import Path


def read_text_file(
    file_path: str | Path,
    as_list: bool = False,
    extensions: Optional[List[str]] = None,
    chunk_size: int = 8192,
) -> Generator[str, None, None] | str | None:
    """
    Reads the content of a file (or files from a directory) using a generator to save memory.

    Args:
        file_path (str | Path): Path to the file or directory.
        as_list (bool): If `True`, returns a generator of strings.
        extensions (Optional[List[str]]): List of file extensions to read from the directory.
        chunk_size (int): Chunk size for reading the file in bytes.

    Returns:
        Generator[str, None, None] | str | None: Generator of strings, a concatenated string, or `None` in case of an error.

    Raises:
        Exception: If an error occurs while reading the file.

    Example:
        >>> from pathlib import Path
        >>> file_path = Path('example.txt')
        >>> content = read_text_file(file_path)
        >>> if content:
        ...    print(f'File content: {content[:100]}...')
        File content: Example text...
    """
    ...
```
- Always provide detailed explanations in comments. Avoid vague terms like *"get"* or *"do"*.
- Instead, use precise terms such as *"extract"*, *"check"*, *"execute"*.
- Instead of: *"we get"*, *"we return"*, *"we transform"*, use the object's name: *"function gets"*, *"variable returns"*, *"code transforms"*.
- Comments must directly precede the code block they describe and explain its purpose.

#### **3. Spaces Around Assignment Operators**:
- Always add spaces around the `=` operator to improve readability.
- Examples:
  - **Incorrect**: `x=5`
  - **Correct**: `x = 5`

#### **4. Using `j_loads` or `j_loads_ns`**:
- For reading JSON or configuration files, replace the standard use of `open` and `json.load` with `j_loads` or `j_loads_ns`.
- Example:

```python
# Incorrect:
with open('config.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Correct:
data = j_loads('config.json')
```

#### **5. Preserving Comments**:
- All existing comments starting with `#` must be preserved without changes in the 'Improved Code' section.
- If a comment seems outdated or unclear, do not modify it. Instead, note it in the 'Changes' section.

#### **6. Handling `...` in Code**:
- Leave `...` as placeholders in the code without changes.
- Do not document lines with `...`.

#### **7. Annotations**
- Type annotations must be defined for all variables.
- For all functions, all input and output parameters must be annotated.
- All parameters must have type annotations.


### **8. webdriver**
The code uses `webdriver`. It is imported from the `webdriver` module of the `hypotez` project.
```python
from src.webdirver import Driver, Chrome, Firefox, Playwright, ...
driver = Driver(Firefox)
```
After which it can be used like:

```python
close_banner = {
  "attribute": null,
  "by": "XPATH",
  "selector": "//button[@id = 'closeXButton']",
  "if_list": "first",
  "use_mouse": false,
  "mandatory": false,
  "timeout": 0,
  "timeout_for_event": "presence_of_element_located",
  "event": "click()",
  "locator_description": "Closing the pop-up window, if it didn't appear - no problem (`mandatory`:`false`)"
}

result = driver.execute_locator(close_banner)
```

#### **9. Do not use `Union[]` in the code. Use `|` instead.**
For example:
```python
x: str | int ...
```

#### **10. `print` is my custom built-in function.**
`from src.utils.printer import pprint as print`


Here it is:
```python
## \file /src/utils/printer.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
.. module::  src.utils
   :platform: Windows, Unix
   :synopsis: Utility functions for pretty printing and text styling.

This module provides functions to print data in a human-readable format with optional text styling, including color, background, and font styles.
"""

import json
import csv
import pandas as pd
from pathlib import Path
from typing import Any
from pprint import pprint as pretty_print

# ANSI escape codes
RESET = "\033[0m"

# Text colors mapping
TEXT_COLORS = {
    "red": "\033[31m",
    "green": "\033[32m",
    "blue": "\033[34m",
    "yellow": "\033[33m",
    "white": "\033[37m",
    "cyan": "\033[36m",
    "magenta": "\033[35m",
    "light_gray": "\033[37m",
    "dark_gray": "\033[90m",
    "light_red": "\033[91m",
    "light_green": "\033[92m",
    "light_blue": "\033[94m",
    "light_yellow": "\033[93m",
}

# Background colors mapping
BG_COLORS = {
    "bg_red": "\033[41m",
    "bg_green": "\033[42m",
    "bg_blue": "\033[44m",
    "bg_yellow": "\033[43m",
    "bg_white": "\033[47m",
    "bg_cyan": "\033[46m",
    "bg_magenta": "\033[45m",
    "bg_light_gray": "\033[47m",
    "bg_dark_gray": "\033[100m",
    "bg_light_red": "\033[101m",
    "bg_light_green": "\033[102m",
    "bg_light_blue": "\033[104m",
    "bg_light_yellow": "\033[103m",
}

# FONT_STYLES
FONT_STYLES = {
    "bold": "\033[1m",
    "underline": "\033[4m",
}

def _color_text(text: str, text_color: str = "", bg_color: str = "", font_style: str = "") -> str:
    """Apply color, background, and font styling to the text.

    This helper function applies the provided color and font styles to the given text using ANSI escape codes.

    :param text: The text to be styled.
    :param text_color: The color to apply to the text. Default is an empty string, meaning no color.
    :param bg_color: The background color to apply. Default is an empty string, meaning no background color.
    :param font_style: The font style to apply to the text. Default is an empty string, meaning no font style.
    :return: The styled text as a string.

    :example:
        >>> _color_text("Hello, World!", text_color="green", font_style="bold")
        '\033[1m\033[32mHello, World!\033[0m'
    """
    return f"{font_style}{text_color}{bg_color}{text}{RESET}"


def pprint(print_data: Any = None, text_color: str = "white", bg_color: str = "", font_style: str = "") -> None:
    """Pretty prints the given data with optional color, background, and font style.

    This function formats the input data based on its type and prints it to the console. The data is printed with optional
    text color, background color, and font style based on the specified parameters. The function can handle dictionaries,
    lists, strings, and file paths.

    :param print_data: The data to be printed. Can be of type ``None``, ``dict``, ``list``, ``str``, or ``Path``.
    :param text_color: The color to apply to the text. Default is 'white'. See ``TEXT_COLORS``.
    :param bg_color: The background color to apply to the text. Default is '' (no background color). See ``BG_COLORS``.
    :param font_style: The font style to apply to the text. Default is '' (no font style). See ``FONT_STYLES``.
    :return: None

    :raises: Exception if the data type is unsupported or an error occurs during printing.

    :example:
        >>> pprint({"name": "Alice", "age": 30}, text_color="green")
        \033[32m{
            "name": "Alice",
            "age": 30
        }\033[0m

        >>> pprint(["apple", "banana", "cherry"], text_color="blue", font_style="bold")
        \033[34m\033[1mapple\033[0m
        \033[34m\033[1mbanana\033[0m
        \033[34m\033[1mcherry\033[0m

        >>> pprint("text example", text_color="yellow", bg_color="bg_red", font_style="underline")
        \033[4m\033[33m\033[41mtext example\033[0m
    """
    if not print_data:
        return
    if isinstance(text_color, str):
        text_color = TEXT_COLORS.get(text_color.lower(), TEXT_COLORS["white"])
    if isinstance(bg_color, str):
        bg_color = BG_COLORS.get(bg_color.lower(), "")
    if isinstance(font_style, str):
        font_style = FONT_STYLES.get(font_style.lower(), "")


    try:
        if isinstance(print_data, dict):
            print(_color_text(json.dumps(print_data, indent=4), text_color))
        elif isinstance(print_data, list):
            for item in print_data:
                print(_color_text(str(item), text_color))
        elif isinstance(print_data, (str, Path)) and Path(print_data).is_file():
            ext = Path(print_data).suffix.lower()
            if ext in ['.csv', '.xls']:
                print(_color_text("File reading supported for .csv, .xls only.", text_color))
            else:
                print(_color_text("Unsupported file type.", text_color))
        else:
            print(_color_text(str(print_data), text_color))
    except Exception as ex:
        print(_color_text(f"Error: {ex}", text_color=TEXT_COLORS["red"]))
# IGNORE_WHEN_COPYING_START - These lines are typically instructions for internal tools
# content_copy
# download
# Use code with caution.
# IGNORE_WHEN_COPYING_END

if __name__ == '__main__':
    pprint({"name": "Alice", "age": 30}, text_color="green")
