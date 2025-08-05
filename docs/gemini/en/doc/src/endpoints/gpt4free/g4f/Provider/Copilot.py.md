# Microsoft Copilot Provider for GPT4Free

## Overview

The `Copilot.py` file defines a provider class for using Microsoft Copilot (also known as GitHub Copilot) in the GPT4Free framework. This provider allows users to interact with the Copilot AI model for code completion, code generation, and other coding tasks.

## Details

The `Copilot` class implements the `AbstractProvider` interface, providing the necessary methods for handling requests to the Copilot API. It leverages the `curl_cffi` library for making HTTP requests, and it includes functionality for managing access tokens, cookies, and conversation state.

## Classes

### `class Conversation`

**Description**: Represents a conversation with Copilot, storing the conversation ID.

**Attributes**:

- `conversation_id` (str): Unique identifier for the conversation.

**Methods**:

- `__init__(self, conversation_id: str)`: Initializes a new conversation with the specified ID.

### `class Copilot`

**Description**: Provider class for interacting with Microsoft Copilot.

**Inherits**:

- `AbstractProvider`: Defines basic methods for all GPT4Free providers.
- `ProviderModelMixin`: Provides functionality for model selection and alias handling.

**Attributes**:

- `label` (str): Human-readable name of the provider ("Microsoft Copilot").
- `url` (str): Base URL for the Copilot API.
- `working` (bool): Indicates whether the provider is currently functional (`True`).
- `supports_stream` (bool): Indicates whether the provider supports streaming responses (`True`).
- `default_model` (str): Default Copilot model to use ("Copilot").
- `models` (list): List of supported Copilot models.
- `model_aliases` (dict): Mapping of model aliases to actual model names.
- `websocket_url` (str): URL for the Copilot websocket API.
- `conversation_url` (str): URL for creating new conversations.
- `_access_token` (str): The access token for the Copilot API (stored as a class attribute).
- `_cookies` (dict): The cookies associated with the Copilot API (stored as a class attribute).

**Methods**:

- `create_completion(cls, model: str, messages: Messages, stream: bool = False, proxy: str = None, timeout: int = 900, prompt: str = None, media: MediaListType = None, conversation: BaseConversation = None, return_conversation: bool = False, api_key: str = None, **kwargs) -> CreateResult`: Sends a completion request to Copilot.
    - **Purpose**: Sends a prompt to the Copilot model and receives a response.
    - **Parameters**:
        - `model` (str): The Copilot model to use (e.g., "Copilot", "Think Deeper").
        - `messages` (Messages): List of messages in the conversation.
        - `stream` (bool, optional): Whether to stream the response. Defaults to `False`.
        - `proxy` (str, optional): Proxy server to use for requests. Defaults to `None`.
        - `timeout` (int, optional): Timeout for the request in seconds. Defaults to 900.
        - `prompt` (str, optional): Prompt to send to the model. Defaults to `None`.
        - `media` (MediaListType, optional): List of media files to upload. Defaults to `None`.
        - `conversation` (BaseConversation, optional): Existing conversation object to use. Defaults to `None`.
        - `return_conversation` (bool, optional): Whether to return the conversation object. Defaults to `False`.
        - `api_key` (str, optional): API key to use for authentication. Defaults to `None`.
    - **Returns**:
        - `CreateResult`: A generator that yields responses from the Copilot model.
    - **Raises Exceptions**:
        - `MissingRequirementsError`: If the `curl_cffi` package is not installed.
        - `NoValidHarFileError`: If no valid HAR file is found for authentication.
        - `MissingAuthError`: If the access token is invalid.
        - `RuntimeError`: If the response from Copilot is invalid.

- `get_model(cls, model: str) -> str`: Retrieves the actual model name based on an alias.
    - **Purpose**: Handles model aliases to ensure consistent model names are used.
    - **Parameters**:
        - `model` (str): The model name or alias.
    - **Returns**:
        - `str`: The actual model name.

## Inner Functions

### `async def get_access_token_and_cookies(url: str, proxy: str = None, target: str = "ChatAI",)`

- **Purpose**: Extracts the access token and cookies from the user's browser data (using `nodriver`).
- **Parameters**:
    - `url` (str): The URL of the Copilot website.
    - `proxy` (str, optional): Proxy server to use for requests. Defaults to `None`.
    - `target` (str, optional): The target for the access token. Defaults to "ChatAI".
- **Returns**:
    - `tuple`: A tuple containing the access token and cookies.
- **How the Function Works**:
    - Uses `nodriver` to launch a browser instance and navigate to the Copilot website.
    - Extracts the access token from the browser's local storage.
    - Retrieves cookies from the browser's network settings.

### `def readHAR(url: str)`

- **Purpose**: Extracts the access token and cookies from a HAR file.
- **Parameters**:
    - `url` (str): The URL of the Copilot website.
- **Returns**:
    - `tuple`: A tuple containing the access token and cookies.
- **How the Function Works**:
    - Iterates through HAR files in the specified directory.
    - Parses each HAR file to find requests matching the Copilot URL.
    - Extracts the access token and cookies from the matching request.

### `def get_clarity() -> bytes`

- **Purpose**: Generates a clarity token for tracking user behavior.
- **Returns**:
    - `bytes`: The clarity token data.
- **How the Function Works**:
    - Decodes a base64 encoded string to generate the clarity token.

## Examples

```python
# Creating a driver instance (example with Chrome)
driver = Driver(Chrome)

# Example of a request to Copilot (using `create_completion`)
response = Copilot.create_completion(model='Copilot', messages=[{'role': 'user', 'content': 'Write a function that reverses a string.'}])

# Iterate through responses
for part in response:
    print(part)

```

## Additional Notes

- The `Copilot` provider relies on authentication through HAR files or by using a browser instance with `nodriver`.
- The provider includes support for streaming responses and media uploads.
- The `get_clarity()` function generates a clarity token for tracking user behavior, but it is not currently used in the code.
- The `Copilot` class includes a `model_aliases` dictionary for mapping common model names to their actual names.
- The code includes extensive logging using the `src.logger` module for debugging purposes.
- The `Copilot` provider utilizes the `src.webdirver` module for interacting with the browser.
- The code is structured to allow for seamless integration with the `hypotez` framework.