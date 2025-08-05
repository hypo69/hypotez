# Модуль api.py

## Обзор

Модуль `api.py` предоставляет API-интерфейсы для взаимодействия с различными моделями и провайдерами, такими как GPT-4. 
Он включает функции для получения списка моделей, провайдеров, версий, обработки изображений, а также для создания и управления диалогами.

## Подробнее

Модуль содержит класс `Api` со статическими методами для получения информации о моделях и провайдерах. 
Также включает методы для подготовки и обработки диалогов с использованием различных провайдеров и моделей, 
обеспечивая стриминг ответов и обработку различных типов контента (текст, изображения, аудио).

## Классы

### `Api`

Описание класса, предоставляющего API-интерфейсы для взаимодействия с моделями и провайдерами.

**Методы:**

- `get_models()`: Возвращает список доступных моделей с информацией об их типах (изображения, зрение) и поддерживаемых провайдерах.
- `get_provider_models(provider: str, api_key: str = None, api_base: str = None)`: Возвращает список моделей, поддерживаемых указанным провайдером.
- `get_providers()`: Возвращает список доступных провайдеров с информацией об их возможностях и требованиях аутентификации.
- `get_version()`: Возвращает информацию о текущей и последней доступной версиях.
- `serve_images(name)`: Отправляет запрошенное изображение из директории с изображениями.
- `_prepare_conversation_kwargs(json_data: dict)`: Подготавливает аргументы для создания или продолжения диалога на основе полученных данных в формате JSON.
- `_create_response_stream(kwargs: dict, conversation_id: str, provider: str, download_media: bool = True)`: Создает поток ответов от модели, обрабатывая различные типы сообщений и контента.
- `_yield_logs()`: Возвращает логи отладки.
- `_format_json(response_type: str, content = None, **kwargs)`: Форматирует данные в JSON-формат для отправки клиенту.
- `handle_provider(provider_handler, model)`: Обрабатывает информацию о провайдере и форматирует её для отправки клиенту.

## Методы класса

### `get_models`

```python
@staticmethod
def get_models():
    """Возвращает список доступных моделей с информацией об их типах и поддерживаемых провайдерах.

    Returns:
        list: Список словарей, где каждый словарь содержит информацию о модели.
            - "name" (str): Имя модели.
            - "image" (bool): Указывает, является ли модель моделью для работы с изображениями.
            - "vision" (bool): Указывает, является ли модель моделью для компьютерного зрения.
            - "providers" (list): Список провайдеров, поддерживающих данную модель.

    Пример:
        >>> Api.get_models()
        [{'name': 'gpt-3.5-turbo', 'image': False, 'vision': False, 'providers': ['OpenAI', 'RetryProvider']}]
    """
    ...
```

### `get_provider_models`

```python
@staticmethod
def get_provider_models(provider: str, api_key: str = None, api_base: str = None):
    """Возвращает список моделей, поддерживаемых указанным провайдером.

    Args:
        provider (str): Имя провайдера.
        api_key (str, optional): API-ключ для провайдера (если требуется). По умолчанию `None`.
        api_base (str, optional): Базовый URL API провайдера (если требуется). По умолчанию `None`.

    Returns:
        list: Список словарей с информацией о моделях провайдера.
            - "model" (str): Имя модели.
            - "default" (bool): Указывает, является ли модель моделью по умолчанию для данного провайдера.
            - "vision" (bool): Указывает, является ли модель моделью для компьютерного зрения.
            - "image" (bool): Указывает, является ли модель моделью для работы с изображениями.
            - "task" (str, optional): Задача, выполняемая моделью (если применимо).

    Пример:
        >>> Api.get_provider_models('OpenAI', api_key='YOUR_API_KEY')
        [{'model': 'gpt-3.5-turbo', 'default': True, 'vision': False, 'image': False, 'task': None}]
    """
    ...
```

### `get_providers`

