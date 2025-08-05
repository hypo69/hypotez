# Module `jjson`

## Overview

This module provides functions for working with JSON data in Python. It simplifies loading, dumping, merging, and converting JSON data in various formats, including dictionaries, lists, and SimpleNamespace objects. It offers features for handling file paths, custom file modes, and error handling with logging.

## Details

The `jjson` module aims to streamline JSON operations within the `hypotez` project. It offers several key features:

- **Robust JSON loading:** `j_loads` handles loading JSON from files, directories, strings, or objects while handling various potential errors with logging.
- **Flexible JSON dumping:** `j_dumps` allows dumping JSON data to files or returning it as a dictionary. It supports various file modes and handles potential errors with logging.
- **SimpleNamespace conversion:** `j_loads_ns` converts loaded JSON data into SimpleNamespace objects for easier access to attributes.
- **Data merging:** The `_merge_data` function allows merging new data with existing data based on different modes (append at the beginning, append at the end).
- **Error handling and logging:** The module uses the `logger` from the `src.logger` module to log potential errors and provide detailed information.

## Functions

### `j_dumps`

**Purpose**: Dump JSON data to a file or return the JSON data as a dictionary.

**Parameters**:

- `data (Dict | SimpleNamespace | List[Dict] | List[SimpleNamespace])`: JSON-compatible data or SimpleNamespace objects to dump.
- `file_path (Optional[Path], optional)`: Path to the output file. If None, returns JSON as a dictionary. Defaults to None.
- `ensure_ascii (bool, optional)`: If True, escapes non-ASCII characters in output. Defaults to True.
- `mode (str, optional)`: File open mode ('w', 'a+', '+a'). Defaults to 'w'.
- `exc_info (bool, optional)`: If True, logs exceptions with traceback. Defaults to True.

**Returns**:

- `Optional[Dict]`: JSON data as a dictionary if successful, or nothing if an error occurs.

**Raises Exceptions**:

- `ValueError`: If the file mode is unsupported.

**Example**:

```python
from src.utils.jjson import j_dumps

data = {"name": "Alice", "age": 30}

# Dump to a file
j_dumps(data, file_path="data.json")

# Return as a dictionary
json_data = j_dumps(data)

# Append data to an existing file
j_dumps(data, file_path="data.json", mode="a+")

# Handle potential errors
try:
    j_dumps(data, file_path="data.json", mode="invalid_mode")
except ValueError as ex:
    logger.error(f"Invalid file mode: {ex}")
```

### `j_loads`

**Purpose**: Load JSON or CSV data from a file, directory, string, or object.

**Parameters**:

- `jjson (dict | SimpleNamespace | str | Path | list)`: Path to file/directory, JSON string, or JSON object.
- `ordered (bool, optional)`: Use OrderedDict to preserve element order. Defaults to True.

**Returns**:

- `dict | list`: Processed data (dictionary or list of dictionaries).

**Raises Exceptions**:

- `FileNotFoundError`: If the specified file is not found.
- `json.JSONDecodeError`: If the JSON data cannot be parsed.

**Example**:

```python
from src.utils.jjson import j_loads

# Load from a file
data = j_loads("data.json")

# Load from a directory
data = j_loads("data_dir")

# Load from a string
data = j_loads('{"name": "Alice", "age": 30}')

# Load from a SimpleNamespace object
data = j_loads(SimpleNamespace(name="Alice", age=30))

# Handle potential errors
try:
    data = j_loads("nonexistent_file.json")
except FileNotFoundError as ex:
    logger.error(f"File not found: {ex}")
```

### `j_loads_ns`

**Purpose**: Load JSON/CSV data and convert to SimpleNamespace.

**Parameters**:

- `jjson (Path | SimpleNamespace | Dict | str)`: Path to file/directory, JSON string, or JSON object.
- `ordered (bool, optional)`: Use OrderedDict to preserve element order. Defaults to True.

**Returns**:

- `SimpleNamespace | List[SimpleNamespace] | Dict`: Processed data as SimpleNamespace objects or a dictionary.

**Example**:

```python
from src.utils.jjson import j_loads_ns

# Load from a file and convert to SimpleNamespace
data = j_loads_ns("data.json")

# Load from a directory and convert to a list of SimpleNamespace objects
data = j_loads_ns("data_dir")

# Load from a string and convert to SimpleNamespace
data = j_loads_ns('{"name": "Alice", "age": 30}')
```

## Inner Functions

### `_convert_to_dict`

**Purpose**: Convert SimpleNamespace and lists to dict.

**Parameters**:

- `value (Any)`: The value to convert.

**Returns**:

- `Any`: Converted value as a dictionary.

**How the Function Works**:

The function recursively traverses the input data structure and converts SimpleNamespace objects and lists to dictionaries.

### `_read_existing_data`

**Purpose**: Read existing JSON data from a file.

**Parameters**:

- `path (Path)`: Path to the JSON file.
- `exc_info (bool, optional)`: If True, logs exceptions with traceback. Defaults to True.

