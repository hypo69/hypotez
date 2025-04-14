# Модуль для работы с асинхронными запросами и потоковыми ответами на основе `curl_cffi`

## Обзор

Этот модуль предоставляет классы для выполнения асинхронных HTTP-запросов с поддержкой потоковых ответов, форм данных и WebSocket соединений, используя библиотеку `curl_cffi`. Он включает в себя классы `StreamResponse`, `StreamSession`, `FormData` и `WebSocket`, которые обеспечивают удобный интерфейс для работы с асинхронными сетевыми операциями.

## Подробнее

Модуль предназначен для упрощения работы с асинхронными HTTP-запросами и потоковыми данными. Он предоставляет абстракции для обработки ответов в виде текста, JSON, итерируемых строк и содержимого, а также поддерживает отправку данных форм и установление WebSocket соединений. Классы модуля используют возможности библиотеки `curl_cffi` для обеспечения высокой производительности и гибкости.

## Классы

### `StreamResponse`

**Описание**: Класс-обертка для обработки асинхронных потоковых ответов.

**Атрибуты**:
- `inner` (Response): Оригинальный объект `Response` из библиотеки `curl_cffi`.

**Методы**:
- `text()`: Асинхронно получает текст ответа.
- `raise_for_status()`: Возбуждает исключение `HTTPError`, если произошла ошибка.
- `json(**kwargs)`: Асинхронно парсит содержимое ответа в формате JSON.
- `iter_lines()`: Асинхронно итерируется по строкам ответа.
- `iter_content()`: Асинхронно итерируется по содержимому ответа.
- `sse()`: Асинхронно итерируется по событиям, отправленным сервером (Server-Sent Events).
- `__aenter__()`: Асинхронно входит в контекст выполнения для объекта ответа.
- `__aexit__(*args)`: Асинхронно выходит из контекста выполнения для объекта ответа.

#### `__init__`

```python
def __init__(self, inner: Response) -> None:
    """
    Инициализирует объект StreamResponse с предоставленным объектом Response.

    Args:
        inner (Response): Объект Response, который необходимо обернуть.
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
    Асинхронно парсит содержимое JSON ответа.

    Args:
        **kwargs: Дополнительные аргументы, передаваемые в json.loads.

    Returns:
        Any: Распарсенное содержимое JSON.
    """
    ...
```

#### `iter_lines`

```python
def iter_lines(self) -> AsyncGenerator[bytes, None]:
    """
    Асинхронно итерируется по строкам ответа.

    Yields:
        bytes: Строка ответа в байтах.
    """
    ...
```

#### `iter_content`

```python
def iter_content(self) -> AsyncGenerator[bytes, None]:
    """
    Асинхронно итерируется по содержимому ответа.

    Yields:
        bytes: Часть содержимого ответа в байтах.
    """
    ...
```

#### `sse`

```python
async def sse(self) -> AsyncGenerator[dict, None]:
    """
    Асинхронно итерируется по событиям, отправленным сервером (Server-Sent Events).

    Yields:
        dict: Событие, отправленное сервером, в виде словаря.
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
    """
    ...
```

### `StreamSession`

**Описание**: Асинхронный класс сессии для обработки HTTP-запросов с потоковой передачей.

**Наследует**:
- `AsyncSession`

**Методы**:
- `request(method: str, url: str, ssl = None, **kwargs)`: Создает и возвращает объект `StreamResponse` для данного HTTP-запроса.
- `ws_connect(url, *args, **kwargs)`: Устанавливает WebSocket соединение.
- `_ws_connect(url, **kwargs)`: Внутренний метод для установки WebSocket соединения.
- `head = partialmethod(request, "HEAD")`: Отправляет HEAD запрос.
- `get = partialmethod(request, "GET")`: Отправляет GET запрос.
- `post = partialmethod(request, "POST")`: Отправляет POST запрос.
- `put = partialmethod(request, "PUT")`: Отправляет PUT запрос.
- `patch = partialmethod(request, "PATCH")`: Отправляет PATCH запрос.
- `delete = partialmethod(request, "DELETE")`: Отправляет DELETE запрос.
- `options = partialmethod(request, "OPTIONS")`: Отправляет OPTIONS запрос.

