# Модуль HuggingChat

## Обзор

Модуль `HuggingChat.py` предоставляет класс `HuggingChat`, который позволяет взаимодействовать с моделями Hugging Face для создания диалогов и обработки изображений. Он поддерживает асинхронную аутентификацию, потоковую передачу данных и работу с изображениями. Этот модуль является частью проекта `hypotez` и предназначен для интеграции с другими компонентами системы.

## Подробнее

Модуль `HuggingChat` предназначен для обеспечения асинхронного взаимодействия с Hugging Face. Он включает в себя поддержку работы с текстовыми и визуальными моделями, аутентификацию через cookies или через запрос логина, а также обработку ответов в формате JSON. Модуль использует библиотеку `curl_cffi` для выполнения HTTP-запросов, что позволяет эффективно работать с потоковыми данными. Он интегрируется с системой аутентификации `hypotez` и предоставляет возможность создания и управления диалогами.

## Классы

### `Conversation`

**Описание**: Класс для управления контекстом диалога.

**Наследует**: `JsonConversation`

**Атрибуты**:

- `models` (dict): Словарь, содержащий информацию о моделях, используемых в диалоге.

### `HuggingChat`

**Описание**: Класс для взаимодействия с Hugging Face Chat.

**Наследует**: `AsyncAuthedProvider`, `ProviderModelMixin`

**Атрибуты**:

- `domain` (str): Домен Hugging Face.
- `origin` (str): URL происхождения.
- `url` (str): URL для чата.
- `working` (bool): Флаг, указывающий, работает ли провайдер.
- `use_nodriver` (bool): Флаг, указывающий, использовать ли без драйвера.
- `supports_stream` (bool): Флаг, указывающий, поддерживает ли потоковую передачу.
- `needs_auth` (bool): Флаг, указывающий, требуется ли аутентификация.
- `default_model` (str): Модель по умолчанию.
- `default_vision_model` (str): Визуальная модель по умолчанию.
- `model_aliases` (dict): Алиасы моделей.
- `image_models` (list): Список моделей для работы с изображениями.
- `text_models` (list): Список моделей для работы с текстом.

**Методы**:

- `get_models()`: Получает список доступных моделей.
- `on_auth_async()`: Выполняет асинхронную аутентификацию.
- `create_authed()`: Создает аутентифицированный запрос.
- `create_conversation()`: Создает новый диалог.
- `fetch_message_id()`: Получает ID последнего сообщения.

## Методы класса

### `get_models`

```python
    @classmethod
    def get_models(cls):
        """Получает список доступных моделей.

        Args:
            cls (HuggingChat): Ссылка на класс `HuggingChat`.

        Returns:
            list: Список доступных моделей.

        Raises:
            Exception: Если происходит ошибка при чтении моделей.

        Как работает функция:
        - Функция отправляет GET-запрос к `cls.url` для получения списка моделей.
        - Извлекает JSON из ответа, используя регулярные выражения для поиска строки, содержащей информацию о моделях.
        - Обрабатывает извлеченную строку, удаляя ненужные части и добавляя кавычки к ключам JSON.
        - Преобразует строку в JSON-объект и извлекает идентификаторы моделей.
        - В случае ошибки логирует сообщение об ошибке и использует резервный список моделей.

        Примеры:
            >>> HuggingChat.get_models()
            ['model1', 'model2', 'model3']
        """
        ...
```

### `on_auth_async`

