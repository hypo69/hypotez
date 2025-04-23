# Модуль Anthropic

## Обзор

Модуль `Anthropic` предоставляет класс `Anthropic`, который является адаптером для работы с API Anthropic. Он наследуется от класса `OpenaiAPI` и реализует методы для взаимодействия с моделями Anthropic, включая поддержку потоковой передачи, системных сообщений и истории сообщений. Модуль предназначен для использования в проектах, требующих интеграции с API Anthropic для обработки текстовых запросов и изображений.

## Подробнее

Модуль предоставляет функциональность для аутентификации, запроса моделей, создания асинхронных генераторов для обмена сообщениями с API Anthropic. Он обрабатывает мультимедийные данные, такие как изображения, и поддерживает использование инструментов (tools) для расширения возможностей модели.

## Классы

### `Anthropic`

**Описание**: Класс `Anthropic` является адаптером для работы с API Anthropic. Он предоставляет методы для взаимодействия с моделями Anthropic, включая поддержку потоковой передачи, системных сообщений и истории сообщений.

**Наследует**: `OpenaiAPI`

**Атрибуты**:
- `label` (str): Метка, идентифицирующая провайдера API ("Anthropic API").
- `url` (str): URL главной страницы Anthropic ("https://console.anthropic.com").
- `login_url` (str): URL страницы для получения ключей API ("https://console.anthropic.com/settings/keys").
- `working` (bool): Флаг, указывающий, работает ли провайдер API (True).
- `api_base` (str): Базовый URL API Anthropic ("https://api.anthropic.com/v1").
- `needs_auth` (bool): Флаг, указывающий, требуется ли аутентификация (True).
- `supports_stream` (bool): Флаг, указывающий, поддерживается ли потоковая передача (True).
- `supports_system_message` (bool): Флаг, указывающий, поддерживаются ли системные сообщения (True).
- `supports_message_history` (bool): Флаг, указывающий, поддерживается ли история сообщений (True).
- `default_model` (str): Модель, используемая по умолчанию ("claude-3-5-sonnet-latest").
- `models` (list[str]): Список поддерживаемых моделей.
- `models_aliases` (dict[str, str]): Словарь псевдонимов моделей для удобства использования.

**Принцип работы**:

Класс `Anthropic` предназначен для взаимодействия с API Anthropic. Он использует HTTP-запросы для отправки и получения данных от API. Класс поддерживает различные функции, такие как потоковая передача, системные сообщения и историю сообщений.

**Методы**:

- `get_models(api_key: str = None, **kwargs)`: Возвращает список доступных моделей.
- `create_async_generator(model: str, messages: Messages, proxy: str = None, timeout: int = 120, media: MediaListType = None, api_key: str = None, temperature: float = None, max_tokens: int = 4096, top_k: int = None, top_p: float = None, stop: list[str] = None, stream: bool = False, headers: dict = None, impersonate: str = None, tools: Optional[list] = None, extra_data: dict = {}) -> AsyncResult`: Создает асинхронный генератор для взаимодействия с API Anthropic.
- `get_headers(stream: bool, api_key: str = None, headers: dict = None) -> dict`: Возвращает заголовки, необходимые для запросов к API Anthropic.

## Методы класса

### `get_models`

