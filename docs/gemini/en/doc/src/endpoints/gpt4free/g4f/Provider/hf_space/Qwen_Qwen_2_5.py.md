# Provider for Qwen Qwen-2.5 (HF Space)

## Overview

This module provides an asynchronous generator provider for the Qwen Qwen-2.5 model hosted on Hugging Face Spaces. It allows you to interact with the model using a simple, asynchronous interface, enabling you to generate text with streaming capabilities.

## Details

The `Qwen_Qwen_2_5` class inherits from `AsyncGeneratorProvider` and `ProviderModelMixin`, providing a unified interface for interacting with various language models. It supports streaming, system messages, and multiple model aliases. The module uses an asynchronous generator to stream responses from the model, improving efficiency and memory management.

## Classes

### `Qwen_Qwen_2_5`

**Description:** This class implements a provider for the Qwen Qwen-2.5 model hosted on Hugging Face Spaces, enabling asynchronous generation of text with streaming capabilities.

**Inherits:** `AsyncGeneratorProvider`, `ProviderModelMixin`

**Attributes:**

- `label`: String representing the name of the provider.
- `url`: Base URL of the Hugging Face Spaces deployment.
- `api_endpoint`: Endpoint for joining the queue and receiving responses.
- `working`: Boolean indicating if the provider is currently operational.
- `supports_stream`: Boolean indicating if the provider supports streaming responses.
- `supports_system_message`: Boolean indicating if the provider supports system messages.
- `supports_message_history`: Boolean indicating if the provider supports message history.
- `default_model`: Default model name used by the provider.
- `model_aliases`: Dictionary mapping alternative model names to the default model.
- `models`: List of supported model names.

**Methods:**

- `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult:`
    - This method creates an asynchronous generator to stream text from the Qwen Qwen-2.5 model.

## Class Methods

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
        """ Создает асинхронный генератор для потоковой передачи текста из модели Qwen Qwen-2.5.

        Args:
            model (str): Имя модели.
            messages (Messages): Список сообщений для модели.
            proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.

        Returns:
            AsyncResult: Результат асинхронной операции.

        Raises:
            Exception: Если возникает ошибка во время операции.
        """
        ...
```

**Purpose:** Creates an asynchronous generator to stream text from the Qwen Qwen-2.5 model.

**Parameters:**

- `model` (str): The name of the model to use.
- `messages` (Messages): A list of messages to pass to the model.
- `proxy` (str, optional): An optional proxy server to use. Defaults to `None`.

**Returns:**

- `AsyncResult`: An asynchronous result object representing the generator.

**Raises Exceptions:**

- `Exception`: If an error occurs during the operation.

**How the Function Works:**

1. Generates a unique session hash using a UUID.
2. Prepares headers and payload for the join request.
3. Sends a join request to the API endpoint.
4. Extracts the event ID from the response.
5. Prepares data stream request with headers and parameters.
6. Sends a data stream request to the data endpoint.
7. Iterates over the response content, extracting data chunks from the stream.
8. Handles different stages of the generation process (process_generating, process_completed).
9. Yields each generated fragment of text.
10. Returns the final response when the generation is completed.

**Examples:**

```python
from src.endpoints.gpt4free.g4f.Provider.hf_space.Qwen_Qwen_2_5 import Qwen_Qwen_2_5

async def example():
    model_name = "qwen-2.5"
    messages = [
        {"role": "user", "content": "Write a short story about a cat named Whiskers."},
    ]
    provider = Qwen_Qwen_2_5()
    async for response in provider.create_async_generator(model=model_name, messages=messages):
        print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(example())