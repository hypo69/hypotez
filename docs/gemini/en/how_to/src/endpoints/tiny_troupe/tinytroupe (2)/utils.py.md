**Instructions for Generating Code Documentation**

How to Use This Code Block
=========================================================================================

Description
-------------------------
The code snippet provides a collection of general utility functions and convenience methods for use within the TinyTroupe project. These functions cover various aspects, including:

- **Model Input Utilities**:
  - **`compose_initial_LLM_messages_with_templates`**: Composes initial messages for LLM model calls based on specified system and optional user templates, using rendering configurations.
- **Model Output Utilities**:
  - **`extract_json`**: Extracts a JSON object from a string, ignoring any text before the first opening curly brace and any Markdown opening/closing tags.
  - **`extract_code_block`**: Extracts a code block from a string, ignoring any text before the first opening triple backticks and any text after the closing triple backticks.
- **Model Control Utilities**:
  - **`repeat_on_error`**: A decorator that repeats the decorated function call if specific exceptions occur, up to a specified number of retries.
- **Validation**:
  - **`check_valid_fields`**: Checks if the fields in a dictionary are valid according to a list of valid fields.
  - **`sanitize_raw_string`**: Sanitizes a string by removing invalid characters and ensuring it doesn't exceed the maximum Python string length.
  - **`sanitize_dict`**: Sanitizes a dictionary by removing invalid characters and ensuring it's not too deeply nested.
- **Prompt Engineering**:
  - **`add_rai_template_variables_if_enabled`**: Adds RAI template variables to a dictionary if RAI disclaimers are enabled in the configuration.
- **Rendering and Markup**:
  - **`inject_html_css_style_prefix`**: Injects a style prefix to all style attributes in an HTML string.
  - **`break_text_at_length`**: Breaks text (or JSON) at a specified length, inserting "(...)" at the break point.
  - **`pretty_datetime`**: Formats a datetime object into a human-readable string.
  - **`dedent`**: Dedents text, removing leading whitespace and indentation.
- **IO and Startup Utilities**:
  - **`read_config_file`**: Reads and caches a configuration file (`config.ini`) for TinyTroupe settings.
  - **`pretty_print_config`**: Prints the current TinyTroupe configuration in a user-friendly format.
  - **`start_logger`**: Initializes a logger for the TinyTroupe project, setting the log level based on the configuration.
- **JSON Serialization and Deserialization**:
  - **`JsonSerializableRegistry`**: A mixin class that provides JSON serialization and deserialization, along with subclass registration.
- **Other**:
  - **`name_or_empty`**: Returns the name of an agent or world, or an empty string if it's None.
  - **`custom_hash`**: Calculates a deterministic hash of an object, converting it to a string first.
  - **`fresh_id`**: Generates a unique ID for a new object.

Execution Steps
-------------------------
1. **Model Input**:
   - **`compose_initial_LLM_messages_with_templates`**:
     - Loads system and user template files from the "prompts" directory.
     - Renders the templates with specified configurations using the `chevron` library.
     - Creates a list of messages, including the system message and optional user message.
2. **Model Output**:
   - **`extract_json`**:
     - Removes text before the first opening curly brace and any Markdown opening/closing tags.
     - Removes trailing text after the last closing curly or square braces.
     - Replaces invalid escape sequences.
     - Returns the parsed JSON object.
   - **`extract_code_block`**:
     - Removes text before the first opening triple backticks and any text after the closing triple backticks.
     - Returns the extracted code block.
3. **Model Control**:
   - **`repeat_on_error`**:
     - Wraps a function, catching specified exceptions and retrying the function call up to a set number of times.
4. **Validation**:
   - **`check_valid_fields`**:
     - Iterates through keys in a dictionary, raising a ValueError if any key is not in the list of valid fields.
   - **`sanitize_raw_string`**:
     - Converts the string to UTF-8, ignoring invalid characters.
     - Truncates the string to the maximum Python string length.
   - **`sanitize_dict`**:
     - Sanitizes the string representation of the dictionary.
     - Ensures the dictionary is not too deeply nested.
5. **Prompt Engineering**:
   - **`add_rai_template_variables_if_enabled`**:
     - Checks if RAI disclaimers are enabled in the configuration.
     - If enabled, loads RAI disclaimers from the "prompts" directory and adds them to the template variables.
6. **Rendering and Markup**:
   - **`inject_html_css_style_prefix`**:
     - Replaces all style attributes in HTML with the specified style prefix.
   - **`break_text_at_length`**:
     - Checks if the text (or JSON) exceeds the maximum length.
     - If yes, truncates the text and adds "(...)" at the break point.
   - **`pretty_datetime`**:
     - Formats a datetime object into a string with the specified format.
   - **`dedent`**:
     - Removes leading whitespace and indentation from text.
7. **IO and Startup Utilities**:
   - **`read_config_file`**:
     - Reads the default configuration file (`config.ini`) from the module directory.
     - Attempts to load a custom configuration file from the current working directory, overriding default values.
   - **`pretty_print_config`**:
     - Prints the current TinyTroupe configuration in a structured format.
   - **`start_logger`**:
     - Creates a logger for the project, setting the log level from the configuration.
8. **JSON Serialization and Deserialization**:
   - **`JsonSerializableRegistry`**:
     - Provides methods for:
       - `to_json`: Serializes the object into a JSON dictionary.
       - `from_json`: Deserializes a JSON dictionary or file into an instance of the class.
       - `__init_subclass__`: Registers subclasses automatically.
9. **Other**:
   - **`name_or_empty`**:
     - Returns the name of an agent or world, or an empty string if it's None.
   - **`custom_hash`**:
     - Calculates a deterministic hash of an object.
   - **`fresh_id`**:
     - Generates a unique ID.

Usage Example
-------------------------
```python
from tinytroupe.src.endpoints.tiny_troupe.tinytroupe (2).utils import compose_initial_LLM_messages_with_templates, extract_json, repeat_on_error, check_valid_fields

# Example usage of compose_initial_LLM_messages_with_templates
system_template = "system_template.md"
user_template = "user_template.md"
rendering_configs = {"name": "Alice"}
messages = compose_initial_LLM_messages_with_templates(system_template, user_template, rendering_configs)
print(messages)

# Example usage of extract_json
text = "```json\n{\"name\": \"Alice\", \"age\": 30}\n```"
json_data = extract_json(text)
print(json_data)

# Example usage of repeat_on_error
@repeat_on_error(retries=3, exceptions=[ValueError, TypeError])
def my_function(x, y):
    if x < 0 or y < 0:
        raise ValueError("Inputs must be non-negative.")
    return x + y

try:
    result = my_function(-1, 2)
except Exception as e:
    print(f"Error occurred: {e}")

# Example usage of check_valid_fields
data = {"name": "Alice", "age": 30, "city": "New York"}
valid_fields = ["name", "age"]
check_valid_fields(data, valid_fields)  # Raises ValueError because "city" is not a valid field

# Example usage of sanitize_raw_string
raw_string = "This string contains invalid characters: <>&"
sanitized_string = sanitize_raw_string(raw_string)
print(sanitized_string)  # Output: This string contains invalid characters
```