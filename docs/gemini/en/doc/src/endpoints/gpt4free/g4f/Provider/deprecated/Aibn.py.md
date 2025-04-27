# Aibn Provider Module

## Overview

This module provides the `Aibn` class, which implements an asynchronous generator provider for interacting with the Aibn.cc API. It handles sending requests, receiving responses, and iterating through the content of the response.

## Details

This module is part of the `hypotez` project and acts as a wrapper for accessing the Aibn.cc API, which allows users to utilize AI models for various tasks. 

The `Aibn` class inherits from the base `AsyncGeneratorProvider`, providing a common framework for interacting with different AI providers. It handles sending messages, receiving responses, and managing the communication with the Aibn.cc API.

## Classes

### `Aibn`

**Description**: 
This class implements an asynchronous generator provider for the Aibn.cc API. It handles the communication with the API, sending messages, and receiving responses.

**Inherits**: 
- `AsyncGeneratorProvider`

**Attributes**:

- `url` (str): URL of the Aibn.cc API.
- `working` (bool): Indicates whether the provider is currently active.
- `supports_message_history` (bool): Indicates whether the provider supports message history.
- `supports_gpt_35_turbo` (bool): Indicates whether the provider supports the GPT-3.5 Turbo model.

**Methods**:

#### `create_async_generator`

**Purpose**: This method creates an asynchronous generator for interacting with the Aibn.cc API. It sends messages to the API and receives responses, iterating through the content of the response.

**Parameters**:

- `model` (str): The name of the AI model to use.
- `messages` (Messages): A list of messages representing the conversation history.
- `proxy` (str, optional): A proxy server to use. Defaults to None.
- `timeout` (int, optional): Timeout for the request in seconds. Defaults to 120.

**Returns**:

- `AsyncResult`: An asynchronous result object containing the generated response.

**Raises Exceptions**:

- `Exception`: If an error occurs during communication with the Aibn.cc API.

**How the Function Works**:

1. The method initializes a `StreamSession` with the specified proxy and timeout.
2. It generates a timestamp and calculates a signature for the request using the `generate_signature` function.
3. The method sends a POST request to the Aibn.cc API endpoint with the messages, signature, and timestamp.
4. It iterates through the content of the response, decoding each chunk and yielding it as a string.

**Example**:

```python
# Example of using create_async_generator
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Aibn import Aibn
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Define a list of messages
messages: Messages = [
    {"role": "user", "content": "Hello, world!"},
]

# Create an instance of the Aibn class
aibn_provider = Aibn()

# Call create_async_generator to generate the response
async_result = await aibn_provider.create_async_generator(
    model="gpt-3.5-turbo", messages=messages
)

# Iterate through the response content
async for chunk in async_result:
    print(chunk)
```

## Functions

### `generate_signature`

**Purpose**: Generates a SHA256 signature for a message based on timestamp, message content, and a secret key.

**Parameters**:

- `timestamp` (int): Timestamp to include in the signature.
- `message` (str): Message content to include in the signature.
- `secret` (str, optional): Secret key used for signature generation. Defaults to "undefined".

**Returns**:

- `str`: The generated SHA256 signature in hexadecimal format.

**How the Function Works**:

1. The function concatenates the timestamp, message, and secret key into a string.
2. It encodes the string using UTF-8 encoding.
3. It calculates the SHA256 hash of the encoded string.
4. It returns the hash in hexadecimal format.

**Example**:

```python
# Example of using generate_signature
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Aibn import generate_signature

# Define a timestamp, message, and secret key
timestamp = int(time.time())
message = "Hello, world!"
secret = "my_secret_key"

# Generate the signature
signature = generate_signature(timestamp, message, secret)

# Print the signature
print(signature)
```