# Модуль Anthropic

## Обзор

Модуль `Anthropic` предоставляет интерфейс для взаимодействия с API Anthropic, используя класс `OpenaiAPI` в качестве основы. Он поддерживает текстовые и мультимедийные запросы, потоковую передачу данных и использование инструментов. Модуль предназначен для интеграции с платформой GPT4Free, обеспечивая доступ к моделям Anthropic Claude.

## Более подробно

Этот модуль реализует функциональность для аутентификации и взаимодействия с API Anthropic. Он включает поддержку различных моделей, таких как Claude 3 Sonnet, Haiku и Opus. Модуль обеспечивает асинхронную генерацию контента, обработку мультимедийных данных и потоковую передачу ответов. Он также обрабатывает ошибки и предоставляет заголовки для запросов к API Anthropic.

## Классы

### `Anthropic`

**Описание**: Класс `Anthropic` расширяет `OpenaiAPI` и предоставляет методы для взаимодействия с API Anthropic.

**Наследует**:
- `OpenaiAPI`: Предоставляет базовую функциональность для взаимодействия с API OpenAI.

**Атрибуты**:
- `label` (str): Метка API ("Anthropic API").
- `url` (str): URL консоли Anthropic ("https://console.anthropic.com").
- `login_url` (str): URL страницы входа в Anthropic ("https://console.anthropic.com/settings/keys").
- `working` (bool): Указывает, что API работает (True).
- `api_base` (str): Базовый URL API Anthropic ("https://api.anthropic.com/v1").
- `needs_auth` (bool): Указывает, требуется ли аутентификация (True).
- `supports_stream` (bool): Указывает, поддерживает ли API потоковую передачу (True).
- `supports_system_message` (bool): Указывает, поддерживает ли API системные сообщения (True).
- `supports_message_history` (bool): Указывает, поддерживает ли API историю сообщений (True).
- `default_model` (str): Модель, используемая по умолчанию ("claude-3-5-sonnet-latest").
- `models` (list[str]): Список поддерживаемых моделей.
- `models_aliases` (dict[str, str]): Псевдонимы для моделей.

**Принцип работы**:
Класс `Anthropic` предоставляет методы для получения списка доступных моделей, создания асинхронных генераторов для взаимодействия с API и формирования заголовков запросов. Он также обрабатывает ответы API и возвращает результаты в формате, совместимом с GPT4Free.

**Методы**:
- `get_models(api_key: str = None, **kwargs)`: Возвращает список доступных моделей.
- `create_async_generator(model: str, messages: Messages, proxy: str = None, timeout: int = 120, media: MediaListType = None, api_key: str = None, temperature: float = None, max_tokens: int = 4096, top_k: int = None, top_p: float = None, stop: list[str] = None, stream: bool = False, headers: dict = None, impersonate: str = None, tools: Optional[list] = None, extra_data: dict = {}, **kwargs) -> AsyncResult`: Создает асинхронный генератор для взаимодействия с API.
- `get_headers(stream: bool, api_key: str = None, headers: dict = None) -> dict`: Формирует заголовки для запросов к API.

## Методы класса

### `get_models`

