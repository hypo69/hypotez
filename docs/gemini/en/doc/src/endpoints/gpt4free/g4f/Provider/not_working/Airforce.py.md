# Airforce Provider Module

## Overview

This module provides an implementation of the `Airforce` provider for the `hypotez` project. The `Airforce` provider enables interaction with the Airforce API for generating text and images.

## Details

The `Airforce` provider is designed to leverage the capabilities of the Airforce API for text completion and image generation. It supports various models, including both text-based models like `llama-3.1-70b-chat` and image-based models like `flux`.

The module offers functionality for splitting messages into chunks, fetching available models, applying aliases, and filtering responses. It also includes asynchronous generator methods for text and image generation, enabling streaming capabilities for text responses.

## Classes

### `Airforce`

**Description:** The `Airforce` class represents the provider for interacting with the Airforce API. It inherits from `AsyncGeneratorProvider` and `ProviderModelMixin`, enabling asynchronous generation of text and images.

**Inherits:** `AsyncGeneratorProvider`, `ProviderModelMixin`

**Attributes:**

- `url (str):` Base URL for the Airforce API.
- `api_endpoint_completions (str):` URL for the completions endpoint.
- `api_endpoint_imagine2 (str):` URL for the imagine2 endpoint.
- `working (bool):` Indicates whether the provider is currently working (not used in this implementation).
- `supports_stream (bool):` Whether the provider supports streaming responses.
- `supports_system_message (bool):` Whether the provider supports system messages.
- `supports_message_history (bool):` Whether the provider supports message history.
- `default_model (str):` Default text model to use.
- `default_image_model (str):` Default image model to use.
- `models (list):` List of available text models.
- `image_models (list):` List of available image models.
- `hidden_models (set):` Set of models that are hidden from the user.
- `additional_models_imagine (list):` Additional models to include for image generation.
- `model_aliases (dict):` Mapping of model aliases to actual model names.

**Methods:**

- `get_models() -> list:` Fetches available models from the Airforce API, including text and image models.
- `get_model(model: str) -> str:` Gets the actual model name from the alias, if provided.
- `_filter_content(part_response: str) -> str:` Filters out unwanted content from the partial response, such as error messages and discord invites.
- `_filter_response(response: str) -> str:` Filters the full response to remove system errors and other unwanted text, such as tokens and prefixes.
- `generate_image(model: str, prompt: str, size: str, seed: int, proxy: str = None) -> AsyncResult:` Generates an image based on the provided prompt, size, seed, and model.
- `generate_text(model: str, messages: Messages, max_tokens: int, temperature: float, top_p: float, stream: bool, proxy: str = None) -> AsyncResult:` Generates text based on the provided messages, model, and parameters.
- `create_async_generator(model: str, messages: Messages, prompt: str = None, proxy: str = None, max_tokens: int = 512, temperature: float = 1, top_p: float = 1, stream: bool = True, size: str = "1:1", seed: int = None, **kwargs) -> AsyncResult:` Creates an asynchronous generator for either text or image generation based on the provided model and parameters.


## Class Methods

### `split_message(message: str, max_length: int = 1000) -> List[str]`

**Purpose:** Splits the message into parts up to the specified `max_length`.

**Parameters:**

- `message (str):` The message to be split.
- `max_length (int, optional):` Maximum length of each part. Defaults to 1000.

**Returns:**

- `List[str]:` A list of message parts.

**Example:**

```python
message = "This is a very long message that needs to be split into parts."
parts = split_message(message, max_length=20)
print(parts)  # Output: ['This is a very long', 'message that needs to be', 'split into parts.']
```

## Functions

### `_filter_content(part_response: str) -> str`

**Purpose:** Filters out unwanted content from the partial response, such as error messages and discord invites.

**Parameters:**

- `part_response (str):` The partial response to filter.

**Returns:**

- `str:` The filtered partial response.

**How the Function Works:**

- The function uses regular expressions to replace specific patterns in the response, including error messages related to rate limits and discord invites.

**Example:**

```python
partial_response = "One message exceeds the 4000chars per message limit...https://discord.com/invite/xyz"
filtered_response = _filter_content(partial_response)
print(filtered_response)  # Output: "One message exceeds the 4000chars per message limit..."
```

### `_filter_response(response: str) -> str`

**Purpose:** Filters the full response to remove system errors and other unwanted text.

**Parameters:**

- `response (str):` The full response to filter.

**Returns:**

- `str:` The filtered response.

**How the Function Works:**

- The function uses regular expressions to replace specific patterns in the response, including system errors, tokens, and prefixes.

**Example:**

```python
response = "[ERROR] '1234-5678-9012-3456-78901234' <|im_end|>"
filtered_response = _filter_response(response)
print(filtered_response)  # Output: ""
```

## Parameter Details

- `model (str):` The name of the model to use.
- `messages (Messages):` A list of messages to use as context for text generation.
- `prompt (str):` The prompt for image generation.
- `max_tokens (int):` Maximum number of tokens to generate.
- `temperature (float):` Temperature parameter for text generation.
- `top_p (float):` Nucleus sampling parameter for text generation.
- `stream (bool):` Whether to stream the text response.
- `size (str):` The size of the generated image.
- `seed (int):` Seed for image generation.
- `proxy (str):` Proxy server address (optional).

## Examples

```python
# Creating a driver instance
driver = Driver(Chrome)

# Example of generating text with the default model
messages = [
    {"role": "user", "content": "Hello, how are you?"}
]
async for result in Airforce.create_async_generator(messages=messages):
    print(result)

# Example of generating an image with the Flux model
prompt = "A beautiful sunset over the ocean."
async for result in Airforce.create_async_generator(model="flux", prompt=prompt):
    print(result)
```