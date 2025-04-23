# Модуль `HuggingChat.py`

## Обзор

Модуль `HuggingChat.py` предназначен для взаимодействия с чат-моделью Hugging Face. Он предоставляет асинхронный интерфейс для аутентификации, создания бесед, отправки сообщений и получения ответов. Модуль поддерживает как текстовые, так и мультимодальные (с использованием изображений) запросы.

## Подробнее

Модуль использует библиотеку `curl_cffi` для выполнения HTTP-запросов, что обеспечивает высокую производительность. Он также включает обработку ошибок, управление cookies и поддержку прокси-серверов.

## Классы

### `Conversation`

**Описание**: Класс для управления состоянием беседы.

**Наследует**: `JsonConversation`

**Атрибуты**:

-   `models` (dict): Словарь, содержащий информацию о моделях, используемых в беседе.

### `HuggingChat`

**Описание**: Класс, реализующий взаимодействие с чат-моделью Hugging Face.

**Наследует**: `AsyncAuthedProvider`, `ProviderModelMixin`

**Атрибуты**:

-   `domain` (str): Доменное имя Hugging Face ("huggingface.co").
-   `origin` (str): Базовый URL Hugging Face.
-   `url` (str): URL для взаимодействия с чат-моделью.
-   `working` (bool): Флаг, указывающий на работоспособность провайдера.
-   `use_nodriver` (bool): Флаг, указывающий на использование без драйвера.
-   `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи данных.
-   `needs_auth` (bool): Флаг, указывающий на необходимость аутентификации.
-   `default_model` (str): Модель, используемая по умолчанию.
-   `default_vision_model` (str): Мультимодальная модель, используемая по умолчанию.
-   `model_aliases` (dict): Псевдонимы моделей.
-   `image_models` (list): Список моделей, поддерживающих обработку изображений.
-   `text_models` (list): Список текстовых моделей.

**Методы**:

-   `get_models()`: Получает список доступных моделей.
-   `on_auth_async()`: Выполняет аутентификацию пользователя.
-   `create_authed()`: Создает аутентифицированный запрос к чат-модели.
-   `create_conversation()`: Создает новую беседу.
-   `fetch_message_id()`: Получает идентификатор последнего сообщения в беседе.

## Методы класса

### `get_models`

```python
    @classmethod
    def get_models(cls):
        """
        Получает список доступных моделей из Hugging Face.

        Функция выполняет HTTP-запрос к странице Hugging Face, извлекает список моделей из JSON,
        и устанавливает атрибуты `text_models`, `models` и `vision_models` класса.

        Returns:
            list: Список доступных моделей.

        Raises:
            Exception: Если происходит ошибка при чтении моделей.
        """
```

**Как работает функция**:

1.  Выполняет HTTP-запрос к странице Hugging Face (`cls.url`).
2.  Извлекает JSON, содержащий список моделей.
3.  Обновляет атрибуты класса: `text_models`, `models` и `vision_models`.
4.  В случае ошибки логирует её и устанавливает атрибут `models` в значение `fallback_models`.

### `on_auth_async`

```python
    @classmethod
    async def on_auth_async(cls, cookies: Cookies = None, proxy: str = None, **kwargs) -> AsyncIterator:
        """
        Асинхронно аутентифицирует пользователя.

        Args:
            cookies (Cookies, optional): Cookies для аутентификации. По умолчанию `None`.
            proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.

        Yields:
            AuthResult: Результат аутентификации.
            RequestLogin: Запрос на логин, если требуется.
        """
