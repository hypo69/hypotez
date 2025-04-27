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
This code snippet defines a Forefront.com provider for the g4f framework. It includes a function `_create_completion` which constructs and sends a completion request to Forefront.com's API, leveraging stream-based responses for real-time feedback. 

Execution Steps
-------------------------
1. **Import Libraries**: Import necessary modules like `os`, `json`, `requests`, and the type hinting functionality.
2. **Define Provider Information**:  Set up the provider's base URL (`url`), supported models (`model`), stream capability (`supports_stream`), and authentication requirement (`needs_auth`).
3. **`_create_completion` Function**: This function takes the model name, a list of messages, and a stream flag as input.
    - **Prepare JSON Payload**: Construct a JSON payload containing the message content, action, and other required information.
    - **Send Request**: Make a POST request to the Forefront API endpoint with the prepared JSON data.
    - **Process Stream**: Iterate through the stream response and yield each token received from the API.
4. **Parameter Information**: The code uses `get_type_hints` to dynamically document the parameter types for `_create_completion` and displays them in a formatted string.

Usage Example
-------------------------

```python
from g4f.Provider.Providers import Forefront

# Instantiate the Forefront provider
forefront_provider = Forefront.Forefront()

# Prepare a list of messages
messages = [
    {"role": "user", "content": "Hello! How are you?"},
    {"role": "assistant", "content": "I am doing well, thanks for asking!"},
]

# Get a completion response with streaming
for token in forefront_provider._create_completion(model='gpt-4', messages=messages, stream=True):
    print(token)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".