# Модуль `DDG.py`

## Обзор

Модуль `DDG.py` предоставляет асинхронный интерфейс для взаимодействия с чат-ботом DuckDuckGo AI. Он включает в себя функциональность для получения ответа от модели, обработки ошибок, управления куки и версиями API.

## Подробнее

Этот модуль является частью проекта `hypotez` и предназначен для интеграции с другими компонентами, требующими доступа к DuckDuckGo AI Chat. Модуль поддерживает стриминг ответов, системные сообщения и сохранение истории сообщений. Он также включает механизмы обработки ошибок, такие как RateLimitError, ResponseStatusError и TimeoutError, а также повторные попытки для повышения надежности.

## Классы

### `DuckDuckGoSearchException`

**Описание**: Базовый класс исключений для модуля `duckduckgo_search`.

### `Conversation`

**Описание**: Класс для хранения информации о текущем разговоре с DuckDuckGo AI.

**Наследует**: `JsonConversation`

**Атрибуты**:
- `vqd` (str): VQD токен для текущей сессии.
- `vqd_hash_1` (str): Хэш VQD токена.
- `message_history` (Messages): История сообщений в формате списка словарей.
- `cookies` (dict): Куки, необходимые для запросов.
- `fe_version` (str): Версия Frontend API.
- `model` (str): Модель, используемая в разговоре.

**Методы**:

#### `__init__`

```python
def __init__(self, model: str):
    """
    Инициализирует объект Conversation.

    Args:
        model (str): Модель, используемая в разговоре.
    """
```
**Назначение**: Конструктор класса `Conversation`.

**Параметры**:
- `model` (str): Модель, используемая в разговоре.

**Как работает функция**:

- Функция инициализирует атрибут `model` экземпляра класса `Conversation` значением, переданным в качестве аргумента.

### `DDG`

**Описание**: Класс, предоставляющий асинхронный интерфейс для взаимодействия с DuckDuckGo AI Chat.

**Наследует**: `AsyncGeneratorProvider`, `ProviderModelMixin`

**Атрибуты**:

- `label` (str): Метка для идентификации провайдера ("DuckDuckGo AI Chat").
- `url` (str): URL для доступа к DuckDuckGo AI Chat ("https://duckduckgo.com/aichat").
- `api_endpoint` (str): URL для API чата ("https://duckduckgo.com/duckchat/v1/chat").
- `status_url` (str): URL для получения статуса ("https://duckduckgo.com/duckchat/v1/status").
- `working` (bool): Флаг, указывающий, что провайдер работает (True).
- `supports_stream` (bool): Флаг, указывающий, поддерживает ли провайдер стриминг (True).
- `supports_system_message` (bool): Флаг, указывающий, поддерживает ли провайдер системные сообщения (True).
- `supports_message_history` (bool): Флаг, указывающий, поддерживает ли провайдер историю сообщений (True).
- `default_model` (str): Модель, используемая по умолчанию ("gpt-4o-mini").
- `models` (list): Список поддерживаемых моделей.
- `model_aliases` (dict): Словарь псевдонимов моделей.
- `last_request_time` (float): Время последнего запроса.
- `max_retries` (int): Максимальное количество повторных попыток при запросах.
- `base_delay` (int): Базовая задержка между повторными попытками.
- `_chat_xfe` (str): Class variable to store the x-fe-version across instances

**Методы**:

#### `sha256_base64`

```python
@staticmethod
def sha256_base64(text: str) -> str:
    """Return the base64 encoding of the SHA256 digest of the text."""
```

**Назначение**: Возвращает base64-encoded SHA256 хэш текста.

**Параметры**:
- `text` (str): Текст для хэширования.

**Возвращает**:
- `str`: Base64-encoded SHA256 хэш текста.

**Как работает функция**:

- Функция преобразует входной текст в байты, используя кодировку UTF-8.
- Вычисляет SHA256 хэш полученных байтов.
- Кодирует полученный хэш в base64.
- Декодирует base64 представление в строку UTF-8 и возвращает её.

