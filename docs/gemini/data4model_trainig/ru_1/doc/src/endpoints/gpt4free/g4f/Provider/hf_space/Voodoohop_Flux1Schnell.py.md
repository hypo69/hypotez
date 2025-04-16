# Модуль `Voodoohop_Flux1Schnell`

## Обзор

Модуль предоставляет асинхронный генератор для создания изображений с использованием API Voodoohop Flux-1-Schnell. Он позволяет генерировать изображения на основе текстового запроса (prompt) с возможностью настройки различных параметров, таких как ширина, высота, количество шагов inference и seed для генерации.

## Подробней

Модуль предназначен для интеграции с другими частями проекта `hypotez`, где требуется генерация изображений на основе текстовых описаний. Он использует асинхронные запросы для взаимодействия с API Voodoohop Flux-1-Schnell и предоставляет результаты в виде генератора изображений.

## Классы

### `Voodoohop_Flux1Schnell`

**Описание**: Класс реализует функциональность асинхронного генератора изображений на основе API Voodoohop Flux-1-Schnell.
**Наследует**: `AsyncGeneratorProvider`, `ProviderModelMixin`.

**Атрибуты**:
- `label` (str): Метка провайдера, `"Voodoohop Flux-1-Schnell"`.
- `url` (str): URL главной страницы Voodoohop Flux-1-Schnell, `"https://voodoohop-flux-1-schnell.hf.space"`.
- `api_endpoint` (str): URL API для генерации изображений, `"https://voodoohop-flux-1-schnell.hf.space/call/infer"`.
- `working` (bool): Флаг, указывающий на работоспособность провайдера, `True`.
- `default_model` (str): Модель, используемая по умолчанию, `"voodoohop-flux-1-schnell"`.
- `default_image_model` (str): Псевдоним для `default_model`.
- `model_aliases` (dict): Псевдонимы моделей, `{"flux-schnell": default_model, "flux": default_model}`.
- `image_models` (list): Список моделей изображений, полученный из ключей `model_aliases`.
- `models` (list): Список доступных моделей, совпадающий с `image_models`.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор изображений на основе заданных параметров.

## Методы класса

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
    """
    Создает асинхронный генератор изображений на основе заданных параметров.

    Args:
        cls (Voodoohop_Flux1Schnell): Класс, для которого создается генератор.
        model (str): Модель для генерации изображения.
        messages (Messages): Список сообщений для формирования запроса.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        prompt (str, optional): Текстовый запрос для генерации изображения. По умолчанию `None`.
        width (int, optional): Ширина изображения. По умолчанию 768.
        height (int, optional): Высота изображения. По умолчанию 768.
        num_inference_steps (int, optional): Количество шагов inference. По умолчанию 2.
        seed (int, optional): Seed для генерации изображения. По умолчанию 0.
        randomize_seed (bool, optional): Флаг для рандомизации seed. По умолчанию `True`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий объекты `ImageResponse` с URL изображений.

    Raises:
        ResponseError: Если возникает ошибка при генерации изображения.

    Как работает функция:
    - Функция принимает параметры для генерации изображения, включая модель, текстовый запрос, размеры изображения, seed и другие настройки.
    - Форматирует текстовый запрос с использованием `format_image_prompt`.
    - Создает payload с данными для запроса к API Voodoohop Flux-1-Schnell.
    - Отправляет асинхронный POST-запрос к API.
    - Получает `event_id` из ответа и начинает цикл ожидания статуса генерации.
    - Отправляет GET-запросы к API для получения статуса генерации.
    - Обрабатывает события, получаемые от API, и извлекает URL изображения при завершении генерации.
    - Возвращает `ImageResponse` с URL изображения и текстовым запросом.

    Внутренние функции:
        Внутри данной функции нет внутренних функций.
    """
    ...
```

## Параметры класса

- `model` (str): Модель для генерации изображения.
- `messages` (Messages): Список сообщений для формирования запроса.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `prompt` (str, optional): Текстовый запрос для генерации изображения. По умолчанию `None`.
- `width` (int, optional): Ширина изображения. По умолчанию 768.
- `height` (int, optional): Высота изображения. По умолчанию 768.
- `num_inference_steps` (int, optional): Количество шагов inference. По умолчанию 2.
- `seed` (int, optional): Seed для генерации изображения. По умолчанию 0.
- `randomize_seed` (bool, optional): Флаг для рандомизации seed. По умолчанию `True`.

## Примеры

Пример использования класса `Voodoohop_Flux1Schnell` для создания асинхронного генератора изображений:

```python
from src.endpoints.gpt4free.g4f.Provider.hf_space.Voodoohop_Flux1Schnell import Voodoohop_Flux1Schnell
from typing import List, Dict

# Пример использования
model = "voodoohop-flux-1-schnell"
messages: List[Dict[str, str]] = [{"role": "user", "content": "Generate a cat image"}]

async def generate_image():
    generator = Voodoohop_Flux1Schnell.create_async_generator(model=model, messages=messages)
    async for image_response in generator:
        print(image_response.images)

# Запуск асинхронной функции (пример для asyncio)
# import asyncio
# asyncio.run(generate_image())