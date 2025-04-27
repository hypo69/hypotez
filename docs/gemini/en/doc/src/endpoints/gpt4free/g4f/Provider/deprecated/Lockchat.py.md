# Lockchat Provider

## Overview

This module provides the `Lockchat` class, which implements the `AbstractProvider` interface for interacting with the Lockchat API. 

## Details

The `Lockchat` class is a provider that enables communication with the Lockchat API for generating text completions. It supports both streaming and non-streaming responses. This module provides a means to utilize Lockchat's AI capabilities within the `hypotez` project. 

## Classes

### `Lockchat`

**Description**: This class represents a provider for interacting with the Lockchat API. It inherits from `AbstractProvider` and provides methods for sending requests to the Lockchat API and receiving responses.

**Inherits**: `AbstractProvider`

**Attributes**:

- `url (str)`: Base URL for the Lockchat API.
- `supports_stream (bool)`: Indicates whether the provider supports streaming responses.
- `supports_gpt_35_turbo (bool)`: Indicates whether the provider supports the `gpt-3.5-turbo` model.
- `supports_gpt_4 (bool)`: Indicates whether the provider supports the `gpt-4` model.

**Methods**:

- `create_completion(model: str, messages: list[dict[str, str]], stream: bool, **kwargs: Any) -> CreateResult`

## Functions

### `create_completion`

**Purpose**: This function sends a request to the Lockchat API to generate a text completion based on the provided model, messages, and other parameters. It supports both streaming and non-streaming responses.

**Parameters**:

- `model (str)`: The name of the language model to use for generating text completions.
- `messages (list[dict[str, str]])`: A list of messages that represent the conversation history. Each message is a dictionary with the following keys:
    - `role (str)`: The role of the speaker (e.g., "user", "assistant").
    - `content (str)`: The text content of the message.
- `stream (bool)`:  Indicates whether to receive the response in a streaming format.
- `kwargs (Any)`: Additional keyword arguments that can be passed to the Lockchat API.

**Returns**:

- `CreateResult`: An object containing the result of the text completion generation.

**Raises Exceptions**:

- `Exception`: If an error occurs during the API request.

**Inner Functions**: None

**How the Function Works**:

1. Constructs a payload for the API request, including the model, messages, stream setting, and any additional keyword arguments.
2. Sets up the request headers with a user-agent string.
3. Sends a POST request to the Lockchat API endpoint for generating completions.
4. Handles the API response:
    - If the API response contains an error, raises an exception.
    - If the API response is successful, iterates through the response lines and yields the generated tokens.
    - If the API response contains an error indicating that the specified model does not exist, logs an error message and retries the request. 

**Examples**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated import Lockchat

provider = Lockchat()

model = "gpt-3.5-turbo"
messages = [
    {"role": "user", "content": "Hello, how are you?"},
    {"role": "assistant", "content": "I am doing well, thank you for asking."},
]

result = provider.create_completion(model=model, messages=messages, stream=False)
print(result)

# Output:
# { ... }

```

## Parameter Details

- `model (str)`: The language model to use for text completion.
- `messages (list[dict[str, str]])`: A list of messages that represent the conversation history.
- `stream (bool)`: Indicates whether to receive the response in a streaming format.
- `kwargs (Any)`: Additional keyword arguments that can be passed to the Lockchat API, such as `temperature` for controlling the creativity of the generated response.

## Examples 

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated import Lockchat

provider = Lockchat()

model = "gpt-4"  # Using the gpt-4 model
messages = [
    {"role": "user", "content": "Write a short poem about a cat."},
]

result = provider.create_completion(model=model, messages=messages, stream=False)
print(result)

# Output (example):
# {
#     "choices": [
#         {
#             "finish_reason": "stop",
#             "index": 0,
#             "message": {
#                 "content": "A furry friend, with eyes so bright,\n"
#                             "A purring sound, a soft delight.\n"
#                             "With whiskers twitching, tail a-swish,\n"
#                             "A gentle creature, a playful wish.",
#                 "role": "assistant"
#             }
#         }
#     ],
#     "created": 1701050044,
#     "id": "cmpl-7652568171237634",
#     "model": "gpt-4",
#     "object": "chat.completion"
# }
```

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated import Lockchat

provider = Lockchat()

model = "gpt-3.5-turbo"  # Using the gpt-3.5-turbo model
messages = [
    {"role": "user", "content": "What is the capital of France?"},
]

result = provider.create_completion(model=model, messages=messages, stream=True)

for token in result:
    print(token, end="")

# Output (example):
# Paris 
```