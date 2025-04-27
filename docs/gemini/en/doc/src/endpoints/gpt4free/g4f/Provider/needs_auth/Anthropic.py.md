# Anthropic API Provider
## Overview

This module implements the `Anthropic` class, which provides an interface for interacting with the Anthropic API for large language models. It inherits functionality from the `OpenaiAPI` class and extends it to handle specific features and requirements of Anthropic.

## Details

The `Anthropic` class is responsible for:

- **Authentication:** Handling API key authentication with the Anthropic API.
- **Model Selection:** Allowing users to specify the desired Anthropic model for interactions.
- **API Requests:** Sending requests to the Anthropic API based on user-provided prompts and parameters.
- **Response Handling:** Parsing and processing responses from the Anthropic API, returning results in a user-friendly format.

## Classes

### `class Anthropic`
**Description**: Класс `Anthropic` предоставляет доступ к API Anthropic для взаимодействия с моделями больших языков. Он наследует функциональность от класса `OpenaiAPI` и расширяет ее, чтобы обрабатывать специфические функции и требования Anthropic.

**Inherits**: `OpenaiAPI`

**Attributes**:

- `label` (str): Имя API провайдера.
- `url` (str): URL-адрес веб-сайта API.
- `login_url` (str): URL-адрес страницы входа в API.
- `working` (bool): Флаг, указывающий на доступность API.
- `api_base` (str): Базовый URL-адрес API.
- `needs_auth` (bool): Флаг, указывающий на необходимость аутентификации.
- `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи ответов.
- `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений.
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений.
- `default_model` (str): Имя модели по умолчанию.
- `models` (list): Список доступных моделей.
- `models_aliases` (dict): Словарь псевдонимов для моделей.

**Methods**:

- `get_models(cls, api_key: str = None, **kwargs)`: Получает список доступных моделей.
- `create_async_generator(cls, model: str, messages: Messages, proxy: str = None, timeout: int = 120, media: MediaListType = None, api_key: str = None, temperature: float = None, max_tokens: int = 4096, top_k: int = None, top_p: float = None, stop: list[str] = None, stream: bool = False, headers: dict = None, impersonate: str = None, tools: Optional[list] = None, extra_data: dict = {}, **kwargs) -> AsyncResult`: Создает асинхронный генератор для взаимодействия с API.
- `get_headers(cls, stream: bool, api_key: str = None, headers: dict = None) -> dict`: Возвращает заголовки для запросов к API.

## Class Methods

### `get_models(cls, api_key: str = None, **kwargs)`

**Purpose**: Функция получает список доступных моделей из API Anthropic. 

**Parameters**:

- `api_key` (str, optional): Ключ API для аутентификации. По умолчанию `None`.

**Returns**:

- `list`: Список доступных моделей.

**Raises Exceptions**:

- `requests.exceptions.HTTPError`: Если запрос к API завершился ошибкой.

**How the Function Works**:

- Функция `get_models` отправляет запрос GET к URL-адресу `https://api.anthropic.com/v1/models`, используя ключ API `api_key` для аутентификации. 
- Если запрос завершился успешно, функция извлекает список моделей из ответа JSON и возвращает его. 
- Если запрос завершился ошибкой, функция вызывает исключение `requests.exceptions.HTTPError`.

**Examples**:

```python
>>> Anthropic.get_models(api_key='YOUR_API_KEY')
['claude-3-5-sonnet-latest', 'claude-3-5-sonnet-20241022', 'claude-3-5-haiku-latest', 'claude-3-5-haiku-20241022', 'claude-3-opus-latest', 'claude-3-opus-20240229', 'claude-3-sonnet-20240229', 'claude-3-haiku-20240307']
```

### `create_async_generator(cls, model: str, messages: Messages, proxy: str = None, timeout: int = 120, media: MediaListType = None, api_key: str = None, temperature: float = None, max_tokens: int = 4096, top_k: int = None, top_p: float = None, stop: list[str] = None, stream: bool = False, headers: dict = None, impersonate: str = None, tools: Optional[list] = None, extra_data: dict = {}, **kwargs) -> AsyncResult`

