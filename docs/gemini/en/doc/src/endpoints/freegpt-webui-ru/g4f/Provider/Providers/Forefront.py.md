# Forefront Provider

## Overview

This module provides a Forefront provider implementation for the `hypotez` project. This provider is designed to interact with the Forefront API to enable access to the Forefront AI models. 

## Details

The Forefront provider offers an integration with the Forefront AI models. It utilizes the `requests` library to send requests to the Forefront API and receives responses in a streaming format. This approach is suitable for large language models (LLMs) that generate text iteratively.

The `_create_completion` function, which is the primary function for generating responses from Forefront models, interacts with the Forefront API by sending JSON data. The response from the API is then streamed and processed to yield individual tokens, representing parts of the generated text.

## Functions

### `_create_completion`

**Purpose**: This function handles the generation of completions from the Forefront AI models. It sends a request to the Forefront API with a specific JSON structure containing the input messages, model selection, and other settings. The response from the API is streamed, and the function yields individual tokens from the generated text.

**Parameters**:

- `model` (str): The Forefront model to be used for generating the response.
- `messages` (list): A list of messages in the conversation. Each message is a dictionary with keys 'role' (e.g., 'user', 'assistant') and 'content' (the message text).
- `stream` (bool): Indicates whether to receive the response in a streaming format.

**Returns**:

- Generator: A generator that yields individual tokens from the generated text.

**Raises Exceptions**:

- RequestsError: If there is an error sending the request to the Forefront API.
- JSONDecodeError: If there is an error decoding the JSON response from the Forefront API.

**Inner Functions**:

- None

**How the Function Works**:

1. The function constructs a JSON payload containing the input messages, model selection, and other settings.
2. It uses the `requests` library to send a POST request to the Forefront API endpoint `https://streaming.tenant-forefront-default.knative.chi.coreweave.com/free-chat`.
3. The API response is streamed and processed iteratively.
4. For each line in the streamed response, the function checks if it contains a 'delta' key. 
5. If present, the 'delta' key represents a token in the generated text. This token is decoded from JSON and yielded to the caller.

**Examples**:

```python
messages = [
    {'role': 'user', 'content': 'Hello, how are you?'},
    {'role': 'assistant', 'content': 'I am doing well, thank you for asking.'},
]
tokens = _create_completion(model='gpt-4', messages=messages, stream=True)
for token in tokens:
    print(token)
```