#  Aichat Provider

##  Overview

This module provides the `Aichat` class, which acts as a provider for interacting with the `aichat.org` service for generating text using AI models. It is used to send prompts to the service and retrieve generated responses.

##  Details

The `Aichat` provider leverages the `chat-gpt.org` service, a popular platform for AI-powered text generation. It is a specialized provider that handles the communication with the service, including setting up requests, handling cookies, and parsing responses.

##  Classes

###  `Aichat`

**Description:**

The `Aichat` class is responsible for interacting with the `aichat.org` service. It inherits from the `AsyncProvider` base class, providing a standard interface for interacting with AI models.

**Inherits:**

- `AsyncProvider`

**Attributes:**

- `url (str)`: The base URL for the `aichat.org` service.
- `working (bool)`: Indicates whether the provider is currently working (set to `False` as it is marked as deprecated).
- `supports_gpt_35_turbo (bool)`: Specifies whether the provider supports the `gpt-3.5-turbo` model.

**Methods:**

- `create_async(model: str, messages: Messages, proxy: str = None, **kwargs) -> str:`:  A static method for creating an asynchronous instance of the provider and generating text using the `aichat.org` service.

##  Class Methods

### `create_async(model: str, messages: Messages, proxy: str = None, **kwargs) -> str:`

**Purpose:**

Asynchronously creates an instance of the `Aichat` provider and generates text using the `aichat.org` service. This method sends a prompt to the service, handles the response, and returns the generated text.

**Parameters:**

- `model (str)`: The name of the AI model to use for text generation (e.g., 'gpt-3.5-turbo').
- `messages (Messages)`: A list of messages representing the conversation history.
- `proxy (str, optional)`:  A proxy server address for making requests. Defaults to `None`.
- `**kwargs`: Additional keyword arguments for customizing the request.

**Returns:**

- `str`: The generated text from the `aichat.org` service.

**Raises Exceptions:**

- `RuntimeError`: Raised if the provider requires cookies but cookies are not found.
- `Exception`: Raised if the service returns an error response.

**How the Function Works:**

1.  The function first checks if cookies are provided. If not, it attempts to retrieve cookies from the browser.
2.  If cookies are not found, it raises a `RuntimeError` indicating the need for cookies.
3.  The function sets up request headers with necessary information, including authorization, language, and content type.
4.  It uses a `StreamSession` to send a POST request to the `aichat.org` service with the formatted prompt and additional parameters.
5.  The function handles any errors that occur during the request and raises an exception if there is a problem with the response.
6.  It parses the response, extracts the generated text, and returns it.

**Examples:**

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Aichat import Aichat
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Example usage
messages: Messages = [
    {'role': 'user', 'content': 'Hello, how are you?'},
]

# Generate text using the gpt-3.5-turbo model
response = await Aichat.create_async(model='gpt-3.5-turbo', messages=messages)
print(response)
```

##  Parameter Details

- `model (str)`: The name of the AI model to use for text generation. This parameter determines which AI model is used by the `aichat.org` service.
- `messages (Messages)`: A list of messages representing the conversation history. This allows the provider to maintain context in the conversation, making the generated text more relevant.
- `proxy (str, optional)`: A proxy server address for making requests. This parameter allows the provider to use a proxy server for making requests, which can be helpful for bypassing network restrictions or improving privacy.
- `**kwargs`: Additional keyword arguments for customizing the request. This allows for more specific control over the request, such as adjusting the temperature or top_p parameters for influencing the diversity and creativity of the generated text.

##  Examples

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Aichat import Aichat
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Example 1: Basic text generation
messages: Messages = [
    {'role': 'user', 'content': 'What is the meaning of life?'},
]
response = await Aichat.create_async(model='gpt-3.5-turbo', messages=messages)
print(response)

# Example 2: Using a proxy server
messages: Messages = [
    {'role': 'user', 'content': 'What is the capital of France?'},
]
response = await Aichat.create_async(model='gpt-3.5-turbo', messages=messages, proxy='http://myproxy:8080')
print(response)

# Example 3: Adjusting temperature and top_p parameters
messages: Messages = [
    {'role': 'user', 'content': 'Write a short poem about love.'},
]
response = await Aichat.create_async(model='gpt-3.5-turbo', messages=messages, temperature=0.8, top_p=0.9)
print(response)
```