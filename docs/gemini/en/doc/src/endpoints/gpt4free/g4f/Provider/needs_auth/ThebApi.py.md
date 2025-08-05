# TheB.AI API Provider

## Overview

This module provides the `ThebApi` class, which implements the `OpenaiTemplate` interface for interacting with the TheB.AI API. This API is a powerful tool for natural language processing and code generation. The `ThebApi` class allows users to make requests to the API, send messages, and retrieve responses.

## Details

The `ThebApi` class inherits from the `OpenaiTemplate` class, which provides a common framework for working with various API providers. The `ThebApi` class defines specific parameters for the TheB.AI API, including the base URL, login URL, and default model. It also specifies that the API requires authentication and is currently operational.

## Classes

### `ThebApi`

**Description**: The `ThebApi` class implements the `OpenaiTemplate` interface for interacting with the TheB.AI API. 

**Inherits**: `OpenaiTemplate`

**Attributes**:

- `label` (str): The label for the API provider.
- `url` (str): The base URL for the API.
- `login_url` (str): The URL for the user login page.
- `api_base` (str): The base URL for the API endpoints.
- `working` (bool): A flag indicating whether the API is currently operational.
- `needs_auth` (bool): A flag indicating whether the API requires authentication.
- `default_model` (str): The default model to use with the API.
- `fallback_models` (list): A list of fallback models to use if the default model is not available.

**Methods**:

- `create_async_generator(model: str, messages: Messages, temperature: float = None, top_p: float = None, **kwargs) -> CreateResult`: This method creates an asynchronous generator that can be used to stream responses from the TheB.AI API. It takes the following parameters:
    - `model` (str): The model to use for the request.
    - `messages` (Messages): A list of messages to send to the API.
    - `temperature` (float): The temperature parameter for the API request.
    - `top_p` (float): The top_p parameter for the API request.
    - `**kwargs`: Additional keyword arguments to pass to the API request.
- `get_models() -> list`: This method returns a list of available models for the TheB.AI API.

## Inner Functions

None

## How the Function Works

The `create_async_generator` method first extracts the system message from the provided list of messages. It then removes any system messages from the list and constructs a dictionary containing the API request parameters, including the system prompt, temperature, and top_p values. Finally, it calls the `create_async_generator` method of the parent class (`OpenaiTemplate`) to initiate the asynchronous request.

## Examples

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.ThebApi import ThebApi
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.ThebApi import models

# Initialize the ThebApi instance
theb_api = ThebApi()

# Get a list of available models
available_models = theb_api.get_models()
print(f"Available models: {available_models}")

# Create a list of messages to send to the API
messages = [
    {"role": "system", "content": "<instruction for gemini model:Loading product descriptions into PrestaShop.>"},
    {"role": "user", "content": "Can you help me with this?"},
]

# Generate a response using the Theb-AI model
response = theb_api.create_async_generator(model=models["theb-ai"], messages=messages)

# Print the response
print(f"Response: {response}")
```

## Parameter Details

- `model` (str): The model to use for the API request. This parameter can be set to one of the following values:
    - `"theb-ai"`: The default TheB.AI model.
    - `"gpt-3.5-turbo"`: The GPT-3.5 Turbo model.
    - `"gpt-4-turbo"`: The GPT-4 Turbo model.
    - `"gpt-4"`: The GPT-4 model.
    - `"claude-3.5-sonnet"`: The Claude model.
    - `"llama-2-7b-chat"`: The Llama 2 7B model.
    - `"llama-2-13b-chat"`: The Llama 2 13B model.
    - `"llama-2-70b-chat"`: The Llama 2 70B model.
    - `"code-llama-7b"`: The Code Llama 7B model.
    - `"code-llama-13b"`: The Code Llama 13B model.
    - `"code-llama-34b"`: The Code Llama 34B model.
    - `"qwen-2-72b"`: The Qwen model.
- `messages` (Messages): A list of messages to send to the API. Each message should be a dictionary containing the following keys:
    - `"role"` (str): The role of the message sender (e.g., "system", "user", "assistant").
    - `"content"` (str): The content of the message.
- `temperature` (float): The temperature parameter controls the randomness of the generated response. A higher temperature value will produce more creative and unpredictable responses. The default value is `None`.
- `top_p` (float): The top_p parameter controls the probability distribution of the generated response. A lower top_p value will produce more predictable and consistent responses. The default value is `None`.

## Examples

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.ThebApi import ThebApi
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.ThebApi import models

# Create an instance of ThebApi
theb_api = ThebApi()

# Define a list of messages
messages = [
    {"role": "system", "content": "<instruction for gemini model:Generate a short story about a cat.>"},
    {"role": "user", "content": "What if the cat was named Whiskers?"},
]

# Generate a response with different temperature and top_p values
response_1 = theb_api.create_async_generator(model=models["theb-ai"], messages=messages, temperature=0.7, top_p=0.9)
response_2 = theb_api.create_async_generator(model=models["theb-ai"], messages=messages, temperature=1.0, top_p=0.5)

# Print the responses
print(f"Response 1 (temperature=0.7, top_p=0.9): {response_1}")
print(f"Response 2 (temperature=1.0, top_p=0.5): {response_2}")

```