# ChatGptt Provider Module

## Overview

This module implements the `ChatGptt` class, providing a provider for interacting with the ChatGptt.me API. It inherits from `AsyncGeneratorProvider` and `ProviderModelMixin` to facilitate asynchronous message generation and model selection.

## Details

The ChatGptt provider is designed to use the ChatGptt.me API, offering access to various GPT models, including `gpt-4`, `gpt-4o`, and `gpt-4o-mini`. The provider supports streaming, system messages, and message history for more interactive and contextually aware interactions.

## Classes

### `class ChatGptt`

**Description**:  This class represents the ChatGptt provider, enabling interaction with the ChatGptt.me API for generating text using GPT models. 

**Inherits**:
    - `AsyncGeneratorProvider`: Implements asynchronous message generation using a generator.
    - `ProviderModelMixin`: Provides functionality for model selection and management.

**Attributes**:
    - `url` (str): The base URL of the ChatGptt.me website.
    - `api_endpoint` (str): The URL of the API endpoint for sending requests.
    - `working` (bool): Indicates whether the provider is currently functional.
    - `supports_stream` (bool): Indicates whether the provider supports streaming responses.
    - `supports_system_message` (bool): Indicates whether the provider supports system messages.
    - `supports_message_history` (bool): Indicates whether the provider supports message history.
    - `default_model` (str): The default model to use for text generation.
    - `models` (list): A list of available GPT models supported by the provider.

**Methods**:

#### `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`

**Purpose**: This method creates an asynchronous generator for interacting with the ChatGptt.me API, allowing streaming responses.

**Parameters**:
    - `model` (str): The desired GPT model to use for text generation.
    - `messages` (Messages): A list of messages to be sent to the API.
    - `proxy` (str, optional): A proxy server URL to use for requests. Defaults to `None`.

**Returns**:
    - `AsyncResult`: An asynchronous result object representing the generator.

**Raises**:
    - `RuntimeError`: If the required authentication tokens are not found in the page HTML.

**How the Method Works**:

1. **Initialization**: The method initializes the necessary headers and session for making API requests.
2. **Initial Page Retrieval**: Retrieves the initial page content from the ChatGptt.me website.
3. **Authentication Token Extraction**: Extracts the necessary authentication tokens (nonce and post ID) from the page HTML.
4. **Payload Preparation**: Prepares the payload with the session data, including messages, authentication tokens, and other relevant information.
5. **API Request and Response**: Sends the prepared payload to the ChatGptt.me API endpoint and handles the response.
6. **Streaming Response**: The method streams the response from the API, yielding the generated text as it becomes available.

**Examples**:

```python
async def generate_text(model: str, messages: Messages) -> str:
    """
    Generates text using the ChatGptt provider.

    Args:
        model (str): The GPT model to use.
        messages (Messages): The messages to send to the API.

    Returns:
        str: The generated text.
    """
    async for chunk in ChatGptt.create_async_generator(model, messages):
        return chunk 

# Example usage:
messages = [
    {"role": "user", "content": "Hello, how are you?"},
]
text = await generate_text(model='gpt-4', messages=messages)
print(text)
```

## Parameter Details

- `model` (str): The desired GPT model for text generation, e.g., 'gpt-4', 'gpt-4o', 'gpt-4o-mini'.
- `messages` (Messages): A list of messages to send to the API. Each message is a dictionary with keys like 'role' and 'content'.
- `proxy` (str, optional): An optional proxy server URL to use for requests.

## Examples

```python
# Example usage:
messages = [
    {"role": "user", "content": "What is the meaning of life?"},
]
async for response in ChatGptt.create_async_generator(model='gpt-4', messages=messages):
    print(response)

# Using a different model:
messages = [
    {"role": "user", "content": "Write a poem about a cat."},
]
async for response in ChatGptt.create_async_generator(model='gpt-4o-mini', messages=messages):
    print(response)

# Using a proxy:
messages = [
    {"role": "user", "content": "Translate 'Hello, world!' to Spanish."},
]
async for response in ChatGptt.create_async_generator(model='gpt-4', messages=messages, proxy='http://proxy_server:port'):
    print(response)
```