# Goabror Provider for GPT4Free

## Overview

This module defines the `Goabror` class, which implements an asynchronous generator-based provider for GPT4Free using the Goabror API. It allows users to access the GPT-4 model and receive responses as an asynchronous stream of messages.

## Details

The `Goabror` class inherits from `AsyncGeneratorProvider` and `ProviderModelMixin`, providing a standardized interface for interacting with GPT4Free models. It leverages the Goabror API for communication and utilizes `aiohttp` for asynchronous requests.

## Classes

### `class Goabror`

**Description**:  Provides asynchronous generation of responses from the Goabror API for GPT4Free.

**Inherits**: 
    - `AsyncGeneratorProvider`: Defines the base structure for asynchronous generator-based providers.
    - `ProviderModelMixin`: Encapsulates common features for different GPT4Free models.

**Attributes**:
    - `url` (str): Base URL for the Goabror service.
    - `api_endpoint` (str): Specific endpoint for the Goabror API for GPT-4.
    - `working` (bool): Flag indicating whether the provider is currently functional.
    - `default_model` (str): Default GPT4Free model name (`gpt-4` in this case).
    - `models` (list): Supported GPT4Free model names.

**Methods**:
    - `create_async_generator()`:  Asynchronously generates responses from the Goabror API based on provided messages.

## Class Methods

### `create_async_generator()`

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
        Асинхронно генерирует ответы от API Goabror на основе предоставленных сообщений.

        Args:
            model (str): Имя модели GPT4Free, например, `gpt-4`.
            messages (Messages): Список сообщений для отправки в API Goabror.
            proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
            **kwargs: Дополнительные аргументы для отправки в API Goabror.

        Returns:
            AsyncResult: Асинхронный результат с генератором ответов от API Goabror.

        Raises:
            Exception: Возникает при ошибках запросов к API Goabror.
        """
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
        }
        async with ClientSession(headers=headers) as session:
            params = {
                "user": format_prompt(messages, include_system=False),
                "system": get_system_prompt(messages),
            }
            async with session.get(f"{cls.api_endpoint}", params=params, proxy=proxy) as response:
                await raise_for_status(response)
                text_response = await response.text()
                try:
                    json_response = json.loads(text_response)
                    if "data" in json_response:
                        yield json_response["data"]
                    else:
                        yield text_response
                except json.JSONDecodeError:
                    yield text_response
```

**Purpose**:  Sends a request to the Goabror API with the provided messages and receives responses asynchronously.

**Parameters**:
    - `model` (str):  The GPT4Free model to use (e.g., `gpt-4`).
    - `messages` (Messages):  A list of messages to be sent to the API.
    - `proxy` (str, optional):  A proxy server to use. Defaults to `None`.
    - `**kwargs`:  Additional keyword arguments for the API request.

**Returns**:
    - `AsyncResult`: An asynchronous result containing a generator that yields responses from the API.

**Raises Exceptions**:
    - `Exception`: If an error occurs during API requests.

**How the Function Works**:
    1. Sets up headers for the HTTP request.
    2. Creates an asynchronous client session with the configured headers.
    3. Prepares request parameters:
        - `user`: The user prompt formatted for Goabror.
        - `system`: The system prompt (if available) formatted for Goabror.
    4. Sends a GET request to the Goabror API endpoint with the prepared parameters and optional proxy.
    5. Raises an exception if the request fails (using `raise_for_status`).
    6. Reads the response text.
    7. Attempts to parse the response as JSON. If successful, yields the `data` field from the JSON response. Otherwise, yields the raw response text.
    8. If a `json.JSONDecodeError` occurs, yields the raw response text.

**Examples**:

```python
async def example_goabror():
    messages = [
        {
            "role": "user",
            "content": "Hello, how are you today?",
        },
    ]
    async for response in Goabror.create_async_generator(model="gpt-4", messages=messages):
        print(f"Goabror Response: {response}")