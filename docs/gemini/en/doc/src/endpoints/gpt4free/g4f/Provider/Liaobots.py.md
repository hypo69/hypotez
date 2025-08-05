## Liaobots Provider

## Overview

This module implements the `Liaobots` class, an asynchronous generator provider for the `hypotez` project. It handles communication with the Liaobots API to interact with various AI models, such as Claude, DeepSeek, Gemini, GPT-4o, Grok, and o3.

## Details

The Liaobots provider is used to access and interact with AI models through the Liaobots API, enabling users to utilize various models for tasks like text generation, translation, summarization, and more. The module defines the `Liaobots` class, which extends the `AsyncGeneratorProvider` and `ProviderModelMixin` classes to provide a unified interface for working with different models.

## Classes

### `Liaobots`

**Description**: This class represents the Liaobots provider for interacting with the Liaobots API.

**Inherits**: 
- `AsyncGeneratorProvider`: Provides a basic interface for working with asynchronous generators.
- `ProviderModelMixin`: Offers functionalities for managing and handling model details.

**Attributes**:
- `url (str)`: Base URL of the Liaobots API.
- `working (bool)`: Indicates whether the provider is currently operational.
- `supports_message_history (bool)`: Specifies if the provider supports message history for context.
- `supports_system_message (bool)`: Indicates if the provider allows specifying system messages.
- `default_model (str)`: The default AI model to use.
- `models (list)`: A list of supported AI models.
- `model_aliases (dict)`: A dictionary mapping model aliases to their actual IDs.
- `_auth_code (str)`: Stores the authentication code for the API.
- `_cookie_jar (CookieJar)`: Handles cookie management for API requests.

**Methods**:
- `is_supported(model: str) -> bool`: Checks if the given AI model is supported.
- `create_async_generator(model: str, messages: Messages, proxy: str = None, connector: BaseConnector = None, **kwargs) -> AsyncResult`: Creates an asynchronous generator to interact with the specified model.
- `initialize_auth_code(session: ClientSession) -> None`: Initializes the authentication code by making login requests.
- `ensure_auth_code(session: ClientSession) -> None`: Ensures the authentication code is initialized and, if not, performs the initialization.

## Class Methods

### `is_supported`

```python
    @classmethod
    def is_supported(cls, model: str) -> bool:
        """
        Проверяет, поддерживается ли заданная модель.
        """
        return model in models or model in cls.model_aliases
```

**Purpose**: Checks if a given AI model is supported by the Liaobots provider.

**Parameters**:
- `model (str)`: The name of the AI model to check.

**Returns**:
- `bool`: `True` if the model is supported, `False` otherwise.

**How the Function Works**:
- The function checks if the provided model name exists in the `models` list or in the `model_aliases` dictionary.
- If the model name is found in either of these, it returns `True` indicating that the model is supported. Otherwise, it returns `False`.

