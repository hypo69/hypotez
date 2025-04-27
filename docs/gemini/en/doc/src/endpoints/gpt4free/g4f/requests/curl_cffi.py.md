# Модуль для работы с HTTP запросами на основе CURL

## Обзор

Этот модуль предоставляет класс `StreamSession`, который позволяет выполнять HTTP запросы с использованием CURL и обрабатывать потоковые ответы. Он включает в себя различные методы для отправки разных типов запросов (GET, POST, PUT, DELETE и т.д.) и обработку ответов в формате JSON, текста или потока байтов.

## Подробности

Модуль использует библиотеку `curl_cffi`, которая предоставляет интерфейс для CURL на Python. Он также использует `AsyncSession` из библиотеки `requests`, чтобы позволить выполнять асинхронные HTTP запросы.

## Классы

### `class StreamResponse`

**Описание**: Класс для обработки потоковых ответов от HTTP запросов.

**Атрибуты**:

- `inner (Response)`: Исходный объект `Response` библиотеки `requests`.

**Методы**:

- `text()`: Асинхронно получает текст ответа.
- `raise_for_status()`: Вызывает исключение `HTTPError` если оно произошло.
- `json()`: Асинхронно парсит JSON контент ответа.
- `iter_lines()`: Асинхронно итерируется по строкам ответа.
- `iter_content()`: Асинхронно итерируется по контенту ответа.
- `sse()`: Асинхронно итерируется по Server-Sent Events ответа.
- `__aenter__()`: Асинхронно входит в контекст выполнения для объекта ответа.
- `__aexit__()`: Асинхронно выходит из контекста выполнения для объекта ответа.

### `class StreamSession`

**Описание**: Асинхронный сессионный класс для обработки HTTP запросов с потоковой обработкой.

**Наследуется от**: `AsyncSession`

**Методы**:

- `request()`: Создает и возвращает объект `StreamResponse` для заданного HTTP запроса.
- `ws_connect()`: Создает соединение с WebSocket.
- `_ws_connect()`: Внутренний метод для создания соединения с WebSocket.
- `head()`: Метод HEAD для HTTP запроса.
- `get()`: Метод GET для HTTP запроса.
- `post()`: Метод POST для HTTP запроса.
- `put()`: Метод PUT для HTTP запроса.
- `patch()`: Метод PATCH для HTTP запроса.
- `delete()`: Метод DELETE для HTTP запроса.
- `options()`: Метод OPTIONS для HTTP запроса.

### `class FormData`

**Описание**: Класс для создания форм данных, используемых в HTTP запросах.

**Методы**:

- `add_field()`: Добавляет поле в форму данных.

### `class WebSocket`

**Описание**: Класс для работы с WebSocket соединениями.

**Атрибуты**:

- `session (StreamSession)`: Сессия, используемая для соединения.
- `url (str)`: URL WebSocket сервера.
- `options (dict)`: Опции соединения.

**Методы**:

- `__aenter__()`: Асинхронно входит в контекст выполнения для объекта WebSocket.
- `__aexit__()`: Асинхронно выходит из контекста выполнения для объекта WebSocket.
- `receive_str()`: Асинхронно получает строку из WebSocket.
- `send_str()`: Асинхронно отправляет строку в WebSocket.

## Примеры

```python
from hypotez.src.endpoints.gpt4free.g4f.requests.curl_cffi import StreamSession, FormData
import asyncio

async def main():
    # Создание сессии
    session = StreamSession()

    # Создание форм данных
    form_data = FormData()
    form_data.add_field("name", "John Doe")
    form_data.add_field("age", 30)

    # Отправка POST запроса
    async with session.post("https://example.com/api/users", data=form_data) as response:
        # Обработка ответа
        if response.ok:
            print(f"Успешно отправлено: {response.text}")
        else:
            print(f"Ошибка: {response.status} - {response.reason}")

# Запуск асинхронной функции
asyncio.run(main())
```

```python
from hypotez.src.endpoints.gpt4free.g4f.requests.curl_cffi import StreamSession, WebSocket
import asyncio

async def main():
    # Создание сессии
    session = StreamSession()

    # Создание WebSocket соединения
    async with session.ws_connect("ws://example.com/chat") as websocket:
        # Отправка сообщения
        await websocket.send_str("Hello, world!")

        # Получение сообщения
        message = await websocket.receive_str()
        print(f"Получено сообщение: {message}")

# Запуск асинхронной функции
asyncio.run(main())
```

## Примечания

- Модуль требует установки библиотеки `curl_cffi`: `pip install -U curl_cffi`
- Используйте `logger` из модуля `src.logger` для логирования.

## Дополнительные сведения

- Библиотека `curl_cffi`: https://pypi.org/project/curl-cffi/
- Библиотека `requests`: https://requests.readthedocs.io/en/latest/