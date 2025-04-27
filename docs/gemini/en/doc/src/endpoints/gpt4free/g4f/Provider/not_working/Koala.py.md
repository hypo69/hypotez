# Koala.py

## Overview

This module implements the `Koala` class, which is a provider for the Koala AI model. It inherits from `AsyncGeneratorProvider` and `ProviderModelMixin` and provides an asynchronous generator for interacting with the Koala API.

## Details

The `Koala` class provides a method `create_async_generator` which takes the following arguments:

- `model`: The desired Koala model (default is `gpt-4o-mini`).
- `messages`: A list of messages in the conversation history.
- `proxy`: An optional proxy server to use.
- `connector`: An optional aiohttp connector to use.
- `**kwargs`: Additional keyword arguments.

The `create_async_generator` method returns an asynchronous generator that yields dictionaries containing the responses from the Koala API.

## Classes

### `class Koala`

**Description:** This class represents the Koala AI model provider.

**Inherits:**

- `AsyncGeneratorProvider`: Provides the base functionality for asynchronous generators.
- `ProviderModelMixin`: Provides common model-related functionality.

**Attributes:**

- `url`: The base URL for the Koala chat interface.
- `api_endpoint`: The endpoint for the Koala API.
- `working`: A boolean flag indicating whether the provider is working (default is `False`).
- `supports_message_history`: A boolean flag indicating whether the provider supports message history (default is `True`).
- `default_model`: The default model to use if no model is specified (default is `gpt-4o-mini`).

**Methods:**

- `create_async_generator()`: Returns an asynchronous generator that yields responses from the Koala API.
- `_parse_event_stream()`: Parses event stream chunks from the API response.

## Class Methods

### `create_async_generator()`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: Optional[str] = None,
        connector: Optional[BaseConnector] = None,
        **kwargs: Any
    ) -> AsyncGenerator[Dict[str, Union[str, int, float, List[Dict[str, Any]], None]], None]:
        """ 
        Создает асинхронный генератор, который получает ответы от API Koala.

        Args:
            model (str): Имя модели Koala.
            messages (Messages): Список сообщений в истории чата.
            proxy (Optional[str], optional): Прокси-сервер. По умолчанию None.
            connector (Optional[BaseConnector], optional): Асинхронный соединитель. По умолчанию None.
            **kwargs (Any): Дополнительные аргументы.

        Returns:
            AsyncGenerator[Dict[str, Union[str, int, float, List[Dict[str, Any]], None]], None]: Асинхронный генератор, 
                который возвращает ответы от API Koala в виде словарей.
        """
```

This method sets up the HTTP headers and sends a POST request to the Koala API with the input text and conversation history. It then parses the response from the API using the `_parse_event_stream` method and yields the parsed chunks as dictionaries.


### `_parse_event_stream()`

```python
    @staticmethod
    async def _parse_event_stream(response: ClientResponse) -> AsyncGenerator[Dict[str, Any], None]:
        """ 
        Парсит данные из потока событий API.

        Args:
            response (ClientResponse): Ответ от API.

        Returns:
            AsyncGenerator[Dict[str, Any], None]: Асинхронный генератор, который возвращает словари с данными.
        """
```

This method iterates over the chunks of the API response, extracts the data from the `data: ` lines, and yields them as dictionaries.

## Parameter Details

- `model` (str): The name of the Koala model to use.
- `messages` (Messages): A list of messages in the conversation history. Each message is a dictionary containing the `role` (user or assistant) and `content` of the message.
- `proxy` (Optional[str]): An optional proxy server to use.
- `connector` (Optional[BaseConnector]): An optional aiohttp connector to use.
- `**kwargs`: Additional keyword arguments.

## Examples

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.Koala import Koala
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Create a list of messages for the conversation history
messages: Messages = [
    {"role": "user", "content": "Hello, how are you?"},
    {"role": "assistant", "content": "I am doing well, thank you for asking. How can I help you today?"},
]

# Create an instance of the Koala class
koala = Koala()

# Create an asynchronous generator for the conversation
async_generator = koala.create_async_generator(model="gpt-4o-mini", messages=messages)

# Iterate over the responses from the API
async for chunk in async_generator:
    print(chunk)
```