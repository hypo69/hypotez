# Pi Provider for GPT4Free

## Overview

This module implements the `Pi` class, a provider for interacting with the Pi AI service within the `gpt4free` project. This provider allows users to communicate with Pi AI using natural language and receive responses in a stream format. 

## Details

The `Pi` class inherits from the `AsyncGeneratorProvider` base class, providing a common interface for asynchronous communication with various AI models. This provider specifically handles communication with the Pi AI API, enabling interactions through its chat feature.

## Classes

### `class Pi`

**Description**:  This class provides a Python interface to interact with the Pi AI service. It inherits from the `AsyncGeneratorProvider` base class and implements asynchronous functions for sending messages and receiving responses from Pi AI.

**Inherits**:  `AsyncGeneratorProvider`

**Attributes**:
  - `url` (str): The base URL for the Pi AI API.
  - `working` (bool): Indicates whether the provider is currently functional (True).
  - `use_nodriver` (bool): Determines whether the provider uses a WebDriver for interaction (True).
  - `supports_stream` (bool): Specifies whether the provider supports streaming responses (True).
  - `use_nodriver` (bool): Determines whether the provider uses a WebDriver for interaction (True).
  - `default_model` (str): The default model used for interactions.
  - `models` (List[str]): A list of supported models.
  - `_headers` (dict):  Stores the headers used for API requests.
  - `_cookies` (dict):  Stores the cookies used for API requests.


**Methods**:

- `create_async_generator(model: str, messages: Messages, stream: bool, proxy: str = None, timeout: int = 180, conversation_id: str = None, **kwargs) -> AsyncResult`

    **Purpose**: This method creates an asynchronous generator to send messages and receive responses from Pi AI. It handles the entire interaction process, including starting a conversation, sending prompts, and receiving responses.

    **Parameters**:
      - `model` (str): The model to use for communication.
      - `messages` (List[dict]): A list of messages to send to the model.
      - `stream` (bool): Specifies whether to receive responses in a streaming format.
      - `proxy` (str):  The proxy to use for API requests.
      - `timeout` (int):  The timeout for API requests in seconds.
      - `conversation_id` (str): The unique ID of the conversation.
      - `**kwargs`: Additional keyword arguments.

    **Returns**:
      - `AsyncResult`:  An asynchronous result object representing the response from Pi AI.

    **Raises Exceptions**:
      - `Exception`: If there are any errors during the interaction process.

- `start_conversation(session: StreamSession) -> str`

    **Purpose**: This method initiates a new conversation with Pi AI and returns the conversation ID.

    **Parameters**:
      - `session` (StreamSession): The `StreamSession` object used for API requests.

    **Returns**:
      - `str`:  The conversation ID for the newly created conversation.

    **Raises Exceptions**:
      - `Exception`: If there are any errors during conversation initiation.

- `get_chat_history(session: StreamSession, conversation_id: str)` 

    **Purpose**: This method retrieves the chat history for a given conversation ID.

    **Parameters**:
      - `session` (StreamSession): The `StreamSession` object used for API requests.
      - `conversation_id` (str): The ID of the conversation to retrieve the history for.

    **Returns**:
      - `dict`: A dictionary containing the chat history for the specified conversation.

    **Raises Exceptions**:
      - `Exception`: If there are any errors retrieving the chat history.

- `ask(session: StreamSession, prompt: str, conversation_id: str)`

    **Purpose**: This method sends a message to Pi AI using a given prompt and conversation ID. It retrieves responses from the service in a streaming format.

    **Parameters**:
      - `session` (StreamSession): The `StreamSession` object used for API requests.
      - `prompt` (str): The message or prompt to send to Pi AI.
      - `conversation_id` (str): The ID of the conversation to send the message to.

    **Returns**:
      - `AsyncGenerator[dict, None, None]`: An asynchronous generator yielding the responses from Pi AI.

    **Raises Exceptions**:
      - `Exception`: If there are any errors sending the message or receiving responses.

