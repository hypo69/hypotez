# Модуль curl_cffi.requests.curl_cffi

## Обзор

Модуль `curl_cffi.requests.curl_cffi` предоставляет набор классов и функций для работы с HTTP-запросами с помощью библиотеки `curl_cffi`. Модуль позволяет осуществлять как синхронные, так и асинхронные запросы, а также обрабатывать потоковые ответы.

## Подробней

Модуль `curl_cffi.requests.curl_cffi` предоставляет асинхронные сессии (`StreamSession`), а также класс `StreamResponse` для работы с потоковыми ответами.

## Классы

### `class StreamResponse`

**Описание**: Класс `StreamResponse` представляет собой обертку для обработки асинхронных потоковых ответов.

**Наследует**: `Response` (from `curl_cffi`)

**Атрибуты**:
- `inner` (Response): Исходный объект `Response`

**Методы**:
- `text()`:  Асинхронно получает текст ответа.
- `raise_for_status()`: Поднимает исключение `HTTPError`, если оно произошло.
- `json()`:  Асинхронно разбирает JSON-контент ответа.
- `iter_lines()`: Асинхронно итерирует по строкам ответа.
- `iter_content()`: Асинхронно итерирует по содержимому ответа.
- `sse()`: Асинхронно итерирует по событиям Server-Sent Events ответа.
- `__aenter__()`: Асинхронный вход в контекстный менеджер для объекта ответа.
- `__aexit__()`: Асинхронный выход из контекстного менеджера для объекта ответа.

**Примеры**:

```python
# Получение текста ответа
response_text = await response.text()
# Получение JSON-контента ответа
response_json = await response.json()
# Итерация по строкам ответа
async for line in response.iter_lines():
    print(line)
# Итерация по содержимому ответа
async for chunk in response.iter_content():
    print(chunk)
```

### `class StreamSession`

**Описание**: Асинхронный класс сессии для обработки HTTP-запросов с потоковой передачей.

**Наследует**: `AsyncSession` (from `curl_cffi`)

**Атрибуты**:

**Методы**:

- `request(method: str, url: str, ssl = None, **kwargs) -> StreamResponse`: Создает и возвращает объект `StreamResponse` для заданного HTTP-запроса.
- `ws_connect(url, *args, **kwargs) -> WebSocket`:  Создает соединение WebSocket.
- `_ws_connect(url, **kwargs)`:  Использует родительский метод `ws_connect` для создания соединения.
- `head`:  Частичный метод `request` для метода HEAD.
- `get`:  Частичный метод `request` для метода GET.
- `post`:  Частичный метод `request` для метода POST.
- `put`:  Частичный метод `request` для метода PUT.
- `patch`:  Частичный метод `request` для метода PATCH.
- `delete`:  Частичный метод `request` для метода DELETE.
- `options`:  Частичный метод `request` для метода OPTIONS.

**Примеры**:

```python
# Создание StreamSession
session = StreamSession()
# Выполнение HTTP-запроса
async with session.get("https://example.com") as response:
    print(response.status_code)
# Создание соединения WebSocket
async with session.ws_connect("ws://example.com") as websocket:
    await websocket.send_str("Hello")
    message = await websocket.receive_str()
    print(message)
```

### `class FormData`

**Описание**: Класс `FormData` используется для создания форм данных для HTTP-запросов.

**Наследует**: `CurlMime` (from `curl_cffi`)

**Атрибуты**:

**Методы**:
- `add_field(name, data=None, content_type: str = None, filename: str = None) -> None`: Добавляет поле в форму данных.

**Примеры**:

```python
# Создание объекта FormData
form_data = FormData()
# Добавление поля в форму
form_data.add_field("name", "John Doe")
# Добавление файла в форму
form_data.add_field("file", open("file.txt", "rb"), content_type="text/plain", filename="file.txt")
# Выполнение HTTP-запроса с формой данных
async with session.post("https://example.com/upload", data=form_data) as response:
    print(response.status_code)
```

### `class WebSocket`

**Описание**: Класс `WebSocket` используется для работы с соединениями WebSocket.

**Атрибуты**:
- `session`:  Объект `StreamSession`.
- `url`:  URL WebSocket-сервера.
- `options`:  Словарь опций соединения.

**Методы**:
- `__aenter__()`:  Асинхронный вход в контекстный менеджер для объекта WebSocket.
- `__aexit__()`:  Асинхронный выход из контекстного менеджера для объекта WebSocket.
- `receive_str()`:  Асинхронно получает строку данных от WebSocket-сервера.
- `send_str()`:  Асинхронно отправляет строку данных на WebSocket-сервер.

**Примеры**:

```python
# Создание объекта WebSocket
websocket = session.ws_connect("ws://example.com")
# Подключение к WebSocket-серверу
async with websocket:
    # Отправка сообщения
    await websocket.send_str("Hello")
    # Получение сообщения
    message = await websocket.receive_str()
    print(message)
```

## Внутренние функции

## Как работает модуль

## Примеры

## Дополнительные сведения