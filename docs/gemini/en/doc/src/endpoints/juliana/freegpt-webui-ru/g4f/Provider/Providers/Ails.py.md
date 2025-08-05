# Provider: Ails

## Overview

This module provides functionality for generating responses using the Ails AI model. 

## Details

The module utilizes the `_create_completion` function to interact with the Ails API and generate text responses. The function sends a request to the API with the specified parameters, such as the model, messages, temperature, and stream flag. 

## Classes

### `Utils`

**Description**: The `Utils` class provides utility functions for hashing data and formatting timestamps.

**Attributes**: None

**Methods**:

- `hash(json_data: Dict[str, str]) -> sha256`: Calculates the SHA-256 hash of the provided JSON data using a secret key.

    **Parameters**:

    - `json_data (Dict[str, str])`: The JSON data to hash.

    **Returns**:

    - `sha256`: The SHA-256 hash of the JSON data.

- `format_timestamp(timestamp: int) -> str`: Formats a timestamp in milliseconds into a string representation.

    **Parameters**:

    - `timestamp (int)`: The timestamp in milliseconds.

    **Returns**:

    - `str`: The formatted timestamp string.

## Functions

### `_create_completion(model: str, messages: list, temperature: float = 0.6, stream: bool = False, **kwargs)`

**Purpose**: This function sends a request to the Ails API to generate a text completion response.

**Parameters**:

- `model (str)`: The Ails model name (e.g., 'gpt-3.5-turbo').
- `messages (list)`: A list of messages to send to the API.
- `temperature (float, optional)`: The temperature parameter for controlling the creativity of the response. Defaults to 0.6.
- `stream (bool, optional)`: Whether to stream the response or return it as a whole. Defaults to `False`.
- `**kwargs`: Additional parameters for the Ails API request.

**Returns**:

- `Generator[str, None, None] | str | None`: A generator that yields chunks of the generated text if `stream` is `True`, otherwise returns the entire text response as a string or `None` if there is an error.

**Raises Exceptions**:

- `Exception`: If there is an error during the API request.

**How the Function Works**:

1. **Set up request headers**: Defines headers for the API request, including the `authorization`, `client-id`, and `client-v` headers.
2. **Prepare request parameters**: Sets up the `full` parameter for the API request.
3. **Generate a timestamp and signature**: Creates a timestamp and calculates a signature for the request using the `Utils.format_timestamp` and `Utils.hash` functions.
4. **Prepare JSON data**: Builds the JSON payload for the API request, including the model, temperature, stream flag, messages, and signature.
5. **Send API request**: Uses the `requests.post` function to send a POST request to the Ails API.
6. **Process response**: If `stream` is `True`, iterates through the response using the `iter_lines` method, extracts the `content` field from each line, and yields the decoded text chunk. Otherwise, returns the decoded response as a string.

**Examples**:

```python
# Example 1: Stream response
for token in _create_completion(model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': 'Hello, world!'}], stream=True):
    print(token, end='')

# Example 2: Get full response
response = _create_completion(model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': 'What is the meaning of life?'}])
print(response)
```

## Parameter Details

- `model (str)`: The Ails model name. This parameter specifies the specific Ails model to use for generating text.
- `messages (list)`: A list of messages to send to the Ails API. Each message should be a dictionary containing the `role` (e.g., 'user' or 'assistant') and `content` of the message.
- `temperature (float, optional)`: The temperature parameter for controlling the randomness of the generated text. Higher temperatures lead to more creative and unpredictable responses, while lower temperatures produce more deterministic and predictable outputs. Defaults to 0.6.
- `stream (bool, optional)`: This parameter determines whether the response is streamed as a series of tokens or returned as a single string. If set to `True`, the function yields chunks of the generated text, allowing for real-time display. Defaults to `False`.
- `**kwargs`: Additional parameters for the Ails API request. These parameters can be used to pass any other options supported by the Ails API.

**Examples**:

```python
# Example 1: Send a message and receive a streamed response
messages = [{'role': 'user', 'content': 'Write a short story about a cat.'}]
for token in _create_completion(model='gpt-3.5-turbo', messages=messages, stream=True):
    print(token, end='')

# Example 2: Get a full response with specific parameters
messages = [{'role': 'user', 'content': 'What is the meaning of life?'}]
response = _create_completion(model='gpt-3.5-turbo', messages=messages, temperature=0.2)
print(response)

# Example 3: Use additional parameters
messages = [{'role': 'user', 'content': 'Translate this text into Spanish: Hello, world!'}]
response = _create_completion(model='gpt-3.5-turbo', messages=messages, **{'top_p': 0.5}) # Use top_p parameter for nucleus sampling
print(response)
```