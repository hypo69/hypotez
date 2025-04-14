# Модуль StabilityAI_SD35Large для работы с моделью StabilityAI SD-3.5-Large

## Обзор

Модуль `StabilityAI_SD35Large` предоставляет асинхронный интерфейс для взаимодействия с моделью StabilityAI SD-3.5-Large, предназначенной для генерации изображений на основе текстовых запросов. Он использует API Hugging Face Space и поддерживает различные параметры для настройки процесса генерации изображений.

## Подробней

Этот модуль является частью проекта `hypotez` и предназначен для интеграции с другими компонентами, требующими функциональности генерации изображений. Он обеспечивает удобный способ отправки запросов к модели StabilityAI SD-3.5-Large и получения результатов в асинхронном режиме.

## Классы

### `StabilityAI_SD35Large`

**Описание**: Класс `StabilityAI_SD35Large` предоставляет методы для генерации изображений с использованием модели StabilityAI SD-3.5-Large.

**Наследует**:

- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Добавляет поддержку выбора модели.

**Атрибуты**:

- `label` (str): Метка провайдера ("StabilityAI SD-3.5-Large").
- `url` (str): URL API Hugging Face Space.
- `api_endpoint` (str): Путь к API для выполнения запросов.
- `working` (bool): Указывает, что провайдер активен.
- `default_model` (str): Модель по умолчанию ('stabilityai-stable-diffusion-3-5-large').
- `default_image_model` (str): Модель изображения по умолчанию.
- `model_aliases` (dict): Псевдонимы моделей ({"sd-3.5": default_model}).
- `image_models` (list): Список моделей изображений.
- `models` (list): Список моделей.

**Методы**:

- `create_async_generator()`: Асинхронно генерирует изображения на основе заданных параметров.

## Методы класса

### `create_async_generator`

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
    """Создает асинхронный генератор для создания изображений.

    Args:
        cls (StabilityAI_SD35Large): Класс, для которого создается генератор.
        model (str): Имя используемой модели.
        messages (Messages): Список сообщений для формирования запроса.
        prompt (str, optional): Основной текст запроса. По умолчанию `None`.
        negative_prompt (str, optional): Негативный текст запроса. По умолчанию `None`.
        api_key (str, optional): API ключ для доступа к сервису. По умолчанию `None`.
        proxy (str, optional): Адрес прокси-сервера. По умолчанию `None`.
        aspect_ratio (str, optional): Соотношение сторон изображения. По умолчанию `"1:1"`.
        width (int, optional): Ширина изображения. По умолчанию `None`.
        height (int, optional): Высота изображения. По умолчанию `None`.
        guidance_scale (float, optional): Масштаб соответствия запросу. По умолчанию `4.5`.
        num_inference_steps (int, optional): Количество шагов для генерации изображения. По умолчанию `50`.
        seed (int, optional): Зерно для генерации случайных чисел. По умолчанию `0`.
        randomize_seed (bool, optional): Флаг для рандомизации зерна. По умолчанию `True`.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий объекты `ImagePreview` и `ImageResponse`.

    Raises:
        ResponseError: Если превышен лимит GPU token.
        RuntimeError: Если не удалось распарсить URL изображения.

    Как работает функция:
    - Формирует заголовки запроса, включая API-ключ, если он предоставлен.
    - Создает асинхронную сессию для выполнения HTTP-запросов.
    - Форматирует текст запроса с использованием предоставленных сообщений и основного текста запроса.
    - Определяет размеры изображения на основе соотношения сторон.
    - Формирует данные запроса, включая текст запроса, негативный текст запроса, зерно, размеры изображения, масштаб соответствия запросу и количество шагов.
    - Отправляет POST-запрос к API для запуска процесса генерации изображения.
    - Получает `event_id` из ответа и использует его для получения событий о процессе генерации.
    - Асинхронно обрабатывает чанки данных из потока событий.
    - Если событие указывает на ошибку, вызывает исключение `ResponseError`.
    - Если событие указывает на генерацию, извлекает URL изображения и возвращает объект `ImagePreview`.
    - Если событие указывает на завершение, извлекает URL изображения и возвращает объект `ImageResponse`.

    Внутренние функции:
        В данной функции нет внутренних функций
    """
    ...
```

## Параметры класса

- `label` (str): Метка провайдера.
- `url` (str): URL API Hugging Face Space.
- `api_endpoint` (str): Путь к API для выполнения запросов.
- `working` (bool): Указывает, что провайдер активен.
- `default_model` (str): Модель по умолчанию.
- `default_image_model` (str): Модель изображения по умолчанию.
- `model_aliases` (dict): Псевдонимы моделей.
- `image_models` (list): Список моделей изображений.
- `models` (list): Список моделей.

## Примеры

```python
# Пример использования create_async_generator
import asyncio
from src.endpoints.gpt4free.g4f.Provider.hf_space.StabilityAI_SD35Large import StabilityAI_SD35Large
from src.endpoints.gpt4free.g4f.typing import Messages

async def main():
    model = 'stabilityai-stable-diffusion-3-5-large'
    messages: Messages = []
    prompt = "A cat sitting on a windowsill"
    negative_prompt = "ugly, distorted"
    api_key = "YOUR_API_KEY"
    aspect_ratio = "16:9"
    width = 1024
    height = 576

    generator = StabilityAI_SD35Large.create_async_generator(
        model=model,
        messages=messages,
        prompt=prompt,
        negative_prompt=negative_prompt,
        api_key=api_key,
        aspect_ratio=aspect_ratio,
        width=width,
        height=height
    )

    async for item in await generator:
        if isinstance(item, ImagePreview):
            print(f"Preview URL: {item.url}")
        elif isinstance(item, ImageResponse):
            print(f"Final URL: {item.url}")
            break

if __name__ == "__main__":
    asyncio.run(main())