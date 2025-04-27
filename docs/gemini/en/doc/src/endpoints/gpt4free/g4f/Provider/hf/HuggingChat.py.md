# HuggingChat Provider

## Overview

This module provides the `HuggingChat` class, which implements an asynchronous provider for interacting with the Hugging Face Chat API. 

It allows you to send text and images to the Hugging Face models and receive responses. 

## Details

The `HuggingChat` class implements the `AsyncAuthedProvider` and `ProviderModelMixin` interfaces, allowing it to be used with the `hypotez` project's architecture. It supports both text and image input, authentication, and streaming responses.

## Classes

### `class HuggingChat(AsyncAuthedProvider, ProviderModelMixin)`

**Description**: 
The `HuggingChat` class represents a provider for interacting with the Hugging Face Chat API. This provider handles authentication, sending requests to the API, and receiving responses. It supports both text and image input.

**Inherits**: 
- `AsyncAuthedProvider`: Provides asynchronous authentication functionality.
- `ProviderModelMixin`: Offers features related to handling different models.

**Attributes**:
- `domain (str)`: The domain name of the Hugging Face Chat API.
- `origin (str)`: The base URL for the Hugging Face Chat API.
- `url (str)`: The URL for the Chat API endpoint.
- `working (bool)`: Indicates whether the provider is currently working.
- `use_nodriver (bool)`: Indicates if the provider uses a headless browser driver or not.
- `supports_stream (bool)`: Indicates if the provider supports streaming responses.
- `needs_auth (bool)`: Indicates if the provider requires authentication.
- `default_model (str)`: The default text model.
- `default_vision_model (str)`: The default vision model.
- `model_aliases (dict)`: A dictionary mapping model aliases to their corresponding Hugging Face model IDs.
- `image_models (list)`: A list of image models supported by the provider.
- `text_models (list)`: A list of text models supported by the provider.
- `vision_models (list)`: A list of vision models (models supporting multimodal input) supported by the provider.

**Methods**:
- `get_models()`: Retrieves a list of all available Hugging Face models.
- `on_auth_async(cookies: Cookies = None, proxy: str = None, **kwargs) -> AsyncIterator`: Asynchronously handles authentication. 
- `create_authed(model: str, messages: Messages, auth_result: AuthResult, prompt: str = None, media: MediaListType = None, return_conversation: bool = False, conversation: Conversation = None, web_search: bool = False, **kwargs) -> AsyncResult`:  Creates a chat session and sends a request to the Hugging Face Chat API.
- `create_conversation(session: Session, model: str)`: Creates a new conversation with the specified model.
- `fetch_message_id(session: Session, conversation_id: str)`: Retrieves the message ID for a given conversation.

### `class Conversation(JsonConversation)`

**Description**: 
This class represents a conversation with a specific model, storing conversation ID and message ID. 

**Inherits**: 
- `JsonConversation`: A base class for conversations, allowing to store conversation data in a JSON format. 

**Attributes**:
- `models (dict)`: A dictionary to store information about different models used in the conversation. 

## Functions

### `add_quotation_mark(match)`

**Purpose**: 
Helper function to add quotation marks around model names in the response from the Hugging Face API.

**Parameters**:
- `match (Match)`: A match object representing the model name found in the API response.

**Returns**:
- `str`: The model name with added quotation marks.

**How the Function Works**:
- It takes a `Match` object representing a model name in the API response.
- It extracts the model name using `match.group(1)` and the colon using `match.group(2)`.
- It returns a string with the model name enclosed in single quotes and the colon.

### `format_prompt(messages)`

**Purpose**: 
Formats a list of messages into a string suitable for sending to the Hugging Face API.

**Parameters**:
- `messages (Messages)`: A list of message objects containing the conversation history.

**Returns**:
- `str`: A string containing the formatted prompt.

**How the Function Works**:
- It iterates over the list of messages.
- It constructs a string where each message is represented by a JSON object with `role` and `content` keys.
- It joins the JSON objects into a single string.

### `format_image_prompt(messages, prompt)`

**Purpose**: 
Formats an image prompt based on the given list of messages and the provided prompt.

