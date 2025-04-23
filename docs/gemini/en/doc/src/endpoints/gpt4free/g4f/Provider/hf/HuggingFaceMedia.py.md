# Модуль: HuggingFaceMedia

## Обзор

Модуль `HuggingFaceMedia` предоставляет асинхронный интерфейс для генерации изображений и видео с использованием моделей Hugging Face. Он поддерживает различные задачи, такие как преобразование текста в изображение и текста в видео, и интегрируется с разными провайдерами через API Hugging Face.

## Более подробно

Этот модуль является частью проекта `hypotez` и предназначен для работы с моделями Hugging Face для генерации мультимедийного контента. Он использует асинхронные запросы для эффективного взаимодействия с API и поддерживает различные параметры конфигурации для управления процессом генерации. Модуль также обрабатывает ошибки и обеспечивает гибкость выбора провайдера для каждой задачи.

## Классы

### `HuggingFaceMedia`

**Описание**:
Класс `HuggingFaceMedia` является асинхронным провайдером для генерации изображений и видео с использованием моделей Hugging Face. Он расширяет `AsyncGeneratorProvider` и `ProviderModelMixin`.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями провайдера.

**Атрибуты**:
- `label` (str): Метка провайдера ("HuggingFace (Image/Video Generation)").
- `parent` (str): Родительский провайдер ("HuggingFace").
- `url` (str): URL Hugging Face ("https://huggingface.co").
- `working` (bool): Флаг, указывающий, что провайдер работает (True).
- `needs_auth` (bool): Флаг, указывающий необходимость аутентификации (True).
- `tasks` (list[str]): Список поддерживаемых задач (["text-to-image", "text-to-video"]).
- `provider_mapping` (dict[str, dict]): Словарь соответствия провайдеров.
- `task_mapping` (dict[str, str]): Словарь соответствия задач.
- `models` (list[str]): Список поддерживаемых моделей.
- `image_models` (list[str]): Список моделей для генерации изображений.
- `video_models` (list[str]): Список моделей для генерации видео.

**Принцип работы**:
Класс `HuggingFaceMedia` использует API Hugging Face для генерации изображений и видео на основе предоставленного текста. Он поддерживает различные модели и провайдеры, позволяя пользователям выбирать наиболее подходящий вариант для их нужд. Класс также обеспечивает обработку ошибок и асинхронное выполнение задач для повышения производительности.

**Методы**:
- `get_models(**kwargs)`: Возвращает список доступных моделей.
- `get_mapping(model: str, api_key: str = None)`: Получает соответствие провайдеров для указанной модели.
- `create_async_generator(model: str, messages: Messages, api_key: str = None, extra_data: dict = {}, prompt: str = None, proxy: str = None, timeout: int = 0, n: int = 1, aspect_ratio: str = None, height: int = None, width: int = None, resolution: str = "480p", **kwargs)`: Создает асинхронный генератор для выполнения задачи генерации.

## Методы класса

### `get_models`

```python
@classmethod
def get_models(cls, **kwargs) -> list[str]:
    """
    Возвращает список доступных моделей Hugging Face для генерации изображений и видео.

    Args:
        **kwargs: Дополнительные аргументы (не используются).

    Returns:
        list[str]: Список доступных моделей.
    """
```

**Назначение**:
Метод `get_models` получает список доступных моделей из API Hugging Face. Если список моделей еще не был получен, он делает запрос к API и сохраняет полученные модели в атрибуте класса `cls.models`.

**Как работает**:
1. Проверяет, если `cls.models` пуст. Если да, то выполняется запрос к API Hugging Face.
2. Формирует URL для запроса к API Hugging Face.
3. Выполняет GET-запрос к API.
4. Обрабатывает ответ API, извлекая информацию о моделях и их провайдерах.
5. Формирует списки моделей для изображений и видео.
6. Сохраняет полученные модели в атрибуте класса `cls.models`.

### `get_mapping`

```python
@classmethod
async def get_mapping(cls, model: str, api_key: str = None):
    """
    Получает соответствие провайдеров для указанной модели.

    Args:
        model (str): Имя модели.
        api_key (str, optional): API-ключ. Defaults to None.

    Returns:
        dict: Словарь соответствия провайдеров.
    """
```

