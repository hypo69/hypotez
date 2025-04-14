# Модуль Anthropic

## Обзор

Модуль `Anthropic` предназначен для взаимодействия с API Anthropic. Он предоставляет функциональность для генерации текста на основе моделей Anthropic, таких как Claude. Модуль поддерживает как потоковую, так и не потоковую генерацию, а также работу с изображениями и инструментами. Этот модуль является частью проекта `hypotez` и интегрируется с другими компонентами для обеспечения доступа к различным AI-моделям.

## Подробнее

Модуль `Anthropic` расширяет класс `OpenaiAPI` и реализует специфическую логику для работы с API Anthropic. Он включает в себя методы для получения списка доступных моделей, создания асинхронного генератора текста и формирования заголовков запросов. Модуль также обрабатывает входящие сообщения, включая изображения, и преобразует их в формат, совместимый с API Anthropic.

## Классы

### `Anthropic`

**Описание**: Класс `Anthropic` предоставляет интерфейс для взаимодействия с API Anthropic.

**Наследует**:
- `OpenaiAPI`: Класс `Anthropic` наследует функциональность от класса `OpenaiAPI`, включая общую логику для работы с API.

**Атрибуты**:
- `label` (str): Метка, идентифицирующая провайдера API как "Anthropic API".
- `url` (str): URL для доступа к консоли Anthropic.
- `login_url` (str): URL для входа в настройки ключей Anthropic.
- `working` (bool): Флаг, указывающий, что API работает (True).
- `api_base` (str): Базовый URL для API Anthropic.
- `needs_auth` (bool): Флаг, указывающий, требуется ли аутентификация (True).
- `supports_stream` (bool): Флаг, указывающий, поддерживается ли потоковая передача (True).
- `supports_system_message` (bool): Флаг, указывающий, поддерживаются ли системные сообщения (True).
- `supports_message_history` (bool): Флаг, указывающий, поддерживается ли история сообщений (True).
- `default_model` (str): Модель, используемая по умолчанию ("claude-3-5-sonnet-latest").
- `models` (list[str]): Список поддерживаемых моделей.
- `models_aliases` (dict[str, str]): Словарь псевдонимов моделей.

**Принцип работы**:
Класс `Anthropic` предоставляет методы для взаимодействия с API Anthropic, включая аутентификацию, отправку запросов и обработку ответов. Он поддерживает как потоковый, так и не потоковый режимы работы, а также позволяет отправлять изображения вместе с текстовыми сообщениями. Класс использует `StreamSession` для асинхронной отправки запросов и обработки ответов.

## Методы класса

### `get_models`

```python
@classmethod
def get_models(cls, api_key: str = None, **kwargs) -> list[str]:
    """
    Получает список доступных моделей Anthropic API.

    Args:
        api_key (str, optional): Ключ API для аутентификации. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        list[str]: Список идентификаторов моделей.

    Raises:
        requests.exceptions.HTTPError: Если возникает HTTP-ошибка при запросе к API.

    Пример:
        >>> Anthropic.get_models(api_key='YOUR_API_KEY')
        ['claude-3-opus-20240229', 'claude-3-sonnet-20240229', ...]
    """
```

**Назначение**: Метод `get_models` получает список доступных моделей Anthropic API.

**Параметры**:
- `api_key` (str, optional): Ключ API для аутентификации. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `list[str]`: Список идентификаторов моделей.

**Вызывает исключения**:
- `requests.exceptions.HTTPError`: Если возникает HTTP-ошибка при запросе к API.

**Как работает функция**:
1. Проверяет, есть ли уже список моделей в `cls.models`. Если есть, возвращает его.
2. Если списка нет, формирует URL для запроса списка моделей.
3. Отправляет GET-запрос к API Anthropic с использованием предоставленного `api_key` в заголовке.
4. Вызывает `raise_for_status` для проверки статуса ответа.
5. Извлекает список идентификаторов моделей из JSON-ответа и сохраняет его в `cls.models`.
6. Возвращает список идентификаторов моделей.

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
    """
    Создает асинхронный генератор для взаимодействия с API Anthropic.

    Args:
        model (str): Идентификатор модели.
        messages (Messages): Список сообщений для отправки в API.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        timeout (int, optional): Время ожидания запроса в секундах. По умолчанию 120.
        media (MediaListType, optional): Список медиафайлов для отправки в API. По умолчанию `None`.
        api_key (str, optional): Ключ API для аутентификации. По умолчанию `None`.
        temperature (float, optional): Температура генерации. По умолчанию `None`.
        max_tokens (int, optional): Максимальное количество токенов в ответе. По умолчанию 4096.
        top_k (int, optional): Параметр top_k. По умолчанию `None`.
        top_p (float, optional): Параметр top_p. По умолчанию `None`.
        stop (list[str], optional): Список стоп-слов. По умолчанию `None`.
        stream (bool, optional): Флаг, указывающий, использовать ли потоковую передачу. По умолчанию `False`.
        headers (dict, optional): Дополнительные заголовки для запроса. По умолчанию `None`.
        impersonate (str, optional): Идентификатор для имитации. По умолчанию `None`.
        tools (Optional[list], optional): Список инструментов для использования. По умолчанию `None`.
        extra_data (dict, optional): Дополнительные данные для запроса. По умолчанию `{}`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор для получения ответов от API.

    Raises:
        MissingAuthError: Если не предоставлен `api_key`.

    Пример:
        >>> async for chunk in Anthropic.create_async_generator(model='claude-3-opus-20240229', messages=[{'role': 'user', 'content': 'Hello'}], api_key='YOUR_API_KEY'):
        ...     print(chunk)
    """