**Parameters**:
- `messages (Messages)`: A list of message objects containing the conversation history.
- `prompt (str)`: The prompt for the image generation.

**Returns**:
- `str`: A formatted image prompt.

**How the Function Works**:
- It constructs a prompt string that combines the last user message from the conversation history with the provided image prompt.

### `get_last_user_message(messages)`

**Purpose**: 
Extracts the last user message from a list of message objects.

**Parameters**:
- `messages (Messages)`: A list of message objects containing the conversation history.

**Returns**:
- `str`: The last user message from the list.

**How the Function Works**:
- It iterates over the list of messages in reverse order.
- It returns the first message with the role "user".

### `get_args_from_nodriver(url: str, proxy: str = None, wait_for: str = None, **kwargs) -> dict`:

**Purpose**: 
Extracts arguments from a web page without using a headless browser driver.

**Parameters**:
- `url (str)`: The URL of the webpage.
- `proxy (str)`: The proxy server to use for the request.
- `wait_for (str)`: A CSS selector that specifies the element to wait for before extracting arguments.
- `**kwargs`: Additional arguments passed to the `requests.get` function.

**Returns**:
- `dict`: A dictionary containing extracted arguments.

**How the Function Works**:
- It sends a GET request to the given URL.
- It waits for the specified element to be present on the page using `wait_for`.
- It extracts the arguments from the form using `requests.get` and parses them into a dictionary.

### `merge_media(media: MediaListType, messages: Messages) -> list`:

**Purpose**:
Merges media from the `media` argument and messages.

**Parameters**:
- `media (MediaListType)`: A list of media objects (images or files).
- `messages (Messages)`: A list of message objects containing the conversation history.

**Returns**:
- `list`: A list of tuples, where each tuple contains an image and its filename.

**How the Function Works**:
- It iterates over the media list and extracts images and filenames.
- If the media list is empty, it extracts images from the messages.
- It returns a list of tuples with images and filenames.

### `to_bytes(image)`:

**Purpose**:
Converts an image to bytes.

**Parameters**:
- `image`: An image object.

**Returns**:
- `bytes`: The image converted to bytes.

**How the Function Works**:
- It checks if the image is a `bytes` object. If so, it returns the object.
- If the image is a `PIL.Image.Image` object, it converts it to bytes using the `image.tobytes` method.
- If the image is a path, it reads the image from the path and converts it to bytes.

## Example File

