# Module `Dynaspark.py`

## Обзор

Модуль предназначен для работы с провайдером Dynaspark, который предоставляет доступ к различным моделям, включая Gemini.
Он поддерживает как текстовые запросы, так и запросы с использованием изображений. Модуль использует асинхронные запросы для взаимодействия с API Dynaspark.

## Детали

Модуль содержит класс `Dynaspark`, который наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`.
Он реализует методы для создания асинхронного генератора, который отправляет запросы к API Dynaspark и возвращает ответы.
Модуль также поддерживает работу через прокси и отправку изображений вместе с текстовыми запросами.

## Классы

### `Dynaspark`

**Описание**: Класс для работы с провайдером Dynaspark.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает поддержку асинхронных генераторов.
- `ProviderModelMixin`: Предоставляет общие методы для работы с моделями.

**Атрибуты**:
- `url` (str): URL Dynaspark.
- `login_url` (str | None): URL для логина (в данном случае `None`, так как аутентификация не требуется).
- `api_endpoint` (str): URL API Dynaspark для генерации ответов.
- `working` (bool): Флаг, указывающий, что провайдер работает.
- `needs_auth` (bool): Флаг, указывающий, требуется ли аутентификация (в данном случае `False`).
- `use_nodriver` (bool): Флаг, указывающий, что не требуется веб-драйвер.
- `supports_stream` (bool): Флаг, указывающий, что поддерживается потоковая передача данных.
- `supports_system_message` (bool): Флаг, указывающий, что поддерживаются системные сообщения (в данном случае `False`).
- `supports_message_history` (bool): Флаг, указывающий, что поддерживается история сообщений (в данном случае `False`).
- `default_model` (str): Модель по умолчанию (`gemini-1.5-flash`).
- `default_vision_model` (str): Модель по умолчанию для работы с изображениями (совпадает с `default_model`).
- `vision_models` (list[str]): Список моделей, поддерживающих работу с изображениями.
- `models` (list[str]): Список всех поддерживаемых моделей (совпадает с `vision_models`).
- `model_aliases` (dict[str, str]): Словарь с псевдонимами моделей.

**Принцип работы**:
Класс использует `aiohttp.ClientSession` для выполнения асинхронных POST-запросов к API Dynaspark.
Он формирует данные запроса в формате `FormData`, добавляя текстовые сообщения и, при необходимости, изображения.
Ответ от API возвращается в формате JSON, из которого извлекается текст ответа.

## Методы класса

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    media: MediaListType = None,
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для взаимодействия с API Dynaspark.

    Args:
        cls (Type[Dynaspark]): Ссылка на класс Dynaspark.
        model (str): Используемая модель.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        media (MediaListType, optional): Список медиафайлов (изображений) для отправки. По умолчанию `None`.
        **kwargs: Дополнительные аргументы (не используются).

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий текст ответа от API.

    How the function works:
    1.  Создает заголовки запроса, включая `User-Agent` и `Origin`.
    2.  Инициализирует `aiohttp.ClientSession` с заданными заголовками.
    3.  Формирует данные запроса в формате `FormData`, добавляя текстовые сообщения и модель.
    4.  Если переданы медиафайлы, добавляет их в `FormData`.
    5.  Выполняет POST-запрос к API Dynaspark.
    6.  Обрабатывает ответ, извлекая текст ответа из JSON.
    7.  Возвращает асинхронный генератор, который выдает текст ответа.

    Пример:
        >>> model = 'gemini-1.5-flash'
        >>> messages = [{'role': 'user', 'content': 'Hello, world!'}]
        >>> async for message in Dynaspark.create_async_generator(model=model, messages=messages):
        ...     print(message)
        <Текст ответа от API>
    """
    ...
```

## Параметры класса `Dynaspark`

- `url` (str): URL базовый адрес сервиса Dynaspark.
- `login_url` (str | None): URL адрес страницы входа в сервис. В данном случае не используется.
- `api_endpoint` (str): URL адрес API для генерации ответов.
- `working` (bool): Флаг, указывающий на работоспособность сервиса.
- `needs_auth` (bool): Флаг, указывающий на необходимость аутентификации.
- `use_nodriver` (bool): Флаг, указывающий на использование без веб-драйвера.
- `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи.
- `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений.
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений.
- `default_model` (str): Модель, используемая по умолчанию.
- `default_vision_model` (str): Модель для работы с изображениями, используемая по умолчанию.
- `vision_models` (list[str]): Список поддерживаемых моделей для работы с изображениями.
- `models` (list[str]): Список всех поддерживаемых моделей.
- `model_aliases` (dict[str, str]): Псевдонимы моделей.

## Примеры

Пример использования класса `Dynaspark` для отправки запроса к API:

```python
model = 'gemini-1.5-flash'
messages = [{'role': 'user', 'content': 'Hello, world!'}]
async for message in Dynaspark.create_async_generator(model=model, messages=messages):
    print(message)