# Lockchat Provider

## Overview

This module defines the `Lockchat` provider for the `g4f` framework, which provides access to the Lockchat API for generating text using GPT-4 and GPT-3.5-turbo models.

## Details

The `Lockchat` provider leverages the Lockchat API to interact with their GPT models. This API utilizes a RESTful interface to handle requests and responses. 

## Classes

### `Lockchat`

**Description**: This class represents the `Lockchat` provider for the `g4f` framework, enabling interaction with the Lockchat API for text generation.

**Attributes**:
- `url`: URL of the Lockchat API.
- `model`: A list of supported models (currently `["gpt-4", "gpt-3.5-turbo"]`).
- `supports_stream`: Boolean value indicating whether the API supports streaming responses.
- `needs_auth`: Boolean value indicating whether the API requires authentication.

**Methods**:
- `_create_completion`: Sends a request to the Lockchat API to generate a completion based on the provided context and parameters.

## Functions

### `_create_completion`

**Purpose**: Sends a request to the Lockchat API to generate a text completion based on the given input.

**Parameters**:
- `model`: The name of the GPT model to use for text generation (e.g., "gpt-4").
- `messages`: A list of messages representing the conversation history.
- `stream`: Boolean value indicating whether to stream the response.
- `temperature`: A value between 0 and 1 that controls the randomness of the generated text (default: 0.7).
- `**kwargs`: Additional keyword arguments for the API request.

**Returns**:
- A generator yielding text tokens as they become available if `stream` is `True`, otherwise returns the full text completion.

**Raises Exceptions**:
- `requests.exceptions.RequestException`: If an error occurs while sending the request to the Lockchat API.

**How the Function Works**:

1. Constructs a payload containing the model name, messages, and other parameters for the API request.
2. Sends a POST request to the Lockchat API endpoint using the `requests` library.
3. If `stream` is `True`, iterates through the response lines, extracting text tokens and yielding them to the caller. 
4. If `stream` is `False`, reads the entire response and returns the generated text.

**Examples**:

```python
from g4f.Providers.Lockchat import Lockchat

lockchat_provider = Lockchat()

# Generate text with GPT-4
messages = [
    {"role": "user", "content": "Hello! Can you write a short story about a cat?"},
]
response = lockchat_provider._create_completion(model="gpt-4", messages=messages, stream=False)

# Print the generated text
print(response)

# Generate text with GPT-3.5-turbo, streaming the response
messages = [
    {"role": "user", "content": "Tell me a joke."},
]
for token in lockchat_provider._create_completion(model="gpt-3.5-turbo", messages=messages, stream=True):
    print(token, end="")
```

## Parameter Details

- `model`: The name of the GPT model to use for text generation. Supported values include "gpt-4" and "gpt-3.5-turbo".
- `messages`: A list of messages representing the conversation history. Each message is a dictionary with keys: `role` (either "user" or "assistant") and `content` (the text of the message).
- `stream`: Boolean value indicating whether to stream the response. If `True`, the function returns a generator that yields text tokens as they become available. If `False`, the function returns the full text completion as a string.
- `temperature`: A value between 0 and 1 that controls the randomness of the generated text. A higher value means more creative and unpredictable text, while a lower value means more coherent and predictable text. The default value is 0.7.
- `**kwargs`: Additional keyword arguments for the API request. These can include parameters such as `top_p`, `top_k`, and `max_tokens`. 

**Examples**:

```python
from g4f.Providers.Lockchat import Lockchat

lockchat_provider = Lockchat()

# Example 1: Generate text with GPT-4, no streaming
messages = [
    {"role": "user", "content": "Write a poem about a cat."},
]
response = lockchat_provider._create_completion(model="gpt-4", messages=messages, stream=False)
print(response)

# Example 2: Generate text with GPT-3.5-turbo, streaming the response
messages = [
    {"role": "user", "content": "What is the meaning of life?"},
]
for token in lockchat_provider._create_completion(model="gpt-3.5-turbo", messages=messages, stream=True):
    print(token, end="")

# Example 3: Generate text with GPT-4, specifying additional parameters
messages = [
    {"role": "user", "content": "Describe the weather in London."},
]
response = lockchat_provider._create_completion(model="gpt-4", messages=messages, stream=False, temperature=0.5, top_p=0.9)
print(response)
```