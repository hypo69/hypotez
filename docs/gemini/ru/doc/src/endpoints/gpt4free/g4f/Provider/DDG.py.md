# Модуль DDG - DuckDuckGo AI Chat

## Обзор

Этот модуль предоставляет класс `DDG` для работы с DuckDuckGo AI Chat. Класс `DDG` реализует асинхронный генератор для обработки чата, используя API DuckDuckGo AI Chat и поддерживает различные модели, включая `gpt-4o-mini`, `meta-llama/Llama-3.3-70B-Instruct-Turbo`, `claude-3-haiku-20240307`, `o3-mini` и `mistralai/Mistral-Small-24B-Instruct-2501`. 

## Подробно

Модуль реализует класс `DDG`, который предоставляет асинхронный генератор для работы с чатом. В нем используются методы для извлечения VQD-токена и хеша, подготовки запросов, обработки ответов и управления состоянием сессии. 

## Классы

### `class DuckDuckGoSearchException(Exception)`

**Описание**: Базовый класс исключения для duckduckgo_search.

### `class Conversation(JsonConversation)`

**Описание**:  Класс для представления сессии чата. Сохраняет информацию о VQD-токенах, истории сообщений, куки и версии FE.

**Атрибуты**:

- `vqd` (str): VQD-токен.
- `vqd_hash_1` (str): Хеш VQD-токена.
- `message_history` (Messages): Список сообщений в сессии.
- `cookies` (dict): Словарь куки.
- `fe_version` (str): Версия FE.

**Методы**:

- `__init__(self, model: str)`: Инициализирует объект `Conversation`.

### `class DDG(AsyncGeneratorProvider, ProviderModelMixin)`

**Описание**: Класс `DDG` для работы с DuckDuckGo AI Chat. Реализует асинхронный генератор для обработки чата, используя API DuckDuckGo AI Chat.

**Атрибуты**:

- `label` (str): "DuckDuckGo AI Chat".
- `url` (str): "https://duckduckgo.com/aichat".
- `api_endpoint` (str): "https://duckduckgo.com/duckchat/v1/chat".
- `status_url` (str): "https://duckduckgo.com/duckchat/v1/status".
- `working` (bool): True - работает.
- `supports_stream` (bool): True - поддерживает потоковую передачу.
- `supports_system_message` (bool): True - поддерживает системные сообщения.
- `supports_message_history` (bool): True - поддерживает историю сообщений.
- `default_model` (str): "gpt-4o-mini".
- `models` (list): Список поддерживаемых моделей.
- `model_aliases` (dict): Словарь псевдонимов моделей.
- `last_request_time` (int): Время последнего запроса.
- `max_retries` (int): Максимальное количество попыток.
- `base_delay` (int): Базовая задержка.
- `_chat_xfe` (str): Версия FE, хранится как статическая переменная класса.

**Методы**:

- `sha256_base64(text: str) -> str`: Возвращает базовый64-кодированный SHA256-хеш текста.
- `parse_dom_fingerprint(js_text: str) -> str`: Парсит отпечаток DOM из JS-текста.
- `parse_server_hashes(js_text: str) -> list`: Парсит хеши сервера из JS-текста.
- `build_x_vqd_hash_1(vqd_hash_1: str, headers: dict) -> str`: Строит заголовок `x-vqd-hash-1`.
- `validate_model(model: str) -> str`: Валидирует и возвращает правильное имя модели.
- `sleep(multiplier=1.0)`: Реализует ограничение частоты запросов между запросами.
- `get_default_cookies(session: ClientSession) -> dict`: Получает куки по умолчанию, необходимые для API-запросов.
- `fetch_fe_version(session: ClientSession) -> str`: Извлекает версию FE из начальной загрузки страницы.
- `fetch_vqd_and_hash(session: ClientSession, retry_count: int = 0) -> tuple[str, str]`: Извлекает необходимый VQD-токен и хеш для сессии чата с попытками.
- `create_async_generator(model: str, messages: Messages, proxy: str = None, timeout: int = 60, cookies: Cookies = None, conversation: Conversation = None, return_conversation: bool = False, **kwargs) -> AsyncResult`: Создает асинхронный генератор для работы с чатом DuckDuckGo AI Chat.

##  Внутренние функции

###  `def sha256_base64(text: str) -> str`:

