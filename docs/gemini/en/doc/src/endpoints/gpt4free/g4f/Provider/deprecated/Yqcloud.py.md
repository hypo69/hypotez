# Yqcloud Provider

## Overview

This module provides the `Yqcloud` class, an asynchronous generator provider for interacting with the Yqcloud GPT4Free API. It leverages the `StreamSession` class from the `hypotez` project to establish an asynchronous HTTP connection and stream responses from the Yqcloud API.

## Details

The `Yqcloud` class is a subclass of `AsyncGeneratorProvider`, which is a base class in the `hypotez` project for handling asynchronous interactions with different AI model providers. The `Yqcloud` class implements the `create_async_generator` method, which is responsible for establishing the connection, sending the prompt, and streaming the response from the Yqcloud API. 

The `_create_header` and `_create_payload` functions provide helper utilities for constructing the HTTP headers and request payload required by the Yqcloud API.

## Classes

### `class Yqcloud(AsyncGeneratorProvider)`

**Description**: An asynchronous generator provider for interacting with the Yqcloud GPT4Free API.

**Inherits**: `AsyncGeneratorProvider`

**Attributes**:

- `url` (str): The base URL of the Yqcloud API.
- `working` (bool): Indicates whether the provider is currently working.
- `supports_gpt_35_turbo` (bool): Indicates whether the provider supports the GPT-3.5 Turbo model.

**Methods**:

- `create_async_generator(model: str, messages: Messages, proxy: str = None, timeout: int = 120, **kwargs) -> AsyncResult`: Asynchronously establishes a connection with the Yqcloud API, sends the prompt, and streams the response as a generator.

### Inner Functions

#### `_create_header()`

**Purpose**: Creates and returns a dictionary of HTTP headers for requests to the Yqcloud API.

**Parameters**: None

**Returns**:

- `dict`: A dictionary containing the HTTP headers.

#### `_create_payload(messages: Messages, system_message: str = "", user_id: int = None, **kwargs)`

**Purpose**: Creates and returns a JSON payload for requests to the Yqcloud API.

**Parameters**:

- `messages` (Messages): A list of messages in the conversation.
- `system_message` (str): A system message to be included in the prompt. Defaults to an empty string.
- `user_id` (int): A unique user ID. If not provided, a random ID will be generated.
- `**kwargs`: Additional keyword arguments to be included in the payload.

**Returns**:

- `dict`: A JSON payload containing the prompt, system message, and other parameters.

## Examples

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Yqcloud import Yqcloud
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Create a list of messages for the conversation
messages = Messages(
    [
        {
            "role": "user",
            "content": "Hello, world!",
        }
    ]
)

# Create an instance of the Yqcloud provider
yqcloud_provider = Yqcloud()

# Asynchronously generate responses from the Yqcloud API
async for chunk in yqcloud_provider.create_async_generator(
    model="gpt-3.5-turbo", messages=messages
):
    print(chunk)
```