**Примеры**:

```python
text = "example"
result = DDG.sha256_base64(text)
print(result)  # Вывод: rnuEjVQQ4O8VjGY9qnUJlwtOrYj9gYoeGrQ2xjeP4ZA=
```

#### `parse_dom_fingerprint`

```python
@staticmethod
def parse_dom_fingerprint(js_text: str) -> str:
    """Парсит js для получения dom_fingerprint"""
```

**Назначение**: Извлекает fingerprint DOM из JavaScript кода.

**Параметры**:
- `js_text` (str): JavaScript код, содержащий fingerprint DOM.

**Возвращает**:
- `str`: fingerprint DOM в виде строки. Возвращает "1000", если `BeautifulSoup` не установлен или если парсинг не удался.

**Как работает функция**:

- Проверяет, установлен ли `BeautifulSoup`. Если нет, возвращает "1000".
- Извлекает HTML snippet из JavaScript кода.
- Извлекает значение смещения (`offset_value`) из JavaScript кода.
- Использует `BeautifulSoup` для парсинга HTML snippet.
- Вычисляет fingerprint как сумму значения смещения и длины содержимого тега `body`.
- Возвращает fingerprint в виде строки.
- Если любой из шагов завершается с ошибкой, возвращает "1000".

**Примеры**:

```python
js_text = "e.innerHTML = '<html><body>test</body></html>'; return String(10)"
result = DDG.parse_dom_fingerprint(js_text)
print(result)  # Вывод: 14
```

#### `parse_server_hashes`

```python
@staticmethod
def parse_server_hashes(js_text: str) -> list:
    """Парсит server_hashes из js текста."""
```

**Назначение**: Извлекает server_hashes из JavaScript кода.

**Параметры**:
- `js_text` (str): JavaScript код, содержащий server_hashes.

**Возвращает**:
- `list`: Список server_hashes. Возвращает `["1", "2"]`, если парсинг не удался.

**Как работает функция**:

- Пытается извлечь список `server_hashes` из предоставленного JavaScript кода.
- Если извлечение успешно, возвращает список `server_hashes`.
- Если извлечение не удалось, возвращает `["1", "2"]`.

**Примеры**:

```python
js_text = 'server_hashes: ["hash1","hash2"]'
result = DDG.parse_server_hashes(js_text)
print(result)  # Вывод: ['hash1', 'hash2']
```

#### `build_x_vqd_hash_1`

```python
@classmethod
def build_x_vqd_hash_1(cls, vqd_hash_1: str, headers: dict) -> str:
    """Строит значение заголовка x-vqd-hash-1."""
```

**Назначение**: Строит значение для заголовка `x-vqd-hash-1` на основе переданных параметров.

**Параметры**:
- `vqd_hash_1` (str): Base64-encoded строка, содержащая server_hashes и dom_fingerprint.
- `headers` (dict): Словарь заголовков запроса, содержащий User-Agent и sec-ch-ua.

**Возвращает**:
- `str`: Base64-encoded JSON, содержащий server_hashes, client_hashes и signals. Возвращает пустую строку, если что-то пошло не так.

**Как работает функция**:

- Декодирует `vqd_hash_1` из base64.
- Извлекает `server_hashes` и `dom_fingerprint` из декодированной строки.
- Создает SHA256 хэши для User-Agent и dom_fingerprint.
- Формирует JSON объект, содержащий `server_hashes`, `client_hashes` (ua_hash, dom_hash) и пустой словарь `signals`.
- Кодирует JSON объект в base64.
- Возвращает полученную base64 строку.

**Примеры**:

```python
vqd_hash_1 = "base64_encoded_string"
headers = {"User-Agent": "test_agent", "sec-ch-ua": "test_ua"}
result = DDG.build_x_vqd_hash_1(vqd_hash_1, headers)
print(result)  # Вывод: base64 encoded json
```

#### `validate_model`

```python
@classmethod
def validate_model(cls, model: str) -> str:
    """Проверяет и возвращает правильное имя модели"""
```

