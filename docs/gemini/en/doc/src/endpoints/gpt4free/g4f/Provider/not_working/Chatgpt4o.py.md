# Chatgpt4o Provider
## Overview

The `Chatgpt4o` provider is a class responsible for communicating with the chatgpt4o.one API to generate responses from the GPT-4O model. 

## Details

The Chatgpt4o provider utilizes a StreamSession to make asynchronous HTTP requests to the chatgpt4o.one API. It handles tasks such as:

* **Authentication and Authorization:** Retrieves necessary parameters, such as `_post_id` and `_nonce`, from the chatgpt4o.one website.
* **Request Formatting:** Formats messages into a structure compatible with the chatgpt4o.one API.
* **Response Handling:** Processes responses from the API, extracts relevant data, and checks for errors.

## Classes

### `class Chatgpt4o`

**Description:** Provides an asynchronous interface for interacting with the chatgpt4o.one API. 

**Inherits:** 
* `AsyncProvider`: Defines methods for asynchronous interaction with a provider.
* `ProviderModelMixin`: Provides functionality for managing model options and aliases.

**Attributes:**

* `url`: The base URL for the chatgpt4o.one API.
* `working`: Indicates whether the provider is currently functional (set to `False` as this provider is not working).
* `_post_id`: A unique identifier used in API requests.
* `_nonce`: A security token used in API requests.
* `default_model`: The default GPT-4O model to use.
* `models`: A list of supported GPT-4O models.
* `model_aliases`: A dictionary mapping aliases to actual model names.

**Methods:**

* `create_async(model: str, messages: Messages, proxy: str = None, timeout: int = 120, cookies: dict = None, **kwargs) -> str`

**Purpose:** Sends a request to the chatgpt4o.one API with the given `model`, `messages`, and optional parameters.

**Parameters:**

* `model (str)`: The GPT-4O model to use.
* `messages (Messages)`: A list of messages to be sent to the model.
* `proxy (str, optional)`: A proxy server to use for the request. Defaults to `None`.
* `timeout (int, optional)`: The timeout for the request in seconds. Defaults to `120`.
* `cookies (dict, optional)`: A dictionary of cookies to send with the request. Defaults to `None`.
* `**kwargs`: Additional keyword arguments to pass to the `StreamSession`.

**Returns:**

* `str`: The response from the API as a string.

**Raises Exceptions:**

* `RuntimeError`: Raised if there are errors retrieving necessary parameters (`_post_id`, `_nonce`) from the chatgpt4o.one website.
* `RuntimeError`: Raised if the API response does not contain the expected `'data'` field.

**How the Function Works:**

1. **Retrieve Parameters:** The function checks if `_post_id` and `_nonce` have been initialized. If not, it performs a GET request to the chatgpt4o.one homepage to extract these parameters from the HTML response. 
2. **Format Prompt:** The `messages` are formatted into a prompt string using the `format_prompt` function. 
3. **Send Request:** A POST request is sent to the `/wp-admin/admin-ajax.php` endpoint with the formatted prompt, `_post_id`, `_nonce`, and other necessary parameters.
4. **Process Response:** The response is parsed as JSON. If the `'data'` field is present, it is returned as a string.

**Example:**

```python
# Creating a Chatgpt4o instance
provider = Chatgpt4o()

# Example messages to be sent to the model
messages = [
    {"role": "user", "content": "Hello, what is the meaning of life?"},
]

# Sending a request to the API
response = await provider.create_async(model='gpt-4o-mini-2024-07-18', messages=messages)

# Printing the response
print(response)
```

## Parameter Details

* `model (str)`: The specific GPT-4O model to use for generating responses. Supported models include `gpt-4o-mini-2024-07-18`, `gpt-4o-mini`, and potentially others.
* `messages (Messages)`: A list of messages to be processed by the model. Each message should be a dictionary containing the following keys:
    * `role (str)`: Indicates the role of the speaker (e.g., `'user'`, `'assistant'`).
    * `content (str)`: The text content of the message.
* `proxy (str, optional)`: A proxy server to use for the HTTP request. This allows users to bypass network restrictions or improve privacy.
* `timeout (int, optional)`: The maximum time in seconds to wait for a response from the API. 
* `cookies (dict, optional)`: A dictionary of cookies to be sent with the request. These can be used for session management or personalization.
* `**kwargs`: Allows for passing additional keyword arguments to the `StreamSession`.

## Examples

```python
# Example 1: Simple request with default model
messages = [
    {"role": "user", "content": "What is the capital of France?"},
]
response = await Chatgpt4o.create_async(model='gpt-4o-mini-2024-07-18', messages=messages)
print(response)  # Output: "Paris"

# Example 2: Request with a specific model
messages = [
    {"role": "user", "content": "Write a poem about a cat."},
]
response = await Chatgpt4o.create_async(model='gpt-4o-mini', messages=messages)
print(response)  # Output: A poem about a cat

# Example 3: Request with a proxy server
messages = [
    {"role": "user", "content": "What is the weather like today?"},
]
response = await Chatgpt4o.create_async(model='gpt-4o-mini-2024-07-18', messages=messages, proxy='http://proxy.example.com:8080')
print(response)  # Output: The weather forecast for today