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
This code block defines the `FreeGpt` class, which implements an asynchronous generator provider for the Free GPT API. It inherits from `AsyncGeneratorProvider` and `ProviderModelMixin` classes, providing functionality for generating text responses using the Free GPT API.

Execution Steps
-------------------------
1. **Initialization**: The `FreeGpt` class initializes the following attributes:
    - `url`: The base URL of the Free GPT API.
    - `working`: A boolean indicating whether the provider is currently working.
    - `supports_message_history`: A boolean indicating whether the provider supports message history.
    - `supports_system_message`: A boolean indicating whether the provider supports system messages.
    - `default_model`: The default model to use for text generation.
    - `models`: A list of supported models for text generation.
2. **`create_async_generator` method**: This method creates an asynchronous generator that iterates over the response chunks received from the Free GPT API.
    - It takes the `model`, `messages`, `proxy`, and `timeout` as arguments.
    - It extracts the last message from the `messages` list as the prompt.
    - It generates a timestamp and builds the request data using the `_build_request_data` method.
    - It selects a random domain from the `DOMAINS` list.
    - It initiates an asynchronous POST request to the Free GPT API using a `StreamSession` object.
    - It iterates over the response chunks, decodes them, and yields them to the caller.
    - It handles the `RATE_LIMIT_ERROR_MESSAGE` and raises a `RateLimitError` if the rate limit is exceeded.
3. **`_build_request_data` method**: This static method builds the request data to be sent to the Free GPT API.
    - It takes the `messages`, `prompt`, `timestamp`, and `secret` as arguments.
    - It constructs a dictionary containing the `messages`, `time`, `pass`, and `sign` fields.
    - It uses the `generate_signature` method to generate a signature for the request.
4. **`generate_signature` function**: This function generates a signature for the request data using a SHA256 hash function.
    - It takes the `timestamp`, `message`, and `secret` as arguments.
    - It concatenates these values and encodes them in UTF-8.
    - It computes the SHA256 hash of the encoded data and returns the hexadecimal representation of the hash.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.FreeGpt import FreeGpt
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

messages: Messages = [
    {"role": "user", "content": "Hello, how are you?"},
]

async def main():
    async for response_chunk in FreeGpt.create_async_generator(model="gemini-1.5-pro", messages=messages):
        print(response_chunk, end="")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".