Okay, here is the English translation of the provided system instructions for the `hypotez` project:

---

### **System Instructions for Processing `hypotez` Project Code**

=========================================================================================

Description of functionality and rules for generating, analyzing, and improving code. Aimed at ensuring a consistent and readable coding style that meets requirements.

---

### **Core Principles**

#### **1. General Guidelines**:
- Adhere to a clear and understandable coding style.
- All changes must be justified and comply with established requirements.

#### **2. Comments**:
- Use `#` for inline comments.
- In comments, avoid using pronouns or first-person plural verbs like *"we do"*, *"we go to"*, *"we return"*, *"we send"*, etc. Instead, use precise terms such as *"extraction"*, *"check"*, *"execution"*, *"replacement"*, *"call"*, *"Function performs"*, *"Function changes value"*, *"Function calls"*, *"sending"*. Use impersonal or action-focused language.
Example:
```python
# Incorrect:
def function(param: str, param1: Optional[str | dict | str] = None) -> dict | None:
    # We get the parameter value
    ...
# Correct:

def function(param: str, param1: Optional[str | dict | str] = None) -> dict | None:
    # Function extracts the parameter value
    # or: # Extraction of the parameter value
    ...
# Incorrect:
if not process_directory.exists():
    logger.error(f"Directory does not exist: {process_directory}")
    continue  # We go to the next directory if the current one doesn't exist

if not process_directory.is_dir():
    logger.error(f"This is not a directory: {process_directory}", None, False)
    continue  # We go to the next directory if the current one is not a directory
# Correct:

if not process_directory.exists():
    logger.error(f"Directory does not exist: {process_directory}")
    continue  # Continue to the next directory if the current one does not exist
if not process_directory.is_dir():
    logger.error(f"This is not a directory: {process_directory}", None, False)
    continue  # Continue to the next directory if the current one is not a directory

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
                SomeError: Description of the situation where `SomeError` is raised.

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
```python
"""
...
```rst
 .. module:: src.<module>.<module name>
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
The module minimizes HTML code, removes tags and attributes, and handles
special cases like scripts, styles, and comments.
Uses BeautifulSoup for reliable HTML parsing.

Dependencies:
    - beautifulsoup4 (pip install beautifulsoup4)
    - lxml (optional, for faster parsing: pip install lxml)

 ```rst
 .. module:: src.utils.string.html_simplification
 ```
"""
```

#### **4. Code Formatting**:
- Use single quotes. `a: str = 'value'`, `print('Hello World!')`;
- Add spaces around operators. For example, `x = 5`;
- All parameters must be type-annotated. `def function(param: str, param1: Optional[str | dict | str] = None) -> dict | None:`;
- Do not use `Union`. Use `|` instead.

#### **5. Logging**:
- Always use the `logger` module from `src.logger.logger` for logging.
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

state: int = 'global' # Assuming state should be int, but example uses string literal. Corrected type hint based on usage intent.

def func():
    print(state)

```
- Correct:
```python

class Config:
    state: str = 'global' # Type hint matches the value 'global'

def func():
    print(Config.state)

```

#### **9. Always declare variables at the beginning of the function. Do not declare them in the middle.**
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

#### **10. Concept of `__root__`**
- `__root__` is the path to the project's root directory.
- It is defined in the `header.py` file, which is located in each project directory (implied, but function searches upwards).
- Here is the code for `header.py`:
```python
import sys # Added missing import
from pathlib import Path

def set_project_root(marker_files=('__root__','.git')) -> Path:
    """ Finds the root directory of the project starting from the current file's directory,
    searching upwards and stopping at the first directory containing any of the marker files.

    Args:
        marker_files (tuple): Filenames or directory names to identify the project root.
    
    Returns:
        Path: Path to the root directory if found, otherwise the directory where the script is located.
    """
    __root__: Path
    current_path: Path = Path(__file__).resolve().parent
    __root__ = current_path
    for parent in [current_path] + list(current_path.parents):
        if any((parent / marker).exists() for marker in marker_files):
            __root__ = parent
            break
    # Add root to sys.path if not already present
    if str(__root__) not in sys.path: # Corrected check: compare string paths
        sys.path.insert(0, str(__root__))
    return __root__


# Get the root directory of the project
__root__: Path = set_project_root()
"""__root__ (Path): Path to the root directory of the project"""

```
- Always use `__root__` in imports:
```python
import header
from header import __root__
```