**Назначение**:  Создает базовый64-кодированный хеш SHA256 от текстовой строки.

**Параметры**:
- `text` (str): Текстовая строка, из которой нужно получить хеш.

**Возвращает**: 
- `str`: Базовый64-кодированный хеш SHA256 от входной текстовой строки. 

**Как работает функция**:
1. Функция кодирует текстовую строку `text` в UTF-8.
2. Вычисляет хеш SHA256 от закодированной строки.
3. Преобразует результат в базовый64-кодированную строку.
4. Возвращает закодированный хеш.

###  `def parse_dom_fingerprint(js_text: str) -> str`:

**Назначение**:  Парсит отпечаток DOM из JS-текста.

**Параметры**:
- `js_text` (str): JS-текст, содержащий отпечаток DOM.

**Возвращает**:
- `str`: Отпечаток DOM или "1000", если парсинг не удался.

**Как работает функция**:
1. Если `has_bs4` -  True, то функция использует BeautifulSoup для парсинга HTML-фрагмента из JS-текста.
2. Извлекает `inner_html_length` - длину `innerHTML`.
3. Извлекает значение `offset_value` из JS-текста.
4. Вычисляет отпечаток DOM, сложив `offset_value` и `inner_html_length`.
5. Возвращает отпечаток DOM в виде строки.
6. Если парсинг не удался, функция возвращает "1000".

###  `def parse_server_hashes(js_text: str) -> list`:

**Назначение**:  Извлекает хеши сервера из JS-текста.

**Параметры**:
- `js_text` (str): JS-текст, содержащий хеши сервера.

**Возвращает**:
- `list`: Список хешей сервера или ["1", "2"], если парсинг не удался.

**Как работает функция**:
1. Извлекает список хешей сервера из JS-текста.
2. Возвращает список хешей сервера.
3. Если парсинг не удался, функция возвращает ["1", "2"].

###  `def build_x_vqd_hash_1(vqd_hash_1: str, headers: dict) -> str`:

**Назначение**:  Создает заголовок `x-vqd-hash-1` для запросов.

**Параметры**:
- `vqd_hash_1` (str): Хеш VQD-токена.
- `headers` (dict): Словарь заголовков запроса.

**Возвращает**:
- `str`: Значение заголовка `x-vqd-hash-1` или пустую строку, если обработка не удалась.

**Как работает функция**:
1. Декодирует `vqd_hash_1` из base64.
2. Парсит хеши сервера и отпечаток DOM из декодированной строки.
3. Вычисляет SHA256-хеш от `User-Agent` и `sec-ch-ua`.
4. Вычисляет SHA256-хеш от отпечатка DOM.
5. Формирует словарь с хешами сервера и клиента.
6. Кодирует словарь в base64.
7. Возвращает закодированный словарь в качестве значения заголовка `x-vqd-hash-1`.
8. Если обработка не удалась, функция возвращает пустую строку.

###  `def validate_model(model: str) -> str`:

**Назначение**:  Валидирует имя модели и возвращает правильное имя.

**Параметры**:
- `model` (str): Имя модели.

**Возвращает**:
- `str`: Правильное имя модели или выдает исключение `ModelNotSupportedError`, если модель не поддерживается.

**Как работает функция**:
1. Если `model` пуст, то возвращается `default_model`.
2. Если `model` присутствует в `model_aliases`, то возвращается псевдоним из `model_aliases`.
3. Если `model` не присутствует в `models`, то вызывается исключение `ModelNotSupportedError`.
4. Возвращается `model`.

###  `async def sleep(multiplier=1.0)`:

**Назначение**:  Реализует ограничение частоты запросов.

**Параметры**:
- `multiplier` (float): Множитель задержки, по умолчанию 1.0.

**Как работает функция**:
1. Вычисляет задержку, основанную на времени последнего запроса и `multiplier`.
2. Если задержка положительна, то ожидает `delay` секунд.
3. Обновляет `last_request_time` текущим временем.

###  `async def get_default_cookies(session: ClientSession) -> dict`:

**Назначение**:  Получает куки по умолчанию, необходимые для API-запросов.

**Параметры**:
- `session` (ClientSession): Сессия aiohttp.

**Возвращает**:
- `dict`: Словарь куки или пустой словарь, если получение куки не удалось.

