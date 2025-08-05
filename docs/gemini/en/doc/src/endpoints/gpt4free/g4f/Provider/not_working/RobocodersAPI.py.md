# Robocoders API Provider

## Overview

This module implements the `RobocodersAPI` class, which acts as a provider for interacting with the Robocoders AI API for code generation and assistance. 

## Details

The `RobocodersAPI` class inherits from `AsyncGeneratorProvider` and `ProviderModelMixin` to provide asynchronous code generation capabilities and support for different AI models. The class leverages the Robocoders AI API to handle requests, process responses, and return generated code.

## Classes

### `class RobocodersAPI(AsyncGeneratorProvider, ProviderModelMixin)`

**Description**: This class provides an asynchronous interface to interact with the Robocoders AI API. It handles communication with the API, manages access tokens, and parses responses.

**Inherits**:
- `AsyncGeneratorProvider`: This class provides an asynchronous generator interface for iterating over generated responses.
- `ProviderModelMixin`: This mixin class provides support for selecting and using different AI models from Robocoders AI.

**Attributes**:

- `label (str)`: A descriptive label for the provider, "API Robocoders AI".
- `url (str)`: The base URL for the Robocoders AI documentation.
- `api_endpoint (str)`: The endpoint URL for sending chat requests to the Robocoders AI API.
- `working (bool)`:  Indicates whether the provider is currently working or not.
- `supports_message_history (bool)`:  Indicates whether the provider supports message history.
- `default_model (str)`: The default AI model used by the provider, "GeneralCodingAgent".
- `agent (List[str])`: A list of available AI agents, including "GeneralCodingAgent", "RepoAgent", and "FrontEndAgent".
- `models (List[str])`:  A list of all supported AI models, derived from the `agent` list.
- `CACHE_DIR (Path)`: The directory path where access tokens and session IDs are cached.
- `CACHE_FILE (Path)`: The path to the cache file for storing access token and session data.

**Methods**:

- `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`: This method initializes an asynchronous generator that interacts with the Robocoders AI API to generate code. It handles authentication, sending requests, and parsing responses.
- `_get_or_create_access_and_session(session: aiohttp.ClientSession) -> Tuple[str, str]`:  This method handles authentication with the Robocoders AI API by retrieving or generating an access token and session ID. It checks the cache for existing credentials, and if necessary, fetches a new access token and creates a new session ID.
- `_fetch_and_cache_access_token(session: aiohttp.ClientSession) -> str`: This method fetches a new access token from the Robocoders AI API and caches it locally for future use.
- `_create_and_cache_session(session: aiohttp.ClientSession, access_token: str) -> str`: This method creates a new session ID with the Robocoders AI API, using the provided access token, and caches the session ID for subsequent requests.
- `_save_cached_data(new_data: dict)`: This method saves new data to the cache file.
- `_update_cached_data(updated_data: dict)`: This method updates existing cache data with new values.
- `_clear_cached_data()`: This method removes the cache file.
- `_get_cached_data() -> dict`: This method retrieves all cached data from the cache file.

**Examples**:
```python
# Example Usage
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.RobocodersAPI import RobocodersAPI

async def main():
    model = "GeneralCodingAgent"
    messages = [
        {"role": "user", "content": "Generate a Python function to reverse a string."},
    ]
    async for response in RobocodersAPI.create_async_generator(model=model, messages=messages):
        print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## Class Methods

### `_get_or_create_access_and_session`

**Purpose**: This method handles authentication with the Robocoders AI API by retrieving or generating an access token and session ID.

**Parameters**:

- `session (aiohttp.ClientSession)`:  An instance of the `aiohttp.ClientSession` class used for making HTTP requests.

**Returns**:

- `Tuple[str, str]`: A tuple containing the access token and session ID, or `None` if authentication fails.

**Raises Exceptions**:

- `Exception`: If there is an error initializing API interaction.

**How the Function Works**:

- The method first attempts to load cached access token and session ID from the `CACHE_FILE`.
- If the cached data is valid, it returns the loaded values.
- If the cached data is invalid, it calls `_fetch_and_cache_access_token` to fetch a new access token and `_create_and_cache_session` to create a new session ID.
- The newly generated access token and session ID are then returned.

**Examples**:

```python
# Example Usage
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.RobocodersAPI import RobocodersAPI

async def get_access_and_session(session):
    access_token, session_id = await RobocodersAPI._get_or_create_access_and_session(session)
    print(f"Access Token: {access_token}")
    print(f"Session ID: {session_id}")

