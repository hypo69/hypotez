# WhiteRabbitNeo Provider

## Overview

This module defines the `WhiteRabbitNeo` class, a provider for the WhiteRabbitNeo API, which is used for interacting with the WhiteRabbitNeo AI chatbot. 

## Details

The `WhiteRabbitNeo` class inherits from the `AsyncGeneratorProvider` class, which provides a framework for asynchronous interactions with AI chatbots. It enables the communication with the WhiteRabbitNeo API, allowing you to send messages and receive responses from the chatbot.

## Classes

### `class WhiteRabbitNeo(AsyncGeneratorProvider)`

**Description**: This class represents a provider for the WhiteRabbitNeo API. It provides the necessary methods to communicate with the WhiteRabbitNeo chatbot, including sending messages and receiving responses.

**Inherits**: `AsyncGeneratorProvider`

**Attributes**:

- `url (str)`: The base URL of the WhiteRabbitNeo API.

- `working (bool)`: A flag indicating whether the provider is currently operational.

- `supports_message_history (bool)`: A flag indicating whether the provider supports message history.

- `needs_auth (bool)`: A flag indicating whether the provider requires authentication.

**Methods**:

- `create_async_generator(model: str, messages: Messages, cookies: Cookies = None, connector: BaseConnector = None, proxy: str = None, **kwargs) -> AsyncResult`: This method creates an asynchronous generator that allows you to send messages and receive responses from the WhiteRabbitNeo chatbot. 

**Parameters**:

- `model (str)`: The model identifier used for the interaction.

- `messages (Messages)`: A list of messages to be sent to the chatbot.

- `cookies (Cookies, optional)`: A dictionary containing the necessary cookies for authentication. Defaults to None.

- `connector (BaseConnector, optional)`: A connector for the HTTP session. Defaults to None.

- `proxy (str, optional)`: A proxy server address. Defaults to None.

**Returns**:

- `AsyncResult`: An asynchronous result object containing the chatbot's responses.

**Raises Exceptions**:

- `ConnectionError`: Raised if an error occurs during establishing a connection to the WhiteRabbitNeo API.

- `HTTPError`: Raised if the server returns an HTTP error code.

- `InvalidCredentials`: Raised if the provided credentials are invalid.

- `Other exceptions`: Raised if an error occurs during the interaction with the API.

**How the Method Works**:

1. The method creates an asynchronous HTTP session with the specified cookies and connector.

2. It constructs a request body containing the messages and other necessary parameters.

3. It sends a POST request to the WhiteRabbitNeo API endpoint `/api/chat`.

4. It iterates through the responses from the API and yields each chunk of data, decoding it with error handling.

**Examples**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.WhiteRabbitNeo import WhiteRabbitNeo
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.WhiteRabbitNeo import Messages

