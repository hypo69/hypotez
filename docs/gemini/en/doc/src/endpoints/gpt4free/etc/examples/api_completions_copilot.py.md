# API Completions Copilot Example

## Overview

This file contains a simple example demonstrating how to use the API for completions using the Copilot model. 

The provided example interacts with a local server running on port 1337 and sends requests with user messages to the server. 

The server responds with the generated completions, which are then printed to the console.

## Details

This file is used for testing and exploring how to use the API for completions with different models. It demonstrates a basic process of sending messages, handling responses, and printing the results. 

## Functions

### `get_completions(model: str, provider: str, messages: List[Dict[str, str]], conversation_id: str) -> None`

**Purpose**: This function is used to send a request to the server for completions.

**Parameters**:

- `model` (str): The name of the model to use for generating completions.
- `provider` (str): The provider of the model.
- `messages` (List[Dict[str, str]]): A list of messages to send to the model. Each message is a dictionary containing the role ("user" or "assistant") and the content of the message.
- `conversation_id` (str): A unique identifier for the conversation.

**Returns**: 

- None: The function prints the results of the generated completions to the console. It does not return any value.

**Raises Exceptions**: 

- None: The function handles errors using `requests.raise_for_status` and prints error messages to the console.

**How the Function Works**:

1. The function takes the specified model, provider, messages, and conversation ID as arguments.
2. It constructs a request body using the provided parameters.
3. It makes a POST request to the server using the `requests` library.
4. The function handles the server's response, extracting the generated completions and printing them to the console.

**Examples**:

```python
# Example 1: Using the Copilot model for a simple conversation.
model = "copilot"
provider = "Copilot"
messages = [{"role": "user", "content": "Hello, how are you?"}]
conversation_id = str(uuid.uuid4())
get_completions(model, provider, messages, conversation_id)

# Example 2: Sending a message to get completions from the Copilot model.
model = "copilot"
provider = "Copilot"
messages = [{"role": "user", "content": "Tell me something about my name."}]
conversation_id = str(uuid.uuid4())
get_completions(model, provider, messages, conversation_id)
```