**Назначение**: Проверяет и возвращает корректное имя модели.

**Параметры**:
- `model` (str): Имя модели для проверки.

**Возвращает**:
- `str`: Корректное имя модели.

**Вызывает исключения**:
- `ModelNotSupportedError`: Если модель не поддерживается.

**Как работает функция**:

- Если `model` не указана, возвращает `cls.default_model`.
- Если `model` есть в `cls.model_aliases`, заменяет `model` на соответствующий псевдоним.
- Если `model` нет в `cls.models`, выбрасывает исключение `ModelNotSupportedError`.
- Возвращает `model`.

**Примеры**:

```python
model = "gpt-4"
result = DDG.validate_model(model)
print(result)  # Вывод: gpt-4o-mini
```

#### `sleep`

```python
@classmethod
async def sleep(cls, multiplier=1.0):
    """Реализует ограничение скорости между запросами"""
```

**Назначение**: Реализует задержку между запросами для ограничения скорости.

**Параметры**:
- `multiplier` (float): Множитель для задержки.

**Как работает функция**:

- Функция проверяет, было ли установлено время последнего запроса (`cls.last_request_time`).
- Если было, вычисляет задержку на основе разницы между текущим временем и временем последнего запроса.
- Если вычисленная задержка больше нуля, функция ожидает это время с помощью `asyncio.sleep()`.
- Обновляет `cls.last_request_time` текущим временем.

**Примеры**:

```python
await DDG.sleep(multiplier=2.0)
```

#### `get_default_cookies`

```python
@classmethod
async def get_default_cookies(cls, session: ClientSession) -> dict:
    """Получает куки, необходимые для API-запросов по умолчанию"""
```

**Назначение**: Получает куки по умолчанию, необходимые для API-запросов.

**Параметры**:
- `session` (ClientSession): Асинхровая сессия для выполнения HTTP-запросов.

**Возвращает**:
- `dict`: Словарь с куками.

**Как работает функция**:

- Функция выполняет GET-запрос к `cls.url` для получения куки.
- Устанавливает обязательные куки `dcs` и `dcm`.
- Возвращает словарь с установленными куками.

**Примеры**:

```python
async with ClientSession() as session:
    cookies = await DDG.get_default_cookies(session)
    print(cookies)
```

#### `fetch_fe_version`

```python
@classmethod
async def fetch_fe_version(cls, session: ClientSession) -> str:
    """Извлекает fe-version из начальной загрузки страницы."""
```

**Назначение**: Извлекает `fe-version` из HTML-кода главной страницы DuckDuckGo.

**Параметры**:
- `session` (ClientSession): Асинхровая сессия для выполнения HTTP-запросов.

**Возвращает**:
- `str`: Значение `fe-version`.

**Как работает функция**:

- Сначала проверяет, сохранена ли уже версия `fe` в `cls._chat_xfe`. Если да, возвращает сохраненную версию.
- Если версия не сохранена, выполняет GET-запрос к главной странице DuckDuckGo.
- Извлекает компоненты `xfe1` и `xfe2` из HTML-кода.
- Формирует `fe-version` как `f"{xfe1}-{xfe2}"`.
- Сохраняет версию в `cls._chat_xfe`.
- Возвращает полученную версию.

**Примеры**:

```python
async with ClientSession() as session:
    fe_version = await DDG.fetch_fe_version(session)
    print(fe_version)
```

#### `fetch_vqd_and_hash`

```python
@classmethod
async def fetch_vqd_and_hash(cls, session: ClientSession, retry_count: int = 0) -> tuple[str, str]:
    """Получает требуемый VQD токен и хэш для сеанса чата с повторными попытками."""
```

**Назначение**: Получает VQD токен и хэш, необходимые для сессии чата.

**Параметры**:
- `session` (ClientSession): Асинхровая сессия для выполнения HTTP-запросов.
- `retry_count` (int): Количество повторных попыток.

**Возвращает**:
- `tuple[str, str]`: Кортеж, содержащий VQD токен и хэш.

