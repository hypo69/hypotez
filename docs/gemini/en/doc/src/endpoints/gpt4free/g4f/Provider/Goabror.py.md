# Module `Goabror`

## Overview

The `Goabror` module is designed to interact with the `goabror.uz` service to generate text using a specified model. It inherits from `AsyncGeneratorProvider` and `ProviderModelMixin` and provides functionality to create an asynchronous generator that yields text responses from the API endpoint.

## More details

This module is used to communicate with the `goabror.uz` API, sending user prompts and system prompts to generate text. It handles both successful responses and errors, yielding the data or the full text response. The module also deals with potential JSON decoding errors, providing flexibility in handling different response formats.

## Classes

### `Goabror`

**Description**:
The `Goabror` class inherits from `AsyncGeneratorProvider` and `ProviderModelMixin`. It defines methods for interacting with the `goabror.uz` API to generate text based on provided messages.

**Inherits**:
- `AsyncGeneratorProvider`: Provides asynchronous generator capabilities.
- `ProviderModelMixin`: Mixin providing model-related functionalities.

**Attributes**:
- `url` (str): The base URL for the `goabror.uz` website.
- `api_endpoint` (str): The API endpoint for generating text.
- `working` (bool): Indicates whether the provider is working (set to `True`).
- `default_model` (str): The default model to use (`gpt-4`).
- `models` (list): A list of available models (currently only `default_model`).

**Methods**:
- `create_async_generator`: Creates an asynchronous generator that yields text responses from the API.

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
    """ Создает асинхронный генератор, который выдает текстовые ответы от API.

    Args:
        cls (Goabror): Класс `Goabror`.
        model (str): Название модели, используемой для генерации текста.
        messages (Messages): Список сообщений, используемых для генерации запроса.
        proxy (str, optional): Прокси-сервер для использования при подключении к API. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий текстовые ответы.

    Raises:
        Exception: Если возникает ошибка при выполнении запроса к API.

    """
```

**Parameters**:
- `cls` (Goabror): The `Goabror` class.
- `model` (str): The model name to use for generating text.
- `messages` (Messages): A list of messages used for generating the request.
- `proxy` (str, optional): Proxy server to use when connecting to the API. Defaults to `None`.
- `**kwargs`: Additional keyword arguments.

**Returns**:
- `AsyncResult`: An asynchronous generator that yields text responses.

**How the function works**:
1. Defines the necessary headers for the HTTP request.
2. Creates an `aiohttp.ClientSession` with the defined headers.
3. Formats the user and system prompts from the input messages.
4. Sends a GET request to the API endpoint with the formatted prompts and proxy (if provided).
5. Raises an exception if the response status indicates an error.
6. Reads the text from the response.
7. Tries to decode the text as JSON. If successful and the JSON contains a "data" field, yields the content of the field. Otherwise, yields the entire text response.
8. If JSON decoding fails, yields the original text response.

**Examples**:
```python
# Пример использования асинхронного генератора
async for message in Goabror.create_async_generator(model='gpt-4', messages=[{'role': 'user', 'content': 'Hello'}], proxy='http://proxy.example.com'):
    print(message)