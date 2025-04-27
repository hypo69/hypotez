# Module: Opchatgpts

## Overview

This module provides an implementation of the `Opchatgpts` class, which is a subclass of `AsyncGeneratorProvider`. This class utilizes the `opchatgpts.net` API to interact with GPT-3.5 Turbo and obtain responses through an asynchronous generator.

## Details

The `Opchatgpts` class leverages the `opchatgpts.net` API for GPT-3.5 Turbo interactions. The class is designed to support message history and utilize an asynchronous generator for efficient response generation.

## Classes

### `class Opchatgpts(AsyncGeneratorProvider)`

**Description**: The `Opchatgpts` class utilizes the `opchatgpts.net` API to interact with GPT-3.5 Turbo. It inherits from the `AsyncGeneratorProvider` class and provides functionality for asynchronous response generation.

**Inherits**: `AsyncGeneratorProvider`

**Attributes**:

- `url (str)`: The base URL for the `opchatgpts.net` API.
- `working (bool)`: Indicates whether the provider is currently working.
- `supports_message_history (bool)`: Indicates whether the provider supports message history.
- `supports_gpt_35_turbo (bool)`: Indicates whether the provider supports GPT-3.5 Turbo.

**Methods**:

- `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`: This method asynchronously generates responses from the GPT-3.5 Turbo model. It takes the model name, messages, and optional proxy information as input.

## Class Methods

### `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`

**Purpose**: This method asynchronously generates responses from the GPT-3.5 Turbo model. It establishes a connection with the `opchatgpts.net` API and handles the communication to obtain the desired response.

**Parameters**:

- `model (str)`: The name of the GPT-3.5 Turbo model to utilize for response generation.
- `messages (Messages)`: A list of messages, including the user's prompt and previous interactions, to be sent to the model.
- `proxy (str, optional)`: A proxy server address for accessing the API. Defaults to `None`.

**Returns**:

- `AsyncResult`: An asynchronous result object representing the generated response.

**Raises Exceptions**:

- `RuntimeError`: If the response from the API is malformed or invalid.

**How the Function Works**:

1. Sets up a connection with the `opchatgpts.net` API using `aiohttp`.
2. Creates a dictionary `data` with essential information, including the `botId`, `chatId`, `contextId`, `customId`, `messages`, `newMessage`, `session`, and `stream`.
3. Sends a POST request to the API endpoint `/wp-json/mwai-ui/v1/chats/submit` with the `data` and optional `proxy` parameters.
4. Iterates through the response content and parses the received lines.
5. If the line indicates a "live" response, the `data` from the line is yielded.
6. If the line indicates an "end" response, the generator loop breaks.
7. The generated response is returned as an asynchronous result object.

**Examples**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated import Opchatgpts

# Example usage with a simple prompt
messages = [
    {"role": "user", "content": "Hello, how are you?"}
]
async_result = await Opchatgpts.create_async_generator(model='gpt-3.5-turbo', messages=messages)
response = await async_result

# Access the response content
print(response)

# Example usage with a more complex prompt and a proxy
messages = [
    {"role": "user", "content": "Can you write a short story about a cat named Whiskers?"}
]
proxy = 'http://proxy_server:port'
async_result = await Opchatgpts.create_async_generator(model='gpt-3.5-turbo', messages=messages, proxy=proxy)
response = await async_result

# Access the response content
print(response)
```