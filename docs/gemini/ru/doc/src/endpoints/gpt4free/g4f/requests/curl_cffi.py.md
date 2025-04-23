# Модуль curl_cffi
## Обзор

Модуль `curl_cffi` предоставляет классы для работы с асинхронными HTTP-запросами и потоковыми ответами, включая поддержку Server-Sent Events (SSE) и WebSocket. Он использует библиотеку `curl_cffi` для эффективного выполнения сетевых операций. Модуль включает классы для управления сессиями, формирования данных формы и обработки WebSocket-соединений.

## Подробнее

Этот модуль предназначен для упрощения работы с асинхронными HTTP-запросами и потоковыми данными. Он предоставляет удобные интерфейсы для отправки различных типов запросов (GET, POST, PUT и т.д.) и обработки ответов в потоковом режиме. Поддержка SSE позволяет получать обновления в реальном времени от сервера, а поддержка WebSocket обеспечивает двустороннюю связь между клиентом и сервером.

## Классы

### `StreamResponse`

**Описание**: Класс-обертка для обработки асинхронных потоковых ответов.

**Атрибуты**:
- `inner` (Response): Оригинальный объект `Response`.

**Методы**:
- `text()`: Асинхронно получает текст ответа.
- `raise_for_status()`: Вызывает исключение `HTTPError`, если произошла ошибка.
- `json(**kwargs)`: Асинхронно разбирает содержимое JSON-ответа.
- `iter_lines()`: Асинхронно итерируется по строкам ответа.
- `iter_content()`: Асинхронно итерируется по содержимому ответа.
- `sse()`: Асинхронно итерируется по Server-Sent Events ответа.
- `__aenter__()`: Асинхронно входит в контекст выполнения для объекта ответа.
- `__aexit__(*args)`: Асинхронно выходит из контекста выполнения для объекта ответа.

### `StreamSession`

**Описание**: Асинхронный класс сессии для обработки HTTP-запросов с потоковой передачей.

**Наследует**:
- `AsyncSession`

**Методы**:
- `request(method: str, url: str, ssl = None, **kwargs) -> StreamResponse`: Создает и возвращает объект `StreamResponse` для данного HTTP-запроса.
- `ws_connect(url, *args, **kwargs)`: Устанавливает WebSocket-соединение.
- `_ws_connect(url, **kwargs)`: Выполняет установку WebSocket-соединения (внутренний метод).
- `head(url: str, ssl = None, **kwargs) -> StreamResponse`: Отправляет HEAD-запрос.
- `get(url: str, ssl = None, **kwargs) -> StreamResponse`: Отправляет GET-запрос.
- `post(url: str, ssl = None, **kwargs) -> StreamResponse`: Отправляет POST-запрос.
- `put(url: str, ssl = None, **kwargs) -> StreamResponse`: Отправляет PUT-запрос.
- `patch(url: str, ssl = None, **kwargs) -> StreamResponse`: Отправляет PATCH-запрос.
- `delete(url: str, ssl = None, **kwargs) -> StreamResponse`: Отправляет DELETE-запрос.
- `options(url: str, ssl = None, **kwargs) -> StreamResponse`: Отправляет OPTIONS-запрос.

### `FormData`

**Описание**: Класс для представления данных формы.
Если `CurlMime` доступен, наследует `CurlMime`, иначе предоставляет заглушку с исключением.

**Методы**:
- `add_field(name, data=None, content_type: str = None, filename: str = None) -> None`: Добавляет поле в данные формы.

### `WebSocket`

**Описание**: Класс для работы с WebSocket-соединениями.

**Атрибуты**:
- `session` (StreamSession): Сессия, используемая для соединения.
- `url` (str): URL WebSocket-соединения.
- `options` (dict): Дополнительные опции для соединения.

**Методы**:
- `__init__(session, url, **kwargs)`: Инициализирует объект WebSocket.
- `__aenter__()`: Асинхронно входит в контекст выполнения для объекта WebSocket.
- `__aexit__(*args)`: Асинхронно выходит из контекста выполнения для объекта WebSocket.
- `receive_str(**kwargs) -> str`: Асинхронно получает строковое сообщение.
- `send_str(data: str)`: Асинхронно отправляет строковое сообщение.

## Методы класса

### `StreamResponse`

#### `text`

```python
    async def text(self) -> str:
        """Asynchronously get the response text."""
        return await self.inner.atext()
```

