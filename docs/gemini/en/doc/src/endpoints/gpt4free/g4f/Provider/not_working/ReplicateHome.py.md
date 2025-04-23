# Module Name

## Overview

This module defines the `ReplicateHome` class, which is an asynchronous provider for interacting with the Replicate.com API. It supports both text and image generation models. The module facilitates sending prompts to the Replicate API, polling for results, and yielding responses as an asynchronous generator. It handles various tasks such as formatting prompts, managing API requests, and processing responses, including error handling and timeout management.

## More details

This module is used to integrate with the Replicate.com API, allowing the `hypotez` project to leverage Replicate's hosted models for text and image generation. The `ReplicateHome` class extends `AsyncGeneratorProvider` and `ProviderModelMixin`, providing an interface for asynchronous generation tasks and model management. It supports streaming responses for text models and provides a means to retrieve image URLs for image models. The module is crucial for enabling AI-powered content generation within the `hypotez` ecosystem, offering flexibility in choosing between different models for various content generation needs.

## Classes

### `ReplicateHome`

**Description**: This class implements an asynchronous provider for interacting with the Replicate.com API, supporting both text and image generation models. It extends `AsyncGeneratorProvider` and `ProviderModelMixin`.

**Inherits**:
- `AsyncGeneratorProvider`: Provides the structure for asynchronous generator-based providers.
- `ProviderModelMixin`: Provides utilities for managing and resolving model aliases and versions.

**Attributes**:
- `url` (str): The base URL for Replicate.com.
- `api_endpoint` (str): The API endpoint for making predictions.
- `working` (bool): Indicates whether the provider is operational.
- `supports_stream` (bool): Indicates whether the provider supports streaming responses.
- `default_model` (str): The default text generation model.
- `default_image_model` (str): The default image generation model.
- `image_models` (list): A list of supported image generation models.
- `text_models` (list): A list of supported text generation models.
- `models` (list): A combined list of all supported models.
- `model_aliases` (dict): A dictionary mapping model aliases to their full names.
- `model_versions` (dict): A dictionary mapping model names to their specific version identifiers.

**Working principle**:
The `ReplicateHome` class facilitates interaction with the Replicate.com API by providing methods for sending prompts and retrieving results. It manages model selection and versioning through `model_aliases` and `model_versions`. The `create_async_generator` method is central to the class, handling the asynchronous request-response cycle. It constructs the appropriate API request, polls for results, and yields the generated content as an asynchronous generator. This class abstracts away the complexities of the Replicate API, providing a streamlined interface for the `hypotez` project to utilize AI-powered content generation.

**Methods**:
- `create_async_generator`: Creates an asynchronous generator for generating content from the Replicate API.

## Class Methods

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    prompt: str = None,
    proxy: str = None,
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для генерации контента из Replicate API.

    Args:
        cls (ReplicateHome): Ссылка на класс.
        model (str): Имя используемой модели.
        messages (Messages): Список сообщений для форматирования запроса.
        prompt (str, optional): Необязательный промпт для использования вместо сообщений. По умолчанию `None`.
        proxy (str, optional): URL прокси-сервера для использования. По умолчанию `None`.
        **kwargs: Дополнительные аргументы ключевого слова.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий сгенерированный контент.

    Raises:
        Exception: Если предсказание не удалось или истекло время ожидания.

    Пример:
        >>> async for chunk in ReplicateHome.create_async_generator(model='google-deepmind/gemma-2b-it', messages=[{'role': 'user', 'content': 'Translate to French: Hello'}]):
        ...     print(chunk)
    """
    ...
```

**Parameters**:
- `cls` (ReplicateHome): Ссылка на класс.
- `model` (str): Имя используемой модели.
- `messages` (Messages): Список сообщений для форматирования запроса.
- `prompt` (str, optional): Необязательный промпт для использования вместо сообщений. По умолчанию `None`.
- `proxy` (str, optional): URL прокси-сервера для использования. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы ключевого слова.

**How the function works**:

1. **Model Resolution**: Функция извлекает полное имя модели, используя `cls.get_model(model)`, что позволяет использовать псевдонимы моделей.
2. **Headers Setup**: Функция подготавливает заголовки HTTP-запроса, включая `user-agent`, `content-type` и т.д.
3. **Session Creation**: Функция создает асинхронный HTTP-сеанс с использованием `ClientSession`, передавая заголовки и необязательный прокси-сервер.
4. **Prompt Formatting**: Если `prompt` не предоставлен, функция либо использует последний элемент `messages` для image_models, либо форматирует `messages` с помощью `format_prompt` для text_models.
5. **Data Preparation**: Функция создает полезные данные JSON, включая имя модели, версию и входной промпт.
6. **API Request**: Функция отправляет POST-запрос к `cls.api_endpoint` с полезными данными JSON.
7. **Response Processing**: Функция проверяет статус ответа и извлекает идентификатор предсказания.
8. **Polling**: Функция выполняет опрос `poll_url` до `max_attempts` раз с задержкой в `delay` секунд.
9. **Result Handling**: Функция обрабатывает результат опроса, выдавая чанки сгенерированного контента или URL-адреса изображений в зависимости от используемой модели.
10. **Error Handling**: Функция генерирует исключение, если предсказание не удается или истекает время ожидания.
11. **Streaming**: Для text_models функция выдает отдельные чанки контента. Для image_models функция выдает `ImageResponse` с URL-адресом изображения.

**Examples**:
```python
async for chunk in ReplicateHome.create_async_generator(model='google-deepmind/gemma-2b-it', messages=[{'role': 'user', 'content': 'Translate to French: Hello'}]):
    print(chunk)
```
```python
async for image_response in ReplicateHome.create_async_generator(model='stability-ai/stable-diffusion-3', messages=[{'role': 'user', 'content': 'A futuristic cityscape'}]):
    print(image_response.image_url)
```

## Class Parameters
- `url` (str): The base URL for Replicate.com.
- `api_endpoint` (str): The API endpoint for making predictions.
- `working` (bool): Indicates whether the provider is operational.
- `supports_stream` (bool): Indicates whether the provider supports streaming responses.
- `default_model` (str): The default text generation model.
- `default_image_model` (str): The default image generation model.
- `image_models` (list): A list of supported image generation models.
- `text_models` (list): A list of supported text generation models.
- `models` (list): A combined list of all supported models.
- `model_aliases` (dict): A dictionary mapping model aliases to their full names.
- `model_versions` (dict): A dictionary mapping model names to their specific version identifiers.

**Examples**:
The `ReplicateHome` class allows you to generate text and images using Replicate's hosted models. You can select from a variety of text and image models and use the class to generate content asynchronously.
```python
async for chunk in ReplicateHome.create_async_generator(model='gemma-2b', messages=[{'role': 'user', 'content': 'Write a short poem about the sea'}]):
    print(chunk)
```
```python
async for image_response in ReplicateHome.create_async_generator(model='sd-3', messages=[{'role': 'user', 'content': 'A cat wearing a hat'}]):
    print(image_response.image_url)
```