# ImageLabs Provider

## Overview

The module contains the `ImageLabs` class, which is a provider for generating images using the ImageLabs API. This class provides functionality for interacting with the API, handling requests, and processing responses.

## Details

The `ImageLabs` class is designed to work with the ImageLabs API, which allows generating images from text prompts. It handles all the necessary steps for generating images, including constructing requests, handling responses, and providing the generated images.

## Classes

### `ImageLabs`

**Description**: This class provides a wrapper for interacting with the ImageLabs API. It offers methods for generating images from prompts.

**Inherits**:
- `AsyncGeneratorProvider`: Base class for asynchronous generators that provide data.
- `ProviderModelMixin`: Mixin class providing model-related functionality.

**Attributes**:

- `url` (str): The base URL of the ImageLabs API.
- `api_endpoint` (str): The specific endpoint for image generation.
- `working` (bool): Indicates whether the provider is currently functioning.
- `supports_stream` (bool):  Indicates whether the provider supports streaming data.
- `supports_system_message` (bool): Indicates whether the provider supports system messages.
- `supports_message_history` (bool): Indicates whether the provider supports message history.
- `default_model` (str): The default model for image generation.
- `default_image_model` (str): The default image model (same as `default_model`).
- `image_models` (list):  A list of supported image models.
- `models` (list): Alias for `image_models`.

**Methods**:

#### `create_async_generator`

**Purpose**: This method creates an asynchronous generator for generating images.

**Parameters**:

- `model` (str): The model to use for image generation.
- `messages` (Messages): A list of messages, the last one containing the prompt.
- `proxy` (str, optional):  A proxy server to use for requests. Defaults to `None`.
- `prompt` (str, optional): The prompt to use for image generation. Defaults to the content of the last message if not specified.
- `negative_prompt` (str, optional):  Negative prompt for guiding the generation process. Defaults to "".
- `width` (int, optional): The desired width of the generated image. Defaults to 1152.
- `height` (int, optional): The desired height of the generated image. Defaults to 896.
- `**kwargs`:  Additional keyword arguments passed to the API.

**Returns**:

- `AsyncResult`: An asynchronous result containing a generator that yields `ImageResponse` objects.

**Raises**:

- `Exception`: If an error occurs during the generation process.

**How the Function Works**:

1. **Setup**: The function sets up the request headers for the API call.
2. **Prompt Processing**: If no `prompt` is provided, it extracts the prompt from the last message in the `messages` list.
3. **API Call**: It constructs a payload with parameters for the image generation request and sends it to the ImageLabs API.
4. **Task ID**: It retrieves the `task_id` from the API response.
5. **Progress Polling**: The function enters a loop, periodically polling the API for progress updates.
6. **Progress Check**: It checks the status of the image generation task.
7. **Yield Image Response**: If the generation is completed, the function yields an `ImageResponse` object with the final image URL.
8. **Error Handling**: If the API response indicates an error, the function raises an exception.

#### `get_model`

**Purpose**: This method returns the default model for the provider.

**Parameters**:

- `model` (str): The requested model.

**Returns**:

- `str`: The default model string.

**How the Function Works**:

The function simply returns the `default_model` attribute, which is always set to `sdxl-turbo`.