**Examples**:
```python
>>> Liaobots.is_supported("gpt-4o")
True

>>> Liaobots.is_supported("claude-3.7-sonnet")
True

>>> Liaobots.is_supported("non-existent-model")
False
```

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        connector: BaseConnector = None,
        **kwargs
    ) -> AsyncResult:
        model = cls.get_model(model)
        
        headers = {
            "referer": "https://liaobots.work/",
            "origin": "https://liaobots.work",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        }
        async with ClientSession(
            headers=headers,
            cookie_jar=cls._cookie_jar,
            connector=get_connector(connector, proxy, True)
        ) as session:
            data = {
                "conversationId": str(uuid.uuid4()),
                "model": models[model],
                "messages": messages,
                "key": "",
                "prompt": kwargs.get("system_message", "You are a helpful assistant."),
            }
            if not cls._auth_code:
                async with session.post(
                    "https://liaobots.work/recaptcha/api/login",
                    data={"token": "abcdefghijklmnopqrst"},
                    verify_ssl=False
                ) as response:
                    await raise_for_status(response)
            try:
                async with session.post(
                    "https://liaobots.work/api/user",
                    json={"authcode": cls._auth_code},
                    verify_ssl=False
                ) as response:
                    await raise_for_status(response)
                    cls._auth_code = (await response.json(content_type=None))["authCode"]
                    if not cls._auth_code:
                        raise RuntimeError("Empty auth code")
                    cls._cookie_jar = session.cookie_jar
                async with session.post(
                    "https://liaobots.work/api/chat",
                    json=data,
                    headers={"x-auth-code": cls._auth_code},
                    verify_ssl=False
                ) as response:
                    await raise_for_status(response)
                    async for line in response.content:
                        if line.startswith(b"data: "):
                            yield json.loads(line[6:]).get("content")
            except:
                async with session.post(
                    "https://liaobots.work/api/user",
                    json={"authcode": "jGDRFOqHcZKAo"},
                    verify_ssl=False
                ) as response:
                    await raise_for_status(response)
                    cls._auth_code = (await response.json(content_type=None))["authCode"]
                    if not cls._auth_code:
                        raise RuntimeError("Empty auth code")
                    cls._cookie_jar = session.cookie_jar
                async with session.post(
                    "https://liaobots.work/api/chat",
                    json=data,
                    headers={"x-auth-code": cls._auth_code},
                    verify_ssl=False
                ) as response:
                    await raise_for_status(response)
                    async for line in response.content:
                        if line.startswith(b"data: "):
                            yield json.loads(line[6:]).get("content")
```

**Purpose**: Creates an asynchronous generator to interact with the specified AI model, sending messages and receiving responses.

**Parameters**:
- `model (str)`: The name of the AI model to interact with.
- `messages (Messages)`: A list of messages to send to the model.
- `proxy (str, optional)`: A proxy server to use for the request. Defaults to `None`.
- `connector (BaseConnector, optional)`: An `aiohttp` connector for network requests. Defaults to `None`.
- `**kwargs`: Additional keyword arguments to pass to the model.

**Returns**:
- `AsyncResult`: An asynchronous generator that yields responses from the AI model.

**How the Function Works**:
- The function first retrieves the actual model ID using the `get_model` method.
- It then sets up an `aiohttp` session with the necessary headers and cookie jar.
- If the `_auth_code` is not initialized, it performs a login request to obtain it.
- It then sends a POST request to the Liaobots API's chat endpoint with the message data, authentication code, and other relevant parameters.
- The function iterates over the response content, yielding the content of each line that starts with "data: " as a JSON object.

**Examples**:
```python
>>> async def send_message(model: str, messages: Messages):
...     async for response in Liaobots.create_async_generator(model, messages):
...         print(response)
... 
>>> await send_message("gpt-4o", [{"role": "user", "content": "Hello, how are you?"}])
Hello, I am an AI language model and do not have feelings. How can I assist you today?

```

### `initialize_auth_code`

```python
    @classmethod
    async def initialize_auth_code(cls, session: ClientSession) -> None:
        """
        Инициализирует код авторизации, выполняя необходимые запросы входа.
        """
        async with session.post(
            "https://liaobots.work/api/user",
            json={"authcode": "pTIQr4FTnVRfr"},
            verify_ssl=False
        ) as response:
            await raise_for_status(response)
            cls._auth_code = (await response.json(content_type=None))["authCode"]
            if not cls._auth_code:
                raise RuntimeError("Empty auth code")
            cls._cookie_jar = session.cookie_jar
```

**Purpose**: Initializes the authentication code required for interacting with the Liaobots API.

**Parameters**:
- `session (ClientSession)`: An `aiohttp` session object to use for the request.

**Returns**:
- `None`: The function does not return a value.

**How the Function Works**:
- It sends a POST request to the Liaobots API's user endpoint with a specific auth code.
- The response is checked for success using `raise_for_status`.
- If the request succeeds, the `_auth_code` attribute is set to the obtained auth code from the response's JSON data.
- If the auth code is empty, a `RuntimeError` is raised.
- The function also stores the session's cookie jar in the `_cookie_jar` attribute.

**Examples**:
- This function is typically called internally within the `ensure_auth_code` function, which is responsible for handling authentication.


### `ensure_auth_code`

```python
    @classmethod
    async def ensure_auth_code(cls, session: ClientSession) -> None:
        """
        Убеждается, что код авторизации инициализирован, а если нет, то выполняет инициализацию.
        """
        if not cls._auth_code:
            await cls.initialize_auth_code(session)
