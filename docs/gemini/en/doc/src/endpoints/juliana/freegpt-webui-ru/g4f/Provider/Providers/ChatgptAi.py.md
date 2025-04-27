# ChatgptAi Provider for g4f

## Overview

This module defines the `ChatgptAi` class, which implements a provider for interacting with the ChatGPT AI service via its website. It enables the generation of text completions using the `gpt-4` model.

## Details

The `ChatgptAi` class is responsible for sending user messages to the ChatGPT website and receiving responses. It uses the `requests` library for HTTP communication and regular expressions to extract relevant data from the website's HTML.

## Classes

### `ChatgptAi`

**Description**: This class represents a provider for interacting with the ChatGPT AI service.

**Attributes**:

- `url`: The URL of the ChatGPT website.
- `model`: A list of supported AI models (currently only `gpt-4`).
- `supports_stream`: Indicates whether the provider supports streaming responses.
- `needs_auth`: Indicates whether the provider requires authentication.

**Methods**:

- `_create_completion(model: str, messages: list, stream: bool, **kwargs)`: This private method handles the generation of text completions. It constructs the request payload, sends it to the ChatGPT website, and extracts the response.


## Functions

### `_create_completion`

**Purpose**: This function generates text completions using the ChatGPT AI service.

**Parameters**:

- `model` (str): The name of the AI model to use (e.g., `gpt-4`).
- `messages` (list): A list of user messages.
- `stream` (bool): Indicates whether to stream the response.
- `**kwargs`: Additional keyword arguments for the request.

**Returns**:

- `Generator`: A generator that yields the response data.

**Raises Exceptions**:

- `Exception`: If an error occurs during the request or response processing.

**How the Function Works**:

1. The function constructs a chat string from the user messages, combining them into a single string with appropriate formatting.
2. It makes a GET request to the ChatGPT website to extract relevant data, including the `nonce`, `post_id`, `url`, and `bot_id` values.
3. It creates a request payload with the extracted data and the chat string, then sends a POST request to the ChatGPT website using the `requests.post()` method.
4. The function yields the parsed JSON response data, allowing for asynchronous processing.

**Examples**:

```python
from hypotez.src.endpoints.juliana.freegpt-webui-ru.g4f.Provider.Providers.ChatgptAi import ChatgptAi

provider = ChatgptAi()
messages = [
    {'role': 'user', 'content': 'Hello!'}
]
completion = provider._create_completion(model='gpt-4', messages=messages)
for response in completion:
    print(response['data'])
```

## Parameter Details

- `model` (str): The name of the AI model to use (e.g., `gpt-4`).
- `messages` (list): A list of user messages, each represented as a dictionary with `role` (e.g., `user` or `assistant`) and `content` keys.
- `stream` (bool): A boolean flag indicating whether the response should be streamed.
- `**kwargs`: Additional keyword arguments for the request, allowing for customization of the request parameters.

## Examples

```python
from hypotez.src.endpoints.juliana.freegpt-webui-ru.g4f.Provider.Providers.ChatgptAi import ChatgptAi

provider = ChatgptAi()
messages = [
    {'role': 'user', 'content': 'Hello!'},
    {'role': 'assistant', 'content': 'Hi there!'}
]
completion = provider._create_completion(model='gpt-4', messages=messages, stream=False)
for response in completion:
    print(response['data'])
```