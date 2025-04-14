# Модуль `DDG.py`

## Обзор

Модуль `DDG.py` предоставляет асинхронный интерфейс для взаимодействия с AI Chat от DuckDuckGo. Он позволяет генерировать ответы на основе предоставленных сообщений, используя различные модели, такие как "gpt-4o-mini", "meta-llama/Llama-3.3-70B-Instruct-Turbo" и другие. Модуль поддерживает потоковую передачу данных, системные сообщения и историю сообщений.

## Подробней

Модуль предназначен для интеграции с другими компонентами проекта `hypotez`, требующими функциональности чат-ботов на основе AI. Он обеспечивает возможность выбора различных моделей, управление кукисами и обработку ошибок, таких как превышение лимита запросов и тайм-ауты.

## Классы

### `DuckDuckGoSearchException`

**Описание**: Базовый класс исключений для модуля `duckduckgo_search`.

### `Conversation`

**Описание**: Класс для хранения информации о текущем состоянии разговора с AI Chat от DuckDuckGo.

**Наследует**: `JsonConversation`

**Атрибуты**:
- `vqd` (str): Идентификатор VQD (Verification Query Data).
- `vqd_hash_1` (str): Хэш VQD.
- `message_history` (Messages): История сообщений в разговоре.
- `cookies` (dict): Куки, используемые в разговоре.
- `fe_version` (str): Версия front-end.
- `model` (str): Используемая модель.

**Методы**:
- `__init__(self, model: str)`: Инициализирует объект `Conversation` с указанной моделью.

### `DDG`

**Описание**: Класс, реализующий асинхронного провайдера для взаимодействия с AI Chat от DuckDuckGo.

**Наследует**: `AsyncGeneratorProvider`, `ProviderModelMixin`

**Атрибуты**:
- `label` (str): Метка провайдера ("DuckDuckGo AI Chat").
- `url` (str): URL главной страницы AI Chat от DuckDuckGo ("https://duckduckgo.com/aichat").
- `api_endpoint` (str): URL API для чата ("https://duckduckgo.com/duckchat/v1/chat").
- `status_url` (str): URL для получения статуса ("https://duckduckgo.com/duckchat/v1/status").
- `working` (bool): Указывает, работает ли провайдер (True).
- `supports_stream` (bool): Поддержка потоковой передачи данных (True).
- `supports_system_message` (bool): Поддержка системных сообщений (True).
- `supports_message_history` (bool): Поддержка истории сообщений (True).
- `default_model` (str): Модель по умолчанию ("gpt-4o-mini").
- `models` (list[str]): Список поддерживаемых моделей.
- `model_aliases` (dict[str, str]): Псевдонимы моделей для удобства использования.
- `last_request_time` (float): Время последнего запроса. Используется для rate limiting.
- `max_retries` (int): Максимальное количество попыток повтора запроса.
- `base_delay` (int): Базовая задержка между повторными запросами в секундах.
- `_chat_xfe` (str): Class variable to store the x-fe-version across instances

**Методы**:
- `sha256_base64(text: str) -> str`: Возвращает base64-encoded SHA256 хэш текста.
- `parse_dom_fingerprint(js_text: str) -> str`: Извлекает fingerprint из javascript текста.
- `parse_server_hashes(js_text: str) -> list`: Извлекает server hashes из javascript текста.
- `build_x_vqd_hash_1(vqd_hash_1: str, headers: dict) -> str`: Строит значение заголовка `x-vqd-hash-1`.
- `validate_model(model: str) -> str`: Проверяет и возвращает корректное имя модели.
- `sleep(multiplier=1.0)`: Реализует rate limiting между запросами.
- `get_default_cookies(session: ClientSession) -> dict`: Получает куки, необходимые для API-запросов.
- `fetch_fe_version(session: ClientSession) -> str`: Получает версию front-end из начальной загрузки страницы.
- `fetch_vqd_and_hash(session: ClientSession, retry_count: int = 0) -> tuple[str, str]`: Получает VQD token и hash для чат сессии с повторными попытками.
- `create_async_generator(...) -> AsyncResult`: Создает асинхронный генератор для взаимодействия с API DuckDuckGo AI Chat.

## Методы класса

### `sha256_base64`

