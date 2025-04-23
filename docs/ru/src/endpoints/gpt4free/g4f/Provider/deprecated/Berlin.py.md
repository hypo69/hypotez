# Документация для модуля `Berlin`

## Обзор

Модуль `Berlin` представляет собой асинхронный генератор провайдера для взаимодействия с API `ai.berlin4h.top`. Он предназначен для получения ответов от языковой модели, в частности, `gpt-3.5-turbo`. Модуль использует `aiohttp` для асинхронных HTTP-запросов и предоставляет возможность работы через прокси.

## Подробней

Этот модуль является частью набора провайдеров в проекте `hypotez`, предназначенных для обеспечения доступа к различным языковым моделям. Он предоставляет асинхронный интерфейс для взаимодействия с API `ai.berlin4h.top`, который возвращает ответы от языковой модели.

## Классы

### `Berlin`

**Описание**: Класс `Berlin` является асинхронным генератором провайдера. Он отвечает за взаимодействие с API `ai.berlin4h.top` для генерации текста на основе предоставленных сообщений.

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:
- `url` (str): URL API `ai.berlin4h.top`.
- `working` (bool): Указывает, работает ли провайдер в данный момент (по умолчанию `False`).
- `supports_gpt_35_turbo` (bool): Указывает, поддерживает ли провайдер модель `gpt-3.5-turbo` (по умолчанию `True`).
- `_token` (str | None): Токен аутентификации, используемый для доступа к API (изначально `None`).

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для получения ответов от API.

## Методы класса

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
    """Создает асинхронный генератор для получения ответов от API.

    Args:
        cls (Berlin): Ссылка на класс `Berlin`.
        model (str): Название языковой модели для использования.
        messages (Messages): Список сообщений для отправки в API.
        proxy (str, optional): URL прокси-сервера для использования. По умолчанию `None`.
        **kwargs: Дополнительные аргументы, передаваемые в API.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий ответы от API.

    Raises:
        RuntimeError: Если при получении ответа от API происходит ошибка.
    """
    ...
```

**Назначение**: Создает асинхронный генератор, который отправляет запросы к API `ai.berlin4h.top` и возвращает ответы.

**Параметры**:
- `cls`: Ссылка на класс `Berlin`.
- `model` (str): Название языковой модели для использования. Если не указано, используется `gpt-3.5-turbo`.
- `messages` (Messages): Список сообщений для отправки в API.
- `proxy` (str, optional): URL прокси-сервера для использования. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы, передаваемые в API.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий ответы от API.

**Как работает функция**:

1. **Подготовка заголовков**: Функция формирует заголовки HTTP-запроса, включая User-Agent, Accept, Referer и Content-Type.
2. **Авторизация**: Если токен отсутствует, выполняется запрос к API для получения токена. Используются жестко заданные логин и пароль.
3. **Формирование данных запроса**: Подготавливаются данные для запроса, включая `prompt` (сформированный из `messages`), `parentMessageId` (случайный UUID) и параметры модели (`model`, `temperature`, `presence_penalty`, `frequency_penalty`, `max_tokens`).
4. **Отправка запроса и обработка ответа**: Отправляется POST-запрос к API `ai.berlin4h.top` с использованием `aiohttp.ClientSession`. Полученные чанки данных преобразуются из JSON и передаются через генератор.
5. **Обработка ошибок**: В случае ошибки при получении ответа от API, поднимается исключение `RuntimeError`.

**Примеры**:

```python
# Пример использования create_async_generator
import asyncio
from typing import List, Dict

async def main():
    model = "gpt-3.5-turbo"
    messages: List[Dict[str, str]] = [{"role": "user", "content": "Hello, how are you?"}]
    proxy = None
    kwargs = {}

    generator = Berlin.create_async_generator(model, messages, proxy, **kwargs)
    async for chunk in generator:
        print(chunk, end="")

if __name__ == "__main__":
    asyncio.run(main())
```
```python
# Пример использования create_async_generator с прокси
import asyncio
from typing import List, Dict

async def main():
    model = "gpt-3.5-turbo"
    messages: List[Dict[str, str]] = [{"role": "user", "content": "Hello, how are you?"}]
    proxy = "http://your_proxy:8080"
    kwargs = {}

    generator = Berlin.create_async_generator(model, messages, proxy, **kwargs)
    async for chunk in generator:
        print(chunk, end="")

if __name__ == "__main__":
    asyncio.run(main())
```
```python
# Пример использования create_async_generator с дополнительными параметрами
import asyncio
from typing import List, Dict

async def main():
    model = "gpt-3.5-turbo"
    messages: List[Dict[str, str]] = [{"role": "user", "content": "Translate to french: Hello, how are you?"}]
    proxy = None
    kwargs = {"temperature": 0.7, "max_tokens": 2000}

    generator = Berlin.create_async_generator(model, messages, proxy, **kwargs)
    async for chunk in generator:
        print(chunk, end="")

if __name__ == "__main__":
    asyncio.run(main())
```

## Параметры класса

- `url` (str): URL API `ai.berlin4h.top`.
- `working` (bool): Указывает, работает ли провайдер в данный момент.
- `supports_gpt_35_turbo` (bool): Указывает, поддерживает ли провайдер модель `gpt-3.5-turbo`.
- `_token` (str | None): Токен аутентификации, используемый для доступа к API.

```