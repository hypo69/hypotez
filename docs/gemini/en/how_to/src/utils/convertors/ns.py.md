**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Convert a SimpleNamespace Object to Various Formats
=========================================================================================

Description
-------------------------
The `src/utils/convertors/ns.py` module provides functions for converting SimpleNamespace objects to different formats, including dictionaries, JSON, CSV, XML, and XLS. 

Execution Steps
-------------------------
1. **Import necessary modules**: Import the required modules, such as `json`, `csv`, `SimpleNamespace`, `Path`, `List`, `Dict`, `Any`, `xml2dict`, `save_csv_file`, `save_xls_file`, and `logger`.
2. **Define the `ns2dict` function**: This function recursively converts an object with key-value pairs to a dictionary. It handles empty keys by substituting them with an empty string.
3. **Define the `ns2csv` function**: This function converts a SimpleNamespace object to CSV format. It uses the `ns2dict` function to convert the SimpleNamespace object to a dictionary and then saves the data to a CSV file using the `save_csv_file` function.
4. **Define the `ns2xml` function**: This function converts a SimpleNamespace object to XML format. It utilizes the `ns2dict` function to convert the SimpleNamespace object to a dictionary and then utilizes the `xml2dict` function to generate the XML string.
5. **Define the `ns2xls` function**: This function converts a SimpleNamespace object to XLS format. It utilizes the `save_xls_file` function to directly save the data to an XLS file. 

Usage Example
-------------------------

```python
from src.utils.convertors.ns import ns2dict, ns2csv, ns2xml, ns2xls
from types import SimpleNamespace

# Create a SimpleNamespace object
data = SimpleNamespace(name="Alice", age=30, city="New York")

# Convert to dictionary
dict_data = ns2dict(data)
print(f"Dictionary: {dict_data}")

# Convert to CSV
ns2csv(data, "data.csv")
print("CSV file created: data.csv")

# Convert to XML
xml_data = ns2xml(data, "person")
print(f"XML data: {xml_data}")

# Convert to XLS
ns2xls(data, "data.xls")
print("XLS file created: data.xls")
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".