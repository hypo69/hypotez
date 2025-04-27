# PollinationsAI Provider for GPT4Free

## Overview

This module provides the `PollinationsAI` class, a provider for GPT4Free that uses the Pollinations AI API for text and image generation. The provider supports various models, including OpenAI, Flux, Dall-E 3, and others, allowing users to access a wide range of language and image generation capabilities. The provider also supports message history, system messages, and various generation parameters.

## Details

The `PollinationsAI` class implements the `AsyncGeneratorProvider` and `ProviderModelMixin` interfaces, enabling asynchronous generation and model selection. The provider fetches and updates the available models dynamically from the Pollinations AI API, ensuring users have access to the latest models.

The provider supports various features:

* **Text Generation**: Generate text using a variety of models, including OpenAI, Gemini, Qwen, and others.
* **Image Generation**: Generate images using models like Flux, Dall-E 3, and Midjourney.
* **Audio Generation**: Generate audio with various models.
* **Message History**: Use message history for context-aware generation.
* **System Messages**: Specify system-level instructions for the model.
* **Model Selection**: Choose the appropriate model based on your needs.
* **Generation Parameters**: Control generation parameters such as temperature, top_p, and frequency_penalty.
* **Media Support**: Include media (images, audio) in the conversation context.

## Classes

### `class PollinationsAI`

**Description**: Класс-поставщик для GPT4Free, который использует API Pollinations AI для генерации текста и изображений. 

**Inherits**: 
    - `AsyncGeneratorProvider`: Интерфейс для асинхронных генераторов.
    - `ProviderModelMixin`: Интерфейс для миксина моделей.

**Attributes**:
    - `label (str)`: "Pollinations AI".
    - `url (str)`: "https://pollinations.ai".
    - `working (bool)`: True.
    - `supports_system_message (bool)`: True.
    - `supports_message_history (bool)`: True.
    - `text_api_endpoint (str)`: "https://text.pollinations.ai".
    - `openai_endpoint (str)`: "https://text.pollinations.ai/openai".
    - `image_api_endpoint (str)`: "https://image.pollinations.ai/".
    - `default_model (str)`: "openai".
    - `default_image_model (str)`: "flux".
    - `default_vision_model (str)`: `default_model`.
    - `text_models (list)`: [`default_model`].
    - `image_models (list)`: [`default_image_model`].
    - `extra_image_models (list)`: ["flux-pro", "flux-dev", "flux-schnell", "midjourney", "dall-e-3", "turbo"].
    - `vision_models (list)`: [`default_vision_model`, "gpt-4o-mini", "o3-mini", "openai", "openai-large"].
    - `extra_text_models (list)`: `vision_models`.
    - `_models_loaded (bool)`: False.
    - `model_aliases (dict)`: 
        ```python
        {
            ### Text Models ###
            "gpt-4o-mini": "openai",
            "gpt-4": "openai-large",
            "gpt-4o": "openai-large",
            "o3-mini": "openai-reasoning",
            "qwen-2.5-coder-32b": "qwen-coder",
            "llama-3.3-70b": "llama",
            "mistral-nemo": "mistral",
            "gpt-4o-mini": "searchgpt",
            "llama-3.1-8b": "llamalight",
            "llama-3.3-70b": "llama-scaleway",
            "phi-4": "phi",
            "gemini-2.0": "gemini",
            "gemini-2.0-flash": "gemini",
            "gemini-2.0-flash-thinking": "gemini-thinking",
            "deepseek-r1": "deepseek-r1-llama",
            "gpt-4o-audio": "openai-audio",
            
            ### Image Models ###
            "sdxl-turbo": "turbo",
        }
        ```

**Methods**:

- `get_models(cls, **kwargs)`:
    - **Purpose**: Получение списка доступных моделей для текста и изображений.
    - **Parameters**:
        - `**kwargs`: Дополнительные аргументы.
    - **Returns**:
        - `list`: Список доступных моделей.
    - **How the Function Works**:
        - Проверяет, загружен ли список моделей. Если нет, то:
            - Получает список моделей для изображений с `image.pollinations.ai`.
            - Получает список моделей для текста с `text.pollinations.ai`.
            - Объединяет списки моделей для текста и изображений.
            - Сохраняет список моделей.
        - Возвращает объединенный список моделей.
    - **Examples**:
        ```python
        >>> PollinationsAI.get_models()
        ['openai', 'flux', 'flux-pro', 'flux-dev', 'flux-schnell', 'midjourney', 'dall-e-3', 'turbo', 'gpt-4o-mini', 'o3-mini', 'openai-large', 'gpt-4o-mini', 'gpt-4', 'gpt-4o', 'o3-mini', 'qwen-2.5-coder-32b', 'llama-3.3-70b', 'mistral-nemo', 'gpt-4o-mini', 'llama-3.1-8b', 'llama-3.3-70b', 'phi-4', 'gemini-2.0', 'gemini-2.0-flash', 'gemini-2.0-flash-thinking', 'deepseek-r1', 'gpt-4o-audio', 'sdxl-turbo']
        ```