```python
@staticmethod
def sha256_base64(text: str) -> str:
    """Return the base64 encoding of the SHA256 digest of the text."""
    sha256_hash = hashlib.sha256(text.encode("utf-8")).digest()
    return base64.b64encode(sha256_hash).decode()
```

**Назначение**: Вычисляет SHA256 хэш переданного текста и кодирует его в base64.

**Параметры**:
- `text` (str): Текст для хэширования.

**Возвращает**:
- `str`: Base64-encoded SHA256 хэш текста.

**Как работает функция**:
1. Кодирует входной текст в UTF-8.
2. Вычисляет SHA256 хэш закодированного текста.
3. Кодирует полученный хэш в base64.
4. Декодирует base64-encoded хэш в строку UTF-8 и возвращает её.

**Примеры**:
```python
text = "example text"
hash_value = DDG.sha256_base64(text)
print(hash_value)
```

### `parse_dom_fingerprint`

```python
@staticmethod
def parse_dom_fingerprint(js_text: str) -> str:
    """Извлекает fingerprint из javascript текста."""
    ...
```

**Назначение**: Извлекает fingerprint из javascript текста, содержащего HTML snippet.

**Параметры**:
- `js_text` (str): JavaScript текст, содержащий HTML snippet и offset value.

**Возвращает**:
- `str`: Строковое представление fingerprint. Возвращает "1000" в случае ошибки или если `BeautifulSoup` не установлен.

**Как работает функция**:
1. Проверяет, установлен ли `BeautifulSoup`. Если нет, возвращает "1000".
2. Извлекает HTML snippet и offset value из JavaScript текста.
3. Использует `BeautifulSoup` для парсинга HTML snippet.
4. Вычисляет fingerprint как сумму offset value и длины inner HTML.
5. Возвращает строковое представление fingerprint.

**Примеры**:
```python
js_text = "e.innerHTML = '<div id=\"test\">Test</div>';" \
          "return String(123) "
fingerprint = DDG.parse_dom_fingerprint(js_text)
print(fingerprint)
```

### `parse_server_hashes`

```python
@staticmethod
def parse_server_hashes(js_text: str) -> list:
    """Извлекает server hashes из javascript текста."""
    ...
```

**Назначение**: Извлекает server hashes из JavaScript текста.

**Параметры**:
- `js_text` (str): JavaScript текст, содержащий server hashes.

**Возвращает**:
- `list[str]`: Список server hashes. Возвращает `["1", "2"]` в случае ошибки.

**Как работает функция**:
1. Пытается извлечь server hashes из JavaScript текста, используя строковые операции.
2. Если извлечение успешно, возвращает список server hashes.
3. В случае ошибки возвращает `["1", "2"]`.

**Примеры**:
```python
js_text = 'server_hashes: ["hash1", "hash2"]'
server_hashes = DDG.parse_server_hashes(js_text)
print(server_hashes)
```

### `build_x_vqd_hash_1`

```python
@classmethod
def build_x_vqd_hash_1(cls, vqd_hash_1: str, headers: dict) -> str:
    """Строит значение заголовка `x-vqd-hash-1`."""
    ...
```

**Назначение**: Строит значение заголовка `x-vqd-hash-1` на основе переданных параметров.

**Параметры**:
- `vqd_hash_1` (str): Base64-encoded строка, содержащая server hashes и fingerprint.
- `headers` (dict): Словарь HTTP-заголовков, содержащий `User-Agent` и `sec-ch-ua`.

**Возвращает**:
- `str`: Base64-encoded JSON, содержащий server hashes и client hashes. Возвращает пустую строку в случае ошибки.

**Как работает функция**:
1. Декодирует `vqd_hash_1` из base64 в строку.
2. Извлекает server hashes и fingerprint из декодированной строки.
3. Вычисляет SHA256 хэши `User-Agent` и fingerprint.
4. Формирует JSON, содержащий server hashes и client hashes.
5. Кодирует JSON в base64 и возвращает результат.

**Примеры**:
```python
vqd_hash_1 = "base64_encoded_string"
headers = {"User-Agent": "Mozilla/5.0", "sec-ch-ua": '"Chromium";v="133"'}
x_vqd_hash_1 = DDG.build_x_vqd_hash_1(vqd_hash_1, headers)
print(x_vqd_hash_1)
```

