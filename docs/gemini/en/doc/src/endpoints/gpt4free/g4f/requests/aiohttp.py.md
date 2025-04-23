# Модуль aiohttp.py

## Обзор

Модуль `aiohttp.py` предоставляет классы и функции для работы с асинхронными HTTP-запросами с использованием библиотеки `aiohttp`. Он содержит классы `StreamResponse` и `StreamSession`, а также функцию `get_connector` для настройки соединений, включая поддержку прокси.

## Более подробно

Этот модуль расширяет возможности `aiohttp` для обработки потоковых ответов и упрощает настройку сессий с поддержкой прокси, что важно для обхода ограничений и обеспечения анонимности при выполнении HTTP-запросов.

## Классы

### `StreamResponse`

**Описание**: Класс `StreamResponse` расширяет класс `ClientResponse` из библиотеки `aiohttp` и предоставляет дополнительные методы для итерации по строкам и содержимому ответа, а также для обработки Server-Sent Events (SSE).

**Наследует**:
- `ClientResponse` (из `aiohttp`)

**Атрибуты**:
- Отсутствуют явно определенные атрибуты, но наследует все атрибуты от `ClientResponse`.

**Методы**:

- `iter_lines`
- `iter_content`
- `json`
- `sse`

### `StreamSession`

**Описание**: Класс `StreamSession` расширяет класс `ClientSession` из библиотеки `aiohttp` и предоставляет удобный способ настройки сессий с поддержкой прокси и пользовательскими заголовками.

**Наследует**:
- `ClientSession` (из `aiohttp`)

**Атрибуты**:
- `headers` (dict): Заголовки для сессии.
- `timeout` (int | tuple | None): Тайм-аут для запросов.
- `connector` (BaseConnector | None): Коннектор для сессии.
- `proxy` (str | None): URL прокси-сервера.
- `proxies` (dict): Словарь прокси-серверов.
- `impersonate` (Any): Параметр для имитации.

**Методы**:
- `__init__`

## Методы класса

### `iter_lines`

```python
async def iter_lines(self) -> AsyncIterator[bytes]:
    """Асинхронно итерирует по строкам содержимого ответа."""
```

**Назначение**:
Асинхронно итерирует по строкам содержимого ответа, удаляя завершающие символы новой строки.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- `AsyncIterator[bytes]`: Асинхронный итератор байтовых строк.

**Как работает**:
Функция асинхронно итерирует по содержимому ответа, возвращая каждую строку как байтовую строку.

**Примеры**:
```python
async def process_response(response: StreamResponse):
    async for line in response.iter_lines():
        print(line)
```

### `iter_content`

```python
async def iter_content(self) -> AsyncIterator[bytes]:
    """Асинхронно итерирует по содержимому ответа."""
```

**Назначение**:
Асинхронно итерирует по содержимому ответа, возвращая каждый чанк данных как байтовую строку.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- `AsyncIterator[bytes]`: Асинхронный итератор байтовых строк.

**Как работает**:
Функция асинхронно итерирует по содержимому ответа, возвращая каждый чанк данных.

**Примеры**:
```python
async def process_response(response: StreamResponse):
    async for chunk in response.iter_content():
        print(chunk)
```

### `json`

```python
async def json(self, content_type: str = None) -> Any:
    """Декодирует JSON-ответ."""
```

**Назначение**:
Декодирует JSON-ответ из содержимого ответа.

**Параметры**:
- `content_type` (str, optional): Тип содержимого. По умолчанию `None`.

**Возвращает**:
- `Any`: Декодированный JSON-объект.

**Как работает**:
Функция вызывает метод `json` родительского класса `ClientResponse` для декодирования JSON-ответа.

**Примеры**:
```python
async def process_response(response: StreamResponse):
    data = await response.json()
    print(data)
```

### `sse`

```python
async def sse(self) -> AsyncIterator[dict]:
    """Асинхронно итерирует по Server-Sent Events ответа."""
```

**Назначение**:
Асинхронно итерирует по Server-Sent Events (SSE) ответа, извлекая данные из каждой строки события.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- `AsyncIterator[dict]`: Асинхронный итератор словарей, представляющих данные каждого события.

**Как работает**:
Функция асинхронно итерирует по строкам содержимого ответа, извлекая данные из строк, начинающихся с `data: `. Если строка содержит `[DONE]`, итерация прекращается.

**Примеры**:
```python
async def process_response(response: StreamResponse):
    async for event in response.sse():
        print(event)
```

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
    """Инициализирует StreamSession с заданными параметрами."""
```

**Назначение**:
Инициализирует экземпляр класса `StreamSession` с заданными параметрами, такими как заголовки, тайм-аут, коннектор, прокси и другие параметры.

**Параметры**:
- `headers` (dict, optional): Заголовки для сессии. По умолчанию `{}`.
- `timeout` (int | tuple | None): Тайм-аут для запросов. По умолчанию `None`.
- `connector` (BaseConnector, optional): Коннектор для сессии. По умолчанию `None`.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `proxies` (dict, optional): Словарь прокси-серверов. По умолчанию `{}`.
- `impersonate` (Any): Параметр для имитации. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры, передаваемые в конструктор `ClientSession`.

**Как работает**:
Функция инициализирует экземпляр класса `StreamSession`, устанавливая заголовки, тайм-аут, коннектор и прокси. Если указан прокси, используется `ProxyConnector` из библиотеки `aiohttp_socks`.

**Примеры**:
```python
session = StreamSession(
    headers={"X-Custom-Header": "value"},
    timeout=30,
    proxy="socks5://user:password@host:port"
)
```

## Функции

### `get_connector`

```python
def get_connector(connector: BaseConnector = None, proxy: str = None, rdns: bool = False) -> Optional[BaseConnector]:
    """Возвращает коннектор для aiohttp с поддержкой прокси."""
```

**Назначение**:
Возвращает коннектор для `aiohttp` с поддержкой прокси. Если прокси указан, используется `ProxyConnector` из библиотеки `aiohttp_socks`.

**Параметры**:
- `connector` (BaseConnector, optional): Существующий коннектор. По умолчанию `None`.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `rdns` (bool, optional): Флаг для удаленного разрешения DNS. По умолчанию `False`.

**Возвращает**:
- `Optional[BaseConnector]`: Коннектор для `aiohttp` или `None`, если прокси не указан и коннектор не предоставлен.

**Как работает**:
Функция проверяет, указан ли прокси. Если да, то пытается импортировать `ProxyConnector` из `aiohttp_socks` и создать коннектор с использованием указанного прокси. Если `aiohttp_socks` не установлен, выбрасывается исключение `MissingRequirementsError`.

**Примеры**:
```python
connector = get_connector(proxy="socks5://user:password@host:port")
session = StreamSession(connector=connector)
```