- `create_async_generator(cls, model: str, messages: Messages, stream: bool = True, proxy: str = None, cache: bool = False, prompt: str = None, aspect_ratio: str = "1:1", width: int = None, height: int = None, seed: Optional[int] = None, nologo: bool = True, private: bool = False, enhance: bool = False, safe: bool = False, n: int = 1, media: MediaListType = None, temperature: float = None, presence_penalty: float = None, top_p: float = None, frequency_penalty: float = None, response_format: Optional[dict] = None, extra_parameters: list[str] = ["tools", "parallel_tool_calls", "tool_choice", "reasoning_effort", "logit_bias", "voice", "modalities", "audio"], **kwargs) -> AsyncResult:`:
    - **Purpose**: Создание асинхронного генератора для текста или изображений.
    - **Parameters**:
        - `model (str)`: Имя модели.
        - `messages (Messages)`: Список сообщений.
        - `stream (bool)`: Включить потоковый вывод (по умолчанию `True`).
        - `proxy (str)`: Прокси-сервер.
        - `cache (bool)`: Включить кэширование (по умолчанию `False`).
        - `prompt (str)`: Запрос для генерации изображений.
        - `aspect_ratio (str)`: Соотношение сторон для генерации изображений.
        - `width (int)`: Ширина изображения.
        - `height (int)`: Высота изображения.
        - `seed (Optional[int])`: Случайное число для генерации.
        - `nologo (bool)`: Удалить логотип (по умолчанию `True`).
        - `private (bool)`: Приватный режим (по умолчанию `False`).
        - `enhance (bool)`: Улучшение качества (по умолчанию `False`).
        - `safe (bool)`: Безопасный режим (по умолчанию `False`).
        - `n (int)`: Количество результатов (по умолчанию `1`).
        - `media (MediaListType)`: Список медиа-файлов.
        - `temperature (float)`: Температура для генерации текста.
        - `presence_penalty (float)`: Штраф за наличие.
        - `top_p (float)`: Верхний p.
        - `frequency_penalty (float)`: Штраф за частоту.
        - `response_format (Optional[dict])`: Формат ответа.
        - `extra_parameters (list[str])`: Дополнительные параметры.
        - `**kwargs`: Дополнительные аргументы.
    - **Returns**:
        - `AsyncResult`: Асинхронный результат.
    - **How the Function Works**:
        - Загружает список доступных моделей.
        - Выбирает модель на основе `model` аргумента.
        - Если модель относится к изображениям, то вызывается `_generate_image` для генерации изображения.
        - Если модель относится к тексту, то вызывается `_generate_text` для генерации текста.
    - **Examples**:
        ```python
        >>> async def main():
        ...     async for chunk in PollinationsAI.create_async_generator(model="openai", messages=[{"role": "user", "content": "Hello, how are you?"}]):
        ...         print(chunk)
        ...
        >>> asyncio.run(main())
        Hello, I am doing well. How are you?
        ```

- `_generate_image(cls, model: str, prompt: str, proxy: str, aspect_ratio: str, width: int, height: int, seed: Optional[int], cache: bool, nologo: bool, private: bool, enhance: bool, safe: bool, n: int) -> AsyncResult:`:
    - **Purpose**: Асинхронная генерация изображений.
    - **Parameters**:
        - `model (str)`: Имя модели.
        - `prompt (str)`: Запрос для генерации изображений.
        - `proxy (str)`: Прокси-сервер.
        - `aspect_ratio (str)`: Соотношение сторон для генерации изображений.
        - `width (int)`: Ширина изображения.
        - `height (int)`: Высота изображения.
        - `seed (Optional[int])`: Случайное число для генерации.
        - `cache (bool)`: Включить кэширование (по умолчанию `False`).
        - `nologo (bool)`: Удалить логотип (по умолчанию `True`).
        - `private (bool)`: Приватный режим (по умолчанию `False`).
        - `enhance (bool)`: Улучшение качества (по умолчанию `False`).
        - `safe (bool)`: Безопасный режим (по умолчанию `False`).
        - `n (int)`: Количество результатов (по умолчанию `1`).
    - **Returns**:
        - `AsyncResult`: Асинхронный результат.
    - **How the Function Works**:
        - Формирует URL для запроса на API.
        - Выполняет асинхронный запрос на API.
        - Обрабатывает ответ и возвращает URL изображения.
    - **Examples**:
        ```python
        >>> async def main():
        ...     async for chunk in PollinationsAI._generate_image(model="flux", prompt="A beautiful cat", aspect_ratio="1:1", width=512, height=512):
        ...         print(chunk)
        ...
        >>> asyncio.run(main())
        https://image.pollinations.ai/prompt/A%20beautiful%20cat?model=flux&nologo=true&private=false&enhance=false&safe=false&width=512&height=512&aspect_ratio=1:1&seed=12345
        ```

