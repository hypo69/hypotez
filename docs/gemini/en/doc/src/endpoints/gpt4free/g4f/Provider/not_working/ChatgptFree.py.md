# ChatgptFree Provider

## Overview

This module provides the `ChatgptFree` class, a provider for interacting with the ChatgptFree AI service. It enables users to send messages and receive responses from the ChatgptFree model.

## Details

The `ChatgptFree` provider implements a simple mechanism for interacting with ChatgptFree's API. It uses HTTP requests with specifically crafted data to send messages and receive responses. The responses are streamed and yielded as they arrive, ensuring a more efficient handling of long responses.

The provider is designed to be used asynchronously and relies on the `StreamSession` class from the `hypotez` project to manage HTTP requests.

## Classes

### `class ChatgptFree(AsyncGeneratorProvider, ProviderModelMixin)`

**Description**: This class represents a ChatgptFree provider and handles communication with the service.

**Inherits**: 
  - `AsyncGeneratorProvider`: Provides a base class for asynchronous providers that yield data.
  - `ProviderModelMixin`: Provides a base class for providers that support multiple models.

**Attributes**:

  - `url (str)`: The base URL for the ChatgptFree service.
  - `working (bool)`: Indicates whether the provider is currently working.
  - `_post_id (str)`: The post ID used in the ChatgptFree API request.
  - `_nonce (str)`: The nonce (a security token) used in the ChatgptFree API request.
  - `default_model (str)`: The default model used by the provider.
  - `models (List[str])`: A list of supported models.
  - `model_aliases (dict)`: A dictionary mapping model aliases to their actual names.

**Methods**:

  - `create_async_generator(model: str, messages: Messages, proxy: str = None, timeout: int = 120, cookies: dict = None, **kwargs) -> AsyncGenerator[str, None]`: Creates an asynchronous generator that yields responses from the ChatgptFree model.

**How the Class Works**:

1. **Initialization**: When instantiated, the `ChatgptFree` class sets the base URL, working status, and initializes the `_post_id` and `_nonce` attributes to `None`. It also defines default models and aliases.
2. **Asynchronous Generator**: The `create_async_generator` method is responsible for handling the interaction with the ChatgptFree API. It creates an asynchronous generator that yields responses from the model.
3. **Requesting Data**: The method uses a `StreamSession` to send a POST request to the ChatgptFree API endpoint. The request includes a formatted prompt, the `_nonce`, and the `_post_id`.
4. **Response Handling**: The method iterates over the streamed response lines. If a line starts with `data: `, it assumes it's a JSON response and attempts to decode it. If successful, it yields the content from the response. If the line is not a JSON response, it accumulates it in a buffer.
5. **Final Response**: The method processes the remaining buffer, attempting to decode it as a JSON response. If successful, it yields the decoded data.

**Examples**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.ChatgptFree import ChatgptFree
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Example 1: Sending a simple message to the default model
async def example_1():
    provider = ChatgptFree()
    messages = Messages(
        [
            {
                'role': 'user',
                'content': 'Hello, how are you?'
            }
        ]
    )
    async for response in provider.create_async_generator(model=provider.default_model, messages=messages):
        print(response)

# Example 2: Sending a message to a specific model
async def example_2():
    provider = ChatgptFree()
    messages = Messages(
        [
            {
                'role': 'user',
                'content': 'Translate this into French: "Hello, how are you?"'
            }
        ]
    )
    async for response in provider.create_async_generator(model='gpt-4o-mini-2024-07-18', messages=messages):
        print(response)

# Example 3: Using a proxy
async def example_3():
    provider = ChatgptFree()
    messages = Messages(
        [
            {
                'role': 'user',
                'content': 'What is the capital of France?'
            }
        ]
    )
    async for response in provider.create_async_generator(model=provider.default_model, messages=messages, proxy='http://your.proxy.server:port'):
        print(response)

# Run the examples (replace with your own async event loop)
asyncio.run(example_1())
asyncio.run(example_2())
asyncio.run(example_3())
```

## Class Methods

### `create_async_generator(model: str, messages: Messages, proxy: str = None, timeout: int = 120, cookies: dict = None, **kwargs) -> AsyncGenerator[str, None]`:

**Purpose**: Creates an asynchronous generator that yields responses from the ChatgptFree model.

**Parameters**:

  - `model (str)`: The model to use for generating responses.
  - `messages (Messages)`: A list of messages to send to the model.
  - `proxy (str, optional)`: A proxy server URL. Defaults to `None`.
  - `timeout (int, optional)`: The timeout for the request in seconds. Defaults to `120`.
  - `cookies (dict, optional)`: A dictionary of cookies to use for the request. Defaults to `None`.
  - `**kwargs`: Additional keyword arguments for the request.

**Returns**:

  - `AsyncGenerator[str, None]`: An asynchronous generator that yields responses from the model.

**Raises Exceptions**:

  - `RuntimeError`: If the post ID or nonce is not found in the initial response.

**How the Function Works**:

1. **Initial Setup**: The method sets up the necessary headers for the API request.
2. **Nonce and Post ID Retrieval**: If the `_nonce` and `_post_id` are not set, the method makes a GET request to the ChatgptFree service to retrieve them.
3. **Prompt Formatting**: The `messages` are formatted into a prompt suitable for the ChatgptFree API.
4. **API Request**: The method sends a POST request to the ChatgptFree API with the formatted prompt and the retrieved nonce and post ID.
5. **Response Processing**: The method iterates over the streamed response lines, processing them as JSON responses if available.
6. **Final Response**: The method processes the remaining buffer, attempting to decode it as a JSON response.


**Examples**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.ChatgptFree import ChatgptFree
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Example 1: Sending a simple message to the default model
async def example_1():
    provider = ChatgptFree()
    messages = Messages(
        [
            {
                'role': 'user',
                'content': 'Hello, how are you?'
            }
        ]
    )
    async for response in provider.create_async_generator(model=provider.default_model, messages=messages):
        print(response)

# Example 2: Sending a message to a specific model
async def example_2():
    provider = ChatgptFree()
    messages = Messages(
        [
            {
                'role': 'user',
                'content': 'Translate this into French: "Hello, how are you?"'
            }
        ]
    )
    async for response in provider.create_async_generator(model='gpt-4o-mini-2024-07-18', messages=messages):
        print(response)

# Example 3: Using a proxy
async def example_3():
    provider = ChatgptFree()
    messages = Messages(
        [
            {
                'role': 'user',
                'content': 'What is the capital of France?'
            }
        ]
    )
    async for response in provider.create_async_generator(model=provider.default_model, messages=messages, proxy='http://your.proxy.server:port'):
        print(response)

# Run the examples (replace with your own async event loop)
asyncio.run(example_1())
asyncio.run(example_2())
asyncio.run(example_3())
```

## Parameter Details

  - `model (str)`: The model to use for generating responses. It should be one of the models listed in the `models` attribute.
  - `messages (Messages)`: A list of messages to send to the model. Each message is represented as a dictionary with `role` and `content` keys.
  - `proxy (str, optional)`: A proxy server URL. Defaults to `None`.
  - `timeout (int, optional)`: The timeout for the request in seconds. Defaults to `120`.
  - `cookies (dict, optional)`: A dictionary of cookies to use for the request. Defaults to `None`.
  - `**kwargs`: Additional keyword arguments for the request.