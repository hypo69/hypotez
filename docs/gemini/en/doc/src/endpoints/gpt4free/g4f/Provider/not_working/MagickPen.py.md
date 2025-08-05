# MagickPen Provider for GPT4Free

## Overview

This module provides the `MagickPen` class, which is a provider for the `gpt4free` module within the `hypotez` project. `MagickPen` enables communication with the MagickPen API to generate text using AI models.

## Details

The `MagickPen` class inherits from `AsyncGeneratorProvider` and `ProviderModelMixin`, which are base classes defining the core functionalities of a provider for the `gpt4free` module. This class facilitates communication with the MagickPen API using a specific endpoint for asking and receiving responses. It supports streaming responses, allowing for incremental output delivery.

The `MagickPen` class supports system messages, enabling context-specific instructions for the AI model, and message history, enabling the model to remember previous interactions.

## Classes

### `class MagickPen(AsyncGeneratorProvider, ProviderModelMixin)`

**Description**: This class provides a provider for the `gpt4free` module to interact with the MagickPen API, allowing for text generation using AI models.

**Inherits**:
  - `AsyncGeneratorProvider`: Provides an asynchronous generator interface for streaming responses.
  - `ProviderModelMixin`: Provides support for managing and selecting available models.

**Attributes**:
  - `url (str)`: The base URL of the MagickPen website.
  - `api_endpoint (str)`: The API endpoint URL used for asking and receiving responses.
  - `working (bool)`: Indicates whether the provider is currently working.
  - `supports_stream (bool)`: Indicates whether the provider supports streaming responses.
  - `supports_system_message (bool)`: Indicates whether the provider supports system messages.
  - `supports_message_history (bool)`: Indicates whether the provider supports message history.
  - `default_model (str)`: The default model to use if no model is specified.
  - `models (list)`: A list of supported models.

**Methods**:
  - `fetch_api_credentials()`: Retrieves API credentials (API secret, signature, timestamp, nonce, and secret) from a JavaScript file on the MagickPen website.
  - `create_async_generator()`: Creates an asynchronous generator that streams responses from the MagickPen API based on the given model, messages, and proxy settings.

## Class Methods

### `fetch_api_credentials()`

```python
    @classmethod
    async def fetch_api_credentials(cls) -> tuple:
        """
        Извлекает учетные данные API (API-секрет, подпись, временную метку, nonce и секрет) из файла JavaScript на веб-сайте MagickPen.

        Returns:
            tuple: Кортеж с учетными данными API.

        Raises:
            Exception: Если возникла ошибка при извлечении данных из файла JavaScript.
        """
        url = "https://magickpen.com/_nuxt/bf709a9ce19f14e18116.js"
        async with ClientSession() as session:
            async with session.get(url) as response:
                text = await response.text()

        pattern = r'"X-API-Secret":"(\w+)"'
        match = re.search(pattern, text)
        X_API_SECRET = match.group(1) if match else None

        timestamp = str(int(time.time() * 1000))
        nonce = str(random.random())

        s = ["TGDBU9zCgM", timestamp, nonce]
        s.sort()
        signature_string = ''.join(s)
        signature = hashlib.md5(signature_string.encode()).hexdigest()

        pattern = r'secret:"(\w+)"'
        match = re.search(pattern, text)
        secret = match.group(1) if match else None

        if X_API_SECRET and timestamp and nonce and secret:
            return X_API_SECRET, signature, timestamp, nonce, secret
        else:
            raise Exception("Unable to extract all the necessary data from the JavaScript file.")
```

**Purpose**: This method retrieves API credentials from the MagickPen website's JavaScript file.

**How the Method Works**:

1. It sends a GET request to the specified JavaScript file URL (`https://magickpen.com/_nuxt/bf709a9ce19f14e18116.js`).
2. The method retrieves the text content of the file.
3. It extracts the `X-API-Secret` value using a regular expression pattern.
4. The method generates a timestamp and a random nonce.
5. It calculates the `signature` based on the `TGDBU9zCgM` string, timestamp, and nonce using MD5 hashing.
6. It extracts the `secret` value using a regular expression pattern.
7. If all the necessary values are retrieved successfully, the method returns them as a tuple.
8. If any values are missing, it raises an exception indicating that the required data could not be extracted from the JavaScript file.