**Назначение**: Асинхронно получает текст ответа.

**Параметры**:
- Нет

**Возвращает**:
- `str`: Текст ответа.

**Как работает функция**:
- Функция вызывает метод `atext()` внутреннего объекта `Response` для асинхронного получения текста ответа.

**Примеры**:

```python
async with session.get('https://example.com') as response:
    text = await response.text()
    print(text)
```

#### `raise_for_status`

```python
    def raise_for_status(self) -> None:
        """Raise an HTTPError if one occurred."""
        self.inner.raise_for_status()
```

**Назначение**: Вызывает исключение `HTTPError`, если произошла ошибка.

**Параметры**:
- Нет

**Возвращает**:
- `None`

**Как работает функция**:
- Функция вызывает метод `raise_for_status()` внутреннего объекта `Response` для проверки статуса ответа и вызова исключения в случае ошибки.

**Примеры**:

```python
async with session.get('https://example.com') as response:
    response.raise_for_status()
```

#### `json`

```python
    async def json(self, **kwargs) -> Any:
        """Asynchronously parse the JSON response content."""
        return json.loads(await self.inner.acontent(), **kwargs)
```

**Назначение**: Асинхронно разбирает содержимое JSON-ответа.

**Параметры**:
- `**kwargs`: Дополнительные параметры для `json.loads()`.

**Возвращает**:
- `Any`: Разобранное содержимое JSON-ответа.

**Как работает функция**:
- Функция вызывает метод `acontent()` внутреннего объекта `Response` для асинхронного получения содержимого ответа, а затем использует `json.loads()` для разбора содержимого как JSON.

**Примеры**:

```python
async with session.get('https://example.com/api/data') as response:
    data = await response.json()
    print(data)
```

#### `iter_lines`

```python
    def iter_lines(self) -> AsyncGenerator[bytes, None]:
        """Asynchronously iterate over the lines of the response."""
        return  self.inner.aiter_lines()
```

**Назначение**: Асинхронно итерируется по строкам ответа.

**Параметры**:
- Нет

**Возвращает**:
- `AsyncGenerator[bytes, None]`: Асинхронный генератор строк ответа.

**Как работает функция**:
- Функция возвращает асинхронный генератор, полученный вызовом метода `aiter_lines()` внутреннего объекта `Response`.

**Примеры**:

```python
async with session.get('https://example.com/large_text_file') as response:
    async for line in response.iter_lines():
        print(line)
```

#### `iter_content`

```python
    def iter_content(self) -> AsyncGenerator[bytes, None]:
        """Asynchronously iterate over the response content."""
        return self.inner.aiter_content()
```

**Назначение**: Асинхронно итерируется по содержимому ответа.

**Параметры**:
- Нет

**Возвращает**:
- `AsyncGenerator[bytes, None]`: Асинхронный генератор содержимого ответа.

**Как работает функция**:
- Функция возвращает асинхронный генератор, полученный вызовом метода `aiter_content()` внутреннего объекта `Response`.

**Примеры**:

```python
async with session.get('https://example.com/large_binary_file') as response:
    async for chunk in response.iter_content():
        print(chunk)
```

#### `sse`

```python
    async def sse(self) -> AsyncGenerator[dict, None]:
        """Asynchronously iterate over the Server-Sent Events of the response."""
        async for line in self.iter_lines():
            if line.startswith(b"data: "):\n
                chunk = line[6:]
                if chunk == b"[DONE]":
                    break
                try:
                    yield json.loads(chunk)
                except json.JSONDecodeError:
                    continue
```

**Назначение**: Асинхронно итерируется по Server-Sent Events ответа.

**Параметры**:
- Нет

**Возвращает**:
- `AsyncGenerator[dict, None]`: Асинхронный генератор событий SSE.

**Как работает функция**:
- Функция асинхронно итерируется по строкам ответа, полученным с помощью `iter_lines()`.
- Если строка начинается с `b"data: "`, она извлекает данные события и пытается разобрать их как JSON.
- Если разбор JSON успешен, функция возвращает разобранное событие.
- Если встречается `b"[DONE]"`, итерация прекращается.

**Примеры**:

```python
async with session.get('https://example.com/sse_stream') as response:
    async for event in response.sse():
        print(event)
```

#### `__aenter__`

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
- Нет

**Возвращает**:
- `self`: Объект `StreamResponse`.

