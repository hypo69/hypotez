# Base Provider 
## Overview
This module defines the base class for all GPT4Free providers, which provides a common interface for interacting with different GPT4Free models. It also defines several utility functions used by providers for handling parameters, creating completions, and managing authentication.

## Details
The core functionality is implemented in the `AbstractProvider` class, which defines abstract methods for creating completions and retrieving parameters. This class is further extended by `AsyncProvider` and `AsyncGeneratorProvider` for asynchronous completion creation and asynchronous generator support, respectively. The `ProviderModelMixin` and `RaiseErrorMixin` classes provide functionality for managing models and handling errors, respectively.

This module plays a crucial role in the `hypotez` project by defining the foundation for interacting with different GPT4Free models. It ensures that all providers adhere to a consistent interface and provides mechanisms for managing essential parameters, including the `model`, `messages`, `stream`, and `timeout` parameters.

## Classes
### `AbstractProvider`
**Description**: Abstract base class for all GPT4Free providers.
**Attributes**:
  - `supports_stream` (bool):  Indicates whether the provider supports streaming responses.
**Methods**:
  - `create_completion(model: str, messages: Messages, stream: bool, **kwargs) -> CreateResult`: Abstract method for creating a completion with the given parameters.
  - `create_async(model: str, messages: Messages, *timeout: int = None, loop: AbstractEventLoop = None, executor: ThreadPoolExecutor = None, **kwargs) -> str`: Asynchronously creates a result based on the given model and messages.
  - `get_create_function() -> callable`: Returns the callable function used for creating completions.
  - `get_async_create_function() -> callable`: Returns the callable function used for creating asynchronous completions.
  - `get_parameters(as_json: bool = False) -> dict[str, Parameter]`: Returns the parameters supported by the provider.
  - `params`: Returns the parameters supported by the provider as a string.

### `AsyncProvider`
**Description**: Provides asynchronous functionality for creating completions.
**Attributes**:
  - `supports_stream` (bool):  Indicates whether the provider supports streaming responses.
**Methods**:
  - `create_completion(model: str, messages: Messages, stream: bool = False, **kwargs) -> CreateResult`: Creates a completion result synchronously.
  - `create_async(model: str, messages: Messages, **kwargs) -> str`: Abstract method for creating asynchronous results.
  - `get_create_function() -> callable`: Returns the callable function used for creating completions.
  - `get_async_create_function() -> callable`: Returns the callable function used for creating asynchronous completions.

### `AsyncGeneratorProvider`
**Description**: Provides asynchronous generator functionality for streaming results.
**Attributes**:
  - `supports_stream` (bool):  Indicates whether the provider supports streaming responses.
**Methods**:
  - `create_completion(model: str, messages: Messages, stream: bool = True, **kwargs) -> CreateResult`: Creates a streaming completion result synchronously.
  - `create_async_generator(model: str, messages: Messages, stream: bool = True, **kwargs) -> AsyncResult`: Abstract method for creating an asynchronous generator.
  - `get_create_function() -> callable`: Returns the callable function used for creating completions.
  - `get_async_create_function() -> callable`: Returns the callable function used for creating asynchronous completions.

### `ProviderModelMixin`
**Description**: Provides functionality for managing models.
**Attributes**:
  - `default_model`: The default model used by the provider.
  - `models`: A list of models supported by the provider.
  - `model_aliases`: A dictionary mapping aliases to model names.
  - `image_models`: A list of models that support image generation.
  - `vision_models`: A list of models that support vision tasks.
  - `last_model`: The last model used by the provider.
**Methods**:
  - `get_models(**kwargs) -> list[str]`: Returns the list of models supported by the provider.
  - `get_model(model: str, **kwargs) -> str`: Returns the model to use, validating it against the supported models and applying any aliases.

### `RaiseErrorMixin`
**Description**: Provides functionality for raising errors.
**Methods**:
  - `raise_error(data: dict, status: int = None)`: Raises an appropriate exception based on the error data provided.

### `AuthFileMixin`
**Description**: Provides functionality for managing authentication files.
**Methods**:
  - `get_cache_file() -> Path`: Returns the path to the authentication cache file.

### `AsyncAuthedProvider`
**Description**: Abstract base class for providers that require authentication.
**Attributes**:
  - `supports_stream` (bool):  Indicates whether the provider supports streaming responses.