async def main():
    messages: Messages = [
        {'role': 'user', 'content': 'Hello, how are you?'},
        {'role': 'assistant', 'content': 'I am doing well, thank you for asking.'}
    ]
    
    provider = WhiteRabbitNeo(model='gpt-3.5-turbo')
    async for chunk in provider.create_async_generator(messages=messages):
        print(chunk)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```

## Parameter Details

- `model (str)`: The model identifier for the interaction. 
- `messages (Messages)`: A list of messages to be sent to the chatbot. Each message is represented as a dictionary with `role` (user or assistant) and `content` fields.
- `cookies (Cookies, optional)`: A dictionary containing the necessary cookies for authentication. Defaults to None.
- `connector (BaseConnector, optional)`: A connector for the HTTP session. Defaults to None.
- `proxy (str, optional)`: A proxy server address. Defaults to None.
- `**kwargs`:  Additional keyword arguments that may be specific to the provider.

## Examples

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.WhiteRabbitNeo import WhiteRabbitNeo
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.WhiteRabbitNeo import Messages

async def main():
    messages: Messages = [
        {'role': 'user', 'content': 'Hello, how are you?'},
        {'role': 'assistant', 'content': 'I am doing well, thank you for asking.'}
    ]
    
    provider = WhiteRabbitNeo(model='gpt-3.5-turbo')
    async for chunk in provider.create_async_generator(messages=messages):
        print(chunk)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.WhiteRabbitNeo import WhiteRabbitNeo
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.WhiteRabbitNeo import Messages

async def main():
    messages: Messages = [
        {'role': 'user', 'content': 'What is the meaning of life?'},
        {'role': 'assistant', 'content': 'The meaning of life is a question that has been pondered by philosophers and theologians for centuries. There is no one definitive answer, and the meaning of life is often a personal and individual quest. Some people find meaning in their relationships, their work, or their faith. Others find meaning in helping others, pursuing their passions, or simply experiencing the world around them.'}
    ]
    
    provider = WhiteRabbitNeo(model='gpt-3.5-turbo')
    async for chunk in provider.create_async_generator(messages=messages):
        print(chunk)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.WhiteRabbitNeo import WhiteRabbitNeo
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.WhiteRabbitNeo import Messages

async def main():
    messages: Messages = [
        {'role': 'user', 'content': 'Write a short story about a cat.'},
        {'role': 'assistant', 'content': 'Whiskers, a sleek black cat with emerald green eyes, lived a life of quiet contemplation. His days were spent sunning himself on the windowsill, meticulously grooming his fur, and occasionally indulging in a playful swat at a stray feather. He was content with his routine, the familiar rhythm of his life, until one day, a curious object caught his eye. A small, brightly colored ball, unlike anything he had seen before, lay abandoned on the porch. Curiosity overcame him, and he cautiously approached the ball. With a playful swat, he sent it rolling across the porch, and a sudden surge of excitement coursed through him. He chased after the ball, his tail swishing with delight, and for the first time in his life, he felt a spark of something new, something thrilling. The ball, he discovered, was not just an object; it was a companion, a source of endless amusement. His life, once predictable, was now filled with unexpected bursts of joy. He spent hours batting the ball, pouncing on it, and chasing it around the house. He was no longer just Whiskers the cat; he was Whiskers the adventurer, exploring the world with newfound enthusiasm. And as the sun began to set, casting long shadows across the porch, Whiskers, with the ball nestled comfortably in his paws, realized that life, even for a cat, was full of unexpected wonders.'}
    ]
    
    provider = WhiteRabbitNeo(model='gpt-3.5-turbo')
    async for chunk in provider.create_async_generator(messages=messages):
        print(chunk)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```

##  Code Example
```python
from __future__ import annotations

from aiohttp import ClientSession, BaseConnector

from ...typing import AsyncResult, Messages, Cookies
from ...requests.raise_for_status import raise_for_status
from ..base_provider import AsyncGeneratorProvider
from ..helper import get_cookies, get_connector, get_random_string

class WhiteRabbitNeo(AsyncGeneratorProvider):
    url = "https://www.whiterabbitneo.com"
    working = True
    supports_message_history = True
    needs_auth = True

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        cookies: Cookies = None,
        connector: BaseConnector = None,
        proxy: str = None,
        **kwargs
    ) -> AsyncResult:
        if cookies is None:
            cookies = get_cookies("www.whiterabbitneo.com")
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
            "Accept": "*/*",
            "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": f"{cls.url}/",
            "Content-Type": "text/plain;charset=UTF-8",
            "Origin": cls.url,
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "TE": "trailers"
        }
        async with ClientSession(
            headers=headers,
            cookies=cookies,
            connector=get_connector(connector, proxy)
        ) as session:
            data = {
                "messages": messages,
                "id": get_random_string(6),
                "enhancePrompt": False,
                "useFunctions": False
            }
            async with session.post(f"{cls.url}/api/chat", json=data, proxy=proxy) as response:
                await raise_for_status(response)
                async for chunk in response.content.iter_any():
                    if chunk:
                        yield chunk.decode(errors="ignore")