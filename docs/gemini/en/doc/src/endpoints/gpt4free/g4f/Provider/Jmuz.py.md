# Jmuz Provider for GPT4Free

## Overview

This module defines the `Jmuz` class, which acts as a provider for the `gpt4free` endpoint. It utilizes the `OpenaiTemplate` class to interact with the Jmuz.me GPT API.

## Details

The `Jmuz` class extends the `OpenaiTemplate` class and provides a concrete implementation for interacting with the Jmuz.me API. It includes configuration settings for the API, model aliases, and overrides methods for handling asynchronous responses.

## Classes

### `class Jmuz(OpenaiTemplate)`

**Description**: This class defines a provider for the `gpt4free` endpoint, utilizing the `OpenaiTemplate` class for interacting with the Jmuz.me API. 

**Inherits**: `OpenaiTemplate` 

**Attributes**:
- `url` (str): URL for the Jmuz.me Discord server.
- `api_base` (str): Base URL for the Jmuz.me GPT API.
- `api_key` (str): API key for accessing the Jmuz.me API.
- `working` (bool): Indicates whether the provider is currently functional.
- `supports_system_message` (bool): Indicates whether the provider supports system messages.
- `default_model` (str): Default model to use for requests.
- `model_aliases` (dict): Dictionary mapping aliases to their corresponding model names.

**Methods**:

#### `get_models(cls, **kwargs)`

**Purpose**: Retrieves a list of available models from the Jmuz.me API.

**Parameters**:
- `**kwargs`: Optional keyword arguments for the API request.

**Returns**:
- `list`: A list of available models.

**How the Function Works**:
- If the `models` attribute is not already populated, it calls the `get_models` method of the superclass (`OpenaiTemplate`) to fetch the model list from the Jmuz.me API.
- The `api_key` and `api_base` attributes are passed as arguments to the superclass method.
- Returns the fetched list of models.

#### `create_async_generator(cls, model: str, messages: Messages, stream: bool = True, api_key: str = None, **kwargs) -> AsyncResult`

**Purpose**: Creates an asynchronous generator for streaming responses from the Jmuz.me API.

**Parameters**:
- `model` (str): The model to use for the request.
- `messages` (Messages): A list of messages to send to the API.
- `stream` (bool): Flag indicating whether to stream the response. Defaults to `True`.
- `api_key` (str): Optional API key. Defaults to `None`.
- `**kwargs`: Optional keyword arguments for the API request.

**Returns**:
- `AsyncResult`: An asynchronous result object representing the API response.

**How the Function Works**:
- Resolves the model name using the `get_model` method.
- Sets up headers for the API request, including the API key and content type.
- Creates an asynchronous generator using the `create_async_generator` method of the superclass (`OpenaiTemplate`).
- Iterates through the chunks received from the API and filters out unwanted content like "Join for free" prompts and Discord links.
- Yields filtered chunks to the caller, providing a streamlined streaming experience.


## Examples

```python
# Creating a Jmuz provider instance
jmuz_provider = Jmuz()

# Fetching a list of available models
models = jmuz_provider.get_models()

# Creating a message list for the API request
messages = [
    {"role": "user", "content": "Hello, how are you?"}
]

# Sending a request using the asynchronous generator
async for chunk in jmuz_provider.create_async_generator(model="gpt-4o", messages=messages):
    print(chunk)
```

## Parameter Details

- `model` (str):  Model name for the API request, which can be any supported model alias or the full name.
- `messages` (Messages): A list of messages to send to the API, each message should be in the format specified for the API.
- `stream` (bool): A flag indicating whether to stream the response (if the provider supports streaming).
- `api_key` (str):  API key for the Jmuz.me service.

## Examples

```python
# Using the default model
async for chunk in jmuz_provider.create_async_generator(messages=messages):
    print(chunk)

# Using a specific model
async for chunk in jmuz_provider.create_async_generator(model="gemini-pro", messages=messages):
    print(chunk)

# Using a custom API key
async for chunk in jmuz_provider.create_async_generator(messages=messages, api_key="your_api_key"):
    print(chunk)
```