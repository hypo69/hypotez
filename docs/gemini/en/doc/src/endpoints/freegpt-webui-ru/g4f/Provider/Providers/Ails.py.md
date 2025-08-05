# Ails Provider for g4f
## Overview
This module implements the `Ails` provider for the g4f API. The `Ails` provider utilizes the `ai.ls` service to provide access to the `gpt-3.5-turbo` model. It offers a streamlined interface for generating text responses based on user input.

## Details
The `Ails` provider is designed to work seamlessly with the g4f system, handling communication with the `ai.ls` service. It leverages the `gpt-3.5-turbo` model for text generation, allowing users to engage in conversational interactions or generate creative content. This provider encapsulates the complexities of interacting with the API, making it easy for developers to integrate text generation capabilities into their applications.

## Classes
### `Utils`
**Description**: 
The `Utils` class provides utility functions for hashing data and formatting timestamps. 

**Attributes**:
- None

**Methods**:
- `hash(json_data: Dict[str, str]) -> sha256`:  
   **Purpose**:  Calculates a SHA-256 hash of the provided JSON data.
   **Parameters**:
    - `json_data (Dict[str, str])`: The JSON data to be hashed.
   **Returns**:
    - `sha256`: The SHA-256 hash of the JSON data.
- `format_timestamp(timestamp: int) -> str`: 
   **Purpose**: Formats a timestamp for use with the `ai.ls` service.
   **Parameters**:
    - `timestamp (int)`: The timestamp to be formatted.
   **Returns**:
    - `str`: The formatted timestamp.

## Functions
### `_create_completion(model: str, messages: list, temperature: float = 0.6, stream: bool = False, **kwargs)`
**Purpose**:  
Generates a text completion using the `gpt-3.5-turbo` model through the `ai.ls` service.

**Parameters**:
- `model (str)`: The name of the model to use (currently only supports `gpt-3.5-turbo`).
- `messages (list)`: A list of messages to provide as context for the completion.
- `temperature (float, optional)`: The sampling temperature for the model. Defaults to 0.6.
- `stream (bool, optional)`: Whether to stream the response. Defaults to `False`.
- `**kwargs`:  Additional keyword arguments.

**Returns**:
- `Generator[str, None, None] | str`: A generator yielding tokens of the completion (if `stream` is `True`) or the complete completion (if `stream` is `False`).

**Raises Exceptions**:
- `Exception`: If an error occurs during the API request.

**How the Function Works**: 
- The function constructs a request to the `ai.ls` API, including model name, messages, and other parameters. 
- It includes a timestamp and a hash for security purposes.
- The function handles both streaming and non-streaming responses. If streaming is enabled, it yields individual tokens of the completion; otherwise, it returns the complete completion as a string.

**Examples**:
```python
# Example 1: Generating a single completion
completion = _create_completion(model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': 'Hello, how are you?'}])
print(completion)

# Example 2: Streaming completion
for token in _create_completion(model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': 'What is the meaning of life?'}], stream=True):
    print(token, end='')
```

## Parameter Details
- `model (str)`: This parameter specifies the model used for generating text responses. Currently, only `gpt-3.5-turbo` is supported.
- `messages (list)`:  A list of messages passed to the model as context for generating a response. Each message is represented as a dictionary containing a `role` (e.g., `user`, `assistant`) and `content`.
- `temperature (float, optional)`: Determines the randomness of the generated text. A higher temperature leads to more creative and unpredictable results, while a lower temperature produces more predictable and coherent responses.
- `stream (bool, optional)`: Specifies whether to receive the generated text in a streamed format. If set to `True`, the function will yield individual tokens of the completion, allowing for real-time updates. If set to `False`, the function will return the complete completion once it's finished.

**Inner Functions**: None

**Examples**:
```python
# Example 1: Non-Streaming Completion
_create_completion(model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': 'What is the meaning of life?'}], stream=False)

# Example 2: Streaming Completion
_create_completion(model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': 'Write a poem about a cat.'}], stream=True) 

# Example 3: Using a different model (not supported)
_create_completion(model='text-davinci-003', messages=[{'role': 'user', 'content': 'What is the meaning of life?'}], stream=False) 
```

## Additional Notes
- The `Ails` provider utilizes the `ai.ls` service, which offers access to the `gpt-3.5-turbo` model. 
- The provided code includes several security measures, such as a timestamp and a hash, to ensure the integrity of the requests made to the API.
- The `Utils` class provides helper functions for hashing and formatting timestamps, simplifying the implementation of the provider.