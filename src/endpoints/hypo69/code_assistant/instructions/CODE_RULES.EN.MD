Okay, here is the English translation of the provided instructions, preserving the Markdown formatting and structure.

```markdown
### **System Instructions for Processing Code in the `hypotez` Project**

=========================================================================================

Description of functionality and rules for generating, analyzing, and improving code. Aimed at ensuring a consistent and readable coding style that meets requirements.

---

### **Main Principles**

#### **1. General Guidelines**:
- Adhere to a clear and understandable coding style.
- All changes must be justified and comply with established requirements.

#### **2. Comments**:
- Use `#` for inline comments.
- In comments, avoid using pronouns like *"we do"*, *"we switch"*, *"we return"*, *"we send"*, etc. Instead, use precise terms like *"extraction"*, *"check"*, *"execution"*, *"replacement"*, *"call"*, *"function performs"*, *"function modifies value"*, *"function calls"*, *"sending"*.
Example:
```python
# Incorrect:
def function(param: str, param1: Optional[str | dict | str] = None) -> dict | None:
    # Getting the parameter value
    ...
# Correct:

def function(param: str, param1: Optional[str | dict | str] = None) -> dict | None:
    # The function extracts the parameter value
    ...
# Incorrect:
if not process_directory.exists():
    logger.error(f"Directory does not exist: {process_directory}")
    continue  # Switching to the next directory if the current one does not exist

if not process_directory.is_dir():
    logger.error(f"This is not a directory: {process_directory}", None, False)
    continue  # Switching to the next directory if the current one is not a directory
# Correct:

if not process_directory.exists():
    logger.error(f"Directory does not exist: {process_directory}")
    continue  # Transition to the next directory if the current one does not exist
if not process_directory.is_dir():
    logger.error(f"This is not a directory: {process_directory}", None, False)
    continue  # Transition to the next directory if the current one is not a directory

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
Mandatorily keep the lines
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
 .. module:: src.<module>.<module name>
 ```
"""
```
if they exist. If not, add them.
Example:
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

 ```rst
 .. module:: src.utils.string.html_simplification
 ```
"""

#### **4. Code Formatting**:
- Use single quotes. `a:str = 'value'`, `print('Hello World!')`;
- Add spaces around operators. For example, `x = 5`;
- All parameters must be type-annotated. `def function(param: str, param1: Optional[str | dict | str] = None) -> dict | None:`;
- Do not use `Union`. Use `|` instead.
- Do not use the term `Product`, only `товар`.

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
#### **6. Do not use `Union[]` in the code. Use `|` instead.**
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
from typing import Generator, Optional, List, Union # Note: Union used here despite rule 6/9, translating as provided.
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
        Generator[str, None, None] | str | None: Generator of strings, a concatenated string, or `None` in case of error.

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
- Always provide detailed explanations in comments. Avoid vague terms,
- such as *"get"* or *"do"*
- . Instead, use precise terms like *"extract"*, *"check"*, *"execute"*.
- Instead of: *"we get"*, *"we return"*, *"we transform"*, use the object name: *"function gets"*, *"variable returns"*, *"code transforms"*.
- Comments must immediately precede the code block they describe and explain its purpose.

#### **3. Spaces around assignment operators**:
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
Here is the code for `j_loads` and `j_loads_ns`:
```python
import json
from pathlib import Path
from types import SimpleNamespace
from typing import Union, Dict, List, Any # Note: Union used here despite rule 6/9, translating as provided.
# Assuming logger and dict2ns are defined elsewhere
# from src.logger.logger import logger
# from src.utils.dicts.dict_tools import dict2ns

def j_loads(
    jjson: Union[dict, SimpleNamespace, str, Path, list], ordered: bool = True
) -> Union[dict, list]:
    """
    Load JSON or CSV data from a file, directory, string, or object.

    Args:
        jjson (dict | SimpleNamespace | str | Path | list): Path to file/directory, JSON string, or JSON object.
        ordered (bool, optional): Use OrderedDict to preserve element order. Defaults to True. # Note: OrderedDict is not used in the provided code.

    Returns:
        dict | list: Processed data (dictionary or list of dictionaries).

    Raises:
        FileNotFoundError: If the specified file is not found.
        json.JSONDecodeError: If the JSON data cannot be parsed.
    """
    # Assuming _string_to_dict and _decode_strings are defined elsewhere
    # Assuming logger is available
    try:
        if isinstance(jjson, SimpleNamespace):
            jjson = vars(jjson)

        if isinstance(jjson, Path):
            if jjson.is_dir():
                files = list(jjson.glob("*.json"))
                return [j_loads(file, ordered=ordered) for file in files]
            # Uncomment if pandas is used and intended
            # if jjson.suffix.lower() == ".csv":
            #     import pandas as pd # Needs import
            #     return pd.read_csv(jjson).to_dict(orient="records")

            return json.loads(jjson.read_text(encoding="utf-8")) # `ordered` parameter has no effect here
        if isinstance(jjson, str):
            # return _string_to_dict(jjson) # Assuming this function exists
            return json.loads(jjson) # Standard way if it's a JSON string
        if isinstance(jjson, list):
             # return _decode_strings(jjson) # Assuming this function exists
             return jjson # Or handle list elements if needed
        if isinstance(jjson, dict):
            # return _decode_strings(jjson) # Assuming this function exists
            return jjson # Or handle dict elements if needed
    except FileNotFoundError:
        # logger.error(f"File not found: {jjson}",None,False)
        print(f"Error: File not found: {jjson}") # Placeholder if logger is not available
        return {}
    except json.JSONDecodeError as ex:
        # logger.error(f"JSON parsing error:\n{jjson}\n", ex, False)
        print(f"Error: JSON parsing error in {jjson}: {ex}") # Placeholder
        return {}
    except Exception as ex:
        # logger.error(f"Error loading data: ", ex, False)
        print(f"Error: Error loading data from {jjson}: {ex}") # Placeholder
        return {}
    return {}


def j_loads_ns(
    jjson: Union[Path, SimpleNamespace, Dict, str], ordered: bool = True
) -> Union[SimpleNamespace, List[SimpleNamespace], Dict]:
    """Load JSON/CSV data and convert to SimpleNamespace."""
    # Assuming dict2ns is available
    data = j_loads(jjson, ordered=ordered)
    if data:
        if isinstance(data, list):
            # return [dict2ns(item) for item in data]
            return [SimpleNamespace(**item) for item in data if isinstance(item, dict)] # Standard way
        if isinstance(data, dict):
            # return dict2ns(data)
            return SimpleNamespace(**data) # Standard way
    return {} # Return empty dict as per original code's potential return type
```