if __name__ == "__main__":
    import asyncio
    import aiohttp
    async with aiohttp.ClientSession() as session:
        asyncio.run(get_access_and_session(session))
```

### `_fetch_and_cache_access_token`

**Purpose**: This method fetches a new access token from the Robocoders AI API and caches it locally for future use.

**Parameters**:

- `session (aiohttp.ClientSession)`:  An instance of the `aiohttp.ClientSession` class used for making HTTP requests.

**Returns**:

- `str`: The newly fetched access token, or `None` if the fetch fails.

**Raises Exceptions**:

- `MissingRequirementsError`: If the "beautifulsoup4" package is not installed.

**How the Function Works**:

- The method first checks if the "beautifulsoup4" package is installed. If not, it raises a `MissingRequirementsError`.
- The method makes a GET request to the Robocoders AI authorization endpoint (`url_auth`) to retrieve the access token.
- The response is parsed using BeautifulSoup to extract the token from the HTML content.
- The extracted token is then saved to the `CACHE_FILE` for future use.
- The method returns the fetched access token.

**Examples**:

```python
# Example Usage
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.RobocodersAPI import RobocodersAPI

async def fetch_access_token(session):
    access_token = await RobocodersAPI._fetch_and_cache_access_token(session)
    print(f"Access Token: {access_token}")

if __name__ == "__main__":
    import asyncio
    import aiohttp
    async with aiohttp.ClientSession() as session:
        asyncio.run(fetch_access_token(session))
```

### `_create_and_cache_session`

**Purpose**: This method creates a new session ID with the Robocoders AI API, using the provided access token, and caches the session ID for subsequent requests.

**Parameters**:

- `session (aiohttp.ClientSession)`: An instance of the `aiohttp.ClientSession` class used for making HTTP requests.
- `access_token (str)`: The access token used for authentication.

**Returns**:

- `str`: The newly created session ID, or `None` if the creation fails.

**Raises Exceptions**:

- `Exception`: If the API response indicates an unauthorized error.
- `Exception`: If the API response indicates a validation error.

**How the Function Works**:

- The method makes a GET request to the Robocoders AI session creation endpoint (`url_create_session`), using the provided access token.
- The response is parsed to extract the session ID (`sid`).
- The session ID is then saved to the `CACHE_FILE`.
- The method returns the newly created session ID.

**Examples**:

```python
# Example Usage
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.RobocodersAPI import RobocodersAPI

async def create_session(session, access_token):
    session_id = await RobocodersAPI._create_and_cache_session(session, access_token)
    print(f"Session ID: {session_id}")

if __name__ == "__main__":
    import asyncio
    import aiohttp
    async with aiohttp.ClientSession() as session:
        access_token = "YOUR_ACCESS_TOKEN"  # Replace with your actual access token
        asyncio.run(create_session(session, access_token))
```

## Parameter Details

- `model (str)`:  The AI model to use for code generation.
- `messages (Messages)`: A list of messages containing user input and previous responses, used for context.
- `proxy (str)`:  Optional proxy server to use for network requests.
- `session (aiohttp.ClientSession)`: An instance of the `aiohttp.ClientSession` class used for making HTTP requests.
- `access_token (str)`: The access token used for authentication with the Robocoders AI API.
- `new_data (dict)`: New data to save to the cache file.
- `updated_data (dict)`:  New values to update the existing cache data with.

## Examples

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.RobocodersAPI import RobocodersAPI

async def generate_code(model, messages):
    async for response in RobocodersAPI.create_async_generator(model=model, messages=messages):
        print(response)

if __name__ == "__main__":
    import asyncio
    import aiohttp

    # Example 1: Basic code generation
    model = "GeneralCodingAgent"
    messages = [
        {"role": "user", "content": "Generate a Python function to reverse a string."},
    ]
    asyncio.run(generate_code(model, messages))

    # Example 2: Using a different model
    model = "RepoAgent"
    messages = [
        {"role": "user", "content": "Create a Git commit with the message 'Updated documentation'."},
    ]
    asyncio.run(generate_code(model, messages))

    # Example 3: Using a proxy server
    model = "GeneralCodingAgent"
    messages = [
        {"role": "user", "content": "What are the benefits of using a proxy server?"},
    ]
    proxy = "http://your_proxy_server:port"  # Replace with your proxy server details
    asyncio.run(generate_code(model, messages, proxy=proxy))
```

## Conclusion

The `RobocodersAPI` class provides a streamlined interface to interact with the Robocoders AI API for code generation and assistance. It handles authentication, caching of credentials, and asynchronous response processing, making it convenient to integrate with other applications.