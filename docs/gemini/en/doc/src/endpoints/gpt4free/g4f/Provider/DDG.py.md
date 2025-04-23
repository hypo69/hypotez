# Module `DDG.py`

## Обзор

Модуль предоставляет класс `DDG` для взаимодействия с DuckDuckGo AI Chat API.
Он поддерживает асинхронные запросы и потоковую передачу ответов.
Модуль включает в себя функциональность для управления куки, заголовками и лимитами запросов.

## Детали

Этот код используется для интеграции с AI Chat API DuckDuckGo, обеспечивая функциональность общения с AI через асинхронные запросы. Он включает в себя обработку ошибок, управление куки и заголовками, а также поддержку различных моделей AI.

## Классы

### `DuckDuckGoSearchException`

**Описание**: Базовый класс исключений для `duckduckgo_search`.

**Наследуется**:
- `Exception`: Наследует от базового класса `Exception`.

**Атрибуты**:
- Отсутствуют.

**Методы**:
- Отсутствуют.

### `Conversation`

**Описание**: Класс для хранения состояния разговора с AI.

**Наследуется**:
- `JsonConversation`: Наследует от `JsonConversation`, который предоставляет базовую структуру для хранения истории разговоров в формате JSON.

**Атрибуты**:
- `vqd` (str): VQD токен для идентификации сессии.
- `vqd_hash_1` (str): Хэш VQD токена.
- `message_history` (Messages): История сообщений в разговоре.
- `cookies` (dict): Куки для сессии.
- `fe_version` (str): Версия front-end.

**Параметры**:
- `model` (str): Модель AI, используемая в разговоре.

**Методы**:
- `__init__(self, model: str)`: Конструктор класса, инициализирует объект `Conversation` с указанной моделью.

### `DDG`

**Описание**: Класс для взаимодействия с DuckDuckGo AI Chat API.

**Наследуется**:
- `AsyncGeneratorProvider`: Наследует от `AsyncGeneratorProvider`, который предоставляет асинхронный генератор для потоковой передачи ответов.
- `ProviderModelMixin`: Предоставляет вспомогательные методы для работы с моделями.

**Атрибуты**:
- `label` (str): Метка для класса, "DuckDuckGo AI Chat".
- `url` (str): URL для DuckDuckGo AI Chat, "https://duckduckgo.com/aichat".
- `api_endpoint` (str): URL для API, "https://duckduckgo.com/duckchat/v1/chat".
- `status_url` (str): URL для получения статуса, "https://duckduckgo.com/duckchat/v1/status".
- `working` (bool): Флаг, указывающий, работает ли класс, `True`.
- `supports_stream` (bool): Флаг, указывающий, поддерживает ли класс потоковую передачу, `True`.
- `supports_system_message` (bool): Флаг, указывающий, поддерживает ли класс системные сообщения, `True`.
- `supports_message_history` (bool): Флаг, указывающий, поддерживает ли класс историю сообщений, `True`.
- `default_model` (str): Модель AI по умолчанию, "gpt-4o-mini".
- `models` (list): Список поддерживаемых моделей AI.
- `model_aliases` (dict): Словарь псевдонимов моделей.
- `last_request_time` (float): Время последнего запроса.
- `max_retries` (int): Максимальное количество попыток повторных запросов.
- `base_delay` (int): Базовая задержка между запросами.
- `_chat_xfe` (str): Классовая переменная для хранения `x-fe-version` между экземплярами.

**Параметры**:
- Отсутствуют.

**Методы**:
- `sha256_base64(text: str) -> str`: Возвращает base64 кодировку SHA256 хэша текста.
- `parse_dom_fingerprint(js_text: str) -> str`: Извлекает fingerprint из JavaScript текста.
- `parse_server_hashes(js_text: str) -> list`: Извлекает server hashes из JavaScript текста.
- `build_x_vqd_hash_1(cls, vqd_hash_1: str, headers: dict) -> str`: Строит значение заголовка `x-vqd-hash-1`.
- `validate_model(cls, model: str) -> str`: Проверяет и возвращает корректное имя модели.
- `sleep(cls, multiplier=1.0)`: Реализует ограничение скорости между запросами.
- `get_default_cookies(cls, session: ClientSession) -> dict`: Получает куки по умолчанию, необходимые для API запросов.
- `fetch_fe_version(cls, session: ClientSession) -> str`: Получает `fe-version` при начальной загрузке страницы.
- `fetch_vqd_and_hash(cls, session: ClientSession, retry_count: int = 0) -> tuple[str, str]`: Получает VQD токен и хэш для сессии чата с повторными попытками.
- `create_async_generator(...) -> AsyncResult`: Создает асинхронный генератор для взаимодействия с API.

## Методы класса `DDG`

### `sha256_base64`

```python
@staticmethod
def sha256_base64(text: str) -> str:
    """
    Возвращает base64 кодировку SHA256 хэша текста.

    Args:
        text (str): Текст для хеширования.

    Returns:
        str: Base64 кодировка SHA256 хэша.

    Raises:
        Нет.

    Example:
        >>> DDG.sha256_base64("example_text")
        '79JEq8MvJpwCsRJQ2Q5rtCz5SmswbkCFP1MbsNU7Cw='
    """
    ...
```

### `parse_dom_fingerprint`

```python
@staticmethod
def parse_dom_fingerprint(js_text: str) -> str:
    """
    Извлекает fingerprint из JavaScript текста.

    Args:
        js_text (str): JavaScript текст для парсинга.

    Returns:
        str: Строковое представление fingerprint.

    Raises:
        Нет.

    Example:
        >>> js_code = "e.innerHTML = '<html><body><div>Example</div></body></html>';"
        >>> DDG.parse_dom_fingerprint(js_code)
        '1000'
    """
    ...
```