**Principle of Operation**:

The `Pi` class acts as a wrapper around the Pi AI API, enabling interactions with the chat service.  The `create_async_generator` method manages the entire conversation flow, including starting, sending messages, and receiving responses in a stream. The `start_conversation` method creates a new conversation with Pi AI. `get_chat_history` retrieves the chat history for a given conversation. `ask` sends a message to Pi AI using a provided prompt. These methods employ the `StreamSession` class for asynchronous communication, allowing for real-time responses. 

## Examples

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.Pi import Pi
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Creating a message list
messages: Messages = [
    {"role": "user", "content": "Hello, Pi! What is the meaning of life?"}
]

# Using the Pi provider
async def main():
    pi_provider = Pi()
    async for response in pi_provider.create_async_generator(model="pi", messages=messages, stream=True):
        print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## Parameter Details

- `model` (str): The model to use for communication.
- `messages` (List[dict]): A list of messages to send to the model. Each message is a dictionary with keys `role` (e.g., "user", "assistant") and `content` (the message text).
- `stream` (bool): Specifies whether to receive responses in a streaming format.
- `proxy` (str):  The proxy to use for API requests.
- `timeout` (int):  The timeout for API requests in seconds.
- `conversation_id` (str): The unique ID of the conversation.
- `**kwargs`: Additional keyword arguments.

## Inner Functions

This class does not contain inner functions.

## How the Function Works

The `Pi` class operates as a bridge between the `gpt4free` project and the Pi AI service. The primary function, `create_async_generator`, orchestrates the entire interaction process. 

1.  **Initialization**: The method initializes the `_headers` and `_cookies` attributes for API requests.
2.  **Conversation Start**: If no conversation ID is provided, it starts a new conversation using the `start_conversation` method, receiving a unique conversation ID.
3.  **Message Sending**: It constructs a message using the provided messages list and sends it to Pi AI via the `ask` method.
4.  **Streaming Responses**: The `ask` method retrieves responses from Pi AI in a streaming format, yielding each response line to the caller.
5.  **Async Generator**: The entire process is wrapped in an asynchronous generator (`create_async_generator`), enabling users to iterate over responses as they arrive.

## Examples

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.Pi import Pi
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Example 1: Starting a new conversation
async def start_new_conversation():
    pi_provider = Pi()
    conversation_id = await pi_provider.start_conversation(session)
    print(f"New conversation started with ID: {conversation_id}")

# Example 2: Sending a message to a conversation
async def send_message():
    pi_provider = Pi()
    conversation_id = "your_conversation_id"  # Replace with the actual ID
    message = {"role": "user", "content": "What is the weather like today?"}
    async for response in pi_provider.ask(session, message, conversation_id):
        print(response)

# Example 3: Retrieving conversation history
async def get_history():
    pi_provider = Pi()
    conversation_id = "your_conversation_id"  # Replace with the actual ID
    history = await pi_provider.get_chat_history(session, conversation_id)
    print(history)

# Example 4: Using create_async_generator for multiple messages
async def multiple_messages():
    messages: Messages = [
        {"role": "user", "content": "Hello, Pi!"},
        {"role": "user", "content": "How are you today?"}
    ]
    pi_provider = Pi()
    async for response in pi_provider.create_async_generator(model="pi", messages=messages, stream=True):
        print(response)
```

## Your Behavior During Code Analysis:

- Inside the code, you might encounter expressions between `<` `>`. For example: `<instruction for gemini model:Loading product descriptions into PrestaShop.>, <next, if available>. These are placeholders where you insert the relevant value.
- Always refer to the system instructions for processing code in the `hypotez` project (the first set of instructions you translated);
- Analyze the file's location within the project. This helps understand its purpose and relationship with other files. You will find the file location in the very first line of code starting with `## \\file /...`;
- Memorize the provided code and analyze its connection with other parts of the project;
- In these instructions, do not suggest code improvements. Strictly follow point 5. **Example File** when composing the response.