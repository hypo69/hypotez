# Module for working with the Qwen Qwen-2-72B model
## Overview

The module contains the class `Qwen_Qwen_2_72B`, which is used to interact with the Qwen Qwen-2-72B model through the Hugging Face Space API.
The module supports asynchronous generation of text using message streaming.

## More details

This module enables interaction with the Qwen Qwen-2-72B model, providing functionalities such as text generation, support for system messages, and message history management. It makes use of asynchronous requests to handle the streaming of generated text efficiently.
The class `Qwen_Qwen_2_72B` defines the necessary methods to communicate with the Hugging Face Space API, format prompts, and process responses.

## Table of contents

- [Classes](#classes)
    - [`Qwen_Qwen_2_72B`](#Qwen_Qwen_2_72B)
        - [Methods](#methods)
            - [`create_async_generator`](#create_async_generator)

## Classes

### `Qwen_Qwen_2_72B`

**Description**: Class for interacting with the Qwen Qwen-2-72B model.

**Inherits**:

- `AsyncGeneratorProvider`: Provides asynchronous generation capabilities.
- `ProviderModelMixin`: Provides model-related utility functions.

**Attributes**:

- `label` (str): Label identifying the provider ("Qwen Qwen-2.72B").
- `url` (str): URL of the Hugging Face Space API ("https://qwen-qwen2-72b-instruct.hf.space").
- `api_endpoint` (str): API endpoint for joining the queue ("https://qwen-qwen2-72b-instruct.hf.space/queue/join?").
- `working` (bool): Indicates whether the provider is working (True).
- `supports_stream` (bool): Indicates whether streaming is supported (True).
- `supports_system_message` (bool): Indicates whether system messages are supported (True).
- `supports_message_history` (bool): Indicates whether message history is supported (False).
- `default_model` (str): The default model name ("qwen-qwen2-72b-instruct").
- `model_aliases` (dict): Aliases for the model ({"qwen-2-72b": default_model}).
- `models` (list): List of supported models (keys from `model_aliases`).

**Working principle**:

The `Qwen_Qwen_2_72B` class is designed to facilitate communication with the Qwen Qwen-2-72B model hosted on Hugging Face Spaces. It initializes several key attributes such as the API endpoint, supported features, and model configurations. The `create_async_generator` method is crucial for generating text asynchronously.
It constructs the necessary headers and payloads for sending requests to the API, manages the session using a unique hash, and processes the streaming response to yield text fragments.

### Methods

#### `create_async_generator`

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
    Asynchronously generates text using the Qwen Qwen-2-72B model.

    Args:
        model (str): Model name.
        messages (Messages): List of messages for the prompt.
        proxy (str, optional): Proxy URL. Defaults to None.
        **kwargs: Additional keyword arguments.

    Returns:
        AsyncResult: An asynchronous generator yielding text fragments.

    Raises:
        aiohttp.ClientError: If there is an issue with the HTTP request.
        json.JSONDecodeError: If there is an issue decoding the JSON response.

    """
    def generate_session_hash() -> str:
        """Генерирует уникальный хэш сессии."""
        return str(uuid.uuid4()).replace('-', '')[:12]

    # Генерация уникального хэша сессии
    session_hash = generate_session_hash()

    headers_join = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'origin': f'{cls.url}',
        'referer': f'{cls.url}/',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }

    # Подготовка запроса
    system_prompt = "\n".join([message["content"] for message in messages if message["role"] == "system"])
    messages = [message for message in messages if message["role"] != "system"]
    prompt = format_prompt(messages)

    payload_join = {
        "data": [prompt, [], system_prompt],
        "event_data": None,
        "fn_index": 0,
        "trigger_id": 11,
        "session_hash": session_hash
    }

    async with aiohttp.ClientSession() as session:
        # Отправка запроса на подключение
        async with session.post(cls.api_endpoint, headers=headers_join, json=payload_join) as response:
            event_id = (await response.json())['event_id']

        # Подготовка запроса потока данных
        url_data = f'{cls.url}/queue/data'

        headers_data = {
            'accept': 'text/event-stream',
            'accept-language': 'en-US,en;q=0.9',
            'referer': f'{cls.url}/',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        }

        params_data = {
            'session_hash': session_hash
        }

        # Отправка запроса потока данных
        async with session.get(url_data, headers=headers_data, params=params_data) as response:
            full_response = ""
            final_full_response = ""
            async for line in response.content:
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith('data: '):
                    try:
                        json_data = json.loads(decoded_line[6:])

                        # Поиск стадий генерации
                        if json_data.get('msg') == 'process_generating':
                            if 'output' in json_data and 'data' in json_data['output']:
                                output_data = json_data['output']['data']
                                if len(output_data) > 1 and len(output_data[1]) > 0:
                                    for item in output_data[1]:
                                        if isinstance(item, list) and len(item) > 1:
                                            fragment = str(item[1])
                                            # Игнорирование фрагментов типа [0, 1] и дубликатов
                                            if not re.match(r'^\\[.*\\]$', fragment) and not full_response.endswith(fragment):
                                                full_response += fragment
                                                yield fragment

                        # Проверка на завершение
                        if json_data.get('msg') == 'process_completed':
                            # Финальная проверка для обеспечения получения полного ответа
                            if 'output' in json_data and 'data' in json_data['output']:
                                output_data = json_data['output']['data']
                                if len(output_data) > 1 and len(output_data[1]) > 0:
                                    final_full_response = output_data[1][0][1]

                                    # Очистка финального ответа
                                    if final_full_response.startswith(full_response):
                                        final_full_response = final_full_response[len(full_response):]

                                    # Возвращение оставшейся части финального ответа
                                    if final_full_response:
                                        yield final_full_response
                                break

                    except json.JSONDecodeError as ex:
                        debug.log("Could not parse JSON:", decoded_line)

```

**Purpose**: Asynchronously generates text using the Qwen Qwen-2-72B model.

**Parameters**:

- `cls`: The class itself.
- `model` (str): Model name.
- `messages` (Messages): List of messages for the prompt.
- `proxy` (str, optional): Proxy URL. Defaults to None.
- `**kwargs`: Additional keyword arguments.

**Returns**:

- `AsyncResult`: An asynchronous generator yielding text fragments.

**Raises**:

- `aiohttp.ClientError`: If there is an issue with the HTTP request.
- `json.JSONDecodeError`: If there is an issue decoding the JSON response.

**Internal functions**:

- `generate_session_hash`: Generates a unique session hash.

**How the function works**:

1.  The function `create_async_generator` generates a unique session hash using the internal function `generate_session_hash`.
2.  It then prepares the headers and payload for the API request.
3.  The function separates system messages from user messages and formats the prompt.
4.  An asynchronous HTTP session is initiated to send a POST request to the API endpoint to join the queue.
5.  The `event_id` is extracted from the response.
6.  Another set of headers and parameters are prepared for the data stream request.
7.  A GET request is sent to the data stream URL, and the response is processed line by line.
8.  The function checks for generation stages and completion messages in the JSON data.
9.  As text fragments are generated, they are yielded to the caller, ensuring no duplicates are sent.
10. The remaining part of the final response is also yielded after cleanup.
11. Any JSON decoding errors are caught and logged for debugging.

**Examples**:

```python
# Example usage (not executable, requires setup)
# model_name = "qwen-2-72b"
# messages = [{"role": "user", "content": "Write a short story."}]
# async for fragment in Qwen_Qwen_2_72B.create_async_generator(model=model_name, messages=messages):
#     print(fragment, end="")
```