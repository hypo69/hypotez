# Module `Aivvm.py`

## Overview

This module defines the `Aivvm` class, which is a provider for interacting with the Aivvm chat service.
It supports models such as `gpt-3.5-turbo` and `gpt-4`. The module facilitates the creation of chat completions using the Aivvm API.

## More details

The `Aivvm` class inherits from `AbstractProvider` and is responsible for sending requests to the Aivvm chat API.
It constructs the necessary headers and data for the API request, including the model, messages, and other parameters such as temperature.
The module handles both streaming and non-streaming responses from the API.

## Table of contents
- [Classes](#Classes)
  - [`Aivvm`](#Aivvm)
- [Functions](#Functions)
  - [`create_completion`](#create_completion)

## Classes

### `Aivvm`

**Description**: A class that implements an integration with the Aivvm chat service for generating text completions.
**Inherits**:
- `AbstractProvider`: Inherits the basic structure and methods for interacting with different providers.

**Attributes**:
- `url` (str): The base URL for the Aivvm chat service.
- `supports_stream` (bool): A flag indicating whether the provider supports streaming responses.
- `working` (bool): A flag indicating whether the provider is currently working.
- `supports_gpt_35_turbo` (bool): A flag indicating whether the provider supports `gpt-3.5-turbo` models.
- `supports_gpt_4` (bool): A flag indicating whether the provider supports `gpt-4` models.

**Working principle**:
The class defines static attributes related to the service's URL and the models it supports.
It primarily implements the `create_completion` method, which constructs a request to the Aivvm API and processes the response.
The method handles the construction of headers and data, sends the request, and yields the response in chunks, decoding the data appropriately.

## Class Methods

### `create_completion`

```python
@classmethod
def create_completion(cls,
        model: str,
        messages: Messages,
        stream: bool,
        **kwargs
    ) -> CreateResult:
    """
    Функция создает запрос на завершение текста к Aivvm API.

    Args:
        model (str): Идентификатор используемой модели. Например, "gpt-3.5-turbo".
        messages (Messages): Список сообщений для отправки в API.
        stream (bool): Флаг, указывающий, следует ли использовать потоковый режим.
        **kwargs: Дополнительные аргументы, такие как `system_message` и `temperature`.

    Returns:
        CreateResult: Итератор, выдающий текстовые фрагменты из ответа API.

    Raises:
        ValueError: Если указанная модель не поддерживается.
    """
```

**Parameters**:
- `model` (str): The ID of the model to use for completion. Examples: "gpt-3.5-turbo", "gpt-4".
- `messages` (Messages): A list of messages to send to the API.
- `stream` (bool): A flag indicating whether to use streaming mode.
- `**kwargs`: Additional keyword arguments, such as `system_message` and `temperature`.

**Raises**:
- `ValueError`: If the specified model is not supported.

**How the function works**:
1. **Model Selection**: If the `model` parameter is not provided, the function defaults to `"gpt-3.5-turbo"`. If the model is specified but not found in the `models` dictionary, a `ValueError` exception is raised.
2. **Data Preparation**: The function constructs a JSON payload (`json_data`) containing the model information, messages, API key (which is set to an empty string), a system message (with a default value), and a temperature setting.
3. **Header Creation**: The necessary HTTP headers are created, including content type, user agent, and referer. The content length is also calculated and added to the headers.
4. **API Request**: The function makes a POST request to the Aivvm chat API endpoint (`https://chat.aivvm.com/api/chat`) with the constructed headers and data.
5. **Response Handling**: The function iterates through the response content in chunks. It attempts to decode each chunk as UTF-8. If a `UnicodeDecodeError` occurs, it tries to decode the chunk using `unicode-escape`. The decoded chunks are then yielded.

**Examples**:
```python
# Пример использования create_completion
model = "gpt-3.5-turbo"
messages = [{"role": "user", "content": "Привет!"}]
stream = True
kwargs = {"system_message": "Ты - полезный ассистент.", "temperature": 0.7}

# Вызов функции (предполагается, что Aivvm инициализирован ранее)
# result = Aivvm.create_completion(model=model, messages=messages, stream=stream, **kwargs)
# for chunk in result:
#     print(chunk)
```

## Class Parameters

- `model` (str): Идентификатор модели, которую нужно использовать. Допустимые значения включают `"gpt-3.5-turbo"`, `"gpt-4"` и другие модели, определенные в словаре `models`.
- `messages` (Messages): Список сообщений, отправляемых в API. Каждое сообщение обычно представляет собой словарь с ключами `"role"` (например, `"user"` или `"assistant"`) и `"content"` (текст сообщения).
- `stream` (bool): Флаг, указывающий, следует ли использовать потоковый режим. Если `True`, функция будет выдавать фрагменты ответа по мере их поступления.
- `**kwargs`: Дополнительные аргументы, которые могут включать:
  - `"system_message"` (str): Системное сообщение, используемое для установки поведения языковой модели.
  - `"temperature"` (float): Параметр, контролирующий случайность генерируемого текста. Более высокие значения делают текст более случайным.