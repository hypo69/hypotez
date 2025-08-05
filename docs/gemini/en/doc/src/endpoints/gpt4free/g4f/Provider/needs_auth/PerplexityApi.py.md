# Perplexity API Provider

## Overview

This module implements the `PerplexityApi` class, which provides access to the Perplexity API. It inherits from the `OpenaiTemplate` class, providing a standardized interface for interacting with various API providers. 

## Details

The `PerplexityApi` class defines the specific details of interacting with the Perplexity API, including:

- **Base URL:** `https://api.perplexity.ai`
- **Default Model:** `llama-3-sonar-large-32k-online`
- **Available Models:**  `llama-3-sonar-small-32k-chat`, `llama-3-sonar-large-32k-chat`, `llama-3-sonar-large-32k-online`, `llama-3-8b-instruct`, `llama-3-70b-instruct`


## Classes

### `PerplexityApi`

**Description:** The `PerplexityApi` class represents a connection to the Perplexity API and provides methods for interacting with it. 

**Inherits:** `OpenaiTemplate`

**Attributes:**
- **label (str):** `Perplexity API` - Name of the API provider.
- **url (str):** `https://www.perplexity.ai` - The URL for the Perplexity website.
- **login_url (str):** `https://www.perplexity.ai/settings/api` - URL for logging into the API.
- **working (bool):** `True` - Indicates whether the API is currently operational.
- **needs_auth (bool):** `True` - Indicates whether authentication is required to use the API.
- **api_base (str):** `https://api.perplexity.ai` - The base URL for the API.
- **default_model (str):** `llama-3-sonar-large-32k-online` - The default model to use for requests.
- **models (list):** A list of available models supported by the API.


**Methods:** 

- **execute_prompt(prompt: str, model: str, temp: float = 0.7, top_p: float = 0.95, n: int = 1, max_tokens: int = 256, stop: str | list[str] | None = None, stream: bool = False, logprobs: int | None = None) -> dict | None:** Sends a request to the Perplexity API with the specified prompt and model. 
- **_get_token(token: str) -> str | None:** Retrieves and returns the user's access token.
- **_send_request(method: str, endpoint: str, data: dict, headers: dict, token: str | None = None) -> dict | None:** Sends an API request to the Perplexity API.
- **_prepare_payload(prompt: str, model: str, temp: float = 0.7, top_p: float = 0.95, n: int = 1, max_tokens: int = 256, stop: str | list[str] | None = None, stream: bool = False, logprobs: int | None = None) -> dict:**  Prepares the request payload for sending to the Perplexity API.
- **_handle_response(response: requests.Response) -> dict | None:** Processes the API response.

**Inner Functions:**

- **_get_token(token: str) -> str | None:** Retrieves and returns the user's access token.
- **_send_request(method: str, endpoint: str, data: dict, headers: dict, token: str | None = None) -> dict | None:** Sends an API request to the Perplexity API.
- **_prepare_payload(prompt: str, model: str, temp: float = 0.7, top_p: float = 0.95, n: int = 1, max_tokens: int = 256, stop: str | list[str] | None = None, stream: bool = False, logprobs: int | None = None) -> dict:**  Prepares the request payload for sending to the Perplexity API.
- **_handle_response(response: requests.Response) -> dict | None:** Processes the API response.

**Examples:**

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.PerplexityApi import PerplexityApi

# Create a PerplexityApi instance
perplexity_api = PerplexityApi()

# Send a request to the Perplexity API
response = perplexity_api.execute_prompt(prompt="What is the capital of France?", model="llama-3-sonar-large-32k-online")

# Process the response
if response:
    print(response['text'])
```

## Class Methods

### `execute_prompt`

```python
def execute_prompt(
    self,
    prompt: str,
    model: str,
    temp: float = 0.7,
    top_p: float = 0.95,
    n: int = 1,
    max_tokens: int = 256,
    stop: str | list[str] | None = None,
    stream: bool = False,
    logprobs: int | None = None,
) -> dict | None:
    """
    Выполняет запрос к API Perplexity с указанным запросом и моделью.

    Args:
        prompt (str): Текст запроса.
        model (str): Имя модели для использования.
        temp (float, optional): Температура для генерации текста. Defaults to 0.7.
        top_p (float, optional): Вероятностный отбор для генерации текста. Defaults to 0.95.
        n (int, optional): Количество генерируемых ответов. Defaults to 1.
        max_tokens (int, optional): Максимальное количество токенов для генерации. Defaults to 256.
        stop (str | list[str] | None, optional): Токен(ы) для остановки генерации. Defaults to None.
        stream (bool, optional): Включить режим потоковой передачи. Defaults to False.
        logprobs (int | None, optional): Количество токенов для вывода лог-вероятностей. Defaults to None.

    Returns:
        dict | None: Ответ API в формате словаря или `None` в случае ошибки.

    Raises:
        Exception: Ошибка при выполнении запроса.

    Example:
        >>> perplexity_api = PerplexityApi()
        >>> response = perplexity_api.execute_prompt(prompt="What is the capital of France?", model="llama-3-sonar-large-32k-online")
        >>> if response:
        ...     print(response['text'])
        Paris
    """
