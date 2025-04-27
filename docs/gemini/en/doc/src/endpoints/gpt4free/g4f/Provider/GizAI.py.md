# GizAI Provider Module
## Overview

This module implements the `GizAI` class, which is a provider for the `hypotez` project, designed to interact with the GizAI chatbot API for generating text.

## Details

The `GizAI` provider leverages the GizAI chatbot API to generate responses based on user input. It provides functionalities for:

- Establishing communication with the GizAI API.
- Sending user messages and receiving responses.
- Handling API responses and potential errors.

## Classes

### `GizAI`

**Description**: This class implements a provider for the GizAI chatbot API, enabling the use of the `chat-gemini-flash` model for text generation. 

**Inherits**: 
- `AsyncGeneratorProvider`: Provides functionalities for asynchronous generation of text responses.
- `ProviderModelMixin`: Offers capabilities for managing and selecting models.

**Attributes**:
- `url (str)`: Base URL for accessing the GizAI web application.
- `api_endpoint (str)`:  Endpoint URL for interacting with the API for inference.
- `working (bool)`: Indicates whether the provider is operational.
- `supports_stream (bool)`: Specifies if the provider supports streaming of responses.
- `supports_system_message (bool)`: Determines if the provider supports system messages.
- `supports_message_history (bool)`: Indicates if the provider supports maintaining message history.
- `default_model (str)`: The default model used by the provider.
- `models (list)`:  A list of supported models.
- `model_aliases (dict)`:  A dictionary mapping model aliases to their corresponding names.

**Methods**:
- `get_model(cls, model: str) -> str`: Retrieves the appropriate model name from the `models` list or `model_aliases` dictionary.
- `create_async_generator(cls, model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`: Creates an asynchronous generator that yields responses from the GizAI API based on the provided model, messages, and optional proxy settings.

#### `get_model`

**Purpose**: This class method determines the correct model name to use based on the input `model` parameter. 

**Parameters**:
- `model (str)`: The desired model name.

**Returns**:
- `str`: The validated model name to use.

**How the Method Works**:
- Checks if the input `model` is present in the `models` list. If found, returns the model name.
- If the `model` is not found in `models`, it searches for a matching alias in the `model_aliases` dictionary. If found, it returns the corresponding model name.
- If neither a match in `models` nor `model_aliases` is found, it returns the default model name stored in `default_model`.

**Example**:
```python
>>> GizAI.get_model("chat-gemini-flash")
'chat-gemini-flash'

>>> GizAI.get_model("gemini-1.5-flash")
'chat-gemini-flash'

>>> GizAI.get_model("invalid_model")
'chat-gemini-flash' 
```

#### `create_async_generator`

**Purpose**: This class method initiates an asynchronous generator that interacts with the GizAI API to obtain responses based on the input messages and selected model.

**Parameters**:
- `model (str)`: The name of the model to use for text generation.
- `messages (Messages)`: A list of messages containing user and system messages.
- `proxy (str, optional)`: A proxy server address for network communication. Defaults to `None`.

**Returns**:
- `AsyncResult`: An asynchronous generator that yields text responses from the GizAI API.

**Raises Exceptions**:
- `Exception`: If an unexpected response status is received from the GizAI API.

**How the Method Works**:
- It retrieves the correct model name using the `get_model` class method.
- It constructs a dictionary (`data`) containing the selected model, input messages, and other relevant information.
- It uses `aiohttp` to establish an asynchronous HTTP session with the necessary headers.
- It sends a POST request to the API endpoint with the formatted `data` and optional proxy configuration.
- If the response status is 201 (Created), the method retrieves the JSON data from the response, extracts the generated text, and yields it through the asynchronous generator.
- If the response status is not 201, it raises an exception with details about the unexpected response.

**Example**:
```python
>>> async def main():
...     gizai = GizAI()
...     messages = [
...         {"role": "user", "content": "Hello, how are you?"},
...         {"role": "assistant", "content": "I am doing well, thank you. How can I help you today?"},
...     ]
...     async for response in gizai.create_async_generator(model="chat-gemini-flash", messages=messages):
...         print(response)
...