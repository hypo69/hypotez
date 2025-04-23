# Module for interacting with the AI365VIP provider

## Overview

This module implements the `AI365VIP` class, which is used to interact with the AI365VIP provider's API. It supports models such as `gpt-3.5-turbo` and `gpt-4o`. The module is designed to asynchronously generate responses from the AI365VIP API based on provided messages.

## More details

This module facilitates communication with the AI365VIP service, providing an interface for sending messages to the AI model and receiving responses. It is used to asynchronously generate responses from the AI365VIP API based on provided messages.
The module uses `aiohttp` for asynchronous HTTP requests and includes functionality for formatting prompts and handling API responses.

## Classes

### `AI365VIP`

**Description**: Class for interacting with the AI365VIP provider.

**Inherits**:
- `AsyncGeneratorProvider`: Provides an asynchronous generator interface.
- `ProviderModelMixin`: Provides model-related functionalities.

**Attributes**:
- `url` (str): The base URL of the AI365VIP service.
- `api_endpoint` (str): The API endpoint for chat requests.
- `working` (bool): Indicates whether the provider is working.
- `default_model` (str): The default model to use if none is specified.
- `models` (list): A list of supported models.
- `model_aliases` (dict): Aliases for model names.

**Working principle**:
The class defines methods for asynchronously generating responses from the AI365VIP API. It formats the messages into a prompt, sends it to the API, and yields the responses as they are received.

**Methods**:
- `create_async_generator`: Creates an asynchronous generator for streaming responses from the AI365VIP API.

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
    """ Создает асинхронный генератор для получения ответов от API AI365VIP.

    Args:
        cls (AI365VIP): Класс AI365VIP.
        model (str): Имя используемой модели.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий ответы от API.

    Raises:
        Exception: Если происходит ошибка при запросе к API.

    Example:
        >>> async for chunk in AI365VIP.create_async_generator(model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': 'Hello'}]):
        ...     print(chunk)
    """
    ...
```

## Class Parameters

- `cls` (AI365VIP): The `AI365VIP` class.
- `model` (str): The name of the model to use.
- `messages` (Messages): A list of messages to send.
- `proxy` (str, optional): The URL of the proxy server. Defaults to `None`.
- `**kwargs`: Additional arguments.

**Examples**:

Example call:

```python
async for chunk in AI365VIP.create_async_generator(model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': 'Hello'}]):
    print(chunk)
```

-------------------------------------------------------------------------------------