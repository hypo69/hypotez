# OpenAssistant.py

## Overview

This module defines the `OpenAssistant` class, which implements the `AsyncGeneratorProvider` interface for generating text responses from the Open Assistant model using the `aiohttp` library.

## Details

This module provides a class `OpenAssistant` that serves as a wrapper for the Open Assistant API. It allows for asynchronous text generation using the `aiohttp` library, enabling efficient handling of requests and responses. The module supports the use of proxy servers and custom cookies for enhanced flexibility.

## Classes

### `class OpenAssistant(AsyncGeneratorProvider)`

**Description**: Implements the `AsyncGeneratorProvider` interface for the Open Assistant model.

**Inherits**: `AsyncGeneratorProvider`

**Attributes**:
- `url` (str): The base URL for the Open Assistant API.
- `needs_auth` (bool): Indicates whether authentication is required for accessing the API.
- `working` (bool): A flag to track whether the provider is currently active.
- `model` (str): The default model used for text generation.

**Methods**:
- `create_async_generator()`: Creates an asynchronous generator for generating text responses from the Open Assistant API.


## Functions

### `create_async_generator(model: str, messages: Messages, proxy: str = None, cookies: dict = None, **kwargs) -> AsyncResult`

**Purpose**: Creates an asynchronous generator for generating text responses from the Open Assistant API.

**Parameters**:
- `model` (str): The Open Assistant model to use for text generation (e.g., "OA_SFT_Llama_30B_6").
- `messages` (Messages): A list of messages in the conversation.
- `proxy` (str, optional): A proxy server address to use for requests. Defaults to `None`.
- `cookies` (dict, optional): A dictionary of cookies for authentication. Defaults to `None`.
- `kwargs`: Additional keyword arguments passed to the `sampling_parameters` dictionary.

**Returns**:
- `AsyncResult`: An asynchronous result object that yields text tokens from the generated response.

**Raises Exceptions**:
- `RuntimeError`: If an error occurs during the API request or response processing.

**How the Function Works**:
1. The function first checks if cookies are provided; if not, it retrieves them from the "open-assistant.io" website.
2. It then creates an `aiohttp` client session with the provided cookies and headers.
3. The function initiates a POST request to the Open Assistant API to start a new chat.
4. It sends a prompt message to the chat using a POST request to the `/prompter_message` endpoint.
5. It sends a message to the assistant model using a POST request to the `/assistant_message` endpoint, specifying the model, sampling parameters, and any plugins.
6. The function then initiates a POST request to the `/events` endpoint to stream the generated text tokens.
7. The generator yields each text token as it is received.
8. Finally, the function deletes the chat using a DELETE request to the `/chat` endpoint.


**Examples**:
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated import OpenAssistant
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

messages = Messages(
    [
        {"role": "user", "content": "Hello, how are you?"},
    ]
)

async def main():
    async for token in OpenAssistant.create_async_generator(model='OA_SFT_Llama_30B_6', messages=messages):
        print(token)
```

## Parameter Details

- `model` (str): The Open Assistant model name to use for text generation.
- `messages` (Messages): A list of messages in the conversation, each message containing a role (`user` or `assistant`) and content.
- `proxy` (str, optional): A proxy server address to use for requests.
- `cookies` (dict, optional): A dictionary of cookies for authentication with the Open Assistant API.
- `kwargs`: Additional keyword arguments for the `sampling_parameters` dictionary, which includes options like `top_k`, `top_p`, `typical_p`, `temperature`, `repetition_penalty`, and `max_new_tokens` to customize text generation behavior. 

**Example of usage with different parameters**:
```python
# Example 1: Using default model and no proxy or cookies
async for token in OpenAssistant.create_async_generator(model='OA_SFT_Llama_30B_6', messages=messages):
    print(token)

# Example 2: Using a specific model, a proxy server, and custom cookies
async for token in OpenAssistant.create_async_generator(
    model='OA_SFT_Llama_30B_6', 
    messages=messages, 
    proxy='http://proxy.example.com:8080',
    cookies={'session_id': '1234567890'}
):
    print(token)

# Example 3: Using a different model and specific sampling parameters
async for token in OpenAssistant.create_async_generator(
    model='OA_SFT_Llama_13B_6',
    messages=messages,
    top_k=10,
    top_p=0.8,
    temperature=0.5
):
    print(token)

```

## Inner Functions

None

## Additional Notes
- The `OpenAssistant` class is deprecated, as Open Assistant API is no longer available. This class is retained for reference purposes only.
- This code is designed for use with the Open Assistant API and requires authentication with the service.
- The code uses `aiohttp` library to handle asynchronous requests and responses.
- The `sampling_parameters` dictionary allows fine-tuning the text generation process based on the specific requirements of the application.
- The code supports the use of proxy servers and custom cookies for enhanced flexibility.
- The module uses `logger` from the `src.logger` module for logging information and errors.