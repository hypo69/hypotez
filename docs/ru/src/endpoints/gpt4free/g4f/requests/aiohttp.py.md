# Модуль для работы с асинхронными HTTP-запросами (aiohttp)

## Обзор

Модуль предоставляет классы и функции для выполнения асинхронных HTTP-запросов с использованием библиотеки `aiohttp`. Он включает в себя поддержку потоковой передачи данных, обработки Server-Sent Events (SSE), а также проксирование запросов через SOCKS5.

## Подробней

Этот модуль предоставляет расширенные возможности для работы с `aiohttp`, включая поддержку потоковой передачи данных и Server-Sent Events. Он также включает в себя функциональность для проксирования запросов, что может быть полезно для обхода ограничений доступа или повышения анонимности.

## Классы

### `StreamResponse`

**Описание**: Класс, представляющий асинхронный ответ HTTP-запроса с возможностью потоковой обработки данных.

**Наследует**: `aiohttp.ClientResponse`

**Методы**:

- `iter_lines()`: Асинхронный итератор по строкам ответа.
- `iter_content()`: Асинхронный итератор по содержимому ответа в виде байтов.
- `json(content_type: str = None)`: Асинхронно декодирует JSON-ответ.
- `sse()`: Асинхронный итератор по Server-Sent Events (SSE) ответа.

#### `iter_lines`

```python
    async def iter_lines(self) -> AsyncIterator[bytes]:
        """Asynchronously iterate over the lines of the response."""
        async for line in self.content:
            yield line.rstrip(b"\\r\\n")
```

**Назначение**: Асинхронно итерирует по строкам ответа, удаляя завершающие символы новой строки.

**Параметры**:
- Отсутствуют

**Возвращает**:
- `AsyncIterator[bytes]`: Асинхронный итератор, возвращающий строки ответа в виде байтов.

**Как работает функция**:
1. Функция асинхронно итерирует по содержимому ответа.
2. Для каждой строки удаляются завершающие символы новой строки (`\r\n`).
3. Строка возвращается в виде байтов.

```mermaid
graph TD
A[Начало] --> B{Получение строки из self.content}
B -- Есть строка --> C[Удаление '\r\n' из строки]
C --> D{Возврат строки}
B -- Нет строк --> E[Конец]
```

**Примеры**:
```python
async for line in response.iter_lines():
    print(line)
```

#### `iter_content`

```python
    async def iter_content(self) -> AsyncIterator[bytes]:
        """Asynchronously iterate over the content of the response."""
        async for chunk in self.content.iter_any():
            yield chunk
```

**Назначение**: Асинхронно итерирует по содержимому ответа в виде чанков байтов.

**Параметры**:
- Отсутствуют

**Возвращает**:
- `AsyncIterator[bytes]`: Асинхронный итератор, возвращающий чанки содержимого ответа в виде байтов.

**Как работает функция**:
1. Функция асинхронно итерирует по содержимому ответа с помощью `self.content.iter_any()`.
2. Каждый чанк возвращается в виде байтов.

```mermaid
graph TD
A[Начало] --> B{Получение чанка из self.content.iter_any()}
B -- Есть чанк --> C{Возврат чанка}
B -- Нет чанков --> D[Конец]
```

**Примеры**:
```python
async for chunk in response.iter_content():
    print(chunk)
```

#### `json`

```python
    async def json(self, content_type: str = None) -> Any:
        """Asynchronously decode JSON-response."""
        return await super().json(content_type=content_type)
```

**Назначение**: Асинхронно декодирует JSON-ответ.

**Параметры**:
- `content_type` (str, optional): Тип содержимого. По умолчанию `None`.

**Возвращает**:
- `Any`: Декодированный JSON-ответ.

**Как работает функция**:
1. Функция вызывает метод `json` родительского класса (`aiohttp.ClientResponse`).
2. Возвращает декодированный JSON-ответ.

```mermaid
graph TD
A[Начало] --> B[Вызов super().json(content_type=content_type)]
B --> C{Возврат декодированного JSON-ответа}
```

**Примеры**:
```python
data = await response.json()
print(data)
```

#### `sse`

```python
    async def sse(self) -> AsyncIterator[dict]:
        """Asynchronously iterate over the Server-Sent Events of the response."""
        async for line in self.content:
            if line.startswith(b"data: "):\n
                chunk = line[6:]\n
                if chunk.startswith(b"[DONE]"):\n
                    break
                try:
                    yield json.loads(chunk)
                except json.JSONDecodeError:
                    continue
```

**Назначение**: Асинхронно итерирует по Server-Sent Events (SSE) ответа.

**Параметры**:
- Отсутствуют

**Возвращает**:
- `AsyncIterator[dict]`: Асинхронный итератор, возвращающий события SSE в виде словарей.

**Как работает функция**:
1. Функция асинхронно итерирует по строкам содержимого ответа.
2. Если строка начинается с `b"data: "`, извлекается полезная нагрузка события.
3. Если полезная нагрузка начинается с `b"[DONE]"`, итерация прекращается.
4. Полезная нагрузка декодируется как JSON.
5. Если декодирование JSON успешно, событие возвращается.
6. Если декодирование JSON не удалось, итерация продолжается.

```mermaid
graph TD
A[Начало] --> B{Получение строки из self.content}
B -- Есть строка --> C{Строка начинается с "data: "}
C -- Да --> D[Извлечение полезной нагрузки]
D --> E{Полезная нагрузка начинается с "[DONE]"}
E -- Да --> F[Конец]
E -- Нет --> G{Декодирование JSON}
G -- Успешно --> H{Возврат события}
G -- Ошибка --> B
C -- Нет --> B
```

**Примеры**:
```python
async for event in response.sse():
    print(event)
```

