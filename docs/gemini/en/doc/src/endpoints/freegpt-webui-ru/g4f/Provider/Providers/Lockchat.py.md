# Lockchat Provider Documentation

## Overview

This module provides the `Lockchat` provider for the `g4f` application, enabling interaction with the `Lockchat` API for generating text using GPT models.

## Details

The `Lockchat` provider utilizes the `requests` library to send requests to the `Lockchat` API endpoint and receive responses in a streaming format. It supports both `gpt-4` and `gpt-3.5-turbo` models.

## Classes

### `Lockchat`

**Description**: This class defines the `Lockchat` provider for `g4f`.

**Inherits**: None

**Attributes**:
- `url` (str): The base URL for the `Lockchat` API.
- `model` (list): A list of supported models for the `Lockchat` API.
- `supports_stream` (bool): Indicates whether the provider supports streaming responses.
- `needs_auth` (bool): Indicates whether the provider requires authentication.

**Methods**:

#### `_create_completion`

**Purpose**: This function sends a request to the `Lockchat` API for text completion and yields streamed response tokens.

**Parameters**:
- `model` (str): The GPT model to use for text completion.
- `messages` (list): A list of messages to be used as context for the completion.
- `stream` (bool): Indicates whether to stream the response.
- `temperature` (float, optional): The temperature parameter for the GPT model. Defaults to 0.7.

**Returns**:
- `Generator[str, None, None]`: A generator that yields individual text tokens from the streamed response.

**Raises Exceptions**:
- `Exception`: If an error occurs during the API request or response processing.

**How the Function Works**:
1. The function constructs a payload dictionary with the necessary parameters for the API request.
2. It sends a POST request to the `Lockchat` API endpoint with the payload and specified headers.
3. The response is iterated line by line using `response.iter_lines()`.
4. Each line is checked for specific tokens indicating errors or content data.
5. If an error token is encountered, a recursive call is made to retry the request.
6. If a content token is found, the JSON data is decoded and the `content` delta is extracted and yielded as a text token.

**Examples**:
```python
# Example 1: Using the `gpt-4` model with streaming enabled
tokens = _create_completion(model='gpt-4', messages=[{'role': 'user', 'content': 'Hello, world!'}] , stream=True)
for token in tokens:
    print(token, end='')

# Example 2: Using the `gpt-3.5-turbo` model with streaming disabled
completion = _create_completion(model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': 'What is the meaning of life?'}], stream=False)
print(completion)
```

## Parameter Details

- `model` (str): The name of the GPT model to use for text generation.
- `messages` (list): A list of message dictionaries representing the conversation history.
- `stream` (bool): Indicates whether to stream the response.
- `temperature` (float): The temperature parameter for the GPT model, controlling the randomness of the generated text.

## Examples

```python
# Example 1: Generate text using the `gpt-4` model with streaming enabled
messages = [{'role': 'user', 'content': 'Hello, world!'}]
for token in Lockchat._create_completion(model='gpt-4', messages=messages, stream=True):
    print(token, end='')

# Example 2: Generate text using the `gpt-3.5-turbo` model with streaming disabled
messages = [{'role': 'user', 'content': 'What is the meaning of life?'}]
completion = Lockchat._create_completion(model='gpt-3.5-turbo', messages=messages, stream=False)
print(completion)
```