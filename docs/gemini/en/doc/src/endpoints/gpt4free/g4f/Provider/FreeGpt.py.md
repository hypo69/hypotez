# FreeGPT Provider
## Overview

This module provides the `FreeGpt` class, which acts as a provider for accessing the FreeGPT API. 

FreeGPT is a free API that allows users to interact with several language models, including Gemini and OpenAI. This module simplifies interactions with the FreeGPT API by offering a high-level interface, handling tasks such as building requests and handling responses.

## Details
This module is part of the larger `hypotez` project. `hypotez` aims to provide a comprehensive framework for working with AI models for various tasks, particularly in the domain of product descriptions and e-commerce.

This particular module is dedicated to providing access to FreeGPT, which serves as a free alternative to more expensive APIs like OpenAI. It allows users to utilize powerful language models without incurring significant costs. This is important for developers and businesses who are starting out or working within budget constraints.

## Classes
### `class FreeGpt`

**Description**: This class represents the FreeGPT provider and provides methods for interacting with the FreeGPT API. It inherits from the `AsyncGeneratorProvider` and `ProviderModelMixin` classes.

**Inherits**:
    - `AsyncGeneratorProvider`:  This class is a base class for asynchronous providers that return data in the form of a generator.
    - `ProviderModelMixin`: This class provides common methods for managing language models, including the ability to set the default model and access a list of supported models.

**Attributes**:
    - `url`: The base URL for the FreeGPT API.
    - `working`: A boolean flag indicating whether the provider is currently operational.
    - `supports_message_history`: A boolean flag indicating whether the provider supports message history.
    - `supports_system_message`: A boolean flag indicating whether the provider supports system messages.
    - `default_model`: The default language model to use with the provider.
    - `models`: A list of supported language models for the provider.

**Methods**:
    - `create_async_generator`: This method creates an asynchronous generator that streams responses from the FreeGPT API. 
    - `_build_request_data`:  This method constructs the request data for sending to the FreeGPT API.

## Class Methods
### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: Optional[str] = None,
        timeout: int = 120,
        **kwargs: Any
    ) -> AsyncGenerator[str, None]:
        prompt = messages[-1]["content"]
        timestamp = int(time.time())
        data = cls._build_request_data(messages, prompt, timestamp)

        domain = random.choice(DOMAINS)

        async with StreamSession(
            impersonate="chrome",
            timeout=timeout,
            proxies={"all": proxy} if proxy else None
        ) as session:
            async with session.post(f"{domain}/api/generate", json=data) as response:
                await raise_for_status(response)
                async for chunk in response.iter_content():
                    chunk_decoded = chunk.decode(errors="ignore")
                    if chunk_decoded == RATE_LIMIT_ERROR_MESSAGE:
                        raise RateLimitError("Rate limit reached")
                    yield chunk_decoded
```

**Purpose**: This method creates an asynchronous generator that streams responses from the FreeGPT API. It handles tasks such as:

- Generating a timestamp for the request.
- Building the request data using the `_build_request_data` method.
- Choosing a random domain from the list of available domains.
- Creating a `StreamSession` to handle the request.
- Sending the request to the API.
- Handling rate limiting errors.
- Yielding chunks of the response data.

**Parameters**:
- `model`: The language model to use for generating responses.
- `messages`: A list of messages, containing the history of the conversation.
- `proxy`: Optional proxy server to use. Defaults to None.
- `timeout`: Timeout for the request in seconds. Defaults to 120 seconds.
- `kwargs`: Additional keyword arguments.

**Returns**:
- `AsyncGenerator[str, None]`: An asynchronous generator that yields chunks of the response data.

**Raises Exceptions**:
- `RateLimitError`: If the API encounters a rate limit.
- `Exception`: If an error occurs while making the request.

**How the Function Works**:
1. The method begins by extracting the prompt from the last message in the `messages` list.
2. It generates a timestamp to be included in the request.
3. It calls the `_build_request_data` method to construct the request data.
4. It randomly selects a domain from the `DOMAINS` list.
5. It creates a `StreamSession` object, specifying the impersonation mode, timeout, and optional proxy settings.
6. It sends a POST request to the FreeGPT API endpoint `/api/generate` with the constructed request data.
7. It uses `raise_for_status` to check if the request was successful.
8. It iterates through the response content chunks.
9. It decodes each chunk and checks if it contains the rate limit error message. If so, it raises a `RateLimitError`.
10. If no error occurs, it yields the decoded chunk of data.

**Examples**:
```python
async def example():
    messages = [{"role": "user", "content": "Hello, how are you?"}]
    async for chunk in FreeGpt.create_async_generator(model='gemini-1.5-pro', messages=messages):
        print(chunk, end="")