**Назначение**:
Метод `get_mapping` получает соответствие провайдеров для указанной модели из API Hugging Face. Если соответствие уже существует в `cls.provider_mapping`, оно возвращается из кэша.

**Как работает**:
1. Проверяет, если соответствие для данной модели уже существует в `cls.provider_mapping`.
2. Если соответствие не найдено, выполняется запрос к API Hugging Face для получения информации о модели и её провайдерах.
3. Формирует заголовок запроса, включая API-ключ, если он предоставлен.
4. Выполняет GET-запрос к API.
5. Обрабатывает ответ API, извлекая информацию о соответствии провайдеров.
6. Сохраняет полученное соответствие в `cls.provider_mapping`.

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
    Создает асинхронный генератор для выполнения задачи генерации изображений или видео.

    Args:
        model (str): Имя модели.
        messages (Messages): Список сообщений для генерации.
        api_key (str, optional): API-ключ. Defaults to None.
        extra_data (dict, optional): Дополнительные данные для запроса. Defaults to {}.
        prompt (str, optional): Текст запроса. Defaults to None.
        proxy (str, optional): Proxy-сервер. Defaults to None.
        timeout (int, optional): Время ожидания запроса. Defaults to 0.
        n (int, optional): Количество генераций. Defaults to 1.
        aspect_ratio (str, optional): Соотношение сторон. Defaults to None.
        height (int, optional): Высота изображения. Defaults to None.
        width (int, optional): Ширина изображения. Defaults to None.
        resolution (str, optional): Разрешение видео. Defaults to "480p".
        **kwargs: Дополнительные аргументы.

    Yields:
        Reasoning: Информация о процессе генерации.
        ProviderInfo: Информация о провайдере.
        ImageResponse | VideoResponse: Сгенерированные изображения или видео.
    """
```

**Назначение**:
Метод `create_async_generator` создает асинхронный генератор для выполнения задачи генерации изображений или видео. Он выбирает подходящего провайдера, формирует запрос к API и возвращает сгенерированные результаты.

**Как работает**:
1. Определяет выбранного провайдера и модель.
2. Форматирует текст запроса.
3. Получает соответствие провайдеров для модели.
4. Определяет параметры запроса, такие как URL, заголовки и данные.
5. Выполняет асинхронные запросы к API выбранного провайдера.
6. Обрабатывает ответы API, возвращая сгенерированные изображения или видео.
7. Поддерживает генерацию нескольких результатов (`n`).
8. Логирует процесс выполнения.

**Внутренние функции**: Если есть какие-либо внутренние функции, то их нужно рассмотреть отдельно.
- `generate(extra_data: dict, aspect_ratio: str = None)`:

```python
async def generate(extra_data: dict, aspect_ratio: str = None):
    """
    Выполняет генерацию изображения или видео с использованием выбранного провайдера.

    Args:
        extra_data (dict): Дополнительные данные для запроса.
        aspect_ratio (str, optional): Соотношение сторон. Defaults to None.

    Yields:
        ProviderInfo: Информация о провайдере.
        ImageResponse | VideoResponse: Сгенерированные изображения или видео.
    """
```
   **Назначение**:
   Внутренняя функция `generate` выполняет фактическую генерацию изображения или видео с использованием выбранного провайдера.

   **Как работает**:
   1. Перебирает доступных провайдеров и выбирает подходящего.
   2. Формирует параметры запроса, такие как URL, заголовки и данные.
   3. Выполняет асинхронный запрос к API выбранного провайдера.
   4. Обрабатывает ответ API, возвращая сгенерированное изображение или видео.
   5. Обрабатывает возможные ошибки и исключения.

**Примеры**:
```python
# Пример вызова create_async_generator
model = "stabilityai/stable-diffusion-2"
messages = [{"role": "user", "content": "generate a cat image"}]
async for item in HuggingFaceMedia.create_async_generator(model=model, messages=messages, n=1):
    print(item)
```
```python
# Пример вызова с указанием API-ключа и дополнительных параметров
model = "stabilityai/stable-diffusion-2"
messages = [{"role": "user", "content": "generate a cat image"}]
extra_data = {"num_inference_steps": 30}
async for item in HuggingFaceMedia.create_async_generator(model=model, messages=messages, api_key="YOUR_API_KEY", extra_data=extra_data, n=2):
    print(item)