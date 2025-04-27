# G4F Provider for Hugging Face Spaces

## Overview

This module provides the `G4F` class, representing a provider for the G4F framework. It handles communication with the G4F Space on Hugging Face and provides functionality for interacting with its models. 

## Details

The `G4F` class inherits from `DeepseekAI_JanusPro7b` and leverages the Hugging Face Spaces infrastructure to execute models, primarily the `flux` model. It supports both text and image generation, and offers various configuration options, including model selection, prompt formatting, and image aspect ratio.

The `G4F` class defines the following attributes:

- **`label`**: "G4F framework"
- **`space`**: "roxky/Janus-Pro-7B"
- **`url`**: "https://huggingface.co/spaces/roxky/g4f-space"
- **`api_url`**: "https://roxky-janus-pro-7b.hf.space"
- **`url_flux`**: "https://roxky-g4f-flux.hf.space/run/predict"
- **`referer`**: f"{api_url}?__theme=light"
- **`default_model`**: "flux"
- **`model_aliases`**: {"flux-schnell": default_model}
- **`image_models`**: [DeepseekAI_JanusPro7b.default_image_model, default_model, "flux-dev", *model_aliases.keys()]
- **`models`**: [DeepseekAI_JanusPro7b.default_model, *image_models]

## Classes

### `class G4F(DeepseekAI_JanusPro7b)`

**Description**: This class represents a provider for the G4F framework, interacting with the G4F Space on Hugging Face.

**Inherits**:  `DeepseekAI_JanusPro7b`

**Attributes**:

- **`label`**: A string identifying the provider.
- **`space`**: The Hugging Face Space name.
- **`url`**: The base URL of the Hugging Face Space.
- **`api_url`**: The URL for API interactions.
- **`url_flux`**: The URL for the FLUX model endpoint.
- **`referer`**: The referer URL for requests.
- **`default_model`**: The default model to use.
- **`model_aliases`**: A dictionary mapping model aliases to their canonical names.
- **`image_models`**: A list of supported image generation models.
- **`models`**: A list of all supported models.

**Methods**:

- **`create_async_generator`**: Asynchronously generates a sequence of responses based on the provided model, messages, and configuration options.

#### `async def create_async_generator(model: str, messages: Messages, proxy: str = None, prompt: str = None, aspect_ratio: str = "1:1", width: int = None, height: int = None, seed: int = None, cookies: dict = None, api_key: str = None, zerogpu_uuid: str = "[object Object]", **kwargs) -> AsyncResult`

**Purpose**: This asynchronous generator method handles the request and response process for the G4F Space model.

**Parameters**:

- **`model` (str)**: The name of the model to use.
- **`messages` (Messages)**: A sequence of messages containing the prompt.
- **`proxy` (str, optional)**: Proxy to use for the requests. Defaults to `None`.
- **`prompt` (str, optional)**: The prompt for the model. Defaults to `None`.
- **`aspect_ratio` (str, optional)**: The aspect ratio for image generation. Defaults to "1:1".
- **`width` (int, optional)**: The desired width for image generation. Defaults to `None`.
- **`height` (int, optional)**: The desired height for image generation. Defaults to `None`.
- **`seed` (int, optional)**: The random seed for image generation. Defaults to `None`.
- **`cookies` (dict, optional)**: A dictionary of cookies to use for the request. Defaults to `None`.
- **`api_key` (str, optional)**: The API key for the Hugging Face Space. Defaults to `None`.
- **`zerogpu_uuid` (str, optional)**: The UUID for the Zero GPU session. Defaults to "[object Object]".
- **`kwargs`**: Additional keyword arguments for the underlying model.

**Returns**:

- **`AsyncResult`**: An asynchronous result object yielding responses as they become available.

**How the Function Works**:

1.  Checks the model and delegates to `FluxDev.create_async_generator` if it's "flux" or "flux-dev".
2.  If the model is not the default, it calls the parent class's `create_async_generator` method.
3.  If it's the default model, the function prepares the prompt and payload, then retrieves a Zero GPU token if needed.
4.  It sends a POST request to the `url_flux` endpoint with the payload and headers containing the API key and UUID.
5.  The function handles the response, extracts the image URL if applicable, and yields a sequence of responses, including reasoning messages and the final image response.

**Examples**:

```python
# Example 1: Generating text using the default model
messages = ["What is the capital of France?"]
async for chunk in G4F.create_async_generator(model="flux", messages=messages):
    print(chunk)

# Example 2: Generating an image with specific dimensions
messages = ["A cat playing with a ball of yarn"]
async for chunk in G4F.create_async_generator(model="flux", messages=messages, width=512, height=512):
    print(chunk)
```