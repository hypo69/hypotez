# StabilityAI_SD35Large Provider

## Overview

This module defines the `StabilityAI_SD35Large` class, which is a provider for generating images using the StabilityAI SD-3.5-Large model hosted on Hugging Face Spaces. 

## Details

The provider leverages the Hugging Face Spaces API to interact with the model and generate images based on user prompts. 

## Classes

### `class StabilityAI_SD35Large(AsyncGeneratorProvider, ProviderModelMixin)`

**Description**: This class represents a provider for the StabilityAI SD-3.5-Large model. It inherits from `AsyncGeneratorProvider` and `ProviderModelMixin`, which define common functionalities for image generation providers.

**Attributes**:

- `label` (str): The label of the provider, which is "StabilityAI SD-3.5-Large".
- `url` (str): The base URL for the Hugging Face Space hosting the StabilityAI SD-3.5-Large model.
- `api_endpoint` (str): The API endpoint for interacting with the model.
- `working` (bool): Indicates whether the provider is currently functional (True).
- `default_model` (str): The default model name for the provider.
- `default_image_model` (str): The default image model name (same as `default_model`).
- `model_aliases` (dict): A dictionary mapping model aliases to their actual names.
- `image_models` (list): A list of image model names supported by the provider.
- `models` (list): A list of supported models (same as `image_models`).

**Methods**:

### `create_async_generator(model: str, messages: Messages, prompt: str = None, negative_prompt: str = None, api_key: str = None, proxy: str = None, aspect_ratio: str = "1:1", width: int = None, height: int = None, guidance_scale: float = 4.5, num_inference_steps: int = 50, seed: int = 0, randomize_seed: bool = True, **kwargs) -> AsyncResult`

**Purpose**: This method creates an asynchronous generator for generating images using the StabilityAI SD-3.5-Large model.

**Parameters**:

- `model` (str): The name of the model to use for image generation.
- `messages` (Messages): A list of messages containing the prompt for image generation.
- `prompt` (str, optional): The prompt for image generation. Defaults to None.
- `negative_prompt` (str, optional): The negative prompt for image generation. Defaults to None.
- `api_key` (str, optional): The API key for accessing the Hugging Face Spaces API. Defaults to None.
- `proxy` (str, optional): The proxy to use for making API requests. Defaults to None.
- `aspect_ratio` (str, optional): The aspect ratio for the generated image. Defaults to "1:1".
- `width` (int, optional): The width of the generated image. Defaults to None.
- `height` (int, optional): The height of the generated image. Defaults to None.
- `guidance_scale` (float, optional): The guidance scale for image generation. Defaults to 4.5.
- `num_inference_steps` (int, optional): The number of inference steps for image generation. Defaults to 50.
- `seed` (int, optional): The random seed for image generation. Defaults to 0.
- `randomize_seed` (bool, optional): Whether to randomize the seed for each image generation. Defaults to True.
- `**kwargs`: Additional keyword arguments.

**Returns**:

- `AsyncResult`: An asynchronous result object that represents the image generation process.

**Raises**:

- `ResponseError`: If there's an error with the API response, such as a GPU token limit being exceeded.
- `RuntimeError`: If there's a problem parsing the image URL from the API response.

**How the Function Works**:

The `create_async_generator` function:

1. Constructs the API request headers, including the API key if provided.
2. Formats the image prompt using the messages provided.
3. Defines the image dimensions based on the specified aspect ratio, width, and height.
4. Sends a POST request to the Hugging Face Spaces API with the formatted prompt and image dimensions.
5. Waits for the API response and extracts the event ID.
6. Makes a GET request to the API to track the image generation process.
7. Continuously checks the response for events, such as "generating" or "complete".
8. For "generating" events, it yields an `ImagePreview` object with the image URL.
9. For "complete" events, it yields an `ImageResponse` object with the image URL and breaks the loop.
10. Handles potential errors like GPU token limit exceeding and parsing failures.

**Example**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf_space.StabilityAI_SD35Large import StabilityAI_SD35Large

# Creating a provider instance
provider = StabilityAI_SD35Large()

# Generating an image
async for image in provider.create_async_generator(
    model='stabilityai-stable-diffusion-3-5-large',
    messages=['Generate an image of a cat playing the piano.'],
):
    # Process the image (e.g., download, display)
    print(f"Image URL: {image.url}")