```python
    @classmethod
    async def on_auth_async(cls, cookies: Cookies = None, proxy: str = None, **kwargs) -> AsyncIterator:
        """Выполняет асинхронную аутентификацию.

        Args:
            cls (HuggingChat): Ссылка на класс `HuggingChat`.
            cookies (Cookies, optional): Cookies для аутентификации. По умолчанию `None`.
            proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
            **kwargs: Дополнительные параметры.

        Yields:
            AuthResult: Результат аутентификации.
            RequestLogin: Запрос на логин, если требуется.

        Как работает функция:
        - Проверяет наличие cookies. Если cookies не предоставлены, пытается получить их из браузера.
        - Если cookies содержат ключ `hf-chat`, возвращает результат аутентификации с этими cookies.
        - Если требуется аутентификация, запрашивает URL для логина и выполняет аутентификацию через `get_args_from_nodriver`.
        - Если аутентификация не требуется, генерирует случайный `session ID`.

        Примеры:
            >>> async for result in HuggingChat.on_auth_async(cookies={'hf-chat': 'cookie_value'}):
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
        """Создает аутентифицированный запрос.

        Args:
            cls (HuggingChat): Ссылка на класс `HuggingChat`.
            model (str): Имя модели для использования.
            messages (Messages): Список сообщений для отправки.
            auth_result (AuthResult): Результат аутентификации.
            prompt (str, optional): Дополнительный текст запроса. По умолчанию `None`.
            media (MediaListType, optional): Список медиафайлов для отправки. По умолчанию `None`.
            return_conversation (bool, optional): Флаг, указывающий, возвращать ли объект диалога. По умолчанию `False`.
            conversation (Conversation, optional): Объект диалога для продолжения. По умолчанию `None`.
            web_search (bool, optional): Флаг, указывающий, использовать ли веб-поиск. По умолчанию `False`.
            **kwargs: Дополнительные параметры.

        Yields:
            str: Текст ответа от модели.
            ImageResponse: Ответ с изображением.
            Sources: Источники веб-поиска.
            FinishReason: Причина завершения.
            TitleGeneration: Сгенерированный заголовок.
            Reasoning: Логическое обоснование ответа.
            Conversation: Объект диалога, если `return_conversation` равен `True`.

        Raises:
            MissingRequirementsError: Если не установлена библиотека `curl_cffi`.

        Как работает функция:
        - Проверяет наличие библиотеки `curl_cffi`. Если она не установлена, вызывает исключение.
        - Определяет модель для использования. Если `media` не равно `None`, использует визуальную модель по умолчанию.
        - Создает сессию `curl_cffi` с использованием данных аутентификации.
        - Если диалог не существует, создает новый диалог с использованием `create_conversation`.
        - Формирует параметры запроса, включая текст запроса, ID диалога и флаги.
        - Добавляет медиафайлы к запросу, если они предоставлены.
        - Отправляет POST-запрос к Hugging Face и обрабатывает ответ.
        - В зависимости от типа ответа (stream, finalAnswer, file, webSearch, title, reasoning) возвращает соответствующие объекты.

        Примеры:
            >>> async for response in HuggingChat.create_authed(model='model1', messages=[{'role': 'user', 'content': 'Hello'}], auth_result=auth_result):
            ...     print(response)
        """
        ...
```

### `create_conversation`

```python
    @classmethod
    def create_conversation(cls, session: Session, model: str):
        """Создает новый диалог.

        Args:
            cls (HuggingChat): Ссылка на класс `HuggingChat`.
            session (Session): Сессия `curl_cffi`.
            model (str): Имя модели для использования.

        Returns:
            str: ID созданного диалога.

        Raises:
            MissingAuthError: Если отсутствует аутентификация.
            ResponseError: Если произошла ошибка при создании диалога.

        Как работает функция:
        - Формирует JSON-данные с указанием модели.
        - Отправляет POST-запрос к Hugging Face для создания диалога.
        - Обрабатывает возможные ошибки аутентификации и ошибки ответа.
        - Возвращает ID созданного диалога из JSON-ответа.

        Примеры:
            >>> conversation_id = HuggingChat.create_conversation(session, 'model1')
            >>> print(conversation_id)
            'conversation_id'
        """
        ...
```

### `fetch_message_id`

```python
    @classmethod
    def fetch_message_id(cls, session: Session, conversation_id: str):
        """Получает ID последнего сообщения.

        Args:
            cls (HuggingChat): Ссылка на класс `HuggingChat`.
            session (Session): Сессия `curl_cffi`.
            conversation_id (str): ID диалога.

        Returns:
            str: ID последнего сообщения.

        Raises:
            RuntimeError: Если не удалось извлечь ID сообщения.

        Как работает функция:
        - Отправляет GET-запрос к Hugging Face для получения данных диалога.
        - Разбирает ответ, разделяя его на строки и анализируя каждую строку как JSON.
        - Извлекает ID последнего сообщения из JSON-данных.
        - Обрабатывает возможные ошибки при разборе ответа.

        Примеры:
            >>> message_id = HuggingChat.fetch_message_id(session, 'conversation_id')
            >>> print(message_id)
            'message_id'
        """
        ...