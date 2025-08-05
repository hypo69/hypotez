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
This code block defines a `GigaChat` class that implements an asynchronous generator provider for GigaChat, a large language model powered by Sberbank. 

Execution Steps
-------------------------
1. **Imports:** The code imports necessary modules like `ssl` for secure communication, `time` for timing operations, `uuid` for generating unique identifiers, `Path` for working with file paths, `json` for JSON manipulation, `ClientSession` and `TCPConnector` from `aiohttp` for asynchronous HTTP requests, `raise_for_status` for handling HTTP errors, and other relevant modules.

2. **Global Variables:** It defines global variables `access_token` and `token_expires_at` to store the access token and its expiration time.

3. **Russian CA Certificate:**  It defines a constant `RUSSIAN_CA_CERT` which stores a Russian-trusted Root CA certificate used for verifying SSL connections.

4. **GigaChat Class:**  
    - **Inherits:** The class inherits from `AsyncGeneratorProvider` and `ProviderModelMixin` to provide asynchronous generator functionality and model management. 
    - **Attributes:** 
        - `url`: The base URL for GigaChat API.
        - `working`:  Indicates whether the provider is operational.
        - `supports_message_history`:  Indicates support for message history.
        - `supports_system_message`:  Indicates support for system messages.
        - `supports_stream`:  Indicates support for streaming responses.
        - `needs_auth`:  Indicates that authentication is required.
        - `default_model`: The default model to use.
        - `models`: A list of available GigaChat models.

5. **`create_async_generator` Class Method:** 
    - **Parameters:** 
        - `model`: The GigaChat model to use.
        - `messages`: A list of messages for the conversation.
        - `stream`: Whether to stream the response.
        - `proxy`:  Optional proxy server address.
        - `api_key`:  The API key for authentication.
        - `connector`: An optional `aiohttp` connector for customizing network connections.
        - `scope`: The API scope (e.g., `GIGACHAT_API_PERS`).
        - `update_interval`: The interval for checking for updates (in seconds).
    - **Functionality:** 
        - Retrieves the correct GigaChat model.
        - Raises an error if `api_key` is not provided.
        - Creates a certificate file (`russian_trusted_root_ca.crt`) in the cookies directory, writing the `RUSSIAN_CA_CERT` content. 
        - Uses `aiohttp` to create an asynchronous HTTP session, with an optional custom connector for proxy or SSL settings.
        - Checks if the access token is about to expire and refreshes it using the `api_key` if necessary.
        - Makes a POST request to the GigaChat API endpoint (`https://gigachat.devices.sberbank.ru/api/v1/chat/completions`) with the model, messages, and other parameters.
        - Handles the response, either yielding individual response chunks if `stream` is True, or returning the full response as a string if `stream` is False.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.GigaChat import GigaChat

async def main():
    # Get the GigaChat provider instance
    provider = GigaChat(api_key='YOUR_API_KEY')

    # Send a message to GigaChat
    messages = [
        {'role': 'user', 'content': 'Hello, GigaChat. How are you?'}
    ]
    async for response_chunk in provider.create_async_generator(model='GigaChat:latest', messages=messages):
        print(response_chunk)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".