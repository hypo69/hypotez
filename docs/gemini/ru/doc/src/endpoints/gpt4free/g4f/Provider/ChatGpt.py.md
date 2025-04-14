# Модуль ChatGpt

## Обзор

Модуль `ChatGpt` предоставляет класс для взаимодействия с моделью ChatGpt от OpenAI. Он позволяет отправлять сообщения и получать ответы, поддерживая как потоковую передачу ответов, так и использование истории сообщений.

## Подробнее

Модуль содержит класс `ChatGpt`, который наследуется от `AbstractProvider` и `ProviderModelMixin`. Он использует библиотеку `requests` для выполнения HTTP-запросов к API ChatGpt. В модуле определены функции для форматирования сообщений, инициализации сессии и получения токенов, необходимых для аутентификации.

## Классы

### `ChatGpt`

**Описание**: Класс для взаимодействия с моделью ChatGpt.

**Наследует**:
- `AbstractProvider`: Абстрактный класс, определяющий интерфейс для провайдеров моделей.
- `ProviderModelMixin`: Класс, предоставляющий общие методы для работы с моделями.

**Атрибуты**:
- `label` (str): Метка провайдера ("ChatGpt").
- `url` (str): URL для ChatGpt ("https://chatgpt.com").
- `working` (bool): Флаг, указывающий, работает ли провайдер (False).
- `supports_message_history` (bool): Флаг, указывающий, поддерживает ли провайдер историю сообщений (True).
- `supports_system_message` (bool): Флаг, указывающий, поддерживает ли провайдер системные сообщения (True).
- `supports_stream` (bool): Флаг, указывающий, поддерживает ли провайдер потоковую передачу (True).
- `default_model` (str): Модель по умолчанию ('auto').
- `models` (List[str]): Список поддерживаемых моделей.
- `model_aliases` (Dict[str, str]): Словарь псевдонимов моделей.

**Методы**:
- `get_model(model: str) -> str`: Возвращает имя модели на основе псевдонима или имени, или модель по умолчанию, если модель не найдена.
- `create_completion(model: str, messages: Messages, stream: bool, **kwargs) -> CreateResult`: Создает запрос на завершение текста и возвращает результат.

## Функции

### `format_conversation(messages: list) -> list`

**Назначение**: Форматирует список сообщений в формат, требуемый API ChatGpt.

**Параметры**:
- `messages` (list): Список сообщений, где каждое сообщение представляет собой словарь с ключами 'role' и 'content'.

**Возвращает**:
- `list`: Список словарей, представляющих отформатированные сообщения.

**Как работает функция**:
Функция итерируется по списку сообщений и преобразует каждое сообщение в словарь, содержащий информацию об авторе (роль), содержимом (текст сообщения) и метаданные. Каждому сообщению присваивается уникальный идентификатор UUID.

**Примеры**:

```python
messages = [
    {'role': 'user', 'content': 'Привет!'},
    {'role': 'assistant', 'content': 'Здравствуйте!'}
]
formatted_messages = format_conversation(messages)
print(formatted_messages)
# Вывод:
# [
#     {'id': '...', 'author': {'role': 'user'}, 'content': {'content_type': 'text', 'parts': ['Привет!']}, 'metadata': {'serialization_metadata': {'custom_symbol_offsets': []}}, 'create_time': ...},
#     {'id': '...', 'author': {'role': 'assistant'}, 'content': {'content_type': 'text', 'parts': ['Здравствуйте!']}, 'metadata': {'serialization_metadata': {'custom_symbol_offsets': []}}, 'create_time': ...}
# ]
```

### `init_session(user_agent: str) -> Session`

**Назначение**: Инициализирует сессию requests с заданным user-agent и устанавливает необходимые заголовки.

**Параметры**:
- `user_agent` (str): User-agent для использования в HTTP-запросах.

**Возвращает**:
- `Session`: Инициализированная сессия requests.

