# Provider MyShell
## Overview
This module provides the `MyShell` class, which implements the `AbstractProvider` interface and represents a provider for the GPT-4 Free API using MyShell.ai.

## Details
The `MyShell` class leverages the MyShell.ai platform for generating text completions. It supports both GPT-3.5 Turbo and GPT-4 models, and it allows for stream-based completions, offering a more efficient and responsive experience. The class utilizes Selenium webdriver to interact with MyShell.ai, handling network requests and responses.

## Classes
### `class MyShell`
**Description**: The `MyShell` class provides an interface for interacting with the MyShell.ai API for generating text completions.

**Inherits**: `AbstractProvider`

**Attributes**:
- `url (str)`: The base URL for interacting with the MyShell.ai API.
- `working (bool)`: Indicates whether the provider is currently functioning.
- `supports_gpt_35_turbo (bool)`: Determines if the provider supports the GPT-3.5 Turbo model.
- `supports_stream (bool)`: Indicates whether the provider supports stream-based completions.

**Methods**:
- `create_completion(model: str, messages: Messages, stream: bool, proxy: str = None, timeout: int = 120, webdriver = None, **kwargs) -> CreateResult`: Generates a completion using the MyShell.ai API based on the provided model, messages, and stream settings.
    - **Purpose**: This method sends a request to the MyShell.ai API to generate a text completion based on the given model, messages, and stream parameters. It handles the web interaction using a WebDriverSession.
    - **Parameters**:
        - `model (str)`: The name of the model to use (e.g., "GPT-4").
        - `messages (Messages)`: A list of messages representing the conversation history.
        - `stream (bool)`: Whether to return the completion as a stream of chunks.
        - `proxy (str, optional)`: A proxy server to use for making the request. Defaults to `None`.
        - `timeout (int, optional)`: The maximum time to wait for a response. Defaults to `120` seconds.
        - `webdriver`: The WebDriver instance to use for interacting with the MyShell.ai website.
    - **Returns**: `CreateResult`: A generator that yields chunks of the completion text if `stream` is `True`, otherwise a single string containing the full completion.
    - **Raises Exceptions**: 
        - `None`
- `_format_prompt(messages: Messages) -> str`: Formats the prompt from the list of messages to be sent to the API.
    - **Purpose**: This method prepares the prompt message for the API request based on the conversation history.
    - **Parameters**: 
        - `messages (Messages)`: A list of messages representing the conversation history.
    - **Returns**: `str`: The formatted prompt message.
    - **Raises Exceptions**:
        - `None`


## Inner Functions
### `_format_prompt(messages: Messages) -> str`: 
This method takes a list of messages representing the conversation history and formats it into a string suitable for sending to the MyShell.ai API.
    - **Purpose**: This method takes a list of messages representing the conversation history and formats it into a string suitable for sending to the MyShell.ai API.
    - **Parameters**: 
        - `messages (Messages)`: A list of messages representing the conversation history.
    - **Returns**: `str`: The formatted prompt message.
    - **Raises Exceptions**:
        - `None`


## Parameter Details
- `model (str)`: The name of the language model to use for generating text (e.g., "gpt-3.5-turbo", "gpt-4").
- `messages (Messages)`: A list of messages representing the conversation history, where each message is a dictionary with `role` (user, assistant) and `content` (text of the message).
- `stream (bool)`: Determines if the completion should be returned as a stream of chunks or as a single string.
- `proxy (str, optional)`: A proxy server address to use for making the request. Defaults to `None`.
- `timeout (int, optional)`: The maximum time to wait for a response from the API. Defaults to 120 seconds.
- `webdriver`: The WebDriver instance to use for interacting with the MyShell.ai website.

## Examples
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.MyShell import MyShell
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Creating a MyShell provider instance
my_shell_provider = MyShell()

# Example messages for the conversation
messages: Messages = [
    {"role": "user", "content": "Hello, how are you?"},
    {"role": "assistant", "content": "I am doing well, thank you. How can I assist you today?"},
]

# Generating a completion with GPT-3.5 Turbo model and streaming enabled
completion = my_shell_provider.create_completion(
    model="gpt-3.5-turbo", messages=messages, stream=True
)

# Iterating through the streamed chunks of the completion
for chunk in completion:
    print(chunk)

# Alternatively, generate a completion without streaming
completion = my_shell_provider.create_completion(
    model="gpt-3.5-turbo", messages=messages, stream=False
)
print(completion)
```
```python
# Creating a driver instance (example with Chrome)
driver = Driver(Chrome)