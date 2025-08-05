# Provider: Forefront

## Overview

This module defines the `Forefront` class, which implements the `AbstractProvider` interface and represents a provider for the Forefront service. This service is a provider of GPT-4-like functionality with a focus on its ability to access the internet.

## Details

The `Forefront` provider leverages the Forefront API to interact with its service. The provider supports both streaming and non-streaming responses, and it is compatible with the `gpt-4` model. 

## Classes

### `Forefront`

**Description**: 
This class implements the `AbstractProvider` interface and represents the Forefront service.

**Inherits**:
    - `AbstractProvider`

**Attributes**:

    - `url (str)`:  The base URL for the Forefront API.
    - `supports_stream (bool)`: Indicates whether the provider supports streaming responses.
    - `supports_gpt_35_turbo (bool)`: Indicates whether the provider supports the GPT-3.5 Turbo model.

**Methods**:

    - `create_completion(model: str, messages: list[dict[str, str]], stream: bool, **kwargs: Any) -> CreateResult`

## Methods

### `create_completion`

**Purpose**: This method initiates a completion request using the Forefront API and streams the response.

**Parameters**:

    - `model (str)`: The model to use for completion (currently only supports `gpt-4`).
    - `messages (list[dict[str, str]])`: A list of messages, where each message is a dictionary with keys `"role"` and `"content"`. 
    - `stream (bool)`: Indicates whether to stream the response.
    - `**kwargs (Any)`: Additional keyword arguments.

**Returns**:

    - `CreateResult`: A generator that yields the response tokens in a streaming fashion. 

**Raises Exceptions**:

    - `requests.exceptions.RequestException`: Raised if there's an error during the API call.
    - `json.JSONDecodeError`: Raised if there's an error decoding the response.

**How the Function Works**:

    - The method constructs a JSON payload containing the message history and other necessary parameters. 
    - It sends a POST request to the Forefront API endpoint using the `requests` library.
    - The response is iterated through using the `iter_lines()` method. Each line is checked for the "delta" key, indicating a response token.
    - The token is decoded and yielded as a dictionary.

**Examples**:

    ```python
    from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Forefront import Forefront

    # Create a Forefront instance
    provider = Forefront()

    # Example messages for the chat history
    messages = [
        {"role": "user", "content": "Hello, world!"},
        {"role": "assistant", "content": "Hello!"},
    ]

    # Initiate a completion request with streaming enabled
    completion = provider.create_completion(model="gpt-4", messages=messages, stream=True)

    # Iterate through the response tokens
    for token in completion:
        print(token)
    ```