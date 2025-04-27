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
This code block defines a `_create_completion` function that interacts with the Caipacity API to generate text completions using the `gpt-3.5-turbo` model. It uses the `requests` library to send a POST request to the API, passing the user's message and other parameters as JSON data. The function also handles streaming responses, yielding individual tokens of the generated text as they become available.

Execution Steps
-------------------------
1. **Prepare Request Data**:
    - It constructs a JSON payload containing the desired model, temperature, stream flag, and the user's messages.
    - It generates a unique client ID using `uuid.uuid4()`.
    - It calculates a signature hash for the message content using the `Utils.hash` function.
2. **Send API Request**:
    - It creates a POST request to the Caipacity API endpoint `https://api.caipacity.com/v1/chat/completions`.
    - It includes necessary headers and parameters in the request.
3. **Process Streaming Response**:
    - It iterates over the lines of the streaming response.
    - It parses each line as JSON data and extracts the generated text token from the `delta` field.
    - It yields the token to the caller, allowing for real-time processing of the generated text.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.freegpt-webui-ru.g4f.Provider.Providers import Ails

# Example message history
messages = [
    {'role': 'user', 'content': 'Hello, how are you?'},
    {'role': 'assistant', 'content': 'I am doing well, thank you. How can I help you?'},
]

# Generate text completion with streaming enabled
for token in Ails._create_completion(model='gpt-3.5-turbo', messages=messages, stream=True):
    print(token, end='')
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".