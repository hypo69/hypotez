# Module for asynchronous generation of responses using the FlowGpt provider.

## Overview

This module contains the `FlowGpt` class, which is an asynchronous generator provider for interacting with the FlowGpt service. It supports message history and system messages, and provides access to various language models such as `gpt-3.5-turbo`, `gpt-4-turbo`, `google-gemini`, `claude-instant`, and others. The module uses asynchronous requests via `aiohttp` to efficiently generate responses.

## More details

The `FlowGpt` class inherits from `AsyncGeneratorProvider` and `ProviderModelMixin`, providing an interface for asynchronous generation of text responses. It supports setting up a connection to the FlowGpt service, sending requests, and processing responses in streaming mode. The module is designed to work with different models by specifying them when creating a generator.

## Classes

### `FlowGpt`

**Description**: Class for asynchronous generation of responses using the FlowGpt provider.
**Inherits**:
- `AsyncGeneratorProvider`: Provides an interface for asynchronous generation of data.
- `ProviderModelMixin`: Mixin for managing available models.

**Attributes**:
- `url` (str): URL of the FlowGpt service.
- `working` (bool): Indicates whether the provider is working.
- `supports_message_history` (bool): Indicates whether the provider supports message history.
- `supports_system_message` (bool): Indicates whether the provider supports system messages.
- `default_model` (str): Default model to use if none is specified.
- `models` (list): List of supported models.
- `model_aliases` (dict): Dictionary of model aliases for easier use.

**Working principle**:
The `FlowGpt` class configures headers for sending requests to the FlowGpt service, prepares data including message history and system messages, sends the request asynchronously, and processes the response in chunks. It extracts text data from the chunks and yields it, providing an asynchronous generator for receiving responses.

### Class Methods

#### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    temperature: float = 0.7,
    **kwargs
) -> AsyncResult:
    """
    Asynchronously creates a generator for receiving responses from the FlowGpt service.

    Args:
        cls (FlowGpt): The class object.
        model (str): Model to be used for generating the response.
        messages (Messages): List of messages forming the conversation history.
        proxy (str, optional): Proxy URL. Defaults to None.
        temperature (float, optional): Sampling temperature. Defaults to 0.7.
        **kwargs: Additional keyword arguments.

    Returns:
        AsyncResult: An asynchronous generator that yields responses from the FlowGpt service.

    Raises:
        Exception: If an error occurs during the request or response processing.

    Example:
        messages = [{"role": "user", "content": "Привет, как дела?"}]
        generator = await FlowGpt.create_async_generator(model="gpt-3.5-turbo", messages=messages)
        async for message in generator:
            print(message)
    """
```

**Parameters**:
- `cls`: Ссылка на класс `FlowGpt`.
- `model` (str): Название модели, используемой для генерации ответа.
- `messages (Messages)`: Список сообщений, формирующих историю разговора.
- `proxy (str, optional)`: URL прокси-сервера. По умолчанию `None`.
- `temperature (float, optional)`: Температура выборки. По умолчанию 0.7.
- `**kwargs`: Дополнительные именованные аргументы.

**Returns**:
- `AsyncResult`: Асинхронный генератор, выдающий ответы от сервиса FlowGpt.

**How the function works**:
The `create_async_generator` function is a class method that configures and sends a request to the FlowGpt service to generate responses. It takes the model name, message history, proxy settings, and temperature as input, and returns an asynchronous generator that yields responses from the service.
The function performs the following steps:
1. Gets the model name using the `get_model` method.
2. Creates a timestamp and generates a signature for authentication.
3. Configures headers for the request, including the `Authorization`, `x-flow-device-id`, `x-nonce`, `x-signature`, and `x-timestamp`.
4. Prepares data to be sent in the request body, including the model name, message history, system message, and temperature.
5. Sends an asynchronous POST request to the FlowGpt service using `aiohttp.ClientSession`.
6. Processes the response in chunks, extracting text data from the chunks and yielding it.
7. Handles errors by raising exceptions if the response status is not successful.

**Examples**:

```python
messages = [{"role": "user", "content": "Привет, как дела?"}]
generator = await FlowGpt.create_async_generator(model="gpt-3.5-turbo", messages=messages)
async for message in generator:
    print(message)