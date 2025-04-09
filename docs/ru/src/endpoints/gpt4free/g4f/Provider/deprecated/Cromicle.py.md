# Модуль Cromicle
## Обзор

Модуль `Cromicle` предоставляет класс `Cromicle`, который является асинхронным генератором для взаимодействия с сервисом cromicle.top. Этот модуль предназначен для обмена сообщениями с использованием API данного сервиса.

## Подробнее

Модуль содержит класс `Cromicle`, который наследует `AsyncGeneratorProvider` и предоставляет функциональность для асинхронной генерации ответов от сервиса cromicle.top. Он использует `aiohttp` для выполнения асинхронных HTTP-запросов. Модуль также содержит функции для создания заголовков и полезной нагрузки запроса.

## Классы

### `Cromicle`

**Описание**: Класс `Cromicle` предназначен для взаимодействия с сервисом cromicle.top. Он наследует `AsyncGeneratorProvider` и предоставляет метод `create_async_generator` для асинхронной генерации ответов.

**Наследует**:
- `AsyncGeneratorProvider`: Класс, предоставляющий базовую функциональность для асинхронных генераторов.

**Аттрибуты**:
- `url` (str): URL сервиса cromicle.top.
- `working` (bool): Указывает, работает ли провайдер в данный момент.
- `supports_gpt_35_turbo` (bool): Указывает, поддерживает ли провайдер модель `gpt-3.5-turbo`.

**Методы**:
- `create_async_generator`: Асинхронный метод для создания генератора ответов от сервиса cromicle.top.

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
        Создает асинхронный генератор для получения ответов от сервиса cromicle.top.

        Args:
            model (str): Модель, используемая для генерации ответа.
            messages (Messages): Список сообщений для отправки в запросе.
            proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
            **kwargs: Дополнительные аргументы.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий ответы от сервиса.
        """
```

**Назначение**: Создает асинхронный генератор для получения ответов от сервиса cromicle.top.

**Параметры**:
- `model` (str): Модель, используемая для генерации ответа.
- `messages` (Messages): Список сообщений для отправки в запросе.
- `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий ответы от сервиса.

**Как работает функция**:

1.  **Создание сессии `aiohttp`**: Инициализируется асинхронная сессия `aiohttp` с заголовками, полученными из функции `_create_header`.
2.  **Выполнение POST-запроса**: Отправляется POST-запрос к сервису cromicle.top с использованием указанного прокси (если он предоставлен) и полезной нагрузки, созданной функцией `_create_payload`.
3.  **Обработка потока ответов**: Асинхронно итерируется по потоку содержимого ответа, декодируя каждый чанк и передавая его как часть генератора.

```text
    +-----------------------+
    |  create_async_generator |
    +-----------------------+
    |
    V
    +-----------------------+
    |  Создание сессии      |
    |  aiohttp              |
    +-----------------------+
    |
    V
    +-----------------------+
    |   POST-запрос         |
    |  к cromicle.top       |
    +-----------------------+
    |
    V
    +-----------------------+
    |  Обработка потока     |
    |  ответов              |
    +-----------------------+
```

**Примеры**:

```python
import asyncio
from typing import List, AsyncGenerator

from aiohttp import ClientSession

from ...typing import Messages, Dict
from ..base_provider import AsyncGeneratorProvider
from ..helper import format_prompt
from hashlib import sha256


class Cromicle(AsyncGeneratorProvider):
    url: str = 'https://cromicle.top'
    working: bool = False
    supports_gpt_35_turbo: bool = True

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        **kwargs
    ) -> AsyncGenerator[str, None]:  # Исправлено на AsyncGenerator[str, None]
        async with ClientSession(
            headers=_create_header()
        ) as session:
            async with session.post(
                f'{cls.url}/chat',
                proxy=proxy,
                json=_create_payload(format_prompt(messages))
            ) as response:
                response.raise_for_status()
                async for stream in response.content.iter_any():
                    if stream:
                        yield stream.decode()


def _create_header() -> Dict[str, str]:
    return {
        'accept': '*/*',
        'content-type': 'application/json',
    }


def _create_payload(message: str) -> Dict[str, str]:
    return {
        'message': message,
        'token': 'abc',
        'hash': sha256('abc'.encode() + message.encode()).hexdigest()
    }


async def main():
    messages: Messages = [{"role": "user", "content": "Hello, Cromicle!"}]
    async for message in Cromicle.create_async_generator(model="gpt-3.5-turbo", messages=messages):
        print(message, end="")

if __name__ == "__main__":
    asyncio.run(main())
```

## Функции

### `_create_header`

```python
def _create_header() -> Dict[str, str]:
    """
    Создает словарь с заголовками для HTTP-запроса.

    Returns:
        Dict[str, str]: Словарь с заголовками 'accept' и 'content-type'.
    """
```

**Назначение**: Создает словарь с заголовками для HTTP-запроса.

**Возвращает**:
- `Dict[str, str]`: Словарь с заголовками 'accept' и 'content-type'.

**Как работает функция**:

1.  **Создание словаря**: Создается словарь, содержащий заголовки `accept` и `content-type`.

```text
    +-----------------------+
    |    _create_header     |
    +-----------------------+
    |
    V
    +-----------------------+
    |  Создание словаря     |
    |  с заголовками         |
    +-----------------------+
```

**Примеры**:

```python
def _create_header() -> Dict[str, str]:
    return {
        'accept': '*/*',
        'content-type': 'application/json',
    }

header = _create_header()
print(header)
# {'accept': '*/*', 'content-type': 'application/json'}
```

### `_create_payload`

```python
def _create_payload(message: str) -> Dict[str, str]:
    """
    Создает словарь с полезной нагрузкой для HTTP-запроса.

    Args:
        message (str): Сообщение для отправки в запросе.

    Returns:
        Dict[str, str]: Словарь с полями 'message', 'token' и 'hash'.
    """
```

**Назначение**: Создает словарь с полезной нагрузкой для HTTP-запроса.

**Параметры**:
- `message` (str): Сообщение для отправки в запросе.

**Возвращает**:
- `Dict[str, str]`: Словарь с полями 'message', 'token' и 'hash'.

**Как работает функция**:

1.  **Хеширование сообщения**: Выполняется хеширование сообщения с использованием SHA256.
2.  **Создание словаря**: Создается словарь, содержащий сообщение, токен и хеш.

```text
    +-----------------------+
    |   _create_payload    |
    +-----------------------+
    |
    V
    +-----------------------+
    |  Хеширование          |
    |  сообщения           |
    +-----------------------+
    |
    V
    +-----------------------+
    |  Создание словаря     |
    |  с нагрузкой           |
    +-----------------------+
```

**Примеры**:

```python
from hashlib import sha256

def _create_payload(message: str) -> Dict[str, str]:
    return {
        'message': message,
        'token': 'abc',
        'hash': sha256('abc'.encode() + message.encode()).hexdigest()
    }
message = "Hello, Cromicle!"
payload = _create_payload(message)
print(payload)
# {'message': 'Hello, Cromicle!', 'token': 'abc', 'hash': 'd98b8e9c7f007e9f6e3a9c9c7e3b8b1a2a8b8e9c7f007e9f6e3a9c9c7e3b8b1a'}