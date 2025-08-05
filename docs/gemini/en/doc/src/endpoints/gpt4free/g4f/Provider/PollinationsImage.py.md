# PollinationsImage Provider for GPT4Free

## Overview

This module provides the `PollinationsImage` class, a provider for generating images using the Pollinations AI platform. It extends the `PollinationsAI` class, adding specialized functionality for image generation, such as prompt formatting, model selection, and parameter control. This provider allows GPT4Free to utilize the powerful image generation capabilities of Pollinations.

## Details

The `PollinationsImage` provider utilizes the `PollinationsAI` base class for communication with the Pollinations API. It specifically focuses on image generation, providing an interface for users to specify prompts, models, and image generation parameters. The provider dynamically retrieves available models from the Pollinations API, allowing users to select from a wide range of image generation models.

## Classes

### `PollinationsImage`

**Description**: This class provides an interface for generating images using the Pollinations AI platform. It extends the `PollinationsAI` class, adding specialized functionality for image generation.

**Inherits**: `PollinationsAI`

**Attributes**:

- `label` (str): Label identifying the provider as "PollinationsImage".
- `default_model` (str): Default model for image generation, set to "flux".
- `default_vision_model` (str): Not used in this provider.
- `default_image_model` (str): Alias for `default_model`.
- `image_models` (list): A list of supported image generation models.
- `_models_loaded` (bool): Flag indicating whether models have been loaded.

**Methods**:

- `get_models(**kwargs)`: Retrieves a list of supported image generation models from the Pollinations API.
- `create_async_generator(model: str, messages: Messages, proxy: str = None, prompt: str = None, aspect_ratio: str = "1:1", width: int = None, height: int = None, seed: Optional[int] = None, cache: bool = False, nologo: bool = True, private: bool = False, enhance: bool = False, safe: bool = False, n: int = 4, **kwargs) -> AsyncResult`: Creates an asynchronous generator for generating images based on the provided parameters.

### `create_async_generator`

**Purpose**: Generates an asynchronous generator for creating images.

**Parameters**:

- `model` (str): The model to use for image generation.
- `messages` (Messages): A list of messages containing prompts for the image.
- `proxy` (str, optional): Proxy server address. Defaults to `None`.
- `prompt` (str, optional): Additional prompt for the image. Defaults to `None`.
- `aspect_ratio` (str, optional): Aspect ratio of the generated image. Defaults to "1:1".
- `width` (int, optional): Width of the generated image. Defaults to `None`.
- `height` (int, optional): Height of the generated image. Defaults to `None`.
- `seed` (Optional[int], optional): Random seed for image generation. Defaults to `None`.
- `cache` (bool, optional): Whether to cache the generated image. Defaults to `False`.
- `nologo` (bool, optional): Whether to remove the Pollinations logo from the image. Defaults to `True`.
- `private` (bool, optional): Whether the image should be private. Defaults to `False`.
- `enhance` (bool, optional): Whether to enhance the image using upscaling. Defaults to `False`.
- `safe` (bool, optional): Whether to apply safe mode for image generation. Defaults to `False`.
- `n` (int, optional): The number of images to generate. Defaults to 4.
- `**kwargs`: Additional keyword arguments for the `PollinationsAI` base class.

**Returns**:

- `AsyncResult`: An asynchronous result object representing the generated image.

**Raises Exceptions**:

- `Exception`: If an error occurs during image generation.

**How the Function Works**:

1. Calls `get_models()` to ensure the list of available models is up-to-date.
2. Formats the prompt using the `format_image_prompt()` helper function.
3. Starts an asynchronous generator that yields image chunks as they are generated.
4. Uses the `_generate_image()` method from the parent class to handle the actual image generation process.
5. Passes all provided parameters, including the formatted prompt and model name, to `_generate_image()`.

**Examples**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider import PollinationsImage

provider = PollinationsImage()

