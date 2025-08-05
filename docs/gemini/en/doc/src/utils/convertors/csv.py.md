# Module: CSV and JSON Conversion Utilities

## Overview

This module provides functions for converting CSV data to JSON and SimpleNamespace formats. The primary functions are:

- `csv2dict`: Converts CSV data to a dictionary.
- `csv2ns`: Converts CSV data to SimpleNamespace objects.
- `csv_to_json`: Converts a CSV file to JSON format and saves it to a JSON file.

## Details

This module is used to manage data transformations between CSV and other formats, primarily JSON. This is crucial for various tasks, such as data analysis, data manipulation, and interoperability with other tools that use JSON as the standard data format. 

## Classes

This module doesn't define any classes.

## Functions

### `csv2dict`

**Purpose**: Converts CSV data to a dictionary.

**Parameters**:
- `csv_file` (str | Path): Path to the CSV file to read.

**Returns**:
- `dict | None`: Dictionary containing the data from CSV converted to JSON format, or `None` if conversion failed.

**Raises Exceptions**:
- `Exception`: If unable to read CSV.

**How the Function Works**:
- The function uses `read_csv_as_dict` function to read CSV data and convert it into a dictionary.
- The `read_csv_as_dict` function is imported from the `src.utils.csv` module and is responsible for handling the actual CSV reading and conversion process.

**Examples**:

```python
# Example 1: Using a CSV file path as a string
csv_file_path = 'data.csv'
data_dict = csv2dict(csv_file_path)
print(data_dict) 

# Example 2: Using a CSV file path as a Path object
from pathlib import Path
csv_file_path = Path('data.csv')
data_dict = csv2dict(csv_file_path)
print(data_dict) 
```

### `csv2ns`

**Purpose**: Converts CSV data to SimpleNamespace objects.

**Parameters**:
- `csv_file` (str | Path): Path to the CSV file to read.

**Returns**:
- `SimpleNamespace | None`: SimpleNamespace object containing the data from CSV, or `None` if conversion failed.

**Raises Exceptions**:
- `Exception`: If unable to read CSV.

**How the Function Works**:
- The function uses `read_csv_as_ns` function to read CSV data and convert it into a SimpleNamespace object.
- The `read_csv_as_ns` function is imported from the `src.utils.csv` module and is responsible for handling the actual CSV reading and conversion process.

**Examples**:

```python
# Example 1: Using a CSV file path as a string
csv_file_path = 'data.csv'
data_ns = csv2ns(csv_file_path)
print(data_ns) 

# Example 2: Using a CSV file path as a Path object
from pathlib import Path
csv_file_path = Path('data.csv')
data_ns = csv2ns(csv_file_path)
print(data_ns) 
```

### `csv_to_json`

**Purpose**: Converts a CSV file to JSON format and saves it to a JSON file.

**Parameters**:
- `csv_file_path` (str | Path): The path to the CSV file to read.
- `json_file_path` (str | Path): The path to the JSON file to save.
- `exc_info` (bool, optional): If True, includes traceback information in the log. Defaults to True.

**Returns**:
- `List[Dict[str, str]] | None`: The JSON data as a list of dictionaries, or None if conversion failed.

**Examples**:
```python
# Example 1: Using string paths
csv_file_path = 'dialogue_log.csv'
json_file_path = 'dialogue_log.json'
json_data = csv_to_json(csv_file_path, json_file_path)
print(json_data)

# Example 2: Using Path objects
from pathlib import Path
csv_file_path = Path('dialogue_log.csv')
json_file_path = Path('dialogue_log.json')
json_data = csv_to_json(csv_file_path, json_file_path)
print(json_data)
```

**How the Function Works**:
- The function first reads the CSV file using the `read_csv_file` function imported from the `src.utils.csv` module.
- If the data is successfully read, it opens the specified JSON file in write mode (`'w'`) with UTF-8 encoding.
- The function then uses the `json.dump` function to write the data to the JSON file with indentation (`indent=4`) for readability.
- If any exceptions occur during the process, an error message is logged using `logger.error` and `None` is returned.

## Parameter Details

- `csv_file` (str | Path): Path to the CSV file to be processed. Can be either a string representing the file path or a Path object.
- `json_file_path` (str | Path): Path to the JSON file where the converted data will be saved. Can be either a string representing the file path or a Path object.
- `exc_info` (bool, optional): Flag that determines whether to include traceback information in the error log. Defaults to True, which means traceback information will be included if an exception occurs. 

## Examples

```python
# Example 1: Converting a CSV file to a dictionary
csv_file_path = 'data.csv'
data_dict = csv2dict(csv_file_path)
print(data_dict) 

# Example 2: Converting a CSV file to SimpleNamespace objects
csv_file_path = 'data.csv'
data_ns = csv2ns(csv_file_path)
print(data_ns)

# Example 3: Converting a CSV file to JSON and saving it
csv_file_path = 'dialogue_log.csv'
json_file_path = 'dialogue_log.json'
json_data = csv_to_json(csv_file_path, json_file_path)
print(json_data)
```