```python
from __future__ import annotations

import json
import re
import os
import requests
import base64
import uuid
from typing import AsyncIterator

try:
    from curl_cffi.requests import Session
    from curl_cffi import CurlMime
    has_curl_cffi = True
except ImportError:
    has_curl_cffi = False

from ..base_provider import ProviderModelMixin, AsyncAuthedProvider, AuthResult
from ..helper import format_prompt, format_image_prompt, get_last_user_message
from ...typing import AsyncResult, Messages, Cookies, MediaListType
from ...errors import MissingRequirementsError, MissingAuthError, ResponseError
from ...image import to_bytes
from ...requests import get_args_from_nodriver, DEFAULT_HEADERS
from ...requests.raise_for_status import raise_for_status
from ...providers.response import JsonConversation, ImageResponse, Sources, TitleGeneration, Reasoning, RequestLogin, FinishReason
from ...cookies import get_cookies
from ...tools.media import merge_media
from .models import default_model, default_vision_model, fallback_models, image_models, model_aliases
from ... import debug

class Conversation(JsonConversation):
    """
    Класс для хранения данных о разговоре с моделью.

    Attributes:
        models (dict): Словарь, содержащий информацию о моделях, используемых в разговоре.
    """
    def __init__(self, models: dict):
        """
        Инициализирует объект Conversation.

        Args:
            models (dict): Словарь, содержащий информацию о моделях.
        """
        self.models: dict = models

class HuggingChat(AsyncAuthedProvider, ProviderModelMixin):
    """
    Класс, реализующий асинхронный провайдер для взаимодействия с Hugging Face Chat API.

    Attributes:
        domain (str): Доменное имя Hugging Face Chat API.
        origin (str): Базовый URL для Hugging Face Chat API.
        url (str): URL для конечной точки API чата.
        working (bool): Указывает, работает ли провайдер в настоящее время.
        use_nodriver (bool): Указывает, использует ли провайдер драйвер headless браузера или нет.
        supports_stream (bool): Указывает, поддерживает ли провайдер потоковую передачу ответов.
        needs_auth (bool): Указывает, требуется ли провайдеру аутентификация.
        default_model (str): Модель по умолчанию для текста.
        default_vision_model (str): Модель по умолчанию для изображений.
        model_aliases (dict): Словарь, сопоставляющий псевдонимы моделей с их соответствующими ID моделей Hugging Face.
        image_models (list): Список моделей изображений, поддерживаемых провайдером.
        text_models (list): Список текстовых моделей, поддерживаемых провайдером.
        vision_models (list): Список моделей видения (моделей, поддерживающих мультимодальный ввод), поддерживаемых провайдером.

    Methods:
        get_models(): Получает список всех доступных моделей Hugging Face.
        on_auth_async(cookies: Cookies = None, proxy: str = None, **kwargs) -> AsyncIterator: Асинхронно обрабатывает аутентификацию. 
        create_authed(model: str, messages: Messages, auth_result: AuthResult, prompt: str = None, media: MediaListType = None, return_conversation: bool = False, conversation: Conversation = None, web_search: bool = False, **kwargs) -> AsyncResult: Создает сеанс чата и отправляет запрос к Hugging Face Chat API.
        create_conversation(session: Session, model: str): Создает новый разговор с указанной моделью.
        fetch_message_id(session: Session, conversation_id: str): Получает ID сообщения для заданного разговора.
    """
    domain = "huggingface.co"
    origin = f"https://{domain}"
    url = f"{origin}/chat"

    working = True
    use_nodriver = True
    supports_stream = True
    needs_auth = True
    default_model = default_model
    default_vision_model = default_vision_model
    model_aliases = model_aliases
    image_models = image_models
    text_models = fallback_models

    @classmethod
    def get_models(cls):
        """
        Получает список всех доступных моделей Hugging Face.

        Returns:
            list: Список моделей Hugging Face.
        """
        if not cls.models:
            try:
                text = requests.get(cls.url).text
                text = re.search(r'models:(\\[.+?\\]),oldModels:', text).group(1)
                text = re.sub(r',parameters:{[^}]+}', '', text)
                text = text.replace('void 0', 'null')
                def add_quotation_mark(match):
                    return f"'{match.group(1)}"{match.group(2)}':"
                text = re.sub(r'([{,])([A-Za-z0-9_]+?):', add_quotation_mark, text)
                models = json.loads(text)
                cls.text_models = [model["id"] for model in models] 
                cls.models = cls.text_models + cls.image_models
                cls.vision_models = [model["id"] for model in models if model["multimodal"]]
            except Exception as e:
                debug.error(f"{cls.__name__}: Error reading models: {type(e).__name__}: {e}")
                cls.models = [*fallback_models]
        return cls.models

    @classmethod
    async def on_auth_async(cls, cookies: Cookies = None, proxy: str = None, **kwargs) -> AsyncIterator:
        """
        Асинхронно обрабатывает аутентификацию.

        Args:
            cookies (Cookies, optional): Словарь с куки. Defaults to None.
            proxy (str, optional): Прокси-сервер для использования в запросе. Defaults to None.
            **kwargs: Дополнительные аргументы, переданные функции `requests.get`.

        Yields:
            AuthResult: Результат аутентификации, содержащий куки и дополнительные параметры.

        Raises:
            MissingAuthError: Если аутентификация не удалась.
        """
        if cookies is None:
            cookies = get_cookies(cls.domain, single_browser=True)
        if "hf-chat" in cookies:
            yield AuthResult(
                cookies=cookies,
                impersonate="chrome",
                headers=DEFAULT_HEADERS
            )
            return
        if cls.needs_auth:
            yield RequestLogin(cls.__name__, os.environ.get("G4F_LOGIN_URL") or "")
            yield AuthResult(
                **await get_args_from_nodriver(
                    cls.url,
                    proxy=proxy,
                    wait_for='form[action$="/logout"]'
                )
            )
        else:
            yield AuthResult(
                cookies = {
                    "hf-chat": str(uuid.uuid4())  # Generate a session ID
                }
            )

    @classmethod
    async def create_authed(
        cls,
        model: str,
        messages: Messages,
        auth_result: AuthResult,
        prompt: str = None,
        media: MediaListType = None,
        return_conversation: bool = False,
        conversation: Conversation = None,
        web_search: bool = False,
        **kwargs
    ) -> AsyncResult:
        """
        Создает сеанс чата и отправляет запрос к Hugging Face Chat API.

        Args:
            model (str): Имя модели.
            messages (Messages): Список объектов сообщений, содержащих историю разговора.
            auth_result (AuthResult): Результат аутентификации, содержащий куки и дополнительные параметры.
            prompt (str, optional): Подсказка для модели. Defaults to None.
            media (MediaListType, optional): Список медиафайлов (изображений или файлов). Defaults to None.
            return_conversation (bool, optional): Указывает, возвращать ли объект Conversation. Defaults to False.
            conversation (Conversation, optional): Объект Conversation, содержащий данные о текущем разговоре. Defaults to None.
            web_search (bool, optional): Указывает, включить ли веб-поиск. Defaults to False.
            **kwargs: Дополнительные аргументы, переданные функции `requests.get`.

        Yields:
            AsyncResult: Асинхронный результат, содержащий ответ от API.

        Raises:
            MissingRequirementsError: Если пакет "curl_cffi" не установлен.
            MissingAuthError: Если аутентификация не удалась.
            ResponseError: Если API вернул ошибку.
        """
        if not has_curl_cffi:
            raise MissingRequirementsError('Install "curl_cffi" package | pip install -U curl_cffi')
        if not model and media is not None:
            model = cls.default_vision_model
        model = cls.get_model(model)

        session = Session(**auth_result.get_dict())

        if conversation is None or not hasattr(conversation, "models"):
            conversation = Conversation({})

        if model not in conversation.models:
            conversationId = cls.create_conversation(session, model)
            debug.log(f"Conversation created: {json.dumps(conversationId[8:] + '...')}")
            messageId = cls.fetch_message_id(session, conversationId)
            conversation.models[model] = {"conversationId": conversationId, "messageId": messageId}
            if return_conversation:
                yield conversation
            inputs = format_prompt(messages)
        else:
            conversationId = conversation.models[model]["conversationId"]
            conversation.models[model]["messageId"] = cls.fetch_message_id(session, conversationId)
            inputs = get_last_user_message(messages)

        settings = {
            "inputs": inputs,
            "id": conversation.models[model]["messageId"],
            "is_retry": False,
            "is_continue": False,
            "web_search": web_search,
            "tools": ["000000000000000000000001"] if model in cls.image_models else [],
        }

        headers = {
            'accept': '*/*',
            'origin': cls.origin,
            'referer': f'{cls.url}/conversation/{conversationId}',
        }
        data = CurlMime()
        data.addpart('data', data=json.dumps(settings, separators=(',', ':')))
        for image, filename in merge_media(media, messages):
            data.addpart(
                "files",
                filename=f"base64;{filename}",
                data=base64.b64encode(to_bytes(image))
            )

        response = session.post(
            f'{cls.url}/conversation/{conversationId}',
            headers=headers,
            multipart=data,
            stream=True
        )
        raise_for_status(response)

        sources = None
        for line in response.iter_lines():
            if not line:
                continue
            try:
                line = json.loads(line)
            except json.JSONDecodeError as e:
                debug.error(f"Failed to decode JSON: {line}, error: {e}")
                continue
            if "type" not in line:
                raise RuntimeError(f"Response: {line}")
            elif line["type"] == "stream":
                yield line["token"].replace('\u0000', '')
            elif line["type"] == "finalAnswer":
                if sources is not None:
                    yield sources
                yield FinishReason("stop")
                break
            elif line["type"] == "file":
                url = f"{cls.url}/conversation/{conversationId}/output/{line['sha']}"
                yield ImageResponse(url, format_image_prompt(messages, prompt), options={"cookies": auth_result.cookies})
            elif line["type"] == "webSearch" and "sources" in line:
                sources = Sources(line["sources"])
            elif line["type"] == "title":
                yield TitleGeneration(line["title"])
            elif line["type"] == "reasoning":
                yield Reasoning(line.get("token"), status=line.get("status"))

    @classmethod
    def create_conversation(cls, session: Session, model: str):
        """
        Создает новый разговор с указанной моделью.

        Args:
            session (Session): Объект сессии `requests`.
            model (str): Имя модели.

        Returns:
            str: ID созданного разговора.

        Raises:
            MissingAuthError: Если аутентификация не удалась.
            ResponseError: Если API вернул ошибку.
        """
        if model in cls.image_models:
            model = cls.default_model
        json_data = {
            'model': model,
        }
        response = session.post(f'{cls.url}/conversation', json=json_data)
        if response.status_code == 401:
            raise MissingAuthError(response.text)
        if response.status_code == 400:
            raise ResponseError(f"{response.text}: Model: {model}")
        raise_for_status(response)
        return response.json().get('conversationId')

    @classmethod
    def fetch_message_id(cls, session: Session, conversation_id: str):
        """
        Получает ID сообщения для заданного разговора.

        Args:
            session (Session): Объект сессии `requests`.
            conversation_id (str): ID разговора.

        Returns:
            str: ID сообщения.

        Raises:
            RuntimeError: Если не удалось извлечь ID сообщения.
            MissingAuthError: Если аутентификация не удалась.
            ResponseError: Если API вернул ошибку.
        """
        # Get the data response and parse it properly
        response = session.get(f'{cls.url}/conversation/{conversation_id}/__data.json?x-sveltekit-invalidated=11')
        raise_for_status(response)

        # Split the response content by newlines and parse each line as JSON
        try:
            json_data = None
            for line in response.text.split('\n'):
                if line.strip():
                    try:
                        parsed = json.loads(line)
                        if isinstance(parsed, dict) and "nodes" in parsed:
                            json_data = parsed
                            break
                    except json.JSONDecodeError:
                        continue

            if not json_data:
                raise RuntimeError("Failed to parse response data")

            if json_data["nodes"][-1]["type"] == "error":
                if json_data["nodes"][-1]["status"] == 403:
                    raise MissingAuthError(json_data["nodes"][-1]["error"]["message"])
                raise ResponseError(json.dumps(json_data["nodes"][-1]))

            data = json_data["nodes"][1]["data"]
            keys = data[data[0]["messages"]]
            message_keys = data[keys[-1]]
            return data[message_keys["id"]]

        except (KeyError, IndexError, TypeError) as e:
            raise RuntimeError(f"Failed to extract message ID: {str(e)}")
```

**Table of Contents (TOC)**

- [HuggingChat Provider](#huggingchat-provider)
    - [Overview](#overview)
    - [Details](#details)
    - [Classes](#classes)
        - [`class HuggingChat(AsyncAuthedProvider, ProviderModelMixin)`](#class-huggingchatasyncauthedproviderprovidermodelmixin)
        - [`class Conversation(JsonConversation)`](#class-conversationjsonconversation)
    - [Functions](#functions)
        - [`add_quotation_mark(match)`](#add_quotation_markmatch)
        - [`format_prompt(messages)`](#format_promptmessages)
        - [`format_image_prompt(messages, prompt)`](#format_image_promptmessages-prompt)
        - [`get_last_user_message(messages)`](#get_last_user_messagess)
        - [`get_args_from_nodriver(url: str, proxy: str = None, wait_for: str = None, **kwargs) -> dict`:](#get_args_from_nodriverurl-str-proxy-str--none-wait_for-str--none--kwargs--dict)
        - [`merge_media(media: MediaListType, messages: Messages) -> list`:](#merge_mediamedia-medialisttype-messages-messages--list)
        - [`to_bytes(image)`:](#to_bytesimage)
    - [Example File](#example-file)