```python
@classmethod
def get_models(cls, api_key: str = None, **kwargs) -> list[str]:
    """
    Функция получает список доступных моделей от API Anthropic.

    Args:
        api_key (str, optional): Ключ API для аутентификации. По умолчанию `None`.

    Returns:
        list[str]: Список идентификаторов доступных моделей.

    Raises:
        requests.exceptions.HTTPError: Если HTTP-запрос завершается с ошибкой.

    Как работает функция:
        - Функция отправляет GET-запрос к API Anthropic для получения списка моделей.
        - Если список моделей еще не был получен, он запрашивается у API и кэшируется.
        - Если запрос к API возвращает ошибку, вызывается исключение.

    Примеры:
        >>> Anthropic.get_models(api_key='ключ_api')
        ['claude-3-opus-latest', 'claude-3-sonnet-latest', ...]
    """
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
    """
    Функция создает асинхронный генератор для взаимодействия с API Anthropic.

    Args:
        model (str): Идентификатор модели для использования.
        messages (Messages): Список сообщений для отправки в API.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        timeout (int, optional): Время ожидания запроса в секундах. По умолчанию 120.
        media (MediaListType, optional): Список медиафайлов для отправки. По умолчанию `None`.
        api_key (str, optional): Ключ API для аутентификации. По умолчанию `None`.
        temperature (float, optional): Температура для управления случайностью генерации текста. По умолчанию `None`.
        max_tokens (int, optional): Максимальное количество токенов в ответе. По умолчанию 4096.
        top_k (int, optional): Параметр top_k для управления разнообразием выборки. По умолчанию `None`.
        top_p (float, optional): Параметр top_p для управления разнообразием выборки. По умолчанию `None`.
        stop (list[str], optional): Список стоп-последовательностей, при которых генерация текста должна остановиться. По умолчанию `None`.
        stream (bool, optional): Флаг, указывающий, использовать ли потоковую передачу. По умолчанию `False`.
        headers (dict, optional): Дополнительные заголовки для запроса. По умолчанию `None`.
        impersonate (str, optional): Идентификатор для имитации. По умолчанию `None`.
        tools (Optional[list], optional): Список инструментов для использования. По умолчанию `None`.
        extra_data (dict, optional): Дополнительные данные для отправки в запросе. По умолчанию `{}`.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий результаты от API.

    Raises:
        MissingAuthError: Если не предоставлен ключ API.

    Как работает функция:
        - Функция проверяет наличие ключа API. Если ключ отсутствует, вызывается исключение.
        - Если предоставлены медиафайлы, они кодируются в base64 и добавляются в сообщение.
        - Функция отправляет POST-запрос к API Anthropic с параметрами, указанными в аргументах.
        - Если включена потоковая передача, функция возвращает асинхронный генератор, который возвращает чанки данных по мере их поступления от API.
        - Если потоковая передача не включена, функция возвращает полный ответ от API.

    Примеры:
        >>> async for chunk in Anthropic.create_async_generator(model='claude-3-opus-latest', messages=[{'role': 'user', 'content': 'Привет' }], api_key='ключ_api'):
        ...     print(chunk)
        Привет!
        >>> async for chunk in Anthropic.create_async_generator(model='claude-3-opus-latest', messages=[{'role': 'user', 'content': 'Привет' }], api_key='ключ_api', stream=True):
        ...     print(chunk)
        Привет!
    """
```

### `get_headers`

```python
@classmethod
def get_headers(cls, stream: bool, api_key: str = None, headers: dict = None) -> dict:
    """
    Функция создает заголовки для HTTP-запроса к API Anthropic.

    Args:
        stream (bool): Флаг, указывающий, использовать ли потоковую передачу.
        api_key (str, optional): Ключ API для аутентификации. По умолчанию `None`.
        headers (dict, optional): Дополнительные заголовки для добавления. По умолчанию `None`.

    Returns:
        dict: Словарь заголовков для HTTP-запроса.

    Как работает функция:
        - Функция создает словарь заголовков, включающий `Accept`, `Content-Type`, `x-api-key` и `anthropic-version`.
        - Если включена потоковая передача, `Accept` устанавливается в `text/event-stream`.
        - Если предоставлен ключ API, он добавляется в заголовок `x-api-key`.
        - Дополнительные заголовки объединяются с основными заголовками.

    Примеры:
        >>> Anthropic.get_headers(stream=True, api_key='ключ_api')
        {'Accept': 'text/event-stream', 'Content-Type': 'application/json', 'x-api-key': 'ключ_api', 'anthropic-version': '2023-06-01'}
        >>> Anthropic.get_headers(stream=False)
        {'Accept': 'application/json', 'Content-Type': 'application/json', 'anthropic-version': '2023-06-01'}
    """
```

## Параметры класса

- `label` (str): Метка, идентифицирующая провайдера API ("Anthropic API").
- `url` (str): URL главной страницы Anthropic ("https://console.anthropic.com").
- `login_url` (str): URL страницы для получения ключей API ("https://console.anthropic.com/settings/keys").
- `working` (bool): Флаг, указывающий, работает ли провайдер API (True).
- `api_base` (str): Базовый URL API Anthropic ("https://api.anthropic.com/v1").
- `needs_auth` (bool): Флаг, указывающий, требуется ли аутентификация (True).
- `supports_stream` (bool): Флаг, указывающий, поддерживается ли потоковая передача (True).
- `supports_system_message` (bool): Флаг, указывающий, поддерживаются ли системные сообщения (True).
- `supports_message_history` (bool): Флаг, указывающий, поддерживается ли история сообщений (True).
- `default_model` (str): Модель, используемая по умолчанию ("claude-3-5-sonnet-latest").
- `models` (list[str]): Список поддерживаемых моделей.
- `models_aliases` (dict[str, str]): Словарь псевдонимов моделей для удобства использования.

## Примеры

Примеры использования класса и его методов:

```python
# Пример получения списка моделей
models = Anthropic.get_models(api_key='ключ_api')
print(models)

# Пример создания асинхронного генератора для взаимодействия с API Anthropic
async def main():
    async for chunk in Anthropic.create_async_generator(
        model='claude-3-opus-latest',
        messages=[{'role': 'user', 'content': 'Привет'}],
        api_key='ключ_api',
        stream=True
    ):
        print(chunk)

# Запуск асинхронной функции
import asyncio
asyncio.run(main())