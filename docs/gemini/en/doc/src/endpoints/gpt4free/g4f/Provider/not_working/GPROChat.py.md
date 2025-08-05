# GPROChat Provider

## Overview

This module provides the `GPROChat` class, which implements an asynchronous generator provider for interacting with the GPROChat API. This provider allows you to send messages and receive responses from the GPROChat service, leveraging its capabilities for natural language processing and generation. 

## Details

The `GPROChat` provider leverages the GPROChat API to handle text generation requests. It provides a user-friendly interface for interacting with the API, allowing you to send messages, manage response streaming, and utilize message history for context. 

## Classes

### `GPROChat`

**Description:** This class implements an asynchronous generator provider for interacting with the GPROChat API. It extends `AsyncGeneratorProvider` for stream-based responses and `ProviderModelMixin` for handling different model options.

**Inherits:** 
- `AsyncGeneratorProvider`
- `ProviderModelMixin`

**Attributes:**

- `url (str)`: The base URL of the GPROChat API.
- `api_endpoint (str)`: The endpoint for sending text generation requests.
- `working (bool)`: Flag indicating whether the provider is functional.
- `supports_stream (bool)`: Indicates whether the provider supports streaming responses.
- `supports_message_history (bool)`: Indicates whether the provider supports using message history.
- `default_model (str)`: The default model used by the provider.

**Methods:**

- `generate_signature(timestamp: int, message: str) -> str`: Generates a signature for the API request based on a timestamp, message, and a secret key.
- `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`: Creates an asynchronous generator for sending a text generation request to the GPROChat API.

**Example:**

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.GPROChat import GPROChat

provider = GPROChat()
messages = [
    {'role': 'user', 'content': 'Hello!'},
    {'role': 'assistant', 'content': 'Hi there!'},
]
async for chunk in provider.create_async_generator(model='gemini-1.5-pro', messages=messages):
    print(chunk)
```


## Class Methods

### `generate_signature`

**Purpose:** Generates a signature for the API request.

**Parameters:**

- `timestamp (int)`: Timestamp in milliseconds.
- `message (str)`: The message to be sent to the API.

**Returns:**

- `str`: The generated signature.

**How the Function Works:**

- This function calculates a SHA-256 hash of a string composed of the timestamp, message, and a secret key.
- The resulting hash is encoded in hexadecimal format and returned as the signature.

**Examples:**

```python
signature = GPROChat.generate_signature(timestamp=1693631200000, message="Hello, world!")
print(signature) # Output: a6564458c4c8d73259a8114e149f17673d22df2f86a29f85342e1105312d94e1
```

### `create_async_generator`

**Purpose:** Creates an asynchronous generator for sending a text generation request to the GPROChat API.

**Parameters:**

- `model (str)`: The model to use for text generation.
- `messages (Messages)`: A list of messages representing the conversation history.
- `proxy (str, optional)`: A proxy server URL. Defaults to None.
- `**kwargs`: Additional keyword arguments.

**Returns:**

- `AsyncResult`: An asynchronous generator that yields chunks of the response.

**How the Function Works:**

1. The function prepares the request data, including the formatted prompt, timestamp, and signature.
2. It establishes an HTTP session with appropriate headers.
3. The function sends a POST request to the API endpoint with the prepared data.
4. The response is streamed in chunks, and each chunk is yielded by the generator.

**Examples:**

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.GPROChat import GPROChat
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

provider = GPROChat()
messages: Messages = [
    {'role': 'user', 'content': 'Hello!'},
    {'role': 'assistant', 'content': 'Hi there!'},
]

async for chunk in provider.create_async_generator(model='gemini-1.5-pro', messages=messages):
    print(chunk)
```

## Parameter Details

- `messages (Messages)`: A list of messages representing the conversation history. Each message is a dictionary with the following keys:
    - `role (str)`: The role of the message sender (e.g., "user", "assistant").
    - `content (str)`: The message content.
- `proxy (str, optional)`: A proxy server URL. If provided, the API request will be sent through the proxy server. Defaults to `None`. 

## Examples

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.GPROChat import GPROChat
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

provider = GPROChat()
messages: Messages = [
    {'role': 'user', 'content': 'Hello!'},
    {'role': 'assistant', 'content': 'Hi there!'},
]

async for chunk in provider.create_async_generator(model='gemini-1.5-pro', messages=messages):
    print(chunk)

```

**Note:** This provider is currently marked as `not_working`. It may require further updates or configuration to function properly.