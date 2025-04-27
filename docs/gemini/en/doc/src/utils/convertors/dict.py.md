# Module: src.utils.convertors.dict

## Overview

This module provides utilities for converting dictionaries to various data formats, including SimpleNamespace, XML, CSV, JSON, XLS, HTML, and PDF. It aims to simplify data manipulation and export tasks. 

## Details

The module contains functions for recursive conversion of dictionaries to SimpleNamespace objects, generating XML strings, and saving data to CSV, JSON, XLS, and PDF files. Additionally, it includes functions to generate an HTML table string from a dictionary. 

The module relies on libraries such as `xml.etree.ElementTree`, `xml.dom.minidom`, `reportlab`, and `pandas` for various conversion tasks.

## Table of Contents

- [Classes](#classes)
- [Functions](#functions)
    - [replace_key_in_dict](#replace_key_in_dict)
    - [dict2ns](#dict2ns)
    - [dict2xml](#dict2xml)
    - [dict2csv](#dict2csv)
    - [dict2xls](#dict2xls)
    - [dict2html](#dict2html)
    - [dict2pdf](#dict2pdf)
    - [example_json2xml](#example_json2xml)

## Classes 

## Functions

### replace_key_in_dict

**Purpose**: This function recursively replaces a specified key in a dictionary or list with a new key. It traverses through nested dictionaries and lists, replacing the target key.

**Parameters**:
- `data` (dict | list): The dictionary or list in which the key replacement is performed.
- `old_key` (str): The key to be replaced.
- `new_key` (str): The new key to replace the old key with.

**Returns**:
- `dict`: The updated dictionary with replaced keys.

**Raises Exceptions**:
- None

**How the Function Works**:
- The function iterates through the keys of the input dictionary or list.
- If the key matches the `old_key`, it's replaced with the `new_key`.
- The function recursively calls itself for nested dictionaries and lists, ensuring key replacements are performed throughout the entire data structure.

**Examples**:

```python
# Example 1: Simple dictionary
data = {"old_key": "value"}
updated_data = replace_key_in_dict(data, "old_key", "new_key")
# updated_data becomes {"new_key": "value"}

# Example 2: Nested dictionary
data = {"outer": {"old_key": "value"}}
updated_data = replace_key_in_dict(data, "old_key", "new_key")
# updated_data becomes {"outer": {"new_key": "value"}}

# Example 3: List of dictionaries
data = [{"old_key": "value1"}, {"old_key": "value2"}]
updated_data = replace_key_in_dict(data, "old_key", "new_key")
# updated_data becomes [{"new_key": "value1"}, {"new_key": "value2"}]

# Example 4: Mixed nested structure with lists and dictionaries
data = {"outer": [{"inner": {"old_key": "value"}}]}
updated_data = replace_key_in_dict(data, "old_key", "new_key")
# updated_data becomes {"outer": [{"inner": {"new_key": "value"}}]}
```

### dict2ns

**Purpose**: This function recursively converts dictionaries to SimpleNamespace objects. It iterates through the dictionary and its nested structures, converting each dictionary to a SimpleNamespace object. 

**Parameters**:
- `data` (Dict[str, Any] | List[Any]): The dictionary or list to be converted.

**Returns**:
- `Any`: The converted data as a SimpleNamespace or a list of SimpleNamespace objects.

**Raises Exceptions**:
- None

**How the Function Works**:
- The function checks if the input is a dictionary or a list. 
- If it's a dictionary, it iterates through each key-value pair.
- If a value is a dictionary, it calls `dict2ns` recursively to convert it.
- If a value is a list, it applies `dict2ns` to each element in the list, converting dictionaries within it.
- Finally, it returns a SimpleNamespace object created using the converted data.

**Examples**:

```python
# Example 1: Converting a simple dictionary
data = {"key1": "value1", "key2": "value2"}
ns = dict2ns(data)
print(ns.key1)  # Output: value1
print(ns.key2)  # Output: value2

# Example 2: Converting a nested dictionary
data = {"key1": "value1", "key2": {"key3": "value3", "key4": "value4"}}
ns = dict2ns(data)
print(ns.key1)  # Output: value1
print(ns.key2.key3)  # Output: value3
print(ns.key2.key4)  # Output: value4
```

### dict2xml

**Purpose**: This function generates an XML string from a dictionary. It handles both simple and complex data types, including nested dictionaries and lists.

**Parameters**:
- `data` (Dict[str, Any]): The dictionary to convert to XML.
- `encoding` (str, optional): The encoding of the XML data. Defaults to 'UTF-8'.

**Returns**:
- `str`: The XML string representing the input dictionary.

**Raises Exceptions**:
- `Exception`: If more than one root node is provided.

**How the Function Works**:
- The function uses `xml.dom.minidom` to create and manipulate XML DOM objects.
- It defines helper functions to handle different data types:
    - `_process_simple`: Creates a simple XML node for integer, string, or float values.
    - `_process_attr`: Generates attributes for an XML element from a dictionary.
    - `_process_complex`: Handles complex data structures like lists or dictionaries by creating child nodes and attributes.
- The main `_process` function recursively traverses the dictionary, generating XML nodes for each key-value pair.
- The function validates that only one root node is provided before generating the final XML string.

**Examples**:

```python
# Example 1: Converting a simple dictionary
data = {"name": "John Doe", "age": 30}
xml_output = dict2xml(data)
print(xml_output)

# Example 2: Converting a nested dictionary with attributes
data = {
    "product": {
        "name": {"@id": "1", "#text": "Test Product"},
        "price": "10.00",
        "id_tax_rules_group": "13",
        "id_category_default": "2",
    }
}
xml_output = dict2xml(data)
print(xml_output)
```

### dict2csv

**Purpose**: This function saves dictionary or SimpleNamespace data to a CSV file. It converts the input data into a format suitable for a CSV file.

**Parameters**:
- `data` (dict | SimpleNamespace): The dictionary or SimpleNamespace object to save.
- `file_path` (str | Path): The path to the CSV file.

**Returns**:
- `bool`: True if the file was saved successfully, False otherwise.

**Raises Exceptions**:
- None

**How the Function Works**:
- The function utilizes the `save_csv_file` function from the `src.utils.xls` module to handle CSV saving.
- It first converts SimpleNamespace objects to dictionaries if necessary.
- It then calls `save_csv_file` to write the data to the specified file path.

**Examples**:

```python
# Example 1: Saving a simple dictionary to CSV
data = {"name": "Alice", "age": 30, "city": "New York"}
file_path = "data.csv"
result = dict2csv(data, file_path)
print(f"File saved: {result}")

# Example 2: Saving a SimpleNamespace object to CSV
data = SimpleNamespace(name="Bob", age=25, country="USA")
file_path = "data.csv"
result = dict2csv(data, file_path)
print(f"File saved: {result}")
```

### dict2xls

**Purpose**: This function saves dictionary or SimpleNamespace data to an XLS file. It converts the input data into a format suitable for an XLS file.

**Parameters**:
- `data` (dict | SimpleNamespace): The dictionary or SimpleNamespace object to save.
- `file_path` (str | Path): The path to the XLS file.

**Returns**:
- `bool`: True if the file was saved successfully, False otherwise.

**Raises Exceptions**:
- None

**How the Function Works**:
- The function utilizes the `save_xls_file` function from the `src.utils.xls` module to handle XLS saving.
- It first converts SimpleNamespace objects to dictionaries if necessary.
- It then calls `save_xls_file` to write the data to the specified file path.

**Examples**:

```python
# Example 1: Saving a simple dictionary to XLS
data = {"name": "Alice", "age": 30, "city": "New York"}
file_path = "data.xls"
result = dict2xls(data, file_path)
print(f"File saved: {result}")

# Example 2: Saving a SimpleNamespace object to XLS
data = SimpleNamespace(name="Bob", age=25, country="USA")
file_path = "data.xls"
result = dict2xls(data, file_path)
print(f"File saved: {result}")
```

### dict2html

**Purpose**: This function generates an HTML table string from a dictionary or SimpleNamespace object. It creates a table structure, recursively handling nested dictionaries and lists.

**Parameters**:
- `data` (dict | SimpleNamespace): The dictionary or SimpleNamespace object to convert to HTML.
- `encoding` (str, optional): The encoding of the HTML data. Defaults to 'UTF-8'.

**Returns**:
- `str`: The HTML string representing the input dictionary.

**Raises Exceptions**:
- None

**How the Function Works**:
- The function utilizes a helper function `dict_to_html_table` to recursively convert the dictionary to HTML table structure.
- The `dict_to_html_table` function iterates through key-value pairs in the dictionary.
- For dictionary values, it recursively calls itself to create nested tables.
- For list values, it generates unordered lists (`<ul>`) with list items (`<li>`).
- The main function converts SimpleNamespace objects to dictionaries if necessary and then calls `dict_to_html_table` to generate the final HTML string.

**Examples**:

```python
# Example 1: Converting a simple dictionary
data = {"name": "Alice", "age": 30, "city": "New York"}
html_output = dict2html(data)
print(html_output)

# Example 2: Converting a nested dictionary
data = {"person": {"name": "Bob", "age": 25, "address": {"street": "Main Street", "city": "New York"}}}
html_output = dict2html(data)
print(html_output)
```

### dict2pdf

**Purpose**: This function saves dictionary data as a PDF file. It converts the dictionary into a simple text representation and then writes it to the PDF file.

**Parameters**:
- `data` (dict | SimpleNamespace): The dictionary or SimpleNamespace object to convert to PDF.
- `file_path` (str | Path): The path to the PDF file.

**Returns**:
- None

**Raises Exceptions**:
- None

**How the Function Works**:
- The function utilizes the `reportlab` library to create and write to PDF files.
- It first converts SimpleNamespace objects to dictionaries if necessary.
- It then creates a `Canvas` object with the specified file path and page size (A4).
- It iterates through key-value pairs in the dictionary, writing each pair as a line of text to the PDF file.
- If there's insufficient space on the current page, a new page is created.

**Examples**:

```python
# Example 1: Saving a simple dictionary to PDF
data = {"name": "Alice", "age": 30, "city": "New York"}
file_path = "data.pdf"
dict2pdf(data, file_path)

# Example 2: Saving a SimpleNamespace object to PDF
data = SimpleNamespace(name="Bob", age=25, country="USA")
file_path = "data.pdf"
dict2pdf(data, file_path)
```

### example_json2xml

**Purpose**: This function provides an example of converting JSON data to XML using the `dict2xml` function.

**Parameters**:
- None

**Returns**:
- None

**Raises Exceptions**:
- None

**How the Function Works**:
- The function defines a sample JSON dictionary.
- It calls `dict2xml` to convert the JSON data to XML.
- It prints the generated XML string.

**Examples**:

```python
# Example usage
json_data = {
    "product": {
        "name": {
            "language": [
                {"@id": "1", "#text": "Test Product"},
                {"@id": "2", "#text": "Test Product"},
                {"@id": "3", "#text": "Test Product"},
            ]
        },
        "price": "10.00",
        "id_tax_rules_group": "13",
        "id_category_default": "2",
    }
}

xml_output = dict2xml(json_data)
print(xml_output)
```