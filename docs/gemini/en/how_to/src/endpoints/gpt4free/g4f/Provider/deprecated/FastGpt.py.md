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
The `FastGpt` class implements an API provider that interacts with `fastgpt.me` to generate text completions. It supports streaming responses and can be used to create completions using different models.

Execution Steps
-------------------------
1. **Initialize a FastGpt object:** Create an instance of the `FastGpt` class.
2. **Call `create_completion`:** Pass the desired model name, messages, and optional arguments to generate a completion. 
3. **Iterate over the response:** The `create_completion` method returns a generator that yields individual tokens of the completion. Iterate over the generator to retrieve the completed text.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.FastGpt import FastGpt

# Initialize the provider
gpt_provider = FastGpt()

# Example message history
messages = [
    {"role": "user", "content": "Hello, how are you?"},
    {"role": "assistant", "content": "I am doing well, thank you. How are you?"}
]

# Generate a completion with streaming enabled
for token in gpt_provider.create_completion(model="text-davinci-003", messages=messages, stream=True):
    print(token, end="")

# Print the full completion
completion = "".join(gpt_provider.create_completion(model="text-davinci-003", messages=messages, stream=False))
print(completion)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".