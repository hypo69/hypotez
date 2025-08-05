# Provider: NoowAi

## Overview

This module provides an asynchronous generator provider for NoowAi, a GPT-4 powered chatbot service. It allows integration with NoowAi for chat-based interactions and utilizes `aiohttp` for asynchronous communication.

## Details

The `NoowAi` class extends the base `AsyncGeneratorProvider` class, providing a framework for handling interactions with the NoowAi service. It implements methods for creating asynchronous generators that stream responses from NoowAi, enabling continuous conversation with the chatbot.

## Classes

### `NoowAi`

**Description**:  This class represents a provider for the NoowAi GPT-4 powered chatbot. It allows interactions with the NoowAi service and manages the flow of messages between the user and the chatbot.

**Inherits**: `AsyncGeneratorProvider`

**Attributes**:

- `url`: The base URL of the NoowAi service.
- `supports_message_history`: Indicates whether the provider supports message history.
- `supports_gpt_35_turbo`: Indicates whether the provider supports the `gpt-3.5-turbo` model.
- `working`: Flag to track whether the provider is currently working.

**Methods**:

- `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`: This method creates an asynchronous generator that streams messages from NoowAi. It sends requests to the NoowAi API with the given model, messages, and optional proxy. It iterates through the server's response, yields each message as a dictionary, and handles different response types (`live`, `end`, `error`).

##  How the `create_async_generator` Method Works:

1.  **Setting up the Request**: Initializes request headers with information about the user-agent, acceptance types, encoding, referer, content-type, origin, etc.

2.  **Preparing Data**: Assembles request data in a dictionary including:
    - `botId`: Bot identifier.
    - `customId`: Custom identifier.
    - `session`: Session information (N/A in this case).
    - `chatId`: Randomly generated chat identifier.
    - `contextId`: Context identifier.
    - `messages`: The entire chat history (messages).
    - `newMessage`: The latest message from the user.
    - `stream`: True for streaming responses.

3.  **Sending the Request**: Sends a POST request to the NoowAi API endpoint `"/wp-json/mwai-ui/v1/chats/submit"` with the prepared data and optional proxy.

4.  **Processing the Response**: Iterates through the response content, line by line.
    - **Data Handling**: If the line starts with `b"data: "`, it decodes the JSON data and yields the `data` part if the `type` is `live`.
    - **End of Response**: If the `type` is `end`, the generator loop breaks.
    - **Error Handling**: If the `type` is `error`, it raises a `RuntimeError` with the error data.

## Example

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.NoowAi import NoowAi
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages
from hypotez.src.logger import logger

async def example():
    messages: Messages = [
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "assistant", "content": "I am doing well, thank you. How can I help you?"},
    ]
    async for response in NoowAi.create_async_generator(model="gpt-3.5-turbo", messages=messages):
        logger.info(f"Response from NoowAi: {response}")

```

## Inner Functions

-  No inner functions are defined within the `NoowAi` class.

```python