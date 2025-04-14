# Модуль для асинхронной работы с HTTP-запросами и WebSocket с использованием `curl_cffi`
=========================================================================================

Модуль предоставляет классы для асинхронной отправки HTTP-запросов с поддержкой потоковой передачи данных,
а также для установки WebSocket-соединений. Использует библиотеку `curl_cffi` для эффективной работы с HTTP и WebSocket.

## Обзор

Модуль содержит классы:

- `StreamResponse`: Обертка для асинхронных потоковых ответов.
- `StreamSession`: Асинхронная сессия для выполнения HTTP-запросов с потоковой передачей.
- `FormData`: Класс для создания данных формы (multipart/form-data) для HTTP-запросов.
- `WebSocket`: Класс для работы с WebSocket-соединениями.

## Подробнее

Этот модуль предназначен для использования в асинхронных приложениях, требующих эффективной обработки HTTP-запросов и WebSocket-соединений.
Он предоставляет удобные интерфейсы для работы с потоковыми данными и поддерживает создание сложных форм данных.

## Классы

### `StreamResponse`

**Описание**: Обертка для асинхронного ответа, обеспечивающая удобный доступ к потоковым данным.

**Принцип работы**: Этот класс оборачивает объект `Response` из `curl_cffi` и предоставляет асинхронные методы для чтения текста, JSON и итерации по строкам или содержимому ответа.

**Атрибуты**:

- `inner` (Response): Оригинальный объект `Response`.
- `url` (str): URL запроса.
- `method` (str): HTTP-метод запроса.
- `request (Request)`: Объект запроса.
- `status` (int): HTTP-код статуса ответа.
- `reason` (str): Описание статуса ответа.
- `ok` (bool): Флаг, указывающий на успешность запроса (статус код < 400).
- `headers`: (Headers): Заголовки ответа.
- `cookies`: (Cookies): Куки ответа.

**Методы**:

- `__init__(self, inner: Response) -> None`: Инициализирует объект `StreamResponse` предоставленным объектом `Response`.
- `text(self) -> str`: Асинхронно получает текст ответа.
- `raise_for_status(self) -> None`: Вызывает исключение `HTTPError`, если произошла ошибка HTTP.
- `json(self, **kwargs) -> Any`: Асинхронно преобразует содержимое ответа JSON в объект Python.
- `iter_lines(self) -> AsyncGenerator[bytes, None]`: Асинхронно итерируется по строкам ответа.
- `iter_content(self) -> AsyncGenerator[bytes, None]`: Асинхронно итерируется по содержимому ответа.
- `sse(self) -> AsyncGenerator[dict, None]`: Асинхронно итерируется по событиям, отправленным сервером (Server-Sent Events).
- `__aenter__(self)`: Асинхронно входит в контекст выполнения для объекта ответа.
- `__aexit__(self, *args)`: Асинхронно выходит из контекста выполнения для объекта ответа, закрывая соединение.

### `StreamSession`

**Описание**: Асинхронная сессия для обработки HTTP-запросов с потоковой передачей.

**Наследует**:

- `AsyncSession`

**Принцип работы**: Этот класс наследуется от `AsyncSession` и предоставляет метод `request`, который возвращает объект `StreamResponse` для обработки потоковых ответов.

**Методы**:

- `request(self, method: str, url: str, ssl=None, **kwargs) -> StreamResponse`: Создает и возвращает объект `StreamResponse` для заданного HTTP-запроса.
- `ws_connect(self, url, *args, **kwargs)`: Устанавливает WebSocket-соединение по указанному URL.
- `_ws_connect(self, url, **kwargs)`: Внутренний метод для установки WebSocket-соединения.
- `head = partialmethod(request, "HEAD")`: Отправляет HTTP-запрос методом HEAD.
- `get = partialmethod(request, "GET")`: Отправляет HTTP-запрос методом GET.
- `post = partialmethod(request, "POST")`: Отправляет HTTP-запрос методом POST.
- `put = partialmethod(request, "PUT")`: Отправляет HTTP-запрос методом PUT.
- `patch = partialmethod(request, "PATCH")`: Отправляет HTTP-запрос методом PATCH.
- `delete = partialmethod(request, "DELETE")`: Отправляет HTTP-запрос методом DELETE.
- `options = partialmethod(request, "OPTIONS")`: Отправляет HTTP-запрос методом OPTIONS.

