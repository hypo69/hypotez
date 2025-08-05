# FlowGpt Provider

## Overview

This module provides the `FlowGpt` class, which implements an asynchronous generator provider for interacting with the FlowGPT API.  The provider supports various language models, including GPT-3.5-turbo, GPT-4, Google Gemini, Claude, and Llama 2, and allows users to access them through an asynchronous generator interface.

## Details

The `FlowGpt` provider utilizes the FlowGPT API to generate responses based on user prompts. It allows the user to set the model, temperature, and other parameters for the generated response. The provider supports message history and system messages, enabling contextual conversations with the chosen language model.

## Classes

### `class FlowGpt`

**Description**: 
This class implements an asynchronous generator provider for interacting with the FlowGPT API.

**Inherits**:
- `AsyncGeneratorProvider`:  Handles the asynchronous generation of responses from the provider.
- `ProviderModelMixin`: Provides methods for managing and selecting language models.

**Attributes**:
- `url (str)`: The base URL of the FlowGPT API.
- `working (bool)`: Indicates whether the provider is currently operational.
- `supports_message_history (bool)`: Determines if the provider supports message history.
- `supports_system_message (bool)`: Indicates if the provider supports system messages.
- `default_model (str)`: The default language model used by the provider.
- `models (list[str])`: A list of supported language models.
- `model_aliases (dict[str, str])`: A dictionary mapping aliases to actual model names.

**Methods**:

#### `create_async_generator(model: str, messages: Messages, proxy: str = None, temperature: float = 0.7, **kwargs) -> AsyncResult`

**Purpose**:  Creates an asynchronous generator for generating responses from the FlowGPT API.

**Parameters**:
- `model (str)`: The desired language model to use.
- `messages (Messages)`: A list of messages representing the conversation history.
- `proxy (str, optional)`: A proxy server URL to use for API requests. Defaults to `None`.
- `temperature (float, optional)`: The temperature parameter, controlling the randomness of the generated response. Defaults to `0.7`.
- `**kwargs`: Additional keyword arguments for customizing the API request.

**Returns**:
- `AsyncResult`: An asynchronous result object representing the generator.

**Raises**:
- `Exception`: If an error occurs during the API request or response processing.

**How the Function Works**:

1. This function first retrieves the model name from the `model_aliases` dictionary if an alias is provided.
2. The function then generates a timestamp, nonce, and signature for authentication.
3. It constructs a `headers` dictionary containing authentication and other request parameters.
4. The function then initializes an asynchronous client session with the configured headers.
5. The `history` list is created from the provided messages, excluding system messages.
6. The `system_message` is constructed from the system messages in the `messages` list.
7.  A dictionary containing the request data, including model, messages, and parameters, is created.
8. The function sends a POST request to the FlowGPT API with the generated data and the configured headers.
9. The response is processed to extract and yield generated text chunks to the caller.

**Examples**:
```python
# Example 1: Using the default model
async def example_1():
    messages = [
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "assistant", "content": "I am doing well, thank you. How about you?"},
    ]
    async for response in FlowGpt.create_async_generator(messages=messages):
        print(response)

# Example 2: Using a specific model with system message
async def example_2():
    messages = [
        {"role": "system", "content": "You are a helpful and polite chatbot."},
        {"role": "user", "content": "What is the capital of France?"},
    ]
    async for response in FlowGpt.create_async_generator(model="gpt-3.5-turbo", messages=messages):
        print(response)
```

## Parameter Details

- `model (str)`: The language model to use for generating responses. Supported models include "gpt-3.5-turbo", "gpt-3.5-long", "gpt-4-turbo", "google-gemini", "claude-instant", "claude-v1", "claude-v2", "llama2-13b", "mythalion-13b", "pygmalion-13b", "chronos-hermes-13b", "Mixtral-8x7B", and "Dolphin-2.6-8x7B". You can use aliases for some models, like "gemini" for "google-gemini".

- `messages (Messages)`: A list of dictionaries representing the conversation history. Each dictionary should have the following keys:
    - `role (str)`: The role of the message sender. Possible values are "user", "assistant", and "system".
    - `content (str)`: The content of the message.

- `proxy (str, optional)`:  A proxy server URL to use for API requests. It can be a string in the format "http://user:password@host:port".  Defaults to `None` (no proxy).

- `temperature (float, optional)`:  Controls the randomness of the generated response.  A higher temperature results in more creative and unexpected outputs.  Defaults to `0.7`.

## Examples

```python
# Example 1: Simple interaction
async def example_1():
    messages = [
        {"role": "user", "content": "Hello, how are you?"},
    ]
    async for response in FlowGpt.create_async_generator(messages=messages):
        print(f"Assistant: {response}")

# Example 2: Using a specific model
async def example_2():
    messages = [
        {"role": "user", "content": "What is the meaning of life?"},
    ]
    async for response in FlowGpt.create_async_generator(model="gpt-4-turbo", messages=messages):
        print(f"Assistant: {response}")

# Example 3: Using a system message
async def example_3():
    messages = [
        {"role": "system", "content": "You are a friendly and informative chatbot."},
        {"role": "user", "content": "What is the capital of France?"},
    ]
    async for response in FlowGpt.create_async_generator(model="google-gemini", messages=messages):
        print(f"Assistant: {response}")
```