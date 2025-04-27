# EasyChat Provider

## Overview

This module provides the `EasyChat` class, a deprecated provider for interacting with the EasyChat API. It utilizes requests to send and receive data from the API, handling both stream and non-stream responses.  

## Details

The `EasyChat` class is a subclass of `AbstractProvider`, which defines the basic interface for interacting with different chat providers. However, the `EasyChat` provider is marked as deprecated and no longer actively maintained. It is recommended to use alternative providers like `FastGPT` instead.

## Classes

### `class EasyChat`

**Description**: 
A deprecated provider for interacting with the EasyChat API. 

**Inherits**: 
`AbstractProvider`

**Attributes**: 
- `url (str)`: The base URL for the EasyChat API.
- `supports_stream (bool)`: Indicates whether the provider supports stream responses.
- `supports_gpt_35_turbo (bool)`: Indicates whether the provider supports the `gpt-3.5-turbo` model.
- `working (bool)`: Indicates whether the provider is currently functional.

**Methods**: 
- `create_completion(model: str, messages: list[dict[str, str]], stream: bool, **kwargs: Any) -> CreateResult`:
   - **Purpose**: Sends a chat completion request to the EasyChat API and handles the response.
   - **Parameters**: 
     - `model (str)`: The model to use for completion.
     - `messages (list[dict[str, str]])`: A list of messages for the chat context.
     - `stream (bool)`: Whether to stream the response or receive it as a single chunk.
     - `**kwargs (Any)`: Additional keyword arguments for customization (e.g., `temperature`, `presence_penalty`).
   - **Returns**: 
     - `CreateResult`: An object containing the chat completion result or an error message.
   - **Raises**:
     - `Exception`: If there is an error communicating with the API or processing the response.

## Functions

### `create_completion`

**Purpose**: 
This function sends a chat completion request to the EasyChat API, handles the response, and yields the generated content, either in streamed or non-streamed form.  

**Parameters**:
- `model (str)`: The model to use for completion.
- `messages (list[dict[str, str]])`: A list of messages for the chat context.
- `stream (bool)`: Whether to stream the response or receive it as a single chunk.
- `**kwargs (Any)`: Additional keyword arguments for customization (e.g., `temperature`, `presence_penalty`).

**Returns**:
- `CreateResult`: An object containing the chat completion result or an error message.

**Raises Exceptions**:
- `Exception`: If there is an error communicating with the API or processing the response.

**How the Function Works**:
1.  **Select a server**: Randomly chooses a server from a list of available EasyChat servers.
2.  **Construct headers**: Sets up HTTP headers for the request, including authorization, language, content type, and user agent information.
3.  **Prepare JSON data**: Constructs a JSON payload containing the chat context, model, stream flag, and optional parameters like temperature, presence penalty, and frequency penalty.
4.  **Initialize a requests session**: Creates a `requests.Session` object to manage cookies and maintain a persistent connection.
5.  **Send the request**: Uses the session to send a POST request to the selected EasyChat server's `/api/openai/v1/chat/completions` endpoint.
6.  **Handle the response**:
    - **Non-streaming**: If `stream` is `False`, retrieves the entire response as JSON, extracts the content from the `choices` list, and yields it.
    - **Streaming**: If `stream` is `True`, iterates over the response's lines, looking for lines with `content`. Parses the content, extracts the generated text, and yields it.
7.  **Raise an exception**: If the API request fails or returns an unexpected response, raises an exception.

**Example**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.EasyChat import EasyChat

# Example usage:
model = "gpt-3.5-turbo"  # Or another supported model
messages = [
    {"role": "user", "content": "Hello, how are you?"},
    {"role": "assistant", "content": "I am doing well, thanks for asking!"},
]
stream = True

try:
    # Create the EasyChat provider instance:
    provider = EasyChat()

    # Send the chat completion request and receive the response:
    for response in provider.create_completion(model=model, messages=messages, stream=stream):
        print(response)  # Output each generated text chunk

except Exception as ex:
    print(f"Error: {ex}")