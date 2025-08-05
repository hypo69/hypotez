# Ylokh Provider

## Overview

This module provides the `Ylokh` class, which implements the `AsyncGeneratorProvider` interface for interacting with the `Ylokh` API. This provider is deprecated and should not be used for new projects.

## Details

The `Ylokh` class inherits from the `AsyncGeneratorProvider` base class and provides functionality for sending messages to the `Ylokh` API and receiving responses. The `Ylokh` API allows you to interact with various language models, including GPT-3.5 Turbo. This class provides a simple interface for interacting with the API, enabling developers to use the service within their applications.

## Classes

### `Ylokh`

**Description**: This class implements the `AsyncGeneratorProvider` interface for interacting with the `Ylokh` API. 

**Inherits**: `AsyncGeneratorProvider`

**Attributes**:

- `url` (str): The base URL of the `Ylokh` API.
- `working` (bool): Indicates whether the provider is currently working.
- `supports_message_history` (bool):  Indicates if the API supports message history.
- `supports_gpt_35_turbo` (bool):  Indicates if the API supports GPT-3.5 Turbo model.

**Methods**:

- `create_async_generator(model: str, messages: Messages, stream: bool = True, proxy: str = None, timeout: int = 120, **kwargs) -> AsyncResult`: This method creates an asynchronous generator for streaming messages to the `Ylokh` API.

#### `create_async_generator(model: str, messages: Messages, stream: bool = True, proxy: str = None, timeout: int = 120, **kwargs) -> AsyncResult`

**Purpose**: This method creates an asynchronous generator to send messages to the `Ylokh` API and receive responses.

**Parameters**:

- `model` (str): The name of the language model to use. Defaults to `"gpt-3.5-turbo"`.
- `messages` (Messages): A list of messages to send to the API.
- `stream` (bool, optional): Indicates whether to stream the response. Defaults to `True`.
- `proxy` (str, optional):  The proxy server address for the request. Defaults to `None`.
- `timeout` (int, optional): The timeout for the request in seconds. Defaults to `120`.
- `**kwargs`: Additional keyword arguments to pass to the API.

**Returns**:

- `AsyncResult`: An asynchronous result object that represents the response from the API.

**How the Function Works**:

1. **Set up the request headers and data**: 
    - Sets the `Origin` and `Referer` headers for the request.
    - Creates a dictionary (`data`) containing the request parameters, including the list of `messages`, model name, and other optional parameters.

2. **Initiate the API request**:
    - Uses `StreamSession` to create a session with the specified headers and proxies.
    - Sends a POST request to the `Ylokh` API endpoint (`https://chatapi.ylokh.xyz/v1/chat/completions`) with the prepared `data`.

3. **Handle the response**:
    - Checks if the request was successful (status code 200) and raises an exception if not.
    - If `stream` is True, creates an asynchronous generator to stream the response:
        - Iterates over the response lines.
        - Extracts the `content` from the received JSON data.
        - Yields the `content` for each received line.
    - If `stream` is False, retrieves the entire response as JSON and yields the `content` from the response.

**Examples**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated import Ylokh
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Example 1: Send a message with GPT-3.5-turbo model and stream the response
messages: Messages = [{"role": "user", "content": "Hello, how are you?"}]
async for content in Ylokh.create_async_generator(messages=messages):
    print(content)

# Example 2: Send a message with a custom model and retrieve the entire response
messages: Messages = [{"role": "user", "content": "What is the meaning of life?"}]
response = await Ylokh.create_async_generator(messages=messages, model="my_custom_model", stream=False)
print(response)
```

## Parameter Details

- `model` (str): The name of the language model to use for generating responses. Defaults to "gpt-3.5-turbo". The API supports various models, including GPT-3.5-turbo.
- `messages` (Messages): A list of messages to send to the API for context. It is a list of dictionaries, where each dictionary represents a message with the following keys:
    - `role` (str): The role of the message sender (e.g., "user", "assistant").
    - `content` (str): The message content.
- `stream` (bool, optional): Indicates whether to stream the response or retrieve the entire response at once. If set to `True`, the function returns an asynchronous generator that yields response chunks as they are received from the API. If set to `False`, the function returns the entire response as a string. Defaults to `True`.
- `proxy` (str, optional):  The proxy server address to use for the request. Defaults to `None`.
- `timeout` (int, optional):  The timeout in seconds for the request. Defaults to `120`.
- `**kwargs`:  Additional keyword arguments to pass to the `Ylokh` API. These arguments may include parameters like `temperature`, `presence_penalty`, `top_p`, `frequency_penalty`, and `allow_fallback`.

## Examples

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated import Ylokh
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Example 1: Send a message with GPT-3.5-turbo model and stream the response
messages: Messages = [{"role": "user", "content": "Hello, how are you?"}]
async for content in Ylokh.create_async_generator(messages=messages):
    print(content)

# Example 2: Send a message with a custom model and retrieve the entire response
messages: Messages = [{"role": "user", "content": "What is the meaning of life?"}]
response = await Ylokh.create_async_generator(messages=messages, model="my_custom_model", stream=False)
print(response)
```