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
The code block defines several utility functions for handling messages, prompts, and formatting. It includes functions for converting various data types to strings, formatting prompts, extracting system prompts and last user messages, handling image prompts, and trimming prompts to a maximum length. Additionally, it provides functions for generating random strings and hexadecimal values, filtering dictionary values, concatenating chunks of data, and formatting cookies. 

Execution Steps
-------------------------
1. **`to_string(value: Any) -> str`**: This function converts various data types to strings. It handles strings, dictionaries, lists, and other types, extracting relevant text content based on specific conditions.
2. **`format_prompt(messages: Messages, add_special_tokens: bool = False, do_continue: bool = False, include_system: bool = True) -> str`**: This function formats a series of messages into a single string, optionally adding special tokens. It iterates through messages, converting content to strings, and joins them with appropriate formatting.
3. **`get_system_prompt(messages: Messages) -> str`**: This function extracts the system prompt from a list of messages. It iterates through the messages, searching for messages with the "system" role and returns their concatenated content.
4. **`get_last_user_message(messages: Messages) -> str`**: This function extracts the last user message from a list of messages. It iterates through the messages, searching for the last message with the "user" role and returns its content.
5. **`format_image_prompt(messages, prompt: str = None) -> str`**: This function formats an image prompt based on a provided prompt or the last user message. It uses either the provided prompt or extracts the last user message as the image prompt.
6. **`format_prompt_max_length(messages: Messages, max_lenght: int) -> str`**: This function trims a prompt to a maximum length by selectively removing messages from the message list based on their role. It first tries removing all but the first three and last three messages, then all but the system messages and the last message, and finally uses only the last message if the prompt is still too long.
7. **`get_random_string(length: int = 10) -> str`**: This function generates a random string of a specified length, containing lowercase letters and digits. It randomly selects characters from the combined set of lowercase letters and digits for the specified length.
8. **`get_random_hex(length: int = 32) -> str`**: This function generates a random hexadecimal string of specified length. It randomly selects hexadecimal characters for the specified length.
9. **`filter_none(**kwargs: Any) -> dict`**: This function filters a dictionary to remove entries with `None` values. It iterates through the dictionary and returns a new dictionary with only the key-value pairs where the value is not `None`.
10. **`async_concat_chunks(chunks: AsyncIterator) -> str`**: This function asynchronously concatenates chunks of data from an asynchronous iterator. It iterates through the asynchronous iterator, collecting chunks and concatenating them.
11. **`concat_chunks(chunks: Iterator) -> str`**: This function concatenates chunks of data from an iterator. It iterates through the iterator, collecting chunks and concatenating them.
12. **`format_cookies(cookies: Cookies) -> str`**: This function formats a dictionary of cookies into a string suitable for setting cookies in a web browser. It iterates through the cookies dictionary and joins each key-value pair into a string separated by semicolons.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.providers.helper import format_prompt

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"},
    {"role": "assistant", "content": "Paris."}
]

prompt = format_prompt(messages)
print(prompt)

```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".