### `FormData`

**Описание**: Класс для создания данных формы (multipart/form-data) для HTTP-запросов.

**Принцип работы**:
Если библиотека `curl_cffi` поддерживает `CurlMime`, класс `FormData` наследуется от `CurlMime` и использует его для создания данных формы.
В противном случае, класс `FormData` вызывает исключение, указывающее на необходимость установки `curl_cffi`.

**Методы**:

- `add_field(self, name, data=None, content_type: str = None, filename: str = None) -> None`: Добавляет поле в форму данных.

### `WebSocket`

**Описание**: Класс для работы с WebSocket-соединениями.

**Принцип работы**: Этот класс позволяет устанавливать и использовать WebSocket-соединения для обмена данными в реальном времени.

**Атрибуты**:

- `session` (StreamSession): Асинхронная сессия, используемая для установки соединения.
- `url` (str): URL WebSocket-сервера.
- `options` (dict): Дополнительные параметры для установки соединения.

**Методы**:

- `__init__(self, session, url, **kwargs) -> None`: Инициализирует объект `WebSocket`.
- `__aenter__(self)`: Асинхронно входит в контекст выполнения для объекта WebSocket, устанавливая соединение.
- `__aexit__(self, *args)`: Асинхронно выходит из контекста выполнения для объекта WebSocket, закрывая соединение.
- `receive_str(self, **kwargs) -> str`: Асинхронно получает строковое сообщение из WebSocket-соединения.
- `send_str(self, data: str)`: Асинхронно отправляет строковое сообщение через WebSocket-соединение.

## Функции

В данном модуле функции отсутствуют. Присутствуют только методы классов.

### `StreamResponse.text`

```python
async def text(self) -> str:
    """Asynchronously get the response text."""
    return await self.inner.atext()
```

**Назначение**: Асинхронно получает текст ответа из `Response`.

**Параметры**:

- Отсутствуют.

**Возвращает**:

- `str`: Текст ответа.

**Как работает функция**:

1. Функция вызывает метод `atext()` объекта `self.inner` (типа `Response`), который асинхронно получает текстовое содержимое ответа.
2. Возвращает полученный текст.

```
    Начало
     ↓
    Получение текста ответа
     ↓
    Возврат текста
     ↓
    Конец
```

**Примеры**:

```python
async with session.get('https://example.com') as response:
    text = await response.text()
    print(text)
```

### `StreamResponse.raise_for_status`

```python
def raise_for_status(self) -> None:
    """Raise an HTTPError if one occurred."""
    self.inner.raise_for_status()
```

**Назначение**: Вызывает исключение `HTTPError`, если произошла ошибка HTTP.

**Параметры**:

- Отсутствуют.

**Возвращает**:

- `None`: Функция ничего не возвращает.

**Как работает функция**:

1. Функция вызывает метод `raise_for_status()` объекта `self.inner` (типа `Response`), который проверяет статус код ответа.
2. Если статус код указывает на ошибку (например, 404, 500), то вызывается исключение `HTTPError`.

```
    Начало
     ↓
    Проверка статуса ответа
     ↓
    Вызов исключения (если ошибка)
     ↓
    Конец
```

**Примеры**:

```python
async with session.get('https://example.com') as response:
    response.raise_for_status()  # Вызовет исключение, если статус код >= 400
```

### `StreamResponse.json`

```python
async def json(self, **kwargs) -> Any:
    """Asynchronously parse the JSON response content."""
    return json.loads(await self.inner.acontent(), **kwargs)
```

