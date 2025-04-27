# You.com Provider

## Overview

This module implements the `You` class, a provider for interacting with the You.com API. It allows users to send messages to various AI models available on the platform and receive responses. The `You` class handles model selection, prompt formatting, and communication with the API.

## Details

The `You` class utilizes the `StreamSession` from `src.requests` to establish a persistent connection with the You.com API. This class also implements the `AsyncGeneratorProvider` and `ProviderModelMixin` interfaces, providing support for asynchronous generation and model management.

### Classes

#### `class You(AsyncGeneratorProvider, ProviderModelMixin)`

**Description**: The `You` class provides methods for interacting with the You.com API. It inherits from `AsyncGeneratorProvider` and `ProviderModelMixin`, enabling asynchronous generation of responses and model selection.

**Inherits**:
 - `AsyncGeneratorProvider`: Handles asynchronous generation of responses.
 - `ProviderModelMixin`: Manages and selects AI models for communication.

**Attributes**:
 - `label` (str): The name of the provider, "You.com".
 - `url` (str): The base URL for the You.com API.
 - `working` (bool): Indicates if the provider is functional.
 - `default_model` (str): The default model for text-based communication.
 - `default_vision_model` (str): The default model for image-related tasks.
 - `image_models` (list): A list of models supporting image generation.
 - `models` (list): A list of all available models on the You.com platform.
 - `_cookies` (Cookies): A dictionary containing cookies for the API.
 - `_cookies_used` (int): Tracks the number of times cookies have been used.
 - `_telemetry_ids` (list): Stores telemetry identifiers.

**Methods**:
 - `create_async_generator(model: str, messages: Messages, stream: bool = True, image: ImageType = None, image_name: str = None, proxy: str = None, timeout: int = 240, chat_mode: str = "default", cookies: Cookies = None, **kwargs) -> AsyncResult`: Asynchronously sends messages to the You.com API and returns a generator for retrieving responses.
 - `upload_file(client: StreamSession, cookies: Cookies, file: bytes, filename: str = None) -> dict`: Uploads an image file to the You.com API and returns information about the upload.

**Principle of Operation**: 
 - The `You` class utilizes the `StreamSession` to establish a connection with the You.com API, enabling streaming responses.
 - The `create_async_generator` method takes input messages, an optional image, and a desired model, formats the prompt, and sends it to the API.
 - The `upload_file` method uploads an image file to the API, retrieving details about the upload for use in prompt formatting.
 - The `get_model` method dynamically retrieves available models from the You.com API based on the user's preferences.

**Examples**:

```python
# Creating a You provider instance
you_provider = You()

# Sending a message using the default model
messages = [
    {"role": "user", "content": "Hello, how are you?"}
]
async_result = await you_provider.create_async_generator(messages=messages)

# Iterating through the response
async for response in async_result:
    print(response)
```

### Methods

#### `create_async_generator(model: str, messages: Messages, stream: bool = True, image: ImageType = None, image_name: str = None, proxy: str = None, timeout: int = 240, chat_mode: str = "default", cookies: Cookies = None, **kwargs) -> AsyncResult`

**Purpose**: Asynchronously sends messages to the You.com API and returns a generator for receiving responses.

**Parameters**:
 - `model` (str): The AI model to use for communication.
 - `messages` (Messages): A list of messages containing user input and previous responses.
 - `stream` (bool, optional): Indicates if responses should be streamed. Defaults to `True`.
 - `image` (ImageType, optional): An image to be processed by the model. Defaults to `None`.
 - `image_name` (str, optional): The name of the image file. Defaults to `None`.
 - `proxy` (str, optional): A proxy server address for connecting to the API. Defaults to `None`.
 - `timeout` (int, optional): The maximum timeout in seconds for connecting to the API. Defaults to `240`.
 - `chat_mode` (str, optional): Specifies the chat mode for interaction with the model. Defaults to "default".
 - `cookies` (Cookies, optional): A dictionary of cookies for authenticating with the You.com API. Defaults to `None`.

**Returns**:
 - `AsyncResult`: An asynchronous result that represents the ongoing communication with the You.com API.

**Raises Exceptions**:
 - `ResponseError`: If the API returns an error response.

**How the Function Works**: 
 - The function first determines the chat mode based on the provided model and image.
 - It retrieves cookies if they are not provided, attempting to load them from a local file or retrieving them from the browser.
 - It uploads the image file to the You.com API if provided.
 - It constructs the request data, including the formatted prompt, chat mode, and model.
 - It initiates a GET request to the You.com API with the prepared data.
 - It iterates through the streaming response, extracting event and data components.
 - It handles error events and yields responses, including text, image previews, and image data.

**Examples**:

```python
# Sending a message using the default model
messages = [
    {"role": "user", "content": "Hello, how are you?"}
]
async_result = await you_provider.create_async_generator(messages=messages)

# Sending a message with an image
image_path = "path/to/image.jpg"
image = ImageType(path=image_path, content_type="image/jpeg")
async_result = await you_provider.create_async_generator(messages=messages, image=image)

# Sending a message using a specific model
async_result = await you_provider.create_async_generator(messages=messages, model="gpt-4o")
```

#### `upload_file(client: StreamSession, cookies: Cookies, file: bytes, filename: str = None) -> dict`

**Purpose**: Uploads an image file to the You.com API and retrieves information about the upload.

**Parameters**:
 - `client` (StreamSession): The HTTP client for connecting to the API.
 - `cookies` (Cookies): A dictionary of cookies for authentication.
 - `file` (bytes): The image file data.
 - `filename` (str, optional): The name of the image file. Defaults to `None`.

**Returns**:
 - `dict`: A dictionary containing information about the uploaded file, including its name, size, and unique identifier.

**Raises Exceptions**:
 - `ResponseError`: If the API returns an error response.

**How the Function Works**:
 - The function retrieves a nonce value from the You.com API for secure file upload.
 - It creates a FormData object and adds the image file data.
 - It sends a POST request to the upload endpoint, providing the nonce, cookies, and file data.
 - It retrieves the response from the API and parses it as JSON data.
 - It returns a dictionary containing information about the uploaded file.

**Examples**:

```python
# Uploading an image
image_path = "path/to/image.jpg"
with open(image_path, "rb") as f:
    image_data = f.read()
upload_info = await you_provider.upload_file(client, cookies, image_data)
print(upload_info)
```