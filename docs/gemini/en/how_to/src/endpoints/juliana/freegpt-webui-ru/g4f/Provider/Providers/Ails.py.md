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
This code block defines the `_create_completion` function, which sends a request to the `api.caipacity.com` endpoint to generate text completions using a language model. The function takes a model name, a list of messages, and optional parameters like temperature and stream.

Execution Steps
-------------------------
1. **Prepare Request Headers:** The code defines a dictionary of headers required for the API request, including authorization, client ID, and user agent.
2. **Prepare Request Parameters:** The code defines a dictionary of parameters for the API request, including "full" set to "false".
3. **Generate Timestamp:** The code generates a timestamp using the `Utils.format_timestamp` function.
4. **Create Signature:** The code generates a signature for the request using a secret key and a hash function.
5. **Format JSON Data:** The code formats a JSON object containing the request data, including the model, temperature, stream, messages, and signature.
6. **Send Request:** The code sends a POST request to the `api.caipacity.com/v1/chat/completions` endpoint using the `requests.post` function.
7. **Process Response:** The code iterates through the response lines, extracts the "content" part, and yields the text tokens to the user.

Usage Example
-------------------------

```python
    messages = [
        {'role': 'user', 'content': 'Hello, how are you?'},
    ]

    for token in _create_completion(model='gpt-3.5-turbo', messages=messages, stream=True):
        print(token, end='')
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".