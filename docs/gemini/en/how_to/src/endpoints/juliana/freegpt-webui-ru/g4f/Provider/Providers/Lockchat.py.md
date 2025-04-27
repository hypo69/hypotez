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
This code block implements a `Lockchat` provider for g4f, which allows users to interact with the Lockchat API for generating text completions using GPT models like `gpt-4` and `gpt-3.5-turbo`. 

Execution Steps
-------------------------
1. **Import Necessary Modules**: Imports `requests` for making HTTP requests, `os` for file path operations, `json` for working with JSON data, and `sha256` for cryptographic hashing from the `...typing` module.
2. **Define API Endpoint and Model Support**: Sets the base URL for the Lockchat API and defines the supported models.
3. **Configure Stream Support and Authentication**: Specifies that the provider supports streaming responses (`supports_stream`) and does not require authentication (`needs_auth`).
4. **Define `_create_completion` Function**: This function handles sending requests to the Lockchat API, processing the response, and yielding text tokens to the caller.
    - **Construct Payload**: Builds a JSON payload containing the model, messages, temperature, and stream flag.
    - **Send Request**: Sends a POST request to the Lockchat API endpoint with the payload and headers.
    - **Process Response**: Iterates over lines of the response, parsing JSON data and yielding content tokens.
5. **Handle Errors**: If the API response indicates a model error, the function attempts to retry the completion request.
6. **Define Parameter String**: Builds a string summarizing the supported parameters and their types for the `_create_completion` function.

Usage Example
-------------------------

```python
from g4f.Provider.Providers import Lockchat

# Initialize Lockchat provider
provider = Lockchat()

# Prepare messages for the API call
messages = [
    {"role": "user", "content": "Hello, how are you?"}
]

# Generate text completion using GPT-4
for token in provider.create_completion(model="gpt-4", messages=messages, stream=True):
    print(token, end="")
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".