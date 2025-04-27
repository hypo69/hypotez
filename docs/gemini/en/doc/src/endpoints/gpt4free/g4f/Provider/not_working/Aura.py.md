# Aura Provider

## Overview

This module provides the `Aura` class, which acts as an asynchronous generator provider for the OpenChat.team API. It extends the `AsyncGeneratorProvider` base class and implements asynchronous generation of responses from the Aura model.

## Details

The `Aura` class is designed to interact with the OpenChat.team API, enabling the retrieval of responses from the Aura model. It utilizes the `aiohttp` library for asynchronous HTTP requests and handles message formatting and processing.

## Classes

### `class Aura`

**Description**: This class represents the Aura provider for the OpenChat.team API. It inherits from `AsyncGeneratorProvider` and implements methods for asynchronous response generation.

**Inherits**: `AsyncGeneratorProvider`

**Attributes**:

- `url (str)`: Base URL for the OpenChat.team API.
- `working (bool)`: Flag indicating whether the provider is currently working or not.

**Methods**:

- `create_async_generator(model: str, messages: Messages, proxy: str = None, temperature: float = 0.5, max_tokens: int = 8192, webdriver = None, **kwargs) -> AsyncResult`: This method initiates an asynchronous process for generating responses from the Aura model.

#### `create_async_generator`

**Purpose**:  This method sets up the asynchronous generation of responses from the Aura model, utilizing the OpenChat.team API.

**Parameters**:

- `model (str)`: Name of the model (e.g., "openchat_3.6").
- `messages (Messages)`: A list of messages representing the conversation history.
- `proxy (str, optional)`: Optional proxy server to use for requests. Defaults to `None`.
- `temperature (float, optional)`: Controls the randomness of the generated responses. Defaults to `0.5`.
- `max_tokens (int, optional)`: Maximum number of tokens allowed in the response. Defaults to `8192`.
- `webdriver (Optional[webdriver.WebDriver], optional)`: Optional Selenium WebDriver instance to use for interacting with the browser. Defaults to `None`.
- `**kwargs`: Additional keyword arguments.

**Returns**:

- `AsyncResult`: An asynchronous result object representing the ongoing response generation process.

**Raises Exceptions**:

- `Exception`: If there's an error during the request or response processing.

**How the Function Works**:

1.  The method retrieves arguments from the browser using the `get_args_from_browser` function, which potentially uses a WebDriver instance for interaction.
2.  It creates an asynchronous `ClientSession` using the retrieved arguments.
3.  The method separates system messages from user messages in the provided `messages` list.
4.  It constructs a data dictionary containing the model information, messages, key, prompt, and temperature settings.
5.  It sends a POST request to the OpenChat.team API endpoint `/api/chat` with the prepared data.
6.  The method iterates through the chunks of the response content, decodes them, and yields each chunk to the `AsyncResult` object, enabling the asynchronous generation of the response.

**Examples**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.Aura import Aura
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Example usage with a simple message history
messages: Messages = [
    {"role": "user", "content": "Hello, how are you?"},
]

# Creating an asynchronous generator for Aura model responses
async_generator = Aura.create_async_generator(model="openchat_3.6", messages=messages)

# Iterating through the generated response chunks
async for chunk in async_generator:
    print(chunk) 

```

**Inner Functions**:

- `get_args_from_browser(url: str, webdriver: Optional[webdriver.WebDriver], proxy: str = None) -> Dict[str, Any]`: This function retrieves arguments for the `aiohttp.ClientSession` from the browser, potentially using a WebDriver instance for interaction.

**Parameter Details**:

- `model (str)`: The name of the model to use for generating responses. It is a key identifier for the model being requested.
- `messages (Messages)`: A list of messages representing the conversation history. This is used to provide context to the model.
- `proxy (str, optional)`: An optional proxy server to use for making requests. This can be helpful for bypassing network restrictions or improving network performance.
- `temperature (float, optional)`: A value that controls the randomness of the generated responses. A higher temperature will result in more creative and unpredictable responses, while a lower temperature will produce more conservative and predictable responses.
- `max_tokens (int, optional)`: The maximum number of tokens allowed in the generated response. This limits the length of the response and helps to prevent excessive generation time.
- `webdriver (Optional[webdriver.WebDriver], optional)`: An optional Selenium WebDriver instance to use for interacting with the browser. This allows for interaction with web pages and extraction of data.
- `**kwargs`: Additional keyword arguments. This allows for flexibility and the inclusion of other parameters specific to the provider or the API.

##  Class Methods

- `create_async_generator`: This method is responsible for initiating the asynchronous generation of responses from the OpenChat.team API. It uses the `aiohttp` library for making HTTP requests and handles the processing and formatting of responses.

## Parameter Details

- `model (str)`: This parameter specifies the name of the model to use for generating responses. It is a key identifier for the model being requested.
- `messages (Messages)`: This parameter represents the conversation history, which is used to provide context to the model. 
- `proxy (str, optional)`: An optional proxy server that can be used for making requests. This can be helpful for bypassing network restrictions or improving network performance.
- `temperature (float, optional)`: A value that controls the randomness of the generated responses. A higher temperature will result in more creative and unpredictable responses, while a lower temperature will produce more conservative and predictable responses.
- `max_tokens (int, optional)`: The maximum number of tokens allowed in the generated response. This limits the length of the response and helps to prevent excessive generation time.
- `webdriver (Optional[webdriver.WebDriver], optional)`: An optional Selenium WebDriver instance that can be used for interacting with the browser. This allows for interaction with web pages and extraction of data.
- `**kwargs`: Additional keyword arguments. This allows for flexibility and the inclusion of other parameters specific to the provider or the API.

## Examples

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.Aura import Aura
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Example usage with a simple message history
messages: Messages = [
    {"role": "user", "content": "Hello, how are you?"},
]

# Creating an asynchronous generator for Aura model responses
async_generator = Aura.create_async_generator(model="openchat_3.6", messages=messages)

# Iterating through the generated response chunks
async for chunk in async_generator:
    print(chunk) 
```