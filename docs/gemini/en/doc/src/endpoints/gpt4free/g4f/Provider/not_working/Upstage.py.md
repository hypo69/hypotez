# Module for interaction with Upstage AI models.

## Overview

This module enables interaction with Upstage AI models for generating text using asynchronous requests. It supports different models, including 'solar-pro' and 'upstage/solar-1-mini-chat', and provides functionality for formatting prompts and handling responses in streaming mode.

## More details

The module facilitates communication with the Upstage AI API, handling request headers, data formatting, and response parsing. It is designed to be integrated into systems requiring asynchronous text generation capabilities. The module uses `aiohttp` for making asynchronous HTTP requests, and the `src.logger` module for logging errors.

## Classes

### `Upstage`

**Description**: The class responsible for interacting with the Upstage AI models.

**Inherits**:
- `AsyncGeneratorProvider`: Inherits asynchronous generation capabilities.
- `ProviderModelMixin`: Inherits functionality for managing and retrieving model information.

**Attributes**:
- `url` (str): URL of the Upstage AI playground.
- `api_endpoint` (str): API endpoint for chat completions.
- `working` (bool): A flag indicating if the provider is operational.
- `default_model` (str): The default model to be used if none is specified.
- `models` (list): List of supported models.
- `model_aliases` (dict): Aliases for model names.

**Working principle**:
The class defines the necessary settings and methods to interact with the Upstage AI API. It prepares the request headers, formats the message payload, sends the request, and parses the streaming response to extract the generated text.

## Class Methods

### `get_model`

```python
    @classmethod
    def get_model(cls, model: str) -> str:
        """
        Возвращает допустимую модель на основе предоставленного имени модели или псевдонима.

        Args:
            model (str): Имя модели для получения.

        Returns:
            str: Допустимое имя модели или имя модели по умолчанию, если предоставленное имя недопустимо.

        """
```

**Purpose**:
Retrieves a valid model name based on the provided model name or alias.

**Parameters**:
- `model` (str): The model name to retrieve.

**Returns**:
- `str`: A valid model name or the default model name if the provided name is invalid.

**How the function works**:
The function checks if the provided model name is in the list of supported models or model aliases. If a match is found in the aliases, it returns the corresponding full model name. If the model name is not found in either list, it returns the default model name.

**Examples**:
```python
Upstage.get_model('solar-pro')  # Returns 'solar-pro'
Upstage.get_model('solar-mini')  # Returns 'upstage/solar-1-mini-chat-ja'
Upstage.get_model('invalid-model')  # Returns 'solar-pro'
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
        """
        Создает асинхронный генератор для взаимодействия с API Upstage.

        Args:
            model (str): Имя модели для использования.
            messages (Messages): Список сообщений для отправки в API.
            proxy (str, optional): URL прокси-сервера для использования. По умолчанию `None`.
            **kwargs: Дополнительные аргументы.

        Returns:
            AsyncResult: Асинхронный генератор, выдающий текстовые фрагменты из ответа API.

        Raises:
            Exception: В случае ошибки во время запроса или обработки ответа.

        """
```

**Purpose**:
Creates an asynchronous generator for interacting with the Upstage API.

**Parameters**:
- `model` (str): The model name to use.
- `messages` (Messages): A list of messages to send to the API.
- `proxy` (str, optional): The URL of the proxy server to use. Defaults to `None`.
- `**kwargs`: Additional arguments.

**Returns**:
- `AsyncResult`: An asynchronous generator yielding text chunks from the API response.

**How the function works**:
The function prepares the request headers and payload, sends an asynchronous POST request to the Upstage API, and processes the streaming response. It extracts the content from the JSON data in each line of the response and yields it as a text chunk. If an error occurs during the request or response processing, it logs the error and continues.

**Examples**:
```python
messages = [{"role": "user", "content": "Tell me a story."}]
async for chunk in Upstage.create_async_generator(model='solar-pro', messages=messages):
    print(chunk)
```
## Class Parameters

- `url` (str): The base URL for the Upstage AI service.
- `api_endpoint` (str): The specific endpoint for chat completions.
- `working` (bool): A flag indicating whether the provider is currently operational.
- `default_model` (str): The default AI model used if none is specified.
- `models` (list): A list of available AI models supported by Upstage.
- `model_aliases` (dict): A dictionary of aliases for the model names.