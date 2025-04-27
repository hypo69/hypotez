# CablyAI Provider

## Overview

This module provides the `CablyAI` class, which acts as a provider for the CablyAI chat service within the `hypotez` project. This provider enables the use of the CablyAI API for text generation and other conversational tasks. It inherits functionalities from the `OpenaiTemplate` base class, ensuring compatibility and consistent interaction within the project.

## Details

The `CablyAI` provider implements the necessary features for seamless integration with the CablyAI platform. It defines the API base URL, login URL, and other essential parameters required for authentication and communication. It also establishes the provider's capabilities, indicating support for streaming, system messages, and message history features. The `CablyAI` provider ensures correct authentication with the CablyAI API using an API key provided by the user.

## Classes

### `CablyAI`

**Description:** The `CablyAI` class represents the CablyAI provider, providing a convenient interface for interacting with the CablyAI service.

**Inherits:** `OpenaiTemplate`

**Attributes:**

- `url (str)`: The base URL for the CablyAI chat service.
- `login_url (str)`: The URL for logging into the CablyAI platform.
- `api_base (str)`: The base URL for the CablyAI API.
- `working (bool)`: Indicates whether the provider is functional (set to `True`).
- `needs_auth (bool)`: Indicates whether the provider requires authentication (set to `True`).
- `supports_stream (bool)`: Indicates whether the provider supports streaming responses (set to `True`).
- `supports_system_message (bool)`: Indicates whether the provider supports system messages (set to `True`).
- `supports_message_history (bool)`: Indicates whether the provider supports message history (set to `True`).

**Methods:**

- `create_async_generator(model: str, messages: Messages, api_key: str = None, stream: bool = False, **kwargs) -> AsyncResult`

    **Purpose:** Creates an asynchronous generator for sending requests to the CablyAI API.

    **Parameters:**

    - `model (str)`: The CablyAI model to use (e.g., 'gpt-3.5-turbo').
    - `messages (Messages)`: A list of messages representing the conversation history.
    - `api_key (str)`: The API key for authenticating with the CablyAI API. Defaults to `None`.
    - `stream (bool)`: Indicates whether to stream the response. Defaults to `False`.
    - `**kwargs`: Additional keyword arguments.

    **Returns:**

    - `AsyncResult`: An asynchronous result object representing the API response.

    **How the Method Works:**

    1.  Sets up headers for the API request, including authorization with the provided API key.
    2.  Calls the `create_async_generator` method of the parent `OpenaiTemplate` class, passing the necessary parameters.
    3.  Returns the `AsyncResult` object.

    **Examples:**

    ```python
    from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.CablyAI import CablyAI
    from hypotez.src.endpoints.gpt4free.g4f.models.Messages import Messages

    api_key = 'YOUR_CABLE_API_KEY'
    model = 'gpt-3.5-turbo'
    messages = Messages(
        [
            {"role": "user", "content": "Hello, how are you?"},
            {"role": "assistant", "content": "I am doing well. How about you?"},
        ]
    )

    cablyai = CablyAI()
    async_generator = cablyai.create_async_generator(model=model, messages=messages, api_key=api_key)
    ```