```python
@classmethod
def get_models(cls, api_key: str = None, **kwargs) -> list[str]:
    """
    Получает список доступных моделей из API Anthropic.

    Args:
        api_key (str, optional): Ключ API для аутентификации. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        list[str]: Список идентификаторов доступных моделей.

    Raises:
        requests.exceptions.HTTPError: Если HTTP-запрос завершается с ошибкой.

    Как работает:
    - Функция проверяет, был ли уже получен список моделей. Если да, то возвращает его.
    - Если список моделей не был получен, функция отправляет GET-запрос к API Anthropic для получения списка моделей.
    - Функция извлекает идентификаторы моделей из JSON-ответа и сохраняет их в атрибуте класса `models`.
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
    """
    Создает асинхронный генератор для взаимодействия с API Anthropic.

    Args:
        model (str): Идентификатор модели для использования.
        messages (Messages): Список сообщений для отправки в API.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        timeout (int, optional): Время ожидания запроса в секундах. По умолчанию 120.
        media (MediaListType, optional): Список мультимедийных файлов для отправки. По умолчанию `None`.
        api_key (str, optional): Ключ API для аутентификации. По умолчанию `None`.
        temperature (float, optional): Температура для управления случайностью генерации. По умолчанию `None`.
        max_tokens (int, optional): Максимальное количество токенов в ответе. По умолчанию 4096.
        top_k (int, optional): Параметр top_k. По умолчанию `None`.
        top_p (float, optional): Параметр top_p. По умолчанию `None`.
        stop (list[str], optional): Список стоп-последовательностей. По умолчанию `None`.
        stream (bool, optional): Указывает, использовать ли потоковую передачу. По умолчанию `False`.
        headers (dict, optional): Дополнительные заголовки для запроса. По умолчанию `None`.
        impersonate (str, optional): Имитация пользователя. По умолчанию `None`.
        tools (Optional[list], optional): Список инструментов для использования. По умолчанию `None`.
        extra_data (dict, optional): Дополнительные данные для запроса. По умолчанию `{}`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий фрагменты ответа от API.

    Raises:
        MissingAuthError: Если не указан ключ API.
        requests.exceptions.HTTPError: Если HTTP-запрос завершается с ошибкой.

    Как работает:
    - Функция проверяет наличие ключа API. Если ключ отсутствует, вызывается исключение `MissingAuthError`.
    - Если переданы мультимедийные файлы, они кодируются в base64 и добавляются в сообщение.
    - Функция формирует данные для запроса, включая сообщения, модель, параметры генерации и другие настройки.
    - Отправляется POST-запрос к API Anthropic с использованием `StreamSession`.
    - Функция обрабатывает потоковые и не потоковые ответы, возвращая фрагменты контента, информацию об использовании и результаты вызовов инструментов.

    Внутренние функции:
    - Отсутствуют.
    """
    ...
```

### `get_headers`

```python
@classmethod
def get_headers(cls, stream: bool, api_key: str = None, headers: dict = None) -> dict:
    """
    Формирует заголовки для запросов к API Anthropic.

    Args:
        stream (bool): Указывает, используется ли потоковая передача.
        api_key (str, optional): Ключ API для аутентификации. По умолчанию `None`.
        headers (dict, optional): Дополнительные заголовки. По умолчанию `None`.

    Returns:
        dict: Словарь заголовков для запроса.

    Как работает:
    - Функция формирует словарь заголовков, включая `Accept`, `Content-Type`, `x-api-key` и `anthropic-version`.
    - Заголовки включают поддержку потоковой передачи, ключ API (если указан) и версию API Anthropic.
    """
    ...
```

## Параметры класса

- `label` (str): Метка API ("Anthropic API").
- `url` (str): URL консоли Anthropic ("https://console.anthropic.com").
- `login_url` (str): URL страницы входа в Anthropic ("https://console.anthropic.com/settings/keys").
- `working` (bool): Указывает, что API работает (True).
- `api_base` (str): Базовый URL API Anthropic ("https://api.anthropic.com/v1").
- `needs_auth` (bool): Указывает, требуется ли аутентификация (True).
- `supports_stream` (bool): Указывает, поддерживает ли API потоковую передачу (True).
- `supports_system_message` (bool): Указывает, поддерживает ли API системные сообщения (True).
- `supports_message_history` (bool): Указывает, поддерживает ли API историю сообщений (True).
- `default_model` (str): Модель, используемая по умолчанию ("claude-3-5-sonnet-latest").
- `models` (list[str]): Список поддерживаемых моделей.
- `models_aliases` (dict[str, str]): Псевдонимы для моделей.

**Примеры**:
```python
# Пример получения списка моделей
models = Anthropic.get_models(api_key="your_api_key")
print(models)

# Пример создания асинхронного генератора (не выполняется из-за отсутствия зависимостей)
# async def main():
#     generator = await Anthropic.create_async_generator(
#         model="claude-3-opus-latest",
#         messages=[{"role": "user", "content": "Hello, Anthropic!"}],
#         api_key="your_api_key"
#     )
#     async for message in generator:
#         print(message)