#### **5. Preserving Comments**:
- All existing comments starting with `#` must be preserved without modification in the 'Improved Code' section.
- If a comment seems outdated or unclear, do not modify it. Instead, note it in the 'Changes' section.

#### **6. Handling `...` in code**:
- Leave `...` as placeholders in the code without modification.
- Do not document lines containing `...`.

#### **7. Annotations**
- Type annotations must be defined for all variables.
- For all functions, all input and output parameters must be type-annotated.
- All parameters must have type annotations.


### **8. webdriver**
- The code uses webdriver. It is imported from the `webdriver` module of the `hypotez` project.
```python
from src.webdriver import Driver, Chrome, Firefox, Playwright # Assuming these exist
# Example Usage:
driver = Driver(Firefox) # Assuming Driver takes a browser class
```
- After which it can be used like:

```python
close_banner = {
  "attribute": None,
  "by": "XPATH", # Standard Selenium locator strategy
  "selector": "//button[@id = 'closeXButton']",
  "if_list": "first", # Custom handling instruction?
  "use_mouse": False, # Custom flag?
  "mandatory": False, # Custom flag?
  "timeout": 0, # Custom timeout? Standard is usually > 0
  "timeout_for_event": "presence_of_element_located", # Standard Selenium expected condition
  "event": "click()", # Action to perform
  "locator_description": "Closing the pop-up window, if it didn't appear - no problem (`mandatory`:`false`)" # Description for logging/debugging
}

# Assuming driver has an execute_locator method
result = driver.execute_locator(close_banner)
```

#### **9. Do not use `Union[]` in the code. Use `|` instead.**
For example:
```python
x: str | int ...
```

#### **10. `print` is my custom built-in function.**
```python
from src.utils.printer import pprint as print
```

Here it is:
```python
from typing import Any # Added Any for print_data

# Define ANSI escape codes (assuming standard codes)
RESET = "\033[0m"
# Example colors/styles (add more as needed)
COLORS = {
    "white": "\033[97m",
    "green": "\033[92m",
    # Add other colors
}
BACKGROUNDS = {
    # Add background colors if needed, e.g., "black_bg": "\033[40m"
    "": "" # Default no background
}
STYLES = {
    # Add styles if needed, e.g., "bold": "\033[1m"
    "": "" # Default no style
}

def _color_text(text: str, text_color: str = "", bg_color: str = "", font_style: str = "") -> str:
    """Apply color, background, and font styling to the text.

    This helper function applies the provided color and font styles to the given text using ANSI escape codes.

    Args:
        text (str): The text string to format.
        text_color (str): The name of the text color (e.g., 'green').
        bg_color (str): The name of the background color.
        font_style (str): The name of the font style (e.g., 'bold').

    Returns:
        str: The formatted text string with ANSI codes.
    """
    color_code = COLORS.get(text_color, COLORS['white']) # Default to white
    bg_code = BACKGROUNDS.get(bg_color, "")
    style_code = STYLES.get(font_style, "")
    return f"{style_code}{color_code}{bg_code}{text}{RESET}"


def pprint(print_data: Any = None, text_color: str = "white", bg_color: str = "", font_style: str = "") -> None:
    """Pretty prints the given data with optional color, background, and font style.

    This function formats the input data based on its type and prints it to the console. The data is printed with optional
    text color, background color, and font style based on the specified parameters. The function can handle dictionaries,
    lists, strings, and potentially other types via str().

    Args:
        print_data (Any): The data to print.
        text_color (str): The name of the text color. Defaults to "white".
        bg_color (str): The name of the background color. Defaults to "".
        font_style (str): The name of the font style. Defaults to "".
    """
    # Basic implementation: just convert to string and colorize
    # A real pretty printer would format dicts/lists nicely
    import json # For basic pretty printing of dicts/lists

    if isinstance(print_data, (dict, list)):
        try:
            # Use json.dumps for indentation
            formatted_data = json.dumps(print_data, indent=4, ensure_ascii=False)
        except TypeError: # Handle non-serializable data
             formatted_data = str(print_data)
    else:
        formatted_data = str(print_data)

    colored_output = _color_text(formatted_data, text_color, bg_color, font_style)
    # Use built-in print to output to console
    __builtins__.print(colored_output)


# Example Usage:
if __name__ == '__main__': # Corrected from 'name == 'main''
    pprint({"name": "Alice", "age": 30}, text_color="green")
    pprint("This is a test message.", text_color="white")
    pprint(['item1', 'item2', {'key': 'value'}], font_style='bold') # Requires 'bold' in STYLES
```

**Task:** Translate the instructions into English.
```