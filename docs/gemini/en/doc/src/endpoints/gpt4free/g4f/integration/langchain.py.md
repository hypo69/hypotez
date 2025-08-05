# LangChain Integration for GPT-4Free

## Overview

This module provides integration with LangChain for GPT-4Free, allowing users to utilize GPT-4Free models within LangChain workflows.

## Details

This file defines a custom `ChatAI` class that extends the `ChatOpenAI` class from LangChain. This allows users to leverage GPT-4Free models using the familiar LangChain API. The `ChatAI` class integrates GPT-4Free's asynchronous and synchronous API clients to handle message processing, model validation, and environment setup. 

## Classes

### `ChatAI`

**Description**: A custom LangChain chat model class for interacting with GPT-4Free models.

**Inherits**: `langchain_community.chat_models.openai.ChatOpenAI`

**Attributes**:

- `model_name` (str): The GPT-4Free model name. Defaults to "gpt-4o".

**Methods**:

- `validate_environment(cls, values: dict) -> dict`: Validates the environment and sets up the GPT-4Free client.

## Inner Functions

### `new_convert_message_to_dict(message: BaseMessage) -> dict`

**Purpose**: Converts a LangChain message to a dictionary compatible with the GPT-4Free API.

**Parameters**:

- `message` (BaseMessage): The LangChain message to convert.

**Returns**:

- `dict`: A dictionary representation of the LangChain message.

**How the Function Works**:

- This function takes a LangChain message object and converts it into a dictionary format that the GPT-4Free API can understand.
- If the message is a `ChatCompletionMessage`, it extracts the `role`, `content`, and `tool_calls` information from the message.
- For other message types, it uses the default `convert_message_to_dict` function from LangChain.

## Examples

```python
from g4f.integration.langchain import ChatAI

# Create a ChatAI instance with a GPT-4Free model
chat_model = ChatAI(model_name="gpt-4o", api_key="YOUR_API_KEY")

# Send a message to the model and get a response
response = chat_model.predict("Hello, how are you?")

print(response)
```