```

**Purpose**: Ensures that the authentication code for the Liaobots API is initialized.

**Parameters**:
- `session (ClientSession)`: An `aiohttp` session object to use for the request if the auth code needs to be initialized.

**Returns**:
- `None`: The function does not return a value.

**How the Function Works**:
- It checks if the `_auth_code` attribute is already set.
- If it's not set (indicating that the auth code hasn't been initialized), the function calls `initialize_auth_code` to obtain the auth code.

**Examples**:
- This function is used internally to ensure that the provider is properly authenticated before making requests to the Liaobots API.

## Parameter Details

- `model (str)`: The name of the AI model to interact with. This can be a supported model ID or a model alias.
- `messages (Messages)`: A list of messages to send to the AI model. Each message is a dictionary with "role" (e.g., "user," "assistant") and "content" fields.
- `proxy (str, optional)`: A proxy server to use for network requests. This is optional and defaults to `None`.
- `connector (BaseConnector, optional)`: An `aiohttp` connector for network requests. This is optional and defaults to `None`.
- `**kwargs`: Additional keyword arguments to pass to the model. This can include parameters specific to the model, such as "system_message" to provide instructions for the model.

## Examples

```python
>>> # Example: Using the default GPT-4o model
>>> async def send_message(messages: Messages):
...     async for response in Liaobots.create_async_generator("gpt-4o", messages):
...         print(response)
... 
>>> await send_message([{"role": "user", "content": "What is the capital of France?"}])
Paris

>>> # Example: Using the Claude-3.7-Sonnet model
>>> async def send_message_to_claude(messages: Messages):
...     async for response in Liaobots.create_async_generator("claude-3.7-sonnet", messages):
...         print(response)
... 
>>> await send_message_to_claude([{"role": "user", "content": "Write a short story about a cat."}])
The tabby cat, named Whiskers, was no ordinary feline. He possessed a peculiar knack for understanding human emotions, a secret he carefully guarded.  One sunny afternoon, he perched on the windowsill, watching a little girl named Lily play in the garden. Lily’s face was clouded with sadness, and Whiskers felt a surge of concern. He knew that something was troubling her. 
Whiskers, with his uncanny intuition, decided to do something about it. He gently hopped onto Lily’s lap and nuzzled her hand, his soft purr a soothing balm against her worries.  Lily, startled at first, couldn’t help but smile at the cat’s affection. She confided in Whiskers about her lost teddy bear, a cherished childhood companion. 

Whiskers, knowing he couldn’t speak human words, decided to act. He nudged Lily towards the garden, his tail swishing back and forth. Lily, confused but trusting, followed the cat’s lead.  As they walked, Whiskers led Lily to a pile of leaves behind a rose bush. Lily, with a gasp of joy, found her beloved teddy bear tucked beneath the leaves. 

Whiskers, proud of his accomplishment, rubbed against Lily’s leg, his purr a silent celebration of their shared moment of happiness.

>>> # Example: Using a custom system message with the Gemini model
>>> async def send_message_with_system(messages: Messages):
...     async for response in Liaobots.create_async_generator("gemini-2.0-flash", messages, system_message="You are a helpful assistant that is a professional programmer."):
...         print(response)
... 
>>> await send_message_with_system([{"role": "user", "content": "Write a Python function that takes a list of numbers and returns the sum of all even numbers."}])
```python
def sum_even_numbers(numbers: list[int]) -> int:
    """
    Calculates the sum of all even numbers in a given list.

    Args:
        numbers (list[int]): A list of numbers.

    Returns:
        int: The sum of all even numbers in the list.

    Examples:
        >>> sum_even_numbers([1, 2, 3, 4, 5])
        6
        >>> sum_even_numbers([1, 3, 5, 7, 9])
        0
    """
    sum = 0
    for number in numbers:
        if number % 2 == 0:
            sum += number
    return sum
```