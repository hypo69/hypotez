# Модуль Pi

## Обзор

Этот модуль предоставляет класс `Pi`, который реализует асинхронный генератор для взаимодействия с API сервиса Pi.ai.  Он реализует интерфейс `AsyncGeneratorProvider` и обеспечивает функциональность для отправки запросов, получения ответов и поддержания контекста диалога.

## Подробности

Класс `Pi` использует HTTP-запросы для взаимодействия с API Pi.ai, используя метод `StreamSession` для потоковой передачи ответов. Он поддерживает асинхронные операции, позволяя вызывать API-запросы и обрабатывать результаты без блокировки основного потока.

## Классы

### `class Pi`

**Описание**: Класс `Pi` реализует асинхронный генератор для взаимодействия с API сервиса Pi.ai.

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:

- `url (str)`: Базовый URL API Pi.ai.
- `working (bool)`: Указывает, доступен ли сервис.
- `use_nodriver (bool)`: Указывает, используется ли драйвер браузера.
- `supports_stream (bool)`: Указывает, поддерживает ли API потоковую передачу.
- `default_model (str)`: Имя модели по умолчанию.
- `models (list)`: Список доступных моделей.
- `_headers (dict)`: Заголовки HTTP-запросов.
- `_cookies (Cookies)`: Cookies для сессии.

**Методы**:

- `create_async_generator()`: Асинхронный генератор для отправки запросов и получения ответов.
- `start_conversation()`: Метод для начала нового диалога.
- `get_chat_history()`: Метод для получения истории диалога.
- `ask()`: Метод для отправки запросов в API Pi.ai.

#### `create_async_generator(model: str, messages: Messages, stream: bool, proxy: str = None, timeout: int = 180, conversation_id: str = None, **kwargs) -> AsyncResult`

**Назначение**: Асинхронный генератор для отправки запросов и получения ответов.

**Параметры**:

- `model (str)`: Имя модели.
- `messages (Messages)`: Список сообщений в диалоге.
- `stream (bool)`: Флаг, указывающий на потоковую передачу.
- `proxy (str, optional)`: Прокси-сервер. По умолчанию `None`.
- `timeout (int, optional)`: Время ожидания ответа. По умолчанию 180 секунд.
- `conversation_id (str, optional)`: ID диалога. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:

- `AsyncResult`: Асинхронный результат, который может быть использован для получения ответов.

**Как работает**:

- Метод `create_async_generator` реализует генератор, который асинхронно отправляет запросы к API Pi.ai и возвращает ответы по одному слову.
- Он использует метод `ask` для отправки запросов и метод `start_conversation` для создания нового диалога.
- Метод использует `StreamSession` для потоковой передачи ответов и обработки запросов.
- Он использует метод `merge_cookies` для обновления cookies после каждого запроса.

#### `start_conversation(session: StreamSession) -> str`

**Назначение**: Метод для начала нового диалога.

**Параметры**:

- `session (StreamSession)`: Сессия HTTP-запросов.

**Возвращает**:

- `str`: ID нового диалога.

**Как работает**:

- Метод отправляет POST-запрос к API Pi.ai для начала нового диалога.
- Он обрабатывает ответ, извлекает ID диалога и возвращает его.

#### `get_chat_history(session: StreamSession, conversation_id: str)`

**Назначение**: Метод для получения истории диалога.

**Параметры**:

- `session (StreamSession)`: Сессия HTTP-запросов.
- `conversation_id (str)`: ID диалога.

**Возвращает**:

- `json`: История диалога в формате JSON.

**Как работает**:

- Метод отправляет GET-запрос к API Pi.ai для получения истории диалога по указанному ID.
- Он обрабатывает ответ и возвращает его в формате JSON.

#### `ask(session: StreamSession, prompt: str, conversation_id: str)`

**Назначение**: Метод для отправки запросов в API Pi.ai.

**Параметры**:

- `session (StreamSession)`: Сессия HTTP-запросов.
- `prompt (str)`: Текст запроса.
- `conversation_id (str)`: ID диалога.

**Возвращает**:

- `generator`: Генератор, который возвращает части ответа по мере их поступления.

**Как работает**:

- Метод отправляет POST-запрос к API Pi.ai с текстом запроса и ID диалога.
- Он обрабатывает ответ, извлекает части ответа и возвращает их через генератор.

## Примеры

```python
from src.endpoints.gpt4free.g4f.Provider.Pi import Pi

# Создание нового диалога с моделью 'pi'
async with Pi.create_async_generator(model='pi', messages=[], stream=True) as generator:
    # Отправка запроса
    await generator.asend('Привет!')

    # Получение ответа
    async for line in generator:
        print(line)

# Получение истории диалога
async with Pi.create_async_generator(model='pi', messages=[], stream=True) as generator:
    conversation_id = await generator.start_conversation()
    history = await Pi.get_chat_history(generator.session, conversation_id)
    print(history)