```python
@staticmethod
def get_providers() -> dict[str, str]:
    """Возвращает список доступных провайдеров с информацией об их возможностях и требованиях аутентификации.

    Returns:
        dict[str, str]: Список словарей, где каждый словарь содержит информацию о провайдере.
            - "name" (str): Имя провайдера.
            - "label" (str): Метка провайдера.
            - "parent" (str, optional): Имя родительского провайдера (если есть).
            - "image" (bool): Указывает, поддерживает ли провайдер работу с изображениями.
            - "vision" (bool): Указывает, поддерживает ли провайдер компьютерное зрение.
            - "nodriver" (bool): Указывает, требуется ли драйвер для работы с провайдером.
            - "hf_space" (bool): Указывает, размещен ли провайдер на HF Space.
            - "auth" (bool): Указывает, требуется ли аутентификация для работы с провайдером.
            - "login_url" (str, optional): URL для входа в систему провайдера (если требуется).

    Пример:
        >>> Api.get_providers()
        [{'name': 'OpenAI', 'label': 'OpenAI', 'parent': None, 'image': False, 'vision': False, 'nodriver': False, 'hf_space': False, 'auth': True, 'login_url': None}]
    """
    ...
```

### `get_version`

```python
@staticmethod
def get_version() -> dict:
    """Возвращает информацию о текущей и последней доступной версиях.

    Returns:
        dict: Словарь с информацией о версиях.
            - "version" (str, optional): Текущая версия.
            - "latest_version" (str, optional): Последняя доступная версия.

    Пример:
        >>> Api.get_version()
        {'version': '1.2.3', 'latest_version': '1.2.4'}
    """
    ...
```

### `serve_images`

```python
def serve_images(self, name):
    """Отправляет запрошенное изображение из директории с изображениями.

    Args:
        name (str): Имя файла изображения.

    Returns:
        flask.Response: Ответ Flask с изображением.

    Пример:
        >>> from flask import Flask
        >>> app = Flask(__name__)
        >>> api = Api()
        >>> @app.route('/images/<name>')
        ... def serve_image(name):
        ...     return api.serve_images(name)
    """
    ...
```

### `_prepare_conversation_kwargs`

```python
def _prepare_conversation_kwargs(self, json_data: dict):
    """Подготавливает аргументы для создания или продолжения диалога на основе полученных данных в формате JSON.

    Args:
        json_data (dict): Данные в формате JSON, содержащие информацию о диалоге.

    Returns:
        dict: Словарь с подготовленными аргументами для создания или продолжения диалога.
            - "model" (str): Имя модели.
            - "provider" (str): Имя провайдера.
            - "messages" (list): Список сообщений в диалоге.
            - "stream" (bool): Указывает, должен ли диалог быть в режиме стриминга.
            - "ignore_stream" (bool): Указывает, следует ли игнорировать стриминг.
            - "return_conversation" (bool): Указывает, следует ли возвращать объект диалога.
            - **kwargs: Дополнительные аргументы.

    
    - Извлекает значения `model`, `provider`, `messages`, и `action` из `json_data`.
    - Добавляет информацию о функциях `bucket_tool` и `continue_tool` в `tool_calls`.
    - Проверяет, является ли диалог новым или продолжением существующего, и устанавливает соответствующие параметры.

    Примеры:
        Пример структуры `json_data`:
        >>> json_data = {
        ...     "model": "gpt-3.5-turbo",
        ...     "provider": "OpenAI",
        ...     "messages": [{"role": "user", "content": "Hello"}],
        ...     "action": "continue",
        ...     "conversation_id": "123"
        ... }
        >>> api = Api()
        >>> kwargs = api._prepare_conversation_kwargs(json_data)
        >>> print(kwargs["model"])
        gpt-3.5-turbo
    """
    ...
```

### `_create_response_stream`

