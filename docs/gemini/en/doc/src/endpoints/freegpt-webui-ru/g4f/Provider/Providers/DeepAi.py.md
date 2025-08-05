# DeepAi Provider

## Overview

This module defines a provider for interacting with the DeepAi API for generating text completions. It provides functions to send requests and handle responses for text completion tasks.

## Details

The DeepAi Provider utilizes the DeepAi API for generating text completions. The code is designed to be user-friendly and supports streaming responses.

## Classes

### `class DeepAi`

**Description**: This class represents the DeepAi Provider, handling interactions with the DeepAi API.

**Attributes**:

- `url (str)`: The base URL for the DeepAi API.
- `model (list)`: A list of supported models for text completion.
- `supports_stream (bool)`: Flag indicating whether the provider supports streaming responses.
- `needs_auth (bool)`: Flag indicating whether the provider requires authentication.

**Methods**:

- `_create_completion(model: str, messages: list, stream: bool, **kwargs)`: This private method sends a request to the DeepAi API for text completion and handles the response.

## Functions

### `_create_completion(model: str, messages: list, stream: bool, **kwargs)`

**Purpose**: This function sends a request to the DeepAi API for text completion and handles the response.

**Parameters**:

- `model (str)`: The model to use for text completion.
- `messages (list)`: A list of messages to be sent to the model.
- `stream (bool)`: A flag indicating whether to stream the response.
- `**kwargs`: Additional keyword arguments for the API request.

**Returns**:

- `Generator[str, None, None]`: A generator yielding the response chunks in string format.

**Raises Exceptions**:

- `requests.exceptions.RequestException`: If there is an error during the request.

**Inner Functions**:

- `md5(text: str) -> str`: This inner function calculates the MD5 hash of the provided text.
- `get_api_key(user_agent: str) -> str`: This inner function generates an API key based on the provided user agent.

**How the Function Works**:

1. It generates an API key based on the user agent.
2. It constructs a POST request to the DeepAi API endpoint with the user agent, API key, and provided messages as input data.
3. It sends the request and iterates through the response chunks.
4. It decodes the response chunks into strings and yields them as a generator.

**Examples**:

```python
from g4f.Provider.Providers.DeepAi import DeepAi

provider = DeepAi()

# Example 1: Simple text completion with streaming
messages = [{"role": "user", "content": "Hello, world!"}]
for chunk in provider._create_completion(model="gpt-3.5-turbo", messages=messages, stream=True):
    print(chunk, end="")

# Example 2: Text completion with additional parameters
messages = [{"role": "user", "content": "Write a poem about the moon."}]
for chunk in provider._create_completion(model="gpt-3.5-turbo", messages=messages, stream=True, temperature=0.7):
    print(chunk, end="")
```