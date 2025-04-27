# Yqcloud Provider for GPT-4Free

## Overview

This module implements the `Yqcloud` class, an asynchronous provider for the `gpt4free` project, utilizing the `yqcloud.top` service. It leverages the `aiohttp` library for asynchronous HTTP requests and provides a stream-based API for interacting with the service.

## Details

The `Yqcloud` provider enables access to the `yqcloud.top` API, which offers a free GPT-4-like service. The provider handles the following functionalities:

- **Stream-based communication**: The `create_async_generator` method provides an asynchronous generator for receiving responses from the server in real-time.
- **Model Selection**: Users can specify the desired model from the supported list. The default model is `gpt-4`.
- **System Messages**: The provider supports system messages, allowing users to provide context and instructions to the model.
- **Message History**: The provider maintains a message history to provide the model with context from previous interactions.
- **Error Handling**: The provider incorporates error handling mechanisms, ensuring proper response status checks and raising exceptions if necessary.
- **Proxy Support**: The provider allows the use of a proxy server for requests.

## Classes

### `class Yqcloud`

**Description**: This class represents the asynchronous provider for the `yqcloud.top` API. It extends the `AsyncGeneratorProvider` and `ProviderModelMixin` classes, inheriting common functionalities for asynchronous generators and model selection.

**Inherits**: 
    - `AsyncGeneratorProvider`: Provides the base functionality for asynchronous generators for receiving responses.
    - `ProviderModelMixin`: Offers methods for model selection and validation.

**Attributes**:

    - `url`: The base URL for the `yqcloud.top` service.
    - `api_endpoint`: The endpoint for the API responsible for generating stream responses.
    - `working`: Indicates the availability of the service.
    - `supports_stream`: Specifies whether the provider supports streaming responses.
    - `supports_system_message`: Indicates whether the provider supports system messages.
    - `supports_message_history`: Specifies whether the provider supports message history.
    - `default_model`: The default model used by the provider.
    - `models`: A list of supported models.

**Methods**:

    - `create_async_generator(model: str, messages: Messages, stream: bool = True, proxy: str = None, conversation: Conversation = None, return_conversation: bool = False, **kwargs) -> AsyncResult`: 
        **Purpose**: Creates an asynchronous generator for interacting with the `yqcloud.top` API, allowing users to receive responses in a stream-based fashion.
        **Parameters**:
            - `model`: The name of the desired model.
            - `messages`: A list of messages in the conversation.
            - `stream`: Boolean value indicating whether to receive responses in a streaming format.
            - `proxy`: Optional proxy server address.
            - `conversation`: An instance of the `Conversation` class representing the current conversation.
            - `return_conversation`: Boolean value indicating whether to return the updated conversation object after processing the request.
            - `**kwargs`: Additional keyword arguments.
        **Returns**:
            - `AsyncResult`: An asynchronous result object, representing the response from the server.
        **Raises Exceptions**:
            - `SomeError`: If there is an error during the process.
        **How the Function Works**:
            - Extracts the desired model from the `models` list.
            - Sets the appropriate headers for the request.
            - Creates or updates the conversation object with the provided message history.
            - Extracts the system message if present from the conversation history.
            - Formats the prompt using the `format_prompt` function.
            - Sends a POST request to the API endpoint with the formatted prompt and other relevant data.
            - Handles the response from the server, iterating over the stream and yielding each message.
            - If `return_conversation` is `True`, updates the conversation history with the assistant's response and yields the updated conversation object.
            - Yields the `FinishReason` indicating the reason for the response completion.

    - `get_model(model: str) -> str`:
        **Purpose**: Retrieves the valid model from the `models` list.
        **Parameters**:
            - `model`: The desired model.
        **Returns**:
            - `str`: The validated model name.
        **How the Function Works**:
            - Checks if the provided model is in the `models` list.
            - Returns the `default_model` if the provided model is not found.
            - Returns the provided model if it is found in the `models` list.

## Inner Functions

- None

## Examples

```python
# Example of using the Yqcloud provider
from hypotez.src.endpoints.gpt4free.g4f.Provider.Yqcloud import Yqcloud
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

async def main():
    provider = Yqcloud()
    messages: Messages = [
        {"role": "user", "content": "Hello, how are you?"},
    ]
    async for response in provider.create_async_generator(model="gpt-4", messages=messages):
        print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## Parameter Details

- `model` (str): The name of the desired model.
- `messages` (Messages): A list of messages in the conversation. Each message is a dictionary with `role` and `content` keys.
- `stream` (bool, optional): Whether to receive responses in a stream-based format. Defaults to `True`.
- `proxy` (str, optional): The address of a proxy server. Defaults to `None`.
- `conversation` (Conversation, optional): An instance of the `Conversation` class representing the current conversation. Defaults to `None`.
- `return_conversation` (bool, optional): Whether to return the updated conversation object after processing the request. Defaults to `False`.

##  Usage Examples

```python
# Example of using the Yqcloud provider with a system message
from hypotez.src.endpoints.gpt4free.g4f.Provider.Yqcloud import Yqcloud
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

async def main():
    provider = Yqcloud()
    messages: Messages = [
        {"role": "system", "content": "You are a friendly and helpful AI assistant."},
        {"role": "user", "content": "What is the meaning of life?"},
    ]
    async for response in provider.create_async_generator(model="gpt-4", messages=messages):
        print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

```python
# Example of using the Yqcloud provider with message history
from hypotez.src.endpoints.gpt4free.g4f.Provider.Yqcloud import Yqcloud
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

async def main():
    provider = Yqcloud()
    messages: Messages = [
        {"role": "user", "content": "Hello, what's your name?"},
        {"role": "assistant", "content": "My name is Bard."},
        {"role": "user", "content": "Nice to meet you, Bard. Can you tell me a joke?"},
    ]
    async for response in provider.create_async_generator(model="gpt-4", messages=messages):
        print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```