```

**Назначение**: Метод `create_async_generator` создает асинхронный генератор для взаимодействия с API Anthropic.

**Параметры**:
- `model` (str): Идентификатор модели.
- `messages` (Messages): Список сообщений для отправки в API.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `timeout` (int, optional): Время ожидания запроса в секундах. По умолчанию 120.
- `media` (MediaListType, optional): Список медиафайлов для отправки в API. По умолчанию `None`.
- `api_key` (str, optional): Ключ API для аутентификации. По умолчанию `None`.
- `temperature` (float, optional): Температура генерации. По умолчанию `None`.
- `max_tokens` (int, optional): Максимальное количество токенов в ответе. По умолчанию 4096.
- `top_k` (int, optional): Параметр top_k. По умолчанию `None`.
- `top_p` (float, optional): Параметр top_p. По умолчанию `None`.
- `stop` (list[str], optional): Список стоп-слов. По умолчанию `None`.
- `stream` (bool, optional): Флаг, указывающий, использовать ли потоковую передачу. По умолчанию `False`.
- `headers` (dict, optional): Дополнительные заголовки для запроса. По умолчанию `None`.
- `impersonate` (str, optional): Идентификатор для имитации. По умолчанию `None`.
- `tools` (Optional[list], optional): Список инструментов для использования. По умолчанию `None`.
- `extra_data` (dict, optional): Дополнительные данные для запроса. По умолчанию `{}`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор для получения ответов от API.

**Вызывает исключения**:
- `MissingAuthError`: Если не предоставлен `api_key`.

**Как работает функция**:
1. Проверяет, предоставлен ли `api_key`. Если нет, вызывает исключение `MissingAuthError`.
2. Если `media` предоставлен, обрабатывает изображения:
   - Преобразует каждое изображение в формат base64.
   - Добавляет изображения в список сообщений.
3. Извлекает системные сообщения из списка сообщений и объединяет их в одну строку.
4. Если системные сообщения отсутствуют, устанавливает `system` в `None`.
5. Создает асинхронную сессию с использованием `StreamSession`.
6. Формирует данные для запроса, включая сообщения, модель, параметры генерации и системное сообщение.
7. Отправляет POST-запрос к API Anthropic с использованием сформированных данных.
8. Обрабатывает ответ в зависимости от того, включена ли потоковая передача:
   - Если потоковая передача выключена, извлекает данные из JSON-ответа и генерирует результаты.
   - Если потоковая передача включена, обрабатывает каждый чанк данных и генерирует результаты.
9. Возвращает асинхронный генератор для получения ответов от API.

### `get_headers`

```python
@classmethod
def get_headers(cls, stream: bool, api_key: str = None, headers: dict = None) -> dict:
    """
    Формирует заголовки запроса для API Anthropic.

    Args:
        stream (bool): Флаг, указывающий, использовать ли потоковую передачу.
        api_key (str, optional): Ключ API для аутентификации. По умолчанию `None`.
        headers (dict, optional): Дополнительные заголовки. По умолчанию `None`.

    Returns:
        dict: Словарь заголовков запроса.

    Пример:
        >>> Anthropic.get_headers(stream=True, api_key='YOUR_API_KEY')
        {'Accept': 'text/event-stream', 'Content-Type': 'application/json', 'x-api-key': 'YOUR_API_KEY', 'anthropic-version': '2023-06-01'}
    """
```

**Назначение**: Метод `get_headers` формирует заголовки запроса для API Anthropic.

**Параметры**:
- `stream` (bool): Флаг, указывающий, использовать ли потоковую передачу.
- `api_key` (str, optional): Ключ API для аутентификации. По умолчанию `None`.
- `headers` (dict, optional): Дополнительные заголовки. По умолчанию `None`.

**Возвращает**:
- `dict`: Словарь заголовков запроса.

**Как работает функция**:
1. Определяет заголовок `Accept` в зависимости от того, включена ли потоковая передача.
2. Устанавливает заголовок `Content-Type` в `application/json`.
3. Добавляет заголовок `x-api-key`, если предоставлен `api_key`.
4. Устанавливает заголовок `anthropic-version` в `2023-06-01`.
5. Объединяет все заголовки в один словарь и возвращает его.