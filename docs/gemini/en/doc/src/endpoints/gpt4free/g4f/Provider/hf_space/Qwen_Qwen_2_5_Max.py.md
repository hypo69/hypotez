# Qwen_Qwen_2_5_Max Provider

## Overview

This module provides the `Qwen_Qwen_2_5_Max` class, which implements an asynchronous generator provider for the Qwen Qwen-2.5-Max model hosted on Hugging Face Spaces. The provider allows for interacting with the model, sending messages, and receiving responses, all within an asynchronous context. 

## Details

The `Qwen_Qwen_2_5_Max` class inherits from `AsyncGeneratorProvider` and `ProviderModelMixin`, providing capabilities for asynchronous message generation and model-related configurations. 

The provider connects to the Qwen Qwen-2.5-Max model hosted on Hugging Face Spaces using a specific API endpoint and handles the communication via HTTP requests. It supports streaming responses, allowing for the delivery of parts of the response as they are generated. 

## Classes

### `class Qwen_Qwen_2_5_Max(AsyncGeneratorProvider, ProviderModelMixin)`

**Description**: This class provides an asynchronous generator provider for the Qwen Qwen-2.5-Max model. It handles communication with the model, formats prompts, and streams responses.

**Inherits**: 
    - `AsyncGeneratorProvider`: Provides asynchronous message generation capabilities.
    - `ProviderModelMixin`: Enables model-specific configuration and settings.

**Attributes**:

    - `label (str)`: Label for the provider, "Qwen Qwen-2.5-Max".
    - `url (str)`: Base URL of the Hugging Face Spaces deployment.
    - `api_endpoint (str)`: API endpoint for interacting with the model.
    - `working (bool)`: Indicates if the provider is operational (True).
    - `supports_stream (bool)`: Indicates support for streaming responses (True).
    - `supports_system_message (bool)`: Indicates support for system messages (True).
    - `supports_message_history (bool)`: Indicates support for message history (False).
    - `default_model (str)`: Default model name.
    - `model_aliases (dict)`: Mapping of model aliases to the default model name.
    - `models (list)`: List of supported models.

**Methods**:

    - `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`: 
        - **Purpose**: This class method generates an asynchronous generator for interacting with the model.
        - **Parameters**:
            - `model (str)`: The model name to use.
            - `messages (Messages)`: A list of messages containing user input and potential system messages.
            - `proxy (str, optional)`: A proxy server address if needed. Defaults to None.
        - **Returns**:
            - `AsyncResult`: An asynchronous result object containing the generator. 
        - **How the Function Works**:
            - Generates a unique session hash for the interaction.
            - Prepares HTTP headers and a payload containing the formatted prompt and system message.
            - Sends a "join" request to the API endpoint to join the model's queue.
            - Extracts the event ID from the response.
            - Prepares a data stream request using the event ID and session hash.
            - Sends the data stream request and iterates through the response content.
            - Parses JSON data from the response stream.
            - Yields fragments of the response as they are received. 
            - Handles completion signals and yields the final response.
        - **Examples**:
            ```python
            async def main():
                messages = [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "What is the capital of France?"}
                ]
                async_result = await Qwen_Qwen_2_5_Max.create_async_generator(model="qwen-qwen2-5-max", messages=messages)
                async for response_part in async_result.generator:
                    print(response_part, end="")
            ```

## Inner Functions

### `generate_session_hash()`

**Purpose**: This function generates a unique session hash for the interaction with the model.

**Parameters**: None

**Returns**: 
    - `str`: A unique session hash.

**How the Function Works**:

- The function combines two randomly generated UUIDs, removing hyphens and taking the first 8 characters of the first UUID and the first 4 characters of the second UUID.
- The result is returned as a string.


## Parameter Details

- `messages (Messages)`: A list of messages representing the conversation history. Each message is a dictionary with keys `role`, `content`, and optionally `name`, `time`.  

    - `role (str)`: Indicates the role of the message sender. Possible values are "user", "system", and "assistant".
    - `content (str)`: The message content.
    - `name (str, optional)`: The name of the message sender.
    - `time (datetime, optional)`: The timestamp of the message.

- `proxy (str, optional)`: A proxy server address to be used for the communication with the model. 

## Examples

```python
# Example usage:
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf_space.Qwen_Qwen_2_5_Max import Qwen_Qwen_2_5_Max
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

async def main():
    messages: Messages = [
        {"role": "system", "content": "You are a helpful and informative AI assistant."},
        {"role": "user", "content": "What is the capital of France?"},
    ]
    async_result = await Qwen_Qwen_2_5_Max.create_async_generator(model="qwen-qwen2-5-max", messages=messages)
    async for response_part in async_result.generator:
        print(response_part, end="")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```