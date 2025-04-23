# Модуль для асинхронных HTTP-запросов с использованием aiohttp

## Обзор

Модуль `aiohttp.py` предоставляет инструменты для выполнения асинхронных HTTP-запросов, включая поддержку потоковой передачи данных, прокси и Server-Sent Events (SSE). Он содержит классы `StreamResponse` и `StreamSession`, а также функцию `get_connector` для настройки прокси-соединений.

## Подробней

Этот модуль расширяет функциональность библиотеки `aiohttp` для обеспечения более гибких и мощных возможностей при работе с HTTP-запросами. Он позволяет обрабатывать потоковые данные, использовать прокси-серверы и работать с SSE, что делает его полезным при взаимодействии с API, требующими этих возможностей. Расположен в `hypotez/src/endpoints/gpt4free/g4f/requests/aiohttp.py`.

## Классы

### `StreamResponse`

**Описание**: Расширяет класс `ClientResponse` из библиотеки `aiohttp` для добавления методов итерации по строкам, содержимому и SSE.

**Наследует**: `aiohttp.ClientResponse`

**Атрибуты**:
- Нет дополнительных атрибутов, кроме унаследованных от `ClientResponse`.

**Методы**:
- `iter_lines()`: Асинхронный итератор для построчного чтения содержимого ответа.
- `iter_content()`: Асинхронный итератор для чтения содержимого ответа чанками.
- `json(content_type: str = None)`: Асинхронный метод для преобразования содержимого ответа в формат JSON.
- `sse()`: Асинхронный итератор для обработки Server-Sent Events (SSE) в ответе.

### `StreamResponse.iter_lines`

```python
async def iter_lines(self) -> AsyncIterator[bytes]:
    """Асинхронный итератор для построчного чтения содержимого ответа."""
    async for line in self.content:
        yield line.rstrip(b"\r\n")
```

**Назначение**: Предоставляет асинхронный итератор для построчного чтения содержимого ответа, удаляя завершающие символы перевода строки.

**Параметры**:
- Нет.

**Возвращает**:
- `AsyncIterator[bytes]`: Асинхронный итератор, возвращающий каждую строку ответа в виде байтовой строки.

**Как работает функция**:
- Функция итерируется по содержимому ответа (`self.content`) асинхронно.
- Для каждой строки удаляются завершающие символы перевода строки (`\r\n`).
- Каждая обработанная строка возвращается через `yield`.

### `StreamResponse.iter_content`

```python
async def iter_content(self) -> AsyncIterator[bytes]:
    """Асинхронный итератор для чтения содержимого ответа чанками."""
    async for chunk in self.content.iter_any():
        yield chunk
```

**Назначение**: Предоставляет асинхронный итератор для чтения содержимого ответа чанками (блоками данных).

**Параметры**:
- Нет.

**Возвращает**:
- `AsyncIterator[bytes]`: Асинхронный итератор, возвращающий каждый чанк содержимого ответа в виде байтовой строки.

**Как работает функция**:
- Функция итерируется по содержимому ответа (`self.content`), используя метод `iter_any()` для получения чанков данных.
- Каждый полученный чанк возвращается через `yield`.

### `StreamResponse.json`

```python
async def json(self, content_type: str = None) -> Any:
    """Асинхронный метод для преобразования содержимого ответа в формат JSON."""
    return await super().json(content_type=content_type)
```

**Назначение**: Асинхронно преобразует содержимое ответа в формат JSON.

**Параметры**:
- `content_type` (str, optional): Тип содержимого, который должен быть у ответа. По умолчанию `None`.

**Возвращает**:
- `Any`: Десериализованный JSON-объект.

**Как работает функция**:
- Функция вызывает метод `json()` из родительского класса (`super()`) для выполнения преобразования содержимого ответа в JSON.

### `StreamResponse.sse`

```python
async def sse(self) -> AsyncIterator[dict]:
    """Асинхронно перебирает Server-Sent Events ответа."""
    async for line in self.content:
        if line.startswith(b"data: "):
            chunk = line[6:]
            if chunk.startswith(b"[DONE]"):\
                break
            try:
                yield json.loads(chunk)
            except json.JSONDecodeError:
                continue
```

