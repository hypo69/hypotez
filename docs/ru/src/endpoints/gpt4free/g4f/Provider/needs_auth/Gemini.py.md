# Модуль `Gemini.py`

## Обзор

Модуль `Gemini.py` предоставляет асинхронный интерфейс для взаимодействия с моделями Google Gemini, включая функциональность для входа в систему через nodriver, автоматическое обновление cookies и загрузку изображений. Модуль поддерживает различные модели Gemini и предоставляет методы для синтеза речи и создания запросов.

## Подробнее

Этот модуль является частью проекта `hypotez` и предназначен для интеграции с моделями Google Gemini. Он использует асинхронные запросы для обеспечения неблокирующего взаимодействия с API Gemini. Модуль также включает механизмы для обработки cookies, что необходимо для аутентификации и поддержания сессии с серверами Google.

## Классы

### `Gemini`

**Описание**:
Класс `Gemini` предоставляет асинхронный генератор для взаимодействия с моделями Google Gemini. Он наследует функциональность от `AsyncGeneratorProvider` и `ProviderModelMixin`.

**Наследует**:

- `AsyncGeneratorProvider`: Обеспечивает базовую структуру для асинхронных генераторов.
- `ProviderModelMixin`: Предоставляет методы для работы с моделями.

**Атрибуты**:

- `label` (str): Метка провайдера, `"Google Gemini"`.
- `url` (str): URL для доступа к Gemini, `"https://gemini.google.com"`.
- `needs_auth` (bool): Указывает, требуется ли аутентификация, `True`.
- `working` (bool): Указывает, работает ли провайдер, `True`.
- `use_nodriver` (bool): Указывает, используется ли nodriver для входа, `True`.
- `default_model` (str): Модель по умолчанию, `""`.
- `default_image_model` (str): Модель для изображений по умолчанию, `""`.
- `default_vision_model` (str): Модель для vision по умолчанию, `""`.
- `image_models` (list[str]): Список поддерживаемых моделей для изображений.
- `models` (list[str]): Список поддерживаемых моделей.
- `model_aliases` (dict[str, str]): Алиасы моделей, `{"gemini-2.0": ""}`.
- `synthesize_content_type` (str): Тип контента для синтеза речи, `"audio/vnd.wav"`.
- `_cookies` (Cookies): Cookies для аутентификации, `None`.
- `_snlm0e` (str): Токен для аутентификации, `None`.
- `_sid` (str): Идентификатор сессии, `None`.
- `auto_refresh` (bool): Автоматическое обновление cookies, `True`.
- `refresh_interval` (int): Интервал обновления cookies в секундах, `540`.
- `rotate_tasks` (dict): Словарь задач для ротации cookies.

**Принцип работы**:
Класс `Gemini` использует асинхронные методы для отправки запросов к серверам Google Gemini. Он управляет cookies для аутентификации, автоматически обновляя их при необходимости. Класс также предоставляет методы для загрузки изображений и синтеза речи.

**Методы**:

- `nodriver_login(proxy: str = None) -> AsyncIterator[str]`
- `start_auto_refresh(proxy: str = None) -> None`
- `create_async_generator(model: str, messages: Messages, proxy: str = None, cookies: Cookies = None, connector: BaseConnector = None, media: MediaListType = None, return_conversation: bool = False, conversation: Conversation = None, language: str = "en", **kwargs) -> AsyncResult`
- `synthesize(params: dict, proxy: str = None) -> AsyncIterator[bytes]`
- `build_request(prompt: str, language: str, conversation: Conversation = None, uploads: list[list[str, str]] = None, tools: list[list[str]] = []) -> list`
- `upload_images(connector: BaseConnector, media: MediaListType) -> list`
- `fetch_snlm0e(session: ClientSession, cookies: Cookies)`

### `Conversation`

**Описание**:
Класс `Conversation` представляет собой структуру данных для хранения информации о разговоре с моделью Gemini.

**Наследует**:

- `JsonConversation`: базовый класс для представления истории разговора в формате JSON.

**Атрибуты**:

- `conversation_id` (str): Идентификатор разговора.
- `response_id` (str): Идентификатор ответа.
- `choice_id` (str): Идентификатор выбора.
- `model` (str): Используемая модель.

**Принцип работы**:
Класс используется для хранения и передачи контекста разговора между запросами к API Gemini.

