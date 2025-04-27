# GithubCopilot Provider for GPT4Free

## Overview

This module implements the `GithubCopilot` class, a provider for GPT4Free that utilizes the GitHub Copilot service. It allows users to interact with GitHub Copilot's AI model for code generation, completion, and other coding tasks.

## Details

The `GithubCopilot` class inherits from `AsyncGeneratorProvider` and `ProviderModelMixin`. It is designed to be used asynchronously with GPT4Free's request handling system. This provider requires authentication with GitHub Copilot and supports streaming responses.

## Classes

### `Conversation`

**Description**: This class represents a conversation with GitHub Copilot. It stores the conversation ID, which is used to identify and maintain the context of the conversation.

**Inherits**: `BaseConversation`

**Attributes**:

- `conversation_id`: The unique identifier for the conversation.

**Methods**:

- `__init__(self, conversation_id: str)`: Initializes a new `Conversation` object with the provided conversation ID.

### `GithubCopilot`

**Description**: This class implements the provider for interacting with GitHub Copilot. It defines the provider's label, URL, authentication requirements, supported models, and provides methods for handling requests and responses.

**Inherits**: `AsyncGeneratorProvider`, `ProviderModelMixin`

**Attributes**:

- `label`: The human-readable name of the provider ("GitHub Copilot").
- `url`: The base URL for the GitHub Copilot service ("https://github.com/copilot").
- `working`: Indicates whether the provider is currently working (set to `True`).
- `needs_auth`: Indicates whether the provider requires authentication (set to `True`).
- `supports_stream`: Indicates whether the provider supports streaming responses (set to `True`).
- `default_model`: The default model used by the provider ("gpt-4o").
- `models`: A list of supported models by the provider (includes `default_model` and other models: "o1-mini", "o1-preview", "claude-3.5-sonnet").

**Methods**:

- `create_async_generator(cls, model: str, messages: Messages, stream: bool = False, api_key: str = None, proxy: str = None, cookies: Cookies = None, conversation_id: str = None, conversation: Conversation = None, return_conversation: bool = False, **kwargs) -> AsyncResult`: This method handles the asynchronous request to GitHub Copilot. It builds the request based on the provided parameters, including model, messages, API key, proxy, cookies, conversation ID, and other optional parameters. It uses `aiohttp` to make the request to the GitHub Copilot API and iteratively processes the streaming response, yielding each line of the response content.

**Inner Functions**:

- None

**How the Function Works**: 
The `create_async_generator` method first sets up the necessary headers and parameters based on the input values. It then performs the following actions:

1. **Get API Token:** If the `api_key` is not provided, it fetches a new token from the GitHub Copilot API.
2. **Create Conversation:** If the `conversation` object is provided, it uses the existing conversation ID. Otherwise, it creates a new conversation by sending a POST request to the API and extracts the conversation ID from the response.
3. **Prepare Request Body:**  It formats the `messages` into a suitable format for GitHub Copilot, taking into account the `stream` parameter and the last user message. It constructs the request body (`json_data`) with the formatted content, intent, references, context, current URL, and other necessary parameters.
4. **Send Request and Stream Response:** It sends a POST request to the GitHub Copilot API with the `json_data` and the required headers. It iteratively processes the streaming response, extracting the `body` from each line and yielding it to the caller.

**Examples**:

```python
# Using GithubCopilot with a custom API key and a conversation ID
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.GithubCopilot import GithubCopilot, Conversation

api_key = "your_api_key"
conversation_id = "your_conversation_id"

async def main():
    async for response_line in GithubCopilot.create_async_generator(
        model="gpt-4o", messages=["Hello, world!"], api_key=api_key, conversation_id=conversation_id
    ):
        print(response_line)

# Creating a new conversation and getting the response
async def main():
    async for response_line in GithubCopilot.create_async_generator(
        model="gpt-4o", messages=["Hello, world!"], return_conversation=True
    ):
        if isinstance(response_line, Conversation):
            conversation_id = response_line.conversation_id
            print(f"New conversation ID: {conversation_id}")
        else:
            print(response_line)
```

## Parameter Details

- `model`: The model to use for the request (e.g., "gpt-4o", "o1-mini", "o1-preview", "claude-3.5-sonnet"). Defaults to the provider's `default_model`.
- `messages`: A list of messages to send to the provider. It is used to provide context and information for the request.
- `stream`: Indicates whether to receive the response in a streaming format. Defaults to `False`.
- `api_key`: Your API key for accessing the GitHub Copilot service. If not provided, it will be fetched automatically.
- `proxy`: A proxy server to use for the request. Defaults to `None`.
- `cookies`: A dictionary of cookies to send with the request. Defaults to `None`.
- `conversation_id`: The conversation ID to use for the request. If not provided, a new conversation will be created.
- `conversation`: A `Conversation` object representing the current conversation.
- `return_conversation`: Indicates whether to return a `Conversation` object with the conversation ID after the first response. Defaults to `False`.

## Examples

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.GithubCopilot import GithubCopilot, Conversation

# Example 1: Using a default model and a custom API key
async def main():
    api_key = "your_api_key"
    async for response_line in GithubCopilot.create_async_generator(
        model="gpt-4o", messages=["Hello, world!"], api_key=api_key
    ):
        print(response_line)

# Example 2: Using a different model and a conversation ID
async def main():
    conversation_id = "your_conversation_id"
    async for response_line in GithubCopilot.create_async_generator(
        model="o1-mini", messages=["Write a function to reverse a string"], conversation_id=conversation_id
    ):
        print(response_line)

# Example 3: Creating a new conversation and getting the response
async def main():
    async for response_line in GithubCopilot.create_async_generator(
        model="gpt-4o", messages=["Hello, world!"], return_conversation=True
    ):
        if isinstance(response_line, Conversation):
            conversation_id = response_line.conversation_id
            print(f"New conversation ID: {conversation_id}")
        else:
            print(response_line)
```