**Вызывает исключения**:
- `RuntimeError`: Если не удалось получить VQD токен и хэш после нескольких попыток.

**Как работает функция**:

- Функция отправляет GET-запрос к `cls.status_url` с определенными заголовками.
- Пытается получить значения `x-vqd-4` и `x-vqd-hash-1` из заголовков ответа.
- Если `vqd` получен, функция возвращает `vqd` и `vqd_hash_1`.
- Если `vqd` не получен, функция повторяет запрос до `cls.max_retries` раз.
- Если после всех попыток не удалось получить `vqd`, функция выбрасывает исключение `RuntimeError`.

**Примеры**:

```python
async with ClientSession() as session:
    vqd, vqd_hash_1 = await DDG.fetch_vqd_and_hash(session)
    print(vqd, vqd_hash_1)
```

#### `create_async_generator`

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
    """Создает асинхронный генератор для взаимодействия с DuckDuckGo AI Chat."""
```

**Назначение**: Создает асинхронный генератор для взаимодействия с DuckDuckGo AI Chat.

**Параметры**:
- `model` (str): Имя модели для использования.
- `messages` (Messages): Список сообщений для отправки.
- `proxy` (str, optional): Прокси для использования.
- `timeout` (int, optional): Время ожидания запроса. По умолчанию 60.
- `cookies` (Cookies, optional): Куки для использования.
- `conversation` (Conversation, optional): Объект Conversation для продолжения существующей беседы.
- `return_conversation` (bool, optional): Флаг, указывающий, нужно ли возвращать объект Conversation.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий сообщения от DuckDuckGo AI Chat.

**Вызывает исключения**:
- `RateLimitError`: Если превышен лимит запросов.
- `TimeoutError`: Если время ожидания истекло.
- `Exception`: Если произошла ошибка при обработке запроса.

**Как работает функция**:

1. **Валидация модели**:
   - Функция вызывает `cls.validate_model(model)` для проверки и получения корректного имени модели.

2. **Повторные попытки**:
   - Функция выполняет запросы с повторными попытками в случае ошибок.

3. **Создание сессии**:
   - Создается асинхронная сессия с использованием `ClientSession`.

4. **Получение `fe_version`**:
   - Если `cls._chat_xfe` не установлена, функция вызывает `cls.fetch_fe_version(session)` для получения `fe_version`.

5. **Инициализация/обновление беседы**:
   - Если `conversation` не передан, создается новый объект `Conversation`.
   - Получаются начальные куки, если они не были предоставлены.
   - Получаются VQD токены с помощью `cls.fetch_vqd_and_hash(session)`.
   - Если `conversation` передан, обновляется история сообщений.

6. **Подготовка заголовков**:
   - Формируются заголовки запроса, включая `x-fe-version`, `x-vqd-4` и `x-vqd-hash-1`.

7. **Подготовка данных**:
   - Формируются данные запроса, включая модель и историю сообщений.

8. **Отправка запроса**:
   - Отправляется POST-запрос к `cls.api_endpoint` с использованием `session.post`.

9. **Обработка ошибок**:
   - Обрабатываются ошибки, такие как `RateLimitError` (429) и `ResponseStatusError`.
   - В случае `RateLimitError`, функция повторяет запрос с увеличенной задержкой.
   - В случае `TimeoutError`, функция выбрасывает исключение `TimeoutError`.

10. **Обработка стримингового ответа**:
    - Функция обрабатывает стриминговый ответ, получая данные построчно.
    - Каждая строка декодируется и обрабатывается как JSON.
    - Извлекаются сообщения и возвращаются через генератор.
    - Обновляется объект `conversation` с полученными данными.

11. **Возврат результата**:
    - Возвращается асинхронный генератор, который выдает сообщения от DuckDuckGo AI Chat.

**Примеры**:

```python
model = "gpt-4o-mini"
messages = [{"role": "user", "content": "Hello"}]
async for message in DDG.create_async_generator(model=model, messages=messages):
    print(message)