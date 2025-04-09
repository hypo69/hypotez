# Модуль для обработки асинхронных запросов с использованием curl_cffi

## Обзор

Модуль предоставляет классы `StreamResponse`, `StreamSession`, `FormData` и `WebSocket` для работы с асинхронными HTTP запросами и WebSocket соединениями с использованием библиотеки `curl_cffi`. Он обеспечивает удобный интерфейс для отправки запросов, обработки ответов и работы с потоковыми данными.

## Подробнее

Этот модуль предназначен для упрощения асинхронной работы с HTTP и WebSocket соединениями. Классы `StreamResponse` и `StreamSession` позволяют отправлять HTTP запросы и обрабатывать потоковые ответы. Класс `FormData` используется для создания multipart/form-data запросов. Класс `WebSocket` обеспечивает функциональность для работы с WebSocket соединениями.

## Классы

### `StreamResponse`

**Описание**: Класс-обертка для обработки асинхронных потоковых ответов.

**Принцип работы**:
Класс `StreamResponse` оборачивает объект `Response` из библиотеки `curl_cffi` и предоставляет асинхронные методы для чтения текста, JSON, итерации по строкам и содержимому ответа. Он также поддерживает контекстный менеджер для автоматического закрытия соединения.

**Аттрибуты**:

-   `inner` (Response): Оригинальный объект `Response`.
-   `url` (str): URL запроса.
-   `method` (str): HTTP метод запроса.
-   `request`: Объект запроса.
-   `status` (int): HTTP статус код ответа.
-   `reason` (str): Текстовое описание статуса ответа.
-   `ok` (bool): Флаг, указывающий на успешность запроса (статус код < 400).
-   `headers`: Заголовки ответа.
-   `cookies`: Куки ответа.

**Методы**:

-   `__init__(self, inner: Response) -> None`: Инициализирует `StreamResponse` с предоставленным объектом `Response`.
-   `text(self) -> str`: Асинхронно получает текст ответа.
-   `raise_for_status(self) -> None`: Возбуждает исключение `HTTPError`, если произошла ошибка.
-   `json(self, **kwargs) -> Any`: Асинхронно разбирает JSON контент ответа.
-   `iter_lines(self) -> AsyncGenerator[bytes, None]`: Асинхронно итерируется по строкам ответа.
-   `iter_content(self) -> AsyncGenerator[bytes, None]`: Асинхронно итерируется по содержимому ответа.
-   `sse(self) -> AsyncGenerator[dict, None]`: Асинхронно итерируется по Server-Sent Events (SSE) ответа.
-   `__aenter__(self)`: Асинхронно входит в контекст выполнения для объекта ответа.
-   `__aexit__(self, *args)`: Асинхронно выходит из контекста выполнения для объекта ответа и закрывает соединение.

### `StreamSession`

**Описание**: Асинхронный класс сессии для обработки HTTP запросов с потоковой передачей.

**Наследует**:

-   `AsyncSession`

**Принцип работы**:
Класс `StreamSession` наследуется от `AsyncSession` и предоставляет метод `request` для создания объектов `StreamResponse`. Он также определяет методы для HTTP методов (GET, POST, PUT, DELETE и т.д.) как `partialmethod` для удобного использования.

**Методы**:

-   `request(self, method: str, url: str, ssl=None, **kwargs) -> StreamResponse`: Создает и возвращает объект `StreamResponse` для данного HTTP запроса.
-   `ws_connect(self, url, *args, **kwargs)`: Устанавливает WebSocket соединение.
-   `_ws_connect(self, url, **kwargs)`: Внутренний метод для установки WebSocket соединения.
-   `head`: Отправляет HEAD запрос.
-   `get`: Отправляет GET запрос.
-   `post`: Отправляет POST запрос.
-   `put`: Отправляет PUT запрос.
-   `patch`: Отправляет PATCH запрос.
-   `delete`: Отправляет DELETE запрос.
-   `options`: Отправляет OPTIONS запрос.

### `FormData`

**Описание**: Класс для создания multipart/form-data запросов.

**Принцип работы**:
Класс `FormData` наследуется от `CurlMime` (если доступен) и предоставляет метод `add_field` для добавления полей в форму. Если `CurlMime` недоступен, класс выбрасывает исключение `RuntimeError`.

**Методы**:

-   `add_field(self, name, data=None, content_type: str = None, filename: str = None) -> None`: Добавляет поле в форму.

### `WebSocket`

**Описание**: Класс для работы с WebSocket соединениями.

**Принцип работы**:
Класс `WebSocket` предоставляет методы для отправки и получения данных через WebSocket соединение. Он использует `curl_cffi` для установки и управления соединением.

**Методы**:

