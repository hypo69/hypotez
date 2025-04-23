# Модуль `DeepSeekAPI.py`

## Обзор

Модуль `DeepSeekAPI.py` предназначен для взаимодействия с API DeepSeek для создания чат-сессий и получения ответов от модели DeepSeek. Он использует асинхронные запросы и предоставляет функциональность для аутентификации и обмена сообщениями с API. Модуль также поддерживает веб-поиск и отображение промежуточных результатов "размышлений" модели.

## Подробнее

Модуль предоставляет класс `DeepSeekAPI`, который наследуется от `AsyncAuthedProvider` и `ProviderModelMixin`. Он реализует методы для аутентификации, создания чат-сессий и обмена сообщениями с API DeepSeek. Модуль использует библиотеку `dsk.api` для взаимодействия с API DeepSeek и `nodriver` для аутентификации.

## Классы

### `DeepSeekAPI`

**Описание**: Класс для взаимодействия с API DeepSeek.

**Наследует**:
- `AsyncAuthedProvider`: Предоставляет асинхронную аутентификацию для провайдера.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями провайдера.

**Атрибуты**:
- `url` (str): URL API DeepSeek.
- `working` (bool): Флаг, указывающий, работает ли провайдер.
- `needs_auth` (bool): Флаг, указывающий, требуется ли аутентификация.
- `use_nodriver` (bool): Флаг, указывающий, используется ли `nodriver` для аутентификации.
- `_access_token` (str): Токен доступа для аутентификации.
- `default_model` (str): Модель, используемая по умолчанию.
- `models` (list): Список поддерживаемых моделей.
- `browser`: Инстанс браузера для аутентификации через nodriver.
- `stop_browser`: Функция для остановки браузера, используемого для аутентификации.

**Методы**:

- `on_auth_async()`: Асинхронный метод для аутентификации.
- `create_authed()`: Асинхронный метод для создания аутентифицированного запроса.

## Методы класса

### `on_auth_async`

```python
@classmethod
async def on_auth_async(cls, proxy: str = None, **kwargs) -> AsyncIterator:
    """Асинхронно выполняет процесс аутентификации для DeepSeek API.

    Args:
        proxy (str, optional): Прокси-сервер для использования при подключении. По умолчанию `None`.
        **kwargs: Дополнительные аргументы, которые могут быть переданы.

    Yields:
        RequestLogin: Объект, содержащий информацию о запросе на логин.
        AuthResult: Объект, содержащий результат аутентификации.

    Raises:
        ImportError: Если библиотека `dsk.api` не установлена.

    
    - Проверяется наличие атрибута `browser` у класса. Если его нет, то запускается `nodriver` для эмуляции браузера.
    - Отправляется запрос на логин.
    - Запускается асинхронная задача `callback`, которая ожидает появления токена доступа в `localStorage` браузера.
    - Как только токен получен, он сохраняется в атрибуте `_access_token` класса.
    - Возвращается результат аутентификации.

    Внутренние функции:
    - `callback(page)`: Асинхронная функция, которая ожидает появления токена доступа в `localStorage` браузера.

        Args:
            page: Объект страницы браузера, предоставленный `nodriver`.

        Как работает внутренняя функция:
        - В бесконечном цикле проверяется наличие токена доступа в `localStorage` страницы браузера.
        - Если токен найден, он сохраняется в атрибуте `_access_token` класса и цикл прерывается.

    Примеры:
        Пример вызова `on_auth_async`::

            async for result in DeepSeekAPI.on_auth_async(proxy='http://proxy.example.com'):
                print(result)
    """
```

### `create_authed`

```python
@classmethod
async def create_authed(
    cls,
    model: str,
    messages: Messages,
    auth_result: AuthResult,
    conversation: JsonConversation = None,
    web_search: bool = False,
    **kwargs
) -> AsyncResult:
    """Создает аутентифицированный запрос к API DeepSeek.

    Args:
        model (str): Название используемой модели.
        messages (Messages): Список сообщений для отправки в API.
        auth_result (AuthResult): Результат аутентификации, содержащий токен доступа.
        conversation (JsonConversation, optional): Объект, представляющий текущую беседу. По умолчанию `None`.
        web_search (bool, optional): Флаг, указывающий, следует ли использовать веб-поиск. По умолчанию `False`.
        **kwargs: Дополнительные аргументы, которые могут быть переданы.

    Yields:
        conversation (JsonConversation): Объект, содержащий информацию о текущей беседе.
        Reasoning (str): Промежуточные результаты "размышлений" модели.
        str: Ответ от API DeepSeek.
        FinishReason (str): Причина завершения беседы.

    Raises:
        ImportError: Если библиотека `dsk.api` не установлена.

    
    - Инициализируется API DeepSeek с использованием токена доступа из `auth_result`.
    - Если `conversation` равен `None`, создается новая чат-сессия и объект `JsonConversation`.
    - Отправляется запрос на завершение чата.
    - Функция генерирует результаты в зависимости от типа получаемого чанка:
        - Если чанк имеет тип `'thinking'`, генерируется `Reasoning` с промежуточными результатами "размышлений" модели.
        - Если чанк имеет тип `'text'`, генерируется текст ответа от API.
        - Если чанк содержит причину завершения (`'finish_reason'`), генерируется `FinishReason`.

    Примеры:
        Пример вызова `create_authed`::

            auth_result = AuthResult(api_key='your_api_key')
            messages = [{'role': 'user', 'content': 'Hello, world!'}]
            async for result in DeepSeekAPI.create_authed(model='deepseek-v3', messages=messages, auth_result=auth_result):
                print(result)
    """
```

## Параметры класса

- `url` (str): URL API DeepSeek.
- `working` (bool): Флаг, указывающий, работает ли провайдер.
- `needs_auth` (bool): Флаг, указывающий, требуется ли аутентификация.
- `use_nodriver` (bool): Флаг, указывающий, используется ли `nodriver` для аутентификации.
- `_access_token` (str): Токен доступа для аутентификации.
- `default_model` (str): Модель, используемая по умолчанию.
- `models` (list): Список поддерживаемых моделей.
- `browser`: Инстанс браузера для аутентификации через nodriver.
- `stop_browser`: Функция для остановки браузера, используемого для аутентификации.

## Примеры

Пример использования класса `DeepSeekAPI`::

    from src.endpoints.gpt4free.g4f.Provider.needs_auth import DeepSeekAPI
    from src.endpoints.gpt4free.g4f.providers.response import AuthResult, JsonConversation
    from src.endpoints.gpt4free.g4f.typing import Messages

    # Пример аутентификации
    async def authenticate():
        async for result in DeepSeekAPI.on_auth_async(proxy='http://proxy.example.com'):
            print(result)
            if isinstance(result, AuthResult):
                auth_result = result
                break

        # Пример создания запроса
        if auth_result:
            messages: Messages = [{'role': 'user', 'content': 'Hello, world!'}]
            async for chunk in DeepSeekAPI.create_authed(model='deepseek-v3', messages=messages, auth_result=auth_result):
                print(chunk)