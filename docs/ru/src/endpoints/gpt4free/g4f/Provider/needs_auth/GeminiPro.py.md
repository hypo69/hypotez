# Модуль `GeminiPro.py`

## Обзор

Модуль `GeminiPro.py` предназначен для взаимодействия с API Google Gemini для генерации контента. Он предоставляет асинхронный генератор для получения ответов от модели Gemini, поддерживает передачу истории сообщений, системные сообщения и аутентификацию через API-ключ. Также, он включает в себя функциональность для работы с мультимедийными данными.

## Подробней

Этот модуль является частью проекта `hypotez` и обеспечивает интеграцию с моделями Gemini от Google. Он использует асинхронные запросы для эффективного взаимодействия с API и предоставляет удобный интерфейс для отправки запросов и получения ответов в режиме реального времени.

## Классы

### `GeminiPro`

**Описание**: Класс `GeminiPro` реализует асинхронного провайдера для работы с API Google Gemini.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию контента.
- `ProviderModelMixin`: Добавляет функциональность выбора и управления моделями.

**Атрибуты**:
- `label` (str): Метка провайдера - "Google Gemini API".
- `url` (str): URL главной страницы Google AI - "https://ai.google.dev".
- `login_url` (str): URL для получения API-ключа - "https://aistudio.google.com/u/0/apikey".
- `api_base` (str): Базовый URL API - "https://generativelanguage.googleapis.com/v1beta".
- `working` (bool): Указывает, что провайдер в рабочем состоянии.
- `supports_message_history` (bool): Поддержка истории сообщений.
- `supports_system_message` (bool): Поддержка системных сообщений.
- `needs_auth` (bool): Требуется аутентификация.
- `default_model` (str): Модель по умолчанию - "gemini-1.5-pro".
- `default_vision_model` (str): Модель для работы с изображениями по умолчанию - "gemini-1.5-pro".
- `fallback_models` (list[str]): Список запасных моделей.
- `model_aliases` (dict[str, str]): Псевдонимы моделей для удобства использования.

**Методы**:
- `get_models()`: Получает список доступных моделей Gemini.
- `create_async_generator()`: Создает асинхронный генератор для взаимодействия с API Gemini.

## Методы класса

### `get_models`

```python
@classmethod
def get_models(cls, api_key: str = None, api_base: str = api_base) -> list[str]:
    """
    Получает список доступных моделей Gemini.

    Args:
        api_key (str, optional): API-ключ для аутентификации. По умолчанию `None`.
        api_base (str, optional): Базовый URL API. По умолчанию используется значение атрибута класса `api_base`.

    Returns:
        list[str]: Список доступных моделей Gemini.

    Raises:
        MissingAuthError: Если `api_key` недействителен.

    
    - Функция пытается получить список доступных моделей Gemini, используя предоставленный `api_key`.
    - Если список моделей уже был получен ранее и сохранен в `cls.models`, функция возвращает сохраненный список.
    - В случае ошибки при запросе к API, функция логирует ошибку и возвращает список запасных моделей (`cls.fallback_models`).
    """
```

**Примеры**:
```python
models = GeminiPro.get_models(api_key='your_api_key')
print(models)  # Вывод: список доступных моделей Gemini
```

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    stream: bool = False,
    proxy: str = None,
    api_key: str = None,
    api_base: str = api_base,
    use_auth_header: bool = False,
    media: MediaListType = None,
    tools: Optional[list] = None,
    connector: BaseConnector = None,
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для взаимодействия с API Gemini.

    Args:
        model (str): Название используемой модели.
        messages (Messages): Список сообщений для отправки в API.
        stream (bool, optional): Флаг для включения потоковой передачи. По умолчанию `False`.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        api_key (str, optional): API-ключ для аутентификации. По умолчанию `None`.
        api_base (str, optional): Базовый URL API. По умолчанию используется значение атрибута класса `api_base`.
        use_auth_header (bool, optional): Использовать заголовок авторизации. По умолчанию `False`.
        media (MediaListType, optional): Список медиафайлов для отправки. По умолчанию `None`.
        tools (Optional[list], optional): Список инструментов (функций), которые можно использовать. По умолчанию `None`.
        connector (BaseConnector, optional): Кастомный коннектор aiohttp. По умолчанию `None`.
        **kwargs: Дополнительные параметры для конфигурации генерации контента.

    Returns:
        AsyncResult: Асинхронный генератор для получения ответов от API.

    Raises:
        MissingAuthError: Если отсутствует `api_key`.
        RuntimeError: Если возникает ошибка при запросе к API.

    
    - Функция создает асинхронный генератор для взаимодействия с API Gemini.
    - Она проверяет наличие `api_key` и вызывает исключение `MissingAuthError`, если ключ отсутствует.
    - Формирует URL для запроса в зависимости от выбранной модели и метода (stream или generateContent).
    - Преобразует список сообщений в формат, требуемый API Gemini, и включает медиафайлы, если они предоставлены.
    - Отправляет асинхронный запрос к API и обрабатывает ответ, возвращая результаты в виде асинхронного генератора.
    """
```

**Примеры**:
```python
messages = [
    {"role": "user", "content": "Hello, Gemini!"}
]
generator = await GeminiPro.create_async_generator(model='gemini-1.5-pro', messages=messages, api_key='your_api_key')
async for response in generator:
    print(response)  # Вывод: ответ от Gemini
```

## Параметры класса

- `label` (str): Метка провайдера.
- `url` (str): URL главной страницы Google AI.
- `login_url` (str): URL для получения API-ключа.
- `api_base` (str): Базовый URL API.
- `working` (bool): Индикатор рабочего состояния провайдера.
- `supports_message_history` (bool): Поддержка истории сообщений.
- `supports_system_message` (bool): Поддержка системных сообщений.
- `needs_auth` (bool): Требуется ли аутентификация.
- `default_model` (str): Модель, используемая по умолчанию.
- `default_vision_model` (str): Модель для работы с изображениями по умолчанию.
- `fallback_models` (list[str]): Список запасных моделей.
- `model_aliases` (dict[str, str]): Псевдонимы моделей.