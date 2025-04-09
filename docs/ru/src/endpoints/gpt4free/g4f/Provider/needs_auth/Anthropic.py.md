# Модуль Anthropic

## Обзор

Модуль `Anthropic` предоставляет класс для взаимодействия с API Anthropic, в частности, с моделями Claude. Он поддерживает как потоковую передачу данных, так и отправку сообщений с изображениями. Этот модуль является частью проекта `hypotez` и предназначен для интеграции с различными AI-моделями, предоставляемыми Anthropic.

## Подробней

Модуль предназначен для работы с API Anthropic, включая аутентификацию, отправку запросов и обработку ответов. Он поддерживает различные модели Claude и предоставляет удобный интерфейс для взаимодействия с ними.

## Классы

### `Anthropic`

**Описание**: Класс для взаимодействия с API Anthropic.

**Наследует**:
- `OpenaiAPI`: Anthropic API наследует функциональность от OpenaiAPI, что позволяет использовать общие методы и атрибуты для работы с API.

**Атрибуты**:
- `label` (str): Метка для данного провайдера API ("Anthropic API").
- `url` (str): URL главной страницы Anthropic ("https://console.anthropic.com").
- `login_url` (str): URL страницы входа в Anthropic ("https://console.anthropic.com/settings/keys").
- `working` (bool): Указывает, работает ли данный провайдер (True).
- `api_base` (str): Базовый URL API Anthropic ("https://api.anthropic.com/v1").
- `needs_auth` (bool): Указывает, требуется ли аутентификация (True).
- `supports_stream` (bool): Указывает, поддерживает ли потоковую передачу (True).
- `supports_system_message` (bool): Указывает, поддерживает ли системные сообщения (True).
- `supports_message_history` (bool): Указывает, поддерживает ли историю сообщений (True).
- `default_model` (str): Модель, используемая по умолчанию ("claude-3-5-sonnet-latest").
- `models` (list[str]): Список поддерживаемых моделей.
- `models_aliases` (dict[str, str]): Словарь псевдонимов моделей.

**Методы**:
- `get_models()`: Возвращает список доступных моделей.
- `create_async_generator()`: Создает асинхронный генератор для обработки сообщений.
- `get_headers()`: Возвращает заголовки для запросов.

### `get_models`

