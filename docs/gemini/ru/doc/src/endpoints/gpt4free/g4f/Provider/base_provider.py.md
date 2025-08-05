# Модуль `base_provider`

## Обзор

Этот модуль предоставляет базовый класс для реализации провайдеров для GPT4Free API. 
Он определяет общие методы и свойства, которые используются всеми провайдерами, 
обеспечивая единый интерфейс для взаимодействия с API.

## Классы

### `class BaseProvider`

**Описание**: Базовый класс для реализации провайдеров для GPT4Free API.

**Наследует**: 
    - `object`

**Атрибуты**:
    - `api_url (str)`: URL-адрес API.
    - `session (requests.Session)`: Сессия `requests` для отправки запросов API.
    - `headers (dict)`: Заголовки HTTP-запросов.
    - `cookies (dict)`: Cookies для аутентификации.

**Методы**:
    - `_build_headers (dict)`: Возвращает заголовки для запросов API.
    - `_build_cookies (dict)`: Возвращает cookies для аутентификации.
    - `_make_request (method: str, url: str, params: dict, data: dict, headers: dict, cookies: dict) -> requests.Response`: Выполняет запрос API с помощью `requests`.
    - `_send_request (method: str, params: dict, data: dict, headers: dict, cookies: dict) -> requests.Response`: Выполняет запрос API с использованием `self.session`.
    - `_process_response (response: requests.Response) -> dict`: Обрабатывает ответ API и возвращает данные.
    - `send_request (method: str, params: dict, data: dict) -> dict`: Отправляет запрос API и возвращает обработанные данные.

## Функции

### `build_response (response: dict, conversation: BaseConversation, is_streaming: bool = False) -> BaseConversation`:

**Назначение**: Строит объект `BaseConversation` из ответа API.

**Параметры**:
- `response (dict)`: Ответ API.
- `conversation (BaseConversation)`: Текущий объект `BaseConversation`.
- `is_streaming (bool)`: Флаг, указывающий, является ли ответ потоковым.

**Возвращает**:
- `BaseConversation`: Объект `BaseConversation`, содержащий данные из ответа API.

**Вызывает исключения**:
- `ValueError`: Если ответ API не содержит ожидаемых данных.

**Как работает функция**:
- Извлекает текст ответа API и добавляет его к `conversation.content`.
- Обновляет `conversation.sources` с информацией об источнике ответа.
- Устанавливает `conversation.finish_reason` в зависимости от статуса ответа.

**Примеры**:
```python
>>> response = {'content': 'Hello, world!', 'sources': ['gpt4free'], 'finish_reason': 'stop'}
>>> conversation = BaseConversation()
>>> build_response(response, conversation)
<BaseConversation(content='Hello, world!', sources=['gpt4free'], finish_reason='stop', ...)>
```

### `get_stream_response (response: requests.Response) -> Generator[BaseConversation, None, None]`:

**Назначение**: Предоставляет потоковый ответ API как генератор объектов `BaseConversation`.

**Параметры**:
- `response (requests.Response)`: Ответ API.

**Возвращает**:
- `Generator[BaseConversation, None, None]`: Генератор объектов `BaseConversation`, 
   содержащих части потокового ответа API.

**Вызывает исключения**:
- `ValueError`: Если ответ API не содержит ожидаемых данных.

**Как работает функция**:
- Получает данные потокового ответа API с помощью `response.iter_lines()`.
- Преобразует каждую часть ответа в JSON.
- Создает объект `BaseConversation` из каждого JSON-объекта.
- Возвращает генератор, который выдает объекты `BaseConversation`.

**Примеры**:
```python
>>> response = requests.get('https://api.gpt4free.com/stream')
>>> for conversation in get_stream_response(response):
...     print(conversation.content)
...
Hello,
world!
```

### `get_default_headers (custom_headers: dict = None) -> dict`:

**Назначение**: Возвращает стандартные заголовки для запросов API.

**Параметры**:
- `custom_headers (dict)`: Дополнительные заголовки.

**Возвращает**:
- `dict`: Словарь стандартных заголовков.

**Как работает функция**:
- Возвращает словарь, содержащий стандартные заголовки, такие как `User-Agent`, `Content-Type` и т. д.
- Если `custom_headers` не равен `None`, добавляет его значения к стандартным заголовкам.

**Примеры**:
```python
>>> get_default_headers()
{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36', 'Content-Type': 'application/json'}
>>> get_default_headers({'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'})
{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36', 'Content-Type': 'application/json', 'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'}
```

### `get_default_cookies (custom_cookies: dict = None) -> dict`:

**Назначение**: Возвращает стандартные cookies для аутентификации.

**Параметры**:
- `custom_cookies (dict)`: Дополнительные cookies.

**Возвращает**:
- `dict`: Словарь стандартных cookies.

**Как работает функция**:
- Возвращает словарь, содержащий стандартные cookies, которые используются для аутентификации в API.
- Если `custom_cookies` не равен `None`, добавляет его значения к стандартным cookies.

**Примеры**:
```python
>>> get_default_cookies()
{'session_id': 'your_session_id'}
>>> get_default_cookies({'user_id': 'your_user_id'})
{'session_id': 'your_session_id', 'user_id': 'your_user_id'}
```

## Внутренние функции

### `get_cookies (custom_cookies: dict = None) -> dict`:

**Назначение**: Возвращает cookies для аутентификации.

**Параметры**:
- `custom_cookies (dict)`: Дополнительные cookies.

**Возвращает**:
- `dict`: Словарь cookies.

**Как работает функция**:
- Вызывает функцию `_build_cookies` для получения стандартных cookies.
- Если `custom_cookies` не равен `None`, добавляет его значения к стандартным cookies.

**Примеры**:
```python
>>> get_cookies()
{'session_id': 'your_session_id'}
>>> get_cookies({'user_id': 'your_user_id'})
{'session_id': 'your_session_id', 'user_id': 'your_user_id'}
```

### `format_prompt (conversation: BaseConversation, prompt: str, model: str, is_streaming: bool = False) -> dict`:

**Назначение**: Форматирует запрос для API GPT4Free.

**Параметры**:
- `conversation (BaseConversation)`: Объект `BaseConversation`, содержащий контекст разговора.
- `prompt (str)`: Текст запроса.
- `model (str)`: Имя модели GPT4Free.
- `is_streaming (bool)`: Флаг, указывающий, является ли запрос потоковым.

**Возвращает**:
- `dict`: Словарь, содержащий данные запроса API GPT4Free.

**Как работает функция**:
- Создает словарь, содержащий данные запроса API GPT4Free:
    - `model`: Имя модели GPT4Free.
    - `prompt`: Текст запроса.
    - `conversation_id`: Идентификатор текущего разговора.
    - `parent_message_id`: Идентификатор предыдущего сообщения в разговоре.
    - `is_streaming`: Флаг, указывающий, является ли запрос потоковым.
- Возвращает созданный словарь.

**Примеры**:
```python
>>> conversation = BaseConversation(conversation_id='12345', parent_message_id='67890')
>>> format_prompt(conversation, 'Hello, world!', 'gpt4free')
{'model': 'gpt4free', 'prompt': 'Hello, world!', 'conversation_id': '12345', 'parent_message_id': '67890', 'is_streaming': False}