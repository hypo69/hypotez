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
This code block provides functions for converting Excel files to JSON format and vice versa. It allows handling multiple sheets within an Excel file and provides options for saving data to a JSON file or loading data from a JSON file into an Excel file.

Execution Steps
-------------------------
1. **Import necessary libraries:** Import `pandas` for Excel file manipulation, `json` for handling JSON data, `logging` for error handling and informational messages, and `Path` from `pathlib` for working with file paths.
2. **Configure logging:** Set up basic logging to display information and error messages in the console.
3. **Define `read_xls_as_dict` function:**
    - This function reads an Excel file and converts it to a JSON dictionary, optionally handling a specific sheet.
    - It takes the Excel file path (`xls_file`), optional JSON file path (`json_file`), and optional sheet name (`sheet_name`) as arguments.
    - It attempts to read the Excel file using `pd.ExcelFile`.
    - If no sheet name is provided, it iterates through all sheets, reads each sheet using `pd.read_excel`, and converts the data to a dictionary of records (`df.to_dict(orient='records')`).
    - If a sheet name is provided, it reads the specified sheet and converts it to a dictionary of records.
    - If a `json_file` path is provided, it saves the converted JSON data to the specified file.
    - It logs information about successful and unsuccessful actions and returns the converted JSON data or `False` if an error occurs.
4. **Define `save_xls_file` function:**
    - This function saves JSON data to an Excel file.
    - It takes a dictionary of data (`data`) where keys are sheet names and values are lists of dictionaries representing rows, and the Excel file path (`file_path`) as arguments.
    - It uses `pd.ExcelWriter` to write the data to the specified file.
    - It iterates through each sheet name and corresponding rows in the data dictionary, creates a Pandas DataFrame from the rows, and writes the DataFrame to the Excel file using `df.to_excel`.
    - It logs information about successful and unsuccessful actions and returns `True` if the save is successful or `False` if an error occurs.

Usage Example
-------------------------

```python
# Reading and optionally saving to JSON
data = read_xls_as_dict('input.xlsx', 'output.json', 'Sheet1')  # Reads sheet named 'Sheet1'
if data:
    print(data)  # Output will be {'Sheet1': [{...}]}

# Saving from JSON data
data_to_save = {'Sheet1': [{'column1': 'value1', 'column2': 'value2'}]}
success = save_xls_file(data_to_save, 'output.xlsx')
if success:
    print("Successfully saved to output.xlsx")
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".