```python
    @classmethod
    def get_models(cls, api_key: str = None, **kwargs) -> list[str]:
        """Получает список доступных моделей Anthropic.

        Args:
            api_key (str, optional): Ключ API для аутентификации. По умолчанию `None`.

        Returns:
            list[str]: Список идентификаторов моделей.

        Raises:
            requests.exceptions.HTTPError: Если возникает ошибка при запросе к API.

        Как работает функция:
        1. Проверяет, если список моделей `cls.models` уже заполнен.
        2. Если список пуст, выполняет GET-запрос к API Anthropic для получения списка моделей.
        3. Добавляет необходимые заголовки, включая `Content-Type`, `x-api-key` и `anthropic-version`.
        4. Обрабатывает ответ, извлекая идентификаторы моделей из JSON-ответа.
        5. Сохраняет полученный список моделей в `cls.models`.
        6. Возвращает список моделей.

        Блок-схема:
        A: Проверка `cls.models`
        |
        -- B: Если `cls.models` пуст -> GET-запрос к API Anthropic
        |
        C: Обработка ответа API и извлечение ID моделей
        |
        D: Сохранение списка моделей в `cls.models`
        |
        E: Возврат списка моделей

        Example:
            >>> Anthropic.get_models(api_key='ключ_api')
            ['claude-3-opus-latest', 'claude-3-sonnet-20240229', ...]
        """
        ...
```

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        timeout: int = 120,
        media: MediaListType = None,
        api_key: str = None,
        temperature: float = None,
        max_tokens: int = 4096,
        top_k: int = None,
        top_p: float = None,
        stop: list[str] = None,
        stream: bool = False,
        headers: dict = None,
        impersonate: str = None,
        tools: Optional[list] = None,
        extra_data: dict = {},
        **kwargs
    ) -> AsyncResult:
        """Создает асинхронный генератор для взаимодействия с API Anthropic.

        Args:
            model (str): Идентификатор модели для использования.
            messages (Messages): Список сообщений для отправки.
            proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
            timeout (int, optional): Время ожидания запроса в секундах. По умолчанию 120.
            media (MediaListType, optional): Список медиафайлов для отправки. По умолчанию `None`.
            api_key (str, optional): Ключ API для аутентификации. По умолчанию `None`.
            temperature (float, optional): Температура для генерации текста. По умолчанию `None`.
            max_tokens (int, optional): Максимальное количество токенов в ответе. По умолчанию 4096.
            top_k (int, optional): Параметр top_k. По умолчанию `None`.
            top_p (float, optional): Параметр top_p. По умолчанию `None`.
            stop (list[str], optional): Список стоп-последовательностей. По умолчанию `None`.
            stream (bool, optional): Указывает, использовать ли потоковую передачу. По умолчанию `False`.
            headers (dict, optional): Дополнительные заголовки для запроса. По умолчанию `None`.
            impersonate (str, optional): Имя пользователя для олицетворения. По умолчанию `None`.
            tools (Optional[list], optional): Список инструментов для использования. По умолчанию `None`.
            extra_data (dict, optional): Дополнительные данные для запроса. По умолчанию `{}`.

        Returns:
            AsyncResult: Асинхронный генератор для получения ответов от API.

        Raises:
            MissingAuthError: Если не предоставлен ключ API.

        Как работает функция:
        1. Проверяет наличие ключа API. Если ключ отсутствует, вызывает исключение `MissingAuthError`.
        2. Обрабатывает медиафайлы (изображения), преобразуя их в формат base64 и добавляя в сообщения.
        3. Разделяет системные сообщения и формирует основное тело запроса.
        4. Отправляет асинхронный POST-запрос к API Anthropic.
        5. Обрабатывает потоковые и не потоковые ответы, извлекая текст, информацию об использовании и вызовы инструментов.

        Блок-схема:
        A: Проверка наличия `api_key`
        |
        -- B: Если `api_key` отсутствует -> Вызов `MissingAuthError`
        |
        C: Обработка медиафайлов (изображений)
        |
        D: Разделение системных сообщений
        |
        E: Отправка асинхронного POST-запроса к API Anthropic
        |
        F: Обработка потоковых и не потоковых ответов

        Примеры:
            >>> messages = [{"role": "user", "content": "Привет, Claude!"}]
            >>> async for chunk in Anthropic.create_async_generator(model="claude-3-opus-latest", messages=messages, api_key="ключ_api"):
            ...     print(chunk, end="")
            Привет! Как я могу помочь вам сегодня?
        """
        ...
```

### `get_headers`

```python
    @classmethod
    def get_headers(cls, stream: bool, api_key: str = None, headers: dict = None) -> dict:
        """Возвращает словарь заголовков для запроса.

        Args:
            stream (bool): Указывает, является ли запрос потоковым.
            api_key (str, optional): Ключ API для аутентификации. По умолчанию `None`.
            headers (dict, optional): Дополнительные заголовки. По умолчанию `None`.

        Returns:
            dict: Словарь заголовков.

        Как работает функция:
        1. Определяет заголовок "Accept" в зависимости от того, является ли запрос потоковым.
        2. Добавляет заголовок "Content-Type" со значением "application/json".
        3. Если предоставлен ключ API, добавляет заголовок "x-api-key".
        4. Добавляет заголовок "anthropic-version" с указанием версии API.
        5. Объединяет все заголовки в один словарь и возвращает его.

        Блок-схема:
        A: Определение заголовка "Accept"
        |
        B: Добавление заголовка "Content-Type"
        |
        C: Проверка наличия `api_key` и добавление заголовка "x-api-key"
        |
        D: Добавление заголовка "anthropic-version"
        |
        E: Объединение заголовков в словарь и возврат

        Примеры:
            >>> Anthropic.get_headers(stream=True, api_key="ключ_api")
            {'Accept': 'text/event-stream', 'Content-Type': 'application/json', 'x-api-key': 'ключ_api', 'anthropic-version': '2023-06-01'}
        """
        ...