# Vitalentum Provider

## Overview

This module provides a class `Vitalentum` that implements the `AsyncGeneratorProvider` interface for interacting with the Vitalentum API to access GPT-3.5 Turbo models. 

## Details

The `Vitalentum` class leverages the `aiohttp` library for asynchronous HTTP communication with the Vitalentum API. It supports the GPT-3.5 Turbo model and allows for asynchronous generation of text responses based on provided messages. 

## Classes

### `class Vitalentum(AsyncGeneratorProvider)`

**Description**: This class implements the `AsyncGeneratorProvider` interface, providing methods for asynchronous interactions with the Vitalentum API to access the GPT-3.5 Turbo model.

**Inherits**: `AsyncGeneratorProvider`

**Attributes**:
- `url` (str): The base URL of the Vitalentum API.
- `supports_gpt_35_turbo` (bool): Indicates if the provider supports GPT-3.5 Turbo.

**Methods**:

- `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`: This method creates an asynchronous generator for processing messages and generating text responses from the GPT-3.5 Turbo model.

## Class Methods

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
        Создает асинхронный генератор для обработки сообщений и генерации текстовых ответов от модели GPT-3.5 Turbo.

        Args:
            model (str): Имя модели.
            messages (Messages): Список сообщений в контексте разговора.
            proxy (str, optional): Прокси-сервер для использования. Defaults to None.
            **kwargs: Дополнительные параметры для отправки в API Vitalentum.

        Returns:
            AsyncResult: Асинхронный результат, который может быть использован для получения результатов генерации.

        Raises:
            Exception: Если возникает ошибка при запросе к API Vitalentum.

        Example:
            >>> messages = [
            ...    {"role": "user", "content": "Hello, how are you?"},
            ...    {"role": "assistant", "content": "I am doing well, thank you. How can I help you?"},
            ... ]
            >>> async_generator = await Vitalentum.create_async_generator(
            ...     model="gpt-3.5-turbo", messages=messages
            ... )
            >>> async for response in async_generator:
            ...     print(response)
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
            "Accept": "text/event-stream",
            "Accept-language": "de,en-US;q=0.7,en;q=0.3",
            "Origin": cls.url,
            "Referer": f"{cls.url}/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
        }
        conversation = json.dumps({"history": [
            {
                "speaker": "human" if message["role"] == "user" else "bot",
                "text": message["content"],
            } for message in messages
        ]})
        data = {
            "conversation": conversation,
            "temperature": 0.7,
            **kwargs
        }
        async with ClientSession(
                headers=headers
            ) as session:
            async with session.post(f"{cls.url}/api/converse-edge", json=data, proxy=proxy) as response:
                response.raise_for_status()
                async for line in response.content:
                    line = line.decode()
                    if line.startswith("data: "):
                        if line.startswith("data: [DONE]"):
                            break
                        line = json.loads(line[6:-1])
                        content = line["choices"][0]["delta"].get("content")

                        if content:
                            yield content
```

**Purpose**: This method creates an asynchronous generator for processing messages and generating text responses from the GPT-3.5 Turbo model.

**Parameters**:
- `model` (str): The name of the model.
- `messages` (Messages): A list of messages in the conversation context.
- `proxy` (str, optional): A proxy server to use. Defaults to `None`.
- `**kwargs`: Additional parameters for sending to the Vitalentum API.

**Returns**:
- `AsyncResult`: An asynchronous result that can be used to obtain generation results.

**Raises Exceptions**:
- `Exception`: If an error occurs during the request to the Vitalentum API.

**How the Function Works**:
- The function begins by defining headers for the HTTP request, including user agent, accept, accept-language, origin, referer, and security-related headers.
- It constructs the conversation JSON data based on the provided messages, including speaker (human or bot) and the content of each message.
- It prepares the data for the API request, including the conversation data, temperature, and any additional keyword arguments passed to the function.
- The function then uses the `ClientSession` and `session.post` methods to perform a POST request to the Vitalentum API endpoint `/api/converse-edge`, passing the JSON data and the optional proxy.
- The response is checked for errors using `response.raise_for_status()`.
- The function iterates over the response content line by line, decoding each line and processing the data if it starts with `data:`.
- The `[DONE]` message is used as a signal to stop the generator.
- For each valid data line, the function extracts the `content` from the response JSON, and if it is not empty, yields it to the caller.

**Examples**:
```python
>>> messages = [
...    {"role": "user", "content": "Hello, how are you?"},
...    {"role": "assistant", "content": "I am doing well, thank you. How can I help you?"},
... ]
>>> async_generator = await Vitalentum.create_async_generator(
...     model="gpt-3.5-turbo", messages=messages
... )
>>> async for response in async_generator:
...     print(response)
```

## Parameter Details

- `model` (str): The name of the GPT-3.5 Turbo model.
- `messages` (Messages): A list of messages in the conversation context, each message being a dictionary with `role` (user or assistant) and `content` keys.
- `proxy` (str, optional): A proxy server address to use for the API request.

## Examples

```python
>>> messages = [
...    {"role": "user", "content": "Hello, how are you?"},
...    {"role": "assistant", "content": "I am doing well, thank you. How can I help you?"},
... ]
>>> async_generator = await Vitalentum.create_async_generator(
...     model="gpt-3.5-turbo", messages=messages
... )
>>> async for response in async_generator:
...     print(response)