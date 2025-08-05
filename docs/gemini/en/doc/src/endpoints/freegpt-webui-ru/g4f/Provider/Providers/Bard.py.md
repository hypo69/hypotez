# Bard Provider for g4f

## Overview

This module provides the `Bard` provider for the `g4f` module, which enables communication with the Google Bard AI model.

## Details

The `Bard` provider is responsible for handling interactions with the Google Bard service, including sending prompts and receiving responses. It relies on the `requests` library for HTTP communication and the `browser_cookie3` library for managing Google account cookies. 

The provider ensures that communication occurs through a proxy server. This is because many countries have restrictions on accessing Google Bard, and using a proxy can help circumvent these limitations.

## Classes

### `class _create_completion`

**Description**: This function handles the interaction with the Google Bard service, sending prompts and receiving responses.

**Parameters**:

- `model` (str): Specifies the AI model to use (currently only "Palm2" is supported).
- `messages` (list): A list of messages that form the context for the prompt.
- `stream` (bool):  Indicates whether to stream the response.
- `**kwargs`: Additional keyword arguments.

**Returns**:

- `Generator[str, None, None]`:  A generator that yields the response chunks from the Bard service.

**Raises Exceptions**:

- `Exception`:  If an error occurs during communication with the Bard service.

**How the Function Works**:

1. **Retrieve Google Account Cookies**:  It uses the `browser_cookie3` library to retrieve the `__Secure-1PSID` cookie from the user's Chrome browser, which is essential for authentication with Google Bard.
2. **Format Prompt**: The `messages` list is formatted into a string representing the conversation history. The prompt is then constructed by appending "Assistant:" to the formatted messages.
3. **Handle Proxy**: The `proxy` argument is used to configure the request session with a proxy server. If no proxy is provided, it logs a warning message.
4. **Initialize Request Session**: A `requests.Session` object is created with optional proxy settings.
5. **Set Headers**: The `headers` dictionary is set with relevant information for communication with Bard, including the authentication cookie.
6. **Retrieve SNlM0e Token**:  It retrieves the `SNlM0e` token from the Bard website, which is required for interacting with the service.
7. **Construct Request Parameters**: The `params` dictionary is created with parameters specific to the Bard service.
8. **Construct Request Data**: The `data` dictionary is created with the formatted prompt and other necessary information.
9. **Send POST Request**: It sends a POST request to the Bard API endpoint, `https://bard.google.com/_/BardChatUi/data/assistant.lamda.BardFrontendService/StreamGenerate`, with the constructed parameters and data.
10. **Process Response**: The response is processed by extracting the chat data and yielding it as a generator. 
11. **Error Handling**:  If no chat data is found, it yields an "error" message.

**Examples**:

```python
from hypotez.src.endpoints.freegpt-webui-ru.g4f.Provider.Providers.Bard import _create_completion

messages = [
    {'role': 'user', 'content': 'Hello, how are you?'},
    {'role': 'assistant', 'content': 'I am doing well, thank you for asking.'}
]

response = _create_completion(model='Palm2', messages=messages, stream=False, proxy='http://127.0.0.1:8080')

# Iterate over the response chunks
for chunk in response:
    print(chunk)
```

## Parameter Details

- `model` (str):  Specifies the AI model to use for generating responses. Currently, only "Palm2" is supported.

- `messages` (list): A list of dictionaries representing the conversation history. Each dictionary contains the following keys:
    - `role`:  The role of the message sender (e.g., 'user', 'assistant').
    - `content`:  The actual message content.

- `stream` (bool):  Specifies whether to stream the response. If set to `True`, the response will be generated in chunks.

- `proxy` (str, optional):  The proxy server address to use for communication. Defaults to `None`.

## Examples

```python
from hypotez.src.endpoints.freegpt-webui-ru.g4f.Provider.Providers.Bard import _create_completion

# Example 1: Basic prompt
messages = [
    {'role': 'user', 'content': 'What is the capital of France?'}
]
response = _create_completion(model='Palm2', messages=messages, stream=False, proxy='http://127.0.0.1:8080')
print(response)

# Example 2: Multiple messages
messages = [
    {'role': 'user', 'content': 'Hello, Bard.'},
    {'role': 'assistant', 'content': 'Hello! How can I help you today?'},
    {'role': 'user', 'content': 'What is the meaning of life?'}
]
response = _create_completion(model='Palm2', messages=messages, stream=False, proxy='http://127.0.0.1:8080')
print(response)
```