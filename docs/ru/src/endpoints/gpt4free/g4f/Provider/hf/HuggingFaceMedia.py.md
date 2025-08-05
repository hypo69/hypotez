# Модуль HuggingFaceMedia

## Обзор

Модуль `HuggingFaceMedia` предназначен для работы с моделями Hugging Face, генерирующими изображения и видео. Он предоставляет функциональность для взаимодействия с различными API Hugging Face для задач преобразования текста в изображение и текст в видео.

## Подробнее

Этот модуль является частью проекта `hypotez` и обеспечивает интеграцию с платформой Hugging Face для генерации медиаконтента на основе текстовых запросов. Он поддерживает выбор различных провайдеров внутри Hugging Face и позволяет настраивать параметры генерации, такие как соотношение сторон, разрешение и другие.

## Классы

### `HuggingFaceMedia`

**Описание**: Класс `HuggingFaceMedia` предоставляет методы для генерации изображений и видео на основе моделей Hugging Face.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Добавляет функциональность для работы с моделями провайдера.

**Атрибуты**:
- `label` (str): Метка провайдера (по умолчанию: `"HuggingFace (Image/Video Generation)"`).
- `parent` (str): Родительский провайдер (по умолчанию: `"HuggingFace"`).
- `url` (str): URL Hugging Face (по умолчанию: `"https://huggingface.co"`).
- `working` (bool): Указывает, работает ли провайдер (по умолчанию: `True`).
- `needs_auth` (bool): Указывает, требуется ли аутентификация (по умолчанию: `True`).
- `tasks` (list[str]): Список поддерживаемых задач (по умолчанию: `["text-to-image", "text-to-video"]`).
- `provider_mapping` (dict[str, dict]): Словарь соответствий между моделями и провайдерами.
- `task_mapping` (dict[str, str]): Словарь соответствий между моделями и задачами.
- `models` (list[str]): Список доступных моделей.
- `image_models` (list[str]): Список моделей для генерации изображений.
- `video_models` (list[str]): Список моделей для генерации видео.

**Методы**:
- `get_models(**kwargs)`: Возвращает список доступных моделей.
- `get_mapping(model: str, api_key: str = None)`: Возвращает информацию о провайдерах для указанной модели.
- `create_async_generator(model: str, messages: Messages, api_key: str = None, extra_data: dict = {}, prompt: str = None, proxy: str = None, timeout: int = 0, n: int = 1, aspect_ratio: str = None, height: int = None, width: int = None, resolution: str = "480p", **kwargs)`: Создает асинхронный генератор для генерации изображений или видео.

## Методы класса

### `get_models`

```python
@classmethod
def get_models(cls, **kwargs) -> list[str]:
    """
    Извлекает список доступных моделей с Hugging Face API.

    Args:
        **kwargs: Дополнительные параметры.

    Returns:
        list[str]: Список идентификаторов моделей.

    Raises:
        Exception: Если не удается получить список моделей с API.

    
    - Функция отправляет GET-запрос к API Hugging Face для получения списка моделей.
    - Фильтрует модели, оставляя только те, у которых есть "inferenceProviderMapping" со статусом "live" и задачей "text-to-image" или "text-to-video".
    - Формирует списки task_mapping, image_models и video_models для дальнейшего использования.

    Примеры:
        >>> HuggingFaceMedia.get_models()
        ['model1', 'model2:provider', ...]
    """
```

### `get_mapping`

```python
@classmethod
async def get_mapping(cls, model: str, api_key: str = None):
    """
    Извлекает информацию о соответствии между моделью и провайдером.

    Args:
        model (str): Идентификатор модели.
        api_key (str, optional): API-ключ для аутентификации. По умолчанию `None`.

    Returns:
        dict: Информация о соответствии между моделью и провайдером.

    Raises:
        HTTPError: Если HTTP-запрос завершается с ошибкой.

    
    - Функция отправляет GET-запрос к API Hugging Face для получения информации о модели.
    - Извлекает "inferenceProviderMapping" со статусом "live" из ответа API.
    - Кэширует соответствие в `cls.provider_mapping` для дальнейшего использования.

    Примеры:
        >>> await HuggingFaceMedia.get_mapping('model1', 'api_key')
        {'provider1': {'status': 'live', 'task': 'text-to-image'}, ...}
    """
```

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    api_key: str = None,
    extra_data: dict = {},
    prompt: str = None,
    proxy: str = None,
    timeout: int = 0,
    # Video & Image Generation
    n: int = 1,
    aspect_ratio: str = None,
    # Only for Image Generation
    height: int = None,
    width: int = None,
    # Video Generation
    resolution: str = "480p",
    **kwargs
):
    """
    Создает асинхронный генератор для генерации изображений или видео на основе текстового запроса.

    Args:
        model (str): Идентификатор модели.
        messages (Messages): Список сообщений для формирования запроса.
        api_key (str, optional): API-ключ для аутентификации. По умолчанию `None`.
        extra_data (dict, optional): Дополнительные данные для запроса. По умолчанию `{}`.
        prompt (str, optional): Текстовый запрос. По умолчанию `None`.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        timeout (int, optional): Максимальное время ожидания запроса в секундах. По умолчанию `0`.
        n (int, optional): Количество генерируемых изображений или видео. По умолчанию `1`.
        aspect_ratio (str, optional): Соотношение сторон изображения или видео. По умолчанию `None`.
        height (int, optional): Высота изображения (только для изображений). По умолчанию `None`.
        width (int, optional): Ширина изображения (только для изображений). По умолчанию `None`.
        resolution (str, optional): Разрешение видео (только для видео). По умолчанию `"480p"`.
        **kwargs: Дополнительные параметры.

    Yields:
        ProviderInfo: Информация о провайдере.
        ImageResponse: Ответ с изображением.
        VideoResponse: Ответ с видео.
        Reasoning: Информация о процессе генерации.

    Raises:
        ModelNotSupportedError: Если модель не поддерживается.
        HTTPError: Если HTTP-запрос завершается с ошибкой.

    
    - Функция выбирает провайдера для указанной модели.
    - Формирует HTTP-запрос к API провайдера.
    - Отправляет запрос и получает ответ с изображением или видео.
    - Возвращает информацию о провайдере и медиаконтент.

    Примеры:
        >>> async for item in HuggingFaceMedia.create_async_generator(
        ...     model='model1',
        ...     messages=[{'role': 'user', 'content': 'text'}]
        ... ):
        ...     print(item)
    """