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
This code block defines a `j_loads` function that loads JSON data from various sources, including files, directories, strings, and objects. It supports the following features:

- **File Loading**: Reads JSON data from a specified file path, handling file extensions like ".json".
- **Directory Loading**: Recursively loads JSON files within a given directory.
- **String Parsing**: Parses JSON data from a string input, removing markdown quotes (if present).
- **Object Conversion**: Handles SimpleNamespace objects by converting them to dictionaries before processing.
- **Ordered Dictionary Support**: Optionally uses OrderedDict to preserve element order in the output.

Execution Steps
-------------------------
1. **Data Input**: The function accepts a `jjson` argument that can be a `dict`, `SimpleNamespace`, `str`, `Path`, or `list`.
2. **Data Type Handling**: The code checks the type of the input and performs appropriate actions based on its type.
3. **File Loading**: For file paths, it reads the file content and parses it as JSON.
4. **Directory Loading**: For directories, it iterates over JSON files within the directory and loads each file separately.
5. **String Parsing**: For strings, it removes markdown quotes and parses the remaining string as JSON.
6. **Object Conversion**: For SimpleNamespace objects, it converts them to dictionaries.
7. **JSON Parsing**: If the data is in a valid JSON format, it parses the JSON data into a Python dictionary.
8. **Ordered Dictionary Support**: If the `ordered` argument is True, it uses OrderedDict to preserve the order of elements in the JSON data.
9. **Error Handling**: The function includes error handling to log potential exceptions during file reading, JSON parsing, and data loading.
10. **Data Return**: It returns the processed JSON data as a dictionary or a list of dictionaries.


Usage Example
-------------------------

```python
from src.utils.jjson import j_loads

# Load JSON data from a file
file_path = Path("data.json")
data = j_loads(file_path)
print(data)

# Load JSON data from a directory
directory_path = Path("json_files")
data = j_loads(directory_path)
print(data)

# Parse JSON data from a string
json_string = '{"name": "John", "age": 30}'
data = j_loads(json_string)
print(data)

# Load JSON data from a SimpleNamespace object
data = j_loads({"name": "Jane", "age": 25})
print(data)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".