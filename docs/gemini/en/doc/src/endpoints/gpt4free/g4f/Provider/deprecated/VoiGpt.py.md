# Provider VoiGpt

## Overview

The `VoiGpt` module provides an implementation of the `AbstractProvider` class for interacting with the VoiGpt API. 

This module implements the `VoiGpt` class, which extends `AbstractProvider` and allows users to interact with the VoiGpt API for generating text completions. The module handles the necessary headers, requests, and response processing for interacting with the API, ensuring a streamlined user experience.


## Details

The `VoiGpt` class allows you to communicate with the VoiGpt API to generate text completions based on the provided messages. The module utilizes a `requests` library for sending HTTP requests to the API and `json` library for parsing the responses. It implements features like message history support and automatic access token retrieval to ensure a smooth API interaction. 

## Classes

### `class VoiGpt`

**Description**:  This class implements a provider for interacting with the VoiGpt API. It extends the `AbstractProvider` class and provides functionality to generate text completions based on provided messages.

**Inherits**: `AbstractProvider`

**Attributes**:
 - `url (str)`: The base URL of the VoiGpt API.
 - `working (bool)`: Indicates whether the provider is currently working or not.
 - `supports_gpt_35_turbo (bool)`: Whether the provider supports the `gpt-3.5-turbo` model.
 - `supports_message_history (bool)`: Indicates whether the provider supports message history.
 - `supports_stream (bool)`:  Whether the provider supports streaming responses.
 - `_access_token (str)`:  The access token for the VoiGpt API.

**Methods**:

- `create_completion(model: str, messages: Messages, stream: bool, proxy: str = None, access_token: str = None, **kwargs) -> CreateResult`

**Purpose**: This method is responsible for generating text completions using the VoiGpt API. It takes various arguments, including the model, messages, stream flag, proxy settings, and optional access token. 

**Parameters**:

 - `model (str)`: The model to use for generating text completions. 
 - `messages (Messages)`: A list of messages to be used for generating the completion.
 - `stream (bool)`: Whether to stream the response. 
 - `proxy (str, optional)`: The proxy to use for the API request. Defaults to None.
 - `access_token (str, optional)`: The access token to use for the API request. Defaults to None.
 - `**kwargs`: Additional keyword arguments.

**Returns**:

 - `CreateResult`: A `CreateResult` object containing the generated text completion.

**Raises Exceptions**:
 - `RuntimeError`: If an error occurs during processing the response from the API.

**Example**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.VoiGpt import VoiGpt
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Assuming you have your access token
access_token = "your_access_token"

# Example messages
messages = [
    {"role": "user", "content": "Hello, how are you?"},
    {"role": "assistant", "content": "I am doing well, thank you for asking!"}
]

# Create a VoiGpt instance and generate a completion
provider = VoiGpt(access_token=access_token)
completion = provider.create_completion(model="gpt-3.5-turbo", messages=messages, stream=False)
print(completion)
```

## Inner Functions

- `inner_function()`: None (not implemented in the provided code)

## How the Function Works:

The `create_completion` function performs the following steps:

1. **Model and Access Token**: It checks if the `model` parameter is provided. If not, it defaults to "gpt-3.5-turbo". Similarly, it checks for the `access_token` and if not provided, it tries to retrieve it from the class attribute `_access_token`.
2. **Fetching Access Token**:  If the `access_token` is still unavailable, the function sends a GET request to the `https://voigpt.com` website using the `requests` library. The headers are set to simulate a typical browser request. The access token is then extracted from the response cookies.
3. **Preparing Request Headers and Payload**: The function constructs the necessary headers for the POST request, including the `Accept-Encoding`, `Accept-Language`, `Cookie`, `Origin`, `Referer`, and `User-Agent`. It also defines the payload with the `messages` to be sent to the API. 
4. **Sending Request**: The function sends a POST request to the `https://voigpt.com/generate_response/` endpoint using the `requests` library. The request includes the constructed headers and the payload.
5. **Response Processing**: The response from the API is parsed using the `json.loads()` method. The `response["response"]` element is then yielded, allowing for iterating over the response or for directly accessing the completion text.
6. **Error Handling**: If an error occurs during JSON parsing, a `RuntimeError` exception is raised, including information from the API response.


## Parameter Details

- `access_token (str, optional)`: This is a required parameter for authentication. It is a CSRF token obtained from the VoiGpt website. 

## Examples

- **Example 1**: Generating a simple completion with a custom access token

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.VoiGpt import VoiGpt
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Example messages
messages = [
    {"role": "user", "content": "Hello, how are you?"},
    {"role": "assistant", "content": "I am doing well, thank you for asking!"}
]

# Set your access token
access_token = "your_access_token"

# Create a VoiGpt instance and generate a completion
provider = VoiGpt(access_token=access_token)
completion = provider.create_completion(model="gpt-3.5-turbo", messages=messages, stream=False)
print(completion)
```

- **Example 2**: Generating a completion without specifying an access token (retrieving it automatically)

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.VoiGpt import VoiGpt
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Example messages
messages = [
    {"role": "user", "content": "Hello, how are you?"},
    {"role": "assistant", "content": "I am doing well, thank you for asking!"}
]

# Create a VoiGpt instance and generate a completion
provider = VoiGpt()
completion = provider.create_completion(model="gpt-3.5-turbo", messages=messages, stream=False)
print(completion)
```

## Your Behavior During Code Analysis:
- Inside the code, you might encounter expressions between `<` `>`. For example: `<instruction for gemini model:Loading product descriptions into PrestaShop.>, <next, if available>. These are placeholders where you insert the relevant value.
- Always refer to the system instructions for processing code in the `hypotez` project (the first set of instructions you translated);
- Analyze the file's location within the project. This helps understand its purpose and relationship with other files. You will find the file location in the very first line of code starting with `## \\file /...`;
- Memorize the provided code and analyze its connection with other parts of the project;
- In these instructions, do not suggest code improvements. Strictly follow point 5. **Example File** when composing the response.