```

**Как работает функция**:

1.  Проверяет наличие cookies. Если cookies отсутствуют, пытается получить их.
2.  Если в cookies есть `hf-chat`, возвращает `AuthResult` с cookies.
3.  Если требуется аутентификация (`cls.needs_auth`), возвращает `RequestLogin` и получает аргументы из `get_args_from_nodriver`.
4.  Если аутентификация не требуется, генерирует случайный `hf-chat` cookie и возвращает `AuthResult`.

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
        Создает аутентифицированный запрос к чат-модели.

        Args:
            model (str): Имя используемой модели.
            messages (Messages): Список сообщений для отправки.
            auth_result (AuthResult): Результат аутентификации.
            prompt (str, optional): Дополнительный промпт. По умолчанию `None`.
            media (MediaListType, optional): Список медиафайлов для отправки. По умолчанию `None`.
            return_conversation (bool, optional): Флаг, указывающий на необходимость возврата объекта Conversation. По умолчанию `False`.
            conversation (Conversation, optional): Объект Conversation. По умолчанию `None`.
            web_search (bool, optional): Флаг, указывающий на необходимость использования веб-поиска. По умолчанию `False`.

        Yields:
            str: Текст ответа от модели.
            ImageResponse: Ответ с изображением, если модель мультимодальная.
            Sources: Источники веб-поиска, если `web_search` включен.
            TitleGeneration: Сгенерированный заголовок беседы.
            Reasoning: Результаты рассуждений модели.
            FinishReason: Причина завершения беседы.

        Raises:
            MissingRequirementsError: Если не установлена библиотека `curl_cffi`.
            ResponseError: Если произошла ошибка при отправке запроса.
        """
```

**Как работает функция**:

1.  Проверяет наличие библиотеки `curl_cffi`.
2.  Получает или создает объект `Conversation`.
3.  Создает или использует существующий `conversationId`.
4.  Формирует данные для отправки в запросе.
5.  Выполняет POST-запрос к Hugging Face.
6.  Обрабатывает ответы от сервера, генерируя текст, изображения, источники веб-поиска и другие типы ответов.

### `create_conversation`

```python
    @classmethod
    def create_conversation(cls, session: Session, model: str):
        """
        Создает новую беседу.

        Args:
            session (Session): Объект сессии `curl_cffi`.
            model (str): Имя используемой модели.

        Returns:
            str: Идентификатор созданной беседы.

        Raises:
            MissingAuthError: Если отсутствует аутентификация.
            ResponseError: Если произошла ошибка при создании беседы.
        """
```

**Как работает функция**:

1.  Формирует JSON с данными модели.
2.  Выполняет POST-запрос к Hugging Face для создания беседы.
3.  Обрабатывает возможные ошибки аутентификации или другие ошибки.
4.  Возвращает `conversationId` из ответа сервера.

### `fetch_message_id`

```python
    @classmethod
    def fetch_message_id(cls, session: Session, conversation_id: str):
        """
        Получает идентификатор последнего сообщения в беседе.

        Args:
            session (Session): Объект сессии `curl_cffi`.
            conversation_id (str): Идентификатор беседы.

        Returns:
            str: Идентификатор последнего сообщения.

        Raises:
            RuntimeError: Если не удалось извлечь идентификатор сообщения.
        """
```

**Как работает функция**:

1.  Выполняет GET-запрос к Hugging Face для получения данных беседы.
2.  Извлекает `messageId` из JSON ответа.
3.  Обрабатывает возможные ошибки при разборе ответа.
4.  Возвращает идентификатор последнего сообщения.

## Параметры класса

-   `domain` (str): Доменное имя Hugging Face ("huggingface.co").
-   `origin` (str): Базовый URL Hugging Face.
-   `url` (str): URL для взаимодействия с чат-моделью.
-   `working` (bool): Флаг, указывающий на работоспособность провайдера.
-   `use_nodriver` (bool): Флаг, указывающий на использование без драйвера.
-   `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи данных.
-   `needs_auth` (bool): Флаг, указывающий на необходимость аутентификации.
-   `default_model` (str): Модель, используемая по умолчанию.
-   `default_vision_model` (str): Мультимодальная модель, используемая по умолчанию.
-   `model_aliases` (dict): Псевдонимы моделей.
-   `image_models` (list): Список моделей, поддерживающих обработку изображений.
-   `text_models` (list): Список текстовых моделей.