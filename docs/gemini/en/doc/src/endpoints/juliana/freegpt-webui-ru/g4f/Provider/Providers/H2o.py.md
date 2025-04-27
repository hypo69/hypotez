# H2o Provider Documentation

## Overview

This module provides a H2o provider for the `hypotez` project, allowing interaction with the H2o GPT-GM API. The provider handles communication with the H2o API, allowing the use of various H2o models for generating responses.

## Details

The provider implements a `_create_completion` function to handle completion requests to the H2o API. It uses a `Session` object from the `requests` library to make HTTP requests to the API endpoint. The code defines a set of models supported by the provider, including their model IDs, and sets the necessary headers for API requests.

The `_create_completion` function builds a conversation context from the provided messages and sends it to the API. It then receives a stream of responses from the API and yields each response token to the caller.

## Classes

### `class Provider`

**Description**: This class represents the base provider for the `hypotez` project. 

**Inherits**: `None`

**Attributes**: 
 - `url` (`str`): The base URL of the provider's API endpoint. 
 - `model` (`list[str]`): A list of model names supported by the provider. 
 - `supports_stream` (`bool`): Indicates whether the provider supports streaming responses.
 - `needs_auth` (`bool`): Indicates whether the provider requires authentication.

**Methods**:
 - `_create_completion`(`model`: `str`, `messages`: `list`, `stream`: `bool`, **kwargs`): This method handles completion requests to the provider's API, sending the conversation context and receiving a stream of responses. 

## Functions

### `_create_completion`

**Purpose**: This function handles completion requests to the H2o GPT-GM API, sending the conversation context and receiving a stream of responses.

**Parameters**:
 - `model` (`str`): The name of the H2o model to use for completion.
 - `messages` (`list`): A list of messages in the conversation.
 - `stream` (`bool`):  Indicates whether to stream the response.
 - `**kwargs` (`dict`): Additional keyword arguments to customize the completion request (e.g., `temperature`, `truncate`).

**Returns**:
 - `Generator[str, None, None]`: A generator that yields each token of the generated response.

**Raises Exceptions**:
 - `Exception`: Raised if an error occurs during communication with the H2o API.

**Inner Functions**:
 - None

**How the Function Works**:
1. Constructs a conversation string from the provided messages.
2. Sends a POST request to the H2o API endpoint with the conversation string and additional parameters.
3. Iterates over the streamed response lines.
4. For each line containing `data`, extracts the token text and yields it to the caller.

**Examples**:
```python
from hypotez.src.endpoints.juliana.freegpt-webui-ru.g4f.Provider.Providers.H2o import Provider
from hypotez.src.endpoints.juliana.freegpt-webui-ru.g4f.Provider.Providers.H2o import _create_completion

provider = Provider()
messages = [
    {'role': 'user', 'content': 'Hello, how are you?'},
    {'role': 'assistant', 'content': 'I am doing well, thank you! How can I help you?'}
]
model = 'falcon-7b'

# Stream the response
for token in _create_completion(model=model, messages=messages, stream=True):
    print(token, end="") 
```
```python
# Get the full response
response = ''.join(list(_create_completion(model=model, messages=messages, stream=True)))
print(response)
```

## Parameter Details

 - `model` (`str`): The name of the H2o model to use for completion. This parameter specifies the model to use for generating responses.
 - `messages` (`list`): A list of messages in the conversation. The provider uses this list to construct the conversation context for the completion request. 
 - `stream` (`bool`): Indicates whether to stream the response. If True, the function returns a generator that yields each token of the response.
 - `temperature` (`float`, optional): Controls the randomness of the generated response (default: `0.4`).
 - `truncate` (`int`, optional): Limits the maximum length of the conversation context (default: `2048`).
 - `max_new_tokens` (`int`, optional): Sets the maximum number of tokens to generate in the response (default: `1024`).
 - `do_sample` (`bool`, optional): Enables or disables sampling of the response (default: `True`).
 - `repetition_penalty` (`float`, optional): Controls the likelihood of repeating the same tokens in the response (default: `1.2`).
 - `return_full_text` (`bool`, optional):  Indicates whether to return the full text of the response (default: `False`).
 - `id` (`str`, optional):  A unique identifier for the request (default: a random UUID).
 - `response_id` (`str`, optional):  A unique identifier for the response (default: a random UUID).
 - `is_retry` (`bool`, optional): Indicates whether the request is a retry (default: `False`).
 - `use_cache` (`bool`, optional): Indicates whether to use the cache for the request (default: `False`).
 - `web_search_id` (`str`, optional):  An identifier for web search requests (default: `''`).

## Examples

### Using the H2o Provider

```python
from hypotez.src.endpoints.juliana.freegpt-webui-ru.g4f.Provider.Providers.H2o import Provider
from hypotez.src.endpoints.juliana.freegpt-webui-ru.g4f.Provider.Providers.H2o import _create_completion

# Creating a Provider instance
provider = Provider()

# Setting the model to use for completion
model_name = 'falcon-7b'

# Defining the conversation context
messages = [
    {'role': 'user', 'content': 'What is the capital of France?'},
    {'role': 'assistant', 'content': 'The capital of France is Paris.'}
]

# Generating a response
for token in provider._create_completion(model=model_name, messages=messages, stream=True):
    print(token, end="")

# Using keyword arguments for customization
response = ''.join(list(provider._create_completion(model=model_name, messages=messages, stream=True, temperature=0.7)))
print(response)
```

### Using the `_create_completion` Function

```python
from hypotez.src.endpoints.juliana.freegpt-webui-ru.g4f.Provider.Providers.H2o import _create_completion

model_name = 'falcon-7b'
messages = [
    {'role': 'user', 'content': 'What is the meaning of life?'}
]

# Generating a response with default parameters
for token in _create_completion(model=model_name, messages=messages, stream=True):
    print(token, end="")

# Generating a response with custom parameters
response = ''.join(list(_create_completion(model=model_name, messages=messages, stream=True, temperature=0.9, max_new_tokens=512)))
print(response)
```

### Understanding the Code

The `_create_completion` function is a core component of the H2o provider. It manages communication with the H2o GPT-GM API and handles the generation of responses. The code demonstrates how to use the provider for both streaming and non-streaming responses, allowing developers to customize the behavior based on their requirements. The use of keyword arguments provides flexibility in controlling various aspects of the completion process, such as temperature, maximum token length, and sampling.

## Conclusion

The H2o provider offers a robust and customizable interface for interacting with the H2o GPT-GM API. This documentation provides a comprehensive overview of the provider's functionality, enabling developers to effectively integrate H2o models into their projects.