### `StreamSession`

**Описание**: Класс, представляющий асинхронную HTTP-сессию с поддержкой потоковой передачи данных и проксирования.

**Наследует**: `aiohttp.ClientSession`

**Аттрибуты**:
- headers (dict): Заголовки HTTP-запроса.
- timeout (int): Время ожидания запроса в секундах.
- connector (BaseConnector): Коннектор для управления соединениями.
- proxy (str): URL прокси-сервера.
- proxies (dict): Словарь URL прокси-серверов для разных протоколов.
- impersonate: Объект для имитации браузера.

**Методы**:
- `__init__(headers: dict = {}, timeout: int = None, connector: BaseConnector = None, proxy: str = None, proxies: dict = {}, impersonate = None, **kwargs)`: Инициализирует новый экземпляр класса `StreamSession`.

#### `__init__`

```python
    def __init__(
        self,
        headers: dict = {},\n
        timeout: int = None,
        connector: BaseConnector = None,
        proxy: str = None,
        proxies: dict = {},\n
        impersonate = None,
        **kwargs
    ):
        if impersonate:\n
            headers = {
                **DEFAULT_HEADERS,
                **headers
            }
        connect = None
        if isinstance(timeout, tuple):\n
            connect, timeout = timeout;\n
        if timeout is not None:\n
            timeout = ClientTimeout(timeout, connect)
        if proxy is None:\n
            proxy = proxies.get("all", proxies.get("https"))
        super().__init__(
            **kwargs,\n
            timeout=timeout,
            response_class=StreamResponse,
            connector=get_connector(connector, proxy),
            headers=headers
        )
```

**Назначение**: Инициализирует новый экземпляр класса `StreamSession`.

**Параметры**:
- `headers` (dict, optional): Заголовки HTTP-запроса. По умолчанию `{}`.
- `timeout` (int, optional): Время ожидания запроса в секундах. По умолчанию `None`.
- `connector` (BaseConnector, optional): Коннектор для управления соединениями. По умолчанию `None`.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `proxies` (dict, optional): Словарь URL прокси-серверов для разных протоколов. По умолчанию `{}`.
- `impersonate` (optional): Объект для имитации браузера. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы, передаваемые в конструктор `aiohttp.ClientSession`.

**Как работает функция**:
1. Если указан параметр `impersonate`, добавляются стандартные заголовки.
2. Если `timeout` является кортежем, извлекаются параметры `connect` и `timeout`.
3. Если `timeout` указан, создается объект `ClientTimeout`.
4. Если `proxy` не указан, он извлекается из словаря `proxies`.
5. Вызывается конструктор родительского класса (`aiohttp.ClientSession`) с указанными параметрами.

```mermaid
graph TD
A[Начало] --> B{impersonate is not None}
B -- Да --> C[Добавление стандартных заголовков]
B -- Нет --> D{timeout is tuple}
D -- Да --> E[Извлечение connect и timeout из timeout]
D -- Нет --> F{timeout is not None}
F -- Да --> G[Создание ClientTimeout]
F -- Нет --> H{proxy is None}
H -- Да --> I[Извлечение proxy из proxies]
H -- Нет --> J[Вызов super().__init__]
J --> K[Конец]
```

**Примеры**:
```python
session = StreamSession(headers={'X-Custom-Header': 'value'}, timeout=30)
```

## Функции

### `get_connector`

```python
def get_connector(connector: BaseConnector = None, proxy: str = None, rdns: bool = False) -> Optional[BaseConnector]:
    if proxy and not connector:\n
        try:\n
            from aiohttp_socks import ProxyConnector
            if proxy.startswith("socks5h://"):\n
                proxy = proxy.replace("socks5h://", "socks5://")
                rdns = True
            connector = ProxyConnector.from_url(proxy, rdns=rdns)
        except ImportError:\n
            raise MissingRequirementsError('Install "aiohttp_socks" package for proxy support')
    return connector
```

**Назначение**: Создает и возвращает коннектор для `aiohttp` с поддержкой проксирования.

**Параметры**:
- `connector` (BaseConnector, optional): Существующий коннектор. По умолчанию `None`.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `rdns` (bool, optional): Флаг, указывающий, следует ли выполнять удаленный DNS-запрос. По умолчанию `False`.

**Возвращает**:
- `Optional[BaseConnector]`: Коннектор для `aiohttp` или `None`, если прокси не указан.

**Вызывает исключения**:
- `MissingRequirementsError`: Если не установлен пакет `aiohttp_socks` и указан прокси.

**Как работает функция**:
1. Если указан `proxy` и не указан `connector`, функция пытается создать `ProxyConnector` из пакета `aiohttp_socks`.
2. Если `proxy` начинается с `socks5h://`, он заменяется на `socks5://` и устанавливается флаг `rdns`.
3. Если пакет `aiohttp_socks` не установлен, вызывается исключение `MissingRequirementsError`.
4. Возвращается коннектор или `None`, если прокси не указан.

```mermaid
graph TD
A[Начало] --> B{proxy and not connector}
B -- Да --> C{Импорт aiohttp_socks.ProxyConnector}
C -- Успешно --> D{proxy.startswith("socks5h://")}
C -- Ошибка --> E[Вызов MissingRequirementsError]
D -- Да --> F[Замена "socks5h://" на "socks5://"]
F --> G[rdns = True]
D -- Нет --> G[Создание ProxyConnector.from_url(proxy, rdns=rdns)]
B -- Нет --> H{Возврат connector}
```

**Примеры**:
```python
connector = get_connector(proxy='socks5://user:password@host:port')
session = StreamSession(connector=connector)
```
```python
connector = get_connector()
session = StreamSession(connector=connector)