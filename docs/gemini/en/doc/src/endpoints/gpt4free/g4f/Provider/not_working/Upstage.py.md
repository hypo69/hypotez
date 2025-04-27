# Upstage Provider

## Overview

This module provides the `Upstage` class, which acts as a provider for the Upstage AI model, enabling interaction with the Upstage API for text generation and other language-based tasks.

## Details

The `Upstage` class extends the `AsyncGeneratorProvider` and `ProviderModelMixin` base classes, offering an asynchronous generator-based interface for communication with the Upstage API. This provider supports various Upstage models, allowing you to choose the most suitable model for your needs.

## Classes

### `Upstage`

**Description**: This class provides access to the Upstage AI model via the Upstage API, supporting asynchronous generation of text and handling various models.

**Inherits**: 
- `AsyncGeneratorProvider`: Provides an asynchronous generator-based interface for interacting with the model.
- `ProviderModelMixin`: Handles model selection and related operations.

**Attributes**:
- `url (str)`: The base URL for the Upstage playground.
- `api_endpoint (str)`: The URL for the Upstage API endpoint.
- `working (bool)`: Indicates whether the provider is currently working.
- `default_model (str)`: The default Upstage model to use.
- `models (List[str])`: A list of supported Upstage models.
- `model_aliases (dict)`: A dictionary mapping model aliases to their corresponding names.

**Methods**:
- `get_model(model: str) -> str`: Retrieves the correct model name based on the provided input.
- `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`: Creates an asynchronous generator for generating responses from the Upstage model.

## Class Methods

### `get_model(model: str) -> str`

**Purpose**: This method checks if the provided `model` is a valid model name. If not, it returns the default model name.

**Parameters**:
- `model (str)`: The name of the Upstage model.

**Returns**:
- `str`: The valid model name, or the default model if the provided name is invalid.

**How the Function Works**:
- The method first checks if the provided `model` is present in the `models` list. If found, it returns the same model name.
- If the model is not found in the `models` list, the method checks if the `model` exists in the `model_aliases` dictionary. If a matching alias is found, the method returns the corresponding model name.
- If neither the model name nor its alias is found, the method returns the default model name defined by the `default_model` attribute.

**Examples**:
- `Upstage.get_model('upstage/solar-1-mini-chat')` returns `'upstage/solar-1-mini-chat'`.
- `Upstage.get_model('solar-mini')` returns `'upstage/solar-1-mini-chat'`.
- `Upstage.get_model('unknown_model')` returns `'solar-pro'`, the default model.

### `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`

**Purpose**: This method creates an asynchronous generator for generating responses from the Upstage model based on provided messages and model selection.

**Parameters**:
- `model (str)`: The name of the Upstage model to use for generation.
- `messages (Messages)`: A list of messages to be sent to the model as input.
- `proxy (str, optional)`: A proxy server to use for the API request. Defaults to `None`.

**Returns**:
- `AsyncResult`: An asynchronous result object that represents the response from the Upstage API.

**How the Function Works**:
- The method first obtains the correct model name using the `get_model` method.
- It then constructs a dictionary containing the necessary request data, including the selected `model`, `messages` formatted for the prompt, and `stream` set to `True` for continuous output.
- The method initiates an asynchronous POST request to the Upstage API endpoint using an `aiohttp.ClientSession`. The request includes the constructed data, headers for API communication, and optional `proxy` information.
- The method waits for the response, ensuring the response status is valid.
- It iterates through the response's content line by line, decoding and extracting the content from the `choices` list.
- If `content` is found, it's appended to the `response_text` variable and yielded to the generator for real-time output.
- The loop continues until a "data: [DONE]" line indicates the end of the response stream.

**Examples**:
```python
# Example with a basic message
messages = [{"role": "user", "content": "Hello, how are you?"}]
async_generator = await Upstage.create_async_generator(model='solar-pro', messages=messages)
async for content in async_generator:
    print(content)

# Example with a more complex prompt using format_prompt
messages = [
    {"role": "user", "content": "What are the key benefits of using Upstage AI?"},
    {"role": "assistant", "content": "Upstage AI offers ..."},
]
async_generator = await Upstage.create_async_generator(model='solar-mini', messages=messages)
async for content in async_generator:
    print(content)
```