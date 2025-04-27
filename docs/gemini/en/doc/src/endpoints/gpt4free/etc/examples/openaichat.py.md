# OpenAI Chat Example 

## Overview

This example demonstrates using the `g4f` library to interact with the OpenAI chat API. The code establishes a connection with the OpenAI API, sends a message, and receives a response. 

## Details

This script utilizes the `g4f` library to connect to the OpenAI Chat API, enabling natural language conversations with AI models.

1. **Import Libraries**: It starts by importing necessary modules: `Client` from `g4f.client` for interacting with the API, `OpenaiChat` and `RetryProvider` from `g4f.Provider` for handling API requests.

2. **Initialization**: The script creates a `Client` instance, specifying a proxy configuration and a retry provider. The proxy configuration requires a working proxy in a country compatible with OpenAI's services. The `RetryProvider` ensures the client retries requests up to 5 times if they fail.

3. **Message Preparation**: A list of messages is created, representing the conversation flow. In this case, it starts with a single message: `{'role': 'user', 'content': 'Hello'}`.

4. **API Call**: The `chat.completions.create` method is called on the client object to send a message to the OpenAI API. The `model` parameter specifies the desired OpenAI model (`gpt-3.5-turbo` in this example). The `messages` parameter includes the conversation history (the prepared messages). The `stream` parameter enables streaming of the response.

5. **Response Processing**: The script iterates through the streamed response, printing the `content` of each message in the `delta` field.

## Classes

### `Client` 

**Description**: Represents a connection to the OpenAI API.

**Attributes**:

- `proxies (dict)`: A dictionary specifying proxy server details.
- `provider (RetryProvider)`: An instance of the `RetryProvider` class for handling API requests.

**Methods**:

- `chat.completions.create(model: str, messages: list, stream: bool)`: Sends a message to the OpenAI Chat API, specifying the model, messages, and whether to stream the response.


## Inner Functions

### `RetryProvider`

**Description**: A class for handling API requests and retrying them if they fail.

**Attributes**:

- `providers (list)`: A list of providers to use for API requests.
- `single_provider_retry (bool)`: Whether to retry only with the current provider or all providers.
- `max_retries (int)`: Maximum number of retries before giving up.

**Methods**:

- `__call__(self, *args, **kwargs) -> Any`: Executes an API request, retrying it if necessary.

## Parameter Details

- `model (str)`: The name of the OpenAI model to use for chat.
- `messages (list)`: A list of messages representing the conversation history.
- `stream (bool)`: Whether to stream the response or wait for the entire response.

## Examples

```python
from g4f.client   import Client
from g4f.Provider import OpenaiChat, RetryProvider

# compatible countries: https://pastebin.com/UK0gT9cn
client = Client(
    proxies = {
        'http': 'http://username:password@host:port', # MUST BE WORKING OPENAI COUNTRY PROXY ex: USA
        'https': 'http://username:password@host:port' # MUST BE WORKING OPENAI COUNTRY PROXY ex: USA
    },
    provider = RetryProvider([OpenaiChat],
                             single_provider_retry=True, max_retries=5)
)

messages = [
    {'role': 'user', 'content': 'Hello'}
]

response = client.chat.completions.create(model='gpt-3.5-turbo',
                                     messages=messages, 
                                     stream=True)

for message in response:
    print(message.choices[0].delta.content or "")
```