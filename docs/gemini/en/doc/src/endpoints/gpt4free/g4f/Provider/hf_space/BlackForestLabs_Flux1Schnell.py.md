# Module BlackForestLabs_Flux1Schnell

## Overview

Этот модуль реализует асинхронный провайдер для генерации изображений с использованием модели BlackForestLabs Flux-1-Schnell. Он позволяет генерировать изображения на основе текстового запроса (prompt) с возможностью настройки параметров, таких как ширина, высота, количество шагов inference и seed.

## More details

Модуль предоставляет класс `BlackForestLabs_Flux1Schnell`, который наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`. Он использует `aiohttp` для выполнения асинхронных HTTP-запросов к API BlackForestLabs Flux-1-Schnell.

## Classes

### `BlackForestLabs_Flux1Schnell`

**Description**: Класс для взаимодействия с моделью BlackForestLabs Flux-1-Schnell для генерации изображений.
**Inherits**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию результатов.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями провайдера.

**Attributes**:
- `label` (str): Метка провайдера.
- `url` (str): URL главной страницы BlackForestLabs Flux-1-Schnell.
- `api_endpoint` (str): URL API для вызова inference.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `default_model` (str): Модель, используемая по умолчанию.
- `default_image_model` (str): Модель изображения, используемая по умолчанию.
- `model_aliases` (dict): Псевдонимы моделей.
- `image_models` (list): Список моделей изображений.
- `models` (list): Список моделей.

**Working principle**:
Класс использует асинхронные HTTP-запросы для взаимодействия с API BlackForestLabs Flux-1-Schnell. Он отправляет POST-запрос с параметрами генерации изображения и получает результат в виде URL изображения. Результат возвращается как `ImageResponse`.

## Class Methods

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    prompt: str = None,
    width: int = 768,
    height: int = 768,
    num_inference_steps: int = 2,
    seed: int = 0,
    randomize_seed: bool = True,
    **kwargs
) -> AsyncResult:
    """Создает асинхронный генератор для генерации изображений.

    Args:
        cls (type): Класс BlackForestLabs_Flux1Schnell.
        model (str): Модель для генерации изображения.
        messages (Messages): Список сообщений для формирования запроса.
        proxy (str, optional): Адрес прокси-сервера. По умолчанию `None`.
        prompt (str, optional): Текстовый запрос для генерации изображения. По умолчанию `None`.
        width (int, optional): Ширина изображения. По умолчанию 768.
        height (int, optional): Высота изображения. По умолчанию 768.
        num_inference_steps (int, optional): Количество шагов inference. По умолчанию 2.
        seed (int, optional): Seed для генерации изображения. По умолчанию 0.
        randomize_seed (bool, optional): Флаг для рандомизации seed. По умолчанию `True`.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий `ImageResponse` с URL изображения.

    Raises:
        ResponseError: Если возникает ошибка при генерации изображения.

    How the function works:
        1. Функция принимает параметры для генерации изображения, такие как модель, текстовый запрос, размеры изображения, seed и другие.
        2. Формируется полезная нагрузка (payload) с данными для POST-запроса к API.
        3. Выполняется POST-запрос к API `cls.api_endpoint` с использованием `aiohttp.ClientSession`.
        4. Проверяется статус ответа с помощью `raise_for_status`.
        5. Извлекается `event_id` из JSON-ответа.
        6. В цикле выполняются GET-запросы к API для получения статуса генерации изображения.
        7. Читаются события из потока ответа.
        8. Если тип события `error`, выбрасывается исключение `ResponseError`.
        9. Если тип события `complete`, извлекается URL изображения из JSON-данных и возвращается `ImageResponse`.

    """
```

### Class Parameters
- `cls` (type): Класс `BlackForestLabs_Flux1Schnell`.
- `model` (str): Модель для генерации изображения.
- `messages` (Messages): Список сообщений для формирования запроса.
- `proxy` (str, optional): Адрес прокси-сервера. По умолчанию `None`.
- `prompt` (str, optional): Текстовый запрос для генерации изображения. По умолчанию `None`.
- `width` (int, optional): Ширина изображения. По умолчанию 768.
- `height` (int, optional): Высота изображения. По умолчанию 768.
- `num_inference_steps` (int, optional): Количество шагов inference. По умолчанию 2.
- `seed` (int, optional): Seed для генерации изображения. По умолчанию 0.
- `randomize_seed` (bool, optional): Флаг для рандомизации seed. По умолчанию `True`.
- `**kwargs`: Дополнительные параметры.

**Examples**:
Пример вызова функции `create_async_generator` с различными параметрами:

```python
# from src.endpoints.gpt4free.g4f.typing import Messages
# messages: Messages = [{"role": "user", "content": "Generate a futuristic cityscape"}]
# result = await BlackForestLabs_Flux1Schnell.create_async_generator(
#     model="black-forest-labs-flux-1-schnell",
#     messages=messages,
#     width=512,
#     height=512,
#     num_inference_steps=5,
#     seed=42,
#     randomize_seed=False
# )
# async for item in result:
#     print(item)