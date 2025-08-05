# Wuguokai Provider

## Overview

This module provides the `Wuguokai` class, which implements the `AbstractProvider` interface for interacting with the Wuguokai API, a free GPT-3.5-turbo-like service. This provider is deprecated and no longer functional, as the Wuguokai API has been discontinued.

## Details

The `Wuguokai` class allows users to send text prompts to the Wuguokai API and receive responses. However, it is crucial to note that the Wuguokai API is no longer available.  This class is preserved as a reference for historical purposes.

## Classes

### `Wuguokai`

**Description**: This class represents a provider for the Wuguokai API. It implements the `AbstractProvider` interface and defines methods for generating responses from the Wuguokai API.

**Inherits**: `AbstractProvider`

**Attributes**:

- `url` (str): Base URL for the Wuguokai API.
- `supports_gpt_35_turbo` (bool): Indicates whether the provider supports GPT-3.5-turbo.
- `working` (bool): Indicates whether the provider is currently functional.

**Methods**:

#### `create_completion`

**Purpose**: This method handles the interaction with the Wuguokai API to generate responses based on provided prompts. It is responsible for formatting the prompt, sending a request to the API, and parsing the response.

**Parameters**:

- `model` (str): The model to use for generating responses.
- `messages` (list[dict[str, str]]): A list of messages representing the conversation history.
- `stream` (bool): Whether to stream the response.
- `**kwargs` (Any): Additional keyword arguments for the API request.

**Returns**:

- `CreateResult`: A result object containing the generated response.

**Raises Exceptions**:

- `Exception`: If the API request fails or returns an error.

**Inner Functions**:

None

**How the Function Works**:

1. Formats the prompt using `format_prompt` function.
2. Constructs the API request headers and data.
3. Sends a POST request to the Wuguokai API endpoint.
4. Parses the response and yields the generated text.

**Examples**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Wuguokai import Wuguokai

provider = Wuguokai()
messages = [
    {"role": "user", "content": "Hello!"},
]
response = provider.create_completion(model="gpt-3.5-turbo", messages=messages, stream=False)
for chunk in response:
    print(chunk)
```