### **11. Error Handling**
- Always handle errors using `try-except` blocks.
- The variable that catches the error must be named `ex`.
Example:
```python
except Exception as ex:
    logger.error('Error while processing data', ex, exc_info=True)
```
- `logger` parameters: `logger(<message>, <error_object>, <exc_info>)`


### **Key Requirements for Responses**:

#### **1. Response Format in Markdown**:
- All responses must be provided in **Markdown** format.

#### **2. Comment Format**:
- Use the specified style for comments and documentation in the code.
- Example:

```python
from typing import Generator, Optional, List, Union # Added Union for example clarity
from pathlib import Path

# Note: The original Russian example used | but the j_loads definition used Union.
# The overall instruction is TO USE |, so adapting the example to use |
# However, keeping Generator return type as is from the example.

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
        as_list (bool): If `True`, returns a generator of lines. Defaults to False.
        extensions (Optional[List[str]]): List of file extensions to read from the directory. Defaults to None.
        chunk_size (int): Size of chunks for reading the file in bytes. Defaults to 8192.

    Returns:
        Generator[str, None, None] | str | None: A generator of strings, a single concatenated string, or `None` in case of an error.

    Raises:
        Exception: If an error occurs while reading the file.

    Example:
        >>> from pathlib import Path
        >>> # Assuming example.txt exists and contains "Example text..."
        >>> file_path = Path('example.txt')
        >>> # Create a dummy file for the example to work
        >>> with open(file_path, 'w') as f:
        ...     f.write('Example text...')
        >>> content = read_text_file(file_path)
        >>> if content:
        ...    print(f'File content: {content[:100]}...')
        File content: Example text......
        >>> # Clean up the dummy file
        >>> import os
        >>> os.remove(file_path)
    """
    ...
```
- Always provide detailed explanations in comments. Avoid vague terms like *"get"* or *"do"*. Instead, use precise terms like *"extract"*, *"check"*, *"execute"*.
- Instead of: *"we get"*, *"we return"*, *"we convert"*, use the object's name: *"the function gets"*, *"the variable returns"*, *"the code converts"*.
- Comments should directly precede the code block they describe and explain its purpose.

#### **3. Spaces Around Assignment Operators**:
- Always add spaces around the `=` operator to improve readability.
- Examples:
  - **Incorrect**: `x=5`
  - **Correct**: `x = 5`

#### **4. Using `j_loads` or `j_loads_ns`**:
- For reading JSON or configuration files, replace standard usage of `open` and `json.load` with `j_loads` or `j_loads_ns`.
- Example:

```python
# Incorrect:
import json
with open('config.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Correct:
# Assuming j_loads is imported from src.utils.jjson
from src.utils.jjson import j_loads 
data = j_loads('config.json') 
```
- Here is the code for `j_loads` and `j_loads_ns` (with translated docstrings):
```python
import json
import codecs
from pathlib import Path
from typing import Any, Dict, List, Optional, Union # Keep Union here as it's in the provided code
from types import SimpleNamespace
from json_repair import repair_json
from collections import OrderedDict # Assuming OrderedDict might be used if ordered=True
# Assuming logger and dict2ns are imported elsewhere correctly
# from src.logger import logger 
# from .convertors.dict import dict2ns 

# Helper functions assumed from the context of j_loads/j_loads_ns
def _decode_strings(data: Any) -> Any:
    """Recursively decode strings in a data structure."""
    if isinstance(data, str):
        try:
           # Attempt to decode unicode escapes, return original if fails
           return codecs.decode(data, 'unicode_escape') 
        except Exception:
            return data
    if isinstance(data, list):
        return [_decode_strings(item) for item in data]
    if isinstance(data, dict):
        return {
            _decode_strings(key): _decode_strings(value) for key, value in data.items()
        }
    return data

def _string_to_dict(json_string: str) -> dict:
    """Remove markdown quotes and parse JSON string."""
    # Simplified check for markdown code fences
    if json_string.strip().startswith("```") and json_string.strip().endswith("```"):
        # Basic cleaning: remove fences and 'json' identifier
        json_string = re.sub(r'^```[json]*\s*', '', json_string.strip())
        json_string = re.sub(r'\s*```$', '', json_string)
        json_string = json_string.strip()
    try:
        # Consider using repair_json here if strings might be malformed
        # repaired = repair_json(json_string)
        # return json.loads(repaired)
        return json.loads(json_string)
    except json.JSONDecodeError as ex:
        # logger.error(f"JSON parsing error:\n {json_string}", ex, False) # Assuming logger exists
        print(f"JSON parsing error: {ex}") # Fallback print
        return {}


