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
The code defines a Forefront provider for the g4f.Provider.Providers module. It uses a Forefront API endpoint to generate responses.

Execution Steps
-------------------------
1. **Imports and Constants**: Imports necessary modules and defines constants for the Forefront API endpoint, model, and support information.
2. **_create_completion Function**:
    - **Defines the `_create_completion` function**: This function takes a model, messages, and stream flag as input. It prepares a JSON payload with messages and sends it to the Forefront API endpoint. 
    - **Handles Streaming Responses**:  It iterates over the streamed response and yields each token for the chat interface.
3. **Parameter Display**: Defines a string `params` to display the supported parameters and their types for the Forefront provider.

Usage Example
-------------------------

```python
from g4f.Provider.Providers import Forefront

# Create a Forefront provider instance
forefront_provider = Forefront.Forefront()

# Define messages for the chat
messages = [
    {'role': 'user', 'content': 'Hello, how are you?'},
]

# Generate a completion using the Forefront provider
completion = forefront_provider.create_completion(model='gpt-3.5-turbo', messages=messages, stream=True)

# Print each token from the completion
for token in completion:
    print(token)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".