**Purpose**: Функция создает асинхронный генератор для взаимодействия с API Anthropic. 

**Parameters**:

- `model` (str): Имя модели.
- `messages` (Messages): Список сообщений для отправки в API.
- `proxy` (str, optional): Proxy-сервер для запросов. По умолчанию `None`.
- `timeout` (int, optional): Таймаут для запроса. По умолчанию 120 секунд.
- `media` (MediaListType, optional): Список медиа-файлов для отправки в API. По умолчанию `None`.
- `api_key` (str, optional): Ключ API для аутентификации. По умолчанию `None`.
- `temperature` (float, optional): Температура модели. По умолчанию `None`.
- `max_tokens` (int, optional): Максимальное количество токенов в ответе. По умолчанию 4096.
- `top_k` (int, optional): Параметр `top_k` для модели. По умолчанию `None`.
- `top_p` (float, optional): Параметр `top_p` для модели. По умолчанию `None`.
- `stop` (list[str], optional): Список стоп-слов для модели. По умолчанию `None`.
- `stream` (bool, optional): Флаг, указывающий на потоковую передачу ответа. По умолчанию `False`.
- `headers` (dict, optional): Дополнительные заголовки для запроса. По умолчанию `None`.
- `impersonate` (str, optional):  Имитация пользователя. По умолчанию `None`.
- `tools` (Optional[list], optional):  Список инструментов, которые могут быть использованы моделью. По умолчанию `None`.
- `extra_data` (dict, optional): Дополнительные данные для запроса. По умолчанию `{}`.

**Returns**:

- `AsyncResult`: Асинхронный генератор, который будет выдавать ответы модели по мере их получения.

**Raises Exceptions**:

- `MissingAuthError`: Если ключ API отсутствует.
- `requests.exceptions.HTTPError`: Если запрос к API завершился ошибкой.

**How the Function Works**:

- Функция `create_async_generator` создает асинхронный генератор для взаимодействия с API Anthropic.
- Она отправляет запрос POST к URL-адресу `https://api.anthropic.com/v1/messages` с данными запроса, включающими:
    - Модель
    - Сообщения
    - Дополнительные параметры (температура, максимальное количество токенов, стоп-слова и т. д.)
- Генератор будет выдавать ответы модели по мере их получения в виде строк или объектов `ToolCalls`, `FinishReason` и `Usage`. 
- Функция также обрабатывает ошибки, вызывая соответствующие исключения.

**Examples**:

```python
>>> messages = [
...     {'role': 'user', 'content': 'Hello, world!' },
...     {'role': 'assistant', 'content': 'Hello, world!' }
... ]
>>> async for response in Anthropic.create_async_generator(model='claude-3-5-sonnet-latest', messages=messages, api_key='YOUR_API_KEY'):
...     print(response)
Hello, world!
```

### `get_headers(cls, stream: bool, api_key: str = None, headers: dict = None) -> dict`

**Purpose**: Функция возвращает заголовки для запросов к API Anthropic.

**Parameters**:

- `stream` (bool): Флаг, указывающий на потоковую передачу ответа.
- `api_key` (str, optional): Ключ API для аутентификации. По умолчанию `None`.
- `headers` (dict, optional): Дополнительные заголовки для запроса. По умолчанию `None`.

**Returns**:

- `dict`: Словарь с заголовками.

**How the Function Works**:

- Функция `get_headers` создает словарь с заголовками для запросов к API Anthropic. 
- Заголовки включают:
    - `Accept`: `text/event-stream` для потоковой передачи ответа или `application/json` для обычного ответа.
    - `Content-Type`: `application/json`.
    - `x-api-key`: Ключ API, если он предоставлен.
    - `anthropic-version`: `2023-06-01`.
    - Дополнительные заголовки, если они предоставлены.

**Examples**:

```python
>>> Anthropic.get_headers(stream=True, api_key='YOUR_API_KEY')
{'Accept': 'text/event-stream', 'Content-Type': 'application/json', 'x-api-key': 'YOUR_API_KEY', 'anthropic-version': '2023-06-01'}
```