### `parse_server_hashes`

```python
@staticmethod
def parse_server_hashes(js_text: str) -> list:
    """
    Извлекает server hashes из JavaScript текста.

    Args:
        js_text (str): JavaScript текст для парсинга.

    Returns:
        list: Список server hashes.

    Raises:
        Нет.

    Example:
        >>> js_code = 'server_hashes: ["hash1","hash2"]'
        >>> DDG.parse_server_hashes(js_code)
        ['hash1', 'hash2']
    """
    ...
```

### `build_x_vqd_hash_1`

```python
@classmethod
def build_x_vqd_hash_1(cls, vqd_hash_1: str, headers: dict) -> str:
    """
    Строит значение заголовка `x-vqd-hash-1`.

    Args:
        vqd_hash_1 (str): Base64 закодированный VQD хэш.
        headers (dict): Словарь заголовков запроса.

    Returns:
        str: Значение для заголовка `x-vqd-hash-1`.

    Raises:
        Нет.

    Example:
        >>> vqd_hash = "some_base64_vqd_hash"
        >>> headers = {"User-Agent": "test_agent", "sec-ch-ua": "test_sec_ch_ua"}
        >>> DDG.build_x_vqd_hash_1(vqd_hash, headers)
        ''
    """
    ...
```

### `validate_model`

```python
@classmethod
def validate_model(cls, model: str) -> str:
    """
    Проверяет и возвращает корректное имя модели.

    Args:
        model (str): Имя модели для валидации.

    Returns:
        str: Корректное имя модели.

    Raises:
        ModelNotSupportedError: Если модель не поддерживается.

    Example:
        >>> DDG.validate_model("gpt-4")
        'gpt-4o-mini'

        >>> DDG.validate_model("unsupported_model")
        Traceback (most recent call last):
          ...
        src.errors.ModelNotSupportedError: Model unsupported_model not supported. Available models: ['gpt-4o-mini', 'meta-llama/Llama-3.3-70B-Instruct-Turbo', 'claude-3-haiku-20240307', 'o3-mini', 'mistralai/Mistral-Small-24B-Instruct-2501']
    """
    ...
```

### `sleep`

```python
@classmethod
async def sleep(cls, multiplier=1.0):
    """
    Реализует ограничение скорости между запросами.

    Args:
        multiplier (float): Множитель задержки.

    Returns:
        None

    Raises:
        Нет.

    Example:
        >>> import asyncio
        >>> asyncio.run(DDG.sleep(multiplier=0.5))
    """
    ...
```

### `get_default_cookies`

```python
@classmethod
async def get_default_cookies(cls, session: ClientSession) -> dict:
    """
    Получает куки по умолчанию, необходимые для API запросов.

    Args:
        session (ClientSession): Асинхронная клиентская сессия.

    Returns:
        dict: Словарь куки.

    Raises:
        Нет.

    Example:
        >>> import asyncio
        >>> from aiohttp import ClientSession
        >>> async def get_cookies():
        ...     async with ClientSession() as session:
        ...         return await DDG.get_default_cookies(session)
        >>> asyncio.run(get_cookies())
        {}
    """
    ...
```

### `fetch_fe_version`

```python
@classmethod
async def fetch_fe_version(cls, session: ClientSession) -> str:
    """
    Получает `fe-version` при начальной загрузке страницы.

    Args:
        session (ClientSession): Асинхронная клиентская сессия.

    Returns:
        str: Версия `fe-version`.

    Raises:
        Нет.

    Example:
        >>> import asyncio
        >>> from aiohttp import ClientSession
        >>> async def get_fe_version():
        ...     async with ClientSession() as session:
        ...         return await DDG.fetch_fe_version(session)
        >>> asyncio.run(get_fe_version())
        ''
    """
    ...
```

### `fetch_vqd_and_hash`

```python
@classmethod
async def fetch_vqd_and_hash(cls, session: ClientSession, retry_count: int = 0) -> tuple[str, str]:
    """
    Получает VQD токен и хэш для сессии чата с повторными попытками.

    Args:
        session (ClientSession): Асинхронная клиентская сессия.
        retry_count (int): Счетчик повторных попыток.

    Returns:
        tuple[str, str]: Кортеж, содержащий VQD токен и хэш.

    Raises:
        RuntimeError: Если не удалось получить VQD токен и хэш после нескольких попыток.

    Example:
        >>> import asyncio
        >>> from aiohttp import ClientSession
        >>> async def get_vqd_and_hash():
        ...     async with ClientSession() as session:
        ...         return await DDG.fetch_vqd_and_hash(session)
        >>> asyncio.run(get_vqd_and_hash())
        ('', '')
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
    timeout: int = 60,
    cookies: Cookies = None,
    conversation: Conversation = None,
    return_conversation: bool = False,
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для взаимодействия с API.

    Args:
        model (str): Имя модели AI.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        timeout (int, optional): Время ожидания запроса. По умолчанию 60.
        cookies (Cookies, optional): Куки для сессии. По умолчанию `None`.
        conversation (Conversation, optional): Объект разговора. По умолчанию `None`.
        return_conversation (bool, optional): Возвращать ли объект разговора. По умолчанию `False`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор.

    Raises:
        RateLimitError: Если превышен лимит запросов.
        TimeoutError: Если запрос превысил время ожидания.
        Exception: Если произошла другая ошибка.

    Example:
        >>> import asyncio
        >>> from aiohttp import ClientSession
        >>> async def generate():
        ...     async for message in await DDG.create_async_generator(model="gpt-4o-mini", messages=[{"role": "user", "content": "Hello"}]):
        ...         print(message)
        >>> asyncio.run(generate())
        None
    """
    ...