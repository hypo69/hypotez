# Module: src.utils.convertors.ns

## Overview

This module provides functions for converting `SimpleNamespace` objects into various formats: dictionaries, JSON, CSV, XML, and XLS. 

## Details

The module offers a set of utilities for working with `SimpleNamespace` objects, commonly used for representing data with key-value pairs.  The functions facilitate efficient conversion of these objects into different formats, making it easier to handle and process data in various applications.

## Functions

### `ns2dict`

**Purpose**: This function recursively converts an object with key-value pairs to a dictionary. It handles empty keys by substituting them with an empty string.

**Parameters**:

- `obj` (Any): The object to convert. Can be `SimpleNamespace`, `dict`, or any object with a similar structure.

**Returns**:

- `Dict[str, Any]`: The converted dictionary with nested structures handled.

**How the Function Works**: 

The function uses a recursive helper function `convert` to process the input object. `convert` iterates through the object's key-value pairs, recursively converting each value to a dictionary if it's a `SimpleNamespace` or has an `items` attribute. For lists, it converts each element recursively. If the value is not a `SimpleNamespace`, `dict`, or list, it's returned as is.

**Examples**:

```python
>>> from src.utils.convertors.ns import ns2dict
>>> from types import SimpleNamespace
>>> ns_obj = SimpleNamespace(name='John', age=30, address={'street': 'Main St', 'city': 'New York'})
>>> ns2dict(ns_obj)
{'name': 'John', 'age': 30, 'address': {'street': 'Main St', 'city': 'New York'}}

>>> ns2dict({'a': 1, 'b': {'c': 2, 'd': 3}})
{'a': 1, 'b': {'c': 2, 'd': 3}}

>>> ns2dict([1, 2, 3])
[1, 2, 3]

>>> ns2dict(None)
None
```

### `ns2csv`

**Purpose**: This function converts a `SimpleNamespace` object to CSV format.

**Parameters**:

- `ns_obj` (`SimpleNamespace`): The `SimpleNamespace` object to convert.
- `csv_file_path` (`str` | `Path`): Path to save the CSV file.

**Returns**:

- `bool`: True if successful, False otherwise.

**How the Function Works**:

The function first converts the `SimpleNamespace` object to a dictionary using `ns2dict`. It then calls the `save_csv_file` function to save the data to the specified CSV file.

**Raises Exceptions**:

- `Exception`: If an error occurs during conversion or saving the file.

**Examples**:

```python
>>> from src.utils.convertors.ns import ns2csv
>>> from types import SimpleNamespace
>>> ns_obj = SimpleNamespace(name='John', age=30, city='New York')
>>> ns2csv(ns_obj, 'data.csv') # This will save the data to a file named "data.csv"
True
```

### `ns2xml`

**Purpose**: This function converts a `SimpleNamespace` object to XML format.

**Parameters**:

- `ns_obj` (`SimpleNamespace`): The `SimpleNamespace` object to convert.
- `root_tag` (`str`): The root element tag for the XML. Defaults to 'root'.

**Returns**:

- `str`: The resulting XML string.

**How the Function Works**:

The function first converts the `SimpleNamespace` object to a dictionary using `ns2dict`. Then, it uses the `xml2dict` function to generate an XML string based on the dictionary data.

**Raises Exceptions**:

- `Exception`: If an error occurs during conversion.

**Examples**:

```python
>>> from src.utils.convertors.ns import ns2xml
>>> from types import SimpleNamespace
>>> ns_obj = SimpleNamespace(name='John', age=30, city='New York')
>>> xml_string = ns2xml(ns_obj, root_tag='person')
>>> print(xml_string)
<person>
  <name>John</name>
  <age>30</age>
  <city>New York</city>
</person>
```

### `ns2xls`

**Purpose**: This function converts a `SimpleNamespace` object to XLS format.

**Parameters**:

- `ns_obj` (`SimpleNamespace`): The `SimpleNamespace` object to convert.
- `xls_file_path` (`str` | `Path`): Path to save the XLS file.

**Returns**:

- `bool`: True if successful, False otherwise.

**How the Function Works**:

The function uses the `save_xls_file` function to save the `SimpleNamespace` object to the specified XLS file.

**Raises Exceptions**:

- `Exception`: If an error occurs during saving the file.

**Examples**:

```python
>>> from src.utils.convertors.ns import ns2xls
>>> from types import SimpleNamespace
>>> ns_obj = SimpleNamespace(name='John', age=30, city='New York')
>>> ns2xls(ns_obj, 'data.xls') # This will save the data to a file named "data.xls"
True
```

## Parameter Details

- `obj` (Any): The object to convert. Can be a `SimpleNamespace`, `dict`, or any object with a similar structure.
- `ns_obj` (`SimpleNamespace`): The `SimpleNamespace` object to convert.
- `csv_file_path` (`str` | `Path`): Path to save the CSV file.
- `xls_file_path` (`str` | `Path`): Path to save the XLS file.
- `root_tag` (`str`): The root element tag for the XML. Defaults to 'root'.