### `validate_model`

```python
@classmethod
def validate_model(cls, model: str) -> str:
    """Проверяет и возвращает корректное имя модели."""
    ...
```

**Назначение**: Проверяет, поддерживается ли указанная модель, и возвращает её корректное имя.

**Параметры**:
- `model` (str): Имя модели для проверки.

**Возвращает**:
- `str`: Корректное имя модели. Если модель не указана, возвращает `cls.default_model`.

**Вызывает исключения**:
- `ModelNotSupportedError`: Если указанная модель не поддерживается.

**Как работает функция**:
1. Если `model` не указана, возвращает `cls.default_model`.
2. Если `model` есть в `cls.model_aliases`, заменяет её на соответствующий псевдоним.
3. Если `model` не найдена в списке `cls.models`, вызывает исключение `ModelNotSupportedError`.
4. Возвращает имя модели.

**Примеры**:
```python
model = "gpt-4"
validated_model = DDG.validate_model(model)
print(validated_model)

model = "unsupported_model"
try:
    validated_model = DDG.validate_model(model)
except ModelNotSupportedError as ex:
    print(f"Error: {ex}")
```

### `sleep`

```python
@classmethod
async def sleep(cls, multiplier=1.0):
    """Реализует rate limiting между запросами."""
    ...
```

**Назначение**: Реализует задержку между запросами для rate limiting.

**Параметры**:
- `multiplier` (float, optional): Множитель задержки. По умолчанию `1.0`.

**Как работает функция**:
1. Вычисляет задержку на основе времени последнего запроса.
2. Если задержка больше нуля, ждет указанное время.
3. Обновляет время последнего запроса.

**Примеры**:
```python
await DDG.sleep()
await DDG.sleep(multiplier=0.5)
```

### `get_default_cookies`

```python
@classmethod
async def get_default_cookies(cls, session: ClientSession) -> dict:
    """Получает куки, необходимые для API-запросов."""
    ...
```

**Назначение**: Получает куки, необходимые для выполнения API-запросов.

**Параметры**:
- `session` (ClientSession): Асинхронная HTTP-сессия.

**Возвращает**:
- `dict`: Словарь куки. Возвращает пустой словарь в случае ошибки.

**Как работает функция**:
1. Отправляет GET-запрос к `cls.url`.
2. Извлекает куки из ответа.
3. Добавляет обязательные куки `dcs` и `dcm` в словарь куки.
4. Обновляет `session.cookie_jar` с новыми куки.
5. Возвращает словарь куки.

**Примеры**:
```python
async with ClientSession() as session:
    cookies = await DDG.get_default_cookies(session)
    print(cookies)
```

### `fetch_fe_version`

```python
@classmethod
async def fetch_fe_version(cls, session: ClientSession) -> str:
    """Fetches the fe-version from the initial page load."""
    ...
```

**Назначение**: Извлекает версию front-end (`fe-version`) из начальной загрузки страницы.

**Параметры**:
- `session` (ClientSession): Асинхронная HTTP-сессия.

**Возвращает**:
- `str`: Версия front-end. Возвращает пустую строку в случае ошибки.

**Как работает функция**:
1. Если `cls._chat_xfe` уже определена, возвращает её значение.
2. Отправляет GET-запрос к URL DuckDuckGo AI Chat.
3. Извлекает значения `__DDG_BE_VERSION__` и `__DDG_FE_CHAT_HASH__` из HTML-контента ответа.
4. Формирует версию front-end как `f"{xfe1}-{xfe2}"`.
5. Сохраняет значение в `cls._chat_xfe` и возвращает его.

**Примеры**:
```python
async with ClientSession() as session:
    fe_version = await DDG.fetch_fe_version(session)
    print(fe_version)
```

### `fetch_vqd_and_hash`

```python
@classmethod
async def fetch_vqd_and_hash(cls, session: ClientSession, retry_count: int = 0) -> tuple[str, str]:
    """Получает VQD token и hash для чат сессии с повторными попытками."""
    ...
```

**Назначение**: Получает VQD (Verification Query Data) token и hash для чат сессии с повторными попытками.

**Параметры**:
- `session` (ClientSession): Асинхронная HTTP-сессия.
- `retry_count` (int, optional): Количество попыток повтора. По умолчанию `0`.

