# Theb Provider for FreeGPT-WebUI

## Overview

This module implements the `Theb` provider for FreeGPT-WebUI. The `Theb` provider leverages the `theb.ai` API to generate responses using the `gpt-3.5-turbo` model. It supports streaming responses, meaning that text is generated and displayed incrementally as it becomes available.

## Details

The `Theb` provider is a wrapper around the `theb.ai` API, providing a convenient way to interact with it from within FreeGPT-WebUI. The provider handles authentication (which is not required for `theb.ai`), sends messages to the API, and manages the streaming of responses.

## Classes

### `Theb` Provider

**Description**:  The `Theb` class represents a provider for the FreeGPT-WebUI application. It allows users to interact with the `theb.ai` API to generate responses using the `gpt-3.5-turbo` model.

**Inherits**:  This class inherits from the `Provider` base class in FreeGPT-WebUI, which provides a common framework for handling provider-specific logic.

**Attributes**:

- `url` (str):  The base URL of the `theb.ai` API.
- `model` (list):  A list containing the name of the model supported by the provider.
- `supports_stream` (bool):  Indicates whether the provider supports streaming responses.
- `needs_auth` (bool):  Indicates whether the provider requires authentication.

**Methods**:

- `_create_completion(model: str, messages: list, stream: bool, **kwargs)`:
    - **Purpose**: This method handles the creation of a response using the `theb.ai` API.
    - **Parameters**:
        - `model` (str): The name of the model to use for generation.
        - `messages` (list):  A list of messages comprising the conversation history.
        - `stream` (bool):  Indicates whether to stream the response.
        - `**kwargs`:  Additional keyword arguments to pass to the API.
    - **Returns**:  A generator that yields individual lines of the response text as they become available.
    - **How the Function Works**:
        - The method creates a configuration object containing the conversation messages and the selected model.
        - It then constructs a command to run the `theb.py` helper script, which interacts with the `theb.ai` API.
        - The helper script sends the configuration data to the API and captures the response.
        - The response is then yielded line by line to the caller using a generator.
    - **Example**:
        ```python
        >>> messages = [
        ...     {"role": "user", "content": "Hello, how are you?"},
        ... ]
        >>> response = _create_completion(model="gpt-3.5-turbo", messages=messages, stream=True)
        >>> for line in response:
        ...     print(line, end="")
        ... 
        I am an AI and do not have feelings, but I am here to assist you. How can I help you today? 
        ```


## Parameter Details

- `model` (str):  The name of the AI model to use for generating responses. For the `Theb` provider, the only supported model is `gpt-3.5-turbo`.
- `messages` (list):  A list of messages representing the conversation history. Each message is a dictionary with the following keys:
    - `role` (str):  Indicates the role of the message sender (e.g., "user" or "assistant").
    - `content` (str):  The text content of the message.
- `stream` (bool):  Specifies whether to stream the response text as it is generated. If `True`, the response is yielded incrementally; otherwise, it is returned as a single string.
- `**kwargs`:  Additional keyword arguments passed to the `theb.ai` API.


## Examples


```python
# Example of using the Theb provider to generate a response
from g4f.Provider.Providers.Theb import Theb

provider = Theb()
messages = [
    {"role": "user", "content": "What is the meaning of life?"},
]
response = provider._create_completion(model="gpt-3.5-turbo", messages=messages, stream=True)

for line in response:
    print(line, end="")
```

**Output**:

```
The meaning of life is a question that has been pondered by philosophers and theologians for centuries. There is no one definitive answer, as the meaning of life is ultimately up to each individual to decide. Some people find meaning in their relationships, their work, their faith, or their hobbies. Others find meaning in helping others, making a difference in the world, or simply experiencing life to the fullest.

Ultimately, the meaning of life is what you make of it. 
```