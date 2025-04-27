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
This code snippet defines three functions: `check_valid_fields`, `sanitize_raw_string`, and `sanitize_dict`. 

`check_valid_fields` validates the keys in a dictionary against a list of valid keys, raising a `ValueError` if any invalid keys are found. 

`sanitize_raw_string` cleans a string by removing invalid characters and ensuring it's not longer than the maximum Python string length.

`sanitize_dict` cleans a dictionary by sanitizing its string values and ensuring it doesn't exceed a maximum nesting depth.

Execution Steps
-------------------------
1. **`check_valid_fields`**:
   - Iterates through each key in the input dictionary.
   - Checks if the key exists in the provided list of valid fields.
   - If an invalid key is found, raises a `ValueError` with a message specifying the invalid key and the valid keys.

2. **`sanitize_raw_string`**:
   - Converts the string to valid UTF-8 by removing invalid characters.
   - Normalizes the string using the Unicode Normalization Form C (NFC).
   - Truncates the string to the maximum allowed Python string length.

3. **`sanitize_dict`**:
   - Iterates through the dictionary's key-value pairs.
   - If the value is a string, sanitizes it using `sanitize_raw_string`.
   - Returns the sanitized dictionary.

Usage Example
-------------------------

```python
# Example usage for check_valid_fields
valid_fields = ['name', 'age', 'city']
data = {'name': 'Alice', 'age': 30, 'country': 'USA'}
try:
    check_valid_fields(data, valid_fields)
except ValueError as e:
    print(f"Error: {e}")

# Example usage for sanitize_raw_string
raw_string = "This is a string with invalid characters: 😜"
sanitized_string = sanitize_raw_string(raw_string)
print(f"Sanitized string: {sanitized_string}")

# Example usage for sanitize_dict
input_dict = {'name': 'Bob', 'age': 35, 'address': '123 Main St, Sometown'}
sanitized_dict = sanitize_dict(input_dict)
print(f"Sanitized dictionary: {sanitized_dict}")
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".