# PerplexityLabs Provider for GPT4Free

## Overview

This module provides a `PerplexityLabs` class, which implements an asynchronous generator for interacting with the Perplexity Labs AI model via GPT4Free. 

## Details

The `PerplexityLabs` class is responsible for sending requests to the Perplexity Labs API and generating responses. It utilizes WebSockets for communication and offers support for multiple Perplexity Labs models.

## Classes

### `PerplexityLabs`

**Description**: This class provides an asynchronous generator for interacting with Perplexity Labs AI models.

**Inherits**: 
    - `AsyncGeneratorProvider`: This class inherits from `AsyncGeneratorProvider`, which implements the asynchronous generator functionality.
    - `ProviderModelMixin`: This class inherits from `ProviderModelMixin`, which provides model-specific logic and configuration.

**Attributes**:

    - `url` (str): The base URL for the Perplexity Labs API.
    - `working` (bool): A flag indicating whether the provider is currently functional.
    - `default_model` (str): The default model name used by the provider.
    - `models` (list): A list of supported model names.

**Methods**:

    - `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`: This method creates and returns an asynchronous generator for a specific model.

**Principle of Operation**:

1. **Initialization**: The class initializes attributes like the base URL, default model, and supported model names.
2. **Creating an Asynchronous Generator**: The `create_async_generator` method is responsible for creating the asynchronous generator instance.
3. **Establishing Connection**: The method establishes a WebSocket connection with the Perplexity Labs API.
4. **Sending Requests**: It sends the user's messages to the API and receives responses from the model.
5. **Generating Responses**: The generator yields the model's responses one by one as they are received.
6. **Handling Errors**: The method handles potential errors during communication and raises appropriate exceptions.

## Methods

### `create_async_generator`

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
        Создает асинхронный генератор для заданной модели Perplexity Labs.

        Args:
            model (str): Имя модели.
            messages (Messages): Список сообщений, которые необходимо отправить модели.
            proxy (str, optional): Прокси-сервер, который нужно использовать. По умолчанию None.
            **kwargs: Дополнительные аргументы.

        Returns:
            AsyncResult: Асинхронный результат.
        """
        headers = {
            "Origin": cls.url,
            "Referer": f"{cls.url}/",
        }
        async with StreamSession(headers=headers, proxy=proxy, impersonate="chrome") as session:
            t = format(random.getrandbits(32), "08x")
            async with session.get(
                f"{API_URL}?EIO=4&transport=polling&t={t}"
            ) as response:
                await raise_for_status(response)
                text = await response.text()
            assert text.startswith("0")
            sid = json.loads(text[1:])["sid"]
            post_data = '40{"jwt":"anonymous-ask-user"}\'
            async with session.post(
                f"{API_URL}?EIO=4&transport=polling&t={t}&sid={sid}",
                data=post_data
            ) as response:
                await raise_for_status(response)
                assert await response.text() == "OK"
            async with session.get(
                f"{API_URL}?EIO=4&transport=polling&t={t}&sid={sid}",
                data=post_data
            ) as response:
                await raise_for_status(response)
                assert (await response.text()).startswith("40")
            async with session.ws_connect(f"{WS_URL}?EIO=4&transport=websocket&sid={sid}", autoping=False) as ws:
                await ws.send_str("2probe")
                assert(await ws.receive_str() == "3probe")
                await ws.send_str("5")
                assert(await ws.receive_str() == "6")
                message_data = {
                    "version": "2.18",
                    "source": "default",
                    "model": model,
                    "messages": [message for message in messages if isinstance(message["content"], str)],
                }
                await ws.send_str("42" + json.dumps(["perplexity_labs", message_data]))
                last_message = 0
                while True:
                    message = await ws.receive_str()
                    if message == "2":
                        if last_message == 0:
                            raise RuntimeError("Unknown error")
                        await ws.send_str("3")
                        continue
                    try:
                        if last_message == 0 and model == cls.default_model:
                            yield "<think>"
                        data = json.loads(message[2:])[1]
                        yield data["output"][last_message:]
                        last_message = len(data["output"])
                        if data["final"]:
                            if data["citations"]:
                                yield Sources(data["citations"])
                            yield FinishReason("stop")
                            break
                    except Exception as e:
                        raise ResponseError(f"Message: {message}") from e
```

**Purpose**: This method establishes a connection to the Perplexity Labs WebSocket API, sends user messages, and receives responses from the model.

**Parameters**:
    - `model` (str): The name of the Perplexity Labs model to be used.
    - `messages` (Messages): A list of messages to be sent to the model.
    - `proxy` (str, optional): A proxy server to be used for the connection. Defaults to None.
    - `**kwargs`: Additional arguments.

**Returns**:
    - `AsyncResult`: An asynchronous result object that represents the ongoing communication with the model.

**How the Function Works**:

1. **Setup**: The method sets up headers and a `StreamSession` object for handling the connection.
2. **WebSocket Connection**: It establishes a WebSocket connection with the Perplexity Labs API.
3. **Sending Messages**: The method sends the user's messages to the API in a specific format.
4. **Receiving Responses**: It waits for responses from the model, parsing them and yielding them to the asynchronous generator.
5. **Finalizing the Session**: Once the model signals the end of the conversation, the method closes the WebSocket connection and signals the end of the asynchronous generator.

**Examples**:

```python
async def example():
    messages = [{"role": "user", "content": "What is the meaning of life?"}]
    async for response in PerplexityLabs.create_async_generator(model="r1-1776", messages=messages):
        print(response)
```

**Inner Functions**:
    - **None**

## Parameter Details

- `model` (str): Specifies the Perplexity Labs model to be used for generating responses.
- `messages` (Messages): A list of messages to be sent to the model.
- `proxy` (str, optional): An optional proxy server to be used for the connection. Defaults to None.
- `**kwargs`: Additional arguments that can be used for customizing the request.

## Examples

```python
async def example():
    messages = [{"role": "user", "content": "What is the meaning of life?"}]
    async for response in PerplexityLabs.create_async_generator(model="r1-1776", messages=messages):
        print(response)
```
```markdown