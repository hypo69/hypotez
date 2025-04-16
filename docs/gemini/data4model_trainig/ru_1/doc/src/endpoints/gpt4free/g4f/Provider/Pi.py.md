# Модуль `Pi` для взаимодействия с Pi.ai

## Обзор

Модуль `Pi` предоставляет асинхронный класс `Pi`, который используется для взаимодействия с сервисом Pi.ai. Он поддерживает потоковую передачу данных и использует `nodriver` для выполнения запросов.

## Подробнее

Модуль предназначен для асинхронного взаимодействия с Pi.ai, обеспечивая возможность начать разговор, отправлять сообщения и получать ответы в потоковом режиме. Класс `Pi` использует `StreamSession` для асинхронных HTTP-запросов и управляет cookies и headers для поддержания сессии.

## Классы

### `Pi`

**Описание**: Асинхронный провайдер для взаимодействия с Pi.ai.

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:
- `url` (str): URL для взаимодействия с Pi.ai (`https://pi.ai/talk`).
- `working` (bool): Указывает, работает ли провайдер (всегда `True`).
- `use_nodriver` (bool): Указывает, используется ли `nodriver` (всегда `True`).
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу (всегда `True`).
- `default_model` (str): Модель по умолчанию (`pi`).
- `models` (list[str]): Список поддерживаемых моделей (только `default_model`).
- `_headers` (dict | None): Заголовки HTTP-запросов (инициализируются при первом запросе).
- `_cookies` (Cookies): Cookies для HTTP-запросов (инициализируются при первом запросе).

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для получения ответов от Pi.ai.
- `start_conversation`: Начинает новый разговор с Pi.ai.
- `get_chat_history`: Получает историю чата.
- `ask`: Отправляет запрос в Pi.ai и возвращает ответ в потоковом режиме.

## Методы класса

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    stream: bool,
    proxy: str = None,
    timeout: int = 180,
    conversation_id: str = None,
    **kwargs
) -> AsyncResult:
    """Создает асинхронный генератор для получения ответов от Pi.ai.

    Args:
        model (str): Модель для использования (всегда `pi`).
        messages (Messages): Список сообщений для отправки.
        stream (bool): Указывает, использовать ли потоковую передачу.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        timeout (int, optional): Время ожидания запроса в секундах. По умолчанию 180.
        conversation_id (str, optional): ID существующего разговора. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий ответы от Pi.ai.

    Как работает функция:
    - Если заголовки (`cls._headers`) не инициализированы, функция получает их и cookies, используя `get_args_from_nodriver`.
    - Использует `StreamSession` для асинхронных HTTP-запросов.
    - Если `conversation_id` не предоставлен, начинает новый разговор, вызывая `start_conversation`.
    - Форматирует prompt, используя `format_prompt`.
    - Вызывает `ask` для получения ответа от Pi.ai.
    - Итерируется по ответу и выдает текст каждой строки, содержащей "text".
    """
    ...
```

**Примеры**:

```python
# Пример использования create_async_generator
messages = [{"role": "user", "content": "Hello, Pi!"}]
async for response in Pi.create_async_generator(model="pi", messages=messages, stream=True):
    print(response)
```

### `start_conversation`

```python
@classmethod
async def start_conversation(cls, session: StreamSession) -> str:
    """Начинает новый разговор с Pi.ai.

    Args:
        session (StreamSession): Асинхронная HTTP-сессия.

    Returns:
        str: ID нового разговора.

    Raises:
        Exception: В случае ошибки при выполнении запроса.

    Как работает функция:
    - Выполняет POST-запрос к `https://pi.ai/api/chat/start` для начала нового разговора.
    - Извлекает `conversation_id` (sid) из ответа JSON.
    """
    ...
```

**Примеры**:

```python
# Пример использования start_conversation
async with StreamSession() as session:
    conversation_id = await Pi.start_conversation(session)
    print(f"Conversation ID: {conversation_id}")
```

### `get_chat_history`

```python
async def get_chat_history(session: StreamSession, conversation_id: str):
    """Получает историю чата.

    Args:
        session (StreamSession): Асинхронная HTTP-сессия.
        conversation_id (str): ID разговора.

    Returns:
        dict: История чата в формате JSON.

    Raises:
        Exception: В случае ошибки при выполнении запроса.

    Как работает функция:
    - Выполняет GET-запрос к `https://pi.ai/api/chat/history` с параметром `conversation_id`.
    - Возвращает историю чата в формате JSON.
    """
    ...
```

**Примеры**:

```python
# Пример использования get_chat_history
async with StreamSession() as session:
    conversation_id = "some_conversation_id"
    history = await Pi.get_chat_history(session, conversation_id)
    print(history)
```

### `ask`

```python
@classmethod
async def ask(cls, session: StreamSession, prompt: str, conversation_id: str):
    """Отправляет запрос в Pi.ai и возвращает ответ в потоковом режиме.

    Args:
        session (StreamSession): Асинхронная HTTP-сессия.
        prompt (str): Текст запроса.
        conversation_id (str): ID разговора.

    Yields:
        str: Части ответа от Pi.ai.

    Raises:
        Exception: В случае ошибки при выполнении запроса.

    Как работает функция:
    - Формирует JSON-данные для отправки, включая текст запроса, `conversation_id` и режим.
    - Выполняет POST-запрос к `https://pi.ai/api/chat` с JSON-данными.
    - Обновляет cookies из ответа.
    - Итерируется по строкам ответа и выдает JSON, если строка начинается с `data: {"text":` или `data: {"title":`.
    """
    ...
```

**Примеры**:

```python
# Пример использования ask
async with StreamSession() as session:
    conversation_id = "some_conversation_id"
    prompt = "Tell me a joke."
    async for line in Pi.ask(session, prompt, conversation_id):
        print(line)
```