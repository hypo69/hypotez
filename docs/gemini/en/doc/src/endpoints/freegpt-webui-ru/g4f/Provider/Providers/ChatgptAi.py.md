# ChatgptAi Provider

## Overview

This module implements the `ChatgptAi` provider for the `g4f` framework. It enables users to interact with the ChatGPT AI model from OpenAI via its web interface.

## Details

The `ChatgptAi` provider leverages the ChatGPT web interface at `https://chatgpt.ai/gpt-4/` to send requests and retrieve responses from the ChatGPT model. It primarily relies on the `requests` library to perform HTTP communication with the website.

## Classes

### `ChatgptAi`

**Description**: This class represents the `ChatgptAi` provider and implements methods for interacting with the ChatGPT model.

**Attributes**:

- `url` (str): The base URL of the ChatGPT web interface.
- `model` (list): A list of supported model names. Currently, only `gpt-4` is supported.
- `supports_stream` (bool): Indicates whether the provider supports streaming responses.
- `needs_auth` (bool): Indicates whether the provider requires authentication.

**Methods**:

- `_create_completion(model: str, messages: list, stream: bool, **kwargs)`: Sends a request to the ChatGPT web interface to generate a response.

## Functions

### `_create_completion(model: str, messages: list, stream: bool, **kwargs)`

**Purpose**: Sends a request to the ChatGPT web interface to generate a response based on the provided context and model.

**Parameters**:

- `model` (str): The name of the model to use for the request.
- `messages` (list): A list of messages representing the context of the conversation.
- `stream` (bool): Indicates whether to stream the response or retrieve the entire response at once.
- `**kwargs`: Additional keyword arguments.

**Returns**:

- `Generator[Dict[str, Any], None, None]`: A generator that yields the responses from the ChatGPT API.

**Raises Exceptions**:

- `requests.exceptions.RequestException`: If there is an error during the HTTP request.
- `ValueError`: If the model is not supported.

**How the Function Works**:

1. The function constructs a chat message string based on the provided `messages`.
2. It retrieves the required information from the ChatGPT website using `requests.get()`.
3. It constructs a POST request to the ChatGPT API with necessary headers and data.
4. It sends the request using `requests.post()` and yields the received response as a JSON dictionary.

**Examples**:

```python
from g4f.Providers.ChatgptAi import ChatgptAi
from g4f.Provider import Provider

chatgpt_provider = ChatgptAi()
provider = Provider(chatgpt_provider)

messages = [
    {"role": "user", "content": "Hello, world!"},
]

response = provider.create_completion(model="gpt-4", messages=messages)
print(next(response))
```

## Parameter Details

- `model` (str): The name of the model to use for the request. Currently, only `gpt-4` is supported.
- `messages` (list): A list of messages representing the context of the conversation. Each message should be a dictionary with the following keys:
    - `role`: The role of the message sender (e.g., 'user', 'assistant').
    - `content`: The content of the message.
- `stream` (bool): Indicates whether to stream the response or retrieve the entire response at once.

## Examples

```python
from g4f.Providers.ChatgptAi import ChatgptAi
from g4f.Provider import Provider

chatgpt_provider = ChatgptAi()
provider = Provider(chatgpt_provider)

messages = [
    {"role": "user", "content": "Hello, world!"},
]

response = provider.create_completion(model="gpt-4", messages=messages)
print(next(response))
```

This example creates a provider instance using the `ChatgptAi` class, defines a list of messages representing a simple conversation, and then uses the `create_completion` method to retrieve a response from the ChatGPT API. The resulting response is printed.