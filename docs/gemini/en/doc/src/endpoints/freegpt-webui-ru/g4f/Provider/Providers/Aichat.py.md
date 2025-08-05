# Aichat Provider

## Overview

This module provides the `Aichat` provider for the `g4f` framework, which utilizes the chat-gpt.org API for generating text completions.

## Details

The `Aichat` provider is designed to interact with the chat-gpt.org API to generate text completions. It leverages the `requests` library for sending HTTP requests to the API endpoint. 

This provider is particularly relevant for users seeking a lightweight and readily available text generation service without requiring authentication. However, it's crucial to note that the chat-gpt.org API might not be as robust or comprehensive as other options like OpenAI or Google Gemini.

## Classes

### `_create_completion`

**Description**: This function is responsible for generating text completions based on provided messages. It uses the chat-gpt.org API to send a POST request with the messages and specified parameters.

**Parameters**:

- `model (str)`: The name of the model to use for text generation. 
- `messages (list)`: A list of messages to use as context for generating the completion. Each message is a dictionary containing `role` and `content` keys.
- `stream (bool)`: Indicates whether to stream the completion response.

**Returns**:

- `Generator[str, None, None]`: A generator that yields text completions.

**Raises Exceptions**:

- `Exception`: If an error occurs while sending the request or processing the response.

**How the Function Works**:

1.  **Message Composition**: The function iterates over the provided `messages` and constructs a string containing the messages and their respective roles. This string represents the input context for the API.
2.  **Request Preparation**:  The function assembles HTTP headers for the request, including essential information about the request origin, content type, and user agent. It also creates a JSON payload containing the messages and generation parameters.
3.  **API Call**:  The function sends a POST request to the chat-gpt.org API endpoint using the prepared headers and JSON data. 
4.  **Response Processing**:  The function retrieves the completion response from the API and yields the text completion from the response's JSON data.

**Examples**:

```python
messages = [
    {'role': 'user', 'content': 'Hello, how are you?'},
    {'role': 'assistant', 'content': 'I am doing well, thank you. How about you?'}
]

for completion in _create_completion(model='gpt-3.5-turbo', messages=messages, stream=False):
    print(completion)
```

## Parameter Details

- `model (str)`: The name of the model to use for text generation. It's currently fixed to `gpt-3.5-turbo`.
- `messages (list)`: A list of messages to use as context for generating the completion. Each message is a dictionary containing `role` and `content` keys.
- `stream (bool)`: Indicates whether to stream the completion response.

## Examples

```python
# Example 1: Simple completion
messages = [
    {'role': 'user', 'content': 'What is the capital of France?'}
]

for completion in _create_completion(model='gpt-3.5-turbo', messages=messages, stream=False):
    print(completion)

# Example 2: Conversation-style completion
messages = [
    {'role': 'user', 'content': 'Hi, I'm looking for a good book to read.'},
    {'role': 'assistant', 'content': 'What kind of books do you like?'},
    {'role': 'user', 'content': 'I like science fiction.'}
]

for completion in _create_completion(model='gpt-3.5-turbo', messages=messages, stream=False):
    print(completion)
```