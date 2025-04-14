# Модуль HuggingChat

## Обзор

Модуль `HuggingChat.py` предоставляет класс `HuggingChat`, который обеспечивает асинхронное взаимодействие с сервисом Hugging Face Chat. Он поддерживает как текстовые, так и мультимодальные модели, требующие аутентификации. Модуль использует библиотеку `curl_cffi` для выполнения HTTP-запросов.

## Подробней

Модуль предназначен для интеграции с сервисом Hugging Face Chat, позволяя отправлять запросы к различным моделям, включая те, которые поддерживают обработку изображений. Он обеспечивает создание и поддержание контекста разговора, а также обработку ответов в реальном времени. В проекте `hypotez` этот модуль используется для предоставления доступа к моделям Hugging Face через интерфейс g4f.

## Классы

### `Conversation`

**Описание**: Класс `Conversation` предназначен для хранения информации о текущем разговоре с моделью.

**Наследует**: `JsonConversation`

**Атрибуты**:

-   `models` (dict): Словарь, содержащий информацию о моделях, используемых в разговоре.

**Методы**:

-   `__init__(self, models: dict)`: Инициализирует объект разговора с заданным словарем моделей.

### `HuggingChat`

**Описание**: Класс `HuggingChat` предоставляет функциональность для взаимодействия с сервисом Hugging Face Chat.

**Наследует**: `AsyncAuthedProvider`, `ProviderModelMixin`

**Атрибуты**:

-   `domain` (str): Доменное имя сервиса Hugging Face Chat (`"huggingface.co"`).
-   `origin` (str): Полный URL сервиса Hugging Face Chat (`"https://huggingface.co"`).
-   `url` (str): URL для чата (`"https://huggingface.co/chat"`).
-   `working` (bool): Флаг, указывающий на работоспособность провайдера (всегда `True`).
-   `use_nodriver` (bool): Флаг, указывающий на использование без драйвера (всегда `True`).
-   `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи данных (всегда `True`).
-   `needs_auth` (bool): Флаг, указывающий на необходимость аутентификации (всегда `True`).
-   `default_model` (str): Модель, используемая по умолчанию.
-   `default_vision_model` (str): Модель для обработки изображений, используемая по умолчанию.
-   `model_aliases` (dict): Словарь псевдонимов моделей.
-   `image_models` (list): Список моделей, поддерживающих обработку изображений.
-   `text_models` (list): Список моделей, поддерживающих обработку текста.

**Методы**:

-   `get_models()`: Получает список доступных моделей из сервиса Hugging Face Chat.
-   `on_auth_async(cookies: Cookies = None, proxy: str = None, **kwargs) -> AsyncIterator`: Выполняет асинхронную аутентификацию пользователя.
-   `create_authed(model: str, messages: Messages, auth_result: AuthResult, prompt: str = None, media: MediaListType = None, return_conversation: bool = False, conversation: Conversation = None, web_search: bool = False, **kwargs) -> AsyncResult`: Создает аутентифицированный запрос к сервису Hugging Face Chat.
-   `create_conversation(session: Session, model: str)`: Создает новый контекст разговора.
-   `fetch_message_id(session: Session, conversation_id: str)`: Извлекает идентификатор последнего сообщения в контексте разговора.

## Функции

### `get_models`

```python
    @classmethod
    def get_models(cls):
        """
        Получает список доступных моделей из сервиса Hugging Face Chat.

        Args:
            cls: Ссылка на класс.

        Returns:
            list: Список доступных моделей.

        Raises:
            Exception: Если возникает ошибка при чтении моделей.

        Как работает функция:
        1. Пытается получить HTML-код страницы чата с моделями `cls.url`.
        2. Извлекает JSON-список моделей из HTML-кода с помощью регулярного выражения.
        3. Очищает JSON от лишних параметров.
        4. Преобразует JSON в список Python.
        5. Извлекает идентификаторы моделей.
        6. В случае неудачи логирует ошибку и возвращает список fallback-моделей.

        ASCII flowchart:
        A - Получение HTML-кода страницы
        |
        B - Извлечение JSON-списка моделей
        |
        C - Очистка JSON от лишних параметров
        |
        D - Преобразование JSON в список Python
        |
        E - Извлечение идентификаторов моделей
        |
        F - Обработка ошибок и возврат fallback-моделей

        Примеры:
            >>> HuggingChat.get_models()
            ['model1', 'model2', ...]
        """
        ...
```

### `on_auth_async`

```python
    @classmethod
    async def on_auth_async(cls, cookies: Cookies = None, proxy: str = None, **kwargs) -> AsyncIterator:
        """
        Выполняет асинхронную аутентификацию пользователя.

        Args:
            cls: Ссылка на класс.
            cookies (Cookies, optional): Куки пользователя. По умолчанию `None`.
            proxy (str, optional): Адрес прокси-сервера. По умолчанию `None`.

        Yields:
            AuthResult: Результат аутентификации.
            RequestLogin: Запрос на ввод данных для аутентификации.

        Raises:
            MissingAuthError: Если не удалось аутентифицироваться.

        Как работает функция:
        1. Проверяет наличие куки "hf-chat".
        2. Если куки есть, возвращает результат аутентификации с куками.
        3. Если куки нет, запрашивает данные для аутентификации.
        4. Получает куки из нодврайвера и возвращает результат аутентификации с новыми куками.

        ASCII flowchart:
        A - Проверка наличия куки "hf-chat"
        |
        B - Возврат результата аутентификации с куками (если куки есть)
        |
        C - Запрос данных для аутентификации (если куки нет)
        |
        D - Получение куки из нодврайвера
        |
        E - Возврат результата аутентификации с новыми куками

        Примеры:
            >>> async for result in HuggingChat.on_auth_async(cookies={'hf-chat': 'some_cookie'}):
            ...     print(result)

            >>> async for result in HuggingChat.on_auth_async():
            ...     print(result)
        """
        ...
