# Модуль Gemini для работы с Google Gemini
## Обзор

Модуль `Gemini` предназначен для взаимодействия с моделями Google Gemini. Он предоставляет асинхронный генератор для обработки текстовых запросов и получения ответов от модели. Модуль поддерживает работу с изображениями и предоставляет возможность автоматического обновления cookies для обеспечения стабильной работы.

## Подробнее

Этот модуль является частью проекта `hypotez` и обеспечивает интеграцию с моделями Google Gemini для генерации текста и обработки запросов. Он использует асинхронные запросы для взаимодействия с API Google Gemini и предоставляет удобные инструменты для обработки ответов и управления cookies.

## Классы

### `Gemini`

**Описание**: Класс `Gemini` является асинхронным генератором и предоставляет методы для взаимодействия с моделями Google Gemini.
   **Наследует**:
      - `AsyncGeneratorProvider`: базовый класс для асинхронных генераторов.
      - `ProviderModelMixin`:  миксин, предоставляющий функциональность для работы с моделями.

   **Атрибуты**:
      - `label` (str): Метка провайдера (Google Gemini).
      - `url` (str): URL для доступа к Gemini.
      - `needs_auth` (bool): Требуется ли аутентификация (True).
      - `working` (bool):  Указывает, работает ли провайдер в данный момент (True).
      - `use_nodriver` (bool):  Использовать ли бездрайверный режим (True).
      - `default_model` (str): Модель по умолчанию (пустая строка).
      - `default_image_model` (str): Модель для обработки изображений по умолчанию (пустая строка).
      - `default_vision_model` (str): Модель для обработки визуальных данных по умолчанию (пустая строка).
      - `image_models` (list): Список моделей, поддерживающих обработку изображений.
      - `models` (list): Список поддерживаемых моделей.
      - `model_aliases` (dict):  Словарь псевдонимов моделей.
      - `synthesize_content_type` (str): Тип контента для синтеза речи (audio/vnd.wav).
      - `_cookies` (Cookies): Cookies для аутентификации.
      - `_snlm0e` (str): Значение параметра SNlM0e, необходимое для запросов.
      - `_sid` (str):  Идентификатор сессии.
      - `auto_refresh` (bool):  Автоматически обновлять cookies (True).
      - `refresh_interval` (int): Интервал обновления cookies в секундах (540).
      - `rotate_tasks` (dict): Словарь задач для ротации cookies.

   **Принцип работы**:
      Класс `Gemini` использует асинхронные методы для аутентификации, отправки запросов и обработки ответов от API Google Gemini. Он поддерживает работу с cookies, автоматическое обновление cookies и загрузку изображений. Класс также предоставляет методы для синтеза речи и обработки ответов с изображениями и видео.

   **Методы**:
      - `nodriver_login(proxy: str = None) -> AsyncIterator[str]`:  Асинхронный генератор для выполнения входа в систему без драйвера.
      - `start_auto_refresh(proxy: str = None) -> None`: Запускает фоновую задачу для автоматического обновления cookies.
      - `create_async_generator(model: str, messages: Messages, proxy: str = None, cookies: Cookies = None, connector: BaseConnector = None, media: MediaListType = None, return_conversation: bool = False, conversation: Conversation = None, language: str = "en", **kwargs) -> AsyncResult`:  Создает асинхронный генератор для отправки запросов и получения ответов от модели Gemini.
      - `synthesize(params: dict, proxy: str = None) -> AsyncIterator[bytes]`:  Синтезирует речь на основе переданного текста.
      - `build_request(prompt: str, language: str, conversation: Conversation = None, uploads: list[list[str, str]] = None, tools: list[list[str]] = []) -> list`: Строит запрос для отправки в API Gemini.
      - `upload_images(connector: BaseConnector, media: MediaListType) -> list`: Загружает изображения в API Gemini.
      - `fetch_snlm0e(session: ClientSession, cookies: Cookies)`:  Извлекает значение параметра SNlM0e из ответа сервера.

### `Conversation`

**Описание**: Класс для представления состояния разговора с моделью Gemini.
    **Наследует**:
        - `JsonConversation`: базовый класс для представления разговора в формате JSON.

    **Атрибуты**:
        - `conversation_id` (str): Идентификатор разговора.
        - `response_id` (str): Идентификатор последнего ответа.
        - `choice_id` (str): Идентификатор выбранного варианта ответа.
        - `model` (str):  Использованная модель.

    **Принцип работы**:
        Класс `Conversation` хранит информацию о состоянии разговора, такую как идентификаторы разговора, ответа и выбранного варианта ответа, а также использованную модель.

### Методы класса

#### `nodriver_login`