## Методы класса `Gemini`

### `nodriver_login`

```python
    @classmethod
    async def nodriver_login(cls, proxy: str = None) -> AsyncIterator[str]:
        """
        Асинхронный метод для входа в систему Gemini с использованием nodriver.

        Args:
            proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.

        Yields:
            AsyncIterator[str]: Асинхронный итератор строк, содержащий URL для входа.

        Raises:
            ImportError: Если модуль `nodriver` не установлен.

        
        - Проверяется, установлен ли модуль `nodriver`. Если нет, функция завершается.
        - Запускается браузер с использованием `get_nodriver`.
        - Если определен `G4F_LOGIN_URL` в переменных окружения, возвращается URL для входа.
        - Открывается страница Gemini в браузере.
        - Выбирается элемент `div.ql-editor.textarea` на странице.
        - Извлекаются cookies из браузера.
        - Закрывается страница браузера.
        - Сохраненные cookies присваиваются атрибуту `_cookies` класса.
        - Останавливается браузер.
        """
```

### `start_auto_refresh`

```python
    @classmethod
    async def start_auto_refresh(cls, proxy: str = None) -> None:
        """
        Запускает фоновую задачу для автоматического обновления cookies.

        Args:
            proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.

        Raises:
            Exception: Если не удается обновить cookies.

        
        - В бесконечном цикле пытается обновить cookies с использованием функции `rotate_1psidts`.
        - В случае ошибки логирует информацию об ошибке и отменяет задачу обновления cookies.
        - После успешного обновления сохраняет новый `__Secure-1PSIDTS` в атрибуте `_cookies` класса.
        - Засыпает на интервал, определенный в `cls.refresh_interval`.
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
        Создает асинхронный генератор для взаимодействия с моделью Gemini.

        Args:
            model (str): Используемая модель.
            messages (Messages): Список сообщений для отправки.
            proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
            cookies (Cookies, optional): Cookies для аутентификации. По умолчанию `None`.
            connector (BaseConnector, optional): Aiohttp connector. По умолчанию `None`.
            media (MediaListType, optional): Список медиафайлов для отправки. По умолчанию `None`.
            return_conversation (bool, optional): Возвращать ли объект Conversation. По умолчанию `False`.
            conversation (Conversation, optional): Объект Conversation. По умолчанию `None`.
            language (str, optional): Язык ответа. По умолчанию "en".
            **kwargs: Дополнительные аргументы.

        Yields:
            AsyncResult: Асинхронный результат ответа от модели.

        Raises:
            MissingAuthError: Если отсутствуют или недействительны cookies.
            RuntimeError: Если не найден токен SNlM0e.

        
        - Инициализирует cookies из переданных аргументов или из сохраненных значений.
        - Форматирует промпт из переданных сообщений.
        - Создает сессию aiohttp с необходимыми заголовками и cookies.
        - Получает токен SNlM0e, если он еще не получен.
        - Загружает изображения, если они есть в списке медиафайлов.
        - Отправляет POST-запрос к API Gemini с необходимыми данными и параметрами.
        - Обрабатывает ответ от API и извлекает контент, reasoning и изображения.
        - Возвращает асинхронный генератор, который выдает части ответа от модели.
        """
```

### `synthesize`

```python
    @classmethod
    async def synthesize(cls, params: dict, proxy: str = None) -> AsyncIterator[bytes]:
        """
        Синтезирует речь на основе переданного текста.

        Args:
            params (dict): Параметры для синтеза речи, включая текст.
            proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.

        Yields:
            AsyncIterator[bytes]: Асинхронный итератор байтов, представляющих аудио.

        Raises:
            ValueError: Если отсутствует параметр "text".

        
        - Проверяет наличие параметра "text" в переданных параметрах.
        - Создает сессию aiohttp с необходимыми заголовками и cookies.
        - Получает токен SNlM0e, если он еще не получен.
        - Отправляет POST-запрос к API Gemini для синтеза речи.
        - Обрабатывает ответ и возвращает асинхронный итератор байтов, представляющих аудио.
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
        Строит запрос для отправки в API Gemini.

        Args:
            prompt (str): Текст запроса.
            language (str): Язык запроса.
            conversation (Conversation, optional): Объект Conversation. По умолчанию `None`.
            uploads (list[list[str, str]], optional): Список загруженных изображений. По умолчанию `None`.
            tools (list[list[str]], optional): Список инструментов. По умолчанию `[]`.

        Returns:
            list: Список, представляющий запрос для API Gemini.

        
        - Формирует структуру данных запроса на основе переданных аргументов.
        - Включает текст запроса, язык, информацию о разговоре, загруженные изображения и инструменты.
        - Возвращает список, который может быть сериализован в JSON и отправлен в API Gemini.
        """
```

