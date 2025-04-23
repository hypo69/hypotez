# Module for asynchronous interaction with MagickPen

## Overview

This module provides an asynchronous interface to interact with the MagickPen service. It includes functionality for fetching API credentials, creating asynchronous generators for streaming responses, and handling communication with the MagickPen API. This module is designed to support streaming responses, system messages, and message history.

## More details

This module is used to interact with the MagickPen service, an AI-powered tool that provides text generation capabilities. It asynchronously fetches API credentials, including `X-API-Secret`, signature, timestamp, nonce, and secret, by parsing a JavaScript file. These credentials are then used to construct headers for subsequent API requests. The module supports streaming responses by yielding chunks of data as they are received from the API, making it suitable for real-time text generation applications. The module provides asynchronous generator for streaming responses from the MagickPen service.

## Classes

### `MagickPen`

**Description**:
This class provides an asynchronous interface to the MagickPen service. It handles the retrieval of API credentials, formatting prompts, and streaming responses from the API.

**Inherits**:
- `AsyncGeneratorProvider`: Provides asynchronous generator functionality.
- `ProviderModelMixin`: Provides model-related utility functions.

**Attributes**:
- `url` (str): The base URL for the MagickPen service.
- `api_endpoint` (str): The API endpoint for sending requests.
- `working` (bool): Indicates whether the provider is working.
- `supports_stream` (bool): Indicates whether the provider supports streaming responses.
- `supports_system_message` (bool): Indicates whether the provider supports system messages.
- `supports_message_history` (bool): Indicates whether the provider supports message history.
- `default_model` (str): The default model to use if none is specified.
- `models` (list): A list of supported models.

**Methods**:
- `fetch_api_credentials()`: Asynchronously fetches API credentials from a JavaScript file.
- `create_async_generator()`: Creates an asynchronous generator for streaming responses from the API.

### `fetch_api_credentials`

```python
    @classmethod
    async def fetch_api_credentials(cls) -> tuple:
        """Asynchronously fetches API credentials required for accessing the MagickPen API.

        Извлекает необходимые API-ключи для доступа к API MagickPen асинхронно.

        Returns:
            tuple: A tuple containing the X_API_SECRET, signature, timestamp, nonce, and secret.
            Кортеж, содержащий X_API_SECRET, подпись, временную метку, nonce и secret.

        Raises:
            Exception: If unable to extract all necessary data from the JavaScript file.
            Исключение, если не удается извлечь все необходимые данные из JavaScript файла.
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
        """Creates an asynchronous generator for streaming responses from the MagickPen API.

        Создает асинхронный генератор для потоковой передачи ответов от API MagickPen.

        Args:
            model (str): The model to use for generating responses. Модель, используемая для генерации ответов.
            messages (Messages): A list of messages to send to the API. Список сообщений для отправки в API.
            proxy (str, optional): The proxy URL to use for the request. Defaults to None. URL прокси-сервера для запроса. По умолчанию None.
            **kwargs: Additional keyword arguments. Дополнительные аргументы ключевого слова.

        Returns:
            AsyncResult: An asynchronous generator that yields chunks of data from the API response.
            Асинхронный генератор, который выдает фрагменты данных из ответа API.
        """
        ...