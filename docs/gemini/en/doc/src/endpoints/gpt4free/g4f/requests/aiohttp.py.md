# Модуль для работы с запросами через aiohttp
===============================================

Модуль предоставляет классы для работы с запросами через aiohttp, включая поддержку Server-Sent Events (SSE) и прокси-серверов.

## Содержание

- [Классы](#classes)
    - [`StreamResponse`](#streamresponse)
    - [`StreamSession`](#streamsession)
- [Функции](#functions)
    - [`get_connector`](#get_connector)

## Классы

### `StreamResponse`

```python
class StreamResponse(ClientResponse):
    """Класс для работы с ответами, поддерживающий потоковое чтение и SSE."""
    async def iter_lines(self) -> AsyncIterator[bytes]:
        """
        Асинхронно итерирует по строкам в ответе.

        Returns:
            AsyncIterator[bytes]: Асинхронный итератор, который возвращает строки в байтовом формате.
        """

    async def iter_content(self) -> AsyncIterator[bytes]:
        """
        Асинхронно итерирует по частям содержимого ответа.

        Returns:
            AsyncIterator[bytes]: Асинхронный итератор, который возвращает части содержимого в байтовом формате.
        """

    async def json(self, content_type: str = None) -> Any:
        """
        Асинхронно десериализует JSON-содержимое ответа.

        Args:
            content_type (str, optional): Тип содержимого. По умолчанию None.

        Returns:
            Any: Десериализованное JSON-содержимое.
        """

    async def sse(self) -> AsyncIterator[dict]:
        """
        Асинхронно итерирует по Server-Sent Events (SSE) в ответе.

        Returns:
            AsyncIterator[dict]: Асинхронный итератор, который возвращает SSE-события в виде словарей.
        """
```

### `StreamSession`

```python
class StreamSession(ClientSession):
    """Класс для работы с сессиями aiohttp, поддерживающий потоковое чтение и SSE."""
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
        """
        Инициализирует объект StreamSession.

        Args:
            headers (dict, optional): Заголовки запроса. По умолчанию {}.
            timeout (int, optional): Таймаут для запросов. По умолчанию None.
            connector (BaseConnector, optional): Соединитель для запросов. По умолчанию None.
            proxy (str, optional): URL прокси-сервера. По умолчанию None.
            proxies (dict, optional): Словарь прокси-серверов. По умолчанию {}.
            impersonate (Any, optional): Информация для подделки запроса. По умолчанию None.
            **kwargs: Дополнительные аргументы для ClientSession.
        """
```

## Функции

### `get_connector`

```python
def get_connector(connector: BaseConnector = None, proxy: str = None, rdns: bool = False) -> Optional[BaseConnector]:
    """
    Возвращает соединитель для запросов с поддержкой прокси-серверов.

    Args:
        connector (BaseConnector, optional): Соединитель для запросов. По умолчанию None.
        proxy (str, optional): URL прокси-сервера. По умолчанию None.
        rdns (bool, optional): Флаг, указывающий, использовать ли обратное DNS-разрешение для прокси-сервера. По умолчанию False.

    Returns:
        Optional[BaseConnector]: Соединитель для запросов.
    """
```