```python
@classmethod
async def nodriver_login(cls, proxy: str = None) -> AsyncIterator[str]:
    """
    Асинхронный генератор для выполнения входа в систему без использования драйвера браузера.

    Args:
        proxy (str, optional): Прокси-сервер для использования при подключении. По умолчанию `None`.

    Returns:
        AsyncIterator[str]: Асинхронный итератор, возвращающий строки с информацией о процессе входа.

    Raises:
        ImportError: Если не установлен модуль `nodriver`.

    Как работает функция:
    - Проверяет, установлен ли модуль `nodriver`. Если нет, завершает работу.
    - Получает экземпляр браузера и функцию остановки браузера из `get_nodriver`.
    - Получает URL для входа из переменной окружения `G4F_LOGIN_URL`.
    - Открывает страницу в браузере.
    - Извлекает cookies из браузера.
    - Закрывает страницу и останавливает браузер.
    - Сохраняет cookies в атрибуте `_cookies` класса.

    Примеры:
        >>> async for chunk in Gemini.nodriver_login():
        ...     print(chunk)
    """
    ...

#### `start_auto_refresh`

```python
@classmethod
async def start_auto_refresh(cls, proxy: str = None) -> None:
    """
    Запускает фоновую задачу для автоматического обновления cookies.

    Args:
        proxy (str, optional): Прокси-сервер для использования при подключении. По умолчанию `None`.

    Returns:
        None

    Как работает функция:
    - Запускает бесконечный цикл, в котором пытается обновить cookies.
    - Вызывает функцию `rotate_1psidts` для обновления cookies.
    - В случае ошибки логирует ошибку и отменяет задачу обновления cookies.
    - Сохраняет новые cookies в атрибуте `_cookies` класса.
    - Засыпает на интервал `refresh_interval` секунд.

    Примеры:
        >>> asyncio.create_task(Gemini.start_auto_refresh())
    """
    ...

#### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    cookies: Cookies = None,
    connector: BaseConnector = None,
    media: MediaListType = None,
    return_conversation: bool = False,
    conversation: Conversation = None,
    language: str = "en",
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для отправки запросов и получения ответов от модели Gemini.

    Args:
        model (str): Имя используемой модели Gemini.
        messages (Messages): Список сообщений для отправки в модель.
        proxy (str, optional): Прокси-сервер для использования при подключении. По умолчанию `None`.
        cookies (Cookies, optional): Cookies для аутентификации. По умолчанию `None`.
        connector (BaseConnector, optional):  aiohttp коннектор для переиспользования соединений. По умолчанию `None`.
        media (MediaListType, optional):  Список медиафайлов для отправки. По умолчанию `None`.
        return_conversation (bool, optional):  Возвращать ли объект Conversation. По умолчанию `False`.
        conversation (Conversation, optional): Объект Conversation для продолжения разговора. По умолчанию `None`.
        language (str, optional): Язык ответа. По умолчанию "en".
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий ответы от модели Gemini.

    Raises:
        MissingAuthError: Если отсутствует или недействителен cookie "__Secure-1PSID".
        RuntimeError: Если не удалось получить SNlM0e.

    Как работает функция:
    - Инициализирует cookies и параметр SNlM0e.
    - Форматирует запрос на основе переданных сообщений и параметров.
    - Отправляет запрос в API Gemini и получает ответ.
    - Обрабатывает ответ и извлекает текст, изображения и другие данные.
    - Возвращает асинхронный генератор, который возвращает части ответа.

    Примеры:
        >>> async for chunk in Gemini.create_async_generator(model="gemini-2.0", messages=[{"role": "user", "content": "Hello"}]):
        ...     print(chunk)
    """
    ...

#### `synthesize`

```python
@classmethod
async def synthesize(cls, params: dict, proxy: str = None) -> AsyncIterator[bytes]:
    """
    Синтезирует речь на основе переданного текста.

    Args:
        params (dict): Словарь параметров, содержащий текст для синтеза.
        proxy (str, optional): Прокси-сервер для использования при подключении. По умолчанию `None`.

    Returns:
        AsyncIterator[bytes]: Асинхронный итератор, возвращающий байты с синтезированной речью.

    Raises:
        ValueError: Если отсутствует параметр "text" в словаре `params`.

    Как работает функция:
    - Проверяет наличие параметра "text" в словаре `params`.
    - Отправляет запрос в API Gemini для синтеза речи.
    - Получает ответ в формате base64 и декодирует его.
    - Возвращает асинхронный итератор, который возвращает байты с синтезированной речью.

    Примеры:
        >>> async for chunk in Gemini.synthesize(params={"text": "Hello"}):
        ...     print(chunk)
    """
    ...

#### `build_request`

```python
def build_request(
    prompt: str,
    language: str,
    conversation: Conversation = None,
    uploads: list[list[str, str]] = None,
    tools: list[list[str]] = []
) -> list:
    """
    Строит запрос для отправки в API Gemini.

    Args:
        prompt (str): Текст запроса.
        language (str): Язык запроса.
        conversation (Conversation, optional): Объект Conversation для продолжения разговора. По умолчанию `None`.
        uploads (list[list[str, str]], optional): Список загруженных изображений. По умолчанию `None`.
        tools (list[list[str]], optional): Список инструментов для использования. По умолчанию [].

    Returns:
        list: Список, представляющий запрос для API Gemini.

    Как работает функция:
    - Форматирует запрос на основе переданных параметров.
    - Включает информацию о тексте запроса, языке, истории разговора и загруженных изображениях.
    - Возвращает список, который может быть отправлен в API Gemini.

    Примеры:
        >>> request = Gemini.build_request(prompt="Hello", language="en")
        >>> print(request)
    """
    ...

#### `upload_images`

```python
async def upload_images(connector: BaseConnector, media: MediaListType) -> list:
    """
    Загружает изображения в API Gemini.

    Args:
        connector (BaseConnector): aiohttp коннектор для переиспользования соединений.
        media (MediaListType): Список медиафайлов для загрузки.

    Returns:
        list: Список URL загруженных изображений.

    Как работает функция:
    - Загружает каждое изображение в API Gemini.
    - Возвращает список URL загруженных изображений.

    Примеры:
        >>> urls = await Gemini.upload_images(connector, [("image.jpg", b"...")])
        >>> print(urls)
    """
    ...

Внутренняя функция upload_image(image: bytes, image_name: str = None)

```python
        async def upload_image(image: bytes, image_name: str = None):
            """
            Загружает одно изображение в API Gemini.
        
            Args:
                image (bytes):  Изображение в формате байтов.
                image_name (str, optional): Имя изображения. По умолчанию `None`.
        
            Returns:
                list: Список, содержащий URL загруженного изображения и имя изображения.
        
            Как работает функция:
                - Отправляет изображение в API Gemini.
                - Возвращает URL загруженного изображения.
            """
            ...

#### `fetch_snlm0e`

```python
@classmethod
async def fetch_snlm0e(cls, session: ClientSession, cookies: Cookies):
    """
    Извлекает значение параметра SNlM0e из ответа сервера.

    Args:
        session (ClientSession):  aiohttp сессия для выполнения запроса.
        cookies (Cookies): Cookies для аутентификации.

    Returns:
        None

    Как работает функция:
    - Отправляет GET-запрос на URL Gemini с переданными cookies.
    - Извлекает значение параметра SNlM0e из ответа.
    - Сохраняет значение параметра SNlM0e в атрибуте `_snlm0e` класса.

    Примеры:
        >>> await Gemini.fetch_snlm0e(session, {"__Secure-1PSID": "..."})
    """
    ...

## Функции

### `iter_filter_base64`

```python
async def iter_filter_base64(chunks: AsyncIterator[bytes]) -> AsyncIterator[bytes]:
    """
    Фильтрует base64 чанки из потока байтов.

    Args:
        chunks (AsyncIterator[bytes]): Асинхронный итератор байтов.

    Returns:
        AsyncIterator[bytes]: Асинхронный итератор отфильтрованных байтов.

    Raises:
        ValueError: Если ответ не содержит ожидаемые маркеры начала.

    Как работает функция:
    - Ищет начальный маркер `[["wrb.fr","XqA3Ic","[\\\\"`.
    - Удаляет все байты до маркера.
    - Передает только те байты, которые находятся между маркерами начала и конца (`\\\\`).

    Примеры:
        >>> async for chunk in iter_filter_base64(chunks):
        ...     print(chunk)
    """
    ...

### `iter_base64_decode`

```python
async def iter_base64_decode(chunks: AsyncIterator[bytes]) -> AsyncIterator[bytes]:
    """
    Декодирует base64 чанки из потока байтов.

    Args:
        chunks (AsyncIterator[bytes]): Асинхронный итератор байтов.

    Returns:
        AsyncIterator[bytes]: Асинхронный итератор декодированных байтов.

    Как работает функция:
    - Буферизует байты, пока не накопится полный base64 блок.
    - Декодирует base64 блок и передает декодированные байты.

    Примеры:
        >>> async for chunk in iter_base64_decode(chunks):
        ...     print(chunk)
    """
    ...

### `rotate_1psidts`

```python
async def rotate_1psidts(url, cookies: dict, proxy: str | None = None) -> str:
    """
    Обновляет cookie __Secure-1PSIDTS.

    Args:
        url (str): URL для обновления cookie.
        cookies (dict): Словарь cookies.
        proxy (str, optional): Прокси-сервер для использования при подключении. По умолчанию `None`.

    Returns:
        str: Новое значение cookie __Secure-1PSIDTS.

    Raises:
        MissingAuthError: Если cookies недействительны.
        HTTPError: Если произошла ошибка при выполнении запроса.

    Как работает функция:
    - Отправляет POST-запрос на URL для обновления cookie.
    - Обновляет cookie в словаре `cookies`.
    - Возвращает новое значение cookie __Secure-1PSIDTS.

    Примеры:
        >>> new_1psidts = await rotate_1psidts(url, cookies)
        >>> print(new_1psidts)
    """
    ...