# Модуль curl_cffi.requests.curl_cffi

## Обзор

Модуль предоставляет классы для работы с асинхронными потоковыми HTTP-запросами, используя библиотеку `curl_cffi`. Он включает поддержку потоковых ответов, форм данных и WebSocket соединений.

## Подробнее

Модуль содержит классы `StreamResponse`, `StreamSession`, `FormData` и `WebSocket`, которые позволяют выполнять асинхронные HTTP-запросы с потоковой передачей данных, обрабатывать ответы, создавать и отправлять формы данных, а также устанавливать и поддерживать WebSocket соединения. Модуль обеспечивает удобный интерфейс для работы с `curl_cffi` в асинхронном режиме.

## Классы

### `StreamResponse`

**Описание**: Класс-обертка для обработки асинхронных потоковых ответов.

**Атрибуты**:
- `inner` (Response): Оригинальный объект `Response`.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `StreamResponse`.
- `text`: Асинхронно получает текст ответа.
- `raise_for_status`: Вызывает исключение `HTTPError`, если произошла ошибка.
- `json`: Асинхронно разбирает содержимое JSON ответа.
- `iter_lines`: Асинхронно итерирует по строкам ответа.
- `iter_content`: Асинхронно итерирует по содержимому ответа.
- `sse`: Асинхронно итерирует по событиям, отправленным сервером (Server-Sent Events).
- `__aenter__`: Асинхронно входит в контекст выполнения для объекта ответа.
- `__aexit__`: Асинхронно выходит из контекста выполнения для объекта ответа.

### `StreamSession`

**Описание**: Асинхронный класс сессии для обработки HTTP-запросов с потоковой передачей данных.

**Наследует**:
- `AsyncSession`

**Методы**:
- `request`: Создает и возвращает объект `StreamResponse` для заданного HTTP-запроса.
- `ws_connect`: Устанавливает WebSocket соединение.
- `_ws_connect`: Внутренний метод для установки WebSocket соединения.
- `head`: Отправляет HTTP-запрос методом HEAD.
- `get`: Отправляет HTTP-запрос методом GET.
- `post`: Отправляет HTTP-запрос методом POST.
- `put`: Отправляет HTTP-запрос методом PUT.
- `patch`: Отправляет HTTP-запрос методом PATCH.
- `delete`: Отправляет HTTP-запрос методом DELETE.
- `options`: Отправляет HTTP-запрос методом OPTIONS.

### `FormData`

**Описание**: Класс для создания и управления формами данных.

**Условия**:
- Если `curl_cffi.CurlMime` доступен, наследует `CurlMime`. Иначе предоставляет заглушку.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `FormData`.
- `add_field`: Добавляет поле в форму данных.

### `WebSocket`

**Описание**: Класс для работы с WebSocket соединениями.

**Атрибуты**:
- `session` (StreamSession): Объект сессии.
- `url` (str): URL для подключения.
- `options` (dict): Опции подключения.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `WebSocket`.
- `__aenter__`: Асинхронно входит в контекст выполнения для объекта WebSocket.
- `__aexit__`: Асинхронно выходит из контекста выполнения для объекта WebSocket.
- `receive_str`: Асинхронно получает строковые данные из WebSocket соединения.
- `send_str`: Асинхронно отправляет строковые данные через WebSocket соединение.

## Методы классов

### `StreamResponse`

#### `__init__`

```python
def __init__(self, inner: Response) -> None:
    """
    Инициализирует объект StreamResponse с предоставленным объектом Response.

    Args:
        inner (Response): Объект Response, который будет обернут.
    """
    ...
```

#### `text`

```python
async def text(self) -> str:
    """
    Асинхронно получает текст ответа.

    Returns:
        str: Текст ответа.
    """
    ...
```

#### `raise_for_status`

```python
def raise_for_status(self) -> None:
    """
    Вызывает исключение HTTPError, если произошла ошибка.
    """
    ...
```

#### `json`

```python
async def json(self, **kwargs) -> Any:
    """
    Асинхронно разбирает содержимое JSON ответа.

    Args:
        **kwargs: Дополнительные аргументы, передаваемые в json.loads.

    Returns:
        Any: Разобранное содержимое JSON.
    """
    ...
```

