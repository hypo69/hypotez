# Модуль StabilityAI_SD35Large

## Обзор

Модуль `StabilityAI_SD35Large` предоставляет асинхронный интерфейс для взаимодействия с моделью Stability AI SD-3.5-Large для генерации изображений. Он позволяет генерировать изображения на основе текстовых запросов (prompt), поддерживая различные параметры конфигурации, такие как соотношение сторон, размеры изображения, seed для воспроизводимости результатов и другие.

## Подробней

Этот модуль является частью системы, использующей различные AI-модели для генерации изображений на основе текстовых описаний. Он интегрируется с API Stability AI через асинхронные HTTP-запросы, используя `aiohttp` для обработки запросов и ответов. Модуль обрабатывает ответы в формате JSON, извлекая URL сгенерированных изображений и предоставляя их в виде объектов `ImageResponse` и `ImagePreview`.
В коде используется вебдрайвер, который импортируется из модуля `webdriver` проекта `hypotez`.

## Классы

### `StabilityAI_SD35Large`

**Описание**: Класс `StabilityAI_SD35Large` предоставляет функциональность для генерации изображений с использованием модели Stability AI SD-3.5-Large.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет общие методы для работы с моделями.

**Аттрибуты**:
- `label` (str): Название провайдера - "StabilityAI SD-3.5-Large".
- `url` (str): URL API Stability AI - "https://stabilityai-stable-diffusion-3-5-large.hf.space".
- `api_endpoint` (str): Конечная точка API для вызова - "/gradio_api/call/infer".
- `working` (bool): Индикатор работоспособности провайдера (всегда `True`).
- `default_model` (str): Модель по умолчанию - 'stabilityai-stable-diffusion-3-5-large'.
- `default_image_model` (str): Модель изображения по умолчанию - 'stabilityai-stable-diffusion-3-5-large'.
- `model_aliases` (dict): Псевдонимы моделей, например, {"sd-3.5": default_model}.
- `image_models` (list): Список моделей изображений, полученный из ключей `model_aliases`.
- `models` (list): Список поддерживаемых моделей, идентичный `image_models`.

**Методы**:
- `create_async_generator()`: Асинхронный генератор для создания изображений на основе запроса.

