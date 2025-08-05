# AiAsk Provider

## Overview

This module defines the `AiAsk` class, which is an asynchronous provider for the AiAsk API.  It provides a mechanism to interact with AiAsk's chat API for generating responses using various AI models.

## Details

The `AiAsk` provider is designed to work with the AiAsk API for generating responses using AI models. It leverages the `aiohttp` library for asynchronous HTTP requests and the `AsyncGeneratorProvider` base class for efficient handling of responses.

## Classes

### `AiAsk`

**Description**: Represents an asynchronous provider for the AiAsk API.

**Inherits**:  `AsyncGeneratorProvider` 

**Attributes**:

- `url (str)`:  The base URL of the AiAsk API.
- `supports_message_history (bool)`: Indicates whether the provider supports message history.
- `supports_gpt_35_turbo (bool)`: Indicates whether the provider supports GPT-3.5 Turbo model.
- `working (bool)`: Flag to track the provider's working status.

**Methods**:

- `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`:  Creates an asynchronous generator for handling responses from the AiAsk API.

####  `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`

**Purpose**:  Creates an asynchronous generator to interact with the AiAsk API and stream responses.

**Parameters**:

- `model (str)`: The name of the AI model to use for generating responses.
- `messages (Messages)`: A list of messages representing the conversation history.
- `proxy (str, optional)`:  A proxy server URL to use for the request. Defaults to `None`.
- `**kwargs`:  Additional keyword arguments passed to the API.

**Returns**:

- `AsyncResult`: An asynchronous result object representing the API response.

**Raises Exceptions**:

- `RuntimeError`: If the rate limit is reached during the request.

**How the Function Works**:

1. **Initialize HTTP Session**:  Creates an asynchronous HTTP session with custom headers for the AiAsk API.
2. **Prepare Request Data**: Constructs a request data dictionary containing the conversation history (`messages`), model information, and additional parameters (e.g., `temperature`).
3. **Send API Request**: Performs a POST request to the AiAsk API endpoint `/v1/chat/gpt/` with the prepared data.
4. **Handle Response**: Iterates over chunks of the response content, yielding each chunk to the generator as it becomes available. 
5. **Rate Limit Handling**:  Checks for a specific rate limit message and raises an exception if encountered.
6. **Error Handling**:  Uses `response.raise_for_status()` to raise an exception if the request fails.


## Parameter Details

- `model (str)`:  The name of the AI model to use for generating responses.
- `messages (Messages)`:  A list of messages representing the conversation history. 
- `proxy (str, optional)`:  A proxy server URL to use for the request. Defaults to `None`.

**Examples**:

```python
# Example 1: Basic Usage
async def example_usage():
    model = "gpt-3.5-turbo"
    messages = [
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "assistant", "content": "I am doing well, thank you for asking!"},
    ]
    async_generator = await AiAsk.create_async_generator(model, messages)
    async for chunk in async_generator:
        print(chunk)

# Example 2: Using a Proxy Server
async def example_with_proxy():
    proxy = "http://your_proxy_server:port"
    model = "gpt-3.5-turbo"
    messages = [{"role": "user", "content": "What is the capital of France?"}]
    async_generator = await AiAsk.create_async_generator(model, messages, proxy=proxy)
    async for chunk in async_generator:
        print(chunk)
```