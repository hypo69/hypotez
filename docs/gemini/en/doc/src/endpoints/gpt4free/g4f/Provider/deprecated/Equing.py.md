# Equing Provider for GPT-4Free

## Overview

This module defines the `Equing` class, a provider for GPT-4Free that utilizes the `https://next.eqing.tech/` API. 

## Details

The `Equing` class inherits from the `AbstractProvider` base class and provides a concrete implementation for generating completions using the Equing API. It supports streaming responses and allows you to configure various parameters like temperature, presence penalty, frequency penalty, and top_p.

## Classes

### `class Equing`

**Description**: The Equing class implements a provider for GPT-4Free using the `https://next.eqing.tech/` API.

**Inherits**: `AbstractProvider`

**Attributes**:

- `url` (str): The base URL of the Equing API.
- `working` (bool): Flag indicating if the provider is currently working.
- `supports_stream` (bool): True, as the provider supports streaming responses.
- `supports_gpt_35_turbo` (bool): True, as the provider supports the gpt-3.5-turbo model.
- `supports_gpt_4` (bool): False, as the provider does not support the gpt-4 model.

**Methods**:

- `create_completion(model: str, messages: list[dict[str, str]], stream: bool, **kwargs: Any) -> CreateResult`: Generates a completion response using the Equing API. 

## Class Methods

### `create_completion`

```python
    @staticmethod
    @abstractmethod
    def create_completion(
        model: str,
        messages: list[dict[str, str]],
        stream: bool, **kwargs: Any) -> CreateResult:
        """ Функция генерирует ответ от Equing API.
        Args:
            model (str): Имя модели (например, "gpt-3.5-turbo").
            messages (list[dict[str, str]]): Список сообщений для передачи модели.
            stream (bool): Флаг, указывающий на то, следует ли использовать потоковую передачу.
            **kwargs (Any): Дополнительные аргументы для настройки модели.

        Returns:
            CreateResult: Результат создания текста, который может быть строкой, потоком или None.

        Raises:
            Exception: В случае ошибки при получении ответа от API.

        Example:
            >>> from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated import Equing
            >>> from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.base_provider import AbstractProvider
            >>> provider = Equing()
            >>> messages = [
            ...     {"role": "user", "content": "Привет, как дела?"},
            ... ]
            >>> response = provider.create_completion(model="gpt-3.5-turbo", messages=messages, stream=False)
            >>> print(response)
            Хорошо, спасибо! А как у тебя дела?
        """
```

**Purpose**: This method is responsible for generating a completion response using the Equing API.

**Parameters**:

- `model` (str): The name of the model to use for generation (e.g., "gpt-3.5-turbo").
- `messages` (list[dict[str, str]]): A list of messages to be passed to the model.
- `stream` (bool): A flag indicating whether to use streaming or not.
- `**kwargs` (Any): Additional arguments for configuring the model.

**Returns**:

- `CreateResult`: The result of the completion, which can be a string, a stream, or None.

**Raises Exceptions**:

- `Exception`: In case of errors while retrieving a response from the API.

**How the Function Works**:

1. Sets up the request headers with necessary information for interacting with the Equing API.
2. Prepares JSON data for the request, including messages, model name, and additional parameters like temperature, presence penalty, frequency penalty, and top_p.
3. Sends a POST request to the Equing API endpoint (`https://next.eqing.tech/api/openai/v1/chat/completions`) with the prepared JSON data.
4. If streaming is not enabled, retrieves the response as JSON and returns the generated content.
5. If streaming is enabled, iterates through the response content, processing each chunk and yielding the generated tokens as a stream.

**Examples**:

```python
>>> from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated import Equing
>>> from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.base_provider import AbstractProvider
>>> provider = Equing()
>>> messages = [
...     {"role": "user", "content": "Привет, как дела?"},
... ]
>>> response = provider.create_completion(model="gpt-3.5-turbo", messages=messages, stream=False)
>>> print(response)
Хорошо, спасибо! А как у тебя дела?
```
```markdown