def j_loads(
    jjson: Union[dict, SimpleNamespace, str, Path, list], ordered: bool = True # Note: ordered param not used in provided implementation
) -> Union[dict, list]:
    """
    Load JSON data from a file, directory, string, or object.
    Note: CSV reading part is commented out.

    Args:
        jjson (dict | SimpleNamespace | str | Path | list): Path to file/directory, JSON string, or JSON object.
        ordered (bool, optional): If True, aims to preserve element order (Note: currently uses standard dict/list). Defaults to True.

    Returns:
        dict | list: Processed data (dictionary or list of dictionaries/items). Returns {} on error.

    Raises:
        FileNotFoundError: (Handled internally) If the specified file is not found.
        json.JSONDecodeError: (Handled internally) If the JSON data cannot be parsed.
    """
    # Added 'logger' and 'dict2ns' placeholders if they were missing
    global logger, dict2ns
    if 'logger' not in globals(): 
        import logging
        logger = logging.getLogger(__name__) 
    if 'dict2ns' not in globals(): 
        dict2ns = lambda d: SimpleNamespace(**d) if isinstance(d, dict) else d


    try:
        data_to_process: Any = None
        if isinstance(jjson, SimpleNamespace):
            data_to_process = vars(jjson)
        elif isinstance(jjson, Path):
            if jjson.is_dir():
                # Read all json files in the directory and return a list of their contents
                all_files_data = []
                files = list(jjson.glob("*.json"))
                if not files:
                     logger.warning(f"No .json files found in directory: {jjson}")
                     return [] # Return empty list if no json files found
                for file in files:
                    file_data = j_loads(file, ordered=ordered) # Recursive call for each file
                    if file_data or isinstance(file_data, list): # Handle case where file is empty list
                       all_files_data.append(file_data)
                return all_files_data
            elif jjson.is_file():
                 # if jjson.suffix.lower() == ".csv": # CSV part commented out
                 #     # Assuming pandas 'pd' is imported
                 #     # return pd.read_csv(jjson).to_dict(orient="records")
                 #     logger.warning("CSV loading is currently disabled.")
                 #     return {}
                 if jjson.suffix.lower() == ".json":
                     file_content = jjson.read_text(encoding="utf-8")
                     # Use _string_to_dict for potential markdown quotes etc.
                     data_to_process = _string_to_dict(file_content) 
                 else:
                     logger.warning(f"Unsupported file extension: {jjson.suffix} for file {jjson}")
                     return {}
            else:
                 raise FileNotFoundError(f"Path is neither a file nor a directory: {jjson}")

        elif isinstance(jjson, str):
            # Process string input
            data_to_process = _string_to_dict(jjson)
        elif isinstance(jjson, (list, dict)):
            # If input is already list/dict, decode internal strings
             data_to_process = _decode_strings(jjson)
        else:
            logger.error(f"Unsupported input type for j_loads: {type(jjson)}")
            return {}
            
        # Ensure the final return type matches the annotation Union[dict, list]
        if isinstance(data_to_process, (dict, list)):
             # If 'ordered' was intended, this is where OrderedDict might be applied
             # if ordered and isinstance(data_to_process, dict):
             #     return OrderedDict(data_to_process)
            return data_to_process
        else:
             # If _string_to_dict returned {}, or other issues occurred
             logger.warning(f"Processed data is not dict or list: {type(data_to_process)}")
             return {} # Return empty dict on failure or unexpected type

    except FileNotFoundError:
        logger.error(f"File not found: {jjson}", exc_info=False)
        return {}
    except json.JSONDecodeError as ex:
        # Log the content causing the error if it's a string or path
        error_context = str(jjson) if isinstance(jjson, (str, Path)) else type(jjson).__name__
        logger.error(f"JSON parsing error processing: {error_context}\nError: {ex}", exc_info=False)
        return {}
    except Exception as ex:
        logger.error(f"Error loading data from: {jjson}. Error: {ex}", exc_info=True) # Log full traceback for unexpected errors
        return {}