**Как работает функция**:
- Функция асинхронно ожидает завершения внутреннего объекта `Response`.
- Сохраняет атрибуты внутреннего объекта `Response` в текущем объекте `StreamResponse`.

**Примеры**:

```python
async with session.get('https://example.com') as response:
    print(response.status)
```

#### `__aexit__`

```python
    async def __aexit__(self, *args):
        """Asynchronously exit the runtime context for the response object."""
        await self.inner.aclose()
```

**Назначение**: Асинхронно выходит из контекста выполнения для объекта ответа.

**Параметры**:
- `*args`: Аргументы исключения.

**Возвращает**:
- Нет

**Как работает функция**:
- Функция асинхронно закрывает внутренний объект `Response`, вызывая метод `aclose()`.

**Примеры**:

```python
async with session.get('https://example.com') as response:
    pass  # Response will be closed automatically
```

### `StreamSession`

#### `request`

```python
    def request(
        self, method: str, url: str, ssl = None, **kwargs
    ) -> StreamResponse:
        """Create and return a StreamResponse object for the given HTTP request."""
        if kwargs.get("data") and isinstance(kwargs.get("data"), CurlMime):
            kwargs["multipart"] = kwargs.pop("data")
        return StreamResponse(super().request(method, url, stream=True, verify=ssl, **kwargs))
```

**Назначение**: Создает и возвращает объект `StreamResponse` для данного HTTP-запроса.

**Параметры**:
- `method` (str): HTTP-метод (GET, POST, PUT и т.д.).
- `url` (str): URL-адрес запроса.
- `ssl`: Параметры SSL.
- `**kwargs`: Дополнительные параметры для запроса.

**Возвращает**:
- `StreamResponse`: Объект `StreamResponse`, представляющий ответ на запрос.

**Как работает функция**:
- Если в параметрах `kwargs` есть ключ `"data"` и его значение является экземпляром класса `CurlMime`, то значение ключа `"data"` удаляется и создается ключ `"multipart"` с этим же значением.
- Функция вызывает метод `request()` родительского класса `AsyncSession` с параметром `stream=True` и возвращает объект `StreamResponse`, обертывающий результат.

**Примеры**:

```python
response = session.request('GET', 'https://example.com')
```

#### `ws_connect`

```python
    def ws_connect(self, url, *args, **kwargs):
        return WebSocket(self, url, **kwargs)
```

**Назначение**: Устанавливает WebSocket-соединение.

**Параметры**:
- `url`: URL-адрес WebSocket.
- `*args`: Дополнительные позиционные аргументы.
- `**kwargs`: Дополнительные именованные аргументы.

**Возвращает**:
- `WebSocket`: Объект `WebSocket`, представляющий соединение.

**Как работает функция**:
- Функция создает и возвращает объект `WebSocket`, используя текущую сессию и предоставленный URL.

**Примеры**:

```python
async with session.ws_connect('wss://example.com') as ws:
    await ws.send_str('Hello')
```

#### `_ws_connect`

```python
    def _ws_connect(self, url, **kwargs):
        return super().ws_connect(url, **kwargs)
```

**Назначение**: Выполняет установку WebSocket-соединения (внутренний метод).

**Параметры**:
- `url`: URL-адрес WebSocket.
- `**kwargs`: Дополнительные параметры для соединения.

**Возвращает**:
- Результат вызова `super().ws_connect(url, **kwargs)`.

**Как работает функция**:
- Функция вызывает метод `ws_connect()` родительского класса `AsyncSession` с предоставленными параметрами.

**Примеры**:
```python
##  Внутренний метод. Не предназначен для непосредственного вызова
```

#### `head`

```python
    head = partialmethod(request, "HEAD")
```

**Назначение**: Отправляет HEAD-запрос.

**Параметры**:
- `url` (str): URL-адрес запроса.
- `ssl`: Параметры SSL.
- `**kwargs`: Дополнительные параметры для запроса.

**Возвращает**:
- `StreamResponse`: Объект `StreamResponse`, представляющий ответ на запрос.

**Как работает функция**:
- Использует `partialmethod` для создания метода `head`, который вызывает метод `request` с HTTP-методом "HEAD".

**Примеры**:

```python
response = session.head('https://example.com')
```

#### `get`

```python
    get = partialmethod(request, "GET")
```

**Назначение**: Отправляет GET-запрос.

