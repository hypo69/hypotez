# Chatgpt4Online Provider

## Overview

This module provides the `Chatgpt4Online` class, which implements an asynchronous generator for interacting with the ChatGPT4Online API. It allows for streaming responses from the API and handling requests with different models and messages.

## Details

The `Chatgpt4Online` class inherits from the `AsyncGeneratorProvider` base class and leverages the `aiohttp` library for asynchronous HTTP requests. This provider targets the ChatGPT4Online API, which offers access to various GPT models, including the popular GPT-4. The `create_async_generator` method facilitates the generation of asynchronous responses from the API based on provided messages and model selections.

## Classes

### `Chatgpt4Online`

**Description**: An asynchronous generator provider class for interacting with the ChatGPT4Online API.

**Inherits**: `AsyncGeneratorProvider`

**Attributes**:
- `url` (str): The base URL of the ChatGPT4Online API.
- `api_endpoint` (str): The specific API endpoint for submitting chat requests.
- `working` (bool): Indicates whether the provider is currently functional.
- `default_model` (str): The default GPT model used by the provider.
- `models` (list): A list of supported GPT models.

**Methods**:
- `get_nonce(headers: dict) -> str`: Asynchronously retrieves a nonce (a random, unpredictable value) from the API for security purposes.
- `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`: Creates an asynchronous generator that yields responses from the API based on the provided model, messages, and optional proxy configuration.


## Class Methods

### `get_nonce(headers: dict) -> str`

```python
    async def get_nonce(headers: dict) -> str:
        """
        Асинхронно извлекает nonce (случайное, непредсказуемое значение) из API для целей безопасности.

        Args:
            headers (dict): Заголовки HTTP-запроса.

        Returns:
            str: Значение nonce, извлеченное из ответа API.

        Raises:
            Exception: В случае ошибки при получении nonce.

        Example:
            >>> headers = {"accept": "text/event-stream", ...}
            >>> nonce = await Chatgpt4Online.get_nonce(headers)
            >>> print(nonce)
            '1234567890' # example nonce value
        """
        async with ClientSession(headers=headers) as session:
            async with session.post(f"https://chatgpt4online.org/wp-json/mwai/v1/start_session") as response:
                return (await response.json())["restNonce"]
```

### `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`

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
        Создает асинхронный генератор, который генерирует ответы из API на основе предоставленной модели, сообщений и
        необязательной конфигурации прокси.

        Args:
            model (str): Имя модели GPT (например, 'gpt-4').
            messages (Messages): Список сообщений для отправки в API.
            proxy (str, optional): URL-адрес прокси-сервера. По умолчанию `None`.
            **kwargs: Дополнительные ключевые аргументы, передаваемые в API.

        Returns:
            AsyncResult: Асинхронный результат, который можно использовать для получения ответов из API.

        Raises:
            Exception: В случае ошибки при отправке запроса или получении ответа.

        Example:
            >>> messages = [{"role": "user", "content": "Hello, world!"}, ...]
            >>> async_generator = await Chatgpt4Online.create_async_generator(model='gpt-4', messages=messages)
            >>> async for response in async_generator:
            ...     print(response)
            'Hello, world!'
        """
        headers = {
            "accept": "text/event-stream",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "dnt": "1",
            "origin": cls.url,
            "priority": "u=1, i",
            "referer": f"{cls.url}/",
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        }
        headers['x-wp-nonce'] = await cls.get_nonce(headers)
        async with ClientSession(headers=headers) as session:
            prompt = format_prompt(messages)
            data = {
                "botId": "default",
                "newMessage": prompt,
                "stream": True,
            }

            async with session.post(f"{cls.url}{cls.api_endpoint}", json=data, proxy=proxy) as response:
                response.raise_for_status()
                full_response = ""

                async for chunk in response.content.iter_any():
                    if chunk:
                        try:
                            # Extract the JSON object from the chunk
                            for line in chunk.decode().splitlines():
                                if line.startswith("data: "):
                                    json_data = json.loads(line[6:])
                                    if json_data["type"] == "live":
                                        full_response += json_data["data"]
                                    elif json_data["type"] == "end":
                                        final_data = json.loads(json_data["data"])
                                        full_response = final_data["reply"]
                                        break
                        except json.JSONDecodeError:
                            continue

                yield full_response
```

## Parameter Details

- `model` (str): The name of the GPT model to be used for the chat request. The `Chatgpt4Online` provider supports `gpt-4` as its `default_model`.
- `messages` (Messages): A list of messages representing the chat conversation. Each message should be a dictionary containing `role` (e.g., `user`, `assistant`) and `content`.
- `proxy` (str, optional): URL of a proxy server. If provided, the API request will be sent through this proxy.
- `**kwargs`: Additional keyword arguments that can be passed to the API.

## Examples

```python
# Example usage:
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.Chatgpt4Online import Chatgpt4Online

messages = [
    {"role": "user", "content": "Hello, how are you?"},
    {"role": "assistant", "content": "I am doing well. How about you?"},
]

async def main():
    async_generator = await Chatgpt4Online.create_async_generator(model='gpt-4', messages=messages)
    async for response in async_generator:
        print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```