**Examples**:

```python
>>> from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.MagickPen import MagickPen
>>> MagickPen.fetch_api_credentials()
('your_x_api_secret', 'your_signature', 'your_timestamp', 'your_nonce', 'your_secret')
```

### `create_async_generator()`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор, который передает ответы из API MagickPen на основе указанной модели, сообщений и настроек прокси.

        Args:
            model (str): Имя модели.
            messages (Messages): Список сообщений для отправки в API.
            proxy (str, optional): Прокси-сервер для использования при отправке запросов. По умолчанию None.

        Returns:
            AsyncResult: Асинхронный результат, который содержит генератор для потоковой передачи ответов.

        Raises:
            Exception: Если возникла ошибка при обработке запроса к API MagickPen.
        """
        model = cls.get_model(model)
        X_API_SECRET, signature, timestamp, nonce, secret = await cls.fetch_api_credentials()

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'nonce': nonce,
            'origin': cls.url,
            'referer': f"{cls.url}/",
            'secret': secret,
            'signature': signature,
            'timestamp': timestamp,
            'x-api-secret': X_API_SECRET,
        }

        async with ClientSession(headers=headers) as session:
            prompt = format_prompt(messages)
            payload = {
                'query': prompt,
                'turnstileResponse': '',
                'action': 'verify'
            }
            async with session.post(cls.api_endpoint, json=payload, proxy=proxy) as response:
                response.raise_for_status()
                async for chunk in response.content:
                    if chunk:
                        yield chunk.decode()
```

**Purpose**: This method creates an asynchronous generator that streams responses from the MagickPen API.

**How the Method Works**:

1. It retrieves the `model` from the available models.
2. It retrieves the API credentials from the `fetch_api_credentials()` method.
3. It constructs the request headers, including API credentials, content type, and other necessary headers.
4. It formats the prompt based on the provided `messages`.
5. It constructs the payload for the POST request, including the prompt, an empty `turnstileResponse` (presumably for CAPTCHA handling), and the `action` set to `verify`.
6. It sends a POST request to the API endpoint (`https://api.magickpen.com/ask`) with the payload and configured headers.
7. It checks the response status and raises an exception if there's an error.
8. It iterates through the response content chunks, decoding them and yielding them to the generator.

**Examples**:

```python
>>> from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.MagickPen import MagickPen
>>> from hypotez.src.endpoints.gpt4free.g4f.typing import Messages
>>> messages = Messages([{'role': 'user', 'content': 'Hello, world!'}]
>>> async_generator = await MagickPen.create_async_generator(model='gpt-4o-mini', messages=messages)
>>> async for chunk in async_generator:
...     print(chunk)
...
Hello, world!
```

## Parameter Details

- `model (str)`: The name of the AI model to use for text generation.
- `messages (Messages)`: A list of messages to send to the API. Each message should be a dictionary with `role` (e.g., `user`, `assistant`) and `content` keys.
- `proxy (str, optional)`: A proxy server to use when sending requests. Defaults to `None`.

## Examples

```python
>>> from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.MagickPen import MagickPen
>>> from hypotez.src.endpoints.gpt4free.g4f.typing import Messages
>>> messages = Messages([{'role': 'user', 'content': 'What is the capital of France?'}])
>>> async_generator = await MagickPen.create_async_generator(model='gpt-4o-mini', messages=messages)
>>> async for chunk in async_generator:
...     print(chunk)
...
Paris
```

```python
>>> from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.MagickPen import MagickPen
>>> from hypotez.src.endpoints.gpt4free.g4f.typing import Messages
>>> messages = Messages([
...     {'role': 'system', 'content': 'You are a helpful and informative chatbot.'},
...     {'role': 'user', 'content': 'Write a short story about a cat who travels the world.'},
... ])
>>> async_generator = await MagickPen.create_async_generator(model='gpt-4o-mini', messages=messages)
>>> async for chunk in async_generator:
...     print(chunk)
...
Once upon a time, there was a cat named Whiskers who had a wanderlust. He wasn't content with just lounging around the house, catching mice, and napping in sunbeams. He longed for adventure, for new sights and smells, for the thrill of the unknown.