**Назначение**: Асинхронно преобразует содержимое ответа JSON в объект Python.

**Параметры**:

- `**kwargs`: Дополнительные параметры, передаваемые в `json.loads()`.

**Возвращает**:

- `Any`: Объект Python, полученный из JSON.

**Как работает функция**:

1. Функция асинхронно получает содержимое ответа с помощью `await self.inner.acontent()`.
2. Преобразует полученное содержимое JSON в объект Python с помощью `json.loads()`.
3. Возвращает полученный объект.

```
    Начало
     ↓
    Получение содержимого ответа
     ↓
    Преобразование JSON в объект Python
     ↓
    Возврат объекта
     ↓
    Конец
```

**Примеры**:

```python
async with session.get('https://example.com/api/data') as response:
    data = await response.json()
    print(data)
```

### `StreamResponse.iter_lines`

```python
def iter_lines(self) -> AsyncGenerator[bytes, None]:
    """Asynchronously iterate over the lines of the response."""
    return  self.inner.aiter_lines()
```

**Назначение**: Асинхронно итерируется по строкам ответа.

**Параметры**:

- Отсутствуют.

**Возвращает**:

- `AsyncGenerator[bytes, None]`: Асинхронный генератор, возвращающий строки ответа в виде байтов.

**Как работает функция**:

1. Функция возвращает асинхронный генератор `self.inner.aiter_lines()`, который позволяет итерироваться по строкам ответа.

```
    Начало
     ↓
    Возврат асинхронного генератора строк
     ↓
    Конец
```

**Примеры**:

```python
async with session.get('https://example.com') as response:
    async for line in response.iter_lines():
        print(line)
```

### `StreamResponse.iter_content`

```python
def iter_content(self) -> AsyncGenerator[bytes, None]:
    """Asynchronously iterate over the response content."""
    return self.inner.aiter_content()
```

**Назначение**: Асинхронно итерируется по содержимому ответа.

**Параметры**:

- Отсутствуют.

**Возвращает**:

- `AsyncGenerator[bytes, None]`: Асинхронный генератор, возвращающий содержимое ответа в виде байтов.

**Как работает функция**:

1. Функция возвращает асинхронный генератор `self.inner.aiter_content()`, который позволяет итерироваться по содержимому ответа.

```
    Начало
     ↓
    Возврат асинхронного генератора содержимого
     ↓
    Конец
```

**Примеры**:

```python
async with session.get('https://example.com/image.jpg') as response:
    async for chunk in response.iter_content():
        # Обработка каждого чанка содержимого
        print(chunk)
```

### `StreamResponse.sse`

```python
async def sse(self) -> AsyncGenerator[dict, None]:
    """Asynchronously iterate over the Server-Sent Events of the response."""
    async for line in self.iter_lines():
        if line.startswith(b"data: ")):
            chunk = line[6:]
            if chunk == b"[DONE]":
                break
            try:
                yield json.loads(chunk)
            except json.JSONDecodeError:
                continue
```

**Назначение**: Асинхронно итерируется по событиям, отправленным сервером (Server-Sent Events).

**Параметры**:

- Отсутствуют.

**Возвращает**:

- `AsyncGenerator[dict, None]`: Асинхронный генератор, возвращающий события в виде словарей.

**Как работает функция**:

1. Функция асинхронно итерируется по строкам ответа с помощью `self.iter_lines()`.
2. Для каждой строки проверяется, начинается ли она с префикса `b"data: "`.
3. Если строка начинается с `b"data: "`, извлекается содержимое события (часть строки после префикса).
4. Если содержимое события равно `b"[DONE]"`, итерация прекращается.
5. Содержимое события преобразуется из JSON в объект Python с помощью `json.loads()`.
6. Полученный объект возвращается через `yield`.
7. Если при преобразовании JSON возникает ошибка `json.JSONDecodeError`, итерация продолжается.

