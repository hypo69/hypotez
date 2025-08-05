# Yqcloud Provider

## Overview

This module provides the `Yqcloud` provider for the `g4f` project, enabling interaction with the Yqcloud AI API for text generation.

## Details

The `Yqcloud` provider utilizes the `requests` library to make API calls to the Yqcloud API, specifically the `generateStream` endpoint. 

## Classes

### `Yqcloud`

**Description**: This class represents the `Yqcloud` provider, handling communication with the Yqcloud API.

**Attributes**:
- `url`: The base URL of the Yqcloud API.
- `model`: A list of supported AI models.
- `supports_stream`: A boolean indicating whether the provider supports streaming responses.
- `needs_auth`: A boolean indicating whether the provider requires authentication.

**Methods**:

- `_create_completion(model: str, messages: list, stream: bool, **kwargs)`: 
    **Purpose**: This private method constructs and sends an API request to the Yqcloud API to generate text completions. 
    
    **Parameters**:
    - `model (str)`: The AI model to use for text generation.
    - `messages (list)`: A list of messages in the conversation history.
    - `stream (bool)`: Whether to stream the response.
    - `**kwargs`: Additional keyword arguments to pass to the API request.
    
    **Returns**:
    - `Generator[str, None, None]`: A generator that yields text chunks of the generated response.
    
    **Raises Exceptions**:
    - `requests.exceptions.RequestException`: If there's an error during the API request.

## Functions

### `params`

**Purpose**: This function provides information about the `Yqcloud` provider, including supported models and parameter types.

**Parameters**: None

**Returns**:
- `str`: A formatted string describing the provider's capabilities.

**How the Function Works**:
- It uses the `get_type_hints` function to retrieve the type annotations of the `_create_completion` function's parameters.
- It then constructs a string that lists the supported AI models and their corresponding parameter types.

**Examples**:

```python
>>> params = Yqcloud.params
>>> print(params) 
g4f.Providers.Yqcloud supports: (model: str, messages: list, stream: bool)
```

## Parameter Details

- `model (str)`: The specific AI model to use for text generation. The `Yqcloud` provider currently supports `gpt-3.5-turbo`. 
- `messages (list)`:  A list of messages in the conversation history. This list is used to provide context for the AI model to generate relevant responses.
- `stream (bool)`:  Indicates whether to stream the response. If `True`, the `_create_completion` function will yield text chunks as they become available, allowing for real-time display of the generated text.

## Examples

```python
# Example of using Yqcloud provider with a list of messages.
messages = [
    {'role': 'user', 'content': 'Hello, how are you?'},
    {'role': 'assistant', 'content': 'I am doing well, thank you.'},
]

# Use the Yqcloud provider to generate a text completion.
for token in Yqcloud._create_completion(model='gpt-3.5-turbo', messages=messages, stream=True):
    print(token, end='')
```

This example demonstrates how to use the `Yqcloud` provider to generate a text completion based on a conversation history. The example also showcases how to stream the response for real-time output.