**Возвращает**:
- `tuple[str, str]`: Кортеж, содержащий VQD token и hash.

**Вызывает исключения**:
- `RuntimeError`: Если не удалось получить VQD token и hash после максимального количества попыток.

**Как работает функция**:
1. Формирует HTTP-заголовки для запроса.
2. Отправляет GET-запрос к `cls.status_url`.
3. Извлекает VQD token и hash из HTTP-заголовков ответа.
4. Если VQD token получен, возвращает его вместе с hash.
5. В случае ошибки повторяет запрос до `cls.max_retries`.

**Примеры**:
```python
async with ClientSession() as session:
    vqd, vqd_hash = await DDG.fetch_vqd_and_hash(session)
    print(f"VQD: {vqd}, Hash: {vqd_hash}")
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
    """Создает асинхронный генератор для взаимодействия с API DuckDuckGo AI Chat."""
    ...
```

**Назначение**: Создает асинхронный генератор для взаимодействия с API DuckDuckGo AI Chat.

**Параметры**:
- `model` (str): Имя используемой модели.
- `messages` (Messages): Список сообщений для отправки.
- `proxy` (str, optional): Адрес прокси-сервера. По умолчанию `None`.
- `timeout` (int, optional): Время ожидания запроса в секундах. По умолчанию `60`.
- `cookies` (Cookies, optional): Куки для использования в сессии. По умолчанию `None`.
- `conversation` (Conversation, optional): Объект `Conversation` для продолжения существующего разговора. По умолчанию `None`.
- `return_conversation` (bool, optional): Возвращать ли объект `Conversation` в конце генерации. По умолчанию `False`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, выдающий ответы от AI Chat DuckDuckGo.

**Вызывает исключения**:
- `ModelNotSupportedError`: Если указанная модель не поддерживается.
- `RateLimitError`: Если превышен лимит запросов.
- `TimeoutError`: Если запрос превысил время ожидания.
- `DuckDuckGoSearchException`: Если произошла ошибка в процессе обработки запроса.
- `ConversationLimitError`: Если превышен лимит разговоров.

**Как работает функция**:

1. **Валидация модели**:
   - Проверяет и устанавливает корректное имя модели, используя метод `validate_model`.

2. **Инициализация сессии**:
   - Создает асинхронную сессию `ClientSession` с заданным таймаутом и куками.

3. **Получение версии front-end**:
   - Если `cls._chat_xfe` не определена, получает её значение, используя `fetch_fe_version`.

4. **Инициализация или обновление разговора**:
   - Если `conversation` не передан:
     - Получает начальные куки, если они не были переданы.
     - Создает новый объект `Conversation` с указанной моделью.
     - Получает VQD токены, используя `fetch_vqd_and_hash`.
     - Инициализирует историю сообщений с первым сообщением пользователя.
   - Если `conversation` передан:
     - Обновляет историю сообщений, добавляя последнее сообщение пользователя.

5. **Подготовка HTTP-заголовков**:
   - Формирует HTTP-заголовки, включая версию front-end, VQD токен и hash.

6. **Подготовка данных запроса**:
   - Формирует данные запроса в формате JSON, включая модель и историю сообщений.

7. **Отправка запроса**:
   - Отправляет POST-запрос к `cls.api_endpoint` с данными и заголовками.
   - Обрабатывает ошибки, такие как `RateLimitError`, `ResponseStatusError`, `TimeoutError` и другие.

8. **Обработка потокового ответа**:
   - Читает ответ построчно.
   - Извлекает сообщения из JSON-форматированных строк.
   - Выдает сообщения через генератор.

9. **Обновление информации о разговоре**:
   - Если `return_conversation` установлен в `True`:
     - Обновляет историю сообщений, добавляя ответ ассистента.
     - Обновляет VQD токен и hash из заголовков ответа.
     - Обновляет куки сессии.
     - Выдает объект `Conversation` через генератор.

10. **Завершение генерации**:
    - Выдает `FinishReason`, указывающий на причину завершения генерации.

**Примеры**:
```python
async def main():
    model = "gpt-4o-mini"
    messages = [{"role": "user", "content": "Hello, how are you?"}]
    async for message in DDG.create_async_generator(model=model, messages=messages):
        print(message)

asyncio.run(main())
```