```
    Начало
     ↓
    Итерация по строкам ответа
     ↓
    Проверка префикса "data: "
     ├── Да → Извлечение содержимого события
     │       ↓
     │       Проверка содержимого "[DONE]"
     │       ├── Да → Завершение итерации
     │       └── Нет → Преобразование JSON в объект Python
     │                   ├── Успех → Возврат объекта
     │                   └── Ошибка → Продолжение итерации
     └── Нет → Продолжение итерации
     ↓
    Конец
```

**Примеры**:

```python
async with session.get('https://example.com/events', stream=True) as response:
    async for event in response.sse():
        print(event)
```

### `StreamResponse.__aenter__`

```python
async def __aenter__(self):
    """Asynchronously enter the runtime context for the response object."""
    inner: Response = await self.inner
    self.inner = inner
    self.url = inner.url
    self.method = inner.request.method
    self.request = inner.request
    self.status: int = inner.status_code
    self.reason: str = inner.reason
    self.ok: bool = inner.ok
    self.headers = inner.headers
    self.cookies = inner.cookies
    return self
```

**Назначение**: Асинхронно входит в контекст выполнения для объекта ответа.

**Параметры**:

- Отсутствуют.

**Возвращает**:

- `self`: Объект `StreamResponse`.

**Как работает функция**:

1. Асинхронно ожидает завершения получения объекта `Response` из `self.inner`.
2. Обновляет `self.inner` полученным объектом `Response`.
3. Сохраняет атрибуты объекта `Response` (URL, метод, статус, заголовки, куки) в атрибуты `StreamResponse`.
4. Возвращает `self`.

```
    Начало
     ↓
    Ожидание получения объекта Response
     ↓
    Обновление self.inner
     ↓
    Сохранение атрибутов Response в StreamResponse
     ↓
    Возврат self
     ↓
    Конец
```

**Примеры**:

```python
async with session.get('https://example.com') as response:
    print(response.status)
```

### `StreamResponse.__aexit__`

```python
async def __aexit__(self, *args):
    """Asynchronously exit the runtime context for the response object."""
    await self.inner.aclose()
```

**Назначение**: Асинхронно выходит из контекста выполнения для объекта ответа.

**Параметры**:

- `*args`: Аргументы, передаваемые при выходе из контекста выполнения.

**Возвращает**:

- Отсутствует.

**Как работает функция**:

1. Асинхронно закрывает соединение, вызвав метод `aclose()` объекта `self.inner`.

```
    Начало
     ↓
    Закрытие соединения
     ↓
    Конец
```

**Примеры**:

```python
async with session.get('https://example.com') as response:
    # Действия с ответом
    pass  # Соединение будет автоматически закрыто при выходе из блока async with
```

### `StreamSession.request`

```python
def request(
    self, method: str, url: str, ssl = None, **kwargs
) -> StreamResponse:
    if kwargs.get("data") and isinstance(kwargs.get("data"), CurlMime):
        kwargs["multipart"] = kwargs.pop("data")
    """Create and return a StreamResponse object for the given HTTP request."""
    return StreamResponse(super().request(method, url, stream=True, verify=ssl, **kwargs))
```

**Назначение**: Создает и возвращает объект `StreamResponse` для заданного HTTP-запроса.

**Параметры**:

- `method` (str): HTTP-метод запроса (GET, POST, PUT и т.д.).
- `url` (str): URL запроса.
- `ssl`: Параметры SSL. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры, передаваемые в метод `super().request()`.

**Возвращает**:

- `StreamResponse`: Объект `StreamResponse`, представляющий ответ на запрос.

**Как работает функция**:

1. Если параметр `data` передан в `kwargs` и является экземпляром `CurlMime`, он заменяется на параметр `multipart`.
2. Вызывает метод `super().request()` (метод класса `AsyncSession`) с параметром `stream=True` для получения потокового ответа.
3. Создает объект `StreamResponse`, оборачивающий полученный потоковый ответ.
4. Возвращает объект `StreamResponse`.

