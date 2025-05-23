# Модуль `ChatGpt.py`

## Обзор

Модуль `ChatGpt.py` предоставляет реализацию провайдера `ChatGpt` для взаимодействия с API ChatGPT. Он включает в себя функции для форматирования сообщений, инициализации сессии, а также создания запросов на завершение текста.

## Подробнее

Модуль содержит класс `ChatGpt`, который наследуется от `AbstractProvider` и `ProviderModelMixin`. Он отвечает за установление соединения с серверами ChatGPT, отправку запросов и обработку ответов. Класс поддерживает различные модели ChatGPT и предоставляет гибкие настройки для взаимодействия с API.

## Классы

### `ChatGpt`

**Описание**: Класс `ChatGpt` предоставляет интерфейс для взаимодействия с моделью ChatGPT. Он позволяет отправлять сообщения и получать ответы, поддерживая потоковую передачу данных.

**Наследует**:
- `AbstractProvider`: Абстрактный базовый класс для всех провайдеров.
- `ProviderModelMixin`: Предоставляет вспомогательные методы для работы с моделями.

**Атрибуты**:
- `label` (str): Метка провайдера, в данном случае "ChatGpt".
- `url` (str): URL для доступа к ChatGPT API.
- `working` (bool): Флаг, указывающий, работает ли провайдер в данный момент.
- `supports_message_history` (bool): Флаг, указывающий, поддерживает ли провайдер историю сообщений.
- `supports_system_message` (bool): Флаг, указывающий, поддерживает ли провайдер системные сообщения.
- `supports_stream` (bool): Флаг, указывающий, поддерживает ли провайдер потоковую передачу данных.
- `default_model` (str): Модель, используемая по умолчанию, в данном случае 'auto'.
- `models` (List[str]): Список поддерживаемых моделей.
- `model_aliases` (Dict[str, str]): Словарь псевдонимов моделей.

**Методы**:
- `get_model(model: str) -> str`: Возвращает имя модели на основе псевдонима или значения по умолчанию.
- `create_completion(model: str, messages: Messages, stream: bool, **kwargs) -> CreateResult`: Создает запрос на завершение текста и возвращает результат.

### `ChatGpt.get_model`

```python
    @classmethod
    def get_model(cls, model: str) -> str:
        """Возвращает имя модели на основе псевдонима или значения по умолчанию.
        Args:
            model (str): Имя модели или псевдоним.

        Returns:
            str: Имя модели.
        """
```

**Назначение**:
Метод `get_model` принимает имя модели в качестве аргумента и возвращает соответствующее имя модели, используя псевдонимы или значение по умолчанию, если имя модели не найдено в списке поддерживаемых моделей.

**Параметры**:
- `model` (str): Имя модели или псевдоним.

**Возвращает**:
- `str`: Имя модели.

**Как работает функция**:
1. Проверяется, находится ли `model` в списке поддерживаемых моделей `cls.models`. Если да, то `model` возвращается без изменений.
2. Если `model` не найдена в `cls.models`, проверяется, находится ли `model` в словаре псевдонимов `cls.model_aliases`. Если да, то возвращается соответствующее значение из словаря псевдонимов.
3. Если `model` не найдена ни в `cls.models`, ни в `cls.model_aliases`, возвращается значение по умолчанию `cls.default_model`.

**Примеры**:

```python
#Пример 1: Модель есть в списке поддерживаемых
model_name = ChatGpt.get_model("gpt-3.5-turbo")
print(model_name) #Вывод: gpt-3.5-turbo

#Пример 2: Модель есть в списке псевдонимов
model_name = ChatGpt.get_model("gpt-4o")
print(model_name) #Вывод: chatgpt-4o-latest

#Пример 3: Модель не найдена, возвращается модель по умолчанию
model_name = ChatGpt.get_model("unsupported-model")
print(model_name) #Вывод: auto
```

### `ChatGpt.create_completion`

```python
    @classmethod
    def create_completion(
        cls,
        model: str,
        messages: Messages,
        stream: bool,
        **kwargs
    ) -> CreateResult:
        """Создает запрос на завершение текста и возвращает результат.

        Args:
            model (str): Имя модели.
            messages (Messages): Список сообщений.
            stream (bool): Флаг, указывающий, использовать ли потоковую передачу данных.
            **kwargs: Дополнительные аргументы.

        Returns:
            CreateResult: Результат создания запроса.

        Raises:
            ValueError: Если указанная модель не поддерживается.
        """
```

**Назначение**:
Метод `create_completion` создает запрос на завершение текста, используя указанную модель и сообщения, и возвращает результат. Он также обрабатывает параметры для потоковой передачи данных и проверяет доступность модели.

**Параметры**:
- `model` (str): Имя модели.
- `messages` (Messages): Список сообщений.
- `stream` (bool): Флаг, указывающий, использовать ли потоковую передачу данных.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `CreateResult`: Результат создания запроса.

**Вызывает исключения**:
- `ValueError`: Если указанная модель не поддерживается.

