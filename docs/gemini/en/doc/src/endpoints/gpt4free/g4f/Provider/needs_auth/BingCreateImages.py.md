# BingCreateImages Provider

## Overview

This module provides the `BingCreateImages` class, an asynchronous generator provider for generating images using Microsoft Designer in Bing. This provider requires authentication and leverages Bing's image creation API to create images based on prompts.

## Details

The `BingCreateImages` class extends `AsyncGeneratorProvider` and `ProviderModelMixin`, inheriting functionality for asynchronous generation and model management. It allows users to generate images using Bing's image creation API based on provided prompts. The provider requires authentication using a cookie `_U` containing an API key.

## Classes

### `BingCreateImages`

**Description**: An asynchronous generator provider for generating images using Microsoft Designer in Bing.

**Inherits**: `AsyncGeneratorProvider` and `ProviderModelMixin`

**Attributes**:

- `label` (str): The name of the provider, "Microsoft Designer in Bing."
- `url` (str): The URL of the Bing image creation service, "https://www.bing.com/images/create."
- `working` (bool): Indicates if the provider is currently working.
- `needs_auth` (bool): Indicates if authentication is required, set to `True`.
- `image_models` (list): A list of image model names supported by the provider.
- `models` (list): A list of models supported by the provider, identical to `image_models`.

**Methods**:

- `__init__(self, cookies: Cookies = None, proxy: str = None, api_key: str = None) -> None`: Initializes a new instance of the `BingCreateImages` class.
    - **Parameters**:
        - `cookies` (Cookies, optional): A dictionary of cookies for authentication. Defaults to `None`.
        - `proxy` (str, optional): A proxy server to use. Defaults to `None`.
        - `api_key` (str, optional): The API key for authentication. Defaults to `None`.
    - **Raises**:
        - `MissingAuthError`: If the `api_key` is provided but `cookies` are missing, or if cookies are missing the `"_U"` cookie.
- `generate(self, prompt: str) -> ImageResponse`: Asynchronously creates a markdown formatted string with images based on the prompt.
    - **Parameters**:
        - `prompt` (str): The prompt to generate images from.
    - **Returns**:
        - `ImageResponse`: An object containing generated images, prompt, and additional metadata.
    - **Raises**:
        - `MissingAuthError`: If cookies are missing or the `"_U"` cookie is not present.
- `create_async_generator(cls, model: str, messages: Messages, prompt: str = None, api_key: str = None, cookies: Cookies = None, proxy: str = None, **kwargs) -> AsyncResult`: Creates an asynchronous generator for image generation.
    - **Parameters**:
        - `model` (str): The name of the image model to use.
        - `messages` (Messages): A list of messages containing the prompt.
        - `prompt` (str, optional): The prompt to generate images from. Defaults to `None`.
        - `api_key` (str, optional): The API key for authentication. Defaults to `None`.
        - `cookies` (Cookies, optional): A dictionary of cookies for authentication. Defaults to `None`.
        - `proxy` (str, optional): A proxy server to use. Defaults to `None`.
        - `**kwargs`: Additional keyword arguments.
    - **Returns**:
        - `AsyncResult`: An asynchronous generator that yields the generated images.

## Functions

### `create_async_generator`

**Purpose**: Creates an asynchronous generator for image generation.

**Parameters**:

- `model` (str): The name of the image model to use.
- `messages` (Messages): A list of messages containing the prompt.
- `prompt` (str, optional): The prompt to generate images from. Defaults to `None`.
- `api_key` (str, optional): The API key for authentication. Defaults to `None`.
- `cookies` (Cookies, optional): A dictionary of cookies for authentication. Defaults to `None`.
- `proxy` (str, optional): A proxy server to use. Defaults to `None`.
- `**kwargs`: Additional keyword arguments.

**Returns**:

- `AsyncResult`: An asynchronous generator that yields the generated images.

**How the Function Works**:

- Initializes a `BingCreateImages` instance with provided cookies, proxy, and api_key.
- Yields the result of the `generate()` method using the formatted prompt from `messages` and `prompt`.

**Examples**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.BingCreateImages import BingCreateImages
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Example with API key and cookies
async def generate_images():
    messages = Messages([{"role": "user", "content": "A photo of a cat wearing a hat"}])
    async for image in BingCreateImages.create_async_generator(model="dall-e-3", messages=messages, api_key="your_api_key", cookies={"your_cookie_name": "your_cookie_value"}):
        print(image)

# Example without API key
async def generate_images():
    messages = Messages([{"role": "user", "content": "A photo of a cat wearing a hat"}])
    async for image in BingCreateImages.create_async_generator(model="dall-e-3", messages=messages):
        print(image)
```

## Inner Functions

### `generate`

**Purpose**: Asynchronously creates a markdown formatted string with images based on the prompt.

**Parameters**:

- `prompt` (str): The prompt to generate images from.

**Returns**:

- `ImageResponse`: An object containing generated images, prompt, and additional metadata.

**How the Function Works**:

- Retrieves cookies from storage or uses provided cookies.
- If no cookies or the `"_U"` cookie is missing, raises a `MissingAuthError`.
- Creates a session using `create_session` with retrieved cookies and proxy.
- Generates images using `create_images` with the session and prompt.
- Returns an `ImageResponse` object containing the generated images, prompt, and preview URLs if multiple images are generated.

## Parameter Details

- `cookies` (Cookies, optional): A dictionary of cookies for authentication. Defaults to `None`.
- `proxy` (str, optional): A proxy server to use. Defaults to `None`.
- `api_key` (str, optional): The API key for authentication. Defaults to `None`.
- `model` (str): The name of the image model to use.
- `messages` (Messages): A list of messages containing the prompt.
- `prompt` (str, optional): The prompt to generate images from. Defaults to `None`.

## Examples

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.BingCreateImages import BingCreateImages
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Example with API key and cookies
async def generate_images():
    messages = Messages([{"role": "user", "content": "A photo of a cat wearing a hat"}])
    async for image in BingCreateImages.create_async_generator(model="dall-e-3", messages=messages, api_key="your_api_key", cookies={"your_cookie_name": "your_cookie_value"}):
        print(image)

# Example without API key
async def generate_images():
    messages = Messages([{"role": "user", "content": "A photo of a cat wearing a hat"}])
    async for image in BingCreateImages.create_async_generator(model="dall-e-3", messages=messages):
        print(image)
```