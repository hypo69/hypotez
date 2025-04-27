# ChatAnywhere Provider

## Overview

This module defines the `ChatAnywhere` class, which provides an asynchronous generator for interacting with the ChatAnywhere API to generate responses using various AI models.

## Details

The `ChatAnywhere` class inherits from `AsyncGeneratorProvider` and implements methods for initiating and managing an asynchronous generator.

### Classes

#### `class ChatAnywhere`

**Description:** This class provides a mechanism to interact with the ChatAnywhere API to generate text responses using various AI models, including GPT-3.5 Turbo.

**Inherits:** `AsyncGeneratorProvider`

**Attributes:**

- `url (str):`  The base URL of the ChatAnywhere API.
- `supports_gpt_35_turbo (bool):`  Indicates whether the provider supports the GPT-3.5 Turbo model (True in this case).
- `supports_message_history (bool):` Indicates whether the provider supports message history (True in this case).
- `working (bool):` A flag indicating whether the provider is currently operational (False by default).

**Methods:**

- `create_async_generator(model: str, messages: Messages, proxy: str = None, timeout: int = 120, temperature: float = 0.5, **kwargs) -> AsyncResult:`
    -  Creates an asynchronous generator that handles requests to the ChatAnywhere API for generating responses.
    -  **Purpose:**  Initiates an asynchronous interaction with the ChatAnywhere API, sending user messages and receiving model responses.
    -  **Parameters:**
        - `model (str):`  Specifies the desired AI model to use for generating responses.
        - `messages (Messages):` A list of messages, including user inputs and previous model responses, for building the context of the conversation.
        - `proxy (str, optional):` An optional proxy server address for routing requests. Defaults to None.
        - `timeout (int, optional):`  Sets the maximum time in seconds to wait for a response from the API. Defaults to 120 seconds.
        - `temperature (float, optional):` Controls the creativity and randomness of the generated responses. Defaults to 0.5.
        - `**kwargs:`  Additional keyword arguments that can be passed to the API.
    -  **Returns:** An `AsyncResult` object, which wraps the asynchronous generator.
    -  **Raises:** `Exception` if an error occurs during the request.
    -  **How it works:**
        -  The method creates an asynchronous `ClientSession` with specified headers and a timeout.
        -  It assembles a data dictionary containing the conversation messages, model ID, prompt (if applicable), temperature, and other parameters.
        -  It performs a POST request to the ChatAnywhere API endpoint (`/v1/chat/gpt/`) with the constructed data.
        -  It handles the response by decoding the received chunks and yields them as strings.

## Parameter Details

- `model (str):` Specifies the AI model to use for generating responses.
- `messages (Messages):` A list containing user inputs and previous model responses.
- `proxy (str, optional):`  An optional proxy server address.
- `timeout (int, optional):` Sets the maximum wait time for a response.
- `temperature (float, optional):` Controls response creativity and randomness.
- `**kwargs:` Additional keyword arguments passed to the API.

## Examples

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.ChatAnywhere import ChatAnywhere
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Example with GPT-3.5 Turbo model and user messages
messages: Messages = [
    {"role": "user", "content": "Hello, how are you?"},
    {"role": "assistant", "content": "I am an AI, so I don't have feelings, but I'm here to help!"},
    {"role": "user", "content": "Can you tell me a joke?"},
]
async_generator = await ChatAnywhere.create_async_generator(model="gpt-3.5-turbo", messages=messages)
async for chunk in async_generator:
    print(chunk)

# Example with a custom proxy and timeout
async_generator = await ChatAnywhere.create_async_generator(model="gpt-3.5-turbo", messages=messages, proxy="http://proxy_server:port", timeout=60)
async for chunk in async_generator:
    print(chunk)
```