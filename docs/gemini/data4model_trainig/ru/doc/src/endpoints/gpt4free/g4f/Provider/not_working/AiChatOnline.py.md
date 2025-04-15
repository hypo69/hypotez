# Модуль для работы с AiChatOnline
## Обзор

Модуль `AiChatOnline.py` предназначен для асинхронного взаимодействия с сервисом AiChatOnline для генерации ответов на основе предоставленных сообщений. Он использует `aiohttp` для выполнения асинхронных HTTP-запросов и предоставляет функциональность для получения уникального идентификатора пользователя и создания асинхронного генератора для получения ответов от модели. Модуль входит в группу `not_working`, что может говорить о его нестабильной работе.

## Подробней

Модуль содержит класс `AiChatOnline`, который наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`. Он предоставляет методы для получения токена пользователя и создания асинхронного генератора, который отправляет запросы к API AiChatOnline и возвращает ответы в виде чанков.

## Классы

### `AiChatOnline`

**Описание**: Класс для взаимодействия с сервисом AiChatOnline.
**Наследует**: `AsyncGeneratorProvider`, `ProviderModelMixin`

**Атрибуты**:
- `site_url` (str): URL сайта AiChatOnline.
- `url` (str): Базовый URL для API AiChatOnline.
- `api_endpoint` (str): Endpoint API для отправки сообщений.
- `working` (bool): Указывает, работает ли провайдер.
- `default_model` (str): Модель, используемая по умолчанию ('gpt-4o-mini').

**Принцип работы**:
Класс использует асинхронные запросы для взаимодействия с API AiChatOnline. Он получает уникальный идентификатор пользователя, формирует запрос с сообщением пользователя и отправляет его на API. Ответы от API возвращаются в виде асинхронного генератора.

## Методы класса

### `grab_token`

```python
@classmethod
async def grab_token(
    cls,
    session: ClientSession,
    proxy: str
) -> str:
    """
    Получает уникальный идентификатор пользователя с использованием асинхронного HTTP-запроса.

    Args:
        cls (AiChatOnline): Класс AiChatOnline.
        session (ClientSession): Асинхровая HTTP-сессия.
        proxy (str): Прокси-сервер для запроса.

    Returns:
        str: Уникальный идентификатор пользователя.

    Raises:
        aiohttp.ClientResponseError: Если HTTP-запрос завершается с ошибкой.
    """
```

**Назначение**: Получение уникального идентификатора пользователя.

**Параметры**:
- `cls` (AiChatOnline): Ссылка на класс.
- `session` (ClientSession): Асинхровая HTTP-сессия для выполнения запросов.
- `proxy` (str): Прокси-сервер для использования при выполнении запроса.

**Возвращает**:
- `str`: Уникальный идентификатор пользователя, полученный из ответа API.

**Как работает функция**:
- Функция выполняет GET-запрос к API для получения уникального идентификатора пользователя.
- В URL запроса добавляется случайная строка для предотвращения кэширования.
- Извлекает идентификатор из JSON-ответа и возвращает его.
- Если запрос завершается с ошибкой, выбрасывается исключение `aiohttp.ClientResponseError`.

**Примеры**:
```python
import asyncio
from aiohttp import ClientSession

async def main():
    async with ClientSession() as session:
        token = await AiChatOnline.grab_token(session, 'http://proxy:8080')
        print(f'Token: {token}')

if __name__ == "__main__":
    asyncio.run(main())
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
        """
        Создает асинхронный генератор для получения ответов от API AiChatOnline.

        Args:
            cls (AiChatOnline): Класс AiChatOnline.
            model (str): Модель для генерации ответов.
            messages (Messages): Список сообщений для отправки в API.
            proxy (str, optional): Прокси-сервер для запроса. По умолчанию `None`.
            **kwargs: Дополнительные аргументы.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий ответы от API.
        """
```

**Назначение**: Создание асинхронного генератора для получения ответов от API AiChatOnline.

**Параметры**:
- `cls` (AiChatOnline): Ссылка на класс.
- `model` (str): Модель, используемая для генерации ответов.
- `messages` (Messages): Список сообщений для отправки в API.
- `proxy` (str, optional): Прокси-сервер для использования при выполнении запроса. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, который возвращает ответы от API.

**Как работает функция**:
- Функция создает заголовки для HTTP-запроса, включая User-Agent, Referer и Content-Type.
- Формирует данные запроса, включая идентификатор разговора и отформатированный промт из сообщений.
- Получает уникальный идентификатор пользователя с помощью метода `grab_token`.
- Отправляет POST-запрос к API с заголовками и данными.
- Получает ответы от API в виде чанков и извлекает из них сообщения.
- Возвращает асинхронный генератор, который возвращает сообщения.

**Внутренние функции**:

Внутри данной функции нет внутренних функций.

**Примеры**:
```python
import asyncio
from aiohttp import ClientSession

async def main():
    messages = [{'role': 'user', 'content': 'Hello, how are you?'}]
    async for chunk in await AiChatOnline.create_async_generator('gpt-4o-mini', messages, proxy='http://proxy:8080'):
        print(chunk, end='')

if __name__ == "__main__":
    asyncio.run(main())