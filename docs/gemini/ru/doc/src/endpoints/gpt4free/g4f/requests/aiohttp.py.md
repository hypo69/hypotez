# Модуль aiohttp.py

## Обзор

Модуль `aiohttp.py` предоставляет инструменты для работы с асинхронными HTTP-запросами, включая поддержку потоковой передачи данных и Server-Sent Events (SSE). Он определяет классы `StreamResponse` и `StreamSession`, расширяющие функциональность `aiohttp` для более удобной обработки потоковых ответов и управления сессиями.

## Подробнее

Этот модуль предназначен для использования в асинхронных приложениях, где требуется эффективная обработка больших объемов данных, передаваемых по сети, или взаимодействие с серверами, использующими потоковую передачу данных, в частности, SSE.

## Классы

### `StreamResponse`

**Описание**: Класс `StreamResponse` расширяет `aiohttp.ClientResponse` для предоставления удобных методов итерации по содержимому ответа, включая поддержку потоковой обработки строк и событий SSE.

**Наследует**: `aiohttp.ClientResponse`

**Атрибуты**:
- Отсутствуют, но наследует все атрибуты `aiohttp.ClientResponse`.

**Методы**:

- `iter_lines()`: Асинхронный генератор, который итерирует по строкам ответа.
- `iter_content()`: Асинхронный генератор, который итерирует по чанкам содержимого ответа.
- `json(content_type: str = None)`: Асинхронно преобразует тело ответа в JSON.
- `sse()`: Асинхронный генератор, который итерирует по Server-Sent Events ответа.

### `StreamSession`

**Описание**: Класс `StreamSession` расширяет `aiohttp.ClientSession` для упрощения настройки сессии с поддержкой прокси, таймаутов и пользовательских заголовков.

**Наследует**: `aiohttp.ClientSession`

**Атрибуты**:
- Отсутствуют, но наследует все атрибуты `aiohttp.ClientSession`.

**Методы**:
- `__init__(headers: dict = {}, timeout: int = None, connector: BaseConnector = None, proxy: str = None, proxies: dict = {}, impersonate=None, **kwargs)`: Инициализирует экземпляр `StreamSession` с заданными параметрами.

## Методы класса `StreamResponse`

### `iter_lines`

```python
    async def iter_lines(self) -> AsyncIterator[bytes]:
        """Асинхронно итерирует по строкам ответа."""
```

**Назначение**: Асинхронно итерирует по строкам ответа, удаляя завершающие символы перевода строки.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- `AsyncIterator[bytes]`: Асинхронный итератор, возвращающий строки ответа в виде байтов.

**Как работает функция**:
- Функция итерирует по содержимому ответа, разделяя его на строки и удаляя символы `\r\n` в конце каждой строки.

**Примеры**:

```python
async def process_response(response: StreamResponse):
    async for line in response.iter_lines():
        print(f"Line: {line}")
```

### `iter_content`

```python
    async def iter_content(self) -> AsyncIterator[bytes]:
        """Асинхронно итерирует по чанкам содержимого ответа."""
```

**Назначение**: Асинхронно итерирует по чанкам содержимого ответа.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- `AsyncIterator[bytes]`: Асинхронный итератор, возвращающий чанки содержимого ответа в виде байтов.

**Как работает функция**:
- Функция итерирует по содержимому ответа, возвращая каждый чанк данных по мере поступления.

**Примеры**:

```python
async def process_response(response: StreamResponse):
    async for chunk in response.iter_content():
        print(f"Chunk: {chunk}")
```

### `json`

```python
    async def json(self, content_type: str = None) -> Any:
        """Асинхронно преобразует тело ответа в JSON."""
```

**Назначение**: Асинхронно преобразует тело ответа в JSON.

**Параметры**:
- `content_type` (str, optional): Тип содержимого, который нужно учитывать при разборе JSON. По умолчанию `None`.

**Возвращает**:
- `Any`: Десериализованный JSON-объект.

**Как работает функция**:
- Функция вызывает метод `json` родительского класса `aiohttp.ClientResponse` для преобразования тела ответа в JSON.

