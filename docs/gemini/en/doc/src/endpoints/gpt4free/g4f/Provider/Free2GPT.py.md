# Free2GPT Provider

## Overview

This module provides the `Free2GPT` class, a provider for utilizing the Free2GPT API for generating text using various language models.

## Details

The `Free2GPT` class inherits from `AsyncGeneratorProvider` and `ProviderModelMixin`, providing functionality for asynchronous generation of text using the Free2GPT API.

This provider offers the following features:

- Support for multiple language models, including Gemini-1.5-Pro and Gemini-1.5-Flash.
- Rate limiting handling to prevent exceeding API quotas.
- Asynchronous generation of text through a generator.
- Support for message history for conversational interactions.

## Classes

### `Free2GPT`

**Description**: Class for interacting with the Free2GPT API for text generation.

**Inherits**:
- `AsyncGeneratorProvider`: Provides functionality for asynchronous generation of text.
- `ProviderModelMixin`: Enables support for multiple language models.

**Attributes**:

- `url` (str): URL for the Free2GPT API endpoint.
- `working` (bool): Indicates if the provider is currently functional.
- `supports_message_history` (bool): Indicates if the provider supports message history.
- `default_model` (str): The default language model to be used.
- `models` (list): List of supported language models.

**Methods**:

- `create_async_generator(model: str, messages: Messages, proxy: str = None, connector: BaseConnector = None, **kwargs) -> AsyncResult`: Asynchronously generates text based on the provided model, messages, proxy, and connector.

**Parameters**:

- `model` (str): The language model to be used.
- `messages` (Messages): A list of messages to be sent to the API.
- `proxy` (str, optional): Proxy server address, defaults to `None`.
- `connector` (BaseConnector, optional): A custom connection object for aiohttp, defaults to `None`.

**Returns**:

- `AsyncResult`: An asynchronous result object containing the generated text.

**Raises**:

- `RateLimitError`: Raised when the API rate limit is exceeded.

**How the Class Works**:

The `Free2GPT` class utilizes the `aiohttp` library for making asynchronous requests to the Free2GPT API. It sends the provided messages, model, and other parameters to the `/api/generate` endpoint. The API returns a stream of text chunks that are yielded by the asynchronous generator. The class handles rate limiting by raising a `RateLimitError` if the API response indicates a quota exceedance.

## Functions

### `generate_signature(time: int, text: str, secret: str = "") -> str`

**Purpose**: Generates a SHA256 signature for a message based on the provided time, text, and secret key.

**Parameters**:

- `time` (int): Timestamp representing the time in milliseconds.
- `text` (str): The message to be signed.
- `secret` (str, optional): Secret key for signing the message, defaults to an empty string.

**Returns**:

- `str`: The SHA256 signature of the message.

**How the Function Works**:

The function combines the time, text, and secret key into a single string. This string is then encoded using UTF-8 and hashed using the SHA256 algorithm. The resulting hash is converted to a hexadecimal string and returned.

**Examples**:

```python
>>> generate_signature(1687084467000, "Hello, world!")
'47b35b0f99b1f570f3290818663f36709652854223e936267f680843a68d55e6'

>>> generate_signature(1687084467000, "Hello, world!", "my_secret")
'c8b9b2902d49e6210a43a7576e93a96a058652981c92a79c8ed3df69180475b6'
```

## Parameter Details

- `model` (str): Specifies the language model to be used. Supported models include `gemini-1.5-pro` and `gemini-1.5-flash`.

- `messages` (Messages): A list of messages to be sent to the API. Each message should be a dictionary with the following keys:

    - `role` (str): The role of the sender, either `user` or `assistant`.
    - `content` (str): The message content.

- `proxy` (str, optional): A string representing the proxy server address, defaults to `None`. 

- `connector` (BaseConnector, optional): A custom connection object for aiohttp, defaults to `None`.

## Examples

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.Free2GPT import Free2GPT
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Example usage with the default model:
provider = Free2GPT()
messages: Messages = [
    {"role": "user", "content": "Hello! How are you today?"},
]
async_result = await provider.create_async_generator(model=provider.default_model, messages=messages)
async for chunk in async_result:
    print(chunk, end="")

# Example usage with a specific model:
provider = Free2GPT()
messages: Messages = [
    {"role": "user", "content": "Write a poem about a cat."},
]
async_result = await provider.create_async_generator(model="gemini-1.5-flash", messages=messages)
async for chunk in async_result:
    print(chunk, end="")
```