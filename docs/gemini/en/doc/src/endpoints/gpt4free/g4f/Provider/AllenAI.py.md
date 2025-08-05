# AllenAI Provider for GPT4Free

## Overview

This module defines the `AllenAI` class, which implements the `AsyncGeneratorProvider` interface to interact with the AllenAI Playground API for generating text using various models. It handles asynchronous requests, message formatting, and response processing. 

## Details

The AllenAI provider is responsible for sending requests to the AllenAI Playground API and processing the responses to provide a text generation service. The `AllenAI` class inherits from `AsyncGeneratorProvider` and `ProviderModelMixin`, which define common functionalities for asynchronous providers. The module also defines a `Conversation` class to manage the conversation context.

## Classes

### `Conversation`

**Description**: Represents a conversation with the AllenAI model. Stores the conversation history (messages) and maintains a unique user identifier (`x_anonymous_user_id`).

**Inherits**: `JsonConversation`

**Attributes**:

- `parent` (str, optional): The parent message ID in the conversation. Used for tracking conversation threads. Defaults to `None`.
- `x_anonymous_user_id` (str): A unique identifier for the user, generated using UUID.

**Methods**:

- `__init__(self, model: str)`: Initializes a new conversation instance with the specified model.

### `AllenAI`

**Description**: Implements the `AsyncGeneratorProvider` interface to provide asynchronous text generation using the AllenAI Playground API.

**Inherits**: `AsyncGeneratorProvider`, `ProviderModelMixin`

**Attributes**:

- `label` (str): The label for the provider, set to "Ai2 Playground".
- `url` (str): The base URL for the AllenAI Playground.
- `login_url` (str, optional): The URL for logging in to the AllenAI Playground. Not used in this implementation, as AllenAI does not require authentication. Defaults to `None`.
- `api_endpoint` (str): The endpoint URL for sending API requests.
- `working` (bool): Indicates whether the provider is currently functioning. Defaults to `True`.
- `needs_auth` (bool): Indicates whether the provider requires authentication. Defaults to `False`.
- `use_nodriver` (bool): Indicates whether the provider requires a webdriver. Defaults to `False`.
- `supports_stream` (bool): Indicates whether the provider supports streaming responses. Defaults to `True`.
- `supports_system_message` (bool): Indicates whether the provider supports system messages. Defaults to `False`.
- `supports_message_history` (bool): Indicates whether the provider supports message history. Defaults to `True`.
- `default_model` (str): The default model to use for text generation.
- `models` (list): A list of supported models.
- `model_aliases` (dict): A dictionary mapping model aliases to the corresponding model names.

**Methods**:

- `create_async_generator(cls, model: str, messages: Messages, proxy: str = None, host: str = "inferd", private: bool = True, top_p: float = None, temperature: float = None, conversation: Conversation = None, return_conversation: bool = False, **kwargs) -> AsyncResult`

    **Purpose**: Asynchronously generates text using the AllenAI Playground API.

    **Parameters**:

    - `model` (str): The model to use for text generation.
    - `messages` (Messages): A list of messages in the conversation.
    - `proxy` (str, optional): A proxy server to use for making API requests. Defaults to `None`.
    - `host` (str, optional): The host to use for the request. Defaults to `inferd`.
    - `private` (bool, optional): Whether the request is private. Defaults to `True`.
    - `top_p` (float, optional): The top_p parameter for controlling the diversity of the generated text. Defaults to `None`.
    - `temperature` (float, optional): The temperature parameter for controlling the randomness of the generated text. Defaults to `None`.
    - `conversation` (Conversation, optional): The conversation context to use. Defaults to `None`.
    - `return_conversation` (bool, optional): Whether to return the conversation object along with the generated text. Defaults to `False`.
    - `**kwargs`: Additional keyword arguments.

    **Returns**:
    - `AsyncResult`: An asynchronous result object that yields generated text chunks and eventually finishes with a "stop" reason.

    **Raises Exceptions**:
    - `RequestError`: If an error occurs during the API request.

    **How the Function Works**:

    1. Formats the prompt using the provided `messages` or extracts the last user message if a `conversation` object is provided.
    2. Initializes or updates the `conversation` object.
    3. Generates a unique boundary for the multipart form data.
    4. Creates headers for the request, including user agent, accept, content-type, and other relevant headers.
    5. Builds the multipart form data using a list of tuples, including the model, host, content (prompt), private flag, and optional parameters (temperature and top_p).
    6. Adds the parent ID to the form data if it exists in the `conversation` object.
    7. Sends a POST request to the API endpoint with the prepared form data and headers using `aiohttp`.
    8. Processes the response asynchronously, yielding each received text chunk and managing the conversation context.
    9. Finishes the response with a "stop" reason after receiving the final text.

    **Examples**:

    ```python
    async def main():
        messages = [
            {"role": "user", "content": "Hello, how are you?"},
        ]
        async for chunk in AllenAI.create_async_generator(model='tulu3-405b', messages=messages):
            print(chunk)
    ```

## Parameter Details

- `model` (str): The specific model name to use for text generation.
- `messages` (Messages): A list of messages in the conversation, each containing a `role` (user or assistant) and a `content` string.
- `proxy` (str, optional): A proxy server address to use for making API requests.
- `host` (str, optional): The host server to use for the request.
- `private` (bool, optional):  Indicates whether the request should be treated as private.
- `top_p` (float, optional):  Controls the diversity of the generated text.
- `temperature` (float, optional): Controls the randomness of the generated text.
- `conversation` (Conversation, optional):  The conversation context to use.
- `return_conversation` (bool, optional): Whether to return the conversation object along with the generated text.

## Inner Functions

None.

## Examples

- **Example 1: Basic Text Generation**

    ```python
    import asyncio

    async def main():
        messages = [
            {"role": "user", "content": "Tell me a story about a brave knight."},
        ]
        async for chunk in AllenAI.create_async_generator(model='tulu3-405b', messages=messages):
            print(chunk)

    if __name__ == "__main__":
        asyncio.run(main())
    ```

- **Example 2: Using Conversation Context**

    ```python
    import asyncio

    async def main():
        conversation = Conversation(model='tulu3-405b')
        messages = [
            {"role": "user", "content": "What is your name?"},
            {"role": "assistant", "content": "My name is Bard."},
            {"role": "user", "content": "Nice to meet you, Bard. Tell me a joke."},
        ]
        async for chunk in AllenAI.create_async_generator(model='tulu3-405b', messages=messages, conversation=conversation):
            print(chunk)

    if __name__ == "__main__":
        asyncio.run(main())
    ```

- **Example 3: Using Optional Parameters**

    ```python
    import asyncio

    async def main():
        messages = [
            {"role": "user", "content": "Write a poem about a cat."},
        ]
        async for chunk in AllenAI.create_async_generator(model='tulu3-405b', messages=messages, temperature=0.7, top_p=0.9):
            print(chunk)

    if __name__ == "__main__":
        asyncio.run(main())
    ```