await example()
```

### `_build_request_data`

```python
    @staticmethod
    def _build_request_data(messages: Messages, prompt: str, timestamp: int, secret: str = "") -> Dict[str, Any]:
        return {
            "messages": messages,
            "time": timestamp,
            "pass": None,
            "sign": generate_signature(timestamp, prompt, secret)
        }
```

**Purpose**: This method constructs the request data for sending to the FreeGPT API. 

**Parameters**:
- `messages`: A list of messages, containing the history of the conversation.
- `prompt`: The current prompt for the AI model.
- `timestamp`: The timestamp for the request.
- `secret`: A secret key, which can be used for additional security. Defaults to an empty string.

**Returns**:
- `Dict[str, Any]`: A dictionary containing the request data.

**How the Function Works**:
- The method creates a dictionary with the following key-value pairs:
    - `messages`: The list of messages.
    - `time`: The timestamp.
    - `pass`: This field is set to `None`.
    - `sign`:  This field is calculated by calling the `generate_signature` function.

**Examples**:
```python
messages = [{"role": "user", "content": "Hello, how are you?"}]
prompt = "Hello, how are you?"
timestamp = int(time.time())
request_data = FreeGpt._build_request_data(messages, prompt, timestamp)
print(request_data)
```

## Functions
### `generate_signature`

```python
def generate_signature(timestamp: int, message: str, secret: str = "") -> str:
    data = f"{timestamp}:{message}:{secret}"
    return hashlib.sha256(data.encode()).hexdigest()
```

**Purpose**: This function calculates the SHA-256 signature for the request data. 

**Parameters**:
- `timestamp`: The timestamp for the request.
- `message`: The message to be included in the signature calculation.
- `secret`: An optional secret key to use for additional security. Defaults to an empty string.

**Returns**:
- `str`: The hexadecimal representation of the SHA-256 hash.

**How the Function Works**:
- The function concatenates the timestamp, message, and secret key into a single string.
- It then encodes this string using UTF-8.
- It calculates the SHA-256 hash of the encoded string.
- It returns the hexadecimal representation of the hash.

**Examples**:
```python
timestamp = int(time.time())
message = "Hello, how are you?"
signature = generate_signature(timestamp, message)
print(signature)
```

## Parameter Details
- `model`: (str) - The language model to be used for generating responses. FreeGPT supports several models, including Gemini models and OpenAI models. 
- `messages`: (Messages) - This is a list of dictionaries that represent the conversation history. Each dictionary in the list represents a single message and has the following structure:
    - `role`: (str) - The role of the message sender. This can be 'user', 'assistant', or 'system'.
    - `content`: (str) - The content of the message.
- `proxy`: (Optional[str]) - An optional proxy server to be used for making API requests. It can be used to bypass network restrictions or improve performance.
- `timeout`: (int) - The timeout value for the API request. It defines the maximum amount of time the request will wait for a response.
- `kwargs`: (Any) - This parameter allows for passing additional keyword arguments to the `create_async_generator` method. This flexibility can be used to include specific parameters for the API request or provide customized functionality.

## Examples

**Example 1: Simple Usage**

```python
async def example_simple():
    messages = [
        {"role": "user", "content": "Hello, how are you?"}
    ]
    async for chunk in FreeGpt.create_async_generator(model='gemini-1.5-pro', messages=messages):
        print(chunk, end="")

await example_simple()
```

**Example 2: Using a Proxy**

```python
async def example_proxy():
    messages = [
        {"role": "user", "content": "What is the meaning of life?"}
    ]
    async for chunk in FreeGpt.create_async_generator(model='gemini-1.5-pro', messages=messages, proxy='http://proxy.example.com:8080'):
        print(chunk, end="")

await example_proxy()
```

**Example 3: Setting a Timeout**

```python
async def example_timeout():
    messages = [
        {"role": "user", "content": "What is the capital of France?"}
    ]
    async for chunk in FreeGpt.create_async_generator(model='gemini-1.5-pro', messages=messages, timeout=60):
        print(chunk, end="")

await example_timeout()
```

These examples demonstrate basic usage scenarios for the `FreeGpt` class. You can adapt them to your specific needs, incorporating different prompts, messages, and configurations to suit your application.