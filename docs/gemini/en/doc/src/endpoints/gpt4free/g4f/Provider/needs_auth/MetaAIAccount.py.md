# MetaAIAccount Provider

## Overview

This module defines the `MetaAIAccount` class, which provides functionality for interacting with Meta AI's conversational AI models. It is a subclass of the `MetaAI` class and inherits its methods for processing prompts and responses.

## Details

The `MetaAIAccount` class is specifically designed to handle requests that require authentication with a Meta AI account. It inherits the necessary authentication logic from the `MetaAI` class and extends it with specific functionalities related to the Meta AI account. This class is designed to be used in conjunction with the `g4f` module's provider system.

## Classes

### `MetaAIAccount`

**Description**: This class represents a Meta AI account provider. It inherits from the `MetaAI` class and adds specific features for handling authentication with Meta AI accounts. 

**Inherits**: `MetaAI`

**Attributes**:
 - `needs_auth`: (bool)  Indicates whether the provider requires authentication. It is set to `True` for this class.
 - `parent`: (str) Specifies the parent provider class. It is set to `"MetaAI"`.
 - `image_models`: (list) Defines a list of image models that the provider supports. It is set to `["meta"]` for this class.

**Methods**:

 - `create_async_generator()`: This method is responsible for creating an asynchronous generator for handling interactions with the Meta AI model. It handles authentication and prompt formatting.

## Class Methods

### `create_async_generator()`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        cookies: Cookies = None,
        **kwargs
    ) -> AsyncResult:
        cookies = get_cookies(".meta.ai", True, True) if cookies is None else cookies
        async for chunk in cls(proxy).prompt(format_prompt(messages), cookies):
            yield chunk
```

**Purpose**: This method creates an asynchronous generator that handles interactions with the Meta AI model. It retrieves cookies for authentication, formats the prompt, and iterates through chunks of the response.

**Parameters**:
 - `model`: (str) Specifies the name of the Meta AI model to be used.
 - `messages`: (Messages)  A list of messages to be sent to the AI model.
 - `proxy`: (str) The proxy server to be used for the request.
 - `cookies`: (Cookies)  A dictionary of cookies to be used for authentication.
 - `**kwargs`: (dict)  Additional keyword arguments to be passed to the request.

**Returns**:
 - `AsyncResult`: An asynchronous generator that yields chunks of the response from the Meta AI model.

**How the Function Works**:

1. The method retrieves cookies for authentication with Meta AI, either from the provided `cookies` parameter or by fetching them from the `.meta.ai` domain.
2. It formats the prompt using the `format_prompt` helper function.
3. It calls the `prompt` method inherited from the `MetaAI` class, passing the formatted prompt and cookies. This initiates a conversation with the AI model.
4. The `prompt` method returns an asynchronous generator that yields chunks of the response.
5. The `create_async_generator` method yields each chunk of the response from the `prompt` method's generator.

**Examples**:
```python
from ...typing import Messages
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.MetaAIAccount import MetaAIAccount

messages: Messages = [
    {"role": "user", "content": "Hello, what's the weather like today?"}
]

async def main():
    async for chunk in await MetaAIAccount.create_async_generator(model='meta', messages=messages):
        print(chunk)
```