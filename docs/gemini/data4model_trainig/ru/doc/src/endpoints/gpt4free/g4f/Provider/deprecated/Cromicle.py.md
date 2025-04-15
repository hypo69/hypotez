# Модуль Cromicle

## Обзор

Модуль `Cromicle` предоставляет асинхронный генератор для взаимодействия с сервисом Cromicle.top. Он использует `aiohttp` для выполнения асинхронных HTTP-запросов и предоставляет функциональность для отправки сообщений и получения ответов в режиме реального времени.

## Подробней

Модуль предназначен для интеграции с сервисом Cromicle.top, который предоставляет API для обмена сообщениями. Он включает в себя функции для создания заголовков запросов, формирования полезной нагрузки и обработки потоковых ответов.

## Классы

### `Cromicle`

**Описание**: Класс `Cromicle` является провайдером асинхронного генератора, который взаимодействует с сервисом Cromicle.top для обмена сообщениями.

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:

-   `url` (str): URL-адрес сервиса Cromicle.top.
-   `working` (bool): Флаг, указывающий, работает ли провайдер.
-   `supports_gpt_35_turbo` (bool): Флаг, указывающий, поддерживает ли провайдер модель `gpt-35-turbo`.

**Методы**:

-   `create_async_generator()`: Создает асинхронный генератор для отправки сообщений и получения потоковых ответов от сервиса Cromicle.top.

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
    """Создает асинхронный генератор для взаимодействия с API Cromicle.

    Args:
        cls (Cromicle): Класс Cromicle.
        model (str): Модель, используемая для генерации ответа.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий потоковые ответы от API.

    Raises:
        Exception: Если возникает HTTP ошибка при запросе к API.
        Exception: Если возникает ошибка декодирования содержимого ответа.

    Example:
        >>> async for chunk in Cromicle.create_async_generator(model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': 'Hello'}]):
        ...     print(chunk)
    """
    ...
```

**Как работает функция**:

1.  Создает асинхронную сессию `aiohttp` с заголовками, созданными функцией `_create_header()`.
2.  Выполняет POST-запрос к сервису Cromicle.top с использованием `session.post()`.
3.  Формирует JSON-полезную нагрузку с помощью функции `_create_payload()`, которая включает отформатированные сообщения.
4.  Итерируется по потоку содержимого ответа с использованием `response.content.iter_any()`.
5.  Декодирует каждый чанк потока и возвращает его с помощью `yield`.

## Функции

### `_create_header`

```python
def _create_header() -> Dict[str, str]:
    """Создает словарь с заголовками для HTTP-запроса.

    Args:
        None

    Returns:
        Dict[str, str]: Словарь с заголовками 'accept' и 'content-type'.

    Raises:
        None

    Example:
        >>> _create_header()
        {'accept': '*/*', 'content-type': 'application/json'}
    """
    ...
```

**Как работает функция**:

Функция `_create_header` создает и возвращает словарь с заголовками HTTP-запроса, необходимыми для взаимодействия с API Cromicle.top.

### `_create_payload`

```python
def _create_payload(message: str) -> Dict[str, str]:
    """Создает словарь с полезной нагрузкой для HTTP-запроса.

    Args:
        message (str): Сообщение для отправки.

    Returns:
        Dict[str, str]: Словарь с полями 'message', 'token' и 'hash'.

    Raises:
        None

    Example:
        >>> _create_payload('Hello')
        {'message': 'Hello', 'token': 'abc', 'hash': '...'}
    """
    ...
```

**Как работает функция**:

Функция `_create_payload` создает словарь с полезной нагрузкой (payload) для HTTP-запроса к API Cromicle.top. Она включает сообщение, токен и хеш, вычисленный на основе сообщения и токена. Хеш используется для проверки целостности сообщения на стороне сервера.