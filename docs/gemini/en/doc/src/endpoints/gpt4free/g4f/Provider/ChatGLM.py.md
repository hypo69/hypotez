# ChatGLM Provider Module

## Overview

This module provides the `ChatGLM` class, which implements an asynchronous generator for interacting with the ChatGLM AI model. It allows sending messages to the model and receiving responses in a streaming fashion. 

## Details

The `ChatGLM` provider is designed for interacting with the ChatGLM model available at `https://chatglm.cn`. It inherits from the base `AsyncGeneratorProvider` class, providing a standard interface for asynchronous communication with AI models. 

## Classes

### `ChatGLM`

**Description**: This class represents a ChatGLM provider, responsible for handling communication with the ChatGLM model.

**Inherits**:
  - `AsyncGeneratorProvider`: This class defines the basic interface for asynchronous communication with AI models.
  - `ProviderModelMixin`: This mixin provides common features for working with AI model providers.

**Attributes**:
  - `url` (str): Base URL for accessing the ChatGLM service.
  - `api_endpoint` (str): Endpoint for sending messages and receiving responses.
  - `working` (bool): Indicates whether the provider is currently working (True).
  - `supports_stream` (bool): Whether the provider supports streaming responses (True).
  - `supports_system_message` (bool): Whether the provider supports system messages (False).
  - `supports_message_history` (bool): Whether the provider supports message history (False).
  - `default_model` (str): Default model to use for interactions.
  - `models` (list): List of available models.

**Methods**:
  - `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`: This method creates an asynchronous generator for interacting with the ChatGLM model.

#### `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`

**Purpose**: This method creates an asynchronous generator for sending messages to the ChatGLM model and receiving responses. It handles communication with the ChatGLM API and yields text chunks as they become available.

**Parameters**:
  - `model` (str): The ChatGLM model to use.
  - `messages` (Messages): A list of messages to send to the model.
  - `proxy` (str, optional): Proxy server to use for communication. Defaults to `None`.

**Returns**:
  - `AsyncResult`: An asynchronous result object that yields text chunks from the ChatGLM model response.

**Raises Exceptions**:
  - `Exception`: If an error occurs during communication with the ChatGLM API.

**How the Function Works**:

1. **Initialize**:  The function starts by generating a unique device ID for the request.
2. **Prepare Headers**: It constructs a dictionary of headers for the HTTP request.
3. **Establish Session**: An asynchronous HTTP session is created with the specified headers.
4. **Prepare Data**:  The function prepares a JSON payload containing the device ID, conversation details, and the messages to send to the model.
5. **Send Request**:  The function sends a POST request to the ChatGLM API with the prepared JSON data.
6. **Handle Response**: The function iterates through the streaming response from the ChatGLM API, decoding each chunk.
7. **Process Response**: For each decoded chunk, the function extracts the text content and yields it to the caller.
8. **Finish Signal**: If the `status` field in the response indicates the conversation is finished, the function yields a `FinishReason` to signal the end of the response.


**Examples**:

```python
from src.endpoints.gpt4free.g4f.Provider.ChatGLM import ChatGLM
from src.endpoints.gpt4free.g4f.typing import Messages

# Example with default model and messages
async def example_chatglm():
    messages: Messages = [
        {"role": "user", "content": "Hello, world!"}
    ]
    async for chunk in ChatGLM.create_async_generator(model='glm-4', messages=messages):
        print(chunk)

# Example with a custom model and proxy
async def example_chatglm_with_model_and_proxy():
    messages: Messages = [
        {"role": "user", "content": "Hello, world!"}
    ]
    async for chunk in ChatGLM.create_async_generator(model='glm-6', messages=messages, proxy='http://proxy.example.com:8080'):
        print(chunk)
```

## Parameter Details

- `model` (str): The ChatGLM model to use for interaction. 
- `messages` (Messages): A list of messages to be sent to the ChatGLM model. Each message in the list should have the following format:
  - `role` (str): The role of the message sender, either "user" or "assistant".
  - `content` (str): The actual content of the message.
- `proxy` (str, optional): A proxy server to use for communication with the ChatGLM API.

```python
                ```