```
    Начало
     ↓
    Проверка наличия и типа параметра data
     ├── Да → Замена data на multipart
     └── Нет → Продолжение
     ↓
    Вызов super().request() с stream=True
     ↓
    Создание объекта StreamResponse
     ↓
    Возврат объекта StreamResponse
     ↓
    Конец
```

**Примеры**:

```python
async with StreamSession() as session:
    response = session.request('GET', 'https://example.com')
    async with response:
        print(response.status)
```

### `StreamSession.ws_connect`

```python
def ws_connect(self, url, *args, **kwargs):
    return WebSocket(self, url, **kwargs)
```

**Назначение**: Устанавливает WebSocket-соединение по указанному URL.

**Параметры**:

- `url` (str): URL WebSocket-сервера.
- `*args`: Дополнительные позиционные аргументы.
- `**kwargs`: Дополнительные параметры, передаваемые в конструктор класса `WebSocket`.

**Возвращает**:

- `WebSocket`: Объект `WebSocket`, представляющий WebSocket-соединение.

**Как работает функция**:

1. Создает объект `WebSocket` с использованием текущей сессии, URL и дополнительных параметров.
2. Возвращает объект `WebSocket`.

```
    Начало
     ↓
    Создание объекта WebSocket
     ↓
    Возврат объекта WebSocket
     ↓
    Конец
```

**Примеры**:

```python
async with StreamSession() as session:
    async with session.ws_connect('wss://example.com') as ws:
        await ws.send_str('Hello, WebSocket!')
```

### `StreamSession._ws_connect`

```python
def _ws_connect(self, url, **kwargs):
    return super().ws_connect(url, **kwargs)
```

**Назначение**: Внутренний метод для установки WebSocket-соединения.

**Параметры**:

- `url` (str): URL WebSocket-сервера.
- `**kwargs`: Дополнительные параметры, передаваемые в метод `super().ws_connect()`.

**Возвращает**:

- Результат вызова `super().ws_connect()`.

**Как работает функция**:

1. Вызывает метод `super().ws_connect()` (метод класса `AsyncSession`) с переданными параметрами.
2. Возвращает результат вызова.

```
    Начало
     ↓
    Вызов super().ws_connect()
     ↓
    Возврат результата
     ↓
    Конец
```

**Примеры**:

```python
async with StreamSession() as session:
    ws = await session._ws_connect('wss://example.com')
    await ws.send('Hello')
```

### `FormData.add_field`

```python
def add_field(self, name, data=None, content_type: str = None, filename: str = None) -> None:
    self.addpart(name, content_type=content_type, filename=filename, data=data)
```

**Назначение**: Добавляет поле в форму данных.

**Параметры**:

- `name` (str): Имя поля.
- `data`: Данные поля. По умолчанию `None`.
- `content_type` (str): Тип содержимого поля. По умолчанию `None`.
- `filename` (str): Имя файла, связанного с полем. По умолчанию `None`.

**Возвращает**:

- `None`: Функция ничего не возвращает.

**Как работает функция**:

1. Вызывает метод `self.addpart()` для добавления поля в форму данных с указанными параметрами.

```
    Начало
     ↓
    Вызов self.addpart()
     ↓
    Конец
```

**Примеры**:

```python
form = FormData()
form.add_field('name', 'John Doe')
form.add_field('file', data=b'file content', filename='example.txt')
```

### `WebSocket.__aenter__`

```python
async def __aenter__(self):
    self.inner = await self.session._ws_connect(self.url, **self.options)
    return self
```

**Назначение**: Асинхронно входит в контекст выполнения для объекта WebSocket, устанавливая соединение.

**Параметры**:

- Отсутствуют.

**Возвращает**:

- `self`: Объект `WebSocket`.

**Как работает функция**:

1. Асинхронно устанавливает WebSocket-соединение, вызвав метод `self.session._ws_connect()` с URL и параметрами соединения.
2. Сохраняет объект, представляющий внутреннее состояние соединения в `self.inner`.
3. Возвращает `self`.

