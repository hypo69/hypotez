# GigaChat Provider

## Overview

This module implements the `GigaChat` class, an asynchronous provider for the GigaChat API. It extends the `AsyncGeneratorProvider` and `ProviderModelMixin` classes and handles authentication, message history, system messages, streaming, and model selection.

## Details

The `GigaChat` provider utilizes Sberbank's GigaChat API to interact with the GigaChat language models. It requires an API key for authentication, and it leverages a custom certificate (`russian_trusted_root_ca.crt`) to establish a secure connection with the API endpoint.

## Classes

### `class GigaChat(AsyncGeneratorProvider, ProviderModelMixin)`

**Description**: This class implements the GigaChat provider for interacting with the GigaChat API.

**Inherits**:
    - `AsyncGeneratorProvider`: Provides the foundation for asynchronous generation of responses.
    - `ProviderModelMixin`: Adds model-related functionality, including model selection and version management.

**Attributes**:
    - `url (str)`: The base URL for the GigaChat API.
    - `working (bool)`: Indicates whether the provider is currently functional.
    - `supports_message_history (bool)`: Specifies whether the provider supports message history.
    - `supports_system_message (bool)`: Indicates whether the provider supports system messages.
    - `supports_stream (bool)`: Specifies whether the provider supports streaming responses.
    - `needs_auth (bool)`: Indicates whether the provider requires authentication.
    - `default_model (str)`: The default GigaChat model.
    - `models (list)`: A list of available GigaChat models.

**Methods**:

    - `create_async_generator(model: str, messages: Messages, stream: bool = True, proxy: str = None, api_key: str = None, connector: BaseConnector = None, scope: str = "GIGACHAT_API_PERS", update_interval: float = 0, **kwargs) -> AsyncResult`

#### `create_async_generator(model: str, messages: Messages, stream: bool = True, proxy: str = None, api_key: str = None, connector: BaseConnector = None, scope: str = "GIGACHAT_API_PERS", update_interval: float = 0, **kwargs) -> AsyncResult`

**Purpose**: This method creates an asynchronous generator for interacting with the GigaChat API. It handles authentication, model selection, and stream management.

**Parameters**:

    - `model (str)`: The GigaChat model to use.
    - `messages (Messages)`: A list of messages representing the conversation history.
    - `stream (bool)`: Indicates whether to stream responses. Defaults to `True`.
    - `proxy (str)`: An optional proxy server to use. Defaults to `None`.
    - `api_key (str)`: The API key for authentication.
    - `connector (BaseConnector)`: An optional connector for the HTTP client. Defaults to `None`.
    - `scope (str)`: The OAuth2 scope for authorization. Defaults to `"GIGACHAT_API_PERS"`.
    - `update_interval (float)`: The interval in seconds for checking for new responses during streaming. Defaults to `0`.
    - `**kwargs`: Additional keyword arguments.

**Returns**:

    - `AsyncResult`: An asynchronous result object representing the response from the GigaChat API.

**Raises Exceptions**:

    - `MissingAuthError`: If the API key is missing.

**How the Function Works**:

1. **Authentication**:
    - Checks if the access token is expired.
    - If expired, performs OAuth2 authentication using the provided API key and retrieves a new access token.
2. **API Request**:
    - Sends a POST request to the GigaChat API endpoint.
    - Includes the access token, model name, messages, stream flag, and other parameters in the request body.
3. **Response Handling**:
    - If streaming is enabled:
        - Iterates over the response lines.
        - Parses each line as JSON.
        - Yields the content of the received message.
        - Returns when the response is complete.
    - If streaming is disabled:
        - Yields the complete response content.
        - Returns.

**Examples**:

```python
from ...typing import Messages

# Example messages for the conversation history
messages: Messages = [
    {"role": "user", "content": "Hello, GigaChat! How are you doing today?"},
    {"role": "assistant", "content": "I am doing well, thank you for asking! How can I help you today?"}
]

# Example usage of the GigaChat provider with streaming enabled
async for response in GigaChat.create_async_generator(model="GigaChat:latest", messages=messages, api_key="YOUR_API_KEY"):
    print(response)

# Example usage of the GigaChat provider with streaming disabled
response = await GigaChat.create_async_generator(model="GigaChat:latest", messages=messages, stream=False, api_key="YOUR_API_KEY")
print(response)
```

**Inner Functions**:

None

## Parameter Details

- `model (str)`: The name of the GigaChat model to use. Available models are:
    - `"GigaChat:latest"` (default)
    - `"GigaChat-Plus"`
    - `"GigaChat-Pro"`
- `messages (Messages)`: A list of messages representing the conversation history. Each message is a dictionary with the following keys:
    - `role (str)`: The role of the speaker (e.g., "user", "assistant").
    - `content (str)`: The text content of the message.
- `stream (bool)`: Indicates whether to stream responses. If `True`, the generator will yield each message part as it arrives. If `False`, the generator will yield the complete response once it is available.
- `proxy (str)`: An optional proxy server to use. If specified, the HTTP client will use this proxy to access the GigaChat API.
- `api_key (str)`: The API key for authentication. This key is required to access the GigaChat API.
- `connector (BaseConnector)`: An optional connector for the HTTP client. If not provided, a default `TCPConnector` will be used.
- `scope (str)`: The OAuth2 scope for authorization. This scope defines the permissions granted to the application when authenticating with the GigaChat API.
- `update_interval (float)`: The interval in seconds for checking for new responses during streaming. If set to `0`, the client will wait indefinitely for the next message part.

## Examples

- See the "Examples" section in the `create_async_generator` method.

```python