**Параметры**:
- `url` (str): URL-адрес запроса.
- `ssl`: Параметры SSL.
- `**kwargs`: Дополнительные параметры для запроса.

**Возвращает**:
- `StreamResponse`: Объект `StreamResponse`, представляющий ответ на запрос.

**Как работает функция**:
- Использует `partialmethod` для создания метода `get`, который вызывает метод `request` с HTTP-методом "GET".

**Примеры**:

```python
response = session.get('https://example.com')
```

#### `post`

```python
    post = partialmethod(request, "POST")
```

**Назначение**: Отправляет POST-запрос.

**Параметры**:
- `url` (str): URL-адрес запроса.
- `ssl`: Параметры SSL.
- `**kwargs`: Дополнительные параметры для запроса.

**Возвращает**:
- `StreamResponse`: Объект `StreamResponse`, представляющий ответ на запрос.

**Как работает функция**:
- Использует `partialmethod` для создания метода `post`, который вызывает метод `request` с HTTP-методом "POST".

**Примеры**:

```python
response = session.post('https://example.com', data={'key': 'value'})
```

#### `put`

```python
    put = partialmethod(request, "PUT")
```

**Назначение**: Отправляет PUT-запрос.

**Параметры**:
- `url` (str): URL-адрес запроса.
- `ssl`: Параметры SSL.
- `**kwargs`: Дополнительные параметры для запроса.

**Возвращает**:
- `StreamResponse`: Объект `StreamResponse`, представляющий ответ на запрос.

**Как работает функция**:
- Использует `partialmethod` для создания метода `put`, который вызывает метод `request` с HTTP-методом "PUT".

**Примеры**:

```python
response = session.put('https://example.com', data={'key': 'value'})
```

#### `patch`

```python
    patch = partialmethod(request, "PATCH")
```

**Назначение**: Отправляет PATCH-запрос.

**Параметры**:
- `url` (str): URL-адрес запроса.
- `ssl`: Параметры SSL.
- `**kwargs`: Дополнительные параметры для запроса.

**Возвращает**:
- `StreamResponse`: Объект `StreamResponse`, представляющий ответ на запрос.

**Как работает функция**:
- Использует `partialmethod` для создания метода `patch`, который вызывает метод `request` с HTTP-методом "PATCH".

**Примеры**:

```python
response = session.patch('https://example.com', data={'key': 'value'})
```

#### `delete`

```python
    delete = partialmethod(request, "DELETE")
```

**Назначение**: Отправляет DELETE-запрос.

**Параметры**:
- `url` (str): URL-адрес запроса.
- `ssl`: Параметры SSL.
- `**kwargs`: Дополнительные параметры для запроса.

**Возвращает**:
- `StreamResponse`: Объект `StreamResponse`, представляющий ответ на запрос.

**Как работает функция**:
- Использует `partialmethod` для создания метода `delete`, который вызывает метод `request` с HTTP-методом "DELETE".

**Примеры**:

```python
response = session.delete('https://example.com')
```

#### `options`

```python
    options = partialmethod(request, "OPTIONS")
```

**Назначение**: Отправляет OPTIONS-запрос.

**Параметры**:
- `url` (str): URL-адрес запроса.
- `ssl`: Параметры SSL.
- `**kwargs`: Дополнительные параметры для запроса.

**Возвращает**:
- `StreamResponse`: Объект `StreamResponse`, представляющий ответ на запрос.

**Как работает функция**:
- Использует `partialmethod` для создания метода `options`, который вызывает метод `request` с HTTP-методом "OPTIONS".

**Примеры**:

```python
response = session.options('https://example.com')
```

### `FormData`

#### `add_field`

```python
        def add_field(self, name, data=None, content_type: str = None, filename: str = None) -> None:
            self.addpart(name, content_type=content_type, filename=filename, data=data)
```

**Назначение**: Добавляет поле в данные формы.

**Параметры**:
- `name`: Имя поля.
- `data`: Данные поля.
- `content_type` (str, optional): Тип содержимого.
- `filename` (str, optional): Имя файла.

**Возвращает**:
- `None`

**Как работает функция**:
- Функция вызывает метод `addpart()` для добавления поля с указанными параметрами.

**Примеры**:

```python
form_data = FormData()
form_data.add_field('name', 'John Doe')
```

### `WebSocket`

#### `__init__`