```
    Начало
     ↓
    Установка WebSocket-соединения
     ↓
    Сохранение внутреннего состояния соединения
     ↓
    Возврат self
     ↓
    Конец
```

**Примеры**:

```python
async with StreamSession() as session:
    async with session.ws_connect('wss://example.com', autoping=False) as ws:
        await ws.send_str('Hello, WebSocket!')
```

### `WebSocket.__aexit__`

```python
async def __aexit__(self, *args):
    await self.inner.aclose() if hasattr(self.inner, "aclose") else await self.inner.close()
```

**Назначение**: Асинхронно выходит из контекста выполнения для объекта WebSocket, закрывая соединение.

**Параметры**:

- `*args`: Аргументы, передаваемые при выходе из контекста выполнения.

**Возвращает**:

- Отсутствует.

**Как работает функция**:

1. Проверяет, имеет ли объект `self.inner` метод `aclose()`.
2. Если метод `aclose()` существует, он вызывается асинхронно для закрытия соединения.
3. Если метод `aclose()` не существует, вызывается метод `close()` для закрытия соединения.

```
    Начало
     ↓
    Проверка наличия метода aclose()
     ├── Да → Вызов aclose()
     └── Нет → Вызов close()
     ↓
    Конец
```

**Примеры**:

```python
async with StreamSession() as session:
    async with session.ws_connect('wss://example.com', autoping=False) as ws:
        await ws.send_str('Hello, WebSocket!')
    # Соединение будет автоматически закрыто при выходе из блока async with
```

### `WebSocket.receive_str`

```python
async def receive_str(self, **kwargs) -> str:
    method = self.inner.arecv if hasattr(self.inner, "arecv") else self.inner.recv
    bytes, _ = await method()
    return bytes.decode(errors="ignore")
```

**Назначение**: Асинхронно получает строковое сообщение из WebSocket-соединения.

**Параметры**:

- `**kwargs`: Дополнительные параметры.

**Возвращает**:

- `str`: Строковое сообщение, полученное из соединения.

**Как работает функция**:

1. Определяет метод для получения данных (`arecv` или `recv`) в зависимости от наличия метода `arecv` у объекта `self.inner`.
2. Асинхронно получает данные, вызвав выбранный метод.
3. Декодирует полученные байты в строку, игнорируя ошибки декодирования.
4. Возвращает полученную строку.

```
    Начало
     ↓
    Определение метода для получения данных (arecv или recv)
     ↓
    Асинхронное получение данных
     ↓
    Декодирование байтов в строку
     ↓
    Возврат строки
     ↓
    Конец
```

**Примеры**:

```python
async with StreamSession() as session:
    async with session.ws_connect('wss://example.com', autoping=False) as ws:
        message = await ws.receive_str()
        print(message)
```

### `WebSocket.send_str`

```python
async def send_str(self, data: str):
    method = self.inner.asend if hasattr(self.inner, "asend") else self.inner.send
    await method(data.encode(), CurlWsFlag.TEXT)
```

**Назначение**: Асинхронно отправляет строковое сообщение через WebSocket-соединение.

**Параметры**:

- `data` (str): Строковое сообщение для отправки.

**Возвращает**:

- Отсутствует.

**Как работает функция**:

1. Определяет метод для отправки данных (`asend` или `send`) в зависимости от наличия метода `asend` у объекта `self.inner`.
2. Кодирует строку `data` в байты.
3. Асинхронно отправляет закодированные данные через WebSocket-соединение с указанием типа `CurlWsFlag.TEXT`.

```
    Начало
     ↓
    Определение метода для отправки данных (asend или send)
     ↓
    Кодирование строки в байты
     ↓
    Асинхронная отправка данных
     ↓
    Конец
```

**Примеры**:

```python
async with StreamSession() as session:
    async with session.ws_connect('wss://example.com', autoping=False) as ws:
        await ws.send_str('Hello, WebSocket!')