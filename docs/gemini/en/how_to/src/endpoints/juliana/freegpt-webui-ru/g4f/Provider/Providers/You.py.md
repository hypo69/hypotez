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
The code block defines a function `_create_completion` which is responsible for sending a request to the You.com API to generate text completion based on the provided `messages` and model. The function supports streaming responses and does not require authentication.

Execution Steps
-------------------------
1. The code block defines several variables:
    - `url`: The base URL for the You.com API.
    - `model`: The specific model to use for text completion (e.g., 'gpt-3.5-turbo').
    - `supports_stream`: Indicates whether the API supports streaming responses (True in this case).
    - `needs_auth`: Indicates whether the API requires authentication (False in this case).
2. The `_create_completion` function takes the following arguments:
    - `model`: The model to use for text completion.
    - `messages`: A list of messages to use as context for text generation.
    - `stream`: A boolean flag indicating whether to stream the response.
3. The function then constructs a command to execute a Python script (`helpers/you.py`) located in the same directory as the current file.
4. The command is executed using the `subprocess.Popen` function, which captures both standard output and error streams.
5. The code iterates over each line of the output stream and yields it as a decoded string.

Usage Example
-------------------------

```python
    messages = [
        {"role": "user", "content": "Hello, how are you?"},
    ]
    
    for response_line in _create_completion(model="gpt-3.5-turbo", messages=messages, stream=True):
        print(response_line)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".