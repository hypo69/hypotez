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
The code block implements a `LocalProvider` class responsible for generating text completions using the `GPT4All` library. It searches for a specified model file, downloads it if necessary, loads the model, and then generates text based on provided messages and a prompt template.

Execution Steps
-------------------------
1. **Find Model Directory**: The `find_model_dir` function searches for a specified model file in the project's `models` directory.
2. **Load Model**: The `create_completion` method loads the specified model from the found directory using the `GPT4All` library. If the model file is not found, the code prompts the user to download it.
3. **Generate Text**: The code generates text based on the provided `messages` and a prompt template using the `model.generate` function. If `stream` is True, the code generates the text incrementally.
4. **Format Prompt**: The code constructs a prompt by concatenating messages based on their roles ("system", "user", or "assistant").

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.locals.provider import LocalProvider

# Define messages for the chatbot conversation
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"},
]

# Create a local provider instance
provider = LocalProvider()

# Generate completion using the 'gpt4all-lora-13b' model
completion = provider.create_completion(model='gpt4all-lora-13b', messages=messages)

# Print the generated response
print(completion)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".