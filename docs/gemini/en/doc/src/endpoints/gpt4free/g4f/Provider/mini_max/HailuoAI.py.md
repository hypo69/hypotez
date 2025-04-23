# Module Name: HailuoAI

## Overview

This module implements the HailuoAI provider for the `hypotez` project, enabling interaction with the Hailuo AI service. It includes functionalities for authentication, message creation, and streaming responses.

## More details

The `HailuoAI` module is designed to facilitate communication with the Hailuo AI platform. It uses asynchronous requests for non-blocking operations and supports streaming responses to efficiently handle large amounts of data. The module is part of a broader system that integrates multiple AI providers, offering a flexible way to interact with different AI models.

## Classes

### `Conversation`

**Description**: This class encapsulates conversation-specific data such as token, chat ID, and character ID.

**Attributes**:
- `token` (str): Authentication token for the conversation.
- `chatID` (str): Unique identifier for the chat.
- `characterID` (str, optional): Identifier for the character or persona in the chat. Defaults to 1.

### `HailuoAI`

**Description**: This class represents the HailuoAI provider, inheriting from `AsyncAuthedProvider` and `ProviderModelMixin`. It handles authentication, message creation, and streaming responses from the Hailuo AI service.

**Inherits**:
- `AsyncAuthedProvider`: Provides asynchronous authentication capabilities.
- `ProviderModelMixin`: Provides utilities for working with provider models.

**Attributes**:
- `label` (str): The label or name of the provider ("Hailuo AI").
- `url` (str): The base URL for the Hailuo AI service ("https://www.hailuo.ai").
- `working` (bool): A flag indicating whether the provider is currently working (True).
- `use_nodriver` (bool): Indicates whether the provider uses a nodriver approach (True).
- `supports_stream` (bool): Indicates whether the provider supports streaming responses (True).
- `default_model` (str): The default model used by the provider ("MiniMax").

**Methods**:

- `on_auth_async`: Handles the asynchronous authentication process.
- `create_authed`: Creates an authenticated session and sends messages to the AI model.

## Class Methods

### `on_auth_async`

```python
@classmethod
async def on_auth_async(cls, proxy: str = None, **kwargs) -> AsyncIterator:
    """Асинхронно обрабатывает процесс аутентификации.

    Args:
        proxy (str, optional): URL прокси-сервера для использования при подключении. По умолчанию `None`.
        **kwargs: Дополнительные параметры.

    Yields:
        AsyncIterator: Асинхронный итератор для результатов аутентификации.
    """
    ...
```

**Purpose**: Asynchronously handles the authentication process for the Hailuo AI provider.

**Parameters**:
- `proxy` (str, optional): URL of the proxy server to use for the connection. Defaults to `None`.
- `**kwargs`: Additional parameters.

**Yields**:
- `AsyncIterator`: An asynchronous iterator for authentication results.

**How the function works**:
1. Checks for a login URL in the environment variables.
2. Yields a `RequestLogin` object if a login URL is found.
3. Creates a `CallbackResults` object to store callback results.
4. Retrieves authentication arguments from the nodriver.
5. Yields an `AuthResult` object containing the authentication results.

### `create_authed`

```python
@classmethod
async def create_authed(
    cls,
    model: str,
    messages: Messages,
    auth_result: AuthResult,
    return_conversation: bool = False,
    conversation: Conversation = None,
    **kwargs
) -> AsyncResult:
    """Создает аутентифицированный сеанс и отправляет сообщения в AI модель.

    Args:
        model (str): Используемая модель.
        messages (Messages): Список сообщений для отправки.
        auth_result (AuthResult): Результаты аутентификации.
        return_conversation (bool, optional): Определяет, нужно ли возвращать объект Conversation. По умолчанию `False`.
        conversation (Conversation, optional): Существующий объект Conversation. По умолчанию `None`.
        **kwargs: Дополнительные параметры.

    Yields:
        AsyncResult: Асинхронный результат с ответом от AI модели.
    """
    ...
```

**Purpose**: Creates an authenticated session and sends messages to the AI model.

**Parameters**:
- `model` (str): The model to be used.
- `messages` (Messages): A list of messages to be sent.
- `auth_result` (AuthResult): Authentication results.
- `return_conversation` (bool, optional): Determines whether to return a Conversation object. Defaults to `False`.
- `conversation` (Conversation, optional): An existing Conversation object. Defaults to `None`.
- `**kwargs`: Additional parameters.

**Yields**:
- `AsyncResult`: An asynchronous result containing the response from the AI model.

**How the function works**:
1. Extracts arguments from the `auth_result`.
2. Creates an asynchronous client session using the extracted arguments.
3. Constructs form data with `characterID`, `msgContent`, `chatID`, and `searchMode`.
4. Generates headers including the token and `yy` header.
5. Sends a POST request to the Hailuo AI service with the form data and headers.
6. Processes the streaming response, yielding title generation and conversation objects.
7. Extracts and yields message content from the response.

**Examples**:

1. **Creating an authenticated session and sending a message**:
    ```python
    auth_result = AuthResult(token='example_token', path_and_query='/api/chat', timestamp='1234567890', impersonate=False)
    messages = [{'role': 'user', 'content': 'Hello, Hailuo AI!'}]
    async for result in HailuoAI.create_authed(model='MiniMax', messages=messages, auth_result=auth_result, return_conversation=True):
        print(result)
    ```

2. **Using an existing conversation**:
    ```python
    conversation = Conversation(token='example_token', chatID='123')
    messages = [{'role': 'user', 'content': 'Continue the conversation...'}]
    async for result in HailuoAI.create_authed(model='MiniMax', messages=messages, auth_result=auth_result, conversation=conversation):
        print(result)