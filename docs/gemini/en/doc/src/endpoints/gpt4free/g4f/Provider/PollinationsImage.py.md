# Module `PollinationsImage.py`

## Overview

This module defines the `PollinationsImage` class, which inherits from `PollinationsAI` and is designed to generate images using the Pollinations AI service. It supports specifying the model, prompt, aspect ratio, dimensions, seed, and other parameters for image generation. The module also manages available image models and ensures they are loaded before generating images.

## More details

The `PollinationsImage` class extends the capabilities of `PollinationsAI` to specifically handle image generation tasks. It manages a list of available image models and provides a method to asynchronously generate images based on a given prompt and other configuration parameters. The module ensures that the models are loaded before generating images, synchronizing model loading using a class-level flag.

## Classes

### `PollinationsImage`

**Description**: This class is responsible for generating images using the Pollinations AI service. It inherits from `PollinationsAI` and provides methods to manage available image models and asynchronously generate images.
**Inherits**: `PollinationsAI`
**Attributes**:
- `label` (str): The label for this provider, set to "PollinationsImage".
- `default_model` (str): The default model used for image generation, set to "flux".
- `default_vision_model` (None): Default vision model.
- `default_image_model` (str): The default image model, which is the same as `default_model`.
- `image_models` (list): A list of available image models, initially containing the default image model.
- `_models_loaded` (bool): A flag to indicate whether the models have been loaded, initialized to `False`.

**Working principle**:
1.  The class inherits from `PollinationsAI`, gaining access to its base functionalities.
2.  It maintains a list of available image models, combining models from the parent class and additional ones.
3.  The `get_models` method ensures that the models are loaded only once by checking the `_models_loaded` flag.
4.  The `create_async_generator` method asynchronously generates images using the specified model and parameters, yielding chunks of data as they are generated.

**Methods**:
- `get_models`: Retrieves and combines available image models, ensuring they are loaded only once.
- `create_async_generator`: Asynchronously generates images using the specified model and parameters.

## Class Methods

### `get_models`

```python
@classmethod
def get_models(cls, **kwargs):
    """
    Метод для получения списка доступных моделей изображений.

    Args:
        **kwargs: Дополнительные аргументы, которые могут быть переданы в метод.

    Returns:
        list: Список доступных моделей изображений.

    Как работает функция:
    - Проверяет, были ли загружены модели ранее, используя флаг `_models_loaded`.
    - Если модели не были загружены:
        - Вызывает метод `get_models` родительского класса (`PollinationsAI`) для загрузки моделей родительского класса.
        - Объединяет модели из текущего класса (`cls.image_models`), родительского класса (`PollinationsAI.image_models`) и дополнительных моделей (`cls.extra_image_models`), удаляя дубликаты.
        - Обновляет список моделей изображений (`cls.image_models`) объединенным списком.
        - Устанавливает флаг `_models_loaded` в `True`, чтобы указать, что модели были загружены.
    - Возвращает список доступных моделей изображений.
    """
```

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    prompt: str = None,
    aspect_ratio: str = "1:1",
    width: int = None,
    height: int = None,
    seed: Optional[int] = None,
    cache: bool = False,
    nologo: bool = True,
    private: bool = False,
    enhance: bool = False,
    safe: bool = False,
    n: int = 4,
    **kwargs
) -> AsyncResult:
    """
    Асинхронно генерирует изображения с использованием указанной модели и параметров.

    Args:
        model (str): Модель для генерации изображений.
        messages (Messages): Список сообщений для формирования запроса.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        prompt (str, optional): Дополнительный текст запроса. По умолчанию `None`.
        aspect_ratio (str, optional): Соотношение сторон изображения. По умолчанию "1:1".
        width (int, optional): Ширина изображения. По умолчанию `None`.
        height (int, optional): Высота изображения. По умолчанию `None`.
        seed (Optional[int], optional): Зерно для генерации случайных чисел. По умолчанию `None`.
        cache (bool, optional): Использовать кэш. По умолчанию `False`.
        nologo (bool, optional): Удалять логотип. По умолчанию `True`.
        private (bool, optional): Сделать изображение приватным. По умолчанию `False`.
        enhance (bool, optional): Улучшить качество изображения. По умолчанию `False`.
        safe (bool, optional): Включить безопасный режим. По умолчанию `False`.
        n (int, optional): Количество генерируемых изображений. По умолчанию 4.
        **kwargs: Дополнительные аргументы.

    Yields:
        AsyncResult: Чанки данных, генерируемые в процессе создания изображения.

    Как работает функция:
    - Вызывает метод `get_models` для обновления списка моделей.
    - Асинхронно генерирует изображения, используя метод `_generate_image` класса `PollinationsAI`.
    - Передает в `_generate_image` параметры, такие как модель, текст запроса (сформированный с помощью `format_image_prompt`), прокси, соотношение сторон, размеры, зерно, настройки кэша, логотипа, приватности, улучшения качества, безопасного режима и количества изображений.
    - Передает чанки данных, генерируемые в процессе создания изображения.
    """
```

## Class Parameters

- `label` (str): The label for this provider, set to "PollinationsImage".
- `default_model` (str): The default model used for image generation, set to "flux".
- `default_vision_model` (None): Default vision model.
- `default_image_model` (str): The default image model, which is the same as `default_model`.
- `image_models` (list): A list of available image models, initially containing the default image model.
- `_models_loaded` (bool): A flag to indicate whether the models have been loaded, initialized to `False`.

## Examples

```python
# Пример создания экземпляра класса PollinationsImage не требуется, так как методы get_models и create_async_generator являются классовыми методами.

# Пример вызова метода get_models:
models = PollinationsImage.get_models()
print(f"Available models: {models}")

# Пример вызова метода create_async_generator (требует асинхронного контекста):
# async def main():
#     async for chunk in PollinationsImage.create_async_generator(model="flux", messages=["Example prompt"]):
#         print(chunk)
#
# import asyncio
# asyncio.run(main())