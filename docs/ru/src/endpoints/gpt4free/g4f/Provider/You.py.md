# Модуль `You`

## Обзор

Модуль `You` предоставляет асинхронный интерфейс для взаимодействия с сервисом You.com, включая поддержку текстовых и визуальных запросов. Он позволяет использовать различные модели, такие как `gpt-4o-mini`, `gpt-4o`, `dall-e` и другие, для генерации текста и изображений. Модуль также обеспечивает загрузку файлов изображений на сервер You.com.

## Подробней

Модуль предназначен для интеграции с платформой You.com, обеспечивая возможность отправки запросов к различным моделям искусственного интеллекта, поддерживаемым сервисом. Он поддерживает как текстовые запросы, так и запросы на генерацию изображений, а также загрузку изображений для обработки.

## Классы

### `You(AsyncGeneratorProvider, ProviderModelMixin)`

**Описание**: Класс `You` является основным классом, предоставляющим функциональность для взаимодействия с сервисом You.com. Он наследует `AsyncGeneratorProvider` и `ProviderModelMixin`, что обеспечивает поддержку асинхронной генерации и управления моделями.

**Принцип работы**:
Класс инициализирует параметры для подключения к You.com, включая URL, список поддерживаемых моделей и настройки cookies. Он реализует методы для создания асинхронных генераторов ответов на основе предоставленных сообщений, а также для загрузки файлов изображений на сервер You.com.

**Аттрибуты**:
- `label` (str): Метка провайдера (You.com).
- `url` (str): URL сервиса You.com.
- `working` (bool): Указывает, работает ли провайдер.
- `default_model` (str): Модель, используемая по умолчанию (gpt-4o-mini).
- `default_vision_model` (str): Модель для обработки изображений по умолчанию ("agent").
- `image_models` (List[str]): Список моделей для генерации изображений (["dall-e"]).
- `models` (List[str]): Список поддерживаемых моделей.
- `_cookies` (Optional[Cookies]): Куки для аутентификации.
- `_cookies_used` (int): Счетчик использованных куки.
- `_telemetry_ids` (List[Any]): Список идентификаторов телеметрии.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для получения ответов от You.com.
- `upload_file`: Загружает файл на сервер You.com и возвращает информацию о загруженном файле.

## Функции

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    stream: bool = True,
    image: ImageType = None,
    image_name: str = None,
    proxy: str = None,
    timeout: int = 240,
    chat_mode: str = "default",
    cookies: Cookies = None,
    **kwargs,
) -> AsyncResult:
    """
    Создает асинхронный генератор для получения ответов от You.com.

    Args:
        model (str): Название модели для использования.
        messages (Messages): Список сообщений для отправки.
        stream (bool, optional): Флаг потоковой передачи данных. По умолчанию `True`.
        image (ImageType, optional): Изображение для отправки. По умолчанию `None`.
        image_name (str, optional): Имя файла изображения. По умолчанию `None`.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        timeout (int, optional): Время ожидания ответа. По умолчанию `240`.
        chat_mode (str, optional): Режим чата. По умолчанию "default".
        cookies (Cookies, optional): Куки для аутентификации. По умолчанию `None`.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор для получения ответов.

    Вызывает исключения:
        MissingRequirementsError: Если отсутствуют необходимые зависимости.
        ResponseError: Если получен ошибочный ответ от сервера.

    Как работает функция:
    1. Определяет режим чата в зависимости от наличия изображения и выбранной модели.
    2. Если не предоставлены куки и режим чата не "default", пытается получить их из файла или через браузер.
    3. Создает асинхронную сессию для отправки запросов.
    4. Если предоставлено изображение, загружает его на сервер You.com.
    5. Формирует данные для отправки в запросе, включая сообщения, режим чата и выбранную модель.
    6. Отправляет GET-запрос к API You.com и обрабатывает ответы, генерируя результаты в виде потока.

    ASCII flowchart:

    Определение режима чата
    ↓
    Получение куки (если необходимо)
    ↓
    Создание асинхронной сессии
    ↓
    Загрузка изображения (если есть)
    ↓
    Формирование данных запроса
    ↓
    Отправка GET-запроса и обработка ответов
    ↓
    Генерация результатов

    Примеры:
    ```python
    # Пример использования с текстовыми сообщениями
    messages = [{"role": "user", "content": "Hello, how are you?"}]
    async for message in You.create_async_generator(model="gpt-4o-mini", messages=messages):
        print(message)

    # Пример использования с изображением
    image_path = "path/to/image.jpg"
    with open(image_path, "rb") as f:
        image_data = f.read()
    async for message in You.create_async_generator(model="agent", messages=messages, image=image_data, image_name="image.jpg"):
        print(message)
    ```
    """
    ...
```

### `upload_file`

```python
@classmethod
async def upload_file(cls, client: StreamSession, cookies: Cookies, file: bytes, filename: str = None) -> dict:
    """
    Загружает файл на сервер You.com и возвращает информацию о загруженном файле.

    Args:
        client (StreamSession): Асинхронный HTTP-клиент.
        cookies (Cookies): Куки для аутентификации.
        file (bytes): Байтовое представление файла для загрузки.
        filename (str, optional): Имя файла. По умолчанию `None`.

    Returns:
        dict: Информация о загруженном файле, включая URL и размер.

    Вызывает исключения:
        ResponseError: Если получен ошибочный ответ от сервера.

    Как работает функция:
    1. Получает одноразовый nonce для загрузки файла с сервера You.com.
    2. Формирует данные формы для загрузки файла, включая сам файл, тип содержимого и имя файла.
    3. Отправляет POST-запрос на API загрузки файла.
    4. Обрабатывает ответ от сервера и возвращает информацию о загруженном файле.

    ASCII flowchart:

    Получение nonce
    ↓
    Формирование данных формы
    ↓
    Отправка POST-запроса
    ↓
    Обработка ответа

    Примеры:
    ```python
    # Пример использования
    import asyncio
    from src.requests import StreamSession  # Предполагается, что StreamSession находится в src.requests

    async def upload_example():
        # Замените 'ваши_куки' на реальные куки
        cookies = {'afUserId': 'ваши_куки'}
        file_path = 'path/to/image.jpg'
        with open(file_path, 'rb') as f:
            file_data = f.read()

        async with StreamSession() as client:
            result = await You.upload_file(client, cookies, file_data, filename='image.jpg')
            print(result)

    asyncio.run(upload_example())
    ```
    """
    ...