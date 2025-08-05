# Messages Module 

## Overview

This module provides a `ConversationHandler` class, designed for managing conversations with AI models. It utilizes the `g4f.client` module for interacting with a specific model (e.g., "gpt-4") and maintains a history of messages exchanged during the conversation. 

## Details

The module facilitates a conversational interaction with AI models by:

- Creating a `ConversationHandler` object.
- Storing the model to be used for conversation.
- Keeping track of the conversation history (user messages and assistant responses).
- Allowing the user to add their messages to the history.
- Retrieving responses from the AI model based on the conversation history.

## Classes

### `ConversationHandler`

**Description**:  This class manages a conversation with an AI model, keeping track of the conversation history and enabling interaction with the model.

**Inherits**: N/A

**Attributes**:
 - `client` (`Client`): An instance of the `Client` class from the `g4f.client` module for communicating with the AI model.
 - `model` (`str`): The name of the AI model used for conversation (e.g., "gpt-4"). 
 - `conversation_history` (`list`): A list containing messages exchanged during the conversation, in the format of dictionaries with `role` and `content` keys.

**Methods**:

 - `add_user_message(content)`:
    **Purpose**: Adds a user message to the conversation history.
    **Parameters**:
      - `content` (`str`): The text of the user's message.
    **Returns**: None.

 - `get_response()`:
    **Purpose**: Retrieves a response from the AI model based on the current conversation history.
    **Parameters**: None.
    **Returns**: `str`: The AI model's response as a string.


## Functions
N/A


## Inner Functions
N/A

## Examples

```python
# Creating a conversation handler instance with the 'gpt-4' model
conversation = ConversationHandler()

# Adding a user message to the conversation history
conversation.add_user_message("Hello!")
print("Assistant:", conversation.get_response())  # Output: "Assistant: Hello!" 

# Adding another user message and getting the response
conversation.add_user_message("How are you?")
print("Assistant:", conversation.get_response())  # Output: "Assistant: I am an AI language model, so I don't have feelings. But I'm here to assist you with your questions!"
```