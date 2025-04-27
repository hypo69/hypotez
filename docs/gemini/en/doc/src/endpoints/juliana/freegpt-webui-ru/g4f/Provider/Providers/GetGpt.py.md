# GetGpt.py

## Overview

This module provides functionality for interacting with the `GetGPT` API for generating text using the `gpt-3.5-turbo` model. It defines the necessary parameters and functions for communication with the API, including encryption and stream handling.

## Details

The module utilizes the `requests` library to send requests to the GetGPT API and handles stream responses for real-time text generation. Encryption is implemented using the `Crypto.Cipher` module to secure data exchange with the API. 

The module utilizes the `gpt-3.5-turbo` model for text generation. The `_create_completion` function handles communication with the GetGPT API, sending messages and receiving streaming responses. The `encrypt` function is used to encrypt sensitive data before sending to the API.


## Functions

### `_create_completion`

**Purpose**: This function handles communication with the GetGPT API to create text completions using the `gpt-3.5-turbo` model. It sends a request with user messages, model parameters, and a unique identifier (`uuid`). It then receives streaming responses from the API and yields the generated text chunks.

**Parameters**:

- `model` (str): The model to use for text generation (e.g., `gpt-3.5-turbo`).
- `messages` (list): A list of messages to send to the API.
- `stream` (bool): Indicates whether to use streaming mode for text generation.
- `**kwargs`: Additional keyword arguments to customize model parameters (e.g., `temperature`, `max_tokens`).

**Returns**:

- Generator: A generator that yields the generated text chunks.

**Raises Exceptions**:

- `Exception`: If an error occurs during communication with the GetGPT API.


**How the Function Works**:

1. The `_create_completion` function first defines two nested functions: `encrypt` and `pad_data`.
2. `encrypt` function encrypts the data before sending it to the API. It uses the AES cipher with a random key and initialization vector.
3. `pad_data` function pads the data to align with the AES block size.
4.  The function then defines the headers for the request, including the `Content-Type`, `Referer`, and `user-agent`.
5.  The function builds a JSON payload with the messages, model parameters, and `uuid`.
6.  The function encrypts the JSON payload using the `encrypt` function.
7.  The function sends a POST request to the GetGPT API with the encrypted payload and stream parameters.
8.  It iterates through the lines of the streaming response and checks for the `content` field.
9.  If the `content` field is present, it decodes the response, extracts the generated text chunk, and yields it.

**Examples**:

```python
messages = [
    {'role': 'user', 'content': 'Hello, world!'},
    {'role': 'assistant', 'content': 'Hi there!'},
]
for chunk in _create_completion(model='gpt-3.5-turbo', messages=messages, stream=True):
    print(chunk, end='')
```

### `pad_data`

**Purpose**: This function pads the given data to align with the AES block size.

**Parameters**:

- `data` (bytes): The data to be padded.

**Returns**:

- bytes: The padded data.

**How the Function Works**:

1. The function calculates the padding size required to align the data with the AES block size.
2. It creates a padding string with the calculated padding size, filled with the padding size value.
3. It concatenates the original data with the padding string and returns the result.

**Examples**:

```python
data = b'Hello, world!'
padded_data = pad_data(data)
print(f'Original data: {data}')
print(f'Padded data: {padded_data}')
```

### `encrypt`

**Purpose**: This function encrypts the given data using the AES cipher with a random key and initialization vector.

**Parameters**:

- `e` (str): The data to be encrypted.

**Returns**:

- str: The encrypted data in hexadecimal format.

**How the Function Works**:

1. The function generates a random key and initialization vector.
2. It encodes the data to be encrypted and uses the AES cipher in CBC mode with the generated key and initialization vector.
3. It encrypts the data and returns the ciphertext in hexadecimal format concatenated with the key and initialization vector in hexadecimal format.

**Examples**:

```python
data = 'Hello, world!'
encrypted_data = encrypt(data)
print(f'Original data: {data}')
print(f'Encrypted data: {encrypted_data}')
```

## Parameter Details

- `model` (str): The model to use for text generation (e.g., `gpt-3.5-turbo`).
- `messages` (list): A list of messages to send to the API.
- `stream` (bool): Indicates whether to use streaming mode for text generation.
- `frequency_penalty` (float, optional): A penalty for using the same words over and over again. Defaults to 0.
- `max_tokens` (int, optional): The maximum number of tokens to generate. Defaults to 4000.
- `presence_penalty` (float, optional): A penalty for using words that have already been used in the response. Defaults to 0.
- `temperature` (float, optional): Controls the randomness of the generated text. Defaults to 1.
- `top_p` (float, optional): Controls the probability of selecting the next token. Defaults to 1.
- `uuid` (str): A unique identifier to track the conversation.

## Examples

```python
# Example 1: Generate text with default parameters
messages = [
    {'role': 'user', 'content': 'What is the meaning of life?'},
]
for chunk in _create_completion(model='gpt-3.5-turbo', messages=messages, stream=True):
    print(chunk, end='')

# Example 2: Generate text with custom parameters
messages = [
    {'role': 'user', 'content': 'Write a poem about a cat.'},
]
for chunk in _create_completion(
    model='gpt-3.5-turbo',
    messages=messages,
    stream=True,
    temperature=0.5,
    max_tokens=100,
):
    print(chunk, end='')
```