# Module Documentation: MetaAIAccount

## Overview

This module defines the `MetaAIAccount` class, which inherits from `MetaAI` and is designed for handling interactions with Meta AI models requiring authentication. It includes methods for creating asynchronous generators to process prompts using Meta AI.

## More details

The `MetaAIAccount` class extends the functionality of `MetaAI` by incorporating authentication mechanisms. This class is specifically tailored for Meta AI models that require user authentication to access their services. It handles tasks such as formatting prompts, managing cookies, and generating responses asynchronously.

## Classes

### `MetaAIAccount`

**Description**: Класс предназначен для взаимодействия с моделями Meta AI, требующими аутентификации.

**Inherits**:
- `MetaAI`: Наследует функциональность базового класса `MetaAI`, расширяя её для поддержки аутентификации.

**Attributes**:
- `needs_auth` (bool): Указывает на необходимость аутентификации для использования этого класса. Всегда `True` для `MetaAIAccount`.
- `parent` (str): Имя родительского класса, в данном случае `"MetaAI"`.
- `image_models` (list): Список моделей изображений, поддерживаемых классом, в данном случае `["meta"]`.

**Working principle**:
Класс `MetaAIAccount` расширяет возможности класса `MetaAI`, добавляя поддержку аутентификации. Он использует куки для аутентификации и асинхронные генераторы для обработки запросов к моделям Meta AI.

## Class Methods

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    cookies: Cookies = None,
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для обработки запросов к моделям Meta AI с использованием аутентификации.

    Args:
        cls (type[MetaAIAccount]): Ссылка на класс `MetaAIAccount`.
        model (str): Имя модели для использования.
        messages (Messages): Список сообщений для обработки.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        cookies (Cookies, optional): Куки для аутентификации. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий чанки ответа от модели.

    Raises:
        Exception: Возникает, если при создании или обработке запроса происходит ошибка.

    Example:
        >>> async for chunk in MetaAIAccount.create_async_generator(model="meta", messages=[{"role": "user", "content": "Hello"}], cookies={"cookie_name": "cookie_value"}):
        ...     print(chunk)
    """
    cookies = get_cookies(".meta.ai", True, True) if cookies is None else cookies
    async for chunk in cls(proxy).prompt(format_prompt(messages), cookies):
        yield chunk
```

**Parameters**:
- `cls` (type[MetaAIAccount]): Ссылка на класс `MetaAIAccount`.
- `model` (str): Имя модели для использования.
- `messages` (Messages): Список сообщений для обработки.
- `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
- `cookies` (Cookies, optional): Куки для аутентификации. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Examples**:

Example usage of `create_async_generator`:
```python
async for chunk in MetaAIAccount.create_async_generator(model="meta", messages=[{"role": "user", "content": "Hello"}], cookies={"cookie_name": "cookie_value"}):
    print(chunk)