**Как работает функция**:
Функция создает объект сессии `requests.Session`, устанавливает куки и заголовки, необходимые для взаимодействия с API ChatGpt, и выполняет GET-запрос к `https://chatgpt.com/`, чтобы установить необходимые куки.

**Примеры**:

```python
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
session = init_session(user_agent)
print(session.headers)
# Вывод:
# {'accept': '*/*', 'accept-language': 'en-US,en;q=0.8', 'cache-control': 'no-cache', 'pragma': 'no-cache', 'priority': 'u=0, i', 'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"', 'sec-ch-ua-arch': '"arm"', 'sec-ch-ua-bitness': '"64"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-model': '""', 'sec-ch-ua-platform': '"macOS"', 'sec-ch-ua-platform-version': '"14.4.0"', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'none', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36', 'Cookie': '_dd_s='}
```

### `ChatGpt.get_model(model: str) -> str`

**Назначение**: Возвращает имя модели на основе псевдонима или имени, или модель по умолчанию, если модель не найдена.

**Параметры**:
- `model` (str): Имя модели или псевдоним.

**Возвращает**:
- `str`: Имя модели.

**Как работает функция**:
Функция проверяет, есть ли указанная модель в списке поддерживаемых моделей или в словаре псевдонимов. Если модель найдена в псевдонимах, возвращается соответствующее имя модели. Если модель не найдена ни в списке, ни в псевдонимах, возвращается модель по умолчанию.

**Примеры**:

```python
model_name = ChatGpt.get_model('gpt-4o')
print(model_name)
# Вывод: chatgpt-4o-latest

model_name = ChatGpt.get_model('gpt-3.5-turbo')
print(model_name)
# Вывод: gpt-3.5-turbo

model_name = ChatGpt.get_model('unknown_model')
print(model_name)
# Вывод: auto
```

### `ChatGpt.create_completion(model: str, messages: Messages, stream: bool, **kwargs) -> CreateResult`

**Назначение**: Создает запрос на завершение текста и возвращает результат.

**Параметры**:
- `model` (str): Имя модели для использования.
- `messages` (Messages): Список сообщений для отправки.
- `stream` (bool): Флаг, указывающий, использовать ли потоковую передачу.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `CreateResult`: Результат запроса.

**Вызывает исключения**:
- `ValueError`: Если указанная модель недоступна.

**Как работает функция**:

1.  Определяет user\_agent
2.  Инициализирует сессию `session: Session = init_session(user_agent)`
3.  Получает конфигурацию `config = get_config(user_agent)`
4.  Запрашивает токены безопасности `pow_req = get_requirements_token(config)`
5.  Задает заголовки, необходимые для запроса `headers = { ... }`
6.  Отправляет POST-запрос на URL `'https://chatgpt.com/backend-anon/sentinel/chat-requirements'` с целью получить дополнительные параметры безопасности (токены)
7.  Обрабатывает ответ, проверяя наличие ошибок и извлекая необходимые данные, такие как `turnstile` и `pow_conf`.
8.  Если требуется, обрабатывает `turnstile` (проверку CAPTCHA) для получения токена `turnstile_token`.
9.  Обновляет заголовки, добавляя токены безопасности, полученные на предыдущих шагах.
10. Формирует JSON-данные для отправки сообщения, включая форматированные сообщения, параметры модели и другие настройки.
11. Выполняет задержку в 2 секунды `time.sleep(2)`
12. Отправляет POST-запрос на URL `'https://chatgpt.com/backend-anon/conversation'` с заголовками, JSON-данными и включенной потоковой передачей.
13. Обрабатывает потоковый ответ, извлекая данные JSON из каждой строки ответа.
14. Извлекает содержимое сообщения ответа и генерирует его.
15. Возвращает результат в виде потока токенов.

**Примеры**:

```python
messages = [
    {'role': 'user', 'content': 'Привет!'}
]
stream = True
result = ChatGpt.create_completion(model='gpt-3.5-turbo', messages=messages, stream=stream)
for token in result:
    print(token, end='')
# Вывод: Здравствуйте!