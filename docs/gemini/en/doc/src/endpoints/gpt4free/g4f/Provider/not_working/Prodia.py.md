# Prodia Provider for GPT4Free

## Overview

This module provides the `Prodia` class, an implementation of an asynchronous image generation provider for the `gpt4free` project. It utilizes the Prodia API to generate images based on text prompts. 

The `Prodia` class is designed to be used within the `gpt4free` framework to offer image generation capabilities. It integrates with the `gpt4free` messaging system and provides an asynchronous generator interface for handling image generation tasks. 

## Details

The `Prodia` provider leverages the Prodia API for image generation. It provides a wide range of models, including realistic, stylized, and anime-focused options. Users can customize various generation parameters, including:

- **Model:** Choose from a selection of pre-trained models.
- **Prompt:**  The text description for the desired image.
- **Negative prompt:**  Text describing what should **not** be included in the image.
- **Steps:**  The number of generation steps (higher values can lead to more detailed images).
- **CFG Scale:**  A parameter that controls how closely the generated image adheres to the prompt (higher values can lead to more consistent results but might make the image less creative).
- **Seed:**  A random seed value for controlling the generated image's randomness. 
- **Sampler:**  The algorithm used for image generation, impacting image quality and speed. 
- **Aspect Ratio:**  The desired aspect ratio for the generated image (square, portrait, landscape).

The provider handles asynchronous communication with the Prodia API, polling the job status until the image generation is complete. It returns an `ImageResponse` object containing the generated image URL and a description of the prompt. 

## Classes

### `Prodia`

**Description**: This class represents the Prodia image generation provider.

**Inherits**: 
- `AsyncGeneratorProvider`:  Provides asynchronous image generation functionality. 
- `ProviderModelMixin`:  Offers model selection and management capabilities.

**Attributes**:

- `url`: The base URL of the Prodia website. 
- `api_endpoint`: The endpoint for sending generation requests.
- `working`: A boolean flag indicating whether the provider is currently working.
- `default_model`:  The default model to use if no specific model is provided.
- `default_image_model`:  The default model for image generation.
- `image_models`:  A list of supported models for image generation.
- `models`: A combined list of all supported models.

**Methods**:

#### `get_model(cls, model: str) -> str`: 

**Purpose**: Determines the model to be used for image generation based on the provided model name.

**Parameters**:

- `model` (str): The name of the desired model.

**Returns**:

- `str`:  The model name to be used.

#### `create_async_generator(cls, model: str, messages: Messages, proxy: str = None, negative_prompt: str = "", steps: str = 20, cfg: str = 7, seed: Optional[int] = None, sampler: str = "DPM++ 2M Karras", aspect_ratio: str = "square", **kwargs) -> AsyncResult`: 

**Purpose**:  Creates an asynchronous generator that sends a request to the Prodia API for image generation and yields the generated image response.

**Parameters**:

- `model` (str): The name of the desired model.
- `messages` (Messages):  A list of messages containing the prompt for image generation.
- `proxy` (str, optional):  A proxy server address to use. Defaults to `None`.
- `negative_prompt` (str, optional):  Text describing what should **not** be included in the image. Defaults to "".
- `steps` (str, optional): The number of generation steps (higher values can lead to more detailed images). Defaults to "20".
- `cfg` (str, optional):  A parameter that controls how closely the generated image adheres to the prompt (higher values can lead to more consistent results but might make the image less creative). Defaults to "7".
- `seed` (Optional[int], optional): A random seed value for controlling the generated image's randomness. Defaults to `None`.
- `sampler` (str, optional):  The algorithm used for image generation, impacting image quality and speed. Defaults to "DPM++ 2M Karras".
- `aspect_ratio` (str, optional): The desired aspect ratio for the generated image (square, portrait, landscape). Defaults to "square".
- `**kwargs`: Additional keyword arguments passed to the API request.

**Returns**:

- `AsyncResult`:  An asynchronous result object representing the image generation process.

#### `_poll_job(cls, session: ClientSession, job_id: str, proxy: str, max_attempts: int = 30, delay: int = 2) -> str`:

**Purpose**:  Polls the Prodia API to check the status of a generation job until it completes.

**Parameters**:

- `session` (ClientSession): An `aiohttp` client session for making API requests.
- `job_id` (str): The ID of the generation job.
- `proxy` (str, optional):  A proxy server address to use. Defaults to `None`.
- `max_attempts` (int, optional): The maximum number of attempts to poll the job status. Defaults to 30.
- `delay` (int, optional):  The delay between attempts in seconds. Defaults to 2.

**Returns**:

- `str`:  The URL of the generated image if the job succeeds.

**Raises**:

- `Exception`:  If the generation job fails or times out.

## Inner Functions 
**Inner Functions**:  None

## How the Function Works: 

The `Prodia` class functions as an asynchronous image generation provider.  When a request is made to generate an image, the `create_async_generator` function takes the desired parameters and sends a request to the Prodia API. 

The API responds with a job ID. The `_poll_job` function then continuously checks the status of the job until it completes.  If the job succeeds, it returns the URL of the generated image; otherwise, it raises an exception.

The `create_async_generator` function then yields an `ImageResponse` object containing the generated image URL and a description of the prompt.

## Examples

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.Prodia import Prodia

# Create a Prodia provider instance
provider = Prodia()

# Define a prompt for image generation
prompt = "A beautiful sunset over a calm ocean."

# Generate an image asynchronously
async def generate_image():
    async for image in provider.create_async_generator(model="absolutereality_v181.safetensors [3d9d4d2b]", messages=[{"content": prompt}]):
        print(f"Generated image URL: {image.image_url}")

# Run the asynchronous function
asyncio.run(generate_image())
```