**Назначение**: Асинхронно перебирает Server-Sent Events (SSE) в содержимом ответа.

**Параметры**:
- Нет.

**Возвращает**:
- `AsyncIterator[dict]`: Асинхронный итератор, возвращающий каждый SSE в виде словаря.

**Как работает функция**:
- Функция итерируется по строкам содержимого ответа (`self.content`) асинхронно.
- Для каждой строки проверяется, начинается ли она с `b"data: "`.
- Если строка является SSE, извлекается полезная нагрузка (данные) путем удаления префикса `b"data: "` и декодируется из JSON.
- Если полезная нагрузка начинается с `b"[DONE]"`, итерация прекращается.
- В случае ошибки декодирования JSON (`json.JSONDecodeError`), итерация продолжается.

### `StreamSession`

**Описание**: Расширяет класс `ClientSession` из библиотеки `aiohttp` для добавления поддержки прокси, пользовательских заголовков и обработки таймаутов.

**Наследует**: `aiohttp.ClientSession`

**Атрибуты**:
- Нет дополнительных атрибутов, кроме унаследованных от `ClientSession`.

**Параметры конструктора**:
- `headers` (dict, optional): Словарь HTTP-заголовков, которые будут добавлены к каждому запросу. По умолчанию `{}`.
- `timeout` (int, optional): Время ожидания запроса в секундах. По умолчанию `None`.
- `connector` (BaseConnector, optional): Пользовательский коннектор для управления соединениями. По умолчанию `None`.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `proxies` (dict, optional): Словарь прокси-серверов для разных схем. По умолчанию `{}`.
- `impersonate` (str, optional): строка для имитации User-Agent
- `**kwargs`: Дополнительные аргументы, передаваемые в конструктор `ClientSession`.

**Как работает класс**:
- Класс `StreamSession` инициализируется с параметрами, которые позволяют настроить HTTP-сессию, включая заголовки, таймауты и прокси.
- Если указан параметр `impersonate`, заголовки объединяются с `DEFAULT_HEADERS`.
- Если указан `proxy` или `proxies`, используется функция `get_connector` для создания коннектора с поддержкой прокси.

### `get_connector`

```python
def get_connector(connector: BaseConnector = None, proxy: str = None, rdns: bool = False) -> Optional[BaseConnector]:
    """Получает или создает коннектор aiohttp с поддержкой прокси."""
    if proxy and not connector:
        try:
            from aiohttp_socks import ProxyConnector
            if proxy.startswith("socks5h://"):
                proxy = proxy.replace("socks5h://", "socks5://")
                rdns = True
            connector = ProxyConnector.from_url(proxy, rdns=rdns)
        except ImportError as ex:
            raise MissingRequirementsError('Install "aiohttp_socks" package for proxy support') from ex
    return connector
```

**Назначение**: Функция создает и возвращает коннектор `aiohttp` с поддержкой прокси, если указан `proxy`.

**Параметры**:
- `connector` (BaseConnector, optional): Существующий коннектор `aiohttp`. По умолчанию `None`.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `rdns` (bool, optional): Флаг для указания, следует ли выполнять удаленный DNS-lookup для SOCKS-прокси. По умолчанию `False`.

**Возвращает**:
- `Optional[BaseConnector]`: Коннектор `aiohttp` с поддержкой прокси или `None`, если `proxy` не указан.

**Вызывает исключения**:
- `MissingRequirementsError`: Если библиотека `aiohttp_socks` не установлена и требуется поддержка прокси.

**Как работает функция**:
- Если `proxy` указан и `connector` не предоставлен, функция пытается импортировать библиотеку `aiohttp_socks`.
- Если `proxy` начинается с `socks5h://`, он заменяется на `socks5://`, а `rdns` устанавливается в `True`.
- Создается коннектор `ProxyConnector` из URL прокси-сервера.
- Если библиотека `aiohttp_socks` не установлена, вызывается исключение `MissingRequirementsError`.

## Функции

Функции в данном модуле отсутствуют, кроме `get_connector`, которая описана выше.