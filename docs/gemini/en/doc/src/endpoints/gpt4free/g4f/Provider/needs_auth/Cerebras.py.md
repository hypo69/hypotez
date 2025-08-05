# Cerebras API Provider

## Overview

This module provides a class, `Cerebras`, for interacting with the Cerebras Inference API. It is a subclass of the `OpenaiAPI` class, implementing a specific interface for interacting with Cerebras' AI models, including the Llama family of models.

## Details

The `Cerebras` class inherits from `OpenaiAPI`, providing a consistent API for working with different AI models, including Cerebras Inference. This allows the user to interact with Cerebras' models in a familiar way using methods inherited from the `OpenaiAPI` class.

## Classes

### `Cerebras`

**Description**: This class provides an interface for interacting with the Cerebras Inference API.

**Inherits**: `OpenaiAPI`

**Attributes**:
- `label`: Label for the Cerebras Inference provider (e.g., "Cerebras Inference").
- `url`: Base URL for the Cerebras Inference API.
- `login_url`: URL for Cerebras' user login page.
- `api_base`: Base URL for the Cerebras API.
- `working`: Flag indicating whether the provider is functional.
- `default_model`: Default model to use with the Cerebras Inference API (e.g., "llama3.1-70b").
- `models`: List of available models for the Cerebras Inference API (e.g., "llama3.1-70b", "llama3.1-8b", "llama-3.3-70b", "deepseek-r1-distill-llama-70b").
- `model_aliases`: Dictionary of model aliases for easier model selection (e.g., "llama-3.1-70b": "llama3.1-70b", "deepseek-r1": "deepseek-r1-distill-llama-70b").

**Methods**:
- `create_async_generator()`: Asynchronously generates chunks of text from the Cerebras Inference API, providing access to the response content.


## Class Methods

### `create_async_generator()`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        api_key: str = None,
        cookies: Cookies = None,
        **kwargs
    ) -> AsyncResult:
        if api_key is None:
            if cookies is None:
                cookies = get_cookies(".cerebras.ai")
            async with ClientSession(cookies=cookies) as session:
                async with session.get("https://inference.cerebras.ai/api/auth/session") as response:
                    await raise_for_status(response)
                    data = await response.json()
                    if data:
                        api_key = data.get("user", {}).get("demoApiKey")
        async for chunk in super().create_async_generator(
            model, messages,
            impersonate="chrome",
            api_key=api_key,
            headers={
                "User-Agent": "ex/JS 1.5.0",
            },
            **kwargs
        ):
            yield chunk
```

**Purpose**: This method generates chunks of text from the Cerebras Inference API asynchronously, providing a streaming interface for the response content.

**Parameters**:

- `model`: (str) The name of the Cerebras model to use for the inference request (e.g., "llama3.1-70b").
- `messages`: (Messages) A list of messages representing the conversation history to be used for the inference request.
- `api_key`: (str, optional) The API key to use for authentication with the Cerebras Inference API. If not provided, the method attempts to retrieve the API key from cookies.
- `cookies`: (Cookies, optional) A dictionary of cookies for authentication with the Cerebras Inference API. If not provided, the method attempts to load cookies from a local file.
- `**kwargs`: (dict) Additional keyword arguments to be passed to the `create_async_generator()` method of the parent class (`OpenaiAPI`).

**Returns**:

- `AsyncResult`: An asynchronous generator that yields chunks of text from the Cerebras Inference API response.

**Raises Exceptions**:

- `Exception`:  If an error occurs during the API request, authentication process, or when parsing the response data.

**How the Function Works**:

1. **Authentication**: The method attempts to obtain an API key for authentication. It checks if the `api_key` parameter is provided. If not, it attempts to load cookies from a local file (`.cerebras.ai`) and use them to retrieve a demo API key from Cerebras' API.
2. **Request Processing**:  The method calls the `create_async_generator()` method of the parent class (`OpenaiAPI`) to make an asynchronous request to the Cerebras Inference API, passing the model name, messages, and other necessary parameters.
3. **Streaming Response**:  The method iterates over the asynchronous response chunks and yields them to the caller, providing a streaming interface for the response content.

**Examples**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.Cerebras import Cerebras
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Example 1: Using a provided API key
api_key = "your_cerebras_api_key"
model = "llama3.1-70b"
messages = [
    {"role": "user", "content": "Hello, how are you?"},
]

async def example1():
    async for chunk in Cerebras.create_async_generator(model=model, messages=messages, api_key=api_key):
        print(chunk)

# Example 2: Using cookies for authentication
async def example2():
    async for chunk in Cerebras.create_async_generator(model=model, messages=messages):
        print(chunk)
```