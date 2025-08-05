# Provider for Google Gemini API
## Overview

This module provides the `GeminiPro` class, which implements the `AsyncGeneratorProvider` and `ProviderModelMixin` interfaces to interact with the Google Gemini API for generating text, translating languages, writing different kinds of creative content, and answering your questions in an informative way. This class provides functionality for asynchronous text generation, utilizing the Google Gemini API and utilizing all the features available from the Gemini Pro model.  It utilizes an asynchronous generator for efficient handling of API responses, stream processing, and resource management.

## Details

The `GeminiPro` class leverages the Google Gemini API for text generation. It supports various features, including:

- Asynchronous text generation with stream processing capabilities.
- Handling user and assistant messages, as well as system messages (for setting the context).
-  Authenticating with a Google API key.
- Managing API requests for different model variations (e.g., `gemini-1.5-pro`, `gemini-2.0-flash-exp`, `gemini-pro`).
-  Integrating with the `src.logger` module for logging information and errors.
-  Support for image processing, allowing input and analysis of image data. 
-  Utilization of tools for task completion, as specified by the `tools` parameter.
-  Support for various request parameters, such as temperature, top_p, top_k, max_tokens, and stop sequences, for controlling generation behavior. 

## Classes

### `class GeminiPro`

**Description**: This class provides access to the Google Gemini API.

**Inherits**: 
- `AsyncGeneratorProvider`: Defines the basic interface for asynchronous text generation providers.
- `ProviderModelMixin`: Provides model-specific features and management.

**Attributes**:

- `label (str)`:  Descriptive label for the provider (e.g., "Google Gemini API").
- `url (str)`: The base URL for the Google Gemini API.
- `login_url (str)`: The URL for obtaining a Google API key.
- `api_base (str)`: The base URL for the Gemini API's endpoint.
- `working (bool)`: Indicates whether the provider is currently operational.
- `supports_message_history (bool)`: True if the provider supports message history.
- `supports_system_message (bool)`: True if the provider supports system messages.
- `needs_auth (bool)`: True if the provider requires authentication (API key).
- `default_model (str)`: The default Gemini model to use.
- `default_vision_model (str)`: The default vision model (same as default_model for compatibility).
- `fallback_models (list[str])`: A list of fallback models to use if the default model is unavailable.
- `model_aliases (dict[str, str])`: A dictionary for mapping model aliases to their actual model names.

**Methods**:

#### `get_models(cls, api_key: str = None, api_base: str = api_base) -> list[str]`

**Purpose**: Retrieves a list of available Gemini models.

**Parameters**:

- `api_key (str)`: Google API key for authentication.
- `api_base (str)`: Base URL for the Gemini API (defaults to the class attribute).

**Returns**:

- `list[str]`: A list of model names, or a list of fallback models if authentication fails.

**Raises Exceptions**:

- `MissingAuthError`: If the provided API key is invalid.

**How the Function Works**:

1.  If the `models` attribute is not populated, the function fetches model information from the Google Gemini API.
2.  It constructs the API URL using the provided `api_base` (or the class attribute if `api_base` is not provided).
3.  It sends a GET request to the API, including the provided `api_key` in the query parameters.
4.  The function checks for successful response status using `raise_for_status`.
5.  The JSON response is parsed, and model names are extracted. 
6.  Only models with a `supportedGenerationMethods` attribute containing "generateContent" are included in the returned list. 
7.  Models are sorted alphabetically.
8.  In case of an error, the function logs the error using `debug.error(e)` and, if an API key is provided, raises a `MissingAuthError`. Otherwise, it returns the fallback models.

#### `create_async_generator(cls, model: str, messages: Messages, stream: bool = False, proxy: str = None, api_key: str = None, api_base: str = api_base, use_auth_header: bool = False, media: MediaListType = None, tools: Optional[list] = None, connector: BaseConnector = None, **kwargs) -> AsyncResult`

**Purpose**: Creates an asynchronous generator for interacting with the Google Gemini API.

**Parameters**:

