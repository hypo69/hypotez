# Модуль BlackForestLabs_Flux1Schnell

## Обзор

Модуль `BlackForestLabs_Flux1Schnell` предоставляет асинхронный генератор для создания изображений с использованием модели BlackForestLabs Flux-1-Schnell. Он позволяет взаимодействовать с API Black Forest Labs Flux-1-Schnell для генерации изображений на основе текстового запроса.

## Подробнее

Этот модуль является провайдером изображений и использует API Black Forest Labs Flux-1-Schnell для генерации изображений на основе текстовых запросов. Он поддерживает настройку ширины, высоты, количества шагов инференса и зерна для генерации изображений.

## Классы

### `BlackForestLabs_Flux1Schnell`

**Описание**: Класс `BlackForestLabs_Flux1Schnell` предоставляет функциональность для генерации изображений с использованием модели BlackForestLabs Flux-1-Schnell. Он наследует от `AsyncGeneratorProvider` и `ProviderModelMixin`.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает базовую функциональность для асинхронных генераторов.
- `ProviderModelMixin`: Предоставляет миксин для работы с моделями провайдера.

**Атрибуты**:
- `label` (str): Название провайдера: `"BlackForestLabs Flux-1-Schnell"`.
- `url` (str): URL провайдера: `"https://black-forest-labs-flux-1-schnell.hf.space"`.
- `api_endpoint` (str): URL API для генерации изображений: `"https://black-forest-labs-flux-1-schnell.hf.space/call/infer"`.
- `working` (bool): Указывает, работает ли провайдер, установлено в `True`.
- `default_model` (str): Модель, используемая по умолчанию: `"black-forest-labs-flux-1-schnell"`.
- `default_image_model` (str): Модель изображения, используемая по умолчанию, совпадает с `default_model`.
- `model_aliases` (dict): Псевдонимы моделей: `{"flux-schnell": default_image_model, "flux": default_image_model}`.
- `image_models` (list): Список моделей изображений, полученный из ключей `model_aliases`.
- `models` (list): Список моделей, совпадающий с `image_models`.

**Принцип работы**:
Класс использует асинхронные запросы к API Black Forest Labs Flux-1-Schnell для генерации изображений на основе входных параметров, таких как текстовый запрос, ширина, высота и другие параметры генерации.

**Методы**:

#### `create_async_generator`

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
            model (str): Модель для генерации изображений.
            messages (Messages): Список сообщений для формирования запроса.
            proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
            prompt (str, optional): Текстовый запрос для генерации изображения. По умолчанию `None`.
            width (int, optional): Ширина изображения. По умолчанию `768`.
            height (int, optional): Высота изображения. По умолчанию `768`.
            num_inference_steps (int, optional): Количество шагов инференса. По умолчанию `2`.
            seed (int, optional): Зерно для генерации. По умолчанию `0`.
            randomize_seed (bool, optional): Флаг для рандомизации зерна. По умолчанию `True`.
            **kwargs: Дополнительные аргументы.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий сгенерированные изображения.

        Raises:
            ResponseError: Если возникает ошибка при генерации изображения.

        Как работает функция:
        - Функция принимает параметры для генерации изображения, такие как модель, текстовый запрос, размеры изображения, количество шагов инференса и зерно.
        - Она форматирует текстовый запрос с использованием функции format_image_prompt.
        - Создает полезную нагрузку (payload) с данными для запроса к API.
        - Отправляет POST-запрос к API Black Forest Labs Flux-1-Schnell.
        - Получает `event_id` из ответа и использует его для получения статуса генерации изображения.
        - В цикле ожидает завершения генерации, обрабатывая события `error` и `complete`.
        - При получении события `complete` извлекает URL изображения и возвращает его в виде объекта `ImageResponse`.
        - При возникновении ошибки выбрасывает исключение `ResponseError`.

        Внутренние функции:
            Внутри этой функции нет внутренних функций.

        """
```

## Параметры класса

- `label` (str): Название провайдера.
- `url` (str): URL провайдера.
- `api_endpoint` (str): URL API для генерации изображений.
- `working` (bool): Указывает, работает ли провайдер.
- `default_model` (str): Модель, используемая по умолчанию.
- `default_image_model` (str): Модель изображения, используемая по умолчанию.
- `model_aliases` (dict): Псевдонимы моделей.
- `image_models` (list): Список моделей изображений.
- `models` (list): Список моделей.

## Примеры

```python
# Пример использования create_async_generator
model = "flux-schnell"
messages = [{"role": "user", "content": "A futuristic cityscape"}]
proxy = None
prompt = "Generate a futuristic cityscape"
width = 512
height = 512
num_inference_steps = 10
seed = 42
randomize_seed = False

async def generate_image():
    async for image_response in BlackForestLabs_Flux1Schnell.create_async_generator(
        model=model,
        messages=messages,
        proxy=proxy,
        prompt=prompt,
        width=width,
        height=height,
        num_inference_steps=num_inference_steps,
        seed=seed,
        randomize_seed=randomize_seed
    ):
        print(f"Image URL: {image_response.images[0]}")

# Запуск асинхронной функции
# import asyncio
# asyncio.run(generate_image())