# DeepseekAI Janus-Pro-7B Provider Module

## Overview

This module provides the `DeepseekAI_JanusPro7b` class, which implements an asynchronous generator provider for the DeepseekAI Janus-Pro-7B model hosted on Hugging Face Spaces. It utilizes the Hugging Face Spaces API for model interactions, allowing for asynchronous text generation and image generation tasks.

## Details

The `DeepseekAI_JanusPro7b` class leverages the Hugging Face Spaces API to interact with the DeepseekAI Janus-Pro-7B model. The provider supports streaming responses, system messages, and message history, enabling the creation of more interactive and engaging conversational experiences.

## Classes

### `DeepseekAI_JanusPro7b`

**Description**: Класс `DeepseekAI_JanusPro7b` реализует асинхронный генератор провайдера для модели DeepseekAI Janus-Pro-7B, размещенной в Hugging Face Spaces. 

**Inherits**: 
- `AsyncGeneratorProvider`: This base class provides a common structure for asynchronous generators, handling tasks like stream management and response parsing.
- `ProviderModelMixin`: This mixin class adds functionality for model selection, configuration, and related operations.

**Attributes**:
- `label` (str): The display name of the provider.
- `space` (str): The Hugging Face Spaces name of the model.
- `url` (str): The URL of the Hugging Face Space for the model.
- `api_url` (str): The base URL of the API for the model.
- `referer` (str): The referer header used for API requests.
- `working` (bool): Indicates whether the provider is currently functioning.
- `supports_stream` (bool): Indicates whether the provider supports streaming responses.
- `supports_system_message` (bool): Indicates whether the provider supports system messages.
- `supports_message_history` (bool): Indicates whether the provider supports message history.
- `default_model` (str): The default model name for text generation.
- `default_image_model` (str): The default model name for image generation.
- `default_vision_model` (str): The default model name for vision tasks.
- `image_models` (list): A list of image models supported by the provider.
- `vision_models` (list): A list of vision models supported by the provider.
- `models` (list): A combined list of vision and image models.

**Methods**:

#### `run`

**Purpose**: This class method handles the execution of API requests to the Hugging Face Spaces endpoint.

**Parameters**:
- `method` (str): The HTTP method to use for the request (e.g., "post" or "image").
- `session` (StreamSession): The StreamSession object for handling requests.
- `prompt` (str): The user prompt for text generation.
- `conversation` (JsonConversation): The conversation context for the request.
- `image` (dict, optional): Image data to use in the request. Defaults to `None`.
- `seed` (int, optional): Random seed for generation. Defaults to `0`.

**Returns**:
- `StreamResponse`: The API response object.

**How the Function Works**:
- The function constructs the API request URL based on the provided `method` and other parameters.
- It sets the request headers, including necessary authentication tokens and referer information.
- It builds the request body, containing the prompt, seed, and other relevant data.
- Finally, it sends the request using the appropriate HTTP method (POST or GET) and returns the API response.


#### `create_async_generator`

**Purpose**: This class method is the main entry point for generating responses asynchronously. It creates a generator that yields responses as they become available.

**Parameters**:
- `model` (str): The model to use for generation (text or image).
- `messages` (Messages): The list of messages in the conversation.
- `media` (MediaListType, optional): List of media files for the request. Defaults to `None`.
- `prompt` (str, optional): The user prompt for generation. Defaults to `None`.
- `proxy` (str, optional): Proxy server to use for requests. Defaults to `None`.
- `cookies` (Cookies, optional): Cookies to use for authentication. Defaults to `None`.
- `api_key` (str, optional): API key for accessing the model. Defaults to `None`.
- `zerogpu_uuid` (str, optional): The UUID for the user's session. Defaults to "[object Object]".
- `return_conversation` (bool, optional): Whether to return the conversation object as the first yield. Defaults to `False`.
- `conversation` (JsonConversation, optional): The conversation context. Defaults to `None`.
- `seed` (int, optional): Random seed for generation. Defaults to `None`.

**Returns**:
- `AsyncResult`: An asynchronous result object that yields responses.

**How the Function Works**:
- The function first determines the appropriate HTTP method based on the model and the presence of a prompt.
- It formats the prompt for the model and generates a random seed if one isn't provided.
- It obtains a session hash for the request and retrieves the necessary authentication tokens if they are not already provided.
- The function creates a StreamSession for handling asynchronous requests, optionally using a proxy.
- If media files are present, it uploads them to the API and updates the media list with the corresponding file information.
- It then initiates an API request using the `run` method, sending the prompt, seed, and other data.
- The function handles the streaming response from the API, parsing the JSON data and yielding responses as they become available. 
- Responses are yielded as `Reasoning` objects for progress updates or as `ImageResponse` objects for image outputs.

