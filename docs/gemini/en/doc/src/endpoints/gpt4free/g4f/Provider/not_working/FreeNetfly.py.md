# FreeNetfly Provider Module

## Overview

This module provides the `FreeNetfly` class, an asynchronous generator provider that interacts with the FreeNetfly API for GPT-based text generation. It offers access to various GPT models, including `gpt-3.5-turbo` and `gpt-4`, allowing for text completion and conversational interactions. 

## Details

This provider is built to handle asynchronous requests to the FreeNetfly API for generating text using GPT models. It implements a retry mechanism with exponential backoff to improve robustness and resilience in case of network errors or API issues.

## Classes

### `class FreeNetfly`

**Description:** This class represents a provider that communicates with the FreeNetfly API to utilize GPT models for text generation. It inherits from `AsyncGeneratorProvider` and `ProviderModelMixin`, enabling it to generate text asynchronously and manage model selection.

**Inherits:**
    - `AsyncGeneratorProvider`: Implements asynchronous text generation capabilities.
    - `ProviderModelMixin`: Provides functionality for model selection and management.

**Attributes:**
    - `url (str)`: The base URL of the FreeNetfly API.
    - `api_endpoint (str)`: The specific endpoint within the API for chat completion requests.
    - `working (bool)`: A flag indicating whether the provider is currently operational (not implemented in this example).
    - `default_model (str)`: The default GPT model to use.
    - `models (list[str])`: A list of supported GPT models.

**Methods:**

#### `create_async_generator`

**Purpose:** Asynchronously generates text using the specified GPT model and messages.

**Parameters:**
    - `model (str)`: The GPT model to use for text generation.
    - `messages (Messages)`: A list of messages for the conversation.
    - `proxy (str, optional)`: A proxy server to use for the request. Defaults to `None`.
    - `**kwargs`: Additional keyword arguments for the API request.

**Returns:**
    - `AsyncResult`: An asynchronous result object containing the generated text.

**Raises Exceptions:**
    - `ClientError`: If an error occurs during the HTTP request.
    - `asyncio.TimeoutError`: If the request times out.

**How the Function Works:**
    - The function sets up headers for the API request, including necessary information like Accept, Content-Type, Origin, and User-Agent.
    - It creates a JSON payload containing the `messages`, `model`, and other parameters for the GPT request.
    - It implements a retry loop with exponential backoff to handle potential errors during the API call.
    - The loop retries the request up to a specified number of times, increasing the delay between attempts exponentially.
    - The function uses `ClientSession` to make the POST request to the FreeNetfly API.
    - The response is then processed using the `_process_response` method, which parses the streamed data and yields individual text chunks.

#### `_process_response`

**Purpose:** Processes the streamed response from the FreeNetfly API to extract generated text.

**Parameters:**
    - `response`: The response object from the API request.

**Returns:**
    - `AsyncGenerator[str, None]`: An asynchronous generator yielding text chunks from the response.

**How the Function Works:**
    - The function iterates over lines from the response content, decoding them into UTF-8 strings.
    - It buffers the data and checks for a specific pattern to identify complete text chunks.
    - When a complete chunk is found, the function extracts the relevant content from the JSON data and yields it.
    - The process continues until the end of the stream is reached, handling any remaining data in the buffer.

## Examples

```python
# Creating a FreeNetfly provider instance
provider = FreeNetfly()

# Defining messages for the conversation
messages = [
    {"role": "user", "content": "Hello, how are you?"},
]

# Generating text using the default model
async def generate_text():
    async for chunk in provider.create_async_generator(model=provider.default_model, messages=messages):
        print(chunk, end="")

# Running the asynchronous task
asyncio.run(generate_text())
```

## Parameter Details

### `model` (str)

The GPT model to use for text generation. Supported models include `gpt-3.5-turbo` and `gpt-4`.

### `messages` (Messages)

A list of messages for the conversation. Each message should be a dictionary with `role` (e.g., "user", "system") and `content` keys.

### `proxy` (str, optional)

A proxy server to use for the API request. Defaults to `None`.

### `**kwargs`

Additional keyword arguments for the API request, such as `temperature`, `presence_penalty`, and `frequency_penalty`.

```python
# Example with custom model and proxy
async def generate_text():
    async for chunk in provider.create_async_generator(model='gpt-4', messages=messages, proxy='http://myproxy:8080'):
        print(chunk, end="")

asyncio.run(generate_text())
```