```python
def _create_response_stream(self, kwargs: dict, conversation_id: str, provider: str, download_media: bool = True) -> Iterator:
    """Создает поток ответов от модели, обрабатывая различные типы сообщений и контента.

    Args:
        kwargs (dict): Аргументы для создания запроса к модели.
        conversation_id (str): Идентификатор диалога.
        provider (str): Имя провайдера.
        download_media (bool, optional): Указывает, следует ли загружать медиафайлы. По умолчанию `True`.

    Yields:
        dict: JSON-ответы с различными типами контента (текст, изображения, логи, ошибки и т.д.).

    
    - Инициализирует логирование и отладку.
    - Получает модель и обработчик провайдера с помощью `get_model_and_provider`.
    - Обрабатывает различные типы ответов от провайдера, такие как текст, изображения, аудио, логи, ошибки и т.д.
    - Форматирует ответы в JSON и отправляет их клиенту.
    - Обрабатывает ошибки и исключения, возникшие в процессе обработки запроса.

    Примеры:
        Пример вызова функции:
        >>> kwargs = {
        ...     "model": "gpt-3.5-turbo",
        ...     "provider": "OpenAI",
        ...     "messages": [{"role": "user", "content": "Hello"}]
        ... }
        >>> api = Api()
        >>> stream = api._create_response_stream(kwargs, "123", "OpenAI")
        >>> for response in stream:
        ...     print(response)
        {'type': 'provider', 'provider': {'name': 'OpenAI', 'model': 'gpt-3.5-turbo'}}
    """

    def decorated_log(text: str, file = None):
        """
        Внутренняя функция для логирования отладочной информации.

        Args:
            text (str): Текст для логирования.
            file (optional): Файл для логирования.
        """
        debug.logs.append(text)
        if debug.logging:
            debug.log_handler(text, file=file)

    debug.log = decorated_log

    ...
```

### `_yield_logs`

```python
def _yield_logs(self):
    """Возвращает логи отладки.

    Yields:
        dict: JSON-ответы с логами отладки.

    
    - Проверяет наличие логов в `debug.logs`.
    - Форматирует каждый лог в JSON и отправляет его клиенту.
    - Очищает список логов `debug.logs`.
    """
    ...
```

### `_format_json`

```python
def _format_json(self, response_type: str, content = None, **kwargs):
    """Форматирует данные в JSON-формат для отправки клиенту.

    Args:
        response_type (str): Тип ответа.
        content (optional): Содержимое ответа.
        **kwargs: Дополнительные аргументы.

    Returns:
        dict: Словарь в формате JSON.

    
    - Создает словарь с типом ответа и содержимым (если есть).
    - Добавляет дополнительные аргументы в словарь.

    Примеры:
        >>> api = Api()
        >>> api._format_json("content", "Hello", urls=["url1", "url2"])
        {'type': 'content', 'content': 'Hello', 'urls': ['url1', 'url2']}
    """
    ...
```

### `handle_provider`

```python
def handle_provider(self, provider_handler, model):
    """Обрабатывает информацию о провайдере и форматирует её для отправки клиенту.

    Args:
        provider_handler: Обработчик провайдера.
        model: Модель.

    Returns:
        dict: Словарь с информацией о провайдере в формате JSON.

    
    - Проверяет, является ли провайдер `BaseRetryProvider` и использует `last_provider`, если это так.
    - Форматирует информацию о провайдере в JSON и отправляет ее клиенту.
    """
    ...
```

## Функции

### `get_error_message`

```python
def get_error_message(exception: Exception) -> str:
    """Форматирует сообщение об ошибке на основе переданного исключения.

    Args:
        exception (Exception): Объект исключения.

    Returns:
        str: Отформатированное сообщение об ошибке.

    Пример:
        >>> try:
        ...     raise ValueError("Invalid value")
        ... except ValueError as ex:
        ...     print(get_error_message(ex))
        ValueError: Invalid value
    """
    return f"{type(exception).__name__}: {exception}"