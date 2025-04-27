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
The code defines two classes, `keyboards` and `PromptsCompressor`, designed to handle keyboard creation and prompt generation in a Telegram bot application. 

**Keyboards Class**
This class provides methods for constructing different keyboard layouts.
- `_keyboard_two_blank`: This method creates a keyboard with two columns, taking lists of data and names as inputs. It generates inline buttons with labels from the `name` list and corresponding callback data from the `data` list.
- `_reply_keyboard`: This method creates a simple reply keyboard with buttons based on the provided list of `name`s.

**PromptsCompressor Class**
This class manages prompts and their formatting.
- `__init__`: Initializes the class with a predefined list of prompt templates, each representing a different prompt structure.
- `get_prompt`: This method retrieves a prompt based on an index and information list. It replaces placeholders in the prompt template with corresponding values from the information list.
- `html_tags_insert`: This static method takes a response string and applies HTML tags to format it according to predefined patterns. It replaces specific text patterns with HTML tags to enhance the visual appearance of the response.

Execution Steps
-------------------------
1. The `keyboards` class offers two protected methods:
    - `_keyboard_two_blank`:
        - Takes lists of data and names as input.
        - Creates inline keyboard buttons using the provided data and names.
        - Arranges buttons in two columns.
        - Returns the constructed inline keyboard.
    - `_reply_keyboard`:
        - Takes a list of names as input.
        - Creates reply keyboard buttons from the names.
        - Returns the constructed reply keyboard.

2. The `PromptsCompressor` class:
    - Initializes with a list of predefined prompt templates stored in a JSON file (`prompts.json`).
    - In the `get_prompt` method:
        - Reads the relevant prompt template from the `prompts.json` file.
        - Replaces placeholders in the template with values from the input information list.
        - Returns the formatted prompt string.
    - The `html_tags_insert` method:
        - Iterates over a predefined list of patterns (regex patterns and corresponding HTML tags).
        - Replaces matched patterns in the response string with their corresponding HTML tags.
        - Returns the formatted response string with HTML tags applied.

Usage Example
-------------------------

```python
from ToolBox.BaseSettings.AuxiliaryClasses import keyboards, PromptsCompressor

# Example usage of keyboards class
keyboard_instance = keyboards()
data = ["option1", "option2", "option3"]
names = ["Choice 1", "Choice 2", "Choice 3"]
keyboard = keyboard_instance._keyboard_two_blank(data, names)
# Send keyboard using bot.send_message(...) with the reply_markup argument

# Example usage of PromptsCompressor class
prompt_compressor = PromptsCompressor()
info_list = ["topic", "keyword1", "keyword2"]
prompt = prompt_compressor.get_prompt(info_list, 0)  # Get the prompt with index 0

response = "## This is a headline\n* Some text * \n```python\nprint('Hello!')\n```"
formatted_response = prompt_compressor.html_tags_insert(response) 
# Send the formatted_response using bot.send_message(...)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".