# Модуль OpenaiTemplate.py

## Обзор

Модуль `OpenaiTemplate.py` предоставляет абстрактный класс `OpenaiTemplate`, который служит шаблоном для взаимодействия с API OpenAI. Он включает в себя функциональность для получения списка моделей, создания асинхронного генератора для обработки сообщений и формирования заголовков запросов. Модуль также поддерживает работу с изображениями и инструментами (tools) через API OpenAI.

## Подробнее

Модуль `OpenaiTemplate` предназначен для упрощения интеграции с API OpenAI в асинхронном режиме. Он предоставляет базовый функционал, такой как аутентификация, обработка ошибок и форматирование запросов. Этот шаблон позволяет легко создавать производные классы для конкретных задач, связанных с использованием моделей OpenAI.

## Классы

### `OpenaiTemplate`

**Описание**: Абстрактный класс, предоставляющий шаблон для взаимодействия с API OpenAI.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.
- `RaiseErrorMixin`: Реализует обработку и возбуждение исключений.

**Атрибуты**:
- `api_base` (str): Базовый URL API OpenAI.
- `api_key` (str): Ключ API для аутентификации.
- `api_endpoint` (str): Конечная точка API для выполнения запросов.
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений.
- `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений.
- `default_model` (str): Модель, используемая по умолчанию.
- `fallback_models` (list[str]): Список запасных моделей.
- `sort_models` (bool): Флаг, указывающий на необходимость сортировки моделей.
- `ssl` (bool): Флаг, указывающий на необходимость использования SSL.

**Методы**:
- `get_models()`: Получает список доступных моделей.
- `create_async_generator()`: Создает асинхронный генератор для обработки сообщений.
- `get_headers()`: Формирует заголовки запроса.

### `OpenaiTemplate.get_models`

```python
@classmethod
def get_models(cls, api_key: str = None, api_base: str = None) -> list[str]:
    """
    Получает список доступных моделей от API OpenAI.

    Args:
        api_key (str, optional): Ключ API для аутентификации. По умолчанию `None`.
        api_base (str, optional): Базовый URL API OpenAI. По умолчанию `None`.

    Returns:
        list[str]: Список доступных моделей.

    Raises:
        Exception: Если происходит ошибка при получении списка моделей.

    Как работает функция:
    - Проверяет, если список моделей уже был получен.
    - Формирует заголовки запроса, включая ключ API, если он предоставлен.
    - Выполняет GET-запрос к API OpenAI для получения списка моделей.
    - Извлекает идентификаторы моделей из полученных данных.
    - Сортирует список моделей, если это необходимо.
    - В случае ошибки логирует её и возвращает список запасных моделей.

    Примеры:
        >>> OpenaiTemplate.get_models(api_key="test_api_key", api_base="https://api.openai.com/v1")
        ['gpt-3.5-turbo', 'gpt-4']
    """
    ...
```

### `OpenaiTemplate.create_async_generator`

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
        messages (Messages): Список сообщений для обработки.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        timeout (int, optional): Максимальное время ожидания запроса в секундах. По умолчанию 120.
        media (MediaListType, optional): Список медиафайлов для обработки. По умолчанию `None`.
        api_key (str, optional): Ключ API для аутентификации. По умолчанию `None`.
        api_endpoint (str, optional): Конечная точка API для выполнения запросов. По умолчанию `None`.
        api_base (str, optional): Базовый URL API OpenAI. По умолчанию `None`.
        temperature (float, optional): Параметр temperature для управления случайностью генерации. По умолчанию `None`.
        max_tokens (int, optional): Максимальное количество токенов в ответе. По умолчанию `None`.
        top_p (float, optional): Параметр top_p для управления выбором токенов. По умолчанию `None`.
        stop (Union[str, list[str]], optional): Список стоп-слов. По умолчанию `None`.
        stream (bool, optional): Флаг, указывающий на использование потоковой передачи данных. По умолчанию `False`.
        prompt (str, optional): Дополнительный промпт для запроса. По умолчанию `None`.
        headers (dict, optional): Дополнительные заголовки запроса. По умолчанию `None`.
        impersonate (str, optional): Пользователь для имитации. По умолчанию `None`.
        extra_parameters (list[str], optional): Список дополнительных параметров для передачи в запросе.
        extra_data (dict, optional): Словарь дополнительных данных для передачи в запросе.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор для получения ответов от API OpenAI.

    Raises:
        MissingAuthError: Если отсутствует ключ API и требуется аутентификация.
        ResponseError: Если получен неподдерживаемый content-type ответа.

    Как работает функция:
    - Проверяет наличие ключа API и выбрасывает исключение, если он отсутствует и требуется аутентификация.
    - Инициализирует асинхронную сессию для выполнения запросов.
    - Определяет модель для использования, используя `cls.get_model`.
    - Если модель поддерживает генерацию изображений, формирует запрос к API для генерации изображений и возвращает URL изображений.
    - Формирует данные запроса, включая сообщения, параметры temperature, max_tokens, top_p и другие.
    - Выполняет POST-запрос к API OpenAI и обрабатывает ответ в зависимости от content-type.
    - Для `application/json` парсит JSON и извлекает контент сообщения, информацию об использовании и причину завершения.
    - Для `text/event-stream` обрабатывает потоковые данные, извлекая дельты контента, информацию об использовании и причину завершения.
    - Возвращает асинхронный генератор для получения ответов от API OpenAI.

    Примеры:
        >>> async for message in OpenaiTemplate.create_async_generator(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello, how are you?"}]):
        ...     print(message)
    """
    ...
```

### `OpenaiTemplate.get_headers`

```python
@classmethod
def get_headers(cls, stream: bool, api_key: str = None, headers: dict = None) -> dict:
    """
    Формирует заголовки запроса для API OpenAI.

    Args:
        stream (bool): Флаг, указывающий на использование потоковой передачи данных.
        api_key (str, optional): Ключ API для аутентификации. По умолчанию `None`.
        headers (dict, optional): Дополнительные заголовки запроса. По умолчанию `None`.

    Returns:
        dict: Словарь с заголовками запроса.

    Как работает функция:
    - Формирует базовые заголовки, включая Accept и Content-Type.
    - Добавляет заголовок Authorization с ключом API, если он предоставлен.
    - Объединяет базовые заголовки с дополнительными заголовками, если они предоставлены.
    """
    ...