**Как работает функция**:
1. Выполняет запрос к `url` для получения куки.
2. Добавляет куки `dcs` и `dcm` в `cookies` и `session.cookie_jar`.
3. Возвращает `cookies`.
4. Если получение куки не удалось, то возвращается пустой словарь.

###  `async def fetch_fe_version(session: ClientSession) -> str`:

**Назначение**:  Извлекает версию FE из начальной загрузки страницы.

**Параметры**:
- `session` (ClientSession): Сессия aiohttp.

**Возвращает**:
- `str`: Версия FE или пустая строка, если извлечение не удалось.

**Как работает функция**:
1. Если `_chat_xfe` не пуст, то возвращается `_chat_xfe`.
2. Выполняет запрос к `url`.
3. Извлекает `__DDG_BE_VERSION__` и `__DDG_FE_CHAT_HASH__` из контента.
4. Формирует `_chat_xfe` и возвращает его.
5. Если извлечение не удалось, то возвращается пустая строка.

###  `async def fetch_vqd_and_hash(session: ClientSession, retry_count: int = 0) -> tuple[str, str]`:

**Назначение**:  Извлекает необходимый VQD-токен и хеш для сессии чата с попытками.

**Параметры**:
- `session` (ClientSession): Сессия aiohttp.
- `retry_count` (int): Счетчик попыток, по умолчанию 0.

**Возвращает**:
- `tuple[str, str]`: VQD-токен и хеш VQD-токена или выдает исключение `RuntimeError`, если получение не удалось.

**Как работает функция**:
1. Выполняет запрос к `status_url` для получения VQD-токена и хеша.
2. Если получение удалось, то возвращает VQD-токен и хеш.
3. Если получение не удалось, то:
    - Если `retry_count` меньше `max_retries`, то увеличивает `retry_count` и ожидает `wait_time` секунд перед повторной попыткой.
    - Если `retry_count` достиг `max_retries`, то выдает исключение `RuntimeError`.

###  `async def create_async_generator(model: str, messages: Messages, proxy: str = None, timeout: int = 60, cookies: Cookies = None, conversation: Conversation = None, return_conversation: bool = False, **kwargs) -> AsyncResult`:

**Назначение**:  Создает асинхронный генератор для работы с чатом DuckDuckGo AI Chat.

**Параметры**:
- `model` (str): Имя модели.
- `messages` (Messages): Список сообщений.
- `proxy` (str): Прокси-сервер, по умолчанию None.
- `timeout` (int): Тайм-аут запроса, по умолчанию 60 секунд.
- `cookies` (Cookies): Куки, по умолчанию None.
- `conversation` (Conversation): Объект `Conversation`, по умолчанию None.
- `return_conversation` (bool): Флаг, указывающий, нужно ли вернуть объект `Conversation`, по умолчанию False.

**Возвращает**:
- `AsyncResult`: Асинхронный результат, который выдает сообщения, объекты `Conversation` или объекты `FinishReason`.

**Как работает функция**:
1. Валидирует модель.
2. Повторяет запрос, пока не будет получен успешный ответ, или пока `retry_count` не достигнет `max_retries`.
3. Создает сессию aiohttp с тайм-аутом.
4. Получает версию FE, если она еще не получена.
5. Инициализирует или обновляет объект `Conversation`.
6. Извлекает VQD-токен и хеш, если объект `Conversation` новый.
7. Добавляет последнее сообщение пользователя в `message_history`.
8. Подготавливает заголовки запроса.
9. Подготавливает данные запроса.
10. Выполняет POST-запрос к `api_endpoint`.
11. Обрабатывает 429 ошибок (RateLimitError).
12. Обрабатывает Streaming-ответ:
    - Выдает сообщения из Streaming-ответа.
    - Обновляет `message_history`, `vqd`, `vqd_hash_1` и `cookies` в объекте `Conversation`.
    - Выдает объект `FinishReason`, если Streaming-ответ завершен.
13. Выдает объект `Conversation`, если `return_conversation` - True.
14. Если запрос завершен успешно, то прерывает цикл.
15. Обрабатывает ошибки:
    - `RateLimitError`, `ResponseStatusError`: Повторяет запрос, если `retry_count` меньше `max_retries`.
    - `asyncio.TimeoutError`: Выдает исключение `TimeoutError`.
    - Другие исключения: Выдает исключение.