## Функции

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
    Асинхронно генерирует изображения, используя модель Stability AI SD-3.5-Large.

    Args:
        cls: Ссылка на класс `StabilityAI_SD35Large`.
        model (str): Имя используемой модели.
        messages (Messages): Список сообщений, используемых для формирования запроса.
        prompt (str, optional): Текстовый запрос для генерации изображения. По умолчанию `None`.
        negative_prompt (str, optional): Негативный запрос, указывающий, чего следует избегать в изображении. По умолчанию `None`.
        api_key (str, optional): API-ключ для доступа к Stability AI. По умолчанию `None`.
        proxy (str, optional): URL прокси-сервера для использования. По умолчанию `None`.
        aspect_ratio (str, optional): Соотношение сторон изображения (например, "1:1"). По умолчанию "1:1".
        width (int, optional): Ширина изображения. Если `None`, используется значение из `aspect_ratio`.
        height (int, optional): Высота изображения. Если `None`, используется значение из `aspect_ratio`.
        guidance_scale (float, optional): Масштаб соответствия запросу. По умолчанию 4.5.
        num_inference_steps (int, optional): Количество шагов для генерации изображения. По умолчанию 50.
        seed (int, optional): Seed для воспроизводимости результатов. По умолчанию 0.
        randomize_seed (bool, optional): Флаг для рандомизации seed. По умолчанию `True`.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий объекты `ImagePreview` и `ImageResponse` с URL сгенерированных изображений.

    Raises:
        ResponseError: Если превышен лимит токенов GPU.
        RuntimeError: Если не удалось распарсить URL изображения из ответа.

    """
```

**Назначение**:
Функция `create_async_generator` является асинхронным генератором, который создает изображения на основе текстового запроса, используя модель Stability AI SD-3.5-Large.

**Параметры**:
- `cls`: Ссылка на класс `StabilityAI_SD35Large`.
- `model` (str): Имя используемой модели.
- `messages (Messages)`: Список сообщений, используемых для формирования запроса.
- `prompt` (str, optional): Текстовый запрос для генерации изображения. По умолчанию `None`.
- `negative_prompt` (str, optional): Негативный запрос, указывающий, чего следует избегать в изображении. По умолчанию `None`.
- `api_key` (str, optional): API-ключ для доступа к Stability AI. По умолчанию `None`.
- `proxy` (str, optional): URL прокси-сервера для использования. По умолчанию `None`.
- `aspect_ratio` (str, optional): Соотношение сторон изображения (например, "1:1"). По умолчанию "1:1".
- `width` (int, optional): Ширина изображения. Если `None`, используется значение из `aspect_ratio`.
- `height` (int, optional): Высота изображения. Если `None`, используется значение из `aspect_ratio`.
- `guidance_scale` (float, optional): Масштаб соответствия запросу. По умолчанию 4.5.
- `num_inference_steps` (int, optional): Количество шагов для генерации изображения. По умолчанию 50.
- `seed` (int, optional): Seed для воспроизводимости результатов. По умолчанию 0.
- `randomize_seed` (bool, optional): Флаг для рандомизации seed. По умолчанию `True`.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, выдающий объекты `ImagePreview` и `ImageResponse` с URL сгенерированных изображений.

**Вызывает исключения**:
- `ResponseError`: Если превышен лимит токенов GPU.
- `RuntimeError`: Если не удалось распарсить URL изображения из ответа.

**Как работает функция**:

1. **Формирование заголовков**:
   - Функция начинает с формирования заголовков HTTP-запроса, включая `Content-Type` и, если предоставлен, `Authorization` с API-ключом.
2. **Создание сессии `ClientSession`**:
   - Создается асинхронная сессия `ClientSession` для выполнения HTTP-запросов.
3. **Форматирование запроса**:
   - Используется функция `format_image_prompt` для подготовки текстового запроса на основе `messages` и `prompt`.
4. **Конфигурация размеров изображения**:
   - Функция `use_aspect_ratio` используется для определения ширины и высоты изображения на основе `aspect_ratio`, `width` и `height`.
5. **Подготовка данных для запроса**:
   - Подготавливаются данные для POST-запроса, включая `prompt`, `negative_prompt`, `seed`, `randomize_seed`, `width`, `height`, `guidance_scale` и `num_inference_steps`.
6. **POST-запрос к API**:
   - Выполняется POST-запрос к API Stability AI (`cls.url + cls.api_endpoint`) с данными в формате JSON.
7. **Получение `event_id`**:
   - Из JSON-ответа извлекается `event_id`, который используется для последующих GET-запросов для получения статуса генерации изображения.
8. **GET-запросы для получения статуса**:
   - Выполняются GET-запросы к API (`cls.url + cls.api_endpoint + event_id`) для получения статуса генерации изображения. Ответ приходит в виде chunk-ов.
9. **Обработка chunk-ов**:
   - Читаются chunk-и из ответа. Каждый chunk проверяется на наличие `event` и `data`.
   - Если `event` равен "error", выбрасывается исключение `ResponseError`.
   - Если `event` равен "generating", извлекается URL изображения из `data`, и генерируется объект `ImagePreview`.
   - Если `event` равен "complete", извлекается URL изображения из `data`, генерируется объект `ImageResponse`, и генератор завершается.
10. **Обработка ошибок**:
    - Если не удается распарсить URL изображения из `data`, выбрасывается исключение `RuntimeError`.

**ASCII flowchart функции**:

```
+---------------------------------------------------+
|                Формирование заголовков              |
+-------------------------+-------------------------+
                            |
+-------------------------+-------------------------+
|     Создание ClientSession                        |
+-------------------------+-------------------------+
                            |
+-------------------------+-------------------------+
|     Форматирование запроса (format_image_prompt)   |
+-------------------------+-------------------------+
                            |
+-------------------------+-------------------------+
|  Конфигурация размеров изображения (use_aspect_ratio) |
+-------------------------+-------------------------+
                            |
+-------------------------+-------------------------+
|     Подготовка данных для запроса                  |
+-------------------------+-------------------------+
                            |
+-------------------------+-------------------------+
|         POST-запрос к API                         |
+-------------------------+-------------------------+
                            |
+-------------------------+-------------------------+
|       Получение event_id                         |
+-------------------------+-------------------------+
                            |
+-------------------------+-------------------------+
|   Цикл GET-запросов для получения статуса        |
|   и обработки chunk-ов                             |
+-------------------------+-------------------------+
                            |
                            |   event == "error"?  -> ResponseError
                            |   event == "generating"? -> ImagePreview
                            |   event == "complete"? -> ImageResponse
                            |   Ошибка парсинга URL? -> RuntimeError
                            |
+-------------------------+-------------------------+
|             Конец цикла                             |
+-------------------------+-------------------------+

```

**Примеры**:

Пример 1: Генерация изображения с использованием минимального набора параметров:

```python
model = "stabilityai-stable-diffusion-3-5-large"
messages = [{"role": "user", "content": "A cat wearing a hat"}]
async for image in StabilityAI_SD35Large.create_async_generator(model=model, messages=messages):
    print(image)
```

Пример 2: Генерация изображения с указанием размеров и seed:

```python
model = "stabilityai-stable-diffusion-3-5-large"
messages = [{"role": "user", "content": "A dog playing in the park"}]
async for image in StabilityAI_SD35Large.create_async_generator(
    model=model, messages=messages, width=512, height=512, seed=42, randomize_seed=False
):
    print(image)
```

Пример 3: Генерация изображения с негативным запросом и масштабом соответствия:

```python
model = "stabilityai-stable-diffusion-3-5-large"
messages = [{"role": "user", "content": "A futuristic city"}]
async for image in StabilityAI_SD35Large.create_async_generator(
    model=model, messages=messages, negative_prompt="people, cars", guidance_scale=7.0
):
    print(image)
```