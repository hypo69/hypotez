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
This code block defines a class for a Lockchat provider within a GPT-4 model service. It handles interacting with the Lockchat API for generating completions.

Execution Steps
-------------------------
1. **Imports**: Necessary libraries are imported for making HTTP requests (requests), working with file paths (os), handling JSON data (json), and type checking (typing).
2. **Configuration**: API URL, supported models, and other parameters are defined.
3. **Define the `_create_completion` Function**:
    - Takes model, messages, stream flag, temperature, and optional keyword arguments.
    - Creates a payload with request details.
    - Makes a POST request to the Lockchat API with the payload.
    - Iterates through response lines, checks for error messages and yields content tokens.
4. **Parameter Description**: A string is constructed to describe the function's parameters and their expected types.

Usage Example
-------------------------

```python
from g4f.Provider.Providers import Lockchat

provider = Lockchat()

messages = [
    {"role": "user", "content": "Hello, how are you?"},
]

completion = provider._create_completion(
    model="gpt-4",
    messages=messages,
    stream=True,
)

for token in completion:
    print(token, end="")

```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".