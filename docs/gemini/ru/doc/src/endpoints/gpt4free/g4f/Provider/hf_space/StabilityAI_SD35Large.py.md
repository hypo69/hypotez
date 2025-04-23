# Модуль `StabilityAI_SD35Large`

## Обзор

Модуль `StabilityAI_SD35Large` представляет собой реализацию асинхронного провайдера для генерации изображений с использованием модели Stability AI SD-3.5-Large. Он предоставляет функциональность для взаимодействия с API Stability AI через Hugging Face Space и поддерживает различные параметры конфигурации, такие как прокси, соотношение сторон и seed.

## Подробнее

Модуль предназначен для интеграции с другими частями проекта, требующими генерации изображений. Он использует `aiohttp` для выполнения асинхронных HTTP-запросов и обрабатывает ответы от API Stability AI, предоставляя результаты в виде объектов `ImageResponse` и `ImagePreview`. Модуль также обеспечивает обработку ошибок и логирование для обеспечения стабильной работы.

## Классы

### `StabilityAI_SD35Large`

**Описание**: Класс `StabilityAI_SD35Large` является асинхронным провайдером для генерации изображений с использованием модели Stability AI SD-3.5-Large.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает базовую функциональность для асинхронных провайдеров, генерирующих данные.
- `ProviderModelMixin`: Предоставляет миксин для работы с моделями провайдера.

**Атрибуты**:
- `label` (str): Метка провайдера ("StabilityAI SD-3.5-Large").
- `url` (str): URL Hugging Face Space, используемого для API Stability AI.
- `api_endpoint` (str): Эндпоинт API для выполнения запросов на генерацию изображений.
- `working` (bool): Флаг, указывающий, что провайдер находится в рабочем состоянии.
- `default_model` (str): Модель, используемая по умолчанию ('stabilityai-stable-diffusion-3-5-large').
- `default_image_model` (str): Модель изображения, используемая по умолчанию.
- `model_aliases` (dict): Псевдонимы моделей, где ключ - псевдоним, значение - имя модели.
- `image_models` (list): Список моделей изображений.
- `models` (list): Список моделей (совпадает с `image_models`).

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для выполнения запросов к API Stability AI и обработки результатов.

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
    """
    Создает асинхронный генератор для генерации изображений с использованием API Stability AI.

    Args:
        cls (StabilityAI_SD35Large): Класс StabilityAI_SD35Large.
        model (str): Имя модели для генерации изображений.
        messages (Messages): Сообщения для формирования запроса.
        prompt (str, optional): Положительный запрос для генерации изображения. По умолчанию `None`.
        negative_prompt (str, optional): Отрицательный запрос для генерации изображения. По умолчанию `None`.
        api_key (str, optional): API-ключ для доступа к API Stability AI. По умолчанию `None`.
        proxy (str, optional): URL прокси-сервера для выполнения запросов. По умолчанию `None`.
        aspect_ratio (str, optional): Соотношение сторон изображения. По умолчанию "1:1".
        width (int, optional): Ширина изображения. Если не указано, используется значение из `aspect_ratio`.
        height (int, optional): Высота изображения. Если не указано, используется значение из `aspect_ratio`.
        guidance_scale (float, optional): Масштаб соответствия запросу. По умолчанию 4.5.
        num_inference_steps (int, optional): Количество шагов для генерации изображения. По умолчанию 50.
        seed (int, optional): Зерно для генерации изображения. По умолчанию 0.
        randomize_seed (bool, optional): Флаг, указывающий, нужно ли рандомизировать зерно. По умолчанию `True`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий объекты `ImagePreview` и `ImageResponse`.

    Raises:
        ResponseError: Если превышен лимит токенов GPU.
        RuntimeError: Если не удалось разобрать URL изображения из ответа API.

    **Как работает функция**:
    - Функция создает заголовки запроса, включая API-ключ, если он предоставлен.
    - Форматирует запрос изображения на основе предоставленных сообщений.
    - Использует функцию `use_aspect_ratio` для определения ширины и высоты изображения на основе соотношения сторон.
    - Формирует данные запроса, включая положительный и отрицательный запросы, seed, флаг рандомизации seed, ширину, высоту, масштаб соответствия запросу и количество шагов для генерации изображения.
    - Выполняет POST-запрос к API Stability AI для запуска процесса генерации изображения.
    - Получает `event_id` из ответа API и использует его для получения событий генерации изображения.
    - Асинхронно получает события генерации изображения и обрабатывает их.
    - Если событие указывает на ошибку, выбрасывается исключение `ResponseError`.
    - Если событие указывает на генерацию или завершение, извлекается URL изображения из данных события.
    - Для события "generating" возвращается объект `ImagePreview`.
    - Для события "complete" возвращается объект `ImageResponse` и генератор завершается.
    """
```

## Примеры

### Пример вызова `create_async_generator`

```python
# Пример вызова create_async_generator
model = "stabilityai-stable-diffusion-3-5-large"
messages = [{"role": "user", "content": "A beautiful landscape"}]
prompt = "A beautiful landscape"
negative_prompt = "ugly, deformed"
api_key = "your_api_key"
proxy = "http://your_proxy"
aspect_ratio = "16:9"
width = 1024
height = 576
guidance_scale = 7.5
num_inference_steps = 75
seed = 42
randomize_seed = False

async def main():
    generator = StabilityAI_SD35Large.create_async_generator(
        model=model,
        messages=messages,
        prompt=prompt,
        negative_prompt=negative_prompt,
        api_key=api_key,
        proxy=proxy,
        aspect_ratio=aspect_ratio,
        width=width,
        height=height,
        guidance_scale=guidance_scale,
        num_inference_steps=num_inference_steps,
        seed=seed,
        randomize_seed=randomize_seed
    )

    async for item in generator:
        if isinstance(item, ImagePreview):
            print(f"Preview URL: {item.url}")
        elif isinstance(item, ImageResponse):
            print(f"Image URL: {item.url}")
        break

# Запуск примера (необходимо для асинхронного кода)
# import asyncio
# asyncio.run(main())