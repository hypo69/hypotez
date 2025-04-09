# Модуль `ChatGpt.py`

## Обзор

Модуль `ChatGpt.py` предоставляет класс `ChatGpt`, который является провайдером для взаимодействия с моделью ChatGPT. Он позволяет создавать запросы к ChatGPT, обрабатывать ответы и поддерживает как потоковую передачу данных, так и работу с историей сообщений. Модуль использует библиотеки `requests`, `uuid`, `time` и другие для организации HTTP-запросов, генерации уникальных идентификаторов и обработки времени.

## Подробней

Этот модуль является частью системы `hypotez` и предназначен для интеграции с различными AI-провайдерами. Он реализует логику взаимодействия с ChatGPT, включая аутентификацию, формирование запросов и обработку ответов. `ChatGpt` поддерживает разные модели ChatGPT, такие как `gpt-3.5-turbo`, `gpt-4` и другие.

## Функции

### `format_conversation`

```python
def format_conversation(messages: list) -> list:
    """
    Преобразует список сообщений в формат, ожидаемый API ChatGPT.

    Args:
        messages (list): Список сообщений, где каждое сообщение представляет собой словарь с ключами 'role' и 'content'.

    Returns:
        list: Список преобразованных сообщений, готовых для отправки в API ChatGPT.

    Как работает функция:
    1.  Функция принимает на вход список сообщений.
    2.  Создает пустой список `conversation` для хранения преобразованных сообщений.
    3.  Итерируется по каждому сообщению в списке `messages`.
    4.  Для каждого сообщения создает словарь, соответствующий формату API ChatGPT, включая `id`, `author`, `content`, `metadata` и `create_time`.
    5.  Добавляет преобразованное сообщение в список `conversation`.
    6.  Возвращает список `conversation`.
    """
```
**ASCII flowchart функции `format_conversation`**

```
A [Вход: messages]
|
B [Инициализация conversation = []]
|
C [Итерация по messages]
|
D [Преобразование message в формат API]
|
E [Добавление в conversation]
|
F [Выход: conversation]
```

**Примеры использования**

```python
messages = [
    {'role': 'user', 'content': 'Hello'},
    {'role': 'assistant', 'content': 'Hi there'}
]
formatted_messages = format_conversation(messages)
print(formatted_messages)
# Вывод:
# [{'id': '...', 'author': {'role': 'user'}, 'content': {'content_type': 'text', 'parts': ['Hello']}, 'metadata': {'serialization_metadata': {'custom_symbol_offsets': []}}, 'create_time': ...}, {'id': '...', 'author': {'role': 'assistant'}, 'content': {'content_type': 'text', 'parts': ['Hi there']}, 'metadata': {'serialization_metadata': {'custom_symbol_offsets': []}}, 'create_time': ...}]
```

### `init_session`

