# GetGpt.py Documentation

## Overview

This module provides a `GetGpt` provider for the `g4f` framework, enabling interaction with the `chat.getgpt.world` service. It uses an encrypted communication mechanism to ensure secure data transmission.

## Details

The `GetGpt` provider utilizes the `chat.getgpt.world` API to generate responses. The code implements a mechanism to encrypt data before sending it to the API, which helps enhance security. 

## Classes

### `GetGpt`
**Description**: The `GetGpt` class acts as a provider for the `g4f` framework, defining methods for interacting with the `chat.getgpt.world` API. 

**Inherits**: 
- `BaseProvider`

**Attributes**:
- `url` (str): The base URL for the API.
- `model` (list): A list of supported models.
- `supports_stream` (bool): Indicates whether the provider supports streaming responses.
- `needs_auth` (bool): Indicates whether the provider requires authentication.

**Methods**:
- `_create_completion(model: str, messages: list, stream: bool, **kwargs)`: This method generates a completion response from the `chat.getgpt.world` API based on the provided parameters.

## Functions

### `_create_completion`

**Purpose**: This function handles the communication with the `chat.getgpt.world` API to generate responses based on user input.

**Parameters**:
- `model` (str): The model to use for generating the response.
- `messages` (list): A list of messages to be used for the conversation.
- `stream` (bool): Indicates whether to stream the response or return it as a single block.
- `**kwargs`: Additional parameters for fine-tuning the API request.

**Returns**:
- `Generator[str, None, None] | str`: A generator of response fragments (if `stream` is `True`) or a single response string (if `stream` is `False`).

**Raises Exceptions**:
- `requests.exceptions.RequestException`: If an error occurs during the API request.

**How the Function Works**:
- Encrypts the API request using AES encryption.
- Sends the encrypted request to the API endpoint.
- Processes the API response:
    - If `stream` is `True`, returns a generator of response fragments, allowing for partial output display.
    - If `stream` is `False`, returns a single string containing the full response.

**Inner Functions**:
- `encrypt(e)`: Encrypts the API request data using AES encryption.
- `pad_data(data: bytes)`: Pads the data to ensure it aligns with the block size of AES encryption.

**Examples**:

```python
>>> _create_completion(model='gpt-3.5-turbo', messages=['Hello, world!'], stream=False)
'Hello, world!'

>>> for fragment in _create_completion(model='gpt-3.5-turbo', messages=['What is the meaning of life?'], stream=True):
...    print(fragment)
The meaning of life is...

>>> _create_completion(model='gpt-3.5-turbo', messages=['Tell me a story about a cat.'], stream=False, temperature=0.5)
Once upon a time, in a quaint little town...
```

## Parameter Details

- `model` (str): The specific model to use for generating the response.
- `messages` (list): A list of message objects, representing the context of the conversation.
- `stream` (bool): Indicates whether to stream the response, allowing for partial output display.
- `**kwargs`: Additional parameters for fine-tuning the API request:
    - `frequency_penalty` (float):  A penalty applied to tokens that have appeared frequently in the text.
    - `max_tokens` (int): The maximum number of tokens to be generated in the response.
    - `presence_penalty` (float): A penalty applied to tokens that have already been present in the text.
    - `temperature` (float): Controls the randomness of the generated response, with higher values indicating more randomness.
    - `top_p` (float): Controls the probability distribution of the generated tokens.

## Examples

```python
# Using GetGpt provider
from g4f.Provider import GetGpt

provider = GetGpt()

# Sending a simple request
response = provider.create_completion(model='gpt-3.5-turbo', messages=['Hello, world!'])

print(response)

# Using streaming mode
for fragment in provider.create_completion(model='gpt-3.5-turbo', messages=['Tell me a joke.'], stream=True):
    print(fragment, end='')

# Using additional parameters
response = provider.create_completion(model='gpt-3.5-turbo', messages=['Write a poem about a cat'], temperature=0.8)

print(response)

```