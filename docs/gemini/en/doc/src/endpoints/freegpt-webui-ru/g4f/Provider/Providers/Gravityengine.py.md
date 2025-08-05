# Gravityengine Provider for g4f

## Overview

This module implements the `Gravityengine` provider for the `g4f` module within the `hypotez` project. The `Gravityengine` provider utilizes the Gravity Engine API for generating text responses. It offers several features including support for stream responses and various GPT models.

## Details

The `Gravityengine` provider is designed to interact with the Gravity Engine API for text generation tasks. It exposes a single function `_create_completion` which handles the API requests and returns text responses. The provider supports different GPT models, including `gpt-3.5-turbo-16k` and `gpt-3.5-turbo-0613`.

## Classes

None

## Functions

### `_create_completion`

**Purpose**: This function sends a request to the Gravity Engine API to generate a text completion based on the provided model, messages, and other parameters.

**Parameters**:

- `model` (str): The GPT model to use for text generation. Supported models are `gpt-3.5-turbo-16k` and `gpt-3.5-turbo-0613`.
- `messages` (list): A list of message objects containing the conversation history.
- `stream` (bool): Indicates whether to use streaming responses.
- `**kwargs`: Additional parameters to be passed to the Gravity Engine API.

**Returns**:

- `Generator[str, None, None]`: A generator that yields text responses.

**Raises Exceptions**:

- `ConnectionError`: If the connection to the Gravity Engine API fails.
- `HTTPError`: If the Gravity Engine API returns an error.

**How the Function Works**:

1. The function builds a request payload with the provided `model`, `messages`, and other parameters.
2. It sends a POST request to the Gravity Engine API endpoint.
3. If the request is successful, it iterates through the response stream and yields each text response.

**Examples**:

```python
# Example usage of _create_completion function
from ...typing import Dict, List

# Define a list of message objects
messages: List[Dict] = [
    {"role": "user", "content": "Hello, how are you?"},
]

# Generate text using the gpt-3.5-turbo-16k model with streaming responses
for response in _create_completion(model="gpt-3.5-turbo-16k", messages=messages, stream=True):
    print(response)

# Generate text using the gpt-3.5-turbo-0613 model without streaming responses
response = _create_completion(model="gpt-3.5-turbo-0613", messages=messages, stream=False)
print(response)
```

## Parameter Details

- `url` (str): The base URL of the Gravity Engine API.
- `model` (list): A list of supported GPT models for text generation.
- `supports_stream` (bool): Indicates whether the provider supports streaming responses.
- `needs_auth` (bool): Indicates whether the provider requires authentication.

## Examples

```python
# Example usage of _create_completion function
from ...typing import Dict, List

# Define a list of message objects
messages: List[Dict] = [
    {"role": "user", "content": "Hello, how are you?"},
]

# Generate text using the gpt-3.5-turbo-16k model with streaming responses
for response in _create_completion(model="gpt-3.5-turbo-16k", messages=messages, stream=True):
    print(response)

# Generate text using the gpt-3.5-turbo-0613 model without streaming responses
response = _create_completion(model="gpt-3.5-turbo-0613", messages=messages, stream=False)
print(response)
```