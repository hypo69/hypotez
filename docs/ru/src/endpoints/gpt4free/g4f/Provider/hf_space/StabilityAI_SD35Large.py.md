# Модуль `StabilityAI_SD35Large.py`

## Обзор

Модуль `StabilityAI_SD35Large.py` предоставляет класс `StabilityAI_SD35Large`, который является асинхронным провайдером для генерации изображений с использованием модели Stability AI SD-3.5-Large. Он позволяет генерировать изображения на основе текстового описания (prompt) с возможностью указания негативного промпта, размеров изображения, guidance scale и других параметров.

## Подробней

Этот модуль используется для интеграции с сервисом Stability AI через их API для создания изображений. Он предоставляет удобный интерфейс для отправки запросов и получения результатов в асинхронном режиме.

## Классы

### `StabilityAI_SD35Large`

**Описание**: Класс реализует асинхронный провайдер для генерации изображений с использованием модели Stability AI SD-3.5-Large.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет общие методы для работы с моделями провайдера.

**Атрибуты**:
- `label` (str): Название провайдера: `"StabilityAI SD-3.5-Large"`.
- `url` (str): URL API Stability AI: `"https://stabilityai-stable-diffusion-3-5-large.hf.space"`.
- `api_endpoint` (str): Endpoint API для запросов: `"/gradio_api/call/infer"`.
- `working` (bool): Флаг, указывающий на работоспособность провайдера: `True`.
- `default_model` (str): Модель по умолчанию: `'stabilityai-stable-diffusion-3-5-large'`.
- `default_image_model` (str): Модель изображения по умолчанию: совпадает с `default_model`.
- `model_aliases` (dict): Алиасы моделей, например `{"sd-3.5": default_model}`.
- `image_models` (list): Список моделей изображений, полученный из ключей `model_aliases`.
- `models` (list): Список моделей, совпадающий с `image_models`.

**Методы**:

- `create_async_generator`: Асинхронный генератор для создания изображений на основе заданных параметров.

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
    """Асинхронный генератор для создания изображений на основе заданных параметров.

    Args:
        cls (StabilityAI_SD35Large): Ссылка на класс.
        model (str): Модель для генерации изображений.
        messages (Messages): Список сообщений, используемых для формирования промпта.
        prompt (str, optional): Текстовое описание изображения (промпт). По умолчанию `None`.
        negative_prompt (str, optional): Негативный промпт, описывающий что не должно быть на изображении. По умолчанию `None`.
        api_key (str, optional): API ключ для доступа к Stability AI. По умолчанию `None`.
        proxy (str, optional): Адрес прокси-сервера. По умолчанию `None`.
        aspect_ratio (str, optional): Соотношение сторон изображения. По умолчанию `"1:1"`.
        width (int, optional): Ширина изображения. По умолчанию `None`.
        height (int, optional): Высота изображения. По умолчанию `None`.
        guidance_scale (float, optional): Guidance scale. По умолчанию `4.5`.
        num_inference_steps (int, optional): Количество шагов inference. По умолчанию `50`.
        seed (int, optional): Зерно для генерации случайных чисел. По умолчанию `0`.
        randomize_seed (bool, optional): Флаг, указывающий на необходимость рандомизации зерна. По умолчанию `True`.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий объекты `ImagePreview` и `ImageResponse`.

    Raises:
        ResponseError: Если превышен лимит GPU token.
        RuntimeError: Если не удалось распарсить URL изображения из ответа.

    Внутренние функции:
        Отсутствуют.
    """
    ...
```

**Назначение**: Создает асинхронный генератор для генерации изображений на основе заданных параметров.

**Параметры**:
- `cls` (StabilityAI_SD35Large): Ссылка на класс.
- `model` (str): Модель для генерации изображений.
- `messages` (Messages): Список сообщений, используемых для формирования промпта.
- `prompt` (str, optional): Текстовое описание изображения (промпт). По умолчанию `None`.
- `negative_prompt` (str, optional): Негативный промпт, описывающий что не должно быть на изображении. По умолчанию `None`.
- `api_key` (str, optional): API ключ для доступа к Stability AI. По умолчанию `None`.
- `proxy` (str, optional): Адрес прокси-сервера. По умолчанию `None`.
- `aspect_ratio` (str, optional): Соотношение сторон изображения. По умолчанию `"1:1"`.
- `width` (int, optional): Ширина изображения. По умолчанию `None`.
- `height` (int, optional): Высота изображения. По умолчанию `None`.
- `guidance_scale` (float, optional): Guidance scale. По умолчанию `4.5`.
- `num_inference_steps` (int, optional): Количество шагов inference. По умолчанию `50`.
- `seed` (int, optional): Зерно для генерации случайных чисел. По умолчанию `0`.
- `randomize_seed` (bool, optional): Флаг, указывающий на необходимость рандомизации зерна. По умолчанию `True`.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, выдающий объекты `ImagePreview` и `ImageResponse`.

**Вызывает исключения**:
- `ResponseError`: Если превышен лимит GPU token.
- `RuntimeError`: Если не удалось распарсить URL изображения из ответа.

**Как работает функция**:

1. **Подготовка заголовков**: Функция подготавливает заголовки для HTTP-запроса, включая `Content-Type` и `Authorization` (если предоставлен `api_key`).
2. **Формирование промпта**: Использует функцию `format_image_prompt` для формирования полного промпта на основе списка сообщений и основного промпта.
3. **Определение размеров изображения**: Использует функцию `use_aspect_ratio` для определения ширины и высоты изображения на основе `aspect_ratio`, `width` и `height`.
4. **Создание тела запроса**: Формирует тело запроса в формате JSON, включающее промпт, негативный промпт, seed, флаг рандомизации зерна, ширину, высоту, guidance scale и количество шагов inference.
5. **Отправка запроса**: Отправляет POST-запрос к API Stability AI и получает `event_id` из ответа.
6. **Получение результата**: Отправляет GET-запрос к endpoint `/gradio_api/call/infer/{event_id}` для получения результата генерации изображения.  Результат возвращается по частям (chunks).
7. **Обработка чанков**: Для каждого полученного чанка проверяется его тип (`event` или `data`).
    - Если `event` равен `"error"`, выбрасывается исключение `ResponseError` с сообщением об ошибке.
    - Если `event` равен `"generating"`, извлекается URL изображения и генерируется объект `ImagePreview`.
    - Если `event` равен `"complete"`, извлекается URL изображения и генерируется объект `ImageResponse`, после чего цикл завершается.
8. **Обработка ошибок**: В случае ошибок парсинга JSON или отсутствия ключей в ответе, выбрасывается исключение `RuntimeError`.

**ASCII flowchart**:

```
    [Начало]
     |
     | Подготовка заголовков (headers)
     |
     | Формирование промпта (format_image_prompt)
     |
     | Определение размеров изображения (use_aspect_ratio)
     |
     | Создание тела запроса (data)
     |
     | Отправка POST-запроса (POST) -> Получение event_id
     |
     | Отправка GET-запроса (GET) -> Получение чанков
     |
     |--- event == "error"? -- Да --> [ResponseError]
     |   |
     |   Нет
     |   |
     |--- event == "generating"? -- Да --> [ImagePreview] -> [yield]
     |   |
     |   Нет
     |   |
     |--- event == "complete"? -- Да --> [ImageResponse] -> [yield] -> [Конец]
     |   |
     |   Нет
     |   |
     [Обработка ошибок]
```

**Примеры**:

Примеры использования функции не предоставлены.