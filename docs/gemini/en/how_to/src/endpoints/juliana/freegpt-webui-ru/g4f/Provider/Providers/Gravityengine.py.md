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
This code block defines a provider for Gravityengine. It includes details about the provider's API URL, supported models, streaming capability, and authentication requirements. It then defines a function for generating chat completions, which sends a request to the Gravityengine API.

Execution Steps
-------------------------
1. The code defines variables for the API URL (`url`), supported models (`model`), streaming support (`supports_stream`), and authentication requirements (`needs_auth`).
2. The `_create_completion` function accepts a model name, a list of messages, a boolean indicating streaming support, and keyword arguments.
3. The function constructs a request body with the model name, temperature, presence penalty, and messages.
4. It sends a POST request to the Gravityengine API endpoint `/api/openai/v1/chat/completions` using the `requests` library.
5. The function yields the content of the returned message from the API response.
6. It generates a string describing the provider's supported parameters and their types.

Usage Example
-------------------------

```python
from g4f.Provider.Providers import Gravityengine

# Initialize Gravityengine provider
provider = Gravityengine.Gravityengine()

# Send a request to generate a chat completion
messages = [
    {"role": "user", "content": "Hello, how are you?"},
]
completion = provider.create_completion(model="gpt-3.5-turbo-16k", messages=messages, stream=True)

# Print the generated response
for chunk in completion:
    print(chunk)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".