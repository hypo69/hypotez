# TeachAnything Provider
## Overview
This module provides the `TeachAnything` class, a subclass of `AsyncGeneratorProvider` and `ProviderModelMixin`, for interacting with the TeachAnything API. It implements asynchronous generation of responses from the TeachAnything API using the `aiohttp` library.

## Details
The `TeachAnything` class allows you to utilize the TeachAnything API for generating responses based on user prompts. It inherits from `AsyncGeneratorProvider`, enabling asynchronous response generation, and `ProviderModelMixin`, allowing for model selection and configuration. 

The `create_async_generator` class method handles sending requests to the TeachAnything API, retrieves responses in chunks, and yields the decoded response text. The `_get_headers` static method constructs the necessary headers for API requests.

## Classes
### `TeachAnything`
**Description**: Class for interacting with the TeachAnything API, inheriting from `AsyncGeneratorProvider` and `ProviderModelMixin`.
**Inherits**: 
  - `AsyncGeneratorProvider`: Provides asynchronous response generation functionality.
  - `ProviderModelMixin`: Allows for model selection and configuration.

**Attributes**:
  - `url` (str): Base URL for the TeachAnything API.
  - `api_endpoint` (str): Endpoint for API requests.
  - `working` (bool): Indicates whether the provider is currently operational.
  - `default_model` (str): Default model to use for generation.
  - `models` (list): List of supported models.

**Methods**:
  - `create_async_generator(model: str, messages: Messages, proxy: str | None = None, **kwargs: Any) -> AsyncResult`: Asynchronously generates responses from the TeachAnything API based on the given model, messages, and optional proxy settings.
  - `_get_headers() -> Dict[str, str]`: Returns a dictionary of HTTP headers used for API requests.

## Class Methods
### `create_async_generator`
```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str | None = None,
        **kwargs: Any
    ) -> AsyncResult:
        headers = cls._get_headers()
        model = cls.get_model(model)
        
        async with ClientSession(headers=headers) as session:
            prompt = format_prompt(messages)
            data = {"prompt": prompt}
            
            timeout = ClientTimeout(total=60)
            
            async with session.post(
                f"{cls.url}{cls.api_endpoint}",
                json=data,
                proxy=proxy,
                timeout=timeout
            ) as response:
                response.raise_for_status()
                buffer = b""
                async for chunk in response.content.iter_any():
                    buffer += chunk
                    try:
                        decoded = buffer.decode('utf-8')
                        yield decoded
                        buffer = b""
                    except UnicodeDecodeError:
                        # If we can't decode, we'll wait for more data
                        continue
                
                # Handle any remaining data in the buffer
                if buffer:
                    try:
                        yield buffer.decode('utf-8', errors='replace')
                    except Exception as e:
                        print(f"Error decoding final buffer: {e}")
```
**Purpose**: Asynchronously generates responses from the TeachAnything API based on the given model, messages, and optional proxy settings.

**Parameters**:
  - `model` (str): The model to use for generation.
  - `messages` (Messages): A list of messages representing the conversation history.
  - `proxy` (str | None, optional): Optional proxy server address. Defaults to `None`.
  - `**kwargs` (Any, optional): Additional keyword arguments.

**Returns**:
  - `AsyncResult`: An asynchronous result object representing the generated response.

**Raises Exceptions**:
  - `Exception`: If an error occurs during the API request or response processing.

**How the Function Works**:
  - The function sets up an asynchronous HTTP session with the specified headers.
  - It formats the conversation history into a prompt.
  - It sends a POST request to the TeachAnything API endpoint with the prompt and optional proxy settings.
  - It retrieves the API response in chunks and yields the decoded response text as it arrives.
  - It handles any remaining data in the buffer at the end of the response stream.

**Examples**:
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.TeachAnything import TeachAnything
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

messages: Messages = [
    {"role": "user", "content": "Hello, how are you?"},
]

async def main():
    async for response_chunk in TeachAnything.create_async_generator(model='gemini-1.5-pro', messages=messages):
        print(response_chunk)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

```

### `_get_headers`
```python
    @staticmethod
    def _get_headers() -> Dict[str, str]:
        return {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "dnt": "1",
            "origin": "https://www.teach-anything.com",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://www.teach-anything.com/",
            "sec-ch-us": '"Not?A_Brand";v="99", "Chromium";v="130"',
            "sec-ch-us-mobile": "?0",
            "sec-ch-us-platform": '"Linux"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
        }
```
**Purpose**: Returns a dictionary of HTTP headers used for API requests to TeachAnything.

**Parameters**: None.

**Returns**:
  - `Dict[str, str]`: A dictionary containing the HTTP headers.

**How the Function Works**:
  - The function constructs a dictionary with common HTTP headers for API requests, including user agent, content type, and security-related headers.

**Examples**: 
  - This method is called internally by the `create_async_generator` method and is not intended for direct use by the developer.


## Parameter Details

  - `model` (str): The model to use for generation. The TeachAnything API supports several models, including 'gemini-1.5-pro' and 'gemini-1.5-flash'. 
  - `messages` (Messages): A list of messages representing the conversation history. Each message is a dictionary with the following keys:
    - `role` (str): The role of the message sender, either 'user' or 'assistant'.
    - `content` (str): The content of the message.

## Examples
- The following code demonstrates how to use the `TeachAnything` provider to generate responses:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.TeachAnything import TeachAnything
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

messages: Messages = [
    {"role": "user", "content": "Hello, how are you?"},
]

async def main():
    async for response_chunk in TeachAnything.create_async_generator(model='gemini-1.5-pro', messages=messages):
        print(response_chunk)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

```

- This code snippet creates a list of messages representing the conversation history.
- The `create_async_generator` class method is called with the desired model and messages.
- The `async for` loop iterates over the generated response chunks and prints them to the console.