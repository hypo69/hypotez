# Cromicle Provider

## Overview

This module defines the `Cromicle` class, which is an asynchronous provider for the `hypotez` project. It provides a mechanism for interacting with the `cromicle.top` API to generate responses using various language models.

## Details

The `Cromicle` class inherits from the `AsyncGeneratorProvider` and provides a mechanism to interact with the `cromicle.top` API. It utilizes `aiohttp` for asynchronous HTTP requests and `hashlib` for message hashing to ensure security.

The class features a `create_async_generator` method, which takes a language model name, a list of messages, and optional proxy settings. This method constructs the necessary request payload, sends it to the API, and returns an asynchronous generator that yields the received response streams.

## Classes

### `Cromicle`

**Description**: This class provides a mechanism for interacting with the `cromicle.top` API to generate responses using various language models.

**Inherits**: `AsyncGeneratorProvider`

**Attributes**:

- `url` (str): The base URL of the `cromicle.top` API.
- `working` (bool): Indicates whether the provider is currently active.
- `supports_gpt_35_turbo` (bool): Indicates whether the provider supports the GPT-3.5 Turbo model.

**Methods**:

- `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`: This method creates an asynchronous generator that yields the responses received from the `cromicle.top` API.

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
                f'{cls.url}/chat',
                proxy=proxy,
                json=_create_payload(format_prompt(messages))
            ) as response:
                response.raise_for_status()
                async for stream in response.content.iter_any():
                    if stream:
                        yield stream.decode()
```

**Purpose**: This method creates an asynchronous generator that yields the responses received from the `cromicle.top` API.

**Parameters**:

- `model` (str): The name of the language model to use for response generation.
- `messages` (Messages): A list of messages representing the conversation history.
- `proxy` (str, optional): A proxy server URL to use for the request. Defaults to `None`.

**Returns**:

- `AsyncResult`: An asynchronous generator that yields the received response streams.

**Raises Exceptions**:

- `HTTPError`: If an HTTP error occurs during the request.

**How the Function Works**:

1. Creates an asynchronous `ClientSession` object with the specified headers.
2. Sends a POST request to the `cromicle.top` API with the formatted prompt and optional proxy settings.
3. Raises an `HTTPError` if the request fails.
4. Iterates over the response content stream using `iter_any()`.
5. Decodes the stream into a string and yields it to the caller.

**Examples**:

```python
    async def main():
        messages = [
            {'role': 'user', 'content': 'Hello, how are you?'},
            {'role': 'assistant', 'content': 'I am doing well, thank you.'},
        ]
        async for stream in Cromicle.create_async_generator(model='gpt-3.5-turbo', messages=messages):
            print(stream)

    if __name__ == "__main__":
        asyncio.run(main())
```

## Parameter Details

- `model` (str): The name of the language model to use for response generation.
- `messages` (Messages): A list of messages representing the conversation history.
- `proxy` (str, optional): A proxy server URL to use for the request. Defaults to `None`.


## Inner Functions

### `_create_header`

```python
def _create_header() -> Dict[str, str]:
    return {
        'accept': '*/*',
        'content-type': 'application/json',
    }
```

**Purpose**: This function creates a dictionary of headers for the HTTP request to the `cromicle.top` API.

**Parameters**: None

**Returns**:

- `Dict[str, str]`: A dictionary containing the request headers.

**How the Function Works**:

1. Creates a dictionary with two key-value pairs:
    - `accept`: `*/*` indicates that the client accepts any data type in the response.
    - `content-type`: `application/json` specifies that the request payload will be in JSON format.

**Examples**:

```python
    headers = _create_header()
    print(headers)  # Output: {'accept': '*/*', 'content-type': 'application/json'}
```

### `_create_payload`

```python
def _create_payload(message: str) -> Dict[str, str]:
    return {
        'message': message,
        'token': 'abc',
        'hash': sha256('abc'.encode() + message.encode()).hexdigest()
    }
```

**Purpose**: This function creates the JSON payload for the HTTP request to the `cromicle.top` API.

**Parameters**:

- `message` (str): The text message to be sent to the API.

**Returns**:

- `Dict[str, str]`: A dictionary representing the JSON payload.

**How the Function Works**:

1. Creates a dictionary with three key-value pairs:
    - `message`: The text message to be sent to the API.
    - `token`: A hardcoded token value (`'abc'`).
    - `hash`: A SHA-256 hash of the concatenated token and message, ensuring security.

**Examples**:

```python
    message = 'Hello, world!'
    payload = _create_payload(message)
    print(payload)  # Output: {'message': 'Hello, world!', 'token': 'abc', 'hash': ...}
```

This concludes the documentation for the `Cromicle` provider.