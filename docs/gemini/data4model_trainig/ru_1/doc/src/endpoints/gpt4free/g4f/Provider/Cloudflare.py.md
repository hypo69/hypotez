# Модуль для работы с Cloudflare AI
## Обзор

Модуль `Cloudflare` предоставляет асинхронный интерфейс для взаимодействия с API Cloudflare AI. Он поддерживает потоковую передачу, системные сообщения и историю сообщений. Этот модуль предназначен для использования в проекте `hypotez` для предоставления доступа к различным моделям Cloudflare AI.

## Подробнее

Модуль `Cloudflare` является частью проекта `hypotez` и предназначен для обеспечения взаимодействия с моделями искусственного интеллекта, предоставляемыми Cloudflare. Он использует асинхронные запросы для эффективной обработки данных и поддерживает потоковую передачу для снижения нагрузки на систему. В модуле реализована поддержка системных сообщений и истории сообщений, что позволяет более точно управлять контекстом диалога с AI-моделями.

## Классы

### `Cloudflare`

**Описание**: Класс `Cloudflare` предоставляет функциональность для взаимодействия с API Cloudflare AI. Он поддерживает асинхронные запросы, потоковую передачу и аутентификацию через файлы кэша.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет общие методы для работы с моделями.
- `AuthFileMixin`: Реализует функциональность аутентификации через файлы.

**Атрибуты**:
- `label` (str): Метка провайдера ("Cloudflare AI").
- `url` (str): URL для доступа к Cloudflare AI ("https://playground.ai.cloudflare.com").
- `working` (bool): Указывает, работает ли провайдер (True).
- `use_nodriver` (bool): Указывает, используется ли бездрайверный режим (True).
- `api_endpoint` (str): URL для API-инференса ("https://playground.ai.cloudflare.com/api/inference").
- `models_url` (str): URL для получения списка моделей ("https://playground.ai.cloudflare.com/api/models").
- `supports_stream` (bool): Поддержка потоковой передачи (True).
- `supports_system_message` (bool): Поддержка системных сообщений (True).
- `supports_message_history` (bool): Поддержка истории сообщений (True).
- `default_model` (str): Модель по умолчанию ("@cf/meta/llama-3.3-70b-instruct-fp8-fast").
- `model_aliases` (dict): Псевдонимы моделей.
- `_args` (dict): Аргументы для сессии.

**Принцип работы**:
Класс `Cloudflare` инициализирует параметры для подключения к API Cloudflare AI. Он использует `AsyncGeneratorProvider` для асинхронной генерации ответов, `ProviderModelMixin` для управления списком моделей и `AuthFileMixin` для аутентификации. При первом запросе класс пытается получить аргументы для сессии из кэш-файла или с использованием бездрайверного режима. Затем он формирует запрос к API Cloudflare AI и возвращает асинхронный генератор для обработки потоковых ответов.

## Методы класса

### `get_models`

```python
@classmethod
def get_models(cls) -> str:
    """Получает список доступных моделей из API Cloudflare.

    Args:
        cls (Cloudflare): Ссылка на класс `Cloudflare`.

    Returns:
        str: Список доступных моделей.

    Raises:
        ResponseStatusError: Если возникает ошибка при получении списка моделей.

    Как работает функция:
    - Функция проверяет, загружен ли уже список моделей. Если нет, она пытается получить аргументы сессии из кэша или с использованием бездрайверного режима.
    - Затем она выполняет GET-запрос к `models_url` для получения списка моделей.
    - В случае успеха список моделей извлекается из JSON-ответа и сохраняется в атрибуте `cls.models`.
    - Если возникает ошибка при выполнении запроса, возвращается текущий (возможно, пустой) список моделей.

    Примеры:
    >>> Cloudflare.get_models()
    ['@cf/meta/llama-3.3-70b-instruct-fp8-fast', ...]
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
    max_tokens: int = 2048,
    cookies: Cookies = None,
    timeout: int = 300,
    **kwargs
) -> AsyncResult:
    """Создает асинхронный генератор для взаимодействия с API Cloudflare.

    Args:
        cls (Cloudflare): Ссылка на класс `Cloudflare`.
        model (str): Имя используемой модели.
        messages (Messages): Список сообщений для отправки в API.
        proxy (str, optional): Адрес прокси-сервера. По умолчанию `None`.
        max_tokens (int, optional): Максимальное количество токенов в ответе. По умолчанию `2048`.
        cookies (Cookies, optional): Куки для отправки в API. По умолчанию `None`.
        timeout (int, optional): Время ожидания ответа от API. По умолчанию `300`.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор для получения ответов от API.

    Raises:
        ResponseStatusError: Если возникает ошибка при отправке запроса.

    Как работает функция:
    - Функция сначала пытается получить аргументы сессии из кэш-файла или с использованием бездрайверного режима.
    - Затем она формирует данные запроса, включая сообщения, модель и параметры генерации.
    - После этого выполняется POST-запрос к `api_endpoint` с использованием асинхронной сессии.
    - Функция обрабатывает потоковые ответы от API, извлекая данные и возвращая их через асинхронный генератор.
    - В случае ошибки аргументы сессии сбрасываются, и кэш-файл удаляется.

    Примеры:
    >>> messages = [{"role": "user", "content": "Hello"}]
    >>> async for response in Cloudflare.create_async_generator(model="@cf/meta/llama-3.3-70b-instruct-fp8-fast", messages=messages):
    ...     print(response)
    """
    ...
```

## Параметры класса

- `label` (str): Метка провайдера ("Cloudflare AI").
- `url` (str): URL для доступа к Cloudflare AI ("https://playground.ai.cloudflare.com").
- `working` (bool): Указывает, работает ли провайдер (True).
- `use_nodriver` (bool): Указывает, используется ли бездрайверный режим (True).
- `api_endpoint` (str): URL для API-инференса ("https://playground.ai.cloudflare.com/api/inference").
- `models_url` (str): URL для получения списка моделей ("https://playground.ai.cloudflare.com/api/models").
- `supports_stream` (bool): Поддержка потоковой передачи (True).
- `supports_system_message` (bool): Поддержка системных сообщений (True).
- `supports_message_history` (bool): Поддержка истории сообщений (True).
- `default_model` (str): Модель по умолчанию ("@cf/meta/llama-3.3-70b-instruct-fp8-fast").
- `model_aliases` (dict): Псевдонимы моделей.
- `_args` (dict): Аргументы для сессии.

## Примеры

```python
messages = [{"role": "user", "content": "Hello"}]
async for response in Cloudflare.create_async_generator(model="@cf/meta/llama-3.3-70b-instruct-fp8-fast", messages=messages):
    print(response)