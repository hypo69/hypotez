# AIChatFree Provider

## Overview

This module provides the `AIChatFree` class, which implements an asynchronous generator provider for the AIChatFree API. This class is designed to interact with the AIChatFree API and provides functionalities for sending messages and retrieving responses.

## Details

The `AIChatFree` class extends `AsyncGeneratorProvider` and `ProviderModelMixin`, inheriting functionalities for asynchronous generation and model handling. It defines its base URL, indicates support for streaming and message history, and sets a default model. 

The `create_async_generator` class method is responsible for creating an asynchronous generator that sends messages to the API and yields responses in chunks. It handles request headers, prepares the request body, sends the POST request, and iterates through the response content to yield decoded chunks.

## Classes

### `AIChatFree`

**Description:**  The `AIChatFree` class implements an asynchronous generator provider for the AIChatFree API, allowing for sending messages and retrieving responses.

**Inherits:**
    - `AsyncGeneratorProvider`: Provides functionalities for asynchronous generation.
    - `ProviderModelMixin`: Provides functionalities for handling models.

**Attributes:**
    - `url` (str): The base URL of the AIChatFree API.
    - `working` (bool): Indicates whether the provider is currently working.
    - `supports_stream` (bool): Indicates whether the provider supports streaming responses.
    - `supports_message_history` (bool): Indicates whether the provider supports message history.
    - `default_model` (str): The default model used by the provider.

**Methods:**
    - `create_async_generator(model: str, messages: Messages, proxy: str = None, connector: BaseConnector = None, **kwargs)`:  Creates an asynchronous generator that sends messages to the API and yields responses in chunks.

## Class Methods

### `create_async_generator`

**Purpose**: This method creates an asynchronous generator that sends messages to the AIChatFree API and yields responses in chunks.

**Parameters**:
    - `model` (str): The model to use for generating responses.
    - `messages` (Messages): A list of messages representing the conversation history.
    - `proxy` (str, optional): Proxy server address. Defaults to None.
    - `connector` (BaseConnector, optional): Custom connector for the HTTP client session. Defaults to None.
    - `**kwargs`: Additional keyword arguments.

**Returns**:
    - `AsyncResult`: An asynchronous result representing the generator.

**Raises Exceptions**:
    - `RateLimitError`: Raised when the rate limit for the API is exceeded.

**How the Function Works**:
    - The method prepares request headers, including user agent, accept types, encoding, and content type.
    - It creates an HTTP client session with optional proxy and connector.
    - The method generates a timestamp and constructs a data dictionary containing the conversation history, timestamp, and a signature generated using the `generate_signature` function.
    - It sends a POST request to the API endpoint `/api/generate` with the prepared data.
    - The method checks the response status. If it's 500 and contains the "Quota exceeded" message, it raises a `RateLimitError`.
    - After ensuring the request was successful, the method iterates through the response content and yields decoded chunks.

**Example**:

```python
async def example_usage():
    messages = [
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "assistant", "content": "I'm doing well, thank you for asking. How can I help you today?"},
    ]
    async for chunk in AIChatFree.create_async_generator(model='gemini-1.5-pro', messages=messages):
        print(chunk)

# Run the example (replace with your own event loop if needed)
import asyncio
asyncio.run(example_usage())
```

## Inner Functions

### `generate_signature`

**Purpose**: This function generates a signature for the request based on the provided time, text, and a secret key.

**Parameters**:
    - `time` (int): The timestamp in milliseconds.
    - `text` (str): The text used for generating the signature.
    - `secret` (str, optional): The secret key. Defaults to an empty string.

**Returns**:
    - `str`: The generated SHA256 signature in hexadecimal format.

**How the Function Works**:
    - The function combines the provided time, text, and secret key into a single string.
    - It encodes the message into bytes and generates the SHA256 hash.
    - Finally, it returns the hexadecimal representation of the hash. 

**Example**:

```python
signature = generate_signature(time=1694585535000, text="Hello, world!", secret="your_secret_key")
print(signature)
```