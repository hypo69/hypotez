# Модуль Gemini для работы с Google Gemini
## Обзор

Модуль `Gemini.py` предназначен для взаимодействия с сервисом Google Gemini. Он предоставляет асинхронные методы для генерации текста, обработки изображений и выполнения других задач с использованием API Google Gemini. Модуль поддерживает автоматическое обновление куки, работу через прокси и загрузку изображений.

## Подробнее

Этот модуль является частью проекта `hypotez` и отвечает за интеграцию с Google Gemini. Он использует асинхронные запросы для взаимодействия с API Gemini, обеспечивая неблокирующие операции. Модуль также включает механизмы для управления куками и автоматического обновления для поддержания сессии с сервисом.

## Классы

### `Gemini`

**Описание**: Основной класс для взаимодействия с Google Gemini.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет функциональность для работы с разными моделями.

**Атрибуты**:
- `label` (str): Метка провайдера ("Google Gemini").
- `url` (str): URL сервиса Google Gemini ("https://gemini.google.com").
- `needs_auth` (bool): Требуется ли аутентификация (True).
- `working` (bool): Показывает, работает ли провайдер (True).
- `use_nodriver` (bool): Использовать ли nodriver (True).
- `default_model` (str): Модель по умолчанию ("").
- `default_image_model` (str): Модель для обработки изображений по умолчанию ("").
- `default_vision_model` (str): Модель для обработки видео по умолчанию ("").
- `image_models` (list): Список поддерживаемых моделей для изображений.
- `models` (list): Список поддерживаемых моделей.
- `model_aliases` (dict): Псевдонимы моделей.
- `synthesize_content_type` (str): Тип контента для синтеза ("audio/vnd.wav").
- `_cookies` (Cookies): Куки для аутентификации.
- `_snlm0e` (str): Токен `SNlM0e`, необходимый для запросов.
- `_sid` (str): Идентификатор сессии.
- `auto_refresh` (bool): Автоматическое обновление куки (True).
- `refresh_interval` (int): Интервал обновления куки (540 секунд).
- `rotate_tasks` (dict): Задачи для ротации куки.

**Методы**:
- `nodriver_login(proxy: str = None)`: Асинхронный метод для входа в систему с использованием nodriver.
- `start_auto_refresh(proxy: str = None)`: Запускает фоновую задачу для автоматического обновления куки.
- `create_async_generator(model: str, messages: Messages, proxy: str = None, cookies: Cookies = None, connector: BaseConnector = None, media: MediaListType = None, return_conversation: bool = False, conversation: Conversation = None, language: str = "en", **kwargs)`: Создает асинхронный генератор для взаимодействия с Gemini.
- `synthesize(params: dict, proxy: str = None)`: Асинхронный метод для синтеза речи.
- `build_request(prompt: str, language: str, conversation: Conversation = None, uploads: list[list[str, str]] = None, tools: list[list[str]] = [])`: Создает запрос к Gemini.
- `upload_images(connector: BaseConnector, media: MediaListType)`: Загружает изображения в Gemini.
- `fetch_snlm0e(session: ClientSession, cookies: Cookies)`: Извлекает токен `SNlM0e` из куки.

### `Conversation`

**Описание**: Класс для хранения информации о контексте разговора.

**Наследует**:
- `JsonConversation`: Базовый класс для хранения контекста в формате JSON.

**Атрибуты**:
- `conversation_id` (str): Идентификатор разговора.
- `response_id` (str): Идентификатор ответа.
- `choice_id` (str): Идентификатор выбора.
- `model` (str): Используемая модель.

## Функции

### `nodriver_login`

