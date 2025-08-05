# Liaobots Provider

## Overview

This module defines a provider for interacting with Liaobots, a service for accessing large language models (LLMs) like GPT-3.5 and GPT-4. 

## Details

This provider allows you to interact with Liaobots through the `_create_completion` function, which sends requests to the Liaobots API for generating text completions. 

The provider requires authentication and supports streaming for real-time responses. 

## Classes

### `_create_completion`

**Description:** This function sends requests to the Liaobots API for generating text completions.

**Parameters:**

- `model` (str): The name of the LLM model to use.
- `messages` (list): A list of messages in the conversation.
- `stream` (bool): Whether to stream the response.
- `**kwargs`:  Additional keyword arguments.

**Returns:**

- Generator[str, None, None]: A generator that yields individual tokens of the generated text.

**Raises Exceptions:**

- `Exception`: If an error occurs during API request.

**How the Function Works:**

1. Constructs a JSON request payload with details like conversation ID, model, messages, API key, and a default prompt.
2. Sends a POST request to the Liaobots API endpoint `https://liaobots.com/api/chat`.
3. If `stream` is True, iterates through the response using `response.iter_content` to retrieve individual tokens in chunks.
4. Decodes each token using `utf-8` and yields it to the caller.

**Examples:**

```python
messages = [
    {'role': 'user', 'content': 'Hello, how are you?'},
    {'role': 'assistant', 'content': 'I am doing well, thank you! How can I assist you today?'},
]

model = 'gpt-3.5-turbo'

# Authenticate with Liaobots
auth_token = 'your_auth_token'

# Use the provider
response = _create_completion(model, messages, stream=True, auth=auth_token)

# Process the streaming response
for token in response:
    print(token, end='')
```

## Parameter Details

- `model` (str):  The name of the LLM model to use. Supported models are `gpt-3.5-turbo` and `gpt-4`.
- `messages` (list): A list of message objects in the conversation. Each message object has the format: `{'role': 'user' | 'assistant', 'content': 'message text'}`.
- `stream` (bool): Whether to stream the response for real-time feedback. 
- `**kwargs`: Additional keyword arguments, including: 
    - `auth` (str): The authentication token for accessing the Liaobots API.

## Examples

### Basic usage with streaming

```python
import os, uuid, requests
from ...typing import sha256, Dict, get_type_hints

url = 'https://liaobots.com'
model = ['gpt-3.5-turbo', 'gpt-4']
supports_stream = True
needs_auth = True

models = {
    'gpt-4': {
        "id":"gpt-4",
        "name":"GPT-4",
        "maxLength":24000,
        "tokenLimit":8000
    },
    'gpt-3.5-turbo': {
        "id":"gpt-3.5-turbo",
        "name":"GPT-3.5",
        "maxLength":12000,
        "tokenLimit":4000
    },
}

def _create_completion(model: str, messages: list, stream: bool, **kwargs):

    print(kwargs)

    headers = {
        'authority': 'liaobots.com',
        'content-type': 'application/json',
        'origin': 'https://liaobots.com',
        'referer': 'https://liaobots.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'x-auth-code': kwargs.get('auth')
    }

    json_data = {
        'conversationId': str(uuid.uuid4()),
        'model': models[model],
        'messages': messages,
        'key': '',
        'prompt': "You are ChatGPT, a large language model trained by OpenAI. Follow the user's instructions carefully. Respond using markdown.",
    }

    response = requests.post('https://liaobots.com/api/chat', 
                             headers=headers, json=json_data, stream=True)

    for token in response.iter_content(chunk_size=2046):
        yield (token.decode('utf-8'))

params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])
```

###  Authentication and Response Handling

```python
# Example usage:
messages = [
    {'role': 'user', 'content': 'What is the meaning of life?'},
    {'role': 'assistant', 'content': 'That is a question that has been pondered by philosophers for centuries.'}
]

model = 'gpt-4'  # Choose a model
auth_token = 'your_auth_token'  # Obtain your auth token from Liaobots 

response_stream = _create_completion(model, messages, stream=True, auth=auth_token)

# Process the streaming response
for token in response_stream:
    print(token, end='')
```

###  Error Handling

```python
try:
    # ...
except Exception as ex:
    logger.error('Error while requesting completion from Liaobots', ex, exc_info=True)
```