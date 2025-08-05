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
This code defines the `Free2GPT` class, an implementation of an asynchronous generator provider for the `Free2GPT` API. It provides a `create_async_generator` method for generating text responses from the API based on user prompts. It handles rate limiting, generates a signature for authentication, and sends requests to the API, returning the responses as chunks of decoded text.

Execution Steps
-------------------------
1. The `create_async_generator` method receives input parameters such as the desired model, messages (including user prompts and previous responses), proxy settings, and a connector for the asynchronous session.
2. It constructs request headers with relevant information like user agent, accept type, and referer.
3. It establishes an asynchronous session using the provided connector and headers.
4. It prepares request data with the input messages, a timestamp, and a generated signature using the `generate_signature` method.
5. It sends a POST request to the Free2GPT API endpoint `/api/generate` with the prepared data.
6. It checks the response status code for potential errors, including rate limit exceeded.
7. If the request was successful, it iterates through the response content, yielding each chunk of decoded text, effectively streaming the response.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.Free2GPT import Free2GPT
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Example input messages
messages: Messages = [
    {"role": "user", "content": "Hello, how are you?"},
    {"role": "assistant", "content": "I am doing well, thanks for asking!"},
]

# Create a Free2GPT provider instance
provider = Free2GPT()

# Generate text response from the API
async for chunk in provider.create_async_generator(model="gemini-1.5-pro", messages=messages):
    print(chunk, end="")

```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".