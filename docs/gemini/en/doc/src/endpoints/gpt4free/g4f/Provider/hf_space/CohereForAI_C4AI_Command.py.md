# CohereForAI_C4AI_Command.py

## Overview

This module defines the `CohereForAI_C4AI_Command` class, which implements an asynchronous generator provider for interacting with the CohereForAI C4AI Command model available on Hugging Face Spaces. This provider allows you to send messages to the model and receive responses in a streaming fashion.

## Details

The `CohereForAI_C4AI_Command` provider utilizes the Hugging Face Spaces API for communication with the CohereForAI C4AI Command model. It manages conversation state, handles model selection, and processes responses to provide a seamless user experience.

## Classes

### `CohereForAI_C4AI_Command`

**Description**: 
- This class implements an asynchronous generator provider for the CohereForAI C4AI Command model.
- Inherits from `AsyncGeneratorProvider` and `ProviderModelMixin`.
- Provides methods for generating responses from the model, managing conversation state, and handling model selection.

**Attributes**:
- `label` (str): Label for the provider, defaults to "CohereForAI C4AI Command".
- `url` (str): Base URL for the Hugging Face Spaces API, defaults to "https://cohereforai-c4ai-command.hf.space".
- `conversation_url` (str): URL for conversation management, defaults to "https://cohereforai-c4ai-command.hf.space/conversation".
- `working` (bool): Flag indicating whether the provider is working, defaults to `True`.
- `default_model` (str): Default model to use, defaults to "command-a-03-2025".
- `model_aliases` (dict): Mapping of model aliases to their actual names, defaults to a dictionary containing aliases and their corresponding models.
- `models` (list): List of available model names, defaults to the keys from `model_aliases`.

**Methods**:
- `get_model(model: str, **kwargs) -> str`: Returns the model name based on the input `model` string.
- `create_async_generator(model: str, messages: Messages, api_key: str = None, proxy: str = None, conversation: JsonConversation = None, return_conversation: bool = False, **kwargs) -> AsyncResult`: Creates an asynchronous generator that handles conversation with the model. 

## Functions

### `get_model`

**Purpose**:
- Retrieves the actual model name from the input `model` string.
- Checks if the input model is a valid alias in `model_aliases` and returns the corresponding actual model name if found.
- If no alias is found, it calls the parent class method `get_model` to handle the case.

**Parameters**:
- `model` (str): The input model string.
- `**kwargs`: Additional keyword arguments.

**Returns**:
- `str`: The actual model name based on the input `model`.

**Raises Exceptions**:
- None

**How the Function Works**:
- This function checks if the input `model` is present in the `model_aliases` dictionary, representing a model alias. 
- If a match is found, it returns the corresponding actual model name.
- Otherwise, it delegates the task to the parent class's `get_model` method to handle cases where the input `model` is not an alias.

**Examples**:
- `get_model("command-a")` returns "command-a-03-2025"
- `get_model("command-r-plus")` returns "command-r-plus-08-2024"
- `get_model("unknown_model")` calls the parent class method `get_model` for further processing.

### `create_async_generator`

**Purpose**: 
- Creates an asynchronous generator that manages conversation with the CohereForAI C4AI Command model. 
- Handles message processing, conversation state management, and response streaming.

**Parameters**:
- `model` (str): The name of the model to use.
- `messages` (Messages): A list of messages in the conversation.
- `api_key` (str, optional): API key for authentication, defaults to `None`.
- `proxy` (str, optional): Proxy server to use, defaults to `None`.
- `conversation` (JsonConversation, optional): Existing conversation state, defaults to `None`.
- `return_conversation` (bool, optional): Flag to return the conversation state, defaults to `False`.
- `**kwargs`: Additional keyword arguments.

**Returns**:
- `AsyncResult`: An asynchronous generator that yields responses from the model.

**Raises Exceptions**:
- `RuntimeError`: If an error occurs while reading the response from the server.

**How the Function Works**:
- This function creates an asynchronous session with necessary headers and cookies.
- Extracts system prompt messages from the input messages and formats user messages.
- Checks if a conversation is already in progress and updates the conversation state if needed.
- Sends a request to the server to get the initial conversation state or to add a new message.
- Processes responses from the server, including streaming responses and error handling.
- Yields the received responses as strings or objects, such as `TitleGeneration`, for further processing.

**Examples**:
- `create_async_generator("command-a", [{"role": "user", "content": "Hello!"}])` starts a new conversation with the model "command-a" and sends the message "Hello!".
- `create_async_generator("command-r-plus", [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "What is the meaning of life?"}], conversation=existing_conversation)` continues an existing conversation with model "command-r-plus" by adding a user message.

## Parameter Details

- `model` (str): Specifies the model to be used for generating responses. The model can be chosen from the list of available models, either by its name or by its alias. Refer to the `models` attribute and `model_aliases` dictionary for available options.

- `messages` (Messages): This parameter provides a list of messages in the conversation. Each message is represented by a dictionary containing the `role` and `content` of the message. The `role` can be "user", "system", or "assistant". The `content` is the text of the message.

- `api_key` (str, optional): This parameter is used for authentication. It should contain the API key obtained from CohereForAI for accessing their services. If you do not provide an `api_key`, the default value `None` is used.

- `proxy` (str, optional): This parameter allows you to specify a proxy server to use for communication with the model. If you do not provide a proxy, the default value `None` is used, meaning that the system will use a direct connection.

- `conversation` (JsonConversation, optional): This parameter allows you to pass an existing conversation state. This is useful for continuing a conversation from a previous state. If you do not provide a conversation state, the default value `None` is used, meaning that a new conversation is started.

- `return_conversation` (bool, optional): This parameter determines whether the conversation state should be returned to the user. If set to `True`, the generator will also yield the updated conversation state along with responses. The default value is `False`, meaning that only responses are yielded. 

- `**kwargs`: This parameter allows you to pass additional keyword arguments specific to the model or the API. These arguments are typically used for customizing the model behavior.

## Examples

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf_space.CohereForAI_C4AI_Command import CohereForAI_C4AI_Command
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Start a new conversation
provider = CohereForAI_C4AI_Command()
messages = [
    {"role": "user", "content": "What is the capital of France?"}
]
async for response in provider.create_async_generator(model="command-a", messages=messages):
    print(response)

# Continue an existing conversation
conversation = ...  # Load conversation state from previous interaction
messages = [
    {"role": "user", "content": "And what about Germany?"}
]
async for response in provider.create_async_generator(model="command-r-plus", messages=messages, conversation=conversation):
    print(response)
```

```python
# Example with specifying API key and proxy
api_key = "YOUR_API_KEY"
proxy = "http://your_proxy_server:port"
async for response in provider.create_async_generator(model="command-a", messages=messages, api_key=api_key, proxy=proxy):
    print(response)
```

```python
# Example with returning conversation state
async for response in provider.create_async_generator(model="command-a", messages=messages, return_conversation=True):
    if isinstance(response, JsonConversation):
        conversation = response
    else:
        print(response)