# HailuoAI Provider

## Overview

This module implements the `HailuoAI` provider, which interacts with the Hailuo AI API for generating responses using their MiniMax model. The `HailuoAI` class inherits from `AsyncAuthedProvider` and `ProviderModelMixin`, enabling asynchronous communication with the API and providing support for different model variations.

## Details

The `HailuoAI` provider offers features including:

- **Asynchronous communication:** Allows for efficient interaction with the Hailuo AI API using `aiohttp`.
- **Model selection:**  Provides support for the `MiniMax` model as the default option.
- **Authentication:**  Handles authentication with Hailuo AI using an API token.
- **Stream processing:** Enables streaming of responses, allowing users to receive partial results as they become available.
- **Conversation management:** Manages conversation context and provides mechanisms for creating and maintaining ongoing conversations with the Hailuo AI model.

## Classes

### `Conversation`

**Description:**

- Represents a conversation with the Hailuo AI model.

**Attributes:**

- `token` (str): The user's authentication token for interacting with the API.
- `chatID` (str): The unique ID of the current conversation.
- `characterID` (str, optional):  The ID of the AI persona (default: 1). 

### `HailuoAI`

**Description:**

- This class implements the Hailuo AI provider, providing the core functionality for communication with the Hailuo AI API.
- Inherits from `AsyncAuthedProvider` and `ProviderModelMixin`.

**Attributes:**

- `label` (str): Label identifying the provider (e.g., "Hailuo AI").
- `url` (str): The base URL of the Hailuo AI API.
- `working` (bool): Flag indicating whether the provider is active.
- `use_nodriver` (bool): Flag indicating whether to use a headless browser.
- `supports_stream` (bool): Flag indicating whether the provider supports streaming responses.
- `default_model` (str): The default model to use with the provider (e.g., "MiniMax").

**Methods:**

### `on_auth_async`

**Purpose:**

- Handles authentication with the Hailuo AI API using a token.
- Returns an iterator that yields the authentication status and relevant details.

**Parameters:**

- `proxy` (str, optional):  Proxy server to use (optional).
- `kwargs`: Additional keyword arguments for customizing authentication.

**Returns:**

- `AsyncIterator`: An asynchronous iterator that yields the authentication status and information.

**Raises:**

- `Exception`: If an error occurs during the authentication process.

### `create_authed`

**Purpose:**

- Creates a conversation with the Hailuo AI model using the provided authentication details and messages.
- Returns an asynchronous iterator that yields the generated responses.

**Parameters:**

- `model` (str): The model to use for generating responses (e.g., "MiniMax").
- `messages` (Messages): A list of messages comprising the conversation history.
- `auth_result` (AuthResult): The authentication result from the `on_auth_async` method.
- `return_conversation` (bool, optional):  Flag indicating whether to return a `Conversation` object (default: `False`).
- `conversation` (Conversation, optional): An existing `Conversation` object to continue with (optional).
- `kwargs`: Additional keyword arguments for customizing the conversation.

**Returns:**

- `AsyncResult`: An asynchronous iterator that yields the generated responses.

**Raises:**

- `Exception`: If an error occurs during the creation of the conversation.

**Examples:**

```python
# Example of using HailuoAI provider
from hypotez.src.endpoints.gpt4free.g4f.Provider.mini_max.HailuoAI import HailuoAI
from hypotez.src.endpoints.gpt4free.g4f.Provider.mini_max.HailuoAI import Conversation
from hypotez.src.endpoints.gpt4free.g4f.Provider.base_provider import Messages
from hypotez.src.endpoints.gpt4free.g4f.Provider.response import AuthResult
from hypotez.src.endpoints.gpt4free.g4f.Provider.mini_max.crypt import CallbackResults

# Mocking some values:
mock_auth_result = AuthResult(
    **{'token': 'YOUR_API_TOKEN', 'path_and_query': '/some/api/endpoint', 'timestamp': 1689791600}
)
mock_messages = Messages(
    user="Hello, how are you?",
    assistant="I am doing well, thanks for asking. How about you?",
)

async def main():
    hailuoai_provider = HailuoAI()
    async for result in hailuoai_provider.create_authed(
        model="MiniMax", messages=mock_messages, auth_result=mock_auth_result
    ):
        print(f"Response: {result}")
    
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## Inner Functions

- No inner functions are defined within the `HailuoAI` class.

## How the Provider Works

- The `HailuoAI` provider utilizes the `AsyncAuthedProvider` base class to handle authentication and asynchronous communication with the Hailuo AI API.
- It uses a `ClientSession` from the `aiohttp` library to send HTTP requests to the API.
- The `create_authed` method constructs a conversation with the API based on the provided authentication details and messages.
- It sends a POST request to the API endpoint and handles the response, streaming the generated text as it arrives.
- It uses the `json.loads` method to decode the responses and extract the relevant information, such as the generated text or conversation ID.
- The `on_auth_async` method handles the authentication process with the Hailuo AI API, returning an iterator that yields the authentication status and relevant details.
- The provider uses a dedicated header (`yy`) for authentication purposes, generated using the `generate_yy_header` function.

## Examples

```python
# Example:
from hypotez.src.endpoints.gpt4free.g4f.Provider.mini_max.HailuoAI import HailuoAI
from hypotez.src.endpoints.gpt4free.g4f.Provider.mini_max.HailuoAI import Conversation
from hypotez.src.endpoints.gpt4free.g4f.Provider.base_provider import Messages
from hypotez.src.endpoints.gpt4free.g4f.Provider.response import AuthResult

