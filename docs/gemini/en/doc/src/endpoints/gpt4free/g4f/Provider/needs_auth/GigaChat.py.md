# Module `GigaChat`

## Overview

This module implements the `GigaChat` class, which provides an interface for interacting with the GigaChat service from Sber. It supports message history, system messages, and streaming responses. The module requires authentication via an API key and handles token management. It also includes specific configurations for working with Russian SSL certificates.

## More details

This module is designed to facilitate interaction with the GigaChat service by handling authentication, managing tokens, and processing responses. The `GigaChat` class extends `AsyncGeneratorProvider` and `ProviderModelMixin`, providing asynchronous message generation capabilities. It ensures secure communication through SSL and manages token expiration to maintain active sessions.

## Classes

### `GigaChat`

**Description**: Class for interacting with the GigaChat service.

**Inherits**:
- `AsyncGeneratorProvider`: Provides asynchronous generation capabilities.
- `ProviderModelMixin`: Provides a mixin for model-related functionality.

**Attributes**:
- `url` (str): The base URL for the GigaChat service.
- `working` (bool): Indicates whether the provider is working.
- `supports_message_history` (bool): Indicates whether the provider supports message history.
- `supports_system_message` (bool): Indicates whether the provider supports system messages.
- `supports_stream` (bool): Indicates whether the provider supports streaming responses.
- `needs_auth` (bool): Indicates whether the provider requires authentication.
- `default_model` (str): The default model to use for GigaChat.
- `models` (list): A list of supported models.

**Working principle**:
The class manages authentication tokens, sends requests to the GigaChat API, and processes streaming responses. It handles SSL certificate configurations for secure communication with the service.

**Methods**:
- `create_async_generator()`: Creates an asynchronous generator for processing messages.

## Class Methods

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    stream: bool = True,
    proxy: str = None,
    api_key: str = None,
    connector: BaseConnector = None,
    scope: str = "GIGACHAT_API_PERS",
    update_interval: float = 0,
    **kwargs
) -> AsyncResult:
    """Создает асинхронный генератор для обработки сообщений с использованием GigaChat.

    Args:
        cls (type): Класс, для которого создается генератор.
        model (str): Модель для использования в GigaChat.
        messages (Messages): Список сообщений для отправки.
        stream (bool, optional): Флаг, указывающий, следует ли использовать потоковую передачу. По умолчанию `True`.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        api_key (str, optional): API-ключ для аутентификации. По умолчанию `None`.
        connector (BaseConnector, optional): Aiohttp коннектор. По умолчанию `None`.
        scope (str, optional): Область действия токена доступа. По умолчанию `"GIGACHAT_API_PERS"`.
        update_interval (float, optional): Интервал обновления. По умолчанию `0`.
        **kwargs: Дополнительные аргументы для передачи в API GigaChat.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий результаты обработки сообщений.

    Raises:
        MissingAuthError: Если отсутствует `api_key`.

    Example:
        >>> async for message in GigaChat.create_async_generator(model="GigaChat:latest", messages=[{"role": "user", "content": "Hello"}], api_key="your_api_key"):
        ...     print(message)
    """
    ...
```

## Class Parameters

- `model` (str): The model to be used for GigaChat.
- `messages` (Messages): A list of messages to be sent.
- `stream` (bool, optional): Flag indicating whether to use streaming. Defaults to `True`.
- `proxy` (str, optional): The proxy server URL. Defaults to `None`.
- `api_key` (str, optional): The API key for authentication. Defaults to `None`.
- `connector` (BaseConnector, optional): Aiohttp connector. Defaults to `None`.
- `scope` (str, optional): The scope of the access token. Defaults to `"GIGACHAT_API_PERS"`.
- `update_interval` (float, optional): Update interval. Defaults to `0`.
- `**kwargs`: Additional arguments to be passed to the GigaChat API.

**Examples**:

Example usage of `create_async_generator` with different parameters:

```python
async for message in GigaChat.create_async_generator(
    model="GigaChat:latest",
    messages=[{"role": "user", "content": "Привет"}],
    api_key="your_api_key",
    proxy="http://your_proxy:8080",
    scope="GIGACHAT_API_PERS",
    update_interval=0.5
):
    print(message)

async for message in GigaChat.create_async_generator(
    model="GigaChat-Plus",
    messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "What is the capital of Russia?"}],
    api_key="your_api_key"
):
    print(message)