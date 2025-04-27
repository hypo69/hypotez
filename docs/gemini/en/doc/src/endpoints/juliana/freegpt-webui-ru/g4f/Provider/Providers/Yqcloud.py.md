# Yqcloud Provider

## Overview

This module provides the `Yqcloud` provider for the `g4f` system, offering a way to interact with the Yqcloud AI model.

## Details

This module implements the `Yqcloud` provider, which utilizes the Yqcloud API to generate text completions. The provider supports stream-based responses and doesn't require authentication.

## Classes

### `Yqcloud`

**Description**: This class represents the `Yqcloud` provider, allowing interaction with the Yqcloud AI model. 

**Attributes**: 

- `model`:  A list of supported models, currently `['gpt-3.5-turbo']`.
- `supports_stream`:  Indicates whether the provider supports stream-based responses (`True`).
- `needs_auth`:  Indicates whether authentication is required (`False`).

**Methods**:

- `_create_completion(model: str, messages: list, stream: bool, **kwargs)`:  This method sends a request to the Yqcloud API to generate a completion based on the provided messages and settings. It supports stream-based responses and returns a generator that yields the text chunks as they become available.

## Functions

### `_create_completion`

**Purpose**: This function sends a request to the Yqcloud API to generate a completion based on the provided messages and settings.

**Parameters**:

- `model (str)`: The name of the AI model to use.
- `messages (list)`: A list of messages containing the conversation history.
- `stream (bool)`:  Whether to receive the response as a stream.
- `**kwargs`:  Additional keyword arguments to be passed to the API request.

**Returns**:

- `Generator[str, None, None]`: A generator that yields text chunks of the response as they are generated.

**How the Function Works**:

- The function constructs a JSON payload with the conversation messages and other settings.
- It then sends a POST request to the Yqcloud API endpoint (`https://api.aichatos.cloud/api/generateStream`) with the JSON data.
- The function iterates through the chunks of the response stream, decoding them into strings and yielding them.

**Examples**:

```python
messages = [
    {'role': 'user', 'content': 'Hello, how are you?'},
    {'role': 'assistant', 'content': 'I am doing well, thank you for asking.'},
]

for chunk in _create_completion(model='gpt-3.5-turbo', messages=messages, stream=True):
    print(chunk, end='')
```

**Inner Functions**: None

## Parameter Details

- `model (str)`: The name of the AI model to use. The current supported model is `'gpt-3.5-turbo'`.
- `messages (list)`: A list of messages containing the conversation history. Each message is a dictionary with `role` (user or assistant) and `content` keys.
- `stream (bool)`:  Whether to receive the response as a stream. If `True`, the function returns a generator yielding text chunks. If `False`, the function returns the complete response string.
- `**kwargs`:  Additional keyword arguments to be passed to the API request.

## Examples

```python
# Example 1: Generating a completion with streaming
messages = [
    {'role': 'user', 'content': 'What is the capital of France?'},
    {'role': 'assistant', 'content': 'Paris.'},
]

for chunk in Yqcloud._create_completion(model='gpt-3.5-turbo', messages=messages, stream=True):
    print(chunk, end='')

# Example 2: Generating a completion without streaming
messages = [
    {'role': 'user', 'content': 'Write a short poem about a cat.'},
]

completion = Yqcloud._create_completion(model='gpt-3.5-turbo', messages=messages, stream=False)
print(completion)
```