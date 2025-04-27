# Grok AI Provider

## Overview

This module provides a provider for the Grok AI service, enabling interaction with the Grok API for generating responses from different Grok models. The provider handles authentication, message formatting, and response parsing, streamlining the integration with Grok AI for various tasks.

## Details

The Grok provider is a part of the `hypotez` project, designed for working with different AI models and services. The provider specifically targets the Grok AI API, offering a convenient interface to utilize its features within the `hypotez` framework. 

## Classes

### `Conversation`

**Description**:  Represents a conversation with Grok AI, storing the conversation ID.

**Attributes**:

-   `conversation_id` (str): The unique identifier of the conversation.

### `Grok`

**Description**: The main class for interacting with the Grok AI service. It inherits from `AsyncAuthedProvider` and `ProviderModelMixin`, ensuring proper authentication and model handling.

**Attributes**:

-   `label` (str): The provider label, set to "Grok AI".
-   `url` (str): The base URL of the Grok API.
-   `cookie_domain` (str): The cookie domain for Grok AI.
-   `assets_url` (str): The URL for accessing Grok AI assets.
-   `conversation_url` (str): The URL for managing Grok AI conversations.
-   `needs_auth` (bool): Indicates whether authentication is required, set to `True`.
-   `working` (bool): Indicates whether the provider is functional, set to `True`.
-   `default_model` (str): The default Grok AI model, set to "grok-3".
-   `models` (List[str]): A list of supported Grok AI models.
-   `model_aliases` (Dict[str, str]): A dictionary mapping model aliases to their corresponding models.

**Methods**:

-   `on_auth_async` (classmethod): Handles authentication with Grok AI. It retrieves cookies, impersonates a Chrome browser, and sets up headers for authenticated requests.
-   `_prepare_payload` (classmethod): Constructs the request payload for Grok AI, including parameters for model selection, message content, and various generation options.
-   `create_authed` (classmethod): Sends a request to Grok AI for generating responses, handling conversation management and response streaming. It formats the prompt, sends requests to the appropriate API endpoint based on the conversation status, and parses responses for text, images, reasoning, and other information.

## Class Methods

### `on_auth_async`

```python
    @classmethod
    async def on_auth_async(cls, cookies: Cookies = None, proxy: str = None, **kwargs) -> AsyncIterator:
        """
        Обработчик аутентификации для Grok AI.

        Args:
            cookies (Cookies, optional): Словарь cookies для авторизации. По умолчанию `None`.
            proxy (str, optional): Прокси-сервер для запросов. По умолчанию `None`.
            **kwargs: Дополнительные аргументы.

        Returns:
            AsyncIterator: Асинхронный итератор, возвращающий `AuthResult` или `RequestLogin`.
        """
```

This method handles the authentication process for the Grok AI provider. It checks for existing cookies, initiates a login request if necessary, and returns an `AuthResult` object containing the authentication information. The method uses a combination of cookies and a proxy server to achieve authentication.

### `_prepare_payload`

```python
    @classmethod
    async def _prepare_payload(cls, model: str, message: str) -> Dict[str, Any]:
        """
        Подготавливает данные для отправки запроса к Grok AI.

        Args:
            model (str): Имя модели Grok AI.
            message (str): Текстовое сообщение для модели.

        Returns:
            Dict[str, Any]: Словарь с данными для запроса.
        """
```

This method prepares the request payload for interacting with the Grok AI API. It constructs a dictionary containing parameters related to the selected model, user message, file attachments, image attachments, generation options, and other settings. This payload is then used when sending requests to the Grok AI API.

### `create_authed`

```python
    @classmethod
    async def create_authed(
        cls,
        model: str,
        messages: Messages,
        auth_result: AuthResult,
        cookies: Cookies = None,
        return_conversation: bool = False,
        conversation: Conversation = None,
        **kwargs
    ) -> AsyncResult:
        """
        Создает запрос к Grok AI с использованием авторизации.

        Args:
            model (str): Имя модели Grok AI.
            messages (Messages): Список сообщений в текущей беседе.
            auth_result (AuthResult): Результат аутентификации.
            cookies (Cookies, optional): Словарь cookies для запроса. По умолчанию `None`.
            return_conversation (bool, optional): Если `True`, возвращает `Conversation` объект. По умолчанию `False`.
            conversation (Conversation, optional): Текущий `Conversation` объект. По умолчанию `None`.
            **kwargs: Дополнительные аргументы.

        Returns:
            AsyncResult: Асинхронный результат, возвращающий `ImagePreview`, `Reasoning`, `ImageResponse`, `TitleGeneration`, или `Conversation`.
        """
```

This method is responsible for sending requests to the Grok AI API for generating responses. It handles authentication, message formatting, response parsing, and conversation management. The method takes into account various parameters, such as the chosen model, conversation history, and authentication information. It iterates through streamed responses, handling text, images, reasoning, and title generation results. It also returns a `Conversation` object if requested, allowing for continued interaction with the same conversation.


## Parameter Details

-   `model` (str): The name of the Grok AI model to be used. For example, `grok-3`, `grok-3-thinking`, or `grok-2`.
-   `messages` (Messages): A list of messages in the current conversation, representing the conversation history.
-   `auth_result` (AuthResult): The result of the authentication process, containing cookies and headers for authenticated requests.
-   `cookies` (Cookies, optional): A dictionary of cookies for the request.
-   `return_conversation` (bool, optional): Specifies whether to return a `Conversation` object, useful for managing ongoing conversations.
-   `conversation` (Conversation, optional): The current `Conversation` object, representing the existing conversation.
-   `proxy` (str, optional): The proxy server to be used for requests.
-   `kwargs`: Additional keyword arguments.

## How the Function Works

The `create_authed` method handles the core functionality of interacting with Grok AI. It first prepares the request payload using the `_prepare_payload` method. Based on the conversation status, it determines the correct API endpoint to send the request. The method then uses a `StreamSession` to send the request and iterates through the streamed responses using `iter_lines`.

During iteration, it parses the received JSON data, extracting information such as the conversation ID, response content, image generation results, reasoning steps, and generated titles. It yields different types of results based on the response data, including `ImagePreview`, `Reasoning`, `ImageResponse`, and `TitleGeneration`. Finally, it returns a `Conversation` object if requested, allowing for continued interaction with the same conversation.


## Examples

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.Grok import Grok

async def example_usage():
    """
    Пример использования Grok AI provider.
    """

    # Authentication is assumed to have been handled beforehand

    # Initialize a conversation with the Grok provider
    async with Grok.create_authed(model="grok-3", messages=[{"role": "user", "content": "Hello, how are you?"}], auth_result=auth_result) as result:
        async for response in result:
            if isinstance(response, Reasoning):
                print(f"Reasoning: {response.status}")  # Output: Reasoning: 🤔 Is thinking...
            elif isinstance(response, TitleGeneration):
                print(f"Title: {response.title}")  # Output: Title: Grok AI Response
            elif isinstance(response, ImageResponse):
                print(f"Image: {response.images[0]}")  # Output: Image: https://assets.grok.com/image-url
            elif isinstance(response, str):
                print(f"Response: {response}")  # Output: Response: I am doing well! How about you? 
            elif isinstance(response, ImagePreview):
                print(f"Image Preview: {response.url}")  # Output: Image Preview: https://assets.grok.com/image-preview-url
            else:
                print(f"Unknown Response Type: {response}")

    # This example demonstrates how to utilize the Grok AI provider for generating responses, 
    # including text, images, reasoning steps, and title generation. The provider handles the authentication process,
    #  message formatting, and response parsing, providing a simplified interface for working with Grok AI.