- `_generate_text(cls, model: str, messages: Messages, media: MediaListType, proxy: str, temperature: float, presence_penalty: float, top_p: float, frequency_penalty: float, response_format: Optional[dict], seed: Optional[int], cache: bool, stream: bool, extra_parameters: list[str], **kwargs) -> AsyncResult:`:
    - **Purpose**: Асинхронная генерация текста.
    - **Parameters**:
        - `model (str)`: Имя модели.
        - `messages (Messages)`: Список сообщений.
        - `media (MediaListType)`: Список медиа-файлов.
        - `proxy (str)`: Прокси-сервер.
        - `temperature (float)`: Температура для генерации текста.
        - `presence_penalty (float)`: Штраф за наличие.
        - `top_p (float)`: Верхний p.
        - `frequency_penalty (float)`: Штраф за частоту.
        - `response_format (Optional[dict])`: Формат ответа.
        - `seed (Optional[int])`: Случайное число для генерации.
        - `cache (bool)`: Включить кэширование (по умолчанию `False`).
        - `stream (bool)`: Включить потоковый вывод (по умолчанию `True`).
        - `extra_parameters (list[str])`: Дополнительные параметры.
        - `**kwargs`: Дополнительные аргументы.
    - **Returns**:
        - `AsyncResult`: Асинхронный результат.
    - **How the Function Works**:
        - Формирует данные для запроса на API.
        - Выполняет асинхронный запрос на API.
        - Обрабатывает ответ и возвращает сгенерированный текст.
    - **Examples**:
        ```python
        >>> async def main():
        ...     async for chunk in PollinationsAI._generate_text(model="openai", messages=[{"role": "user", "content": "Write a poem about a cat."}], temperature=0.7):
        ...         print(chunk)
        ...
        >>> asyncio.run(main())
        The cat, a creature of softest grace,
        With eyes of emerald, a velvet face.
        A hunter by instinct, yet gentle and kind,
        A purring companion, a friend you'll find.
        ...
        ```

## Parameter Details

- `model (str)`: Имя модели, которую нужно использовать для генерации.
- `messages (Messages)`: Список сообщений, которые представляют собой контекст для генерации.
- `stream (bool)`: Включить потоковый вывод.
- `proxy (str)`: URL прокси-сервера.
- `cache (bool)`: Включить кэширование ответов.
- `prompt (str)`: Запрос для генерации изображения.
- `aspect_ratio (str)`: Соотношение сторон для генерации изображения.
- `width (int)`: Ширина изображения.
- `height (int)`: Высота изображения.
- `seed (Optional[int])`: Случайное число для генерации изображения.
- `nologo (bool)`: Удалить логотип с изображения.
- `private (bool)`: Приватный режим генерации изображения.
- `enhance (bool)`: Улучшить качество изображения.
- `safe (bool)`: Безопасный режим генерации изображения.
- `n (int)`: Количество изображений, которые нужно сгенерировать.
- `media (MediaListType)`: Список медиа-файлов для контекста генерации.
- `temperature (float)`: Температура для генерации текста.
- `presence_penalty (float)`: Штраф за наличие.
- `top_p (float)`: Верхний p.
- `frequency_penalty (float)`: Штраф за частоту.
- `response_format (Optional[dict])`: Формат ответа.
- `extra_parameters (list[str])`: Дополнительные параметры, передаваемые модели.

## Examples

**1. Генерация текста с моделью OpenAI**:

```python
>>> from hypotez.src.endpoints.gpt4free.g4f.Provider.PollinationsAI import PollinationsAI
>>> async def main():
...     async for chunk in PollinationsAI.create_async_generator(model="openai", messages=[{"role": "user", "content": "Write a story about a cat."}]):
...         print(chunk)
...
>>> asyncio.run(main())
Once upon a time, in a cozy little cottage nestled amidst a sprawling garden, lived a mischievous cat named Whiskers. With fur as black as midnight and eyes that sparkled like emeralds, Whiskers was a creature of both charm and cunning.
```

**2. Генерация изображения с моделью Flux**:

```python
>>> from hypotez.src.endpoints.gpt4free.g4f.Provider.PollinationsAI import PollinationsAI
>>> async def main():
...     async for chunk in PollinationsAI.create_async_generator(model="flux", prompt="A cat playing with a ball of yarn", width=512, height=512):
...         print(chunk)
...
>>> asyncio.run(main())
https://image.pollinations.ai/prompt/A%20cat%20playing%20with%20a%20ball%20of%20yarn?model=flux&nologo=true&private=false&enhance=false&safe=false&width=512&height=512&aspect_ratio=1:1&seed=12345