#### `request`

```python
def request(
    self, method: str, url: str, ssl = None, **kwargs
) -> StreamResponse:
    """
    Создает и возвращает объект StreamResponse для данного HTTP-запроса.

    Args:
        method (str): HTTP-метод (GET, POST, и т.д.).
        url (str): URL-адрес запроса.
        ssl: Параметры SSL.
        **kwargs: Дополнительные аргументы, передаваемые в базовый метод request.

    Returns:
        StreamResponse: Объект StreamResponse, представляющий ответ на запрос.
    """
    ...
```

#### `ws_connect`

```python
def ws_connect(self, url, *args, **kwargs):
    """
    Устанавливает WebSocket соединение.

    Args:
        url: URL-адрес WebSocket.
        *args: Дополнительные позиционные аргументы.
        **kwargs: Дополнительные именованные аргументы.

    Returns:
        WebSocket: Объект WebSocket, представляющий соединение.
    """
    ...
```

#### `_ws_connect`

```python
def _ws_connect(self, url, **kwargs):
    """
    Внутренний метод для установки WebSocket соединения.

    Args:
        url: URL-адрес WebSocket.
        **kwargs: Дополнительные именованные аргументы.

    Returns:
        super().ws_connect(url, **kwargs): Результат вызова базового метода ws_connect.
    """
    ...
```

### `FormData`

**Описание**: Класс для представления данных формы.

**Наследует**:
- `CurlMime` (если `has_curl_mime` is `True`)

**Методы**:
- `add_field(self, name, data=None, content_type: str = None, filename: str = None)`: Добавляет поле в форму.
- `__init__(self) -> None`: Инициализирует объект FormData и вызывает исключение, если `CurlMimi` отсутствует.

#### `add_field`

```python
def add_field(self, name, data=None, content_type: str = None, filename: str = None) -> None:
    """
    Добавляет поле в форму.

    Args:
        name: Имя поля.
        data: Данные поля.
        content_type: Тип содержимого поля.
        filename: Имя файла поля.
    """
    ...
```

#### `__init__`

```python
def __init__(self) -> None:
    """
    Инициализирует объект FormData и вызывает исключение, если CurlMimi отсутствует.
    """
    ...
```

### `WebSocket`

**Описание**: Класс для работы с WebSocket соединениями.

**Атрибуты**:
- `session` (StreamSession): Сессия, используемая для соединения.
- `url` (str): URL-адрес WebSocket.
- `options` (dict): Опции соединения.

**Методы**:
- `__aenter__()`: Асинхронно входит в контекст выполнения для объекта WebSocket.
- `__aexit__(*args)`: Асинхронно выходит из контекста выполнения для объекта WebSocket.
- `receive_str(**kwargs)`: Асинхронно получает строку из WebSocket.
- `send_str(data: str)`: Асинхронно отправляет строку в WebSocket.

#### `__init__`

```python
def __init__(self, session, url, **kwargs) -> None:
    """
    Инициализирует объект WebSocket.

    Args:
        session: Сессия, используемая для соединения.
        url: URL-адрес WebSocket.
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
    """
    ...
```

#### `receive_str`

```python
async def receive_str(self, **kwargs) -> str:
    """
    Асинхронно получает строку из WebSocket.

    Args:
        **kwargs: Дополнительные именованные аргументы.

    Returns:
        str: Строка, полученная из WebSocket.
    """
    ...
```

#### `send_str`

```python
async def send_str(self, data: str):
    """
    Асинхронно отправляет строку в WebSocket.

    Args:
        data (str): Строка, отправляемая в WebSocket.
    """
    ...
```