```python
    @classmethod
    async def nodriver_login(cls, proxy: str = None) -> AsyncIterator[str]:
        """
        Асинхронный метод для входа в систему с использованием nodriver.

        Args:
            proxy (str, optional): Прокси для подключения. По умолчанию `None`.

        Yields:
            AsyncIterator[str]: Асинхронный итератор строк, содержащий информацию о процессе входа.

        Raises:
            ImportError: Если модуль `nodriver` не установлен.

        Как работает функция:
        1. Проверяет, установлен ли модуль `nodriver`. Если нет, то функция завершается.
        2. Получает инстанс браузера и функцию остановки браузера с помощью `get_nodriver`.
        3. Пытается получить URL для входа из переменной окружения `G4F_LOGIN_URL` и возвращает его через `yield`.
        4. Открывает страницу `f"{cls.url}/app"` в браузере.
        5. Выбирает элемент `div.ql-editor.textarea` на странице.
        6. Получает куки из браузера.
        7. Закрывает страницу.
        8. Сохраняет куки в атрибут класса `_cookies`.
        9. Останавливает браузер.

        ASCII flowchart:

        Проверка has_nodriver
        |
        Получение browser, stop_browser
        |
        Получение login_url из env
        |
        Открытие страницы в браузере
        |
        Получение cookies
        |
        Закрытие страницы, остановка браузера

        Примеры:
            >>> async for chunk in Gemini.nodriver_login():
            ...     print(chunk)
        """
```

### `start_auto_refresh`

```python
    @classmethod
    async def start_auto_refresh(cls, proxy: str = None) -> None:
        """
        Запускает фоновую задачу для автоматического обновления куки.

        Args:
            proxy (str, optional): Прокси для подключения. По умолчанию `None`.

        Как работает функция:
        1. Бесконечный цикл, который пытается обновить куки с помощью `rotate_1psidts`.
        2. Если обновление куки завершается успешно, то обновляет значение `__Secure-1PSIDTS` в атрибуте класса `_cookies`.
        3. Если обновление куки не удается, то логирует ошибку и отменяет задачу ротации куки.
        4. Засыпает на `cls.refresh_interval` секунд.

        ASCII flowchart:

        Бесконечный цикл
        |
        Обновление куки
        |
        Обновление __Secure-1PSIDTS
        |
        Обработка ошибок
        |
        Сон

        Примеры:
            >>> asyncio.create_task(Gemini.start_auto_refresh())
        """
```

