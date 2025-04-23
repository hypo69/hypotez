# Module `Chatgpt4Online`

## Overview

The `Chatgpt4Online` module provides an asynchronous implementation for interacting with the ChatGPT4Online service. It allows generating responses from the ChatGPT-4 model via an unofficial API. This module includes functionality for obtaining a nonce, constructing headers, sending prompts, and processing streamed responses.

## More details

This module is designed to asynchronously communicate with the `chatgpt4online.org` service. It handles the specifics of the API endpoint, including session initialization, header construction, and streamed response processing. It is important to use this module in an asynchronous context due to its reliance on `aiohttp` for non-blocking I/O operations.

## Classes

### `Chatgpt4Online`

**Description**: An asynchronous provider for interacting with the ChatGPT4Online service.

**Inherits**:
- `AsyncGeneratorProvider`: Inherits asynchronous generator capabilities from the base class.

**Attributes**:
- `url` (str): The base URL for the ChatGPT4Online service.
- `api_endpoint` (str): The API endpoint for submitting chat requests.
- `working` (bool): Indicates whether the provider is currently operational (set to `False`).
- `default_model` (str): The default model used by the provider (`gpt-4`).
- `models` (list): A list of supported models (currently only `gpt-4`).

**Methods**:
- `get_nonce(headers: dict) -> str`: Asynchronously retrieves a nonce from the ChatGPT4Online service.
- `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`: Creates an asynchronous generator that yields responses from the ChatGPT4Online service.

### Class Methods

#### `get_nonce`

```python
async def get_nonce(headers: dict) -> str:
    """
    Асинхронно получает nonce (одноразовый код) от сервиса ChatGPT4Online.

    Args:
        headers (dict): Заголовки HTTP-запроса.

    Returns:
        str: Значение nonce, полученное из ответа сервиса.

    Raises:
        ClientError: Возникает, если запрос не удался.

    Example:
        >>> headers = {'User-Agent': 'Mozilla/5.0'}
        >>> nonce = await Chatgpt4Online.get_nonce(headers)
        >>> print(nonce)
        'example_nonce'
    """
```

#### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для получения ответов от сервиса ChatGPT4Online.

    Args:
        cls: Ссылка на класс.
        model (str): Название используемой модели.
        messages (Messages): Список сообщений для отправки в запросе.
        proxy (str, optional): Адрес прокси-сервера. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Yields:
        str: Части ответа от сервиса.

    Raises:
        aiohttp.ClientError: Если запрос не удался.
        json.JSONDecodeError: Если не удается декодировать JSON из ответа.

    Internal functions:
        - None

    How the function works:
        1. Функция устанавливает необходимые заголовки, включая полученный nonce.
        2. Форматирует сообщения для отправки в запросе.
        3. Отправляет POST-запрос к API-endpoint с использованием `aiohttp.ClientSession`.
        4. Итерируется по частям ответа (chunks) и извлекает данные JSON.
        5. Извлекает и выдает полезные данные из JSON (`live` или `end`).

    Examples:
        >>> async for message in Chatgpt4Online.create_async_generator(model='gpt-4', messages=[{'role': 'user', 'content': 'Hello'}]):
        ...     print(message)
        Hello!
    """
```

## Class Parameters

- `url` (str): Базовый URL сервиса ChatGPT4Online.
- `api_endpoint` (str): Конечная точка API для отправки запросов чата.
- `working` (bool): Указывает, работает ли провайдер в данный момент.
- `default_model` (str): Модель, используемая по умолчанию (`gpt-4`).
- `models` (list): Список поддерживаемых моделей (в настоящее время содержит только `gpt-4`).