```

### `_get_token`

```python
def _get_token(self, token: str) -> str | None:
    """
    Возвращает токен доступа пользователя.

    Args:
        token (str): Токен доступа.

    Returns:
        str | None: Токен доступа или `None` в случае ошибки.

    Raises:
        Exception: Ошибка при получении токена.

    Example:
        >>> perplexity_api = PerplexityApi()
        >>> token = perplexity_api._get_token("my_access_token")
        >>> if token:
        ...     print(token)
        my_access_token
    """
```

### `_send_request`

```python
def _send_request(
    self, method: str, endpoint: str, data: dict, headers: dict, token: str | None = None
) -> dict | None:
    """
    Отправляет запрос к API Perplexity.

    Args:
        method (str): Метод HTTP-запроса (например, 'POST', 'GET').
        endpoint (str): Конечная точка API.
        data (dict): Данные для отправки.
        headers (dict): Заголовки запроса.
        token (str | None, optional): Токен доступа. Defaults to None.

    Returns:
        dict | None: Ответ API в формате словаря или `None` в случае ошибки.

    Raises:
        Exception: Ошибка при отправке запроса.

    Example:
        >>> perplexity_api = PerplexityApi()
        >>> response = perplexity_api._send_request(method='POST', endpoint='/generate', data={'prompt': 'What is the capital of France?'}, headers={'Authorization': 'Bearer my_access_token'})
        >>> if response:
        ...     print(response['text'])
        Paris
    """
```

### `_prepare_payload`

```python
def _prepare_payload(
    self,
    prompt: str,
    model: str,
    temp: float = 0.7,
    top_p: float = 0.95,
    n: int = 1,
    max_tokens: int = 256,
    stop: str | list[str] | None = None,
    stream: bool = False,
    logprobs: int | None = None,
) -> dict:
    """
    Подготавливает полезную нагрузку для отправки к API Perplexity.

    Args:
        prompt (str): Текст запроса.
        model (str): Имя модели для использования.
        temp (float, optional): Температура для генерации текста. Defaults to 0.7.
        top_p (float, optional): Вероятностный отбор для генерации текста. Defaults to 0.95.
        n (int, optional): Количество генерируемых ответов. Defaults to 1.
        max_tokens (int, optional): Максимальное количество токенов для генерации. Defaults to 256.
        stop (str | list[str] | None, optional): Токен(ы) для остановки генерации. Defaults to None.
        stream (bool, optional): Включить режим потоковой передачи. Defaults to False.
        logprobs (int | None, optional): Количество токенов для вывода лог-вероятностей. Defaults to None.

    Returns:
        dict: Полезная нагрузка для отправки к API.

    Example:
        >>> perplexity_api = PerplexityApi()
        >>> payload = perplexity_api._prepare_payload(prompt="What is the capital of France?", model="llama-3-sonar-large-32k-online")
        >>> print(payload)
        {'prompt': 'What is the capital of France?', 'model': 'llama-3-sonar-large-32k-online', 'temp': 0.7, 'top_p': 0.95, 'n': 1, 'max_tokens': 256, 'stop': None, 'stream': False, 'logprobs': None}
    """
```

### `_handle_response`

```python
def _handle_response(self, response: requests.Response) -> dict | None:
    """
    Обрабатывает ответ API Perplexity.

    Args:
        response (requests.Response): Ответ API.

    Returns:
        dict | None: Обработанный ответ API в формате словаря или `None` в случае ошибки.

    Raises:
        Exception: Ошибка при обработке ответа.

    Example:
        >>> perplexity_api = PerplexityApi()
        >>> response = perplexity_api._handle_response(response)
        >>> if response:
        ...     print(response['text'])
        Paris
    """
```