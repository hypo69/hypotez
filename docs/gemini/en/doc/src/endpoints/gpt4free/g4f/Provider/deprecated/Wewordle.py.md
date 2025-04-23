# Module Wewordle

## Overview

This module defines the `Wewordle` class, which is a provider for interacting with the Wewordle service to generate text using a GPT-3.5 Turbo model. It uses asynchronous HTTP requests to communicate with the Wewordle API.

## More details

The `Wewordle` class inherits from `AsyncProvider` and is designed to asynchronously generate text based on provided messages. It constructs specific headers and a JSON payload to interact with the Wewordle API endpoint. The module handles creating a unique user and app ID for each request.

## Classes

### `Wewordle`

**Description**: A class that provides asynchronous text generation using the Wewordle service.

**Inherits**:
- `AsyncProvider`: Inherits asynchronous request handling capabilities.

**Attributes**:
- `url` (str): The base URL for the Wewordle API.
- `working` (bool): A flag indicating whether the provider is currently working (deprecated).
- `supports_gpt_35_turbo` (bool): A flag indicating support for the GPT-3.5 Turbo model.

**Methods**:
- `create_async`: Asynchronously generates text using the Wewordle service.

### `create_async`

```python
@classmethod
async def create_async(
    cls,
    model: str,
    messages: list[dict[str, str]],
    proxy: str = None,
    **kwargs
) -> str:
    """ Асинхронно генерирует текст, используя сервис Wewordle.

    Args:
        cls: Класс Wewordle.
        model (str): Модель для использования (в данном случае, GPT-3.5 Turbo).
        messages (list[dict[str, str]]): Список сообщений для отправки в API.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        str: Сгенерированный текст.

    Raises:
        aiohttp.ClientResponseError: Если HTTP-запрос завершается с ошибкой.

    Example:
        >>> result = await Wewordle.create_async(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello"}])
        >>> print(result)
        "Hello, how can I assist you today?"
    """
```

**Parameters**:
- `cls`: The class itself.
- `model` (str): The model to use (in this case, GPT-3.5 Turbo).
- `messages` (list[dict[str, str]]): A list of messages to send to the API.
- `proxy` (str, optional): A proxy server to use. Defaults to `None`.
- `**kwargs`: Additional keyword arguments.

**Returns**:
- `str`: The generated text.

**How the function works**:
1. **Настройка заголовков**: Функция определяет заголовки HTTP-запроса, включая `accept`, `pragma`, `Content-Type` и `Connection`.
2. **Генерация идентификаторов**: Генерирует случайные идентификаторы пользователя (`_user_id`) и приложения (`_app_id`).
3. **Формирование данных запроса**: Создает структуру данных, включающую идентификаторы, сообщения и информацию о подписчике. В данных подписчика включается информация о дате запроса и анонимные идентификаторы.
4. **Выполнение асинхронного запроса**: Использует `aiohttp.ClientSession` для выполнения POST-запроса к API Wewordle (`{cls.url}/gptapi/v1/android/turbo`) с использованием указанного прокси и JSON-данных.
5. **Обработка ответа**: Извлекает содержимое сообщения из ответа JSON и возвращает его. Если содержимое отсутствует, возвращает `None`.
6. **Обработка ошибок**: В случае ошибки HTTP-запроса вызывается исключение `aiohttp.ClientResponseError`.

**Examples**:
```python
# Пример вызова функции create_async
result = await Wewordle.create_async(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello"}])
print(result)
# Вывод: "Hello, how can I assist you today?"
```

## Class Parameters

- `url` (str): The base URL for the Wewordle API.
- `working` (bool): A flag indicating whether the provider is currently working (deprecated).
- `supports_gpt_35_turbo` (bool): A flag indicating support for the GPT-3.5 Turbo model.