-   `__init__(self, session, url, **kwargs) -> None`: Инициализирует объект `WebSocket`.
-   `__aenter__(self)`: Асинхронно входит в контекст выполнения для объекта WebSocket.
-   `__aexit__(self, *args)`: Асинхронно выходит из контекста выполнения для объекта WebSocket и закрывает соединение.
-   `receive_str(self, **kwargs) -> str`: Асинхронно получает строку из WebSocket соединения.
-   `send_str(self, data: str)`: Асинхронно отправляет строку через WebSocket соединение.

## Функции

В данном модуле функции отсутствуют.

### Как работает класс `StreamResponse`:

1.  **Инициализация**: При создании экземпляра `StreamResponse` передается объект `Response` из `curl_cffi`.
2.  **Чтение данных**: Методы `text()`, `json()`, `iter_lines()`, `iter_content()` позволяют асинхронно читать данные из ответа в различных форматах.
3.  **Обработка ошибок**: Метод `raise_for_status()` позволяет проверить статус код ответа и вызвать исключение при ошибке.
4.  **Контекстный менеджер**: Методы `__aenter__()` и `__aexit__()` позволяют использовать `StreamResponse` как контекстный менеджер, что гарантирует закрытие соединения после завершения работы с ответом.

```
StreamResponse
│
├─── inner: Response
│
├─── text() - Асинхронно получает текст ответа
│
├─── json() - Асинхронно разбирает JSON контент ответа
│
├─── iter_lines() - Асинхронно итерируется по строкам ответа
│
├─── iter_content() - Асинхронно итерируется по содержимому ответа
│
├─── raise_for_status() - Вызывает исключение при ошибке
│
└─── __aenter__()/__aexit__() - Контекстный менеджер для управления ресурсами
```

### Как работает класс `StreamSession`:

1.  **Наследование**: Класс наследуется от `AsyncSession`, что позволяет использовать его для отправки асинхронных запросов.
2.  **Создание запроса**: Метод `request()` создает объект `StreamResponse`, который оборачивает ответ от `curl_cffi`.
3.  **HTTP методы**: Определены методы для всех основных HTTP методов (GET, POST, PUT, DELETE и т.д.).
4.  **WebSocket**: Определены методы для установки WebSocket соединения.

```
StreamSession
│
├─── AsyncSession
│
├─── request() - Создает StreamResponse для HTTP запроса
│
├─── get() - Отправляет GET запрос
│
├─── post() - Отправляет POST запрос
│
├─── put() - Отправляет PUT запрос
│
├─── delete() - Отправляет DELETE запрос
│
└─── ws_connect() - Устанавливает WebSocket соединение
```

### Как работает класс `FormData`:

1.  **Наследование**: Класс наследуется от `CurlMime`, если библиотека доступна.
2.  **Добавление полей**: Метод `add_field()` позволяет добавлять поля в форму.

```
FormData
│
└─── add_field() - Добавляет поле в форму
```

### Как работает класс `WebSocket`:

1.  **Инициализация**: При создании экземпляра `WebSocket` передается объект `StreamSession` и URL для подключения.
2.  **Установка соединения**: Метод `__aenter__()` устанавливает WebSocket соединение.
3.  **Отправка и получение данных**: Методы `send_str()` и `receive_str()` позволяют отправлять и получать данные через соединение.
4.  **Закрытие соединения**: Метод `__aexit__()` закрывает соединение при выходе из контекста менеджера.

```
WebSocket
│
├─── __aenter__() - Устанавливает WebSocket соединение
│
├─── send_str() - Отправляет строку через соединение
│
└─── receive_str() - Получает строку из соединения
```

## Примеры

### Использование `StreamSession` для отправки GET запроса:

```python
import asyncio
from curl_cffi.requests import Response
from g4f.requests import StreamSession

async def make_request():
    session = StreamSession()
    response: Response = session.get('https://example.com')
    async with response as r:
        print(r.status)
        content = await r.text()
        print(content[:100])

asyncio.run(make_request())
```

### Использование `StreamResponse` для чтения потокового ответа:

```python
import asyncio
from curl_cffi.requests import Response
from g4f.requests import StreamSession

async def read_stream():
    session = StreamSession()
    response: Response = session.get('https://example.com', stream=True)
    async with response as r:
        async for line in r.iter_lines():
            print(line)
            break

asyncio.run(read_stream())
```

### Использование `FormData` для отправки POST запроса с данными формы:

```python
import asyncio
from g4f.requests import StreamSession, FormData

async def send_form_data():
    session = StreamSession()
    form_data = FormData()
    form_data.add_field('name', 'John Doe')
    form_data.add_field('email', 'john.doe@example.com')

    response = session.post('https://example.com/submit', data=form_data)
    async with response as r:
        print(await r.text())

asyncio.run(send_form_data())
```

### Использование `WebSocket` для обмена сообщениями:

```python
import asyncio
from g4f.requests import StreamSession, WebSocket

async def use_websocket():
    session = StreamSession()
    async with WebSocket(session, 'wss://echo.websocket.org') as ws:
        await ws.send_str('Hello, WebSocket!')
        message = await ws.receive_str()
        print(f'Received: {message}')

asyncio.run(use_websocket())