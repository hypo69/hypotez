# Module `MetaAI.py`

## Overview

This module implements the `MetaAI` class, which serves as an asynchronous provider for interacting with the Meta AI service. It handles tasks such as updating access tokens, sending prompts, fetching sources, and managing cookies to ensure proper communication with the Meta AI platform. The module also defines custom exceptions and utility functions to facilitate error handling and data extraction.

## More details

The `MetaAI` class extends `AsyncGeneratorProvider` and `ProviderModelMixin`, providing an interface for generating responses asynchronously from the Meta AI service. It manages cookies, access tokens, and session details to maintain authenticated communication. The module is designed to support text-based prompts and image generation requests, handling various response formats and potential errors.

The module is located in the project at `hypotez/src/endpoints/gpt4free/g4f/Provider/needs_auth/MetaAI.py`. This indicates that it is part of a larger system designed to provide free access to various AI models, with this specific file handling the Meta AI integration, including necessary authentication mechanisms.

## Classes

### `Sources`

**Description**:
Represents a list of sources with their titles and links.

**Attributes**:
- `list` (List[Dict[str, str]]): List of dictionaries, where each dictionary contains the title and link of a source.

**Methods**:
- `__init__(self, link_list: List[Dict[str, str]]) -> None`: Initializes the `Sources` object with a list of links.
- `__str__(self) -> str`: Returns a formatted string representation of the list of sources.

### `AbraGeoBlockedError`

**Description**:
Custom exception raised when Meta AI is not available in the user's country due to geographic restrictions.

### `MetaAI`

**Description**:
Class for interacting with the Meta AI service. It extends `AsyncGeneratorProvider` and `ProviderModelMixin` to provide asynchronous response generation capabilities.

**Inherits**:
- `AsyncGeneratorProvider`: Provides a base class for asynchronous providers that generate responses in chunks.
- `ProviderModelMixin`: Provides a mixin for handling model-related functionalities.

**Attributes**:
- `label` (str): Label identifying the provider as "Meta AI".
- `url` (str): Base URL for the Meta AI service.
- `working` (bool): Boolean indicating whether the provider is currently operational.
- `default_model` (str): Default model used by the provider, set to 'meta-ai'.
- `session` (ClientSession): Asynchronous client session for making HTTP requests.
- `cookies` (Cookies): Dictionary storing cookies required for authentication.
- `access_token` (str): Access token used for authenticated requests.

**Methods**:
- `__init__(self, proxy: str = None, connector: BaseConnector = None)`: Initializes the `MetaAI` object with optional proxy and connector.
- `create_async_generator(cls, model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`: Creates an asynchronous generator for processing prompts.
- `update_access_token(self, birthday: str = "1999-01-01")`: Updates the access token for authenticated requests.
- `prompt(self, message: str, cookies: Cookies = None) -> AsyncResult`: Sends a prompt to the Meta AI service and yields the response in chunks.
- `update_cookies(self, cookies: Cookies = None)`: Updates the cookies required for authentication.
- `fetch_sources(self, fetch_id: str) -> Sources`: Fetches sources related to a specific fetch ID.
- `extract_value(text: str, key: str = None, start_str = None, end_str = '\',\') -> str`: Extracts a value from a given text using specified start and end strings.

## Class Methods

### `__init__`

```python
def __init__(self, proxy: str = None, connector: BaseConnector = None) -> None:
    """Инициализирует объект `MetaAI`.

    Args:
        proxy (str, optional): Прокси-сервер для использования при подключении. По умолчанию `None`.
        connector (BaseConnector, optional): Кастомный коннектор для `aiohttp.ClientSession`. По умолчанию `None`.
    """
    ...
```

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
    """Создает асинхронный генератор для обработки подсказок.

    Args:
        model (str): Модель для использования.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): Прокси-сервер для использования при подключении. По умолчанию `None`.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий фрагменты ответа.
    """
    ...
```

### `update_access_token`

```python
async def update_access_token(self, birthday: str = "1999-01-01") -> None:
    """Обновляет токен доступа для аутентифицированных запросов.

    Args:
        birthday (str, optional): Дата рождения для использования при обновлении токена. По умолчанию "1999-01-01".

    Raises:
        ResponseError: Если не удается получить токен доступа.
    """
    ...
```

### `prompt`

```python
async def prompt(self, message: str, cookies: Cookies = None) -> AsyncResult:
    """Отправляет запрос в сервис Meta AI и возвращает ответ по частям.

    Args:
        message (str): Текст сообщения для отправки.
        cookies (Cookies, optional): Куки для использования при запросе. По умолчанию `None`.

    Yields:
        AsyncResult: Части ответа от сервиса Meta AI.

    Raises:
        ResponseError: Если возникает ошибка при получении ответа.
    """
    ...
```

### `update_cookies`

```python
async def update_cookies(self, cookies: Cookies = None) -> None:
    """Обновляет куки, необходимые для аутентификации.

    Args:
        cookies (Cookies, optional): Куки для обновления. По умолчанию `None`.

    Raises:
        AbraGeoBlockedError: Если Meta AI недоступна в стране пользователя.
        ResponseError: Если не удается получить куки.
    """
    ...
```

### `fetch_sources`

```python
async def fetch_sources(self, fetch_id: str) -> Sources:
    """Извлекает источники, связанные с определенным идентификатором извлечения.

    Args:
        fetch_id (str): Идентификатор извлечения для получения источников.

    Returns:
        Sources: Объект `Sources`, содержащий список источников.

    Raises:
        RuntimeError: Если возникает ошибка при обработке ответа.
        ResponseError: Если не удается получить источники.
    """
    ...
```

### `extract_value`

```python
@staticmethod
def extract_value(text: str, key: str = None, start_str = None, end_str = '\',\') -> str:
    """Извлекает значение из текста, используя указанные начальные и конечные строки.

    Args:
        text (str): Текст для извлечения значения.
        key (str, optional): Ключ для поиска начальной строки. По умолчанию `None`.
        start_str (str, optional): Начальная строка для поиска значения. По умолчанию `None`.
        end_str (str, optional): Конечная строка для поиска значения. По умолчанию '\',\''.

    Returns:
        str: Извлеченное значение.
    """
    ...
```

## Functions

### `generate_offline_threading_id`

```python
def generate_offline_threading_id() -> str:
    """Генерирует автономный идентификатор потока.

    Returns:
        str: Сгенерированный автономный идентификатор потока.
    """
    ...
```

## Function Details

### `generate_offline_threading_id`

**Purpose**: Generates a unique ID for offline threading.

**Returns**:
- `str`: A string representing the generated offline threading ID.

**How the function works**:
- Generates a random 64-bit integer.
- Gets the current timestamp in milliseconds.
- Combines the timestamp and random value using bitwise operations.
- Returns the combined value as a string.

**Examples**:
```python
threading_id = generate_offline_threading_id()
print(f"Generated threading ID: {threading_id}")