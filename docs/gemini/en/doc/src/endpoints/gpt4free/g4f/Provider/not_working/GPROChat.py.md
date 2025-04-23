# Module for interacting with the GPROChat service

## Overview

The module defines the `GPROChat` class, which allows interaction with the GPROChat service for generating text. The module supports asynchronous operation, message history, and streaming responses.

## More details

The `GPROChat` class is an asynchronous generator provider, meaning it can generate text in chunks asynchronously. It uses the `aiohttp` library to make HTTP requests to the GPROChat API. The module also includes functions for generating signatures to authenticate requests. The class determines which model to use (default is `gemini-1.5-pro`).

## Classes

### `GPROChat`

**Description**: Class for interacting with the GPROChat service.

**Inherits**: `AsyncGeneratorProvider`, `ProviderModelMixin`

**Attributes**:

- `url` (str): The base URL of the GPROChat service ("https://gprochat.com").
- `api_endpoint` (str): The API endpoint for generating text ("https://gprochat.com/api/generate").
- `working` (bool): A flag indicating whether the service is currently working (`False`).
- `supports_stream` (bool): A flag indicating whether the service supports streaming responses (`True`).
- `supports_message_history` (bool): A flag indicating whether the service supports message history (`True`).
- `default_model` (str): The default model to use if none is specified (`'gemini-1.5-pro'`).

**Working principle**:

The `GPROChat` class inherits from `AsyncGeneratorProvider` and `ProviderModelMixin`. It defines static methods for generating request signatures and creating asynchronous generators for interacting with the GPROChat API. The class uses `aiohttp.ClientSession` to send asynchronous POST requests to the API endpoint. The responses are streamed and yielded in chunks.

## Class Methods

### `generate_signature`

```python
@staticmethod
def generate_signature(timestamp: int, message: str) -> str:
    """Генерирует подпись для запроса к API GPROChat.

    Args:
        timestamp (int): Временная метка в миллисекундах.
        message (str): Сообщение, для которого генерируется подпись.

    Returns:
        str: Подпись, сгенерированная на основе временной метки и сообщения.
    """
```

**Purpose**: Generates a signature for the GPROChat API request using a timestamp, message, and secret key.

**Parameters**:

- `timestamp` (int): The timestamp in milliseconds.
- `message` (str): The message for which the signature is generated.

**Returns**:

- `str`: The generated signature.

**How the function works**:

The function calculates the SHA256 hash of the concatenated string of timestamp, message, and a secret key. The resulting hash is returned as the signature.

**Examples**:

```python
timestamp = int(time.time() * 1000)
message = "Test message"
signature = GPROChat.generate_signature(timestamp, message)
print(signature)
```

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
    """Создает асинхронный генератор для взаимодействия с API GPROChat.

    Args:
        model (str): Имя модели для использования.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): URL прокси-сервера. Defaults to `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий ответы от API.
    """
```

**Purpose**: Creates an asynchronous generator for interacting with the GPROChat API.

**Parameters**:

- `cls`: The class object.
- `model` (str): The name of the model to use.
- `messages` (Messages): The list of messages to send.
- `proxy` (str, optional): The proxy server URL. Defaults to `None`.
- `**kwargs`: Additional arguments.

**Returns**:

- `AsyncResult`: An asynchronous generator that yields responses from the API.

**How the function works**:

The function prepares the request headers and data, including the timestamp and signature. It then uses `aiohttp.ClientSession` to send an asynchronous POST request to the API endpoint. The responses are streamed and yielded in chunks.

**Examples**:

```python
messages = [{"role": "user", "content": "Hello, GPROChat!"}]
async def generate_response():
    async for chunk in GPROChat.create_async_generator(model='gemini-1.5-pro', messages=messages):
        print(chunk, end="")

import asyncio
asyncio.run(generate_response())
```

## Class Parameters

- `url` (str): The base URL of the GPROChat service.
- `api_endpoint` (str): The API endpoint for generating text.
- `working` (bool): A flag indicating whether the service is currently working.
- `supports_stream` (bool): A flag indicating whether the service supports streaming responses.
- `supports_message_history` (bool): A flag indicating whether the service supports message history.
- `default_model` (str): The default model to use if none is specified.