- `model (str)`: The name of the Gemini model to use for text generation.
- `messages (Messages)`: A list of user and assistant messages (possibly including system messages).
- `stream (bool)`: Set to `True` to enable stream processing for receiving responses in real-time.
- `proxy (str)`: Proxy server address to use for API requests.
- `api_key (str)`: The Google API key for authentication.
- `api_base (str)`: The base URL for the Gemini API.
- `use_auth_header (bool)`: Set to `True` to include the API key in the request header instead of the query parameters.
- `media (MediaListType)`:  A list of media data (images) for the request. 
- `tools (Optional[list])`: A list of tools (functions) to be available for the model to use during generation. 
- `connector (BaseConnector)`: An optional connector for the client session (useful for setting specific network options).
- `**kwargs`: Additional parameters, including `stop` (stop sequences), `temperature`, `max_tokens`, `top_p`, and `top_k` for controlling text generation.

**Returns**:

- `AsyncResult`: An asynchronous result object.

**Raises Exceptions**:

- `MissingAuthError`: If the API key is missing.

**How the Function Works**:

1.  The function checks if an API key is provided. If not, it raises a `MissingAuthError`.
2.  The specified model is retrieved using `cls.get_model`, which handles model aliases and fallback models.
3.  Based on the `use_auth_header` setting, either the API key is placed in the request header or the query parameters.
4.  The API URL is constructed using the `api_base` and the chosen model name.
5.  An asynchronous client session is created with the appropriate headers and connector settings.
6.  The user and assistant messages from `messages` are prepared for the API request.
7.  Any media data in `media` is encoded and included in the request.
8.  A dictionary containing the API request payload is constructed. This includes the messages, generation settings (temperature, max_tokens, etc.), and potential tools.
9.  System messages are added to the request if present.
10. The API POST request is sent to the constructed URL.
11.  The response is checked for success using `response.ok`. 
12.  If stream processing is enabled, the function yields chunks of text data as they are received. This also includes the `FinishReason` and `Usage` objects when available.
13. If stream processing is not enabled, the function retrieves the entire response as JSON and yields the generated text.

## Parameter Details

- `model (str)`: Name of the Gemini model to use (e.g., "gemini-1.5-pro").
- `messages (Messages)`:  A list of dictionaries representing user and assistant messages, each with a `role` (user or assistant) and a `content` (text) key.
- `stream (bool)`:  Whether to enable stream processing for receiving responses in real-time.
- `proxy (str)`:  Proxy server address to use for API requests.
- `api_key (str)`:  Google API key for authentication.
- `api_base (str)`:  Base URL for the Gemini API endpoint.
- `use_auth_header (bool)`: Whether to include the API key in the request header or query parameters.
- `media (MediaListType)`:  A list of tuples, each containing a media data object and a filename (for image processing).
- `tools (Optional[list])`: A list of dictionaries representing available tools. Each tool definition includes:
    - `name`:  The name of the function.
    - `description`:  A description of the function's purpose.
    - `parameters`:  A dictionary specifying the function parameters.
    - `properties`: A dictionary mapping parameter names to their type and description.
- `connector (BaseConnector)`:  An optional connector for the client session (for network configuration).
- `stop (Optional[list])`: A list of stop sequences for the model to consider during text generation.
- `temperature (float)`:  The temperature parameter controls the randomness of the generated text.
- `max_tokens (int)`:  Maximum number of tokens to generate.
- `top_p (float)`:  Probability threshold for sampling during text generation.
- `top_k (int)`:  Number of tokens to consider during sampling.


## Examples

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.GeminiPro import GeminiPro
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.GeminiPro import Messages

# Create an instance of the GeminiPro provider
gemini_provider = GeminiPro(api_key="YOUR_API_KEY")

# Define the messages for the conversation
messages = Messages([
    {"role": "user", "content": "Hello, how are you?"},
    {"role": "assistant", "content": "I am doing well, thank you! How can I help you today?"}
])

# Generate text using the GeminiPro model
async for response in gemini_provider.create_async_generator(model="gemini-1.5-pro", messages=messages):
    print(response)

# Example with media data
media = [("your_image_bytes", "image.png")]

async for response in gemini_provider.create_async_generator(
    model="gemini-1.5-pro",
    messages=messages,
    media=media,
    temperature=0.7,
    max_tokens=50
):
    print(response)
```

```python
# Example with tools 
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.GeminiPro import GeminiPro
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.GeminiPro import Messages

tools = [
    {
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "title": "Location to get the weather for"
                    }
                }
            }
        }
    }
]

gemini_provider = GeminiPro(api_key="YOUR_API_KEY")

messages = Messages([
    {"role": "user", "content": "What's the weather like in London?"}
])

async for response in gemini_provider.create_async_generator(
    model="gemini-1.5-pro",
    messages=messages,
    tools=tools
):
    print(response)