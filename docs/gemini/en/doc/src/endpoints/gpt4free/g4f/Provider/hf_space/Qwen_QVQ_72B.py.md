# Qwen_QVQ_72B Provider

## Overview

This module provides a class `Qwen_QVQ_72B` which implements a provider for the Qwen QVQ-72B model hosted on Hugging Face Spaces. This provider allows users to interact with the model and receive responses through asynchronous generators.

## Details

The `Qwen_QVQ_72B` class inherits from `AsyncGeneratorProvider` and `ProviderModelMixin`. It defines various attributes and methods for handling requests, sending data, and receiving responses from the Qwen QVQ-72B model.

## Classes

### `class Qwen_QVQ_72B(AsyncGeneratorProvider, ProviderModelMixin)`

**Description**: This class represents a provider for the Qwen QVQ-72B model, allowing users to interact with it via asynchronous generators.

**Inherits**:
- `AsyncGeneratorProvider`: Base class for providers using asynchronous generators.
- `ProviderModelMixin`: Mixin class providing common model-related attributes and methods.

**Attributes**:

- `label`: Specifies the provider's label ("Qwen QVQ-72B").
- `url`: The base URL of the Hugging Face Spaces endpoint ("https://qwen-qvq-72b-preview.hf.space").
- `api_endpoint`: The specific API endpoint for generating responses ("/gradio_api/call/generate").
- `working`: A flag indicating whether the provider is currently working (set to True).
- `default_model`: Default model alias ("qwen-qvq-72b-preview").
- `default_vision_model`: The same as `default_model`.
- `model_aliases`: A dictionary mapping model aliases to their corresponding model names.
- `vision_models`: A list of vision model aliases.
- `models`: A list containing both vision models and model aliases.


**Methods**:

- `create_async_generator(model: str, messages: Messages, media: MediaListType = None, api_key: str = None, proxy: str = None, **kwargs) -> AsyncResult`: This method is the core function for interacting with the Qwen QVQ-72B model. It takes model name, messages, media, API key, and proxy information as input. It then establishes a connection to the Qwen QVQ-72B model on Hugging Face Spaces and returns an asynchronous generator that yields text chunks of the model's response.

## Class Methods

### `create_async_generator(model: str, messages: Messages, media: MediaListType = None, api_key: str = None, proxy: str = None, **kwargs) -> AsyncResult`

**Purpose**: This method is responsible for sending requests to the Qwen QVQ-72B model and receiving responses through an asynchronous generator.

**Parameters**:

- `model` (str): The name of the model to use.
- `messages` (Messages): A list of messages, including user input and previous responses, to send to the model.
- `media` (MediaListType, optional): A list of media files (e.g., images) to be included in the request. Defaults to None.
- `api_key` (str, optional): The API key for authentication. Defaults to None.
- `proxy` (str, optional): Proxy server URL for connecting. Defaults to None.
- `**kwargs`: Additional keyword arguments for the API request.

**Returns**:

- `AsyncResult`: An asynchronous generator that yields text chunks of the model's response.

**Raises Exceptions**:

- `ResponseError`: If the model returns an error response.

**How the Function Works**:

1. The function first sets up headers for the HTTP request, including `Accept` and authorization if an `api_key` is provided.
2. It then creates an asynchronous session with the configured headers.
3. If media is provided, the function uploads the media files to the Hugging Face Spaces endpoint and retrieves the uploaded file's path.
4. The function then constructs the request payload containing messages and the uploaded media path, if applicable.
5. It sends a POST request to the Qwen QVQ-72B model's API endpoint with the prepared data.
6. Upon receiving the response, the function extracts the event ID and establishes a stream connection with the event endpoint.
7. It iterates through the event response's content stream, checking for "event" and "data" chunks.
8. If an "error" event is encountered, it raises a `ResponseError` with the provided error message.
9. If "complete" or "generating" events are detected, the function attempts to parse the data chunk as JSON.
10. If the "generating" event occurs, it yields the generated text chunk.
11. When a "complete" event is received, the function breaks the loop, signifying the end of the response.
12. Finally, the function returns the asynchronous generator for users to iterate through the generated text chunks.

**Examples**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf_space.Qwen_QVQ_72B import Qwen_QVQ_72B
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Send a simple text request
messages = Messages([
    {"role": "user", "content": "Hello, how are you?"}
])
async_generator = await Qwen_QVQ_72B.create_async_generator(model="qwen-qvq-72b-preview", messages=messages)
async for chunk in async_generator:
    print(chunk)

# Send a request with an image
messages = Messages([
    {"role": "user", "content": "Describe this image:"},
    {"role": "user", "content": "https://example.com/image.jpg"}
])
async_generator = await Qwen_QVQ_72B.create_async_generator(model="qwen-qvq-72b-preview", messages=messages)
async for chunk in async_generator:
    print(chunk)
```
```python