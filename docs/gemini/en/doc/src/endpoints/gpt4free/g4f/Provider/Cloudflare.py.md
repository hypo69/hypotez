# Cloudflare AI Endpoint Provider

## Overview

This module defines the `Cloudflare` class, an endpoint provider for accessing the Cloudflare AI playground API. It inherits from `AsyncGeneratorProvider`, `ProviderModelMixin`, and `AuthFileMixin`, enabling asynchronous interaction with the Cloudflare AI service.

## Details

The Cloudflare provider utilizes a stream-based approach for interacting with the Cloudflare AI API. It supports various features, including streaming responses, system messages, and message history. The provider caches API credentials and cookies for improved efficiency.

## Classes

### `Cloudflare`

**Description**: This class implements an asynchronous provider for interacting with the Cloudflare AI API.

**Inherits**:
- `AsyncGeneratorProvider`: Enables asynchronous stream-based interaction with the Cloudflare AI API.
- `ProviderModelMixin`: Provides methods for handling and managing models.
- `AuthFileMixin`: Handles authentication and authorization with Cloudflare AI.

**Attributes**:
- `label` (str): The display name of the provider ("Cloudflare AI").
- `url` (str): The base URL of the Cloudflare AI playground.
- `working` (bool): Indicates whether the provider is currently operational.
- `use_nodriver` (bool): Flag to determine if the provider requires a headless browser (NoDriver).
- `api_endpoint` (str): The API endpoint for inference requests.
- `models_url` (str): The URL for retrieving available models.
- `supports_stream` (bool): Indicates support for streaming responses.
- `supports_system_message` (bool): Indicates support for system messages.
- `supports_message_history` (bool): Indicates support for message history.
- `default_model` (str): The default model used for requests.
- `model_aliases` (dict): A mapping of model aliases to their actual names.
- `_args` (dict): A dictionary to store request arguments, including headers and cookies.

**Methods**:
- `get_models()`: Fetches the list of available models from Cloudflare AI.
- `create_async_generator()`: Creates an asynchronous generator to handle streaming responses from the Cloudflare AI API.

## Functions

### `get_models()`

**Purpose**: Retrieves a list of available models from the Cloudflare AI service.

**Parameters**: None.

**Returns**:
- `list`: A list of model names supported by Cloudflare AI.

**Raises Exceptions**:
- `ResponseStatusError`: If there's an error retrieving the model list from Cloudflare AI.

**How the Function Works**:
- If the model list is not already cached, the function fetches it from the Cloudflare AI API using a `Session` object.
- It retrieves the model list from the `models_url` endpoint and parses the JSON response.
- The extracted model names are stored in the `models` attribute and returned as a list.

**Examples**:
```python
>>> Cloudflare.get_models()
['@cf/meta/llama-2-7b-chat-fp16', '@cf/meta/llama-2-7b-chat-int8', ...]
```

### `create_async_generator()`

**Purpose**: Creates an asynchronous generator to handle streaming responses from the Cloudflare AI API.

**Parameters**:
- `model` (str): The name of the model to use for inference.
- `messages` (list): A list of messages (including system messages, if supported) for the conversation.
- `proxy` (str, optional): A proxy server address to use for requests. Defaults to `None`.
- `max_tokens` (int, optional): The maximum number of tokens allowed in the response. Defaults to `2048`.
- `cookies` (dict, optional): A dictionary of cookies to send with requests. Defaults to `None`.
- `timeout` (int, optional): The request timeout in seconds. Defaults to `300`.

**Returns**:
- `AsyncResult`: An asynchronous result object that yields responses, usage information, and finish reason.

**Raises Exceptions**:
- `ResponseStatusError`: If there's an error sending the inference request or receiving the response.

**How the Function Works**:
- The function constructs a request payload containing the conversation messages, model name, maximum tokens, stream flag, system message, and tools (if applicable).
- It sends the request to the Cloudflare AI API endpoint using a `StreamSession` object, which handles streaming responses.
- The generator iterates over the response lines and yields the following:
    - JSON-decoded response data for each line starting with `'0:'`.
    - Usage information for the request, including the number of tokens used.
    - The finish reason indicating why the generation ended.

**Examples**:
```python
>>> async def main():
...     messages = [{"role": "user", "content": "Hello, how are you?"}]
...     async for response in Cloudflare.create_async_generator(model="llama-2-7b", messages=messages):
...         print(response)
...
>>> asyncio.run(main())
{'content': 'I am doing well, thank you for asking! How are you today?', 'parts': [{'type': 'text', 'text': 'I am doing well, thank you for asking! How are you today?'}]}
```

## Parameter Details

- `model` (str): The name of the model to use for inference. Must be one of the supported models listed in `Cloudflare.get_models()`.
- `messages` (list): A list of messages (including system messages, if supported) for the conversation. Each message is a dictionary with `role` (e.g., "user", "assistant"), `content` (the message text), and potentially other keys based on the model's requirements.
- `proxy` (str, optional): A proxy server address to use for requests. Defaults to `None`.
- `max_tokens` (int, optional): The maximum number of tokens allowed in the response. Defaults to `2048`.
- `cookies` (dict, optional): A dictionary of cookies to send with requests. Defaults to `None`.
- `timeout` (int, optional): The request timeout in seconds. Defaults to `300`.

## Examples

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.Cloudflare import Cloudflare
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Get available models
models = Cloudflare.get_models()
print(models)

# Define conversation messages
messages: Messages = [
    {"role": "user", "content": "Hello, how are you?"},
    {"role": "assistant", "content": "I am doing well, thank you for asking! How are you today?"},
]

# Send a request using the default model
async def main():
    async for response in Cloudflare.create_async_generator(messages=messages):
        print(response)

asyncio.run(main())
```