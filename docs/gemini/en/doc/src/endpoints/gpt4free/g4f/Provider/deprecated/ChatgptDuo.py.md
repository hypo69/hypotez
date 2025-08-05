# ChatgptDuo.py

## Overview

This module provides the `ChatgptDuo` class, an asynchronous provider for accessing the ChatGPT Duo API. The class implements the `AsyncProvider` interface and is designed to interact with ChatGPT Duo's API for generating responses based on user prompts. 

## Details

This module is part of the `hypotez` project's `endpoints` package, specifically within the `gpt4free` directory. This indicates that it's responsible for handling communication with the ChatGPT Duo API, which is a service providing free access to OpenAI's GPT models. 

The `ChatgptDuo` class inherits from the `AsyncProvider` base class, meaning it supports asynchronous communication with the API. It defines the following attributes:

- `url`: The base URL of the ChatGPT Duo API.
- `supports_gpt_35_turbo`: A boolean indicating whether the provider supports the GPT-3.5 Turbo model.
- `working`: A boolean flag to track the provider's active status.

## Classes

### `ChatgptDuo`

**Description**: This class represents an asynchronous provider for interacting with the ChatGPT Duo API. It inherits from the `AsyncProvider` base class, providing a standardized interface for communication with different AI providers.

**Attributes**:

- `url (str)`: The base URL of the ChatGPT Duo API.
- `supports_gpt_35_turbo (bool)`: Indicates if the provider supports the GPT-3.5 Turbo model.
- `working (bool)`: Tracks the provider's active status.

**Methods**:

#### `create_async`

**Purpose**:  Asynchronously creates an instance of the `ChatgptDuo` provider and makes a request to the API to generate a response based on the provided prompt. 

**Parameters**:

- `model (str)`: Specifies the language model to use for the response.
- `messages (Messages)`: A list of messages representing the conversation history.
- `proxy (str, optional)`: A proxy server address for accessing the API. Defaults to None.
- `timeout (int, optional)`:  Specifies the timeout for the request. Defaults to 120 seconds.

**Returns**:

- `str`: The generated response from the ChatGPT Duo API. 

**Raises Exceptions**:

- `requests.exceptions.HTTPError`:  Raised if the API request encounters an HTTP error.

#### `get_sources`

**Purpose**: Retrieves the list of sources used by the ChatGPT Duo API to generate the last response. 

**Returns**:

- `list`: A list of source information dictionaries, each containing:
  - `title`: The title of the source.
  - `url`: The URL of the source.
  - `snippet`: A snippet of text from the source.

**Example**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.ChatgptDuo import ChatgptDuo
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

messages: Messages = [
    {"role": "user", "content": "What is the capital of France?"},
]

async def main():
    response = await ChatgptDuo.create_async(model="gpt-3.5-turbo", messages=messages)
    print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## Parameter Details

- `model (str)`: Specifies the language model used for generating the response.  
- `messages (Messages)`: A list of messages, where each message is a dictionary with a `role` ("user" or "assistant") and `content` (the text of the message). This represents the conversation history.
- `proxy (str, optional)`:  A proxy server address to be used for the API request, allowing for access through a proxy. 
- `timeout (int, optional)`: Sets the maximum time (in seconds) to wait for a response from the API. If the timeout expires, an exception is raised. 


## Examples

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.ChatgptDuo import ChatgptDuo
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Example 1: Basic Usage
messages: Messages = [
    {"role": "user", "content": "What is the capital of France?"},
]
response = await ChatgptDuo.create_async(model="gpt-3.5-turbo", messages=messages)
print(response)

# Example 2: Using a Proxy
messages: Messages = [
    {"role": "user", "content": "What is the meaning of life?"},
]
response = await ChatgptDuo.create_async(model="gpt-3.5-turbo", messages=messages, proxy="http://127.0.0.1:8080")
print(response)

# Example 3: Setting a Timeout
messages: Messages = [
    {"role": "user", "content": "Tell me a joke."},
]
response = await ChatgptDuo.create_async(model="gpt-3.5-turbo", messages=messages, timeout=60)
print(response)

# Example 4: Retrieving Sources
messages: Messages = [
    {"role": "user", "content": "What are the main causes of climate change?"},
]
response = await ChatgptDuo.create_async(model="gpt-3.5-turbo", messages=messages)
print(response)
sources = ChatgptDuo.get_sources()
print(sources)
```

## Notes

- The `ChatgptDuo` class has been marked as deprecated, suggesting that there might be a more up-to-date or preferred alternative available within the `hypotez` project. 
- The code indicates that the provider supports the GPT-3.5 Turbo model (`supports_gpt_35_turbo = True`).
- The `working` flag likely indicates whether the provider is currently functioning or has encountered an issue.

**Further Improvements**:

-  The documentation should include information about the specific API endpoints used by the `ChatgptDuo` class.
- It would be helpful to provide more details about the `format_prompt` function used to prepare the prompt for the API request.
-  Additional examples could be added, illustrating the usage of the `get_sources` method.