# Ollama Provider

## Overview

This module provides the `Ollama` class, which implements the `OpenaiAPI` interface for interacting with the Ollama language model. It allows users to send messages to the Ollama model and receive responses. 

## Details

The `Ollama` class is designed to work with the Ollama API, providing a simplified interface for sending messages and receiving responses. It handles the necessary configuration, authentication, and API calls to interact with the Ollama model. 

## Classes

### `class Ollama(OpenaiAPI)`

**Description**: This class provides an interface for interacting with the Ollama language model. It inherits from the `OpenaiAPI` class and implements the necessary methods for sending messages and receiving responses.

**Inherits**: `OpenaiAPI`

**Attributes**:
- `label` (str): The label for the provider, which is "Ollama" in this case.
- `url` (str): The base URL of the Ollama API.
- `login_url` (None): The login URL for the provider, which is `None` as Ollama does not require authentication.
- `needs_auth` (bool): Indicates whether the provider requires authentication. Set to `False` for Ollama.
- `working` (bool): Indicates whether the provider is currently working. Set to `True` for Ollama.

**Methods**:
- `get_models(api_base: str = None, **kwargs)`: Retrieves a list of available Ollama models.
    - **Args**:
        - `api_base` (str): Optional base URL for the API. If `None`, uses environment variables `OLLAMA_HOST` and `OLLAMA_PORT`.
        - `**kwargs`: Additional keyword arguments.
    - **Returns**: A list of available Ollama models.
- `create_async_generator(model: str, messages: Messages, api_base: str = None, **kwargs) -> AsyncResult`: Creates an asynchronous generator for interacting with the Ollama model.
    - **Args**:
        - `model` (str): The name of the Ollama model to use.
        - `messages` (Messages): A list of messages to be sent to the model.
        - `api_base` (str): Optional base URL for the API. If `None`, uses environment variables `OLLAMA_HOST` and `OLLAMA_PORT`.
        - `**kwargs`: Additional keyword arguments.
    - **Returns**: An asynchronous result object.

## Inner Functions

### `get_models(cls, api_base: str = None, **kwargs)`

**Purpose**:  The function retrieves a list of available Ollama models.

**Parameters**:
- `api_base` (str): Optional base URL for the API. If `None`, uses environment variables `OLLAMA_HOST` and `OLLAMA_PORT`.
- `**kwargs`: Additional keyword arguments.

**Returns**: A list of available Ollama models.

**How the Function Works**:
1. The function first checks if the `models` attribute is empty. If it is, it proceeds to retrieve the models.
2. If `api_base` is `None`, it uses environment variables `OLLAMA_HOST` and `OLLAMA_PORT` to construct the API URL. Otherwise, it uses the provided `api_base` with the appropriate path.
3. The function sends a GET request to the API endpoint to retrieve the list of models.
4. The response is parsed as JSON, and the model names are extracted from the `models` field.
5. The extracted model names are stored in the `models` attribute and the first model is set as the default.
6. The function returns the list of available Ollama models.

### `create_async_generator(cls, model: str, messages: Messages, api_base: str = None, **kwargs) -> AsyncResult`

**Purpose**: Creates an asynchronous generator for interacting with the Ollama model.

**Parameters**:
- `model` (str): The name of the Ollama model to use.
- `messages` (Messages): A list of messages to be sent to the model.
- `api_base` (str): Optional base URL for the API. If `None`, uses environment variables `OLLAMA_HOST` and `OLLAMA_PORT`.
- `**kwargs`: Additional keyword arguments.

**Returns**: An asynchronous result object.

**How the Function Works**:
1. The function first checks if `api_base` is `None`. If it is, it uses environment variables `OLLAMA_HOST` and `OLLAMA_PORT` to construct the base URL.
2. The function calls the `create_async_generator` method of the parent class (`OpenaiAPI`) to initiate the asynchronous interaction with the model.
3. It passes the provided `model`, `messages`, and `api_base` to the parent class method.
4. The parent class method handles the asynchronous communication with the model and returns an asynchronous result object.
5. This result object allows the user to access the response from the model asynchronously.

## Parameter Details

- `model` (str):  The name of the Ollama model to be used for the request.
- `messages` (Messages):  A list of messages to be sent to the model. Each message is represented as a dictionary.
- `api_base` (str): The base URL of the API. If `None`, defaults to `http://localhost:11434/v1`.
- `**kwargs`: Additional keyword arguments that may be specific to the Ollama API.

## Examples

**Example of retrieving Ollama models:**

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.local.Ollama import Ollama

models = Ollama.get_models()
print(models) 
```

**Example of sending a message to Ollama:**

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.local.Ollama import Ollama
from hypotez.src.endpoints.gpt4free.g4f.Provider.local.Ollama import Messages

messages: Messages = [
    {"role": "user", "content": "Hello, world!"},
]

response = Ollama.create_async_generator(
    model="Ollama", messages=messages
).get_response()

print(response)
```