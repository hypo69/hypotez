# ChatGptEs Provider
## Overview

This module implements the `ChatGptEs` class, which provides an asynchronous generator-based interface for interacting with the ChatGPT.es API. It leverages the `curl_cffi` library for handling requests and implements logic for automatically bypassing Cloudflare protection. 

## Details

The `ChatGptEs` class is a subclass of `AsyncGeneratorProvider` and `ProviderModelMixin`, inheriting functionalities for asynchronous generation and model management. The provider uses the ChatGPT.es website for its functionality, sending requests to the specified API endpoint. 

This provider supports streaming responses, enabling users to receive parts of the response as they become available. However, it doesn't support system messages or message history features, meaning conversations are treated independently. 

## Classes

### `ChatGptEs`

**Description**: This class represents the ChatGPT.es provider, handling asynchronous interactions with the ChatGPT.es API.

**Inherits**:
    - `AsyncGeneratorProvider`: Provides asynchronous generation capabilities.
    - `ProviderModelMixin`: Provides functionality for managing supported models.

**Attributes**:
    - `url` (str): The base URL of the ChatGPT.es website.
    - `api_endpoint` (str): The URL of the API endpoint for sending requests.
    - `working` (bool): Indicates whether the provider is operational (True).
    - `supports_stream` (bool): Indicates support for streaming responses (True).
    - `supports_system_message` (bool): Indicates support for system messages (False).
    - `supports_message_history` (bool): Indicates support for message history (False).
    - `default_model` (str): The default model used for communication.
    - `models` (list): A list of supported models.
    - `SYSTEM_PROMPT` (str): A prompt used to set the language context for the model.

**Methods**:
    - `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`: Asynchronously generates responses from the ChatGPT.es API based on the provided model, messages, and optional proxy settings.

## Class Methods

### `create_async_generator`

**Purpose**:  Asynchronously generates responses from the ChatGPT.es API.

**Parameters**:
    - `model` (str): The name of the model to use for communication.
    - `messages` (Messages): A list of messages representing the conversation history.
    - `proxy` (str, optional): An optional proxy server URL. Defaults to `None`.

**Returns**:
    - `AsyncResult`: An asynchronous result object containing the generated responses.

**Raises Exceptions**:
    - `MissingRequirementsError`: Raised if the `curl_cffi` package is not installed.

**How the Function Works**:

1. **Check for `curl_cffi` dependency**:  Ensures that the `curl_cffi` package is installed. If not, raises a `MissingRequirementsError`.
2. **Model selection**: Retrieves the model from the `models` list based on the provided `model` parameter.
3. **Prompt formatting**: Constructs the final prompt by combining the `SYSTEM_PROMPT` with the formatted conversation history.
4. **Session setup**: Creates a `curl_cffi` session with custom headers for Cloudflare bypass. Optionally configures proxy settings.
5. **Initial request**: Sends a GET request to the ChatGPT.es base URL to retrieve necessary data (nonce, post_id).
6. **Nonce extraction**: Extracts the `nonce` value from the response using regular expressions, searching for different potential patterns.
7. **Post ID extraction**:  Extracts the `post_id` from the response using regular expressions.
8. **Data preparation**: Creates a dictionary with data to send to the API endpoint, including the `nonce`, `post_id`, prompt, client ID, and conversation history.
9. **API request**: Sends a POST request to the `api_endpoint` with the prepared data.
10. **Response handling**: Parses the response and yields the generated text if the request was successful. If there are errors, raises an appropriate exception.

**Examples**:

```python
# Example 1: Using the default model with a simple message
messages = [
    {"role": "user", "content": "Hello, how are you?"}
]
async_result = await ChatGptEs.create_async_generator(model="gpt-4o", messages=messages)
for response in async_result:
    print(response)

# Example 2: Using a specific model and specifying a proxy
messages = [
    {"role": "user", "content": "What is the meaning of life?"}
]
async_result = await ChatGptEs.create_async_generator(model="gpt-4", messages=messages, proxy="http://proxy.example.com:8080")
for response in async_result:
    print(response)
```