### `upload_images`

```python
    async def upload_images(connector: BaseConnector, media: MediaListType) -> list:
        """
        Загружает изображения на сервер Gemini.

        Args:
            connector (BaseConnector): Aiohttp connector.
            media (MediaListType): Список медиафайлов для загрузки.

        Returns:
            list: Список URL загруженных изображений и их имен.

        
        - Для каждого изображения в списке медиафайлов выполняет следующие действия:
        - Создает сессию aiohttp с необходимыми заголовками.
        - Преобразует изображение в байты.
        - Отправляет OPTIONS-запрос для получения URL загрузки.
        - Отправляет POST-запрос для начала загрузки.
        - Отправляет POST-запрос для завершения загрузки.
        - Возвращает список URL загруженных изображений и их имен.
        """
```

### `fetch_snlm0e`

```python
    @classmethod
    async def fetch_snlm0e(cls, session: ClientSession, cookies: Cookies):
        """
        Получает токен SNlM0e из ответа сервера Gemini.

        Args:
            session (ClientSession): Aiohttp сессия.
            cookies (Cookies): Cookies для аутентификации.

        
        - Отправляет GET-запрос к URL Gemini с переданными cookies.
        - Извлекает текст ответа.
        - Ищет токен SNlM0e в тексте ответа с помощью регулярного выражения.
        - Сохраняет токен SNlM0e в атрибуте `_snlm0e` класса.
        - Ищет идентификатор сессии `FdrFJe` и сохраняет его в атрибуте `_sid` класса.
        """
```

## Методы класса `Conversation`

### `__init__`

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
        self.conversation_id = conversation_id
        self.response_id = response_id
        self.choice_id = choice_id
        self.model = model
```

## Функции

### `iter_filter_base64`

```python
async def iter_filter_base64(chunks: AsyncIterator[bytes]) -> AsyncIterator[bytes]:
    """
    Фильтрует base64 данные из асинхронного итератора байтов.

    Args:
        chunks (AsyncIterator[bytes]): Асинхронный итератор байтов.

    Yields:
        AsyncIterator[bytes]: Отфильтрованный асинхронный итератор байтов.

    Raises:
        ValueError: Если ответ не содержит ожидаемые данные.

    
    - Ищет начало base64 данных в каждом чанке.
    - Если начало найдено, возвращает данные после начала.
    - Если конец найден, возвращает данные до конца и завершает итерацию.
    """
```

### `iter_base64_decode`

```python
async def iter_base64_decode(chunks: AsyncIterator[bytes]) -> AsyncIterator[bytes]:
    """
    Декодирует base64 данные из асинхронного итератора байтов.

    Args:
        chunks (AsyncIterator[bytes]): Асинхронный итератор байтов.

    Yields:
        AsyncIterator[bytes]: Декодированный асинхронный итератор байтов.

    
    - Накапливает чанки в буфере.
    - Декодирует base64 данные из буфера и возвращает их.
    """
```

### `rotate_1psidts`

```python
async def rotate_1psidts(url, cookies: dict, proxy: str | None = None) -> str:
    """
    Обновляет cookie "__Secure-1PSIDTS".

    Args:
        url (str): URL для обновления cookies.
        cookies (dict): Текущие cookies.
        proxy (str | None, optional): Прокси-сервер для использования. По умолчанию `None`.

    Returns:
        str: Новое значение cookie "__Secure-1PSIDTS".

    Raises:
        MissingAuthError: Если cookies недействительны.

    
    - Проверяет, был ли файл кэша изменен в течение последней минуты, чтобы избежать 429 Too Many Requests.
    - Отправляет POST-запрос к `ROTATE_COOKIES_URL` для обновления cookies.
    - Если ответ содержит ошибку аутентификации, вызывает исключение `MissingAuthError`.
    - Обновляет cookies в переданном словаре `cookies`.
    - Возвращает новое значение cookie "__Secure-1PSIDTS".
    """