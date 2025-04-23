# Module HuggingFaceAPI

## Overview

The `HuggingFaceAPI` module is designed to interact with the Hugging Face API for text generation. It extends the `OpenaiTemplate` class and provides methods for retrieving models, creating asynchronous generators, and handling API requests. The module supports both text and vision models and includes mechanisms for managing API keys and handling potential errors such as unsupported models or payment requirements.

## More details

This module is an essential part of the `hypotez` project, enabling integration with Hugging Face's models for various tasks such as conversational AI. It handles model selection, authentication, and request generation, streamlining the process of using Hugging Face's capabilities within the project.

## Classes

### `HuggingFaceAPI`

**Description**:
This class inherits from `OpenaiTemplate` and provides specific methods for interacting with the Hugging Face API, including model selection, asynchronous generation, and error handling.

**Inherits**:
- `OpenaiTemplate`: Inherits methods for generating requests and processing responses in a format compatible with OpenAI's API.

**Attributes**:
- `label` (str): The label of the provider, set to "HuggingFace (Text Generation)".
- `parent` (str): The parent provider, set to "HuggingFace".
- `url` (str): The base URL for the Hugging Face API, set to "https://api-inference.huggingface.com".
- `api_base` (str): The API base URL, set to "https://api-inference.huggingface.co/v1".
- `working` (bool): A flag indicating whether the provider is currently working, set to `True`.
- `needs_auth` (bool): A flag indicating whether authentication is required, set to `True`.
- `default_model` (str): The default model to use for text generation, set to `default_llama_model`.
- `default_vision_model` (str): The default model to use for vision tasks, set to `default_vision_model`.
- `vision_models` (list[str]): A list of supported vision models.
- `model_aliases` (dict[str, str]): A dictionary of model aliases.
- `fallback_models` (list[str]): A list of fallback models to use if the primary models are unavailable.
- `provider_mapping` (dict[str, dict]): A dictionary mapping models to their provider-specific configurations.

**Methods**:
- `get_model(model: str, **kwargs) -> str`: Retrieves the model name, handling potential `ModelNotSupportedError` exceptions.
- `get_models(**kwargs) -> list[str]`: Retrieves a list of supported models from the Hugging Face API.
- `get_mapping(cls, model: str, api_key: str = None)`: Retrieves provider mapping for a specific model.
- `create_async_generator(model: str, messages: Messages, api_base: str = None, api_key: str = None, max_tokens: int = 2048, max_inputs_lenght: int = 10000, media: MediaListType = None, **kwargs)`: Creates an asynchronous generator for processing messages using the Hugging Face API.
- `calculate_lenght(messages: Messages) -> int`: Calculates the length of the messages.

## Class Methods

### `get_model`

```python
@classmethod
def get_model(cls, model: str, **kwargs) -> str:
    """
    Функция извлекает имя модели, обрабатывая исключение ModelNotSupportedError, если модель не поддерживается.

    Args:
        model (str): Имя модели, которую нужно получить.
        **kwargs: Дополнительные аргументы.

    Returns:
        str: Имя модели.

    Raises:
        ModelNotSupportedError: Если запрошенная модель не поддерживается.
    """
    ...
```

### `get_models`

```python
@classmethod
def get_models(cls, **kwargs) -> list[str]:
    """
    Функция извлекает список поддерживаемых моделей из API Hugging Face.
    Если список моделей еще не получен, функция отправляет запрос к API Hugging Face для получения списка моделей.
    Если запрос успешен, функция фильтрует модели, чтобы включить только те, которые поддерживают conversational task.
    Если запрос не успешен, функция использует список fallback_models.

    Args:
        **kwargs: Дополнительные аргументы.

    Returns:
        list[str]: Список поддерживаемых моделей.
    """
    ...
```

### `get_mapping`

```python
@classmethod
async def get_mapping(cls, model: str, api_key: str = None):
    """
    Функция извлекает provider mapping для указанной модели.

    Args:
        model (str): Имя модели, для которой нужно получить provider mapping.
        api_key (str, optional): API-ключ для аутентификации. По умолчанию `None`.

    Returns:
        dict: Provider mapping для указанной модели.
    """
    ...
```

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    api_base: str = None,
    api_key: str = None,
    max_tokens: int = 2048,
    max_inputs_lenght: int = 10000,
    media: MediaListType = None,
    **kwargs
):
    """
    Функция создает асинхронный генератор для обработки сообщений с использованием API Hugging Face.

    Args:
        model (str): Имя модели для использования.
        messages (Messages): Список сообщений для обработки.
        api_base (str, optional): Базовый URL API. По умолчанию `None`.
        api_key (str, optional): API-ключ для аутентификации. По умолчанию `None`.
        max_tokens (int, optional): Максимальное количество токенов в ответе. По умолчанию 2048.
        max_inputs_lenght (int, optional): Максимальная длина входных данных. По умолчанию 10000.
        media (MediaListType, optional): Список медиафайлов для обработки. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Yields:
        ProviderInfo: Информация о провайдере.
        str: Часть сгенерированного текста.

    Raises:
        ModelNotSupportedError: Если модель не поддерживается.
        PaymentRequiredError: Если требуется оплата для использования модели.

    """
    ...
```

### `calculate_lenght`

```python
def calculate_lenght(messages: Messages) -> int:
    """
    Функция вычисляет длину сообщений.

    Args:
        messages (Messages): Список сообщений.

    Returns:
        int: Суммарная длина сообщений.
    """
    ...
```