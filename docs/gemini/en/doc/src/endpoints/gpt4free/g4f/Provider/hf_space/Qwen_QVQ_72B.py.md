# Документация для модуля `Qwen_QVQ_72B.py`

## Обзор

Модуль `Qwen_QVQ_72B.py` предоставляет асинхронную реализацию взаимодействия с моделью Qwen QVQ-72B, размещенной на платформе Hugging Face Space. Этот модуль позволяет отправлять текстовые запросы и изображения для получения ответов от модели. Он поддерживает как текстовые запросы, так и запросы, включающие изображения, и предоставляет асинхронный генератор для обработки ответов от модели.

## Детали

Модуль содержит класс `Qwen_QVQ_72B`, который наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`. Он определяет методы для создания асинхронного генератора, который отправляет запросы к API Qwen QVQ-72B и возвращает ответы в виде асинхронного генератора.

## Классы

### `Qwen_QVQ_72B`

**Описание**:
Класс для взаимодействия с моделью Qwen QVQ-72B через API Hugging Face Space.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию ответов.
- `ProviderModelMixin`: Предоставляет общие методы для работы с моделями.

**Атрибуты**:
- `label` (str): Метка провайдера, "Qwen QVQ-72B".
- `url` (str): URL API Hugging Face Space, "https://qwen-qvq-72b-preview.hf.space".
- `api_endpoint` (str): Endpoint API для генерации, "/gradio_api/call/generate".
- `working` (bool): Флаг, указывающий на работоспособность провайдера, `True`.
- `default_model` (str): Модель по умолчанию, "qwen-qvq-72b-preview".
- `default_vision_model` (str): Модель для обработки изображений по умолчанию, "qwen-qvq-72b-preview".
- `model_aliases` (dict): Псевдонимы моделей, {"qvq-72b": default_vision_model}.
- `vision_models` (list): Список моделей для обработки изображений.
- `models` (list): Список поддерживаемых моделей.

**Принцип работы**:
Класс использует `aiohttp.ClientSession` для асинхронных HTTP-запросов к API Hugging Face Space. Он поддерживает отправку текстовых запросов и запросов с изображениями. Для отправки изображений используется `FormData`, и изображения предварительно загружаются на сервер. Ответы от сервера обрабатываются асинхронно, и результаты возвращаются в виде асинхронного генератора.

## Методы класса

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls, model: str, messages: Messages,
    media: MediaListType = None,
    api_key: str = None, 
    proxy: str = None,
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для взаимодействия с моделью Qwen QVQ-72B.
    
    Args:
        model (str): Имя модели для использования.
        messages (Messages): Список сообщений для отправки в модель.
        media (MediaListType, optional): Список медиафайлов для отправки в модель. По умолчанию `None`.
        api_key (str, optional): API ключ для аутентификации. По умолчанию `None`.
        proxy (str, optional): Адрес прокси-сервера. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий ответы от модели.

    Raises:
        ResponseError: Если возникает ошибка при запросе к API.
        RuntimeError: Если не удается прочитать ответ от сервера.

    Пример:
        Пример вызова с текстовыми сообщениями:

        >>> model = "qwen-qvq-72b-preview"
        >>> messages = [{"role": "user", "content": "Hello, Qwen!"}]
        >>> generator = await Qwen_QVQ_72B.create_async_generator(model=model, messages=messages)
        >>> async for chunk in generator:
        ...     print(chunk)

        Пример вызова с медиафайлами:

        >>> model = "qwen-qvq-72b-preview"
        >>> messages = [{"role": "user", "content": "Describe this image."}]
        >>> media = [[("image.jpg", b"...")]]
        >>> generator = await Qwen_QVQ_72B.create_async_generator(model=model, messages=messages, media=media)
        >>> async for chunk in generator:
        ...     print(chunk)
    """
    ...
```

## Параметры класса

- `cls` (type): Ссылка на класс.
- `model` (str): Имя используемой модели.
- `messages` (Messages): Список сообщений для отправки модели.
- `media` (MediaListType, optional): Список медиафайлов для отправки модели. По умолчанию `None`.
- `api_key` (str, optional): API-ключ для аутентификации. По умолчанию `None`.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

## Примеры

Пример использования класса `Qwen_QVQ_72B` для отправки текстового запроса:

```python
model = "qwen-qvq-72b-preview"
messages = [{"role": "user", "content": "Привет, Qwen!"}]
generator = await Qwen_QVQ_72B.create_async_generator(model=model, messages=messages)
async for chunk in generator:
    print(chunk)
```

Пример использования класса `Qwen_QVQ_72B` для отправки запроса с изображением:

```python
model = "qwen-qvq-72b-preview"
messages = [{"role": "user", "content": "Опиши это изображение."}]
media = [[("image.jpg", b"...")]]
generator = await Qwen_QVQ_72B.create_async_generator(model=model, messages=messages, media=media)
async for chunk in generator:
    print(chunk)
```