#### `iter_lines`

```python
def iter_lines(self) -> AsyncGenerator[bytes, None]:
    """
    Асинхронно итерирует по строкам ответа.

    Returns:
        AsyncGenerator[bytes, None]: Асинхронный генератор строк ответа.
    """
    ...
```

#### `iter_content`

```python
def iter_content(self) -> AsyncGenerator[bytes, None]:
    """
    Асинхронно итерирует по содержимому ответа.

    Returns:
        AsyncGenerator[bytes, None]: Асинхронный генератор содержимого ответа.
    """
    ...
```

#### `sse`

```python
async def sse(self) -> AsyncGenerator[dict, None]:
    """
    Асинхронно итерирует по событиям, отправленным сервером (Server-Sent Events) ответа.

    Yields:
        dict: Событие, отправленное сервером.
    """
    ...
```

#### `__aenter__`

```python
async def __aenter__(self):
    """
    Асинхронно входит в контекст выполнения для объекта ответа.

    Returns:
        self: Объект StreamResponse.
    """
    ...
```

#### `__aexit__`

```python
async def __aexit__(self, *args):
    """
    Асинхронно выходит из контекста выполнения для объекта ответа.

    Args:
        *args: Аргументы для выхода из контекста.
    """
    ...
```

### `StreamSession`

#### `request`

```python
def request(
    self, method: str, url: str, ssl = None, **kwargs
) -> StreamResponse:
    """
    Создает и возвращает объект StreamResponse для заданного HTTP-запроса.

    Args:
        method (str): HTTP метод запроса (GET, POST, и т.д.).
        url (str): URL запроса.
        ssl: Параметры SSL.
        **kwargs: Дополнительные аргументы, передаваемые в базовый метод request.

    Returns:
        StreamResponse: Объект StreamResponse для обработки ответа.
    """
    ...
```

#### `ws_connect`

```python
def ws_connect(self, url, *args, **kwargs):
    """
    Устанавливает WebSocket соединение.

    Args:
        url (str): URL для подключения.
        *args: Дополнительные позиционные аргументы.
        **kwargs: Дополнительные именованные аргументы.
    """
    ...
```

#### `_ws_connect`

```python
def _ws_connect(self, url, **kwargs):
    """
    Внутренний метод для установки WebSocket соединения.

    Args:
        url (str): URL для подключения.
        **kwargs: Дополнительные именованные аргументы.
    """
    ...
```

### `FormData`

#### `add_field`

```python
def add_field(self, name, data=None, content_type: str = None, filename: str = None) -> None:
    """
    Добавляет поле в форму данных.

    Args:
        name: Имя поля.
        data: Данные поля.
        content_type (str, optional): Тип содержимого. Defaults to None.
        filename (str, optional): Имя файла. Defaults to None.
    """
    ...
```

### `WebSocket`

#### `__init__`

```python
def __init__(self, session, url, **kwargs) -> None:
    """
    Инициализирует объект WebSocket.

    Args:
        session: Объект сессии.
        url (str): URL для подключения.
        **kwargs: Дополнительные именованные аргументы.
    """
    ...
```

#### `__aenter__`

```python
async def __aenter__(self):
    """
    Асинхронно входит в контекст выполнения для объекта WebSocket.

    Returns:
        self: Объект WebSocket.
    """
    ...
```

#### `__aexit__`

```python
async def __aexit__(self, *args):
    """
    Асинхронно выходит из контекста выполнения для объекта WebSocket.

    Args:
        *args: Аргументы для выхода из контекста.
    """
    ...
```

#### `receive_str`

```python
async def receive_str(self, **kwargs) -> str:
    """
    Асинхронно получает строковые данные из WebSocket соединения.

    Args:
        **kwargs: Дополнительные именованные аргументы.

    Returns:
        str: Полученные строковые данные.
    """
    ...
```

#### `send_str`

```python
async def send_str(self, data: str):
    """
    Асинхронно отправляет строковые данные через WebSocket соединение.

    Args:
        data (str): Строковые данные для отправки.
    """
    ...
```