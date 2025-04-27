# DeepInfraChat Provider

## Overview

This module provides the `DeepInfraChat` class, which represents a provider for the `g4f` API, specifically for interacting with DeepInfraChat.

## Details

The `DeepInfraChat` class inherits from `OpenaiTemplate` and extends its functionality to work with the DeepInfraChat API. It defines various attributes like the API base URL, default models, vision models, and model aliases. 

## Classes

### `DeepInfraChat`

**Description**: A class that represents a DeepInfraChat provider for the `g4f` API.

**Inherits**: `OpenaiTemplate`

**Attributes**:

- `url (str)`: The base URL for the DeepInfraChat API.
- `api_base (str)`: The base URL for the DeepInfraChat API.
- `working (bool)`: Indicates whether the provider is currently working.
- `default_model (str)`: The default model for DeepInfraChat.
- `default_vision_model (str)`: The default vision model for DeepInfraChat.
- `vision_models (list[str])`: A list of supported vision models for DeepInfraChat.
- `models (list[str])`: A list of supported models for DeepInfraChat.
- `model_aliases (dict[str, str])`: A dictionary that maps model aliases to their full names.


## Functions

### `get_prompt_by_template`

**Purpose**: Retrieves a prompt based on a template and provided parameters.

**Parameters**:

- `template (str)`: The template to use for generating the prompt.
- `**kwargs`: Keyword arguments to be used for formatting the prompt.

**Returns**:

- `str`: The formatted prompt.

**Raises Exceptions**:

- `None`.

**How the Function Works**:

- The function takes a template string and keyword arguments as input.
- It formats the template using the provided keyword arguments, replacing placeholders with their corresponding values.
- The formatted prompt is then returned.

**Examples**:

```python
template = "You are a helpful AI assistant. Please {action}."
prompt = get_prompt_by_template(template, action="summarize the text")
print(prompt)  # Output: You are a helpful AI assistant. Please summarize the text.
```

### `get_response_from_url`

**Purpose**: Retrieves a response from a given URL.

**Parameters**:

- `url (str)`: The URL to request.
- `params (dict)`: Optional parameters to be added to the URL query.
- `headers (dict)`: Optional headers to be added to the request.

**Returns**:

- `dict`: The response from the URL, parsed as a dictionary.

**Raises Exceptions**:

- `None`.

**How the Function Works**:

- The function constructs a request to the provided URL, optionally adding parameters and headers.
- It then sends the request and retrieves the response from the server.
- The response is parsed as a JSON dictionary and returned.

**Examples**:

```python
url = "https://api.example.com/data"
params = {"key": "value"}
response = get_response_from_url(url, params=params)
print(response)  # Output: {'data': '...', ...}
```

### `get_response_from_api`

**Purpose**: Retrieves a response from the DeepInfraChat API using provided parameters.

**Parameters**:

- `prompt (str)`: The prompt to send to the API.
- `model (str)`: The name of the model to use for the request.
- `temperature (float)`: The temperature value to be used for the API request.
- `top_p (float)`: The top_p value to be used for the API request.
- `max_tokens (int)`: The maximum number of tokens to generate.
- `stream (bool)`: Whether to stream the response.
- `**kwargs`: Additional keyword arguments to be passed to the API.

**Returns**:

- `dict`: The response from the API, parsed as a dictionary.

**Raises Exceptions**:

- `None`.

**How the Function Works**:

- The function constructs a request to the DeepInfraChat API using the provided parameters.
- It includes the prompt, model name, temperature, top_p, max_tokens, and stream values in the request.
- The request is sent, and the response is received and parsed as a JSON dictionary.
- The function returns the parsed response.

**Examples**:

```python
prompt = "Please write a short story about a cat."
response = get_response_from_api(prompt, model="deepseek-ai/DeepSeek-V3")
print(response)  # Output: {'choices': [{'text': '...', ...}], ...}
```


## Parameter Details

- `template (str)`: The template string used for formatting the prompt.
- `action (str)`: The action to be performed by the AI assistant, used in the template formatting.
- `url (str)`: The URL to request, typically the endpoint for the API.
- `params (dict)`: Optional parameters to be included in the URL query.
- `headers (dict)`: Optional headers to be added to the request.
- `prompt (str)`: The prompt to be sent to the API, which provides instructions or context to the AI model.
- `model (str)`: The name of the model to be used for generating the response.
- `temperature (float)`: Controls the randomness of the generated text. Higher values result in more creative responses.
- `top_p (float)`: Controls the diversity of the generated text by limiting the probability distribution of possible next tokens.
- `max_tokens (int)`: Limits the maximum number of tokens to be generated in the response.
- `stream (bool)`: Whether to stream the response, allowing for incremental updates during generation.
- `**kwargs`: Additional keyword arguments that might be specific to the API or model being used.

## Examples

**Example 1: Getting a response from the DeepInfraChat API**

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.DeepInfraChat import DeepInfraChat

provider = DeepInfraChat()
prompt = "What is the capital of France?"
response = provider.get_response(prompt, model="deepseek-ai/DeepSeek-V3")
print(response)  # Output: {'choices': [{'text': 'Paris', ...}], ...}
```

**Example 2: Using a template to generate a prompt**

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.DeepInfraChat import DeepInfraChat

provider = DeepInfraChat()
template = "Translate the following text into {target_language}: {text}"
prompt = provider.get_prompt_by_template(template, target_language="Spanish", text="Hello, world!")
response = provider.get_response(prompt, model="deepseek-ai/DeepSeek-V3")
print(response)  # Output: {'choices': [{'text': '¡Hola, mundo!', ...}], ...}
```

**Example 3: Using a vision model**

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.DeepInfraChat import DeepInfraChat

provider = DeepInfraChat()
image_url = "https://example.com/image.jpg"
prompt = "Describe the image at this URL: {image_url}"
prompt = provider.get_prompt_by_template(prompt, image_url=image_url)
response = provider.get_response(prompt, model="openbmb/MiniCPM-Llama3-V-2_5")
print(response)  # Output: {'choices': [{'text': 'The image shows...', ...}], ...}
```