# Example 1: Generating an image with a simple prompt
async for chunk in provider.create_async_generator(model="flux", messages=[{"role": "user", "content": "A cat wearing a hat"}], n=1):
    # Process the image chunks as they are generated
    print(f"Chunk: {chunk}")

# Example 2: Generating images with specific parameters
async for chunk in provider.create_async_generator(model="flux", messages=[{"role": "user", "content": "A futuristic cityscape"}], width=512, height=512, n=2):
    # Process the image chunks
    print(f"Chunk: {chunk}")
```

## Inner Functions

### `_generate_image`

**Purpose**: This method is inherited from the parent class and handles the actual image generation process using the Pollinations API. It is responsible for sending requests to the API, receiving image data, and streaming the results.

**Parameters**:

- `model` (str): The model to use for image generation.
- `prompt` (str): The prompt for the image.
- `proxy` (str, optional): Proxy server address. Defaults to `None`.
- `aspect_ratio` (str, optional): Aspect ratio of the generated image. Defaults to "1:1".
- `width` (int, optional): Width of the generated image. Defaults to `None`.
- `height` (int, optional): Height of the generated image. Defaults to `None`.
- `seed` (Optional[int], optional): Random seed for image generation. Defaults to `None`.
- `cache` (bool, optional): Whether to cache the generated image. Defaults to `False`.
- `nologo` (bool, optional): Whether to remove the Pollinations logo from the image. Defaults to `True`.
- `private` (bool, optional): Whether the image should be private. Defaults to `False`.
- `enhance` (bool, optional): Whether to enhance the image using upscaling. Defaults to `False`.
- `safe` (bool, optional): Whether to apply safe mode for image generation. Defaults to `False`.
- `n` (int, optional): The number of images to generate. Defaults to 4.

**Returns**:

- `AsyncResult`: An asynchronous result object representing the generated image.

**Raises Exceptions**:

- `Exception`: If an error occurs during image generation.

## Parameter Details

- `model` (str): The specific image generation model to use.
- `messages` (Messages): A list of messages containing prompts for the image generation. The provider will use the last user message as the main prompt.
- `proxy` (str, optional): A proxy server address to use for connecting to the Pollinations API.
- `prompt` (str, optional): An additional prompt for the image generation. This prompt will be concatenated with the last user message in the `messages` list.
- `aspect_ratio` (str, optional): The desired aspect ratio for the generated image. For example, "1:1" for a square image or "16:9" for a widescreen image.
- `width` (int, optional): The desired width of the generated image in pixels.
- `height` (int, optional): The desired height of the generated image in pixels.
- `seed` (Optional[int], optional): A random seed to use for image generation. This allows for reproducing the same image with the same seed and prompt.
- `cache` (bool, optional): Whether to cache the generated image for future retrieval. This can speed up subsequent generations of the same image.
- `nologo` (bool, optional): Whether to remove the Pollinations logo from the generated image.
- `private` (bool, optional): Whether the generated image should be marked as private. This restricts access to the image.
- `enhance` (bool, optional): Whether to enhance the generated image using upscaling. This can improve image quality.
- `safe` (bool, optional): Whether to apply safe mode for image generation. This can help filter out potentially offensive or inappropriate content.
- `n` (int, optional): The number of images to generate. This allows for generating multiple variations of the image based on the same prompt.

## Examples

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider import PollinationsImage

provider = PollinationsImage()

# Example 1: Generating an image with a simple prompt
async for chunk in provider.create_async_generator(model="flux", messages=[{"role": "user", "content": "A cat wearing a hat"}], n=1):
    # Process the image chunks as they are generated
    print(f"Chunk: {chunk}")

# Example 2: Generating images with specific parameters
async for chunk in provider.create_async_generator(model="flux", messages=[{"role": "user", "content": "A futuristic cityscape"}], width=512, height=512, n=2):
    # Process the image chunks
    print(f"Chunk: {chunk}")
```