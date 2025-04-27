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
This code block defines a GetGPT class representing a provider for GPT models. The `_create_completion` function within the class handles generating responses from the GPT model using an encrypted API request.

Execution Steps
-------------------------
1. The `_create_completion` function is called with the model, messages, and stream parameters, along with optional kwargs like `frequency_penalty`, `max_tokens`, etc.
2. The `encrypt` function encrypts the data payload using AES encryption with a randomly generated key and IV.
3. The function constructs a JSON payload containing the messages, model name, and other parameters.
4. It sends a POST request to the GPT API endpoint (`https://chat.getgpt.world/api/chat/stream`) with the encrypted data.
5. The function iterates through the response stream and yields each chunk of generated text received from the GPT model.

Usage Example
-------------------------

```python
from g4f.Provider.Providers import GetGpt

# Initialize a GetGPT provider instance
gpt_provider = GetGpt()

# Generate a text completion using the GPT model
messages = [{"role": "user", "content": "Hello world!"}]
for response_chunk in gpt_provider._create_completion(model='gpt-3.5-turbo', messages=messages, stream=True):
    print(response_chunk)

```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".