**Returns**:

- `dict`: Existing JSON data as a dictionary.

**How the Function Works**:

The function reads the contents of the specified file and parses it as JSON data using `json.loads`. It handles potential errors during reading and parsing, logging them with detailed information.

### `_merge_data`

**Purpose**: Merge new data with existing data based on mode.

**Parameters**:

- `data (Dict)`: New data to merge.
- `existing_data (Dict)`: Existing data to merge with.
- `mode (str)`: Mode for merging ('w', 'a+', '+a').

**Returns**:

- `Dict`: Merged data as a dictionary.

**How the Function Works**:

The function merges new data with existing data based on the specified mode. It supports appending new data at the beginning or end of existing lists or dictionaries.

### `_decode_strings`

**Purpose**: Recursively decode strings in a data structure.

**Parameters**:

- `data (Any)`: The data structure to decode.

**Returns**:

- `Any`: The data structure with decoded strings.

**How the Function Works**:

The function recursively traverses the input data structure and decodes strings using `codecs.decode` with the `unicode_escape` encoding.

### `_string_to_dict`

**Purpose**: Remove markdown quotes and parse JSON string.

**Parameters**:

- `json_string (str)`: The JSON string to parse.

**Returns**:

- `dict`: The parsed JSON data as a dictionary.

**How the Function Works**:

The function removes markdown quotes (`````, ````json`) from the input string and then attempts to parse it as JSON data using `json.loads`. It handles potential errors during parsing, logging them with detailed information.

## Class `Config`

**Description**: Class for storing configuration settings.

**Attributes**:

- `MODE_WRITE (str)`: File open mode for writing (default: 'w').
- `MODE_APPEND_START (str)`: File open mode for appending at the beginning (default: 'a+').
- `MODE_APPEND_END (str)`: File open mode for appending at the end (default: '+a').

**Examples**:

```python
from src.utils.jjson import Config

# Accessing configuration settings
print(Config.MODE_WRITE)  # Output: 'w'
print(Config.MODE_APPEND_START)  # Output: 'a+'
```

## Parameter Details

- `file_path (Optional[Path], optional)`:  A file path (string or Path object) that points to the JSON file to load or dump data. If this parameter is `None`, then the function will return a dictionary object. Defaults to `None`.

- `ensure_ascii (bool, optional)`:  A boolean value that controls the handling of non-ASCII characters during the JSON encoding. If set to `True`, non-ASCII characters will be escaped. Defaults to `True`.

- `mode (str, optional)`:  A string that specifies the mode used to open a file for writing or appending data. It can be one of the following values:
  -  `'w'`:  Opens the file for writing, overwriting any existing content.
  -  `'a+'`:  Opens the file for appending, and creates the file if it does not exist. It allows reading and writing from the end of the file.
  -  `'+a'`:  Opens the file for appending, and creates the file if it does not exist. It allows reading and writing from the beginning of the file. Defaults to `'w'`.

- `exc_info (bool, optional)`: A boolean value that determines whether to log error information with stack traces. If set to `True`, detailed information about the exception will be logged, including the traceback. If set to `False`, only the error message will be logged. Defaults to `True`.

- `ordered (bool, optional)`:  A boolean value that controls whether the data should be stored in an ordered dictionary (OrderedDict) to preserve the order of elements. If set to `True`, an OrderedDict will be used, preserving the element order. If set to `False`, a regular dictionary will be used, where the order is not guaranteed. Defaults to `True`.

## Examples

```python
from src.utils.jjson import j_dumps, j_loads, j_loads_ns, Config

# Example 1: Dumping JSON data to a file
data = {"name": "Alice", "age": 30, "city": "New York"}
j_dumps(data, file_path="user_data.json")

# Example 2: Loading JSON data from a file
data = j_loads("user_data.json")
print(data)  # Output: {'name': 'Alice', 'age': 30, 'city': 'New York'}

# Example 3: Appending data to an existing file
new_data = {"occupation": "Software Engineer"}
j_dumps(new_data, file_path="user_data.json", mode=Config.MODE_APPEND_START)

# Example 4: Loading JSON data from a string
data = j_loads('{"name": "Bob", "age": 25}')
print(data)  # Output: {'name': 'Bob', 'age': 25}

# Example 5: Loading JSON data from a SimpleNamespace object
data = j_loads_ns(SimpleNamespace(name="Charlie", age=35))
print(data)  # Output: SimpleNamespace(name='Charlie', age=35)

# Example 6: Loading JSON data from a directory
data = j_loads_ns("data_dir")
print(data)  # Output: [SimpleNamespace(name='Alice', age=30), SimpleNamespace(name='Bob', age=25), SimpleNamespace(name='Charlie', age=35)]

# Example 7: Handling potential errors
try:
    data = j_loads("nonexistent_file.json")
except FileNotFoundError as ex:
    logger.error(f"File not found: {ex}")
```