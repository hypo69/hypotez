# HuggingFaceAPI Provider

## Overview

This module provides the `HuggingFaceAPI` class, which is a provider class for interacting with the Hugging Face API. It handles authentication, model selection, and stream-based communication with the API.

## Details

The `HuggingFaceAPI` class extends the `OpenaiTemplate` class, which is used for all providers. It has a `get_model` method that allows you to specify the model to use and a `get_models` method that retrieves a list of available models from the Hugging Face API.

## Classes

### `HuggingFaceAPI`

**Description**: This class provides the functionality for interacting with the Hugging Face API. It implements the `get_model`, `get_models`, and `create_async_generator` methods for interacting with the API.

**Inherits**: `OpenaiTemplate`

**Attributes**:

- `label` (str): Label of the provider.
- `parent` (str): Parent provider.
- `url` (str): Base URL of the API.
- `api_base` (str): Base URL for the API calls.
- `working` (bool): Indicates if the provider is working.
- `needs_auth` (bool): Indicates if the provider requires authentication.
- `default_model` (str): Default model for text generation.
- `default_vision_model` (str): Default model for image generation.
- `vision_models` (list[str]): List of available vision models.
- `model_aliases` (dict[str, str]): Mapping of model aliases.
- `fallback_models` (list[str]): List of fallback models.
- `provider_mapping` (dict[str, dict]): Mapping of provider models to their corresponding task and providerId.

**Methods**:

- `get_model(model: str, **kwargs) -> str`: Retrieves the model identifier based on the provided model name and optional arguments.
- `get_models(**kwargs) -> list[str]`: Retrieves a list of available models from the Hugging Face API.
- `get_mapping(model: str, api_key: str = None) -> dict`: Retrieves the provider mapping for the specified model.
- `create_async_generator(model: str, messages: Messages, api_base: str = None, api_key: str = None, max_tokens: int = 2048, max_inputs_lenght: int = 10000, media: MediaListType = None, **kwargs) -> Generator[ProviderInfo, None, None]`: Creates an asynchronous generator for streaming responses from the API.

## Functions

### `calculate_lenght(messages: Messages) -> int`:

**Purpose**: Calculates the total length of the messages in a chat history.

**Parameters**:

- `messages` (Messages): Chat history messages.

**Returns**:

- `int`: Total length of the messages.

**How the Function Works**:

This function iterates through the provided chat history messages and calculates the total length of the messages. It takes into account the length of each message's content and adds a constant value (16) to account for the message metadata.

**Examples**:

```python
messages = [
    {"role": "user", "content": "Hello, how are you?"},
    {"role": "assistant", "content": "I'm doing well, thanks for asking."},
]
length = calculate_lenght(messages)
print(f"Total length of messages: {length}") # Output: Total length of messages: 49
```
```python