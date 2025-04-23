# src/endpoints/gpt4free/g4f/Provider/ChatGpt.py

## Обзор

Модуль `ChatGpt.py` предназначен для взаимодействия с моделью ChatGpt через API. Он включает в себя функции для форматирования сообщений, инициализации сессии, получения моделей и создания завершений. Модуль поддерживает историю сообщений, системные сообщения и потоковую передачу данных.

## Более подробно

Модуль содержит класс `ChatGpt`, который является провайдером для работы с моделью ChatGpt. В модуле реализована поддержка различных моделей, таких как `gpt-3.5-turbo`, `gpt-4o`, `gpt-4` и другие. Также модуль содержит функции для форматирования запросов и обработки ответов от API ChatGpt.
В коде реализована поддержка токенов безопасности, таких как `turnstile` и `proofofwork`, для защиты от несанкционированного доступа.

## Классы

### `ChatGpt`

**Описание**: Класс `ChatGpt` является провайдером для работы с моделью ChatGpt.

**Наследует**:
- `AbstractProvider`: Абстрактный класс, определяющий интерфейс для всех провайдеров.
- `ProviderModelMixin`: Класс, предоставляющий общие методы для работы с моделями провайдера.

**Атрибуты**:
- `label` (str): Метка провайдера, в данном случае `"ChatGpt"`.
- `url` (str): URL для доступа к ChatGpt, `"https://chatgpt.com"`.
- `working` (bool): Флаг, указывающий, работает ли провайдер, в данном случае `False`.
- `supports_message_history` (bool): Флаг, указывающий, поддерживает ли провайдер историю сообщений, `True`.
- `supports_system_message` (bool): Флаг, указывающий, поддерживает ли провайдер системные сообщения, `True`.
- `supports_stream` (bool): Флаг, указывающий, поддерживает ли провайдер потоковую передачу данных, `True`.
- `default_model` (str): Модель, используемая по умолчанию, `"auto"`.
- `models` (List[str]): Список поддерживаемых моделей.
- `model_aliases` (Dict[str, str]): Словарь с псевдонимами моделей.

**Принцип работы**:
Класс `ChatGpt` предоставляет методы для взаимодействия с API ChatGpt. Он включает в себя функции для получения токенов безопасности, форматирования сообщений и создания запросов к API. Класс также поддерживает потоковую передачу данных, что позволяет получать ответы от API в режиме реального времени.

**Методы**:
- `get_model(model: str) -> str`: Возвращает имя модели на основе псевдонима или имени по умолчанию.
- `create_completion(model: str, messages: Messages, stream: bool, **kwargs) -> CreateResult`: Создает запрос к API ChatGpt и возвращает результат.

## Функции

### `format_conversation(messages: list) -> list`

**Назначение**: Форматирует список сообщений в формат, требуемый для API ChatGpt.

**Параметры**:
- `messages` (list): Список сообщений, где каждое сообщение представляет собой словарь с ключами `role` и `content`.

**Возвращает**:
- `list`: Отформатированный список сообщений.

**Как работает функция**:
Функция преобразует входной список сообщений в формат, который соответствует структуре, ожидаемой API ChatGpt. Для каждого сообщения создается уникальный идентификатор `uuid`, добавляется информация об авторе (`role`), содержимом (`content`) и метаданные.

**Примеры**:

```python
messages = [
    {'role': 'user', 'content': 'Hello'},
    {'role': 'assistant', 'content': 'Hi there'}
]
formatted_messages = format_conversation(messages)
print(formatted_messages)
# Вывод:
# [{'id': '...', 'author': {'role': 'user'}, 'content': {'content_type': 'text', 'parts': ['Hello']}, 'metadata': {'serialization_metadata': {'custom_symbol_offsets': []}}, 'create_time': ...}, 
#  {'id': '...', 'author': {'role': 'assistant'}, 'content': {'content_type': 'text', 'parts': ['Hi there']}, 'metadata': {'serialization_metadata': {'custom_symbol_offsets': []}}, 'create_time': ...}]
```

### `init_session(user_agent: str) -> Session`

**Назначение**: Инициализирует сессию для взаимодействия с API ChatGpt.

**Параметры**:
- `user_agent` (str): User-agent для установки в заголовках HTTP-запросов.

**Возвращает**:
- `Session`: Объект сессии `requests.Session`.

**Как работает функция**:
Функция создает объект сессии `requests.Session` и устанавливает необходимые заголовки и куки для взаимодействия с API ChatGpt. Это включает в себя установку `user-agent`, принятых типов контента и других параметров, необходимых для успешного выполнения запросов.

**Примеры**:

```python
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
session = init_session(user_agent)
print(session.headers)
# Вывод:
# {'accept': '*/*', 'accept-language': 'en-US,en;q=0.8', 'cache-control': 'no-cache', 'pragma': 'no-cache', 'priority': 'u=0, i', 'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"', 'sec-ch-ua-arch': '"arm"', 'sec-ch-ua-bitness': '"64"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-model': '""', 'sec-ch-ua-platform': '"macOS"', 'sec-ch-ua-platform-version': '"14.4.0"', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'none', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36', 'Accept-Encoding': 'gzip, deflate, br'}
```

### `ChatGpt.get_model(model: str) -> str`

**Назначение**: Возвращает имя модели на основе псевдонима или имени по умолчанию.

**Параметры**:
- `model` (str): Имя модели или псевдоним.

**Возвращает**:
- `str`: Имя модели.

**Как работает функция**:
Функция проверяет, является ли входное имя модели допустимым, сравнивая его с предопределенным списком моделей и псевдонимов. Если модель найдена в списке псевдонимов, она возвращает соответствующее имя модели. В противном случае, если модель есть в списке поддерживаемых моделей, она возвращает само имя модели. Если модель не найдена ни в одном из списков, возвращается имя модели по умолчанию.

**Примеры**:

```python
model_name = ChatGpt.get_model('gpt-4o')
print(model_name)
# Вывод: chatgpt-4o-latest

model_name = ChatGpt.get_model('gpt-3.5-turbo')
print(model_name)
# Вывод: gpt-3.5-turbo

model_name = ChatGpt.get_model('invalid-model')
print(model_name)
# Вывод: auto
```

### `ChatGpt.create_completion(model: str, messages: Messages, stream: bool, **kwargs) -> CreateResult`

**Назначение**: Создает запрос к API ChatGpt и возвращает результат.

**Параметры**:
- `model` (str): Имя модели.
- `messages` (Messages): Список сообщений.
- `stream` (bool): Флаг, указывающий, использовать ли потоковую передачу данных.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `CreateResult`: Результат запроса.

**Как работает функция**:
Функция выполняет следующие шаги:
1. Получает имя модели с помощью `ChatGpt.get_model(model)`.
2. Инициализирует сессию с помощью `init_session(user_agent)`.
3. Получает конфигурацию и токены безопасности.
4. Форматирует сообщения с помощью `format_conversation(messages)`.
5. Отправляет запрос к API ChatGpt и обрабатывает ответ.
6. Если `stream=True`, возвращает генератор, который выдает токены по мере их поступления.

**Примеры**:

```python
messages = [
    {'role': 'user', 'content': 'Hello'}
]
stream = True
result = ChatGpt.create_completion(model='gpt-3.5-turbo', messages=messages, stream=stream)
for token in result:
    print(token)
# Вывод:
# Hi
# there
```