# Mock authentication result
mock_auth_result = AuthResult(
    **{'token': 'YOUR_API_TOKEN', 'path_and_query': '/some/api/endpoint', 'timestamp': 1689791600}
)

# Example conversation
conversation = Conversation(
    token='YOUR_API_TOKEN',
    chatID='your_chat_id',
    characterID=1
)

# Messages for the conversation
messages = Messages(
    user="Hello, how are you today?",
    assistant="I am doing well, thank you for asking. How about you?",
)

# Create a HailuoAI provider instance
hailuoai_provider = HailuoAI()

# Generate a response using the provider
async for result in hailuoai_provider.create_authed(
    model="MiniMax",
    messages=messages,
    auth_result=mock_auth_result,
    return_conversation=True,
    conversation=conversation,
):
    if isinstance(result, str):
        print(f"Response: {result}")
    elif isinstance(result, Conversation):
        print(f"Updated Conversation: {result.__dict__}")
    else:
        print(f"Unknown result type: {result}")
```
```python
# Another example of using the HailuoAI provider:

# Mocking some values:
mock_auth_result = AuthResult(
    **{'token': 'YOUR_API_TOKEN', 'path_and_query': '/some/api/endpoint', 'timestamp': 1689791600}
)

# Example of a conversation
mock_messages = Messages(
    user="Hello, how are you?",
    assistant="I am doing well, thanks for asking. How about you?",
)

# Creating a HailuoAI provider instance
hailuoai_provider = HailuoAI()

# Generating responses
async for result in hailuoai_provider.create_authed(
    model="MiniMax",
    messages=mock_messages,
    auth_result=mock_auth_result,
    return_conversation=True,
    conversation=None,
):
    print(f"Response: {result}")
```

## Parameter Details

- `token` (str): The user's API token for authentication with the Hailuo AI API.
- `chatID` (str): The unique ID of the current conversation.
- `characterID` (str, optional): The ID of the AI persona (default: 1).
- `model` (str): The specific model to use for generating responses (e.g., "MiniMax").
- `messages` (Messages): A list of messages comprising the conversation history.
- `auth_result` (AuthResult): The authentication result from the `on_auth_async` method.
- `return_conversation` (bool, optional): Flag indicating whether to return a `Conversation` object (default: `False`).
- `conversation` (Conversation, optional): An existing `Conversation` object to continue with (optional).
- `proxy` (str, optional): Proxy server to use (optional).
- `kwargs`: Additional keyword arguments for customizing the interaction with the Hailuo AI API.

## Exceptions

- `Exception`: Generic exception for errors during authentication or communication with the API.
- `json.JSONDecodeError`: Exception for errors encountered while decoding JSON responses from the API.


```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.mini_max.HailuoAI import HailuoAI
from hypotez.src.endpoints.gpt4free.g4f.Provider.mini_max.HailuoAI import Conversation
from hypotez.src.endpoints.gpt4free.g4f.Provider.base_provider import Messages
from hypotez.src.endpoints.gpt4free.g4f.Provider.response import AuthResult

# Mock authentication result
mock_auth_result = AuthResult(
    **{'token': 'YOUR_API_TOKEN', 'path_and_query': '/some/api/endpoint', 'timestamp': 1689791600}
)

# Mock a conversation
conversation = Conversation(
    token='YOUR_API_TOKEN',
    chatID='your_chat_id',
    characterID=1
)

# Example messages for the conversation
messages = Messages(
    user="Hello, how are you today?",
    assistant="I am doing well, thank you for asking. How about you?",
)

# Create a HailuoAI provider instance
hailuoai_provider = HailuoAI()

# Attempt to generate a response
async for result in hailuoai_provider.create_authed(
    model="MiniMax",
    messages=messages,
    auth_result=mock_auth_result,
    return_conversation=True,
    conversation=conversation,
):
    if isinstance(result, str):
        print(f"Response: {result}")
    elif isinstance(result, Conversation):
        print(f"Updated Conversation: {result.__dict__}")
    else:
        print(f"Unknown result type: {result}")