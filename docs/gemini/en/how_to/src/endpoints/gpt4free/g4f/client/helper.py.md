**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use This Code Block
========================================================================================

Description
-------------------------
This code block provides helper functions for parsing and filtering data from strings, primarily focusing on code blocks and JSON objects.

Execution Steps
-------------------------
1. **`filter_markdown`**:
    - Extracts a code block from a string using regular expressions.
    - Checks if the code block type is allowed (optional).
    - Returns the code block content or a default value if not found.

2. **`filter_json`**:
    - Utilizes `filter_markdown` to extract a JSON code block.
    - Returns the extracted JSON code block or the original text if not found.

3. **`find_stop`**:
    - Determines the first occurrence of a stop word in a string.
    - Truncates the string and a chunk of data (if provided) at the position of the stop word.
    - Returns the index of the stop word, the truncated string, and the truncated chunk.

4. **`filter_none`**:
    - Creates a dictionary from keyword arguments.
    - Filters out key-value pairs where the value is `None`.
    - Returns the filtered dictionary.

5. **`safe_aclose`**:
    - Safely closes an asynchronous generator.
    - Attempts to call `aclose` on the generator if available.
    - Logs any errors encountered during the closure process.


Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.client.helper import filter_markdown, filter_json

text = "```python\nprint('Hello, world!')\n```"

code_block = filter_markdown(text)
print(code_block)  # Output: print('Hello, world!')

json_text = '{"name": "Alice", "age": 30}'
json_data = filter_json(json_text)
print(json_data)  # Output: {"name": "Alice", "age": 30}
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".