# Модуль для работы с Google Gemini API
================================================

Модуль содержит класс :class:`GeminiPro`, который используется для взаимодействия с Google Gemini API для генерации контента, включая поддержку потоковой передачи, мультимодальных запросов (изображения) и инструментов (tools).

Пример использования
----------------------

```python
# Пример использования класса GeminiPro
# from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth import GeminiPro
# from hypotez.src.endpoints.gpt4free.g4f.typing import Messages, MediaListType
#
# messages: Messages = [{"role": "user", "content": "Hello, how are you?"}]
# media: MediaListType = None
#
# async def main():
#     generator = await GeminiPro.create_async_generator(
#         model="gemini-1.5-pro",
#         messages=messages,
#         stream=True,
#         api_key="YOUR_API_KEY",
#         media=media
#     )
#     async for item in generator:
#         print(item)
# Замените "YOUR_API_KEY" на ваш актуальный API ключ.
```

## Оглавление
- [Обзор](#обзор)
- [Подробнее](#подробнее)
- [Классы](#классы)
    - [GeminiPro](#geminipro)
- [Функции](#функции)
    - [get_models](#get_models)
    - [create_async_generator](#create_async_generator)

## Обзор

Модуль `GeminiPro` предоставляет интерфейс для взаимодействия с API Google Gemini. Он поддерживает как потоковую, так и не потоковую генерацию контента, а также позволяет передавать изображения в запросах. Класс `GeminiPro` реализует методы для получения списка доступных моделей и создания асинхронного генератора для получения ответов от API.

## Подробнее

Этот модуль является частью проекта `hypotez` и используется для интеграции с API Google Gemini, позволяя пользователям использовать модели Gemini для различных задач, таких как генерация текста, ответы на вопросы и обработка изображений. Он обеспечивает асинхронное взаимодействие с API, что позволяет эффективно использовать ресурсы и обрабатывать большое количество запросов.
Модуль обрабатывает аутентификацию через API ключ, поддерживает выбор модели и настройку параметров генерации контента, таких как температура, максимальное количество токенов и другие.

## Классы

### `GeminiPro`

**Описание**: Класс для взаимодействия с Google Gemini API.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию контента.
- `ProviderModelMixin`: Предоставляет методы для управления моделями.

**Атрибуты**:
- `label` (str): Название провайдера ("Google Gemini API").
- `url` (str): URL главной страницы Google AI.
- `login_url` (str): URL страницы для получения API ключа.
- `api_base` (str): Базовый URL для API запросов.
- `working` (bool): Флаг, указывающий, работает ли провайдер.
- `supports_message_history` (bool): Флаг, указывающий, поддерживает ли провайдер историю сообщений.
- `supports_system_message` (bool): Флаг, указывающий, поддерживает ли провайдер системные сообщения.
- `needs_auth` (bool): Флаг, указывающий, требуется ли аутентификация.
- `default_model` (str): Модель, используемая по умолчанию ("gemini-1.5-pro").
- `default_vision_model` (str): Модель для обработки изображений, используемая по умолчанию.
- `fallback_models` (list[str]): Список моделей, которые используются, если не удалось получить список моделей из API.
- `model_aliases` (dict[str, str]): Словарь псевдонимов моделей.

**Методы**:
- `get_models`: Получает список доступных моделей.
- `create_async_generator`: Создает асинхронный генератор для получения ответов от API.

## Функции

### `get_models`

```python
@classmethod
def get_models(cls, api_key: str = None, api_base: str = api_base) -> list[str]:
    """Получает список доступных моделей из API Google Gemini.

    Args:
        api_key (str, optional): API ключ для аутентификации. По умолчанию `None`.
        api_base (str, optional): Базовый URL для API запросов. По умолчанию `api_base`.

    Returns:
        list[str]: Список доступных моделей.

    Raises:
        MissingAuthError: Если `api_key` не указан и не удалось получить список моделей из API.

    Как работает функция:
    1. Проверяет, если список моделей уже получен. Если да, возвращает его.
    2. Если список моделей не получен, пытается получить его из API.
    3. Формирует URL для запроса списка моделей.
    4. Отправляет GET запрос к API.
    5. Обрабатывает ответ API, извлекая имена моделей.
    6. Если произошла ошибка при получении списка моделей, возвращает список fallback моделей.

    ASCII flowchart:
    Начало --> Проверка списка моделей (A)
    A -- Да --> Возврат списка моделей
    A -- Нет --> Формирование URL (B)
    B --> GET запрос к API (C)
    C -- Успех --> Обработка ответа (D) --> Извлечение имен моделей (E) --> Возврат списка моделей
    C -- Ошибка --> Обработка ошибки (F) --> Возврат fallback моделей

    Примеры:
        >>> GeminiPro.get_models(api_key="YOUR_API_KEY")
        ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-2.0-flash-exp', 'gemini-pro']
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
    """Создает асинхронный генератор для получения ответов от API Google Gemini.

    Args:
        model (str): Название модели для использования.
        messages (Messages): Список сообщений для отправки в API.
        stream (bool, optional): Флаг, указывающий, использовать ли потоковую передачу. По умолчанию `False`.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        api_key (str, optional): API ключ для аутентификации. По умолчанию `None`.
        api_base (str, optional): Базовый URL для API запросов. По умолчанию `api_base`.
        use_auth_header (bool, optional): Флаг, указывающий, использовать ли заголовок авторизации. По умолчанию `False`.
        media (MediaListType, optional): Список медиафайлов для отправки в API. По умолчанию `None`.
        tools (Optional[list], optional): Список инструментов (functions) для использования. По умолчанию `None`.
        connector (BaseConnector, optional): Aiohttp connector. По умолчанию `None`.
        **kwargs: Дополнительные параметры для передачи в API.

    Returns:
        AsyncResult: Асинхронный генератор для получения ответов от API.

    Raises:
        MissingAuthError: Если `api_key` не указан.
        RuntimeError: Если произошла ошибка при отправке запроса в API.

    Как работает функция:
    1. Проверяет наличие API ключа. Если ключ отсутствует, вызывает исключение MissingAuthError.
    2. Получает название модели для использования.
    3. Формирует заголовки и параметры запроса.
    4. Определяет метод API (streamGenerateContent или generateContent) в зависимости от параметра stream.
    5. Формирует URL для запроса.
    6. Создает асинхронную сессию с использованием aiohttp.
    7. Формирует данные запроса, включая сообщения, медиафайлы и параметры генерации.
    8. Отправляет POST запрос к API.
    9. Обрабатывает ответ API. Если используется потоковая передача, обрабатывает каждый чанк данных.
    10. Возвращает асинхронный генератор для получения ответов от API.

    ASCII flowchart:
    Начало --> Проверка API ключа (A)
    A -- Нет API ключа --> Вызов исключения MissingAuthError
    A -- Есть API ключ --> Получение названия модели (B)
    B --> Формирование заголовков и параметров (C)
    C --> Определение метода API (D)
    D --> Формирование URL (E)
    E --> Создание асинхронной сессии (F)
    F --> Формирование данных запроса (G)
    G --> POST запрос к API (H)
    H -- Успех --> Обработка ответа (I)
    H -- Ошибка --> Вызов исключения RuntimeError
    I -- Потоковая передача --> Обработка каждого чанка данных (J) --> Возврат ответа
    I -- Без потоковой передачи --> Обработка ответа целиком (K) --> Возврат ответа

    Примеры:
        >>> messages: Messages = [{"role": "user", "content": "Hello, how are you?"}]
        >>> import asyncio
        >>> async def main():
        ...     generator = await GeminiPro.create_async_generator(
        ...         model="gemini-1.5-pro",
        ...         messages=messages,
        ...         stream=True,
        ...         api_key="YOUR_API_KEY"
        ...     )
        ...     async for item in generator:
        ...         print(item)
        >>> asyncio.run(main())
    """
    ...