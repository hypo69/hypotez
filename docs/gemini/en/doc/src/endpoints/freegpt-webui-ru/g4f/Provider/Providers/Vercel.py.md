# Provider for Vercel models

## Overview

This module defines the `Vercel` class, which implements a provider for using models hosted on Vercel. 

## Details

The module provides the following functionality:

- **Model Support:** The `vercel_models` dictionary defines the supported models and their corresponding parameters. 
- **Client Class:** The `Client` class provides methods for retrieving an API token, generating text with the models, and retrieving default model parameters.
- **`_create_completion` Function:** This function prepares the conversation history for a model and iteratively yields generated tokens. 


## Classes

### `Client`
**Description**: The `Client` class provides methods for interacting with the Vercel API.

**Attributes**:
- `session`: A `requests.Session` object for making HTTP requests.
- `headers`: A dictionary containing default HTTP headers for requests.


**Methods**:
- `get_token()`: Retrieves an API token from Vercel.
- `get_default_params(model_id: str)`: Retrieves default parameters for a given model ID.
- `generate(model_id: str, prompt: str, params: dict = {})`: Generates text using the specified model ID and prompt. 


## Functions

### `_create_completion`

**Purpose**: This function prepares the conversation history and calls the `Client.generate` function to generate text.

**Parameters**:
- `model` (str): The name of the model.
- `messages` (list): A list of messages in the conversation.
- `stream` (bool): Indicates whether the response should be streamed.
- `**kwargs`: Optional keyword arguments passed to the `Client.generate` function.

**Returns**:
- `Generator[str, None, None]`:  A generator that yields generated tokens.

**Raises Exceptions**:
- `Exception`: If an error occurs during token generation.


**How the Function Works**:

- The function builds a conversation string from the `messages` list. 
- It calls the `Client.generate` function with the conversation string and model name.
- The `Client.generate` function sends a request to the Vercel API and streams the response.
- The `_create_completion` function iterates through the streamed response and yields each generated token.

**Examples**:
```python
# Example: Generating text with the 'gpt-3.5-turbo' model
messages = [
    {'role': 'user', 'content': 'Hello, how are you?'},
]
completion = _create_completion(model='gpt-3.5-turbo', messages=messages, stream=True)

# Iterate over the generated tokens
for token in completion:
    print(token) 
```