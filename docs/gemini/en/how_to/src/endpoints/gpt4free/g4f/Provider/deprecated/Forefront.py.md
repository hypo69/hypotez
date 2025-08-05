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
The code defines a `Forefront` class that inherits from `AbstractProvider`, representing a GPT-4-like language model provider. It implements the `create_completion` method to generate text completions using the Forefront API. 

Execution Steps
-------------------------
1. The `create_completion` method receives the desired model, a list of messages (including the user's prompt), a flag indicating if streaming is enabled, and optional keyword arguments.
2. It constructs a JSON payload (`json_data`) containing the user's message, model, and other configuration settings.
3. It sends a POST request to the Forefront API endpoint (`https://streaming.tenant-forefront-default.knative.chi.coreweave.com/free-chat`) with the JSON payload and enables streaming if requested.
4. The method iterates over the streaming response, extracting completion tokens from each line containing `delta`. It yields each extracted token to the caller, enabling real-time display of the generated text.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Forefront import Forefront

# Initialize the provider
provider = Forefront()

# Prepare a list of messages
messages = [
    {"role": "user", "content": "Hello, how are you?"},
]

# Generate the completion using streaming
for token in provider.create_completion(model="gpt-4", messages=messages, stream=True):
    print(token, end="")
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".