```

### `create_authed`

```python
    @classmethod
    async def create_authed(
        cls,
        model: str,
        messages: Messages,
        auth_result: AuthResult,
        prompt: str = None,
        media: MediaListType = None,
        return_conversation: bool = False,
        conversation: Conversation = None,
        web_search: bool = False,
        **kwargs
    ) -> AsyncResult:
        """
        Создает аутентифицированный запрос к сервису Hugging Face Chat.

        Args:
            cls: Ссылка на класс.
            model (str): Идентификатор модели.
            messages (Messages): Список сообщений.
            auth_result (AuthResult): Результат аутентификации.
            prompt (str, optional): Дополнительный промпт. По умолчанию `None`.
            media (MediaListType, optional): Список медиафайлов. По умолчанию `None`.
            return_conversation (bool, optional): Флаг, указывающий, нужно ли возвращать объект разговора. По умолчанию `False`.
            conversation (Conversation, optional): Объект разговора. По умолчанию `None`.
            web_search (bool, optional): Флаг, указывающий, нужно ли использовать поиск в интернете. По умолчанию `False`.
            **kwargs: Дополнительные аргументы.

        Yields:
            str: Части ответа от сервиса Hugging Face Chat.
            ImageResponse: Ответ с изображением.
            Sources: Источники, найденные в интернете.
            TitleGeneration: Сгенерированный заголовок.
            Reasoning: Рассуждения модели.
            FinishReason: Причина завершения разговора.
            Conversation: Объект разговора (если `return_conversation` равен `True`).

        Raises:
            MissingRequirementsError: Если не установлена библиотека `curl_cffi`.
            ResponseError: Если произошла ошибка при выполнении запроса.

        Как работает функция:
        1. Проверяет наличие библиотеки `curl_cffi`.
        2. Определяет модель для запроса.
        3. Создает или использует существующий контекст разговора.
        4. Формирует параметры запроса.
        5. Отправляет запрос к сервису Hugging Face Chat.
        6. Обрабатывает ответ в реальном времени.
        7. Возвращает части ответа, изображения, источники, заголовки и причину завершения разговора.

        ASCII flowchart:
        A - Проверка наличия библиотеки `curl_cffi`
        |
        B - Определение модели для запроса
        |
        C - Создание или использование существующего контекста разговора
        |
        D - Формирование параметров запроса
        |
        E - Отправка запроса к сервису Hugging Face Chat
        |
        F - Обработка ответа в реальном времени
        |
        G - Возврат результатов

        Примеры:
            >>> auth_result = AuthResult(cookies={'hf-chat': 'some_cookie'})
            >>> messages = [{'role': 'user', 'content': 'Hello'}]
            >>> async for result in HuggingChat.create_authed(model='model1', messages=messages, auth_result=auth_result):
            ...     print(result)
        """
        ...
```

### `create_conversation`

```python
    @classmethod
    def create_conversation(cls, session: Session, model: str):
        """
        Создает новый контекст разговора.

        Args:
            cls: Ссылка на класс.
            session (Session): Сессия `curl_cffi`.
            model (str): Идентификатор модели.

        Returns:
            str: Идентификатор созданного контекста разговора.

        Raises:
            MissingAuthError: Если не удалось аутентифицироваться.
            ResponseError: Если произошла ошибка при выполнении запроса.

        Как работает функция:
        1. Формирует JSON-запрос с указанием модели.
        2. Отправляет POST-запрос к сервису Hugging Face Chat для создания контекста разговора.
        3. Обрабатывает возможные ошибки аутентификации или ошибки при выполнении запроса.
        4. Возвращает идентификатор созданного контекста разговора.

        ASCII flowchart:
        A - Формирование JSON-запроса
        |
        B - Отправка POST-запроса
        |
        C - Обработка ошибок аутентификации
        |
        D - Обработка ошибок при выполнении запроса
        |
        E - Возврат идентификатора контекста разговора

        Примеры:
            >>> session = Session()
            >>> conversation_id = HuggingChat.create_conversation(session, 'model1')
            >>> print(conversation_id)
            'some_conversation_id'
        """
        ...
```

### `fetch_message_id`

```python
    @classmethod
    def fetch_message_id(cls, session: Session, conversation_id: str):
        """
        Извлекает идентификатор последнего сообщения в контексте разговора.

        Args:
            cls: Ссылка на класс.
            session (Session): Сессия `curl_cffi`.
            conversation_id (str): Идентификатор контекста разговора.

        Returns:
            str: Идентификатор последнего сообщения.

        Raises:
            RuntimeError: Если не удалось извлечь идентификатор сообщения.

        Как работает функция:
        1. Отправляет GET-запрос к сервису Hugging Face Chat для получения данных контекста разговора.
        2. Разбивает ответ на строки и пытается разобрать каждую строку как JSON.
        3. Извлекает идентификатор последнего сообщения из JSON-данных.
        4. Обрабатывает возможные ошибки при разборе JSON или извлечении данных.
        5. Проверяет наличие ошибок в ответе и, если есть, вызывает исключение.

        ASCII flowchart:
        A - Отправка GET-запроса
        |
        B - Разбиение ответа на строки
        |
        C - Разбор каждой строки как JSON
        |
        D - Извлечение идентификатора последнего сообщения
        |
        E - Обработка ошибок при разборе JSON
        |
        F - Проверка на наличие ошибок в ответе

        Примеры:
            >>> session = Session()
            >>> message_id = HuggingChat.fetch_message_id(session, 'some_conversation_id')
            >>> print(message_id)
            'some_message_id'
        """
        ...