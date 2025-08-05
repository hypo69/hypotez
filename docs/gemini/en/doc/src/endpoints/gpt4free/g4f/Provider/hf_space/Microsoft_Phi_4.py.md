# Microsoft Phi-4 Provider for GPT4Free

## Overview

This module provides an implementation of the `Microsoft_Phi_4` class, which acts as a provider for accessing the Microsoft Phi-4 multimodal language model via the GPT4Free platform. It utilizes the Hugging Face Space API for model interaction. This provider supports both text and image generation, as well as streaming responses and system messages.

## Details

The `Microsoft_Phi_4` class extends the `AsyncGeneratorProvider` and `ProviderModelMixin` classes from the GPT4Free framework. It defines the necessary properties and methods for interacting with the Microsoft Phi-4 model, including:

- **`label`**: Specifies the user-friendly label for the provider ("Microsoft Phi-4").
- **`space`**: Identifies the Hugging Face Space where the model is hosted ("microsoft/phi-4-multimodal").
- **`url`**: Provides the URL of the Hugging Face Space.
- **`api_url`**: Defines the API endpoint for interacting with the model.
- **`referer`**: Sets the referer header used in requests to the API.

The class also defines attributes for supported features:

- **`working`**: Indicates whether the provider is currently functional (set to `True`).
- **`supports_stream`**: Specifies whether streaming responses are supported (set to `True`).
- **`supports_system_message`**: Indicates whether system messages are supported (set to `True`).
- **`supports_message_history`**: Specifies whether message history is supported (set to `True`).

The `Microsoft_Phi_4` class further defines the following attributes for model management:

- **`default_model`**: Specifies the default model used for both text and vision tasks ("phi-4-multimodal").
- **`default_vision_model`**: Specifies the default model for vision tasks.
- **`model_aliases`**: Provides aliases for different model versions.
- **`vision_models`**: Lists the models supported for vision tasks.
- **`models`**: Defines a combined list of all supported models.

## Classes

### `class Microsoft_Phi_4(AsyncGeneratorProvider, ProviderModelMixin)`

**Description**: Represents a provider for accessing the Microsoft Phi-4 multimodal language model via the GPT4Free platform. 

**Inherits**:
- `AsyncGeneratorProvider`: Provides a base class for asynchronous providers that return generators.
- `ProviderModelMixin`: Provides a base class for providers with model selection functionality.

**Attributes**:
- `label`: String representing the user-friendly label for the provider ("Microsoft Phi-4").
- `space`: String representing the Hugging Face Space where the model is hosted ("microsoft/phi-4-multimodal").
- `url`: String representing the URL of the Hugging Face Space.
- `api_url`: String representing the API endpoint for interacting with the model.
- `referer`: String representing the referer header used in requests to the API.
- `working`: Boolean indicating whether the provider is currently functional (set to `True`).
- `supports_stream`: Boolean indicating whether streaming responses are supported (set to `True`).
- `supports_system_message`: Boolean indicating whether system messages are supported (set to `True`).
- `supports_message_history`: Boolean indicating whether message history is supported (set to `True`).
- `default_model`: String representing the default model used for both text and vision tasks ("phi-4-multimodal").
- `default_vision_model`: String representing the default model for vision tasks.
- `model_aliases`: Dictionary mapping model aliases to the actual model names.
- `vision_models`: List of strings representing the models supported for vision tasks.
- `models`: List of strings representing all supported models.

**Methods**:

- `run(method: str, session: StreamSession, prompt: str, conversation: JsonConversation, media: list = None)`: Executes a specific API method (predict, post, or get) using the provided session, prompt, conversation, and media.

- `create_async_generator(model: str, messages: Messages, media: MediaListType = None, prompt: str = None, proxy: str = None, cookies: Cookies = None, api_key: str = None, zerogpu_uuid: str = "[object Object]", return_conversation: bool = False, conversation: JsonConversation = None, **kwargs) -> AsyncResult`: Creates an asynchronous generator that yields responses from the Microsoft Phi-4 model based on the provided input parameters.

## Functions

### `run(method: str, session: StreamSession, prompt: str, conversation: JsonConversation, media: list = None)`

**Purpose**: Executes a specific API method (predict, post, or get) using the provided session, prompt, conversation, and media.

**Parameters**:

- `method` (str): The API method to execute ("predict", "post", or "get").
- `session` (StreamSession): The session object used to execute the request.
- `prompt` (str): The prompt to send to the model.
- `conversation` (JsonConversation): The conversation object containing information about the current session.
- `media` (list, optional): A list of media files to include in the request. Defaults to `None`.

**Returns**:
- StreamResponse: The response object from the API.

**Raises Exceptions**:
- None

**How the Function Works**:

- The function constructs the appropriate API URL based on the specified `method`.
- It assembles the request headers, including necessary authentication tokens and referer information.
- The function then performs the API request (POST or GET) based on the specified `method`.

**Examples**:

- `response = Microsoft_Phi_4.run("predict", session, "What is the meaning of life?", conversation, media)`
- `response = Microsoft_Phi_4.run("post", session, "Tell me a story.", conversation)`
- `response = Microsoft_Phi_4.run("get", session, None, conversation)`

### `create_async_generator(model: str, messages: Messages, media: MediaListType = None, prompt: str = None, proxy: str = None, cookies: Cookies = None, api_key: str = None, zerogpu_uuid: str = "[object Object]", return_conversation: bool = False, conversation: JsonConversation = None, **kwargs) -> AsyncResult`

**Purpose**: Creates an asynchronous generator that yields responses from the Microsoft Phi-4 model based on the provided input parameters.

**Parameters**:

- `model` (str): The specific model to use for the request.
- `messages` (Messages): A list of messages representing the conversation history.
- `media` (MediaListType, optional): A list of media files to include in the request. Defaults to `None`.
- `prompt` (str, optional): The prompt to send to the model. Defaults to `None`.
- `proxy` (str, optional): The proxy to use for the request. Defaults to `None`.
- `cookies` (Cookies, optional): Cookies to include in the request. Defaults to `None`.
- `api_key` (str, optional): The API key for authentication. Defaults to `None`.
- `zerogpu_uuid` (str, optional): The zerogpu UUID for authentication. Defaults to "[object Object]".
- `return_conversation` (bool, optional): Whether to return the conversation object as the first element in the generator. Defaults to `False`.
- `conversation` (JsonConversation, optional): The conversation object containing information about the current session. Defaults to `None`.

**Returns**:
- AsyncResult: An asynchronous result object that yields responses from the model.

**Raises Exceptions**:
- None

**How the Function Works**:

- The function prepares the prompt for the model by formatting it based on the conversation history and provided prompt.
- It creates a unique session hash if a conversation object is not provided.
- The function initializes a StreamSession object with the specified proxy and impersonation settings.
- It obtains a valid API key and zerogpu UUID if not provided.
- If `return_conversation` is set to `True`, the function yields the conversation object.
- The function processes any media files by uploading them to the API and retrieving the corresponding file paths.
- It then executes the `predict` API method to send the prompt and receive an initial response.
- The function executes the `post` API method to send the formatted message history and media data.
- It then executes the `get` API method to retrieve streamed responses from the API endpoint.
- The generator yields each received response as a string until the `process_completed` signal is received.

**Examples**:

- `async for response in Microsoft_Phi_4.create_async_generator(model="phi-4", messages=[{"role": "user", "content": "Hello"}], media=[("image.jpg", "image.jpg")]):`
- `async for response in Microsoft_Phi_4.create_async_generator(model="phi-4", prompt="What is the capital of France?", conversation=conversation):`

## Parameter Details

- `model` (str): The specific model to use for the request. This can be one of the supported models listed in `vision_models` or `models`.
- `messages` (Messages): A list of messages representing the conversation history. Each message is a dictionary with the following structure:

```json
{
  "role": "user" | "assistant" | "system",
  "content": str | dict
}
```

- `media` (MediaListType): A list of media files to include in the request. Each media item is a tuple containing the file path (str or Path) and the original filename (str).

- `prompt` (str): The prompt to send to the model. 

- `proxy` (str): The proxy to use for the request. This is a string representing the proxy URL.

- `cookies` (Cookies): Cookies to include in the request. This can be a dictionary or a list of tuples.

- `api_key` (str): The API key for authentication. This key is required for accessing the Microsoft Phi-4 model.

- `zerogpu_uuid` (str): The zerogpu UUID for authentication. This is used to identify the user and session.

- `return_conversation` (bool): Whether to return the conversation object as the first element in the generator.

- `conversation` (JsonConversation): The conversation object containing information about the current session. This includes the session hash, zerogpu token, and zerogpu UUID.

## Examples

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf_space.Microsoft_Phi_4 import Microsoft_Phi_4
from hypotez.src.endpoints.gpt4free.g4f.Provider.response import JsonConversation

# Example 1: Generating text with a simple prompt
async def example1():
    async for response in Microsoft_Phi_4.create_async_generator(model="phi-4-multimodal", prompt="What is the meaning of life?"):
        print(response)

# Example 2: Generating text with a prompt and conversation history
async def example2():
    conversation = JsonConversation(session_hash="your_session_hash", zerogpu_token="your_api_key", zerogpu_uuid="your_zerogpu_uuid")
    messages = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"},
    ]
    async for response in Microsoft_Phi_4.create_async_generator(model="phi-4-multimodal", messages=messages, prompt="Tell me a joke"):
        print(response)

# Example 3: Generating an image with a prompt
async def example3():
    async for response in Microsoft_Phi_4.create_async_generator(model="phi-4-multimodal", prompt="Generate an image of a cat"):
        print(response)

# Example 4: Generating text with a prompt and image
async def example4():
    async for response in Microsoft_Phi_4.create_async_generator(model="phi-4-multimodal", prompt="Describe this image:", media=[("image.jpg", "image.jpg")]):
        print(response)
```
```python