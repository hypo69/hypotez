# Модуль OpenaiTemplate.py

## Обзор

Модуль `OpenaiTemplate.py` предоставляет абстрактный класс `OpenaiTemplate`, который служит основой для взаимодействия с API OpenAI. Он включает в себя функциональность для получения списка моделей, создания асинхронных генераторов для обработки сообщений, обработки изображений, а также для управления заголовками запросов.

## Подробней

Этот модуль является частью проекта `hypotez` и предназначен для упрощения интеграции с различными моделями OpenAI. Он предоставляет инструменты для асинхронного взаимодействия с API, обработки ответов в формате JSON и SSE (Server-Sent Events), а также для обработки ошибок и аутентификации.

## Классы

### `OpenaiTemplate`

**Описание**:
Абстрактный класс, предоставляющий базовую функциональность для взаимодействия с API OpenAI.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.
- `RaiseErrorMixin`: Включает обработку ошибок.

**Атрибуты**:
- `api_base` (str): Базовый URL API. По умолчанию "".
- `api_key` (str | None): Ключ API для аутентификации. По умолчанию `None`.
- `api_endpoint` (str | None): Конечная точка API. По умолчанию `None`.
- `supports_message_history` (bool): Поддержка истории сообщений. По умолчанию `True`.
- `supports_system_message` (bool): Поддержка системных сообщений. По умолчанию `True`.
- `default_model` (str): Модель по умолчанию. По умолчанию "".
- `fallback_models` (list[str]): Список резервных моделей. По умолчанию [].
- `sort_models` (bool): Флаг для сортировки моделей. По умолчанию `True`.
- `ssl` (bool | None): Флаг для проверки SSL. По умолчанию `None`.

**Методы**:
- `get_models(api_key: str = None, api_base: str = None) -> list[str]`: Получает список доступных моделей.
- `create_async_generator(...) -> AsyncResult`: Создает асинхронный генератор для обработки сообщений.
- `get_headers(stream: bool, api_key: str = None, headers: dict = None) -> dict`: Формирует заголовки для запросов к API.

### `get_models`