def j_loads_ns(
    jjson: Union[Path, SimpleNamespace, Dict, str], ordered: bool = True
) -> Union[SimpleNamespace, List[SimpleNamespace], Dict]: # Return type allows Dict if conversion fails
    """Load JSON data and convert nested dictionaries to SimpleNamespace."""
    # Added 'logger' and 'dict2ns' placeholders if they were missing
    global logger, dict2ns
    if 'logger' not in globals(): 
        import logging
        logger = logging.getLogger(__name__) 
    if 'dict2ns' not in globals(): 
        dict2ns = lambda d: SimpleNamespace(**d) if isinstance(d, dict) else d

    data = j_loads(jjson, ordered=ordered) # Load data using j_loads first
    
    if not data and not isinstance(data, list): # Check if j_loads failed (returned {}) or returned empty list
        return {} # Return empty dict if loading failed

    try:
        if isinstance(data, list):
            # Convert each item in the list if it's a dict
            return [dict2ns(item) for item in data]
        elif isinstance(data, dict):
            # Convert the dictionary itself
            return dict2ns(data)
        else:
            # Should not happen if j_loads works correctly, but handle defensively
            logger.warning(f"j_loads returned unexpected type {type(data)}, returning as is.")
            return data # Return the data as is if not list/dict (though annotation expects NS or List[NS])
    except Exception as ex:
        logger.error(f"Error converting loaded data to SimpleNamespace: {ex}", exc_info=True)
        return {} # Return empty dict on conversion error


```

#### **5. Preserving Comments**:
- All existing comments starting with `#` must be preserved unchanged in the "Improved Code" section.
- If a comment seems outdated or unclear, do not modify it. Instead, note it in the "Changes" section (or similar review notes).

#### **6. Handling `...` in Code**:
- Leave `...` as placeholders in the code without modification.
- Do not document lines containing only `...`.

#### **7. Annotations**
- Type annotations must be defined for all variables.
- All input and output parameters for all functions must be annotated.
- (Redundant) All parameters must have type annotations.


#### **8. `webdriver`**
- The code uses `webdriver`. It is imported from the `webdriver` module of the `hypotez` project.
```python
# Corrected import path assuming 'webdriver' is under 'src'
from src.webdriver import Driver, Chrome, Firefox, Playwright # Added Playwright based on usage pattern
# Assuming Driver initialization needs a browser type class
driver = Driver(Firefox) # Or Driver(browser_type=Firefox) depending on constructor

# After which it can be used like:

close_banner = {
  "attribute": None, # Specifies which attribute's value to use/check (if any)
  "by": "XPATH", # Locator strategy (e.g., "ID", "CSS_SELECTOR", "XPATH")
  "selector": "//button[@id = 'closeXButton']", # The locator string itself
  "if_list": "first", # Action if selector finds multiple elements ("first", "all", etc.)
  "use_mouse": False, # Whether to simulate mouse movement for the action
  "mandatory": False, # If False, failure to find/interact doesn't raise an error
  "timeout": 0, # Explicit wait timeout for this specific locator (0 might mean use default)
  "timeout_for_event": "presence_of_element_located", # Expected condition for the timeout
  "event": "click()", # The action to perform on the element (as a string method call)
  "locator_description": "Closing the pop-up window, it's okay if it didn't appear (`mandatory`:`false`)" # Human-readable description
}

result = driver.execute_locator(close_banner)
```

