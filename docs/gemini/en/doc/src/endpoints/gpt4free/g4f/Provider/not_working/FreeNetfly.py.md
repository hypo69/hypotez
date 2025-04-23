# Модуль `FreeNetfly`

## Обзор

Модуль `FreeNetfly` предоставляет асинхронный генератор для взаимодействия с API `free.netfly.top`. Он позволяет получать ответы от моделей, таких как `gpt-3.5-turbo` и `gpt-4`, используя асинхронные запросы. Модуль поддерживает прокси и автоматические повторные попытки при сбоях соединения.

## Более подробно

Этот модуль предназначен для интеграции с другими частями проекта `hypotez`, где требуется взаимодействие с API `free.netfly.top`. Он обеспечивает надежный способ отправки запросов и обработки ответов в асинхронном режиме.

## Классы

### `FreeNetfly`

**Описание**:
Класс `FreeNetfly` является подклассом `AsyncGeneratorProvider` и `ProviderModelMixin` и предоставляет функциональность для взаимодействия с API `free.netfly.top`.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает базовую структуру для асинхронных генераторов.
- `ProviderModelMixin`: Предоставляет методы для работы с моделями.

**Атрибуты**:
- `url` (str): URL API `free.netfly.top`.
- `api_endpoint` (str): Endpoint API для запросов completions.
- `working` (bool): Указывает, работает ли провайдер.
- `default_model` (str): Модель, используемая по умолчанию (`gpt-3.5-turbo`).
- `models` (List[str]): Список поддерживаемых моделей (`gpt-3.5-turbo`, `gpt-4`).

**Принцип работы**:
Класс использует `aiohttp` для асинхронных HTTP-запросов. Он отправляет сообщения пользователя к API `free.netfly.top` и возвращает ответы в виде асинхронного генератора. В случае ошибок соединения, он автоматически повторяет попытки запроса с экспоненциальным увеличением задержки.

### Методы класса

- `create_async_generator`
- `_process_response`

## Методы класса

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для получения ответов от API `free.netfly.top`.

    Args:
        model (str): Название модели для использования (`gpt-3.5-turbo`, `gpt-4`).
        messages (Messages): Список сообщений для отправки в API.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий ответы от API.

    Raises:
        ClientError: Если возникает ошибка при выполнении HTTP-запроса.
        asyncio.TimeoutError: Если время ожидания запроса истекает.

    Как работает функция:
    - Функция формирует заголовки и данные для POST-запроса к API `free.netfly.top`.
    - Использует `aiohttp.ClientSession` для отправки асинхронного запроса.
    - В случае ошибки соединения, функция повторяет попытки запроса до `max_retries` раз с экспоненциальным увеличением задержки.
    - Обрабатывает ответ с помощью `_process_response` и возвращает асинхронный генератор.

    Примеры:
        Пример вызова функции:
        >>> model = 'gpt-3.5-turbo'
        >>> messages = [{'role': 'user', 'content': 'Hello, world!'}]
        >>> async for chunk in FreeNetfly.create_async_generator(model=model, messages=messages):
        ...     print(chunk, end='')
    """
```

### `_process_response`

```python
@classmethod
async def _process_response(cls, response) -> AsyncGenerator[str, None]:
    """
    Обрабатывает ответ от API, извлекая содержимое из JSON-формата.

    Args:
        response: Объект ответа `aiohttp.ClientResponse`.

    Yields:
        str: Части содержимого ответа.

    Как работает функция:
    - Функция читает ответ построчно, накапливая данные в буфере.
    - Разбивает буфер на подстроки, разделенные `\\n`.
    - Извлекает JSON из строк, начинающихся с `data: `.
    - Извлекает содержимое из поля `content` в структуре JSON.
    - Возвращает содержимое в виде асинхронного генератора.

    Примеры:
        Пример использования (внутри `create_async_generator`):
        >>> async with session.post(f"{cls.url}{cls.api_endpoint}", json=data, proxy=proxy, timeout=timeout) as response:
        ...     async for chunk in cls._process_response(response):
        ...         yield chunk
    """