**Примеры**:

```python
async def process_response(response: StreamResponse):
    data = await response.json()
    print(f"JSON data: {data}")
```

### `sse`

```python
    async def sse(self) -> AsyncIterator[dict]:
        """Асинхронно итерирует по Server-Sent Events ответа."""
```

**Назначение**: Асинхронно итерирует по Server-Sent Events (SSE) ответа.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- `AsyncIterator[dict]`: Асинхронный итератор, возвращающий события SSE в виде словарей.

**Как работает функция**:
- Функция итерирует по строкам ответа, ожидая строк, начинающихся с "data: ".
- Извлекает данные из этих строк, преобразует их в JSON и возвращает в виде словаря.
- Если встречается строка "data: [DONE]", итерация прекращается.

**Примеры**:

```python
async def process_response(response: StreamResponse):
    async for event in response.sse():
        print(f"SSE Event: {event}")
```

## Методы класса `StreamSession`

### `__init__`

```python
    def __init__(
        self,
        headers: dict = {},
        timeout: int = None,
        connector: BaseConnector = None,
        proxy: str = None,
        proxies: dict = {},
        impersonate = None,
        **kwargs
    ):
        """Инициализирует экземпляр StreamSession с заданными параметрами."""
```

**Назначение**: Инициализирует экземпляр `StreamSession` с заданными параметрами, такими как заголовки, таймаут, прокси и т.д.

**Параметры**:
- `headers` (dict, optional): Заголовки HTTP-запроса. По умолчанию `{}`.
- `timeout` (int, optional): Таймаут для запроса в секундах. По умолчанию `None`. Может быть кортежем `(connect, read)`, где `connect` - таймаут для установки соединения, `read` - таймаут для чтения данных.
- `connector` (BaseConnector, optional): Объект коннектора для управления соединениями. По умолчанию `None`.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `proxies` (dict, optional): Словарь URL прокси-серверов для разных протоколов. По умолчанию `{}`.
- `impersonate` (optional): Не используется.
- `**kwargs`: Дополнительные аргументы, передаваемые в конструктор `aiohttp.ClientSession`.

**Как работает функция**:
- Функция инициализирует `StreamSession`, настраивая заголовки, таймаут и прокси.
- Если указан `impersonate`, добавляет стандартные заголовки.
- Если указан `timeout` в виде кортежа, разделяет его на таймаут соединения и таймаут чтения.
- Если указан `proxy`, использует его для создания коннектора через `get_connector`.

**Примеры**:

```python
async def create_session():
    session = StreamSession(
        headers={"X-Custom-Header": "value"},
        timeout=30,
        proxy="http://proxy.example.com"
    )
    return session
```

## Функции

### `get_connector`

```python
def get_connector(connector: BaseConnector = None, proxy: str = None, rdns: bool = False) -> Optional[BaseConnector]:
    """Возвращает коннектор для aiohttp с поддержкой прокси."""
```

**Назначение**: Создает и возвращает коннектор для `aiohttp` с поддержкой прокси, если указан `proxy`.

**Параметры**:
- `connector` (BaseConnector, optional): Существующий коннектор, который нужно использовать. По умолчанию `None`.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `rdns` (bool, optional): Флаг, указывающий, нужно ли выполнять разрешение DNS на стороне прокси-сервера. По умолчанию `False`.

**Возвращает**:
- `Optional[BaseConnector]`: Коннектор для `aiohttp` с поддержкой прокси, или `None`, если `proxy` не указан.

**Вызывает исключения**:
- `MissingRequirementsError`: Если указан `proxy`, но не установлен пакет `aiohttp_socks`.

**Как работает функция**:
- Если указан `proxy`, пытается создать `ProxyConnector` из пакета `aiohttp_socks`.
- Если `aiohttp_socks` не установлен, выбрасывает исключение `MissingRequirementsError`.
- Если `proxy` начинается с "socks5h://", заменяет его на "socks5://" и устанавливает `rdns` в `True`.

**Примеры**:

```python
connector = get_connector(proxy="socks5://proxy.example.com:1080")
```