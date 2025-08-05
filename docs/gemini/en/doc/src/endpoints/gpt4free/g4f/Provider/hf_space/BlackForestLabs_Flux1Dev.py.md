# BlackForestLabs_Flux1Dev Provider

## Overview

This module provides the `BlackForestLabs_Flux1Dev` class, which implements an asynchronous generator provider for the BlackForestLabs Flux-1-Dev model hosted on Hugging Face Spaces. 

## Details

This provider utilizes the Hugging Face Spaces API to interact with the Flux-1-Dev model for generating images based on provided prompts. It handles sending prompts, receiving streaming responses, and parsing the results into a user-friendly format.

## Classes

### `class BlackForestLabs_Flux1Dev(AsyncGeneratorProvider, ProviderModelMixin)`

**Description**: This class represents the BlackForestLabs Flux-1-Dev provider for image generation. It inherits from `AsyncGeneratorProvider` for asynchronous streaming responses and `ProviderModelMixin` for model-related functionality.

**Inherits**:
    - `AsyncGeneratorProvider`: Enables asynchronous generation of image previews and results during the image generation process.
    - `ProviderModelMixin`: Provides common methods and attributes related to handling models, such as aliases, default models, and model lists.

**Attributes**:
    - `label`: A descriptive label for the provider, "BlackForestLabs Flux-1-Dev".
    - `url`: The base URL of the Hugging Face Space hosting the model, "https://black-forest-labs-flux-1-dev.hf.space".
    - `space`: The Hugging Face Space name, "black-forest-labs/FLUX.1-dev".
    - `referer`: The URL used as a referer header for requests, "https://black-forest-labs-flux-1-dev.hf.space/?__theme=light".
    - `working`: Boolean flag indicating the provider's status. True indicates that the provider is operational.
    - `default_model`: The default model name, "black-forest-labs-flux-1-dev".
    - `default_image_model`: The default model name for image generation, "black-forest-labs-flux-1-dev".
    - `model_aliases`: A dictionary mapping aliases to model names, {"flux-dev": "black-forest-labs-flux-1-dev", "flux": "black-forest-labs-flux-1-dev"}.
    - `image_models`: A list of image model names, ["flux-dev", "flux"].
    - `models`: A list of model names, which includes image models.

**Methods**:

#### `run(method: str, session: StreamSession, conversation: JsonConversation, data: list = None)`

**Purpose**: This class method handles HTTP requests to the Hugging Face Space API. It sends POST requests to join the queue and GET requests to retrieve streaming data.

**Parameters**:
    - `method` (str): The HTTP method to use, either "post" or "get".
    - `session` (`StreamSession`): An instance of `StreamSession` for handling asynchronous requests.
    - `conversation` (`JsonConversation`): Contains conversation-specific information, including the zerogpu token, UUID, and session hash.
    - `data` (list, optional): Data to be sent in the request body for POST requests. Defaults to `None`.

**Returns**:
    - `StreamSession.post` or `StreamSession.get`: Returns the response object for the corresponding HTTP request.

**Raises Exceptions**:
    - `None`

#### `create_async_generator(model: str, messages: Messages, prompt: str = None, proxy: str = None, aspect_ratio: str = "1:1", width: int = None, height: int = None, guidance_scale: float = 3.5, num_inference_steps: int = 28, seed: int = 0, randomize_seed: bool = True, cookies: dict = None, api_key: str = None, zerogpu_uuid: str = "[object Object]", **kwargs) -> AsyncResult`

**Purpose**: This class method creates an asynchronous generator to handle the image generation process. It sends the prompt to the model, manages streaming responses, and parses the results.

**Parameters**:
    - `model` (str): The model name to use.
    - `messages` (`Messages`): Contains the conversation history.
    - `prompt` (str, optional): The prompt to use for image generation. Defaults to `None`.
    - `proxy` (str, optional): Proxy URL to use for requests. Defaults to `None`.
    - `aspect_ratio` (str, optional): Aspect ratio of the generated image. Defaults to "1:1".
    - `width` (int, optional): Desired width of the generated image. Defaults to `None`.
    - `height` (int, optional): Desired height of the generated image. Defaults to `None`.
    - `guidance_scale` (float, optional): Guidance scale for image generation. Defaults to 3.5.
    - `num_inference_steps` (int, optional): Number of inference steps for image generation. Defaults to 28.
    - `seed` (int, optional): Random seed for image generation. Defaults to 0.
    - `randomize_seed` (bool, optional): Whether to randomize the seed for image generation. Defaults to `True`.
    - `cookies` (dict, optional): Cookies to use for requests. Defaults to `None`.
    - `api_key` (str, optional): API key for the Hugging Face Space. Defaults to `None`.
    - `zerogpu_uuid` (str, optional): Unique identifier for the user session. Defaults to "[object Object]".

**Returns**:
    - `AsyncResult`: An asynchronous result object representing the ongoing image generation process.

**Raises Exceptions**:
    - `RuntimeError`: Raised if there are errors parsing messages from the streaming response.

**Inner Functions**:
    - `None`

**How the Function Works**:

1. **Initialization**:
   - Creates a `StreamSession` with specified proxy settings.
   - Formats the prompt using `format_image_prompt`.
   - Uses `use_aspect_ratio` to handle image dimensions.
   - Creates a `JsonConversation` object for storing conversation-specific data.
   - Retrieves a zeroGPU token if necessary using `get_zerogpu_token`.

2. **Request**:
   - Sends a POST request to join the generation queue with the formatted data.
   - Retrieves the `event_id` from the response to identify the specific generation process.

3. **Streaming Response**:
   - Sends a GET request to retrieve streaming data.
   - Iterates through the streaming response lines.

4. **Parsing**:
   - Decodes the received JSON data.
   - Parses progress messages, image previews, and generation status updates.
   - Raises `ResponseError` if an error is encountered during generation.

5. **Result**:
   - Yields the final generated image.
   - Closes the stream session.

**Examples**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf_space.BlackForestLabs_Flux1Dev import BlackForestLabs_Flux1Dev
from hypotez.src.endpoints.gpt4free.g4f.requests import StreamSession
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

async def generate_image(prompt: str, messages: Messages):
  provider = BlackForestLabs_Flux1Dev()
  async with StreamSession(impersonate="chrome") as session:
    async for result in provider.create_async_generator(messages=messages, prompt=prompt, session=session):
      # Process the generated image preview or result
      print(result)