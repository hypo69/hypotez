# AiChatOnline Provider for GPT4Free

## Overview

This module provides the `AiChatOnline` class, a provider for the `GPT4Free` service. It allows users to interact with the AiChatOnline platform for generating text using AI models. This provider currently utilizes the GPT-4O-mini model.

## Details

The `AiChatOnline` provider extends the `AsyncGeneratorProvider` and `ProviderModelMixin` classes, inheriting their functionalities for asynchronous generation and model management.

## Classes

### `class AiChatOnline(AsyncGeneratorProvider, ProviderModelMixin)`

**Description**: This class represents the AiChatOnline provider for GPT4Free. It allows users to interact with the AiChatOnline platform for text generation using AI models.

**Inherits**:
- `AsyncGeneratorProvider`: Provides functionality for asynchronous text generation.
- `ProviderModelMixin`: Provides functionality for model management.

**Attributes**:
- `site_url (str)`: Base URL of the AiChatOnline website.
- `url (str)`: URL for API interactions.
- `api_endpoint (str)`: Endpoint for the chat API.
- `working (bool)`: Flag indicating whether the provider is currently functional (set to `False` in the provided code).
- `default_model (str)`: Default model used by the provider (`gpt-4o-mini`).

**Methods**:

#### `grab_token(session: ClientSession, proxy: str)`

**Purpose**: This method retrieves a unique identifier (token) from the AiChatOnline platform using a provided `ClientSession` and optional proxy.

**Parameters**:
- `session (ClientSession)`: A `ClientSession` object used for network requests.
- `proxy (str)`: Optional proxy server address.

**Returns**:
- `str`: The retrieved unique identifier (token).

**Raises Exceptions**:
- `aiohttp.ClientResponseError`: If there's an error during the API request.

**How the Function Works**:
- Makes a GET request to the AiChatOnline API to retrieve a unique identifier.
- Extracts the identifier from the response data.

**Examples**:
```python
# Example using a ClientSession and a proxy
async def example_grab_token():
    async with ClientSession() as session:
        token = await AiChatOnline.grab_token(session, proxy='http://proxy.example.com:8080')
        print(f"Retrieved token: {token}")
```

#### `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs)`

**Purpose**: This method creates an asynchronous generator for text generation using the specified AI model, messages, and optional proxy.

**Parameters**:
- `model (str)`: The name of the AI model to use (e.g., 'gpt-4o-mini').
- `messages (Messages)`: A list of messages to be used for the conversation.
- `proxy (str, optional)`: Optional proxy server address. Defaults to `None`.
- `**kwargs`: Additional keyword arguments.

**Returns**:
- `AsyncResult`: An asynchronous generator that yields the generated text responses.

**Raises Exceptions**:
- `aiohttp.ClientResponseError`: If there's an error during the API request.

**How the Function Works**:
- Creates a `ClientSession` with specific headers.
- Builds a JSON payload containing the conversation ID and formatted prompt.
- Retrieves a unique identifier (token) using the `grab_token` method.
- Makes a POST request to the AiChatOnline API with the payload and headers.
- Processes the response in chunks, yielding the generated text responses from the JSON data.

**Examples**:
```python
# Example using a model, messages, and a proxy
async def example_create_async_generator():
    messages = [
        {"role": "user", "content": "Hello, how are you?"},
    ]
    async for response in AiChatOnline.create_async_generator(model='gpt-4o-mini', messages=messages, proxy='http://proxy.example.com:8080'):
        print(f"Response: {response}")
```

## Parameter Details

- `model (str)`: The name of the AI model to use for text generation (e.g., 'gpt-4o-mini').
- `messages (Messages)`: A list of messages to be used for the conversation, containing the user's input and previous responses from the AI.
- `proxy (str, optional)`: A proxy server address to be used for network requests.

## Examples

```python
from __future__ import annotations

import json
from aiohttp import ClientSession

from ...typing import AsyncResult, Messages
from ..base_provider import AsyncGeneratorProvider, ProviderModelMixin
from ..helper import get_random_string, format_prompt

class AiChatOnline(AsyncGeneratorProvider, ProviderModelMixin):
    site_url = "https://aichatonline.org"
    url = "https://aichatonlineorg.erweima.ai"
    api_endpoint = "/aichatonline/api/chat/gpt"
    working = False
    default_model = 'gpt-4o-mini'

    @classmethod
    async def grab_token(
        cls,
        session: ClientSession,
        proxy: str
    ):
        async with session.get(f'https://aichatonlineorg.erweima.ai/api/v1/user/getUniqueId?canvas=-{get_random_string()}', proxy=proxy) as response:
            response.raise_for_status()
            return (await response.json())['data']
        
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        **kwargs
    ) -> AsyncResult:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
            "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": f"{cls.url}/chatgpt/chat/",
            "Content-Type": "application/json",
            "Origin": cls.url,
            "Alt-Used": "aichatonline.org",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "TE": "trailers"
        }
        async with ClientSession(headers=headers) as session:
            data = {
                "conversationId": get_random_string(),
                "prompt": format_prompt(messages),
            }
            headers['UniqueId'] = await cls.grab_token(session, proxy)
            async with session.post(f"{cls.url}{cls.api_endpoint}", headers=headers, json=data, proxy=proxy) as response:
                response.raise_for_status()
                async for chunk in response.content:
                    try:
                        yield json.loads(chunk)['data']['message']
                    except:
                        continue