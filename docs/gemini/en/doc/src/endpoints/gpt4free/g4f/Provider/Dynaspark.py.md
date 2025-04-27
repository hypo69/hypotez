# Dynaspark Provider Module

## Overview

This module provides a Python class, `Dynaspark`, that implements an asynchronous generator for interacting with the Dynaspark API for generating text and processing images using AI models. It inherits from the `AsyncGeneratorProvider` and `ProviderModelMixin` base classes, ensuring compatibility with the `hypotez` project's framework for AI model interactions.

## Details

The `Dynaspark` class leverages the Dynaspark API, which offers a range of AI models, including Gemini-based models, for text generation and image processing tasks. This provider allows you to integrate these models seamlessly into your projects, enabling you to perform various tasks like:

- Generating creative text formats (stories, poems, scripts, etc.).
- Translating text into different languages.
- Summarizing and analyzing text content.
- Processing and understanding images.

## Classes

### `Dynaspark`

**Description**: 
- An asynchronous generator provider for interacting with the Dynaspark API. 
- Enables the use of AI models for text generation, image processing, and more.

**Inherits**:
- `AsyncGeneratorProvider`:  Provides an asynchronous generator framework for retrieving data from the API.
- `ProviderModelMixin`: Implements common model-related functionalities, such as setting model defaults, aliases, and managing model-specific parameters.

**Attributes**:

- `url` (str): The base URL of the Dynaspark API.
- `login_url` (None):  No login URL required for this provider.
- `api_endpoint` (str):  The endpoint of the Dynaspark API for generating responses.
- `working` (bool): Indicates whether the provider is currently active.
- `needs_auth` (bool):  Determines if authentication is required to use the provider.
- `use_nodriver` (bool):  Specifies whether a web driver is required for interaction.
- `supports_stream` (bool):  Indicates if the provider supports streaming responses.
- `supports_system_message` (bool):  Indicates if the provider supports system messages.
- `supports_message_history` (bool):  Indicates if the provider supports message history.
- `default_model` (str): The default model for text generation.
- `default_vision_model` (str): The default model for image processing.
- `vision_models` (list):  A list of available vision models.
- `models` (list): A list of available models for both text and vision.
- `model_aliases` (dict):  A dictionary mapping model aliases to their actual names.

**Methods**:

#### `create_async_generator(model: str, messages: Messages, proxy: str = None, media: MediaListType = None, **kwargs) -> AsyncResult`

**Purpose**: 
- Initializes an asynchronous generator for retrieving responses from the Dynaspark API.
- This method sets up a connection to the API and configures the necessary parameters for generating responses.

**Parameters**:

- `model` (str): The AI model to be used.
- `messages` (Messages):  A list of messages containing the user input and context.
- `proxy` (str, optional): A proxy server to be used for API requests. Defaults to None.
- `media` (MediaListType, optional): A list of media items (e.g., images) to be processed. Defaults to None.
- `**kwargs`:  Additional keyword arguments for customizing requests.

**Returns**:

- `AsyncResult`: An asynchronous generator that yields text responses from the Dynaspark API.

**How the Method Works**:

1.  Creates an `aiohttp` session with the specified headers for communication with the Dynaspark API.
2.  Constructs a `FormData` object to send the model, messages, and optional media data to the API.
3.  If media is provided, it encodes the image and adds it to the `FormData` object.
4.  Sends a POST request to the Dynaspark API endpoint.
5.  Handles response status codes, raising an error if necessary.
6.  Yields the response text from the API.

**Example**:

```python
async def generate_response(model: str, messages: list) -> str:
    """
    Example function that uses the Dynaspark provider to generate text from the API.

    Args:
        model (str): The AI model to be used.
        messages (list): A list of messages for the AI model.

    Returns:
        str: The generated text response from the API.

    """

    provider = Dynaspark()
    async for response in provider.create_async_generator(model, messages):
        return response

```

## Parameter Details

- `model` (str):  The name of the AI model to use for generation. For example, `gemini-1.5-flash`, `gemini-1.5-flash-8b`, `gemini-2.0-flash`, `gemini-2.0-flash-lite`.
- `messages` (Messages):  A list of messages that represent the conversation history and the user's input.
- `proxy` (str): A proxy server address, if needed.
- `media` (MediaListType): A list of media items to process, such as images.

## Examples

```python
from src.endpoints.gpt4free.g4f.Provider.Dynaspark import Dynaspark
from src.endpoints.gpt4free.g4f.typing import Messages

async def main():
    """
    Example of using the Dynaspark provider.
    """

    provider = Dynaspark()
    messages: Messages = [
        {"role": "user", "content": "Hello, how are you?"},
    ]

    # Generate text using the default model
    async for response in provider.create_async_generator(provider.default_model, messages):
        print(response)

    # Generate text using a specific model
    async for response in provider.create_async_generator("gemini-1.5-flash-8b", messages):
        print(response)

    # Process an image using a vision model
    image_path = "path/to/image.jpg"  # Replace with your image path
    media = [(image_path, "image.jpg")]  # Assuming the image is JPEG
    async for response in provider.create_async_generator(provider.default_vision_model, messages, media=media):
        print(response)

```
```python