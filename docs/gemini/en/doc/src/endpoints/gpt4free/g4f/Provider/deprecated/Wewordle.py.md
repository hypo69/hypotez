# Provider.deprecated.Wewordle Module

## Overview

This module contains the `Wewordle` class, which implements a deprecated version of the `AsyncProvider` interface for interacting with the `wewordle.org` API. It provides functionality for sending requests to the API and receiving responses.

## Details

The `Wewordle` class is marked as deprecated, which means it's no longer actively maintained and might be removed in future updates. The module relies on the `aiohttp` library for asynchronous HTTP requests and utilizes a randomized user ID and application ID for API authentication.

## Classes

### `class Wewordle`

**Description**:  The `Wewordle` class implements a deprecated version of the `AsyncProvider` interface for interacting with the `wewordle.org` API.

**Inherits**:  `AsyncProvider`

**Attributes**:

- `url (str)`: Base URL for the `wewordle.org` API.
- `working (bool)`: Indicates whether the provider is currently active.
- `supports_gpt_35_turbo (bool)`: Indicates support for the GPT-3.5 Turbo model.

**Methods**:

- `create_async(model: str, messages: list[dict[str, str]], proxy: str = None, **kwargs) -> str`: Asynchronously sends a request to the `wewordle.org` API with a list of messages, using the provided model and optional proxy. Returns the content of the response message if successful, otherwise returns `None`.

**How the Method Works**:

1. The method generates a random user ID and application ID using `random.choices`.
2. It constructs a request payload with the user ID, messages, and subscriber information (including a timestamp and dummy data).
3. The method uses the `aiohttp` library to send a POST request to the API endpoint with the generated payload, specifying the model, proxy, and headers.
4. If the request succeeds, the method parses the JSON response and returns the content of the message.

**Examples**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Wewordle import Wewordle

messages = [
    {"role": "user", "content": "Hello, world!"},
    {"role": "assistant", "content": "Hello to you too!"},
]
model = "gpt-3.5-turbo"

response = await Wewordle.create_async(model, messages)
print(response)
```

**Inner Functions**:

- None

## Parameter Details

- `model (str)`: The name of the AI model to use for the request.
- `messages (list[dict[str, str]])`: A list of messages to be sent to the API. Each message is a dictionary containing the role (`user` or `assistant`) and the content of the message.
- `proxy (str)`: Optional proxy server to use for the request. Defaults to `None`.
- `**kwargs`:  Additional keyword arguments that are passed to the `aiohttp` session.

## Examples

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Wewordle import Wewordle

messages = [
    {"role": "user", "content": "Hello, how are you?"},
    {"role": "assistant", "content": "I'm doing well, thank you! How are you?"},
]

model = "gpt-3.5-turbo"
response = await Wewordle.create_async(model, messages)

if response:
    print(response)

messages = [
    {"role": "user", "content": "What is the meaning of life?"},
    {"role": "assistant", "content": "The meaning of life is a philosophical question that has been pondered by people for centuries. There is no one definitive answer, and what it means to each individual may vary depending on their personal beliefs and experiences."},
]

response = await Wewordle.create_async(model, messages)

if response:
    print(response)

```