# Provider for Ails.ai

## Overview

This module implements the `Ails` class, a provider for the Ails.ai API. It inherits from the `AsyncGeneratorProvider` class, providing a mechanism for asynchronous generation of responses from the Ails.ai model. 

## Details

The `Ails` class utilizes the Ails.ai API to generate responses based on user input. It supports both GPT-3.5-turbo and GPT-4 models.  The class offers features for managing message history, handling proxy settings, and customizing parameters.

## Classes

### `Ails`

**Description:** This class provides an interface for interacting with the Ails.ai API.

**Inherits:** `AsyncGeneratorProvider`

**Attributes:**

- `url (str):` The base URL for the Ails.ai API.
- `working (bool):` Indicates if the provider is currently working.
- `supports_message_history (bool):` Indicates whether the provider supports message history.
- `supports_gpt_35_turbo (bool):` Indicates whether the provider supports the GPT-3.5-turbo model.

**Methods:**

#### `create_async_generator(model: str, messages: Messages, stream: bool, proxy: str = None, **kwargs) -> AsyncResult:`

**Purpose:** This method creates an asynchronous generator that yields responses from the Ails.ai model.

**Parameters:**

- `model (str):` The name of the model to use.
- `messages (Messages):` A list of messages containing the conversation history.
- `stream (bool):` Indicates whether to stream the response.
- `proxy (str, optional):` A proxy server to use. Defaults to `None`.
- `**kwargs:` Additional keyword arguments for the model.

**Returns:**

- `AsyncResult`: An asynchronous result object containing the generated response.

**How the Function Works:**

1. The function initializes the `ClientSession` with appropriate headers for communication with the Ails.ai API.
2. It constructs a JSON payload containing the model parameters, message history, and other settings.
3. It sends a POST request to the Ails.ai API endpoint using the `ClientSession`.
4. The function iterates over the streamed response lines, extracting the generated tokens and yielding them as a stream.
5. It handles potential errors by raising an exception if the response contains error codes.

#### `_hash(json_data: dict[str, str]) -> SHA256:`

**Purpose:** This helper function calculates a SHA256 hash of the provided JSON data.

**Parameters:**

- `json_data (dict[str, str]):` The JSON data to hash.

**Returns:**

- `SHA256`: The SHA256 hash of the JSON data.

**How the Function Works:**

1. It constructs a string combining the timestamp, message content, and other identifiers.
2. It encodes the string and calculates the SHA256 hash using the `hashlib` module.
3. It returns the hexadecimal representation of the hash.

#### `_format_timestamp(timestamp: int) -> str:`

**Purpose:** This helper function formats a timestamp.

**Parameters:**

- `timestamp (int):` The timestamp to format.

**Returns:**

- `str`: The formatted timestamp.

**How the Function Works:**

1. It extracts the last digit of the timestamp.
2. It adjusts the last digit based on its parity (even or odd).
3. It returns the formatted timestamp as a string.

## Parameter Details

- `model (str):` The name of the Ails.ai model to use. Currently, it supports "gpt-3.5-turbo."
- `messages (Messages):` A list of messages that represent the conversation history. Each message is a dictionary containing the role (e.g., "user" or "assistant") and content of the message.
- `stream (bool):`  Indicates whether to stream the response as it is generated. Set to `True` for real-time output.
- `proxy (str, optional):`  A proxy server to use for communication with the Ails.ai API. Defaults to `None`.
- `**kwargs:` Additional keyword arguments for the model. This allows for customization of parameters like temperature, top_p, etc.

## Examples

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Ails import Ails
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Example 1: Simple message generation
messages: Messages = [{"role": "user", "content": "Hello, how are you?"}]
provider = Ails()
async for token in provider.create_async_generator(model="gpt-3.5-turbo", messages=messages, stream=True):
    print(token, end="")

# Example 2: Generating response with a proxy
messages: Messages = [{"role": "user", "content": "What is the meaning of life?"}]
provider = Ails()
async for token in provider.create_async_generator(model="gpt-3.5-turbo", messages=messages, stream=True, proxy="http://myproxy:8080"):
    print(token, end="")

# Example 3: Using additional keyword arguments
messages: Messages = [{"role": "user", "content": "Write a poem about the stars."}]
provider = Ails()
async for token in provider.create_async_generator(model="gpt-3.5-turbo", messages=messages, stream=True, temperature=0.8):
    print(token, end="")
```

## Usage

1. **Import:** Import the `Ails` class from the `hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated` module.
2. **Instantiate:** Create an instance of the `Ails` class.
3. **Prepare Messages:** Prepare a list of messages (`Messages`) containing the conversation history.
4. **Generate Response:** Call the `create_async_generator` method with the desired model, messages, and any additional parameters.
5. **Process Response:** Iterate over the yielded tokens to receive the generated response.

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Ails import Ails
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

messages: Messages = [{"role": "user", "content": "What is the meaning of life?"}]
provider = Ails()
async for token in provider.create_async_generator(model="gpt-3.5-turbo", messages=messages, stream=True):
    print(token, end="")
```