```python
def init_session(user_agent: str) -> Session:
    """
    Инициализирует сессию requests с необходимыми заголовками и куками.

    Args:
        user_agent (str): User-agent для установки в заголовках сессии.

    Returns:
        Session: Инициализированная сессия requests.

    Как работает функция:
    1.  Функция принимает строку user-agent в качестве аргумента.
    2.  Создает новый объект `Session` из библиотеки `requests`.
    3.  Определяет словарь `cookies` и `headers` для сессии.
    4.  Выполняет GET-запрос к `https://chatgpt.com/` с установленными cookies и headers.
    5.  Возвращает настроенную сессию.
    """
```

**ASCII flowchart функции `init_session`**

```
A [Вход: user_agent]
|
B [Создание session = Session()]
|
C [Определение cookies и headers]
|
D [GET-запрос к chatgpt.com]
|
E [Выход: session]
```

**Примеры использования**

```python
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
session = init_session(user_agent)
print(session)
# Вывод: <requests.sessions.Session object at 0x...>
```

## Классы

### `ChatGpt`

```python
class ChatGpt(AbstractProvider, ProviderModelMixin):
    """
    Провайдер для взаимодействия с API ChatGPT.

    Inherits:
        AbstractProvider: Абстрактный класс провайдера.
        ProviderModelMixin: Миксин для работы с моделями провайдера.

    Attributes:
        label (str): Метка провайдера ("ChatGpt").
        url (str): URL ChatGPT ("https://chatgpt.com").
        working (bool): Индикатор работоспособности провайдера (False).
        supports_message_history (bool): Поддержка истории сообщений (True).
        supports_system_message (bool): Поддержка системных сообщений (True).
        supports_stream (bool): Поддержка потоковой передачи (True).
        default_model (str): Модель по умолчанию ('auto').
        models (list): Список поддерживаемых моделей.
        model_aliases (dict): Алиасы моделей.
    """
```
**Методы:**

- `get_model(model: str) -> str:`: Возвращает имя модели на основе заданного алиаса или значения по умолчанию.
- `create_completion(model: str, messages: Messages, stream: bool, **kwargs) -> CreateResult:`: Создает запрос на завершение текста к API ChatGPT и обрабатывает ответ.

```python
    @classmethod
    def get_model(cls, model: str) -> str:
        """
        Возвращает имя модели на основе заданного алиаса или значения по умолчанию.

        Args:
            model (str): Имя модели или алиас.

        Returns:
            str: Имя модели.

        Как работает функция:
        1.  Функция принимает строку `model` в качестве аргумента.
        2.  Проверяет, есть ли `model` в списке поддерживаемых моделей `cls.models`.
        3.  Если `model` есть в списке, возвращает `model`.
        4.  Если `model` есть в словаре `cls.model_aliases`, возвращает соответствующее значение из словаря.
        5.  В противном случае возвращает значение `cls.default_model`.
        """
```
**ASCII flowchart функции `get_model`**

```
A [Вход: model]
|
B [Проверка: model in cls.models]
|
C [Если да: возврат model]
|
D [Если нет: проверка model in cls.model_aliases]
|
E [Если да: возврат cls.model_aliases[model]]
|
F [Если нет: возврат cls.default_model]
```

**Примеры использования**

```python
model_name = ChatGpt.get_model('gpt-4o')
print(model_name)
# Вывод: chatgpt-4o-latest

model_name = ChatGpt.get_model('gpt-3.5-turbo')
print(model_name)
# Вывод: gpt-3.5-turbo

model_name = ChatGpt.get_model('unknown-model')
print(model_name)
# Вывод: auto
```
```python
    @classmethod
    def create_completion(
        cls,
        model: str,
        messages: Messages,
        stream: bool,
        **kwargs
    ) -> CreateResult:
        """
        Создает запрос на завершение текста к API ChatGPT и обрабатывает ответ.

        Args:
            model (str): Имя модели.
            messages (Messages): Список сообщений для отправки.
            stream (bool): Флаг потоковой передачи.
            **kwargs: Дополнительные параметры.

        Returns:
            CreateResult: Результат запроса.

        Raises:
            ValueError: Если указанная модель недоступна.

        Как работает функция:
        1.  Функция принимает имя модели, список сообщений, флаг потоковой передачи и дополнительные аргументы.
        2.  Получает имя модели с помощью `cls.get_model(model)`.
        3.  Проверяет, доступна ли полученная модель в списке `cls.models`.
        4.  Если модель недоступна, вызывает исключение `ValueError`.
        5.  Инициализирует сессию с помощью `init_session`.
        6.  Получает конфигурацию, токены и заголовки.
        7.  Выполняет POST-запрос к API ChatGPT с необходимыми данными и заголовками.
        8.  Обрабатывает потоковый ответ, если `stream` равен `True`.
        9.  Возвращает результат запроса.
        """
```

**ASCII flowchart функции `create_completion`**

```
A [Вход: model, messages, stream, kwargs]
|
B [Получение имени модели: model = cls.get_model(model)]
|
C [Проверка: model in cls.models]
|
D [Если нет: Вызов ValueError]
|
E [Инициализация сессии: session = init_session()]
|
F [Получение конфигурации, токенов, заголовков]
|
G [POST-запрос к API ChatGPT]
|
H [Обработка потокового ответа (если stream)]
|
I [Выход: CreateResult]
```

**Примеры использования**

```python
messages = [
    {'role': 'user', 'content': 'Напиши Hello World на Python'}
]
result = ChatGpt.create_completion(model='gpt-3.5-turbo', messages=messages, stream=False)
print(result)
# Вывод: <generator object AbstractProvider.create_completion.<locals>.stream_response at 0x...> (если stream=True)
# или строка с ответом (если stream=False)