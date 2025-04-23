## \file hypotez/src/endpoints/gpt4free/g4f/Provider/hf_space/StabilityAI_SD35Large.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для работы с StabilityAI SD-3.5-Large через Hugging Face Space.
=====================================================================

Модуль содержит класс :class:`StabilityAI_SD35Large`, который используется для генерации изображений с использованием модели StabilityAI SD-3.5-Large, размещенной на Hugging Face Space.
Он поддерживает асинхронную генерацию изображений с возможностью указания различных параметров, таких как промпт, негативный промпт, seed и соотношение сторон.

Зависимости:
    - aiohttp
    - typing
    - src.typing
    - src.providers.response
    - src.image
    - src.errors
    - src.providers.base_provider
    - src.providers.helper

Пример использования:
    >>> model = "stabilityai-stable-diffusion-3-5-large"
    >>> messages = [{"role": "user", "content": "A cat wearing a hat"}]
    >>> async for image in StabilityAI_SD35Large.create_async_generator(model=model, messages=messages):
    ...     print(image.url)

 .. module:: src.endpoints.gpt4free.g4f.Provider.hf_space.StabilityAI_SD35Large
"""

## Overview

Модуль предоставляет класс `StabilityAI_SD35Large` для взаимодействия с моделью StabilityAI SD-3.5-Large, размещенной на платформе Hugging Face Space, с целью генерации изображений на основе текстовых запросов.

## More details

Этот модуль обеспечивает асинхронное взаимодействие с API Hugging Face Space для генерации изображений. Он поддерживает настройку различных параметров генерации, таких как модель, промпт, негативный промпт, seed, соотношение сторон и другие. Модуль использует библиотеку `aiohttp` для выполнения асинхронных HTTP-запросов и обрабатывает ответы от API, включая ошибки и прогресс генерации.

## Classes

### `StabilityAI_SD35Large`

**Описание**: Класс для генерации изображений с использованием модели StabilityAI SD-3.5-Large через Hugging Face Space.
**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет общие методы для работы с моделями провайдера.

**Атрибуты**:
- `label` (str): Метка провайдера ("StabilityAI SD-3.5-Large").
- `url` (str): URL Hugging Face Space ("https://stabilityai-stable-diffusion-3-5-large.hf.space").
- `api_endpoint` (str): Конечная точка API для запросов ("/gradio_api/call/infer").
- `working` (bool): Флаг, указывающий, что провайдер работает (True).
- `default_model` (str): Модель по умолчанию ('stabilityai-stable-diffusion-3-5-large').
- `default_image_model` (str): Модель изображения по умолчанию (совпадает с `default_model`).
- `model_aliases` (dict): Псевдонимы моделей ({"sd-3.5": default_model}).
- `image_models` (list): Список моделей изображений (совпадает со списком ключей `model_aliases`).
- `models` (list): Список моделей (совпадает со списком `image_models`).

**Принцип работы**:
1. Класс определяет URL API и параметры для взаимодействия с Hugging Face Space.
2. Метод `create_async_generator` создает асинхронный генератор, который отправляет запросы к API и возвращает изображения.
3. Генератор использует `aiohttp` для асинхронных HTTP-запросов.
4. Запросы включают параметры, такие как промпт, негативный промпт, seed и размеры изображения.
5. Ответы от API обрабатываются для получения URL изображений и информации о прогрессе.
6. В случае ошибок API, генерируется исключение `ResponseError`.

### Class Methods

#### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls, model: str, messages: Messages,
    prompt: str = None,
    negative_prompt: str = None,
    api_key: str = None, 
    proxy: str = None,
    aspect_ratio: str = "1:1",
    width: int = None,
    height: int = None,
    guidance_scale: float = 4.5,
    num_inference_steps: int = 50,
    seed: int = 0,
    randomize_seed: bool = True,
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для создания изображений с использованием StabilityAI SD-3.5-Large.

    Args:
        cls: Класс StabilityAI_SD35Large.
        model (str): Название модели для использования.
        messages (Messages): Список сообщений для формирования промпта.
        prompt (str, optional): Основной промпт для генерации изображения. По умолчанию `None`.
        negative_prompt (str, optional): Негативный промпт, чтобы избежать определенных элементов в изображении. По умолчанию `None`.
        api_key (str, optional): API ключ для доступа к сервису. По умолчанию `None`.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        aspect_ratio (str, optional): Соотношение сторон изображения (например, "1:1", "16:9"). По умолчанию "1:1".
        width (int, optional): Ширина изображения в пикселях. Если не указано, используется значение из соотношения сторон.
        height (int, optional): Высота изображения в пикселях. Если не указано, используется значение из соотношения сторон.
        guidance_scale (float, optional): Шкала соответствия промпту. По умолчанию 4.5.
        num_inference_steps (int, optional): Количество шагов для генерации изображения. По умолчанию 50.
        seed (int, optional): Seed для воспроизводимости результатов. По умолчанию 0.
        randomize_seed (bool, optional): Флаг для рандомизации seed. По умолчанию `True`.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий объекты `ImagePreview` и `ImageResponse`.

    Raises:
        ResponseError: Если произошла ошибка при запросе к API.
        RuntimeError: Если не удалось распарсить URL изображения из ответа API.

    Как работает функция:
    1. Формирует заголовки запроса, включая API ключ, если он предоставлен.
    2. Создает асинхронную сессию с использованием `aiohttp.ClientSession`.
    3. Форматирует промпт, объединяя сообщения и основной промпт.
    4. Вычисляет размеры изображения на основе соотношения сторон и предоставленных значений ширины и высоты.
    5. Формирует JSON-данные для запроса к API, включая промпт, негативный промпт, seed, размеры изображения и другие параметры.
    6. Отправляет POST-запрос к API.
    7. Получает `event_id` из ответа.
    8. Отправляет GET-запрос к API с `event_id` для получения данных о прогрессе генерации.
    9. Обрабатывает чанки данных, приходящие в ответе.
    10. Если приходит событие "error", генерируется исключение `ResponseError`.
    11. Если приходит событие "generating", извлекается URL изображения и возвращается объект `ImagePreview`.
    12. Если приходит событие "complete", извлекается URL изображения и возвращается объект `ImageResponse`.
    13. В случае ошибок при парсинге JSON или извлечении URL, генерируется исключение `RuntimeError`.

    Примеры:
        >>> model = "stabilityai-stable-diffusion-3-5-large"
        >>> messages = [{"role": "user", "content": "A cat wearing a hat"}]
        >>> async for image in StabilityAI_SD35Large.create_async_generator(model=model, messages=messages):
        ...     print(image.url)
        # Вывод: URL сгенерированного изображения (может быть предварительным или финальным)

        >>> model = "stabilityai-stable-diffusion-3-5-large"
        >>> messages = [{"role": "user", "content": "A dog playing guitar"}]
        >>> async for image in StabilityAI_SD35Large.create_async_generator(
        ...     model=model, messages=messages, aspect_ratio="16:9", seed=42
        ... ):
        ...     print(image.url)
        # Вывод: URL сгенерированного изображения с соотношением сторон 16:9 и seed 42.
    """
```

## Class Parameters

- `label` (str): Метка провайдера.
- `url` (str): URL Hugging Face Space.
- `api_endpoint` (str): Конечная точка API.
- `working` (bool): Флаг, указывающий, что провайдер работает.
- `default_model` (str): Модель по умолчанию.
- `default_image_model` (str): Модель изображения по умолчанию.
- `model_aliases` (dict): Псевдонимы моделей.
- `image_models` (list): Список моделей изображений.
- `models` (list): Список моделей.