**Methods**:
  - `on_auth_async(**kwargs) -> AuthResult`: Asynchronously authenticates the provider.
  - `on_auth(**kwargs) -> AuthResult`: Synchronously authenticates the provider.
  - `get_create_function() -> callable`: Returns the callable function used for creating completions.
  - `get_async_create_function() -> callable`: Returns the callable function used for creating asynchronous completions.
  - `write_cache_file(cache_file: Path, auth_result: AuthResult = None)`: Writes the authentication result to the cache file.
  - `create_completion(model: str, messages: Messages, **kwargs) -> CreateResult`: Creates a completion result synchronously.
  - `create_async_generator(model: str, messages: Messages, **kwargs) -> AsyncResult`: Creates an asynchronous generator for streaming results.

## Parameter Details
- `model` (str): The GPT4Free model to use for generating text or images. It must be a valid model name supported by the provider.
- `messages` (Messages): A list of messages to be processed by the model. Each message should be a dictionary with the following keys: `role`, `content`, `name`, `function_call`, `tool_code`, `content_type`.
- `stream` (bool): Indicates whether to stream the results.
- `timeout` (int): The maximum time to wait for the completion process to finish.
- `proxy` (str):  The proxy server to use when connecting to the GPT4Free API.
- `media` (list): A list of media items to be used as input to the model.
- `response_format` (dict): Defines the format of the response.
- `conversation` (dict):  A dictionary containing information about the conversation, including the conversation ID and message ID.
- `seed` (int): The seed value to use for random number generation.
- `tools` (list): A list of tools that the model can use during the completion process.
- `api_key` (str): The API key required for authentication.
- `api_base` (str): The base URL of the GPT4Free API.
- `max_retries` (int): The maximum number of retries in case of errors.
- `web_search` (bool):  Indicates whether to use web search for the completion process.
- `guidance_scale` (float): The guidance scale to use for text generation.
- `num_inference_steps` (int): The number of inference steps to use for text generation.
- `randomize_seed` (bool):  Indicates whether to use a randomized seed for text generation.
- `safe` (bool): Indicates whether to use safe mode for text generation.
- `enhance` (bool):  Indicates whether to enhance the quality of the generated text.
- `private` (bool):  Indicates whether to use private mode for text generation.
- `aspect_ratio` (str):  The aspect ratio of the generated image.
- `n` (int): The number of responses to generate.


## Examples
```python
# Example 1: Creating a completion using the default model.
response = provider.create_completion(model="text-davinci-003", messages=[
    {"role": "user", "content": "Write a short story about a cat."}
])
print(response)

# Example 2: Creating a completion with a specific model and streaming the results.
response = provider.create_completion(model="text-davinci-003", messages=[
    {"role": "user", "content": "Write a short story about a cat."}
], stream=True)
for chunk in response:
    print(chunk)

# Example 3: Creating a completion with custom parameters.
response = provider.create_completion(model="text-davinci-003", messages=[
    {"role": "user", "content": "Write a short story about a cat."}
], temperature=0.5, max_tokens=50)
print(response)
```
```python
# Example 4: Creating a completion with a proxy server.
response = provider.create_completion(model="text-davinci-003", messages=[
    {"role": "user", "content": "Write a short story about a cat."}
], proxy="http://user:password@127.0.0.1:3128")
print(response)

# Example 5: Creating a completion with a custom seed value.
response = provider.create_completion(model="text-davinci-003", messages=[
    {"role": "user", "content": "Write a short story about a cat."}
], seed=42)
print(response)
```
```python
# Example 6: Creating a completion with a custom response format.
response = provider.create_completion(model="text-davinci-003", messages=[
    {"role": "user", "content": "Write a short story about a cat."}
], response_format={"type": "json_object"})
print(response)

# Example 7: Creating a completion with a custom conversation ID.
response = provider.create_completion(model="text-davinci-003", messages=[
    {"role": "user", "content": "Write a short story about a cat."}
], conversation={"conversation_id": "550e8400-e29b-11d4-a716-...", "message_id": "550e8400-e29b-11d4-a716-..."})
print(response)
```
```python
# Example 8: Creating a completion with a custom tool.
response = provider.create_completion(model="text-davinci-003", messages=[
    {"role": "user", "content": "Write a short story about a cat."}
], tools=[{"type": "code", "function": "get_weather"}])
print(response)