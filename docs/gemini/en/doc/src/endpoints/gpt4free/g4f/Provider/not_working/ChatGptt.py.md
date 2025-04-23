# Module for interacting with the ChatGpt platform

## Overview

This module provides an asynchronous implementation for interacting with the ChatGpt platform. It includes functionalities for creating asynchronous generators to handle responses, managing message histories, and supporting system messages. This module is designed to be used with the `hypotez` project.

## More details

The `ChatGptt` class inherits from `AsyncGeneratorProvider` and `ProviderModelMixin`, providing functionalities for asynchronous request handling and model management. It is designed to interact with the ChatGpt platform through its API, handling authentication and data streaming. This module is located in the `hypotez/src/endpoints/gpt4free/g4f/Provider/not_working/` directory, indicating that it may not be fully functional or under development.

## Classes

### `ChatGptt`

**Description**:
This class extends `AsyncGeneratorProvider` and `ProviderModelMixin` to provide an interface for interacting with the ChatGpt platform. It handles the creation of asynchronous generators, manages message histories, and supports system messages.

**Inherits**:
- `AsyncGeneratorProvider`: Provides asynchronous generator functionalities.
- `ProviderModelMixin`: Manages model-related functionalities.

**Attributes**:
- `url` (str): The base URL for the ChatGpt platform.
- `api_endpoint` (str): The API endpoint for sending messages.
- `working` (bool): Indicates whether the provider is currently working.
- `supports_stream` (bool): Indicates whether the provider supports streaming responses.
- `supports_system_message` (bool): Indicates whether the provider supports system messages.
- `supports_message_history` (bool): Indicates whether the provider supports message history.
- `default_model` (str): The default model to use if none is specified.
- `models` (list): A list of supported models.

**Working principle**:
The `ChatGptt` class uses asynchronous requests to interact with the ChatGpt platform. It first retrieves authentication tokens from the initial page content and then sends a payload containing the message and other required parameters to the API endpoint. The response is streamed back to the caller via an asynchronous generator.

**Methods**:
- `create_async_generator()`: Creates an asynchronous generator for handling responses from the ChatGpt platform.

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
    """ Создает асинхронный генератор для обработки ответов от платформы ChatGpt.
    Args:
        cls (ChatGptt): Ссылка на класс.
        model (str): Модель для использования.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий результаты.

    Raises:
        RuntimeError: Если не удается найти токены аутентификации на странице HTML.

    How the function works:
        - Извлекает параметры модели.
        - Формирует заголовки запроса.
        - Создает сессию клиента для асинхронных запросов.
        - Отправляет запрос на начальную страницу для получения токенов аутентификации.
        - Извлекает токены nonce и post_id из HTML-кода страницы.
        - Подготавливает полезную нагрузку с данными сессии и сообщением.
        - Отправляет POST-запрос к API-endpoint и возвращает результат через генератор.
    """
```

### Parameters:
- `cls` (ChatGptt): Ссылка на класс.
- `model` (str): Модель для использования.
- `messages` (Messages): Список сообщений для отправки.
- `proxy` (str, optional): Прокси-сервер для использования. Defaults to `None`.
- `**kwargs`: Дополнительные параметры.

### Examples:

```python
# Пример использования create_async_generator
messages = [{"role": "user", "content": "Hello, ChatGpt!"}]
async for message in ChatGptt.create_async_generator(model='gpt-4', messages=messages):
    print(message)
```
```python
# Пример использования create_async_generator с прокси
messages = [{"role": "user", "content": "Hello, ChatGpt!"}]
async for message in ChatGptt.create_async_generator(model='gpt-4', messages=messages, proxy='http://proxy.example.com'):
    print(message)
```