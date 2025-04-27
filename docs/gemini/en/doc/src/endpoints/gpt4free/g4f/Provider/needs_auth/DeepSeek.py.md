# DeepSeek Provider for GPT4Free

## Overview

This module implements the `DeepSeek` class, which provides an interface to the DeepSeek API for GPT4Free. DeepSeek is an AI-powered language model that can be used for a variety of tasks, including text generation, translation, and summarization.

## Details

The `DeepSeek` class inherits from the `OpenaiAPI` class, providing a common interface for interacting with different language models. It defines the necessary configuration parameters for accessing the DeepSeek API, including the API base URL, the default model, and whether authentication is required.

## Classes

### `DeepSeek`

**Description:**
The `DeepSeek` class provides a wrapper for the DeepSeek API, handling authentication, model selection, and API requests.

**Inherits:**
  `OpenaiAPI` class

**Attributes:**
  - `label` (str): "DeepSeek" - a label for the provider.
  - `url` (str): "https://platform.deepseek.com" - the main URL of the DeepSeek platform.
  - `login_url` (str): "https://platform.deepseek.com/api_keys" - the URL for accessing the DeepSeek API keys.
  - `working` (bool): `True` - indicates that the provider is currently functional.
  - `api_base` (str): "https://api.deepseek.com" - the base URL for the DeepSeek API.
  - `needs_auth` (bool): `True` - indicates that authentication is required for accessing the API.
  - `supports_stream` (bool): `True` - indicates that the API supports streaming responses.
  - `supports_message_history` (bool): `True` - indicates that the API supports message history.
  - `default_model` (str): "deepseek-chat" - the default model to use with the API.
  - `fallback_models` (list): [default_model] - a list of fallback models to use if the default model is unavailable.

**Methods:**

- **`__init__(self, api_key: str | None = None, model: str | None = None, max_tokens: int = 2048, temperature: float = 0.7, top_p: float = 1.0, frequency_penalty: float = 0.0, presence_penalty: float = 0.0, stop: list | None = None, stream: bool = False, **kwargs: Any):`**:
    - **Purpose:** Initializes the `DeepSeek` object, setting up the API connection and configuration.
    - **Parameters:**
      - `api_key` (str | None, optional): The API key for the DeepSeek API. Defaults to `None`.
      - `model` (str | None, optional): The specific DeepSeek model to use. Defaults to `None`.
      - `max_tokens` (int, optional): Maximum number of tokens to generate in the response. Defaults to `2048`.
      - `temperature` (float, optional): Controls the randomness of the generated text. Defaults to `0.7`.
      - `top_p` (float, optional): Controls the probability distribution of the generated text. Defaults to `1.0`.
      - `frequency_penalty` (float, optional): Penalty for using frequently used words. Defaults to `0.0`.
      - `presence_penalty` (float, optional): Penalty for using previously generated words. Defaults to `0.0`.
      - `stop` (list | None, optional): A list of stop sequences to use for generation. Defaults to `None`.
      - `stream` (bool, optional): Whether to stream the response or not. Defaults to `False`.
      - `**kwargs` (Any, optional): Additional keyword arguments to pass to the API request.
- **`get_message(self, message: str, history: list | None = None, stream: bool = False, **kwargs: Any) -> str | list[dict]:`**:
    - **Purpose:** Sends a message to the DeepSeek API and retrieves the response.
    - **Parameters:**
      - `message` (str): The message to send to the API.
      - `history` (list | None, optional): A list of previous messages in the conversation. Defaults to `None`.
      - `stream` (bool, optional): Whether to stream the response or not. Defaults to `False`.
      - `**kwargs` (Any, optional): Additional keyword arguments to pass to the API request.
    - **Returns:**
      - `str | list[dict]:` The response from the API.
- **`request_api(self, model: str | None = None, endpoint: str | None = None, method: str = "POST", body: dict | str | None = None, headers: dict | None = None, stream: bool = False, **kwargs: Any) -> dict | None: `**:
    - **Purpose:** Sends a generic API request to the DeepSeek API.
    - **Parameters:**
      - `model` (str | None, optional): The specific model to use for the request. Defaults to `None`.
      - `endpoint` (str | None, optional): The API endpoint to target. Defaults to `None`.
      - `method` (str, optional): The HTTP method to use. Defaults to "POST".
      - `body` (dict | str | None, optional): The request body data. Defaults to `None`.
      - `headers` (dict | None, optional): Additional headers for the request. Defaults to `None`.
      - `stream` (bool, optional): Whether to stream the response. Defaults to `False`.
      - `**kwargs` (Any, optional): Additional keyword arguments to pass to the API request.
    - **Returns:**
      - `dict | None`: The response from the API as a dictionary or `None` if an error occurs.
- **`_handle_response(self, response: requests.Response, stream: bool = False) -> str | list[dict]:`**:
    - **Purpose:** Processes the response from the DeepSeek API, handling different response formats.
    - **Parameters:**
      - `response` (requests.Response): The response object from the API request.
      - `stream` (bool, optional): Whether the response is streamed or not. Defaults to `False`.
    - **Returns:**
      - `str | list[dict]:` The processed response data.
- **`authenticate(self, api_key: str | None = None) -> bool: `**:
    - **Purpose:** Authenticates with the DeepSeek API using the provided API key.
    - **Parameters:**
      - `api_key` (str | None, optional): The API key to use for authentication. Defaults to `None`.
    - **Returns:**
      - `bool`: `True` if authentication is successful, `False` otherwise.

## Parameter Details

- `api_key` (str): The API key provided by DeepSeek for accessing the API.
- `model` (str): The specific DeepSeek model to use for the request.
- `max_tokens` (int): The maximum number of tokens to generate in the response.
- `temperature` (float): Controls the randomness of the generated text.
- `top_p` (float): Controls the probability distribution of the generated text.
- `frequency_penalty` (float): Penalty for using frequently used words.
- `presence_penalty` (float): Penalty for using previously generated words.
- `stop` (list): A list of stop sequences to use for generation.
- `stream` (bool): Whether to stream the response or not.
- `history` (list): A list of previous messages in the conversation.
- `endpoint` (str): The API endpoint to target for the request.
- `method` (str): The HTTP method to use for the request.
- `body` (dict | str): The request body data.
- `headers` (dict): Additional headers for the request.

## Examples

```python
# Creating a DeepSeek object
deepseek = DeepSeek(api_key="YOUR_API_KEY")

# Generating text
response = deepseek.get_message("Hello, how are you?")
print(response)

# Sending a request to a specific endpoint
response = deepseek.request_api(endpoint="/v1/chat/completions", method="POST", body={"message": "Hello, world!"})
print(response)
```

## How the Class Works

The `DeepSeek` class provides a convenient way to interact with the DeepSeek API without needing to deal directly with low-level HTTP requests. It handles authentication, model selection, and response processing.

When a request is made using `get_message` or `request_api`, the class:

1. Authenticates with the DeepSeek API if necessary.
2. Constructs the API request URL and headers based on the provided parameters.
3. Sends the request to the API using the `requests` library.
4. Processes the response, handling different response formats and extracting relevant data.
5. Returns the processed response data.

This class simplifies the process of using the DeepSeek API for various tasks, such as text generation, translation, and summarization.