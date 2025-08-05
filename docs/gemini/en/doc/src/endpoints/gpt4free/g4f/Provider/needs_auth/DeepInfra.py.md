# DeepInfra Provider for GPT4Free

## Overview

This module provides the `DeepInfra` class, which implements a provider for the GPT4Free project. It allows users to utilize the DeepInfra API for text generation and image creation.

## Details

The `DeepInfra` class extends the `OpenaiTemplate` class. It leverages the DeepInfra API for text generation and image creation. It requires authentication and provides a range of functionalities, including:

- Retrieving a list of available models (text and image generation).
- Generating text using specified models.
- Generating images using specified models.

## Classes

### `class DeepInfra(OpenaiTemplate)`

**Description**: This class implements the DeepInfra provider for GPT4Free. It inherits from `OpenaiTemplate` and provides functionalities for interacting with the DeepInfra API for text generation and image creation.

**Attributes**:

- `url`: The base URL for DeepInfra.
- `login_url`: The login URL for DeepInfra's dashboard.
- `api_base`: The base URL for DeepInfra's API.
- `working`: Indicates whether the provider is currently working.
- `needs_auth`:  Indicates whether the provider requires authentication.
- `default_model`: The default model used for text generation.
- `default_image_model`: The default model used for image generation.

**Methods**:

- `get_models(**kwargs)`: Retrieves a list of available models from the DeepInfra API.
- `get_image_models(**kwargs)`: Retrieves a list of available image generation models from the DeepInfra API.
- `create_async_generator(model: str, messages: Messages, stream: bool, prompt: str = None, temperature: float = 0.7, max_tokens: int = 1028, **kwargs) -> AsyncResult`: Creates an asynchronous generator for text generation.
- `create_async_image(prompt: str, model: str, api_key: str = None, api_base: str = "https://api.deepinfra.com/v1/inference", proxy: str = None, timeout: int = 180, extra_data: dict = {}, **kwargs) -> ImageResponse`: Creates an asynchronous generator for image generation.

## Functions

### `format_image_prompt(messages: Messages, prompt: str = None) -> str`

**Purpose**: Formats the prompt for image generation.

**Parameters**:

- `messages` (Messages): A list of messages containing context for the prompt.
- `prompt` (str, optional): The user-provided prompt. Defaults to `None`.

**Returns**:

- `str`: The formatted prompt for image generation.

**How the Function Works**:

This function combines the context from the `messages` list and the user-provided `prompt` to create a formatted prompt for image generation.

**Examples**:

```python
>>> messages = [{"role": "user", "content": "Create a picture of a cat."}]
>>> format_image_prompt(messages, prompt=None)
'Create a picture of a cat.'

>>> messages = [{"role": "user", "content": "What does a cat look like?"}, {"role": "assistant", "content": "A cat is a furry, four-legged animal with pointy ears and a tail."}]
>>> format_image_prompt(messages, prompt="A cat sitting on a couch.")
'A cat is a furry, four-legged animal with pointy ears and a tail. A cat sitting on a couch.'
```

## Parameter Details

- `messages` (Messages): A list of messages containing context for the prompt.
- `prompt` (str, optional): The user-provided prompt. Defaults to `None`.
- `model` (str): The model to use for text or image generation.
- `api_key` (str, optional): The API key for authentication with DeepInfra. Defaults to `None`.
- `api_base` (str, optional): The base URL for the DeepInfra API. Defaults to `https://api.deepinfra.com/v1/inference`.
- `proxy` (str, optional): The proxy to use for making requests. Defaults to `None`.
- `timeout` (int, optional): The timeout for requests in seconds. Defaults to `180`.
- `extra_data` (dict, optional): Additional data to be included in the request payload. Defaults to `{}`.

## Examples

### Using `DeepInfra` for Text Generation

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.DeepInfra import DeepInfra
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.DeepInfra import Messages

# Create a DeepInfra provider instance
provider = DeepInfra()

# Define the messages for the prompt
messages = Messages([{"role": "user", "content": "Write a short story about a cat."}])

# Generate text using the DeepInfra provider
async for response in provider.create_async_generator(model="meta-llama/Meta-Llama-3.1-70B-Instruct", messages=messages, stream=True):
    print(response)
```

### Using `DeepInfra` for Image Generation

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.DeepInfra import DeepInfra

# Create a DeepInfra provider instance
provider = DeepInfra()

# Generate an image using the DeepInfra provider
async for response in provider.create_async_image(prompt="A cat sitting on a couch.", model="stabilityai/sd3.5"):
    print(response)
```