```python
@classmethod
def get_models(cls, api_key: str = None, api_base: str = None) -> list[str]:
    """
    Извлекает список доступных моделей из API OpenAI.

    Args:
        api_key (str, optional): Ключ API для аутентификации. По умолчанию `None`.
        api_base (str, optional): Базовый URL API. По умолчанию `None`.

    Returns:
        list[str]: Список идентификаторов доступных моделей.

    Raises:
        Exception: Если возникает ошибка при запросе к API.

    
    - Функция выполняет HTTP-запрос к API OpenAI для получения списка доступных моделей.
    - Если `api_key` не предоставлен, функция пытается использовать `cls.api_key`.
    - В случае успеха, функция извлекает идентификаторы моделей из JSON-ответа и возвращает их в виде списка.
    - Если происходит ошибка (например, сетевая ошибка или неверный ключ API), функция логирует ошибку и возвращает список резервных моделей `cls.fallback_models`.

    Примеры:
        >>> OpenaiTemplate.get_models(api_key="test_key", api_base="https://api.openai.com/v1")
        ['gpt-3.5-turbo', 'gpt-4']

        >>> OpenaiTemplate.get_models()
        []
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
    api_endpoint: str = None,
    api_base: str = None,
    temperature: float = None,
    max_tokens: int = None,
    top_p: float = None,
    stop: Union[str, list[str]] = None,
    stream: bool = False,
    prompt: str = None,
    headers: dict = None,
    impersonate: str = None,
    extra_parameters: list[str] = ["tools", "parallel_tool_calls", "tool_choice", "reasoning_effort", "logit_bias", "modalities", "audio"],
    extra_data: dict = {},
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для взаимодействия с API OpenAI.

    Args:
        model (str): Идентификатор модели для использования.
        messages (Messages): Список сообщений для отправки в API.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        timeout (int, optional): Время ожидания запроса в секундах. По умолчанию 120.
        media (MediaListType, optional): Список медиа-файлов для отправки. По умолчанию `None`.
        api_key (str, optional): Ключ API для аутентификации. По умолчанию `None`.
        api_endpoint (str, optional): Конечная точка API. По умолчанию `None`.
        api_base (str, optional): Базовый URL API. По умолчанию `None`.
        temperature (float, optional): Температура для управления случайностью генерации. По умолчанию `None`.
        max_tokens (int, optional): Максимальное количество токенов в ответе. По умолчанию `None`.
        top_p (float, optional): Параметр для управления разнообразием токенов. По умолчанию `None`.
        stop (Union[str, list[str]], optional): Список стоп-слов. По умолчанию `None`.
        stream (bool, optional): Флаг для включения потоковой передачи данных. По умолчанию `False`.
        prompt (str, optional): Дополнительный промпт для отправки. По умолчанию `None`.
        headers (dict, optional): Дополнительные заголовки для запроса. По умолчанию `None`.
        impersonate (str, optional): Имя пользователя для имитации. По умолчанию `None`.
        extra_parameters (list[str], optional): Список дополнительных параметров для передачи в API. По умолчанию `["tools", "parallel_tool_calls", "tool_choice", "reasoning_effort", "logit_bias", "modalities", "audio"]`.
        extra_data (dict, optional): Дополнительные данные для отправки в API. По умолчанию `{}`.
        **kwargs: Дополнительные именованные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий результаты из API.

    Raises:
        MissingAuthError: Если отсутствует ключ API и требуется аутентификация.
        ResponseError: Если получен неподдерживаемый content-type.

    
    - Функция создает асинхронный генератор для взаимодействия с API OpenAI.
    - Если `api_key` не предоставлен, функция пытается использовать `cls.api_key`.
    - Функция формирует данные запроса на основе переданных аргументов, включая сообщения, параметры модели и дополнительные параметры.
    - Если указана модель для генерации изображений, функция выполняет запрос к конечной точке `/images/generations` и возвращает URL-адреса сгенерированных изображений.
    - В противном случае, функция выполняет запрос к конечной точке `/chat/completions` и обрабатывает ответы в формате JSON или SSE (Server-Sent Events).
    - Функция возвращает асинхронный генератор, который выдает частичные результаты по мере их получения из API.

    Примеры:
        ```python
        messages = [{"role": "user", "content": "Напиши стихотворение."}]
        async for response in OpenaiTemplate.create_async_generator(model="gpt-3.5-turbo", messages=messages):
            print(response)
        ```
    """
    ...
```

### `get_headers`

```python
@classmethod
def get_headers(cls, stream: bool, api_key: str = None, headers: dict = None) -> dict:
    """
    Формирует заголовки для HTTP-запросов к API OpenAI.

    Args:
        stream (bool): Флаг, указывающий, используется ли потоковая передача данных.
        api_key (str, optional): Ключ API для аутентификации. По умолчанию `None`.
        headers (dict, optional): Дополнительные заголовки. По умолчанию `None`.

    Returns:
        dict: Словарь с заголовками для запроса.

    
    - Функция формирует словарь с заголовками для HTTP-запросов к API OpenAI.
    - В зависимости от значения флага `stream`, функция устанавливает заголовок `Accept` в `text/event-stream` или `application/json`.
    - Если предоставлен `api_key`, функция добавляет заголовок `Authorization` с ключом API.
    - Функция объединяет предоставленные дополнительные заголовки с базовыми заголовками и возвращает результирующий словарь.

    Примеры:
        >>> OpenaiTemplate.get_headers(stream=True, api_key="test_key")
        {'Accept': 'text/event-stream', 'Content-Type': 'application/json', 'Authorization': 'Bearer test_key'}

        >>> OpenaiTemplate.get_headers(stream=False)
        {'Accept': 'application/json', 'Content-Type': 'application/json'}
    """
    ...