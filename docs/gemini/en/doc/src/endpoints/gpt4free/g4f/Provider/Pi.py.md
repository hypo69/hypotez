# Модуль `Pi`

## Обзор

Модуль `Pi` представляет собой асинхронный провайдер для взаимодействия с сервисом `pi.ai`. Он позволяет вести диалог с использованием API `pi.ai`, поддерживая потоковую передачу данных и асинхронные запросы. Модуль использует `StreamSession` для эффективного управления HTTP-сессиями и обработки потоковых ответов.

## Более подробно

Модуль `Pi` предназначен для интеграции с `pi.ai` через его API. Он предоставляет функциональность для начала разговора, отправки запросов и получения ответов в режиме реального времени. В модуле реализована поддержка управления cookies и заголовками, а также обработка ошибок при взаимодействии с API.

## Классы

### `Pi`

**Описание**: Асинхронный провайдер для взаимодействия с `pi.ai`.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.

**Атрибуты**:
- `url` (str): URL для взаимодействия с `pi.ai` (`https://pi.ai/talk`).
- `working` (bool): Указывает, работает ли провайдер (`True`).
- `use_nodriver` (bool): Указывает, использовать ли бездрайверный режим (`True`).
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу данных (`True`).
- `default_model` (str): Модель, используемая по умолчанию (`pi`).
- `models` (List[str]): Список поддерживаемых моделей (`[default_model]`).
- `_headers` (dict): Заголовки HTTP-запросов.
- `_cookies` (Cookies): Cookies для HTTP-запросов.

**Принцип работы**:
Класс `Pi` использует асинхронные запросы для взаимодействия с API `pi.ai`. Он поддерживает начало разговора, отправку сообщений и получение ответов в потоковом режиме. Для управления сессиями используется `StreamSession`, что позволяет эффективно обрабатывать потоковые данные. Класс также обеспечивает управление cookies и заголовками для поддержания сессии с сервером.

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
    """
    Создает асинхронный генератор для получения ответов от `pi.ai`.

    Args:
        model (str): Модель для использования (в данном случае всегда "pi").
        messages (Messages): Список сообщений для отправки.
        stream (bool): Указывает, использовать ли потоковый режим.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        timeout (int, optional): Время ожидания запроса в секундах. По умолчанию 180.
        conversation_id (str, optional): Идентификатор существующего разговора. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий ответы от `pi.ai`.

    Как работает:
        Если заголовки не инициализированы, функция извлекает их и cookies из `pi.ai` с использованием `get_args_from_nodriver`.
        Затем, используя `StreamSession`, отправляет запросы к `pi.ai` для получения ответов.
        Если `conversation_id` не предоставлен, начинается новый разговор с использованием `start_conversation`.
        После этого отправляется запрос с сообщением пользователя (`prompt`) и асинхронно обрабатываются ответы, извлекая текст из каждой строки ответа.
    """
    ...
```

**Параметры**:
- `model` (str): Модель для использования (в данном случае всегда "pi").
- `messages` (Messages): Список сообщений для отправки.
- `stream` (bool): Указывает, использовать ли потоковый режим.
- `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
- `timeout` (int, optional): Время ожидания запроса в секундах. По умолчанию 180.
- `conversation_id` (str, optional): Идентификатор существующего разговора. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Примеры**:

```python
# Пример использования create_async_generator
messages = [{"role": "user", "content": "Привет, как дела?"}]
async for response in Pi.create_async_generator(model="pi", messages=messages, stream=True):
    print(response)
```

### `start_conversation`

```python
@classmethod
async def start_conversation(cls, session: StreamSession) -> str:
    """
    Начинает новый разговор с `pi.ai` и возвращает идентификатор разговора.

    Args:
        session (StreamSession): Асинхронная HTTP-сессия.

    Returns:
        str: Идентификатор нового разговора.
    """
    ...
```

**Параметры**:
- `session` (StreamSession): Асинхронная HTTP-сессия.

**Примеры**:

```python
# Пример использования start_conversation
import asyncio
from src.requests import StreamSession

async def main():
    async with StreamSession() as session:
        conversation_id = await Pi.start_conversation(session)
        print(f"ID разговора: {conversation_id}")

if __name__ == "__main__":
    asyncio.run(main())
```

### `get_chat_history`

```python
async def get_chat_history(session: StreamSession, conversation_id: str):
    """
    Получает историю чата по идентификатору разговора.

    Args:
        session (StreamSession): Асинхронная HTTP-сессия.
        conversation_id (str): Идентификатор разговора.

    Returns:
        json: Возвращает историю сообщений.
    """
    ...
```

**Параметры**:
- `session` (StreamSession): Асинхронная HTTP-сессия.
- `conversation_id` (str): Идентификатор разговора.

**Примеры**:

```python
# Пример использования get_chat_history
import asyncio
from src.requests import StreamSession

async def main():
    async with StreamSession() as session:
        conversation_id = "some_conversation_id"  # Укажите существующий ID разговора
        history = await Pi.get_chat_history(session, conversation_id)
        print(f"История чата: {history}")

if __name__ == "__main__":
    asyncio.run(main())
```

### `ask`

```python
@classmethod
async def ask(cls, session: StreamSession, prompt: str, conversation_id: str):
    """
    Отправляет запрос к `pi.ai` и возвращает ответ.

    Args:
        session (StreamSession): Асинхронная HTTP-сессия.
        prompt (str): Текст запроса.
        conversation_id (str): Идентификатор разговора.

    Yields:
        str: Части ответа от `pi.ai`.
    """
    ...
```

**Параметры**:
- `session` (StreamSession): Асинхронная HTTP-сессия.
- `prompt` (str): Текст запроса.
- `conversation_id` (str): Идентификатор разговора.

**Примеры**:

```python
# Пример использования ask
import asyncio
from src.requests import StreamSession

async def main():
    async with StreamSession() as session:
        conversation_id = "some_conversation_id"  # Укажите существующий ID разговора
        prompt = "Как дела?"
        async for line in Pi.ask(session, prompt, conversation_id):
            print(line)

if __name__ == "__main__":
    asyncio.run(main())
```