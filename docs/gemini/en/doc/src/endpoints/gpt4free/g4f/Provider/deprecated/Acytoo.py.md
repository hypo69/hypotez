# Acytoo Provider

## Overview

This module provides the `Acytoo` class, which implements an asynchronous generator provider for the Acytoo API. The provider allows interaction with the Acytoo chatbot using the `gpt-3.5-turbo` model.

## Details

This provider is designed to handle asynchronous requests to the Acytoo API for generating text. It uses an asynchronous generator to stream responses from the API, allowing for efficient handling of large responses. The module also includes helper functions for creating headers and payloads for API requests.

## Classes

### `class Acytoo`

**Description**: This class represents an asynchronous generator provider for the Acytoo API. It inherits from the `AsyncGeneratorProvider` base class.

**Inherits**: `AsyncGeneratorProvider`

**Attributes**:

* `url (str)`: The base URL for the Acytoo API.
* `working (bool)`: Indicates whether the provider is currently operational.
* `supports_message_history (bool)`: Indicates whether the provider supports message history.
* `supports_gpt_35_turbo (bool)`: Indicates whether the provider supports the `gpt-3.5-turbo` model.

**Methods**:

* `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`: This method creates an asynchronous generator for sending requests to the Acytoo API and receiving responses.

**How the Class Works**:

* The `create_async_generator` method initiates a POST request to the Acytoo API endpoint `/api/completions`. 
* It uses an asynchronous session to manage the request and response, handling the `Proxy` setting if provided.
* The request payload is constructed using the `_create_payload` function, which includes the model, messages, temperature, and other optional parameters.
* The response is streamed using an asynchronous generator, allowing for efficient handling of potentially large responses.

## Class Methods

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        **kwargs
    ) -> AsyncResult:
        async with ClientSession(
            headers=_create_header()
        ) as session:
            async with session.post(
                f'{cls.url}/api/completions',
                proxy=proxy,
                json=_create_payload(messages, **kwargs)
            ) as response:
                response.raise_for_status()
                async for stream in response.content.iter_any():
                    if stream:
                        yield stream.decode()
```

**Purpose**: This method creates an asynchronous generator for sending requests to the Acytoo API and receiving responses.

**Parameters**:

* `model (str)`: The model to use for generating text.
* `messages (Messages)`: A list of messages to be used as context for the generation.
* `proxy (str, optional)`: A proxy server to use for the request. Defaults to `None`.
* `**kwargs`: Optional keyword arguments for the API request.

**Returns**:

* `AsyncResult`: An asynchronous generator yielding decoded response streams.

**How the Function Works**:

1. It creates an asynchronous session with the specified headers.
2. It sends a POST request to the Acytoo API endpoint `/api/completions`.
3. The request includes the `proxy` if specified, and the payload is built using the `_create_payload` function.
4. The function checks the response status and raises an error if it is not successful.
5. It uses an asynchronous generator to iterate through response content chunks, decoding them and yielding them to the caller.

## Functions

### `_create_header`

```python
def _create_header():
    return {
        'accept': '*/*',
        'content-type': 'application/json',
    }
```

**Purpose**: This function creates a header dictionary for API requests to the Acytoo API.

**Returns**:

* `dict`: A dictionary containing the headers for the request.

**How the Function Works**:

This function defines a simple dictionary with two headers: `accept` and `content-type`. These headers are used to specify the acceptable data formats and the type of data being sent in the request.

### `_create_payload`

```python
def _create_payload(messages: Messages, temperature: float = 0.5, **kwargs):
    return {
        'key'         : '',
        'model'       : 'gpt-3.5-turbo',
        'messages'    : messages,
        'temperature' : temperature,
        'password'    : ''
    }
```

**Purpose**: This function creates a payload dictionary for API requests to the Acytoo API.

**Parameters**:

* `messages (Messages)`: A list of messages to be used as context for the generation.
* `temperature (float, optional)`: The temperature parameter for the model. Defaults to `0.5`.
* `**kwargs`: Optional keyword arguments for the API request.

**Returns**:

* `dict`: A dictionary containing the payload for the request.

**How the Function Works**:

This function constructs a payload dictionary for sending to the Acytoo API. It includes the following key-value pairs:

* `key`: An API key for authentication.
* `model`: The model to use for generating text.
* `messages`: A list of messages that provide context for the generation.
* `temperature`: A parameter controlling the creativity of the model's responses.
* `password`: A password for authentication.


## Example

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Acytoo import Acytoo

async def main():
    provider = Acytoo()
    messages = [
        {"role": "user", "content": "Hello, how are you?"},
    ]
    async for stream in provider.create_async_generator(model="gpt-3.5-turbo", messages=messages):
        print(stream)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

This example demonstrates how to use the `Acytoo` provider to send a request to the Acytoo API and retrieve the response. The example shows how to create a list of messages, pass them to the provider's `create_async_generator` method, and then process the streamed response.