#### **9. Do not use `Union[]` in the code. Use `|` instead**
For example:
```python
x: str | int ...
```

#### **10. `print` is my built-in function.**
Imported as `from src.utils.printer import pprint as print`

Here it is:
```python
import sys # Needed for stdout
from typing import Any
# Define color/style constants (assuming standard ANSI codes)
RESET = "\033[0m" 
# Example colors (add more as needed)
COLORS = {
    "black": "\033[30m", "red": "\033[31m", "green": "\033[32m", 
    "yellow": "\033[33m", "blue": "\033[34m", "magenta": "\033[35m", 
    "cyan": "\033[36m", "white": "\033[37m",
}
BG_COLORS = {
     "black": "\033[40m", "red": "\033[41m", "green": "\033[42m", 
     "yellow": "\033[43m", "blue": "\033[44m", "magenta": "\033[45m", 
     "cyan": "\033[46m", "white": "\033[47m",
}
FONT_STYLES = {
    "bold": "\033[1m", "underline": "\033[4m", "italic": "\033[3m", # Italic might not be widely supported
}


def _color_text(text: str, text_color: str = "", bg_color: str = "", font_style: str = "") -> str:
    """Apply color, background, and font styling to the text.

    This helper function applies the provided color and font styles to the given text 
    using ANSI escape codes.

    Args:
        text (str): The text to format.
        text_color (str): The name of the text color (e.g., 'red', 'green').
        bg_color (str): The name of the background color.
        font_style (str): The name of the font style (e.g., 'bold', 'underline').

    Returns:
        str: The formatted text string with ANSI codes.
    """
    color_code = COLORS.get(text_color.lower(), "")
    bg_code = BG_COLORS.get(bg_color.lower(), "")
    style_code = FONT_STYLES.get(font_style.lower(), "")
    
    # Only add RESET if some formatting was applied
    reset_code = RESET if color_code or bg_code or style_code else ""
    
    return f"{style_code}{color_code}{bg_code}{text}{reset_code}"


def pprint(print_data: Any = None, text_color: str = "white", bg_color: str = "", font_style: str = "") -> None:
    """Pretty prints the given data with optional color, background, and font style.

    This function formats the input data based on its type and prints it to the console. 
    The data is printed with optional text color, background color, and font style 
    based on the specified parameters. It handles various data types including dicts, 
    lists, strings, etc., using standard print for complex objects if specific formatting isn't implemented.
    Handles Path objects by printing their string representation.

    Args:
        print_data (Any, optional): The data to print. Defaults to None.
        text_color (str, optional): Text color name. Defaults to "white".
        bg_color (str, optional): Background color name. Defaults to "".
        font_style (str, optional): Font style name. Defaults to "".
    """
    output_str: str = ""
    
    # Handle specific types for potentially better formatting
    if print_data is None:
        output_str = "None"
    elif isinstance(print_data, (dict, list, tuple, set)):
        # Use standard print's representation for complex types by default
        # Could implement custom recursive formatting here if needed
        import pprint as standard_pprint
        output_str = standard_pprint.pformat(print_data)
    elif isinstance(print_data, Path):
         output_str = str(print_data) # Print Path object as string
    else:
        output_str = str(print_data) # Convert other types to string

    # Apply coloring to the entire formatted string
    colored_output = _color_text(output_str, text_color, bg_color, font_style)
    
    # Print to standard output
    print(colored_output, file=sys.stdout) # Use standard print here


# Example Usage:
if __name__ == '__main__':
    from pathlib import Path # Needed for Path example

    pprint({"name": "Alice", "age": 30}, text_color="green", font_style="bold")
    pprint(["apple", "banana", "cherry"], text_color="yellow")
    pprint("This is a test message.", text_color="cyan", bg_color="black")
    pprint(Path('/usr/local/bin'), text_color='magenta', font_style='underline')
    pprint(12345, text_color='red')
    pprint(None, text_color='blue', font_style='italic')
```