### `create_async_generator`

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
        Создает асинхронный генератор для взаимодействия с Gemini.

        Args:
            model (str): Используемая модель.
            messages (Messages): Список сообщений для отправки.
            proxy (str, optional): Прокси для подключения. По умолчанию `None`.
            cookies (Cookies, optional): Куки для аутентификации. По умолчанию `None`.
            connector (BaseConnector, optional): Коннектор для HTTP-сессии. По умолчанию `None`.
            media (MediaListType, optional): Список медиафайлов для отправки. По умолчанию `None`.
            return_conversation (bool, optional): Возвращать ли контекст разговора. По умолчанию `False`.
            conversation (Conversation, optional): Объект разговора. По умолчанию `None`.
            language (str, optional): Язык. По умолчанию "en".
            **kwargs: Дополнительные аргументы.

        Yields:
            AsyncResult: Асинхронный результат генерации.

        Raises:
            MissingAuthError: Если отсутствует или недействителен cookie "__Secure-1PSID".
            RuntimeError: Если не удалось получить SNlM0e.

        Как работает функция:
        1. Инициализирует куки, если они не были переданы.
        2. Форматирует запрос на основе переданных сообщений и контекста разговора.
        3. Создает асинхронную сессию `ClientSession`.
        4. Проверяет наличие токена `_snlm0e` и, если его нет, пытается получить его с помощью `fetch_snlm0e` или `nodriver_login`.
        5. Загружает изображения с помощью `upload_images`.
        6. Отправляет POST-запрос к API Gemini и обрабатывает ответ.
        7. Извлекает контент из ответа и возвращает его через `yield`.
        8. Обрабатывает ошибки и логирует их.

        ASCII flowchart:

        Инициализация куки
        |
        Форматирование запроса
        |
        Создание ClientSession
        |
        Проверка _snlm0e
        |
        Загрузка изображений
        |
        Отправка POST-запроса
        |
        Обработка ответа
        |
        Извлечение контента
        |
        Обработка ошибок

        Примеры:
            >>> async for chunk in Gemini.create_async_generator(model="gemini-2.0", messages=[{"role": "user", "content": "Hello"}], cookies=cookies):
            ...     print(chunk)
        """
```

### `synthesize`

```python
    @classmethod
    async def synthesize(cls, params: dict, proxy: str = None) -> AsyncIterator[bytes]:
        """
        Асинхронный метод для синтеза речи.

        Args:
            params (dict): Параметры для синтеза речи, включая текст.
            proxy (str, optional): Прокси для подключения. По умолчанию `None`.

        Yields:
            AsyncIterator[bytes]: Асинхронный итератор байтов, представляющих аудио.

        Raises:
            ValueError: Если отсутствует параметр "text".

        Как работает функция:
        1. Проверяет наличие параметра "text" в переданных параметрах.
        2. Создает асинхронную сессию `ClientSession`.
        3. Проверяет наличие токена `_snlm0e` и, если его нет, пытается получить его с помощью `fetch_snlm0e`.
        4. Формирует данные для запроса и отправляет POST-запрос к API Gemini.
        5. Обрабатывает ответ, декодирует base64 и возвращает аудио через `yield`.
        
        ASCII flowchart:

        Проверка параметра "text"
        |
        Создание ClientSession
        |
        Проверка _snlm0e
        |
        Формирование данных запроса
        |
        Отправка POST-запроса
        |
        Декодирование base64
        |
        Возврат аудио
        
        Примеры:
            >>> async for chunk in Gemini.synthesize(params={"text": "Hello"}, cookies=cookies):
            ...     print(chunk)
        """
```

### `build_request`

```python
    def build_request(
        prompt: str,
        language: str,
        conversation: Conversation = None,
        uploads: list[list[str, str]] = None,
        tools: list[list[str]] = []
    ) -> list:
        """
        Создает запрос к Gemini.

        Args:
            prompt (str): Текст запроса.
            language (str): Язык запроса.
            conversation (Conversation, optional): Объект разговора. По умолчанию `None`.
            uploads (list[list[str, str]], optional): Список загруженных изображений. По умолчанию `None`.
            tools (list[list[str]], optional): Список инструментов. По умолчанию `None`.

        Returns:
            list: Сформированный запрос для Gemini.

        Как работает функция:
        1. Формирует список изображений для загрузки.
        2. Создает структуру запроса, включающую текст запроса, язык, контекст разговора, загруженные изображения и инструменты.

        ASCII flowchart:

        Формирование списка изображений
        |
        Создание структуры запроса

        Примеры:
            >>> request = Gemini.build_request(prompt="Hello", language="en")
        """
```

### `upload_images`

```python
    async def upload_images(connector: BaseConnector, media: MediaListType) -> list:
        """
        Загружает изображения в Gemini.

        Args:
            connector (BaseConnector): Коннектор для HTTP-сессии.
            media (MediaListType): Список медиафайлов для загрузки.

        Returns:
            list: Список URL загруженных изображений.

        Как работает функция:
        1. Определяет асинхронную функцию `upload_image` для загрузки одного изображения.
        2. Функция `upload_image` создает сессию `ClientSession` и отправляет запросы для загрузки изображения.
        3. Использует `asyncio.gather` для параллельной загрузки всех изображений.

        ASCII flowchart:

        Для каждого изображения:
            Создание ClientSession
            |
            Отправка запросов для загрузки
        |
        Сбор результатов

        Примеры:
            >>> urls = await Gemini.upload_images(connector, media=[("image.jpg", b"...")])
        """
```

### `fetch_snlm0e`

```python
    @classmethod
    async def fetch_snlm0e(cls, session: ClientSession, cookies: Cookies):
        """
        Извлекает токен `SNlM0e` из куки.

        Args:
            session (ClientSession): Асинхронная сессия.
            cookies (Cookies): Куки для запроса.

        Как работает функция:
        1. Отправляет GET-запрос к URL Gemini.
        2. Извлекает токен `SNlM0e` из ответа с помощью регулярного выражения.
        3. Извлекает `sid` из ответа с помощью регулярного выражения.
        4. Сохраняет токен в атрибуте класса `_snlm0e`.

        ASCII flowchart:

        Отправка GET-запроса
        |
        Извлечение SNlM0e из ответа
        |
        Сохранение токена

        Примеры:
            >>> await Gemini.fetch_snlm0e(session, cookies)
        """
```

### `Conversation.__init__`

```python
    def __init__(self,
        conversation_id: str,
        response_id: str,
        choice_id: str,
        model: str
    ) -> None:
        """
        Инициализирует объект Conversation.

        Args:
            conversation_id (str): Идентификатор разговора.
            response_id (str): Идентификатор ответа.
            choice_id (str): Идентификатор выбора.
            model (str): Используемая модель.
        """
```

### `iter_filter_base64`

```python
async def iter_filter_base64(chunks: AsyncIterator[bytes]) -> AsyncIterator[bytes]:
    """
    Фильтрует base64 чанки из асинхронного итератора байтов.

    Args:
        chunks (AsyncIterator[bytes]): Асинхронный итератор байтов.

    Yields:
        AsyncIterator[bytes]: Отфильтрованный асинхронный итератор байтов.

    Raises:
        ValueError: Если ответ не содержит ожидаемый формат.

    Как работает функция:
    1. Ищет стартовую последовательность `[["wrb.fr","XqA3Ic","[\\\\"`.
    2. После нахождения стартовой последовательности, ищет окончание `\\\\`.
    3. Возвращает чанки между стартовой и конечной последовательностями.

    ASCII flowchart:

    Поиск стартовой последовательности
    |
    Поиск конечной последовательности
    |
    Возврат чанков

    Примеры:
        >>> async for chunk in iter_filter_base64(chunks):
        ...     print(chunk)
    """
```

### `iter_base64_decode`

```python
async def iter_base64_decode(chunks: AsyncIterator[bytes]) -> AsyncIterator[bytes]:
    """
    Декодирует base64 чанки из асинхронного итератора байтов.

    Args:
        chunks (AsyncIterator[bytes]): Асинхронный итератор байтов.

    Yields:
        AsyncIterator[bytes]: Декодированный асинхронный итератор байтов.

    Как работает функция:
    1. Буферизует чанки.
    2. Выполняет base64 декодирование.
    3. Возвращает декодированные чанки.

    ASCII flowchart:

    Буферизация чанков
    |
    Декодирование base64
    |
    Возврат декодированных чанков

    Примеры:
        >>> async for chunk in iter_base64_decode(chunks):
        ...     print(chunk)
    """
```

### `rotate_1psidts`

```python
async def rotate_1psidts(url, cookies: dict, proxy: str | None = None) -> str:
    """
    Обновляет куки `__Secure-1PSIDTS`.

    Args:
        url (str): URL для обновления куки.
        cookies (dict): Текущие куки.
        proxy (str | None, optional): Прокси для подключения. По умолчанию `None`.

    Returns:
        str: Новое значение `__Secure-1PSIDTS`.

    Raises:
        MissingAuthError: Если куки недействительны.

    Как работает функция:
    1. Формирует путь к файлу, где хранятся куки.
    2. Проверяет, не был ли файл изменен в течение последней минуты, чтобы избежать `429 Too Many Requests`.
    3. Отправляет POST-запрос к `ROTATE_COOKIES_URL` для обновления куки.
    4. Обновляет куки в переданном словаре.
    5. Сохраняет новые куки в файл.
    6. Возвращает новое значение `__Secure-1PSIDTS`.

    ASCII flowchart:

    Формирование пути к файлу
    |
    Проверка времени изменения файла
    |
    Отправка POST-запроса
    |
    Обновление куки
    |
    Сохранение куки в файл
    |
    Возврат нового значения __Secure-1PSIDTS

    Примеры:
        >>> new_1psidts = await rotate_1psidts(url, cookies)
    """