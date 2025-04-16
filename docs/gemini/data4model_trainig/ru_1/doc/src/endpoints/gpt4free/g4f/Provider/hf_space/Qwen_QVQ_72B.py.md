# Модуль Qwen_QVQ_72B

## Обзор

Модуль `Qwen_QVQ_72B` предоставляет асинхронный интерфейс для взаимодействия с моделью Qwen QVQ-72B, размещенной на платформе Hugging Face Space. Он поддерживает как текстовые запросы, так и запросы с использованием изображений. Модуль предназначен для генерации текста на основе предоставленных сообщений и медиа-контента.

## Подробнее

Модуль использует `aiohttp` для выполнения асинхронных HTTP-запросов к API Hugging Face Space. Он включает в себя функциональность для загрузки изображений, форматирования запросов и обработки потоковых ответов от API. Модуль также обрабатывает ошибки, возникающие в процессе взаимодействия с API, и предоставляет информацию об ошибках.

## Классы

### `Qwen_QVQ_72B`

**Описание**: Класс `Qwen_QVQ_72B` предоставляет интерфейс для взаимодействия с моделью Qwen QVQ-72B. Он наследует функциональность от классов `AsyncGeneratorProvider` и `ProviderModelMixin`, что позволяет ему асинхронно генерировать текст и управлять моделями.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает базовую функциональность для асинхронных генераторов.
- `ProviderModelMixin`: Предоставляет методы для работы с моделями.

**Атрибуты**:
- `label` (str): Метка провайдера, `"Qwen QVQ-72B"`.
- `url` (str): URL-адрес Hugging Face Space, `"https://qwen-qvq-72b-preview.hf.space"`.
- `api_endpoint` (str): Конечная точка API для генерации текста, `"/gradio_api/call/generate"`.
- `working` (bool): Указывает, работает ли провайдер, `True`.
- `default_model` (str): Модель по умолчанию, `"qwen-qvq-72b-preview"`.
- `default_vision_model` (str): Модель для обработки изображений по умолчанию, `"qwen-qvq-72b-preview"`.
- `model_aliases` (dict): Псевдонимы моделей, `{"qvq-72b": default_vision_model}`.
- `vision_models` (list): Список моделей для обработки изображений, `list(model_aliases.keys())`.
- `models` (list): Список моделей, `vision_models`.

**Принцип работы**:
Класс `Qwen_QVQ_72B` использует асинхронные HTTP-запросы для взаимодействия с API Hugging Face Space. Он поддерживает как текстовые запросы, так и запросы с использованием изображений. При получении запроса с изображением класс загружает изображение на сервер, а затем отправляет запрос на генерацию текста с использованием загруженного изображения. Ответ от сервера обрабатывается потоково, что позволяет генерировать текст асинхронно.

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
    """Создает асинхронный генератор для взаимодействия с моделью Qwen QVQ-72B.

    Args:
        model (str): Название модели.
        messages (Messages): Список сообщений для отправки модели.
        media (MediaListType, optional): Список медиа-файлов (например, изображений) для отправки модели. По умолчанию `None`.
        api_key (str, optional): API-ключ для аутентификации. По умолчанию `None`.
        proxy (str, optional): Адрес прокси-сервера. По умолчанию `None`.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор, который выдает текст, сгенерированный моделью.

    Raises:
        ResponseError: Если получен ответ с ошибкой от API.
        RuntimeError: Если не удалось прочитать ответ от API.

    Как работает функция:
    - Функция принимает на вход модель, список сообщений, список медиа-файлов (если есть), API-ключ (если есть) и прокси (если есть).
    - Если предоставлен API-ключ, он добавляется в заголовок запроса.
    - Если предоставлены медиа-файлы (изображения), функция загружает их на сервер и получает URL-адрес загруженного изображения.
    - Затем функция отправляет запрос на генерацию текста с использованием URL-адреса изображения (если есть) и списка сообщений.
    - Функция обрабатывает ответ от сервера потоково, выдавая текст по частям.
    - Если в ответе содержится ошибка, функция вызывает исключение `ResponseError`.
    - Если не удается прочитать ответ от сервера, функция вызывает исключение `RuntimeError`.

    Внутренние функции:
    - Отсутствуют

    Примеры:
    Пример вызова функции без медиа-файлов:

    ```python
    model = "qwen-qvq-72b-preview"
    messages = [{"role": "user", "content": "Hello, how are you?"}]
    async for chunk in Qwen_QVQ_72B.create_async_generator(model, messages):
        print(chunk, end="")
    ```

    Пример вызова функции с медиа-файлом:

    ```python
    model = "qwen-qvq-72b-preview"
    messages = [{"role": "user", "content": "Describe this image."}]
    media = [[("image.jpg", b"image_data")]] # image_data - байтовое представление изображения
    async for chunk in Qwen_QVQ_72B.create_async_generator(model, messages, media=media):
        print(chunk, end="")
    ```
    """
    headers = {
        "Accept": "application/json",
    }
    if api_key is not None:
        headers["Authorization"] = f"Bearer {api_key}"
    async with ClientSession(headers=headers) as session:
        if media:
            data = FormData()
            data_bytes = to_bytes(media[0][0])
            data.add_field("files", data_bytes, content_type=is_accepted_format(data_bytes), filename=media[0][1])
            url = f"{cls.url}/gradio_api/upload?upload_id={get_random_string()}"
            async with session.post(url, data=data, proxy=proxy) as response:
                await raise_for_status(response)
                image = await response.json()
            data = {"data": [{"path": image[0]}, format_prompt(messages)]}
        else:
            data = {"data": [None, format_prompt(messages)]}
        async with session.post(f"{cls.url}{cls.api_endpoint}", json=data, proxy=proxy) as response:
            await raise_for_status(response)
            event_id = (await response.json()).get("event_id")
            async with session.get(f"{cls.url}{cls.api_endpoint}/{event_id}") as event_response:
                await raise_for_status(event_response)
                event = None
                text_position = 0
                async for chunk in event_response.content:
                    if chunk.startswith(b"event: "):
                        event = chunk[7:].decode(errors="replace").strip()
                    if chunk.startswith(b"data: "):
                        if event == "error":
                            raise ResponseError(f"GPU token limit exceeded: {chunk.decode(errors='replace')}")
                        if event in ("complete", "generating"):
                            try:
                                data = json.loads(chunk[6:])
                            except (json.JSONDecodeError, KeyError, TypeError) as e:
                                raise RuntimeError(f"Failed to read response: {chunk.decode(errors='replace')}", e)
                            if event == "generating":
                                if isinstance(data[0], str):
                                    yield data[0][text_position:]
                                    text_position = len(data[0])
                            else:
                                break
```

## Параметры класса

- `label` (str): Метка провайдера, `"Qwen QVQ-72B"`.
- `url` (str): URL-адрес Hugging Face Space, `"https://qwen-qvq-72b-preview.hf.space"`.
- `api_endpoint` (str): Конечная точка API для генерации текста, `"/gradio_api/call/generate"`.
- `working` (bool): Указывает, работает ли провайдер, `True`.
- `default_model` (str): Модель по умолчанию, `"qwen-qvq-72b-preview"`.
- `default_vision_model` (str): Модель для обработки изображений по умолчанию, `"qwen-qvq-72b-preview"`.
- `model_aliases` (dict): Псевдонимы моделей, `{"qvq-72b": default_vision_model}`.
- `vision_models` (list): Список моделей для обработки изображений, `list(model_aliases.keys())`.
- `models` (list): Список моделей, `vision_models`.