```python
    def __init__(self, session, url, **kwargs) -> None:
        if not has_curl_ws:
            raise RuntimeError("CurlWsFlag in curl_cffi is missing | pip install -U curl_cffi")
        self.session: StreamSession = session
        self.url: str = url
        del kwargs["autoping"]
        self.options: dict = kwargs
```

**Назначение**: Инициализирует объект WebSocket.

**Параметры**:
- `session`: Сессия, используемая для соединения.
- `url`: URL WebSocket-соединения.
- `**kwargs`: Дополнительные опции для соединения.

**Возвращает**:
- `None`

**Как работает функция**:
- Проверяет наличие `CurlWsFlag` и вызывает исключение, если он отсутствует.
- Сохраняет сессию, URL и опции соединения.
- Удаляет параметр `"autoping"` из опций.

**Примеры**:
```python
# Пример создания инстанса класса
async with StreamSession() as session:
    async with WebSocket(session, 'wss://echo.websocket.org', extra_headers={'Authorization': 'Bearer token'}) as websocket:
        # ...
        pass
```

#### `__aenter__`

```python
    async def __aenter__(self):
        self.inner = await self.session._ws_connect(self.url, **self.options)
        return self
```

**Назначение**: Асинхронно входит в контекст выполнения для объекта WebSocket.

**Параметры**:
- Нет

**Возвращает**:
- `self`: Объект `WebSocket`.

**Как работает функция**:
- Функция асинхронно устанавливает WebSocket-соединение, вызывая метод `_ws_connect()` сессии и возвращает объект `WebSocket`.

**Примеры**:
```python
# Пример работы с классом в контексте async with
async with StreamSession() as session:
    async with WebSocket(session, 'wss://echo.websocket.org', extra_headers={'Authorization': 'Bearer token'}) as websocket:
        # ...
        pass
```

#### `__aexit__`

```python
    async def __aexit__(self, *args):
        await self.inner.aclose() if hasattr(self.inner, "aclose") else await self.inner.close()
```

**Назначение**: Асинхронно выходит из контекста выполнения для объекта WebSocket.

**Параметры**:
- `*args`: Аргументы исключения.

**Возвращает**:
- Нет

**Как работает функция**:
- Функция асинхронно закрывает WebSocket-соединение, вызывая метод `aclose()`, если он существует, иначе вызывает метод `close()`.

**Примеры**:
```python
# Пример выхода из контеста async with.
async with StreamSession() as session:
    async with WebSocket(session, 'wss://echo.websocket.org', extra_headers={'Authorization': 'Bearer token'}) as websocket:
        # ...
        pass #При выходе из конеткста соединение будет закрыто.
```

#### `receive_str`

```python
    async def receive_str(self, **kwargs) -> str:
        method = self.inner.arecv if hasattr(self.inner, "arecv") else self.inner.recv
        bytes, _ = await method()
        return bytes.decode(errors="ignore")
```

**Назначение**: Асинхронно получает строковое сообщение.

**Параметры**:
- `**kwargs`: Дополнительные параметры для получения сообщения.

**Возвращает**:
- `str`: Полученное строковое сообщение.

**Как работает функция**:
- Функция асинхронно получает сообщение, вызывая метод `arecv()` или `recv()` внутреннего объекта соединения.
- Декодирует полученные байты в строку, игнорируя ошибки декодирования.

**Примеры**:
```python
# Пример получения данных из websocket
async with StreamSession() as session:
    async with WebSocket(session, 'wss://echo.websocket.org', extra_headers={'Authorization': 'Bearer token'}) as websocket:
        data = await websocket.receive_str()
        print(data)
```

#### `send_str`

```python
    async def send_str(self, data: str):
        method = self.inner.asend if hasattr(self.inner, "asend") else self.inner.send
        await method(data.encode(), CurlWsFlag.TEXT)
```

**Назначение**: Асинхронно отправляет строковое сообщение.

**Параметры**:
- `data` (str): Строковое сообщение для отправки.

**Возвращает**:
- Нет

**Как работает функция**:
- Функция асинхронно отправляет строковое сообщение, вызывая метод `asend()` или `send()` внутреннего объекта соединения.
- Кодирует строку в байты, используя кодировку UTF-8.

**Примеры**:
```python
# Пример отправки данных в websocket
async with StreamSession() as session:
    async with WebSocket(session, 'wss://echo.websocket.org', extra_headers={'Authorization': 'Bearer token'}) as websocket:
        await websocket.send_str('Hello, WebSocket!')