**Как работает функция**:
1. Получает имя модели, используя метод `cls.get_model(model)`.
2. Проверяет, находится ли полученная модель в списке поддерживаемых моделей `cls.models`. Если нет, вызывает исключение `ValueError`.
3. Инициализирует сессию с использованием `init_session`.
4. Получает конфигурацию с использованием `get_config`.
5. Получает токен требований с использованием `get_requirements_token`.
6. Формирует заголовки запроса.
7. Отправляет POST-запрос на `https://chatgpt.com/backend-anon/sentinel/chat-requirements` для получения данных, необходимых для прохождения защиты.
8. Обрабатывает ответ, проверяя наличие ошибок и извлекая необходимые токены.
9. Формирует `json_data` с данными для запроса к API ChatGPT.
10. Отправляет POST-запрос на `https://chatgpt.com/backend-anon/conversation` с потоковой передачей данных.
11. Обрабатывает потоковый ответ, извлекая токены и возвращая их.

## Функции

### `format_conversation`

```python
def format_conversation(messages: list):
    """Форматирует список сообщений в формат, ожидаемый API ChatGPT.

    Args:
        messages (list): Список сообщений.

    Returns:
        list: Отформатированный список сообщений.
    """
```

**Назначение**:
Функция `format_conversation` преобразует список сообщений в формат, который соответствует структуре, ожидаемой API ChatGPT. Каждое сообщение преобразуется в словарь с определенными полями, такими как `id`, `author`, `content`, `metadata` и `create_time`.

**Параметры**:
- `messages` (list): Список сообщений, где каждое сообщение представляет собой словарь с ключами `role` и `content`.

**Возвращает**:
- `list`: Отформатированный список сообщений, готовый для отправки в API ChatGPT.

**Как работает функция**:
1. Инициализируется пустой список `conversation` для хранения отформатированных сообщений.
2. Перебирается каждое сообщение в списке `messages`.
3. Для каждого сообщения создается словарь, содержащий:
   - `id`: Уникальный идентификатор сообщения, сгенерированный с помощью `uuid.uuid4()`.
   - `author`: Словарь с ролью автора сообщения, взятой из ключа `role` исходного сообщения.
   - `content`: Словарь с типом контента (`content_type`) и содержимым сообщения, взятым из ключа `content` исходного сообщения.
   - `metadata`: Словарь с метаданными сериализации.
   - `create_time`: Текущее время в формате Unix timestamp с точностью до миллисекунд.
4. Отформатированное сообщение добавляется в список `conversation`.
5. Функция возвращает список `conversation`, содержащий все отформатированные сообщения.

**Примеры**:

```python
messages = [
    {'role': 'user', 'content': 'Hello'},
    {'role': 'assistant', 'content': 'Hi there!'}
]
formatted_messages = format_conversation(messages)
print(formatted_messages)
# Вывод:
# [
#     {'id': '...', 'author': {'role': 'user'}, 'content': {'content_type': 'text', 'parts': ['Hello']}, 'metadata': {'serialization_metadata': {'custom_symbol_offsets': []}}, 'create_time': ...},
#     {'id': '...', 'author': {'role': 'assistant'}, 'content': {'content_type': 'text', 'parts': ['Hi there!']}, 'metadata': {'serialization_metadata': {'custom_symbol_offsets': []}}, 'create_time': ...}
# ]
```

### `init_session`

```python
def init_session(user_agent):
    """Инициализирует сессию requests с необходимыми заголовками и куками.

    Args:
        user_agent (str): User-Agent для сессии.

    Returns:
        Session: Инициализированная сессия requests.
    """
```

**Назначение**:
Функция `init_session` создает и инициализирует сессию `requests.Session` с необходимыми заголовками и куками, чтобы эмулировать поведение браузера при взаимодействии с API ChatGPT.

**Параметры**:
- `user_agent` (str): Строка, представляющая User-Agent браузера.

**Возвращает**:
- `Session`: Инициализированная сессия `requests.Session`.

**Как работает функция**:
1. Создается инстанс `requests.Session`.
2. Определяются куки `_dd_s` (пустая строка).
3. Определяются заголовки, включающие:
   - `accept`: Принимаемые типы контента.
   - `accept-language`: Предпочитаемые языки.
   - `cache-control`: Управление кэшированием.
   - `pragma`: Директивы прагмы.
   - `priority`: Приоритет запроса.
   - `sec-ch-ua`: Информация о браузере.
   - `sec-ch-ua-arch`: Архитектура.
   - `sec-ch-ua-bitness`: Битность.
   - `sec-ch-ua-mobile`: Мобильность.
   - `sec-ch-ua-model`: Модель устройства.
   - `sec-ch-ua-platform`: Платформа.
   - `sec-ch-ua-platform-version`: Версия платформы.
   - `sec-fetch-dest`: Назначение запроса.
   - `sec-fetch-mode`: Режим запроса.
   - `sec-fetch-site`: Сайт запроса.
   - `sec-fetch-user`: Пользовательский запрос.
   - `upgrade-insecure-requests`: Обновление небезопасных запросов.
   - `user-agent`: User-Agent браузера.
4. Выполняется GET-запрос к `https://chatgpt.com/` с использованием определенных кук и заголовков.
5. Возвращается инициализированная сессия.

**Примеры**:

```python
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
session = init_session(user_agent)
print(session)
# Вывод: <requests.sessions.Session object at 0x...>
```