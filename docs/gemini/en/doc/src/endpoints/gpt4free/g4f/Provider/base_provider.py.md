# Base Provider Module

## Overview

This module defines the base class for all GPT-4Free providers. It outlines the common functionality and structure that all providers should implement. 

## Details

The module provides the `BaseProvider` class, which serves as a blueprint for creating various GPT-4Free provider implementations.  Providers interact with GPT-4Free APIs, allowing users to access powerful language models and generate responses to user queries. 

## Classes

### `BaseProvider`

**Description**: This is the abstract base class for all GPT-4Free providers. It provides a common interface and structure for interacting with the GPT-4Free API.

**Inherits**:  `ABC`

**Attributes**:

- `api_key` (str): The GPT-4Free API key used for authentication.

**Methods**:

- `__init__(self, api_key: str = None, stream: bool = False, stream_timeout: int = 10, **kwargs: Any)`: Initializes a new `BaseProvider` instance.
    - **Parameters**:
        - `api_key` (str): The GPT-4Free API key.
        - `stream` (bool): Whether to enable streaming responses. Defaults to `False`.
        - `stream_timeout` (int): Timeout in seconds for streaming responses. Defaults to 10.
        - `**kwargs` (Any): Additional keyword arguments passed to the provider.
    - **Example**:
        ```python
        provider = BaseProvider(api_key='YOUR_API_KEY')
        ```
- `format_prompt(self, prompt: str) -> str`: Formats the user prompt before sending it to the GPT-4Free API.
    - **Parameters**:
        - `prompt` (str): The user prompt.
    - **Returns**:
        - `str`: The formatted prompt.
    - **Example**:
        ```python
        prompt = "What is the meaning of life?"
        formatted_prompt = provider.format_prompt(prompt)
        ```
- `get_response(self, prompt: str, **kwargs: Any) -> BaseConversation`: Sends a request to the GPT-4Free API and retrieves the generated response.
    - **Parameters**:
        - `prompt` (str): The user prompt.
        - `**kwargs` (Any): Additional keyword arguments passed to the API.
    - **Returns**:
        - `BaseConversation`: An object representing the generated response.
    - **Example**:
        ```python
        response = provider.get_response(prompt="What is the meaning of life?")
        ```
- `stream_response(self, prompt: str, **kwargs: Any) -> Streaming`: Sends a request to the GPT-4Free API and retrieves the generated response in a streaming format.
    - **Parameters**:
        - `prompt` (str): The user prompt.
        - `**kwargs` (Any): Additional keyword arguments passed to the API.
    - **Returns**:
        - `Streaming`: An object representing the streaming response.
    - **Example**:
        ```python
        stream = provider.stream_response(prompt="What is the meaning of life?")
        for chunk in stream:
            print(chunk)
        ```

## Functions

### `get_cookies`

**Purpose**: Retrieves cookies from a given URL.

**Parameters**:
- `url` (str): The URL to retrieve cookies from.

**Returns**:
- `dict`: A dictionary containing the retrieved cookies.

**Raises Exceptions**:
- `requests.exceptions.RequestException`: If an error occurs during the request.

**How the Function Works**:
- Uses the `requests` library to make a GET request to the specified URL.
- Extracts cookies from the response headers and returns them as a dictionary.

**Examples**:
- ```python
  cookies = get_cookies("https://www.example.com")
  ```

### `format_prompt`

**Purpose**: Formats the user prompt before sending it to the GPT-4Free API.

**Parameters**:
- `prompt` (str): The user prompt.

**Returns**:
- `str`: The formatted prompt.

**Raises Exceptions**:
- `None`: This function doesn't raise any exceptions.

**How the Function Works**:
- This function ensures that the prompt is properly formatted for the GPT-4Free API.

**Examples**:
- ```python
  prompt = "What is the meaning of life?"
  formatted_prompt = format_prompt(prompt)
  ```

### `_process_response`

**Purpose**:  Processes the response from the GPT-4Free API.

**Parameters**:
- `response_json` (dict): The JSON response from the GPT-4Free API.
- `stream` (bool): Whether the response was received in a streaming format.

**Returns**:
- `BaseConversation`: An object representing the generated response.

**Raises Exceptions**:
- `None`: This function doesn't raise any exceptions.

**How the Function Works**:
- Extracts relevant information from the JSON response.
- Creates a `BaseConversation` object containing the generated text, sources, and other relevant information.

**Examples**:
- ```python
  response = provider.get_response(prompt="What is the meaning of life?")
  ```

### `_get_conversation_response`

**Purpose**: Retrieves the generated response from the GPT-4Free API.

**Parameters**:
- `prompt` (str): The user prompt.
- `**kwargs` (Any): Additional keyword arguments passed to the API.

**Returns**:
- `BaseConversation`: An object representing the generated response.

**Raises Exceptions**:
- `Exception`: If an error occurs during the request.

**How the Function Works**:
- Makes a request to the GPT-4Free API using the `requests` library.
- Processes the response and returns a `BaseConversation` object.

**Examples**:
- ```python
  response = provider._get_conversation_response(prompt="What is the meaning of life?")
  ```

### `_get_stream_response`

**Purpose**: Retrieves the generated response from the GPT-4Free API in a streaming format.

**Parameters**:
- `prompt` (str): The user prompt.
- `**kwargs` (Any): Additional keyword arguments passed to the API.

**Returns**:
- `Streaming`: An object representing the streaming response.

**Raises Exceptions**:
- `Exception`: If an error occurs during the request.

**How the Function Works**:
- Makes a request to the GPT-4Free API using the `requests` library.
- Processes the streaming response and returns a `Streaming` object.

**Examples**:
- ```python
  stream = provider._get_stream_response(prompt="What is the meaning of life?")
  for chunk in stream:
      print(chunk)
  ```

## Parameter Details

- `api_key` (str): The GPT-4Free API key used for authentication.
- `stream` (bool): Whether to enable streaming responses. Defaults to `False`.
- `stream_timeout` (int): Timeout in seconds for streaming responses. Defaults to 10.
- `prompt` (str): The user prompt.
- `response_json` (dict): The JSON response from the GPT-4Free API.
- `url` (str): The URL to retrieve cookies from.

## Examples

### Basic Provider Usage

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.base_provider import BaseProvider

provider = BaseProvider(api_key="YOUR_API_KEY")

prompt = "What is the meaning of life?"

response = provider.get_response(prompt=prompt)

print(response.text)
```

### Streaming Response Usage

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.base_provider import BaseProvider

provider = BaseProvider(api_key="YOUR_API_KEY", stream=True)

prompt = "What is the meaning of life?"

stream = provider.stream_response(prompt=prompt)

for chunk in stream:
    print(chunk, end="")
```