## Inner Functions:

### `get_zerogpu_token`

**Purpose**: This function retrieves the necessary authentication tokens for accessing the Hugging Face Spaces API.

**Parameters**:
- `space` (str): The Hugging Face Spaces name of the model.
- `session` (StreamSession): The StreamSession object for handling requests.
- `conversation` (JsonConversation, optional): The conversation context. Defaults to `None`.
- `cookies` (Cookies, optional): Cookies for authentication. Defaults to `None`.

**Returns**:
- `tuple`: A tuple containing the `zerogpu_uuid` and `zerogpu_token`.

**How the Function Works**:
- If a conversation object is provided, it attempts to retrieve the `zerogpu_uuid` from it.
- The function obtains cookies for authentication and retrieves the `zerogpu_token` from the Hugging Face Spaces website if it's not available.
- It then makes a request to the API endpoint to obtain a new JWT token for authentication.
- Finally, it returns the retrieved `zerogpu_uuid` and `zerogpu_token`. 

## Examples

```python
# Example 1: Generating text using the default model
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf_space.DeepseekAI_JanusPro7b import DeepseekAI_JanusPro7b
async def generate_text():
    provider = DeepseekAI_JanusPro7b()
    async for response in provider.create_async_generator(model="janus-pro-7b", messages=["Hello, world!"]):
        print(response.content)

# Example 2: Generating an image with a prompt
async def generate_image():
    provider = DeepseekAI_JanusPro7b()
    async for response in provider.create_async_generator(model="janus-pro-7b-image", prompt="A beautiful sunset over the ocean"):
        print(response.content)
```
```python
# Example 3: Using media files in the request
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf_space.DeepseekAI_JanusPro7b import DeepseekAI_JanusPro7b
from hypotez.src.image import is_accepted_format, to_bytes
async def generate_text_with_image():
    provider = DeepseekAI_JanusPro7b()
    media = [(to_bytes('path/to/image.jpg'), 'image.jpg')]
    async for response in provider.create_async_generator(model="janus-pro-7b-image", messages=["What is this image?"], media=media):
        print(response.content)
```
```python
# Example 4: Using a custom model with seed
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf_space.DeepseekAI_JanusPro7b import DeepseekAI_JanusPro7b
async def generate_text_with_custom_model_and_seed():
    provider = DeepseekAI_JanusPro7b()
    async for response in provider.create_async_generator(model="janus-pro-7b", messages=["Tell me a story."], seed=12345):
        print(response.content)
```

## Parameter Details:

- `model` (str): The model name to use for generation. Possible values include `janus-pro-7b` for text, `janus-pro-7b-image` for images.
- `messages` (Messages): A list of messages in the conversation, containing the user's prompts and the model's responses.
- `media` (MediaListType): A list of media files, such as images, that can be used in the request.
- `prompt` (str): The user's prompt for generation, which can be used instead of `messages` for a single prompt.
- `proxy` (str): A proxy server address to use for requests.
- `cookies` (Cookies): A dictionary of cookies for authentication.
- `api_key` (str): The API key for accessing the model.
- `zerogpu_uuid` (str): The UUID for the user's session.
- `return_conversation` (bool): Whether to return the conversation object as the first yield.
- `conversation` (JsonConversation): The conversation context object containing information about the current conversation.
- `seed` (int): A random seed for generation, which can be used to control the variability of the responses.


## How the Code Works:

The code defines the `DeepseekAI_JanusPro7b` class, which implements a provider for the DeepseekAI Janus-Pro-7B model hosted on Hugging Face Spaces. The class inherits from `AsyncGeneratorProvider` and `ProviderModelMixin` to provide a common structure for asynchronous generators and model-specific functionality.

The `run` method handles API requests to the Hugging Face Spaces endpoint. It constructs the API request URL, sets the headers (including authentication tokens), builds the request body, and sends the request using the appropriate HTTP method.

The `create_async_generator` method is the main entry point for generating responses asynchronously. It receives parameters such as the model name, conversation messages, and media files, and then initiates an asynchronous API request using the `run` method. It handles the streaming response from the API, parsing the JSON data and yielding responses as they become available.

The `get_zerogpu_token` function retrieves the authentication tokens required for accessing the Hugging Face Spaces API. It obtains cookies from the Hugging Face website, retrieves the `zerogpu_token` and makes a request to the API to obtain a new JWT token for authentication.

Overall, this module provides a robust and easy-to-use mechanism for interacting with the DeepseekAI Janus-Pro-7B model on Hugging Face Spaces, supporting both text and image generation tasks.