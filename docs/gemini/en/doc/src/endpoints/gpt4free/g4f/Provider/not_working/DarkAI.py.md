# DarkAI Provider

## Overview

This module provides the `DarkAI` class, which implements an asynchronous generator provider for interacting with the DarkAI API. The `DarkAI` provider allows you to use the DarkAI models (like `llama-3-70b`) for text generation and other NLP tasks.

## Details

The `DarkAI` class inherits from `AsyncGeneratorProvider` and `ProviderModelMixin` and provides functionality for making asynchronous API calls to the DarkAI endpoint.  The provider supports streaming responses for a more interactive and efficient communication with the AI model.

## Classes

### `class DarkAI`

**Description**: This class implements an asynchronous generator provider for the DarkAI API. 

**Inherits**: 
- `AsyncGeneratorProvider`:  Provides a base implementation for asynchronous generator providers.
- `ProviderModelMixin`:  Provides utility methods for managing and accessing models.

**Attributes**:

- `url` (str): Base URL of the DarkAI API endpoint.
- `api_endpoint` (str):  Specific endpoint for interacting with the chat service.
- `working` (bool): Flag indicating whether the provider is currently working (set to `False` initially).
- `supports_stream` (bool): Indicates whether the provider supports streaming responses (`True` in this case).
- `default_model` (str): Default model to use when none is specified (`llama-3-70b` by default).
- `models` (list): List of supported models.
- `model_aliases` (dict): Dictionary for mapping model aliases to their canonical names. 

**Methods**:

- `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`: This method creates an asynchronous generator that interacts with the DarkAI API to generate text or perform other NLP tasks.

## Functions

### `create_async_generator()`

**Purpose**: This function initiates an asynchronous generator for communication with the DarkAI API.

**Parameters**:

- `model` (str): The DarkAI model to use (e.g., `llama-3-70b`). 
- `messages` (Messages):  A list of message objects, each containing a message content and a role (user or assistant).
- `proxy` (str, optional):  A proxy server to use for making requests. Defaults to `None`.
- `kwargs`: Additional keyword arguments for customizing requests.

**Returns**:

- `AsyncResult`: An asynchronous result object that provides access to the generated text as a stream.

**How the Function Works**:

1. **Model Selection**: The function uses `get_model` to resolve the model name (handling aliases if needed).
2. **Setting Headers**:  The function prepares headers for the API request, including `accept`, `content-type`, and `user-agent`.
3. **Asynchronous Session**: It establishes an asynchronous session with `aiohttp` for making API calls.
4. **Formatting Prompt**: The function formats the prompt using the `format_prompt` helper.
5. **API Call**: The function sends a POST request to the DarkAI API endpoint with the formatted prompt, the model name, and any additional kwargs.
6. **Error Handling**:  The function checks the response status code using `raise_for_status` to handle potential API errors.
7. **Streaming Data**: The function reads the response content as a stream (using `StreamReader`) and iterates through it in chunks. It extracts the text data and yields it as a generator, enabling streaming of the AI model's response.
8. **End of Stream**:  When the response stream ends, the function returns. 


**Examples**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.DarkAI import DarkAI
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Example messages list
messages: Messages = [
    {'role': 'user', 'content': 'Tell me a joke.'},
]

# Using DarkAI with the default model (llama-3-70b)
async def main():
    async for chunk in DarkAI.create_async_generator(model='llama-3-70b', messages=messages):
        print(chunk, end='')

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```
```python
# Example with a custom model
async def main():
    async for chunk in DarkAI.create_async_generator(model='gpt-3.5-turbo', messages=messages):
        print(chunk, end='')

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())