# Module CodeLinkAva

## Overview

This module implements the `CodeLinkAva` class, which is a provider for interacting with the CodeLinkAva AI model. It supports asynchronous generation of responses and is designed to work with GPT-3.5 Turbo. The module handles communication with the CodeLinkAva API to generate text based on provided messages.

## More details

The `CodeLinkAva` module is part of a system that integrates various AI providers for text generation. It uses asynchronous requests via `aiohttp` to communicate with the CodeLinkAva API, process responses, and yield content. The module is configured to work with specific API endpoints and request headers.

## Classes

### `CodeLinkAva`

**Description**: Represents the CodeLinkAva provider for generating text asynchronously.

**Inherits**:
- `AsyncGeneratorProvider`: Inherits from the base class for asynchronous generator providers.

**Attributes**:
- `url` (str): The base URL for the CodeLinkAva API ("https://ava-ai-ef611.web.app").
- `supports_gpt_35_turbo` (bool): A flag indicating whether the provider supports the GPT-3.5 Turbo model (True).
- `working` (bool): A flag indicating whether the provider is currently working (False).

**Methods**:
- `create_async_generator(model: str, messages: list[dict[str, str]], **kwargs) -> AsyncGenerator`: Creates an asynchronous generator for generating text from the CodeLinkAva API.

## Class Methods

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: list[dict[str, str]],
    **kwargs
) -> AsyncGenerator:
    """
    Создает асинхронный генератор для генерации текста с использованием API CodeLinkAva.

    Args:
        model (str): Модель для использования (например, "gpt-3.5-turbo").
        messages (list[dict[str, str]]): Список сообщений для отправки в API. Каждое сообщение представляет собой словарь с ключами "role" и "content".
        **kwargs: Дополнительные аргументы для передачи в API.

    Returns:
        AsyncGenerator: Асинхронный генератор, который выдает текст по мере поступления от API.

    Raises:
        Exception: Возникает, если происходит ошибка при запросе к API.

    Example:
        messages = [{"role": "user", "content": "Hello, how are you?"}]
        generator = CodeLinkAva.create_async_generator(model="gpt-3.5-turbo", messages=messages)
        async for content in generator:
            print(content)
    """
    ...
```

### Class Parameters
- `cls`: Ссылка на класс. Используется для доступа к атрибутам класса, таким как `cls.url`.
- `model` (str): Имя модели, которую следует использовать для генерации текста.
- `messages` (list[dict[str, str]]): Список сообщений, отправляемых в API. Каждое сообщение содержит роль (`user` или `assistant`) и контент сообщения.
- `kwargs` (dict): Дополнительные параметры, передаваемые в API.

### How the function works:
1. **Defines Headers**: Configures the necessary HTTP headers, including User-Agent, Accept, and Referer, for the API request.
2. **Session Creation**: Uses `aiohttp.ClientSession` to create an asynchronous HTTP session with the defined headers.
3. **Data Preparation**: Constructs a payload with messages, temperature, and stream parameters.
4. **API Request**: Sends an asynchronous POST request to the CodeLinkAva API endpoint (`https://ava-alpha-api.codelink.io/api/chat`) with the payload.
5. **Response Handling**:
   - Checks the response status and raises an exception for HTTP errors.
   - Iterates through the response content line by line.
   - Decodes each line and checks if it starts with `data: `.
   - If the line indicates the end of the stream (`data: [DONE]`), the loop breaks.
   - Parses the JSON content from the line (removing the `data: ` prefix and trailing newline).
   - Extracts the content from the `choices` array in the JSON response.
   - Yields the extracted content to the asynchronous generator.

### Examples

```python
messages = [{"role": "user", "content": "Напиши короткое стихотворение о весне."}]
generator = CodeLinkAva.create_async_generator(model="gpt-3.5-turbo", messages=messages)
async for content in generator:
    print(content)
```

```python
messages = [
    {"role": "system", "content": "Ты полезный ассистент."},
    {"role": "user", "content": "Как дела?"}
]
generator = CodeLinkAva.create_async_generator(model="gpt-3.5-turbo", messages=messages)
async for content in generator:
    print(content)