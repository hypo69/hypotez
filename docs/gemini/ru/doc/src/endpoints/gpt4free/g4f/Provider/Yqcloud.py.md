# Модуль для работы с Yqcloud
==========================

Модуль предоставляет асинхронный генератор для взаимодействия с сервисом Yqcloud, используя его API для генерации текста.

## Обзор

Модуль содержит класс `Yqcloud`, который наследует `AsyncGeneratorProvider` и `ProviderModelMixin`.
Он предназначен для асинхронного взаимодействия с API Yqcloud для генерации текста на основе предоставленных сообщений.
Класс поддерживает потоковую передачу данных, системные сообщения и историю сообщений.

## Подробнее

Этот модуль является частью проекта `hypotez` и предназначен для обеспечения возможности взаимодействия с Yqcloud в рамках задач генерации текста.
Он использует `aiohttp` для выполнения асинхронных HTTP-запросов и предоставляет удобный интерфейс для отправки запросов и получения ответов от API Yqcloud.

## Классы

### `Conversation`

**Описание**: Класс, представляющий собой структуру для хранения истории разговоров с моделью.

**Наследует**: `JsonConversation`

**Атрибуты**:
- `userId` (str): Уникальный идентификатор пользователя.
- `message_history` (Messages): Список сообщений в истории разговора.
- `model` (str): Модель, используемая в разговоре.

**Методы**:
- `__init__(self, model: str)`: Инициализирует объект `Conversation` с указанной моделью и генерирует уникальный `userId`.

### `Yqcloud`

**Описание**: Класс, предоставляющий интерфейс для взаимодействия с API Yqcloud.

**Наследует**: `AsyncGeneratorProvider`, `ProviderModelMixin`

**Атрибуты**:
- `url` (str): Базовый URL сервиса Yqcloud.
- `api_endpoint` (str): URL API для генерации текста.
- `working` (bool): Флаг, указывающий, работает ли провайдер.
- `supports_stream` (bool): Флаг, указывающий, поддерживает ли провайдер потоковую передачу данных.
- `supports_system_message` (bool): Флаг, указывающий, поддерживает ли провайдер системные сообщения.
- `supports_message_history` (bool): Флаг, указывающий, поддерживает ли провайдер историю сообщений.
- `default_model` (str): Модель, используемая по умолчанию.
- `models` (List[str]) : Список поддерживаемых моделей.

**Методы**:
- `create_async_generator(model: str, messages: Messages, stream: bool = True, proxy: str = None, conversation: Conversation = None, return_conversation: bool = False, **kwargs) -> AsyncResult`:
   Создает асинхронный генератор для получения ответов от API Yqcloud.

## Функции

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    stream: bool = True,
    proxy: str = None,
    conversation: Conversation = None,
    return_conversation: bool = False,
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для получения ответов от API Yqcloud.

    Args:
        model (str): Модель для генерации текста.
        messages (Messages): Список сообщений для отправки в API.
        stream (bool): Флаг, указывающий, использовать ли потоковую передачу данных. По умолчанию `True`.
        proxy (str): URL прокси-сервера для использования. По умолчанию `None`.
        conversation (Conversation): Объект `Conversation` для хранения истории разговора. По умолчанию `None`.
        return_conversation (bool): Флаг, указывающий, возвращать ли объект `Conversation` в конце генерации. По умолчанию `False`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий ответы от API.

    Как работает функция:
    1. Получает модель, используя `cls.get_model(model)`.
    2. Формирует заголовки запроса, включая `origin`, `referer` и `user-agent`.
    3. Если `conversation` не предоставлен, создает новый объект `Conversation` с указанной моделью и сохраняет историю сообщений.
    4. Извлекает системное сообщение из истории сообщений, если оно присутствует.
    5. Формирует данные для отправки в API, включая `prompt`, `userId`, `network`, `system`, `withoutContext` и `stream`.
    6. Отправляет POST-запрос к API Yqcloud с использованием `aiohttp.ClientSession`.
    7. Обрабатывает ответ от API, декодирует чанки и возвращает их через генератор.
    8. Если `return_conversation` установлен в `True`, добавляет ответ ассистента в историю разговора и возвращает объект `Conversation`.
    9. Возвращает признак завершения `"stop"`.

    Внутренние функции: Нет

    ASCII flowchart:
    Начало --> Получение модели
    Получение модели --> Формирование заголовков
    Формирование заголовков --> Создание/обновление conversation
    Создание/обновление conversation --> Извлечение системного сообщения
    Извлечение системного сообщения --> Формирование данных запроса
    Формирование данных запроса --> Отправка POST-запроса
    Отправка POST-запроса --> Обработка ответа API
    Обработка ответа API --> Возврат чанков через генератор
    Обработка ответа API --> (return_conversation=True) Добавление ответа в историю и возврат conversation
    Обработка ответа API --> Возврат FinishReason("stop")
    """
    model = cls.get_model(model)
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "origin": f"{cls.url}",
        "referer": f"{cls.url}/",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }

    if conversation is None:
        conversation = Conversation(model)
        conversation.message_history = messages
    else:
        conversation.message_history.append(messages[-1])

    # Extract system message if present
    system_message = ""
    current_messages = conversation.message_history
    if current_messages and current_messages[0]["role"] == "system":
        system_message = current_messages[0]["content"]
        current_messages = current_messages[1:]

    async with ClientSession(headers=headers) as session:
        prompt = format_prompt(current_messages)
        data = {
            "prompt": prompt,
            "userId": conversation.userId,
            "network": True,
            "system": system_message,
            "withoutContext": False,
            "stream": stream
        }

        async with session.post(cls.api_endpoint, json=data, proxy=proxy) as response:
            await raise_for_status(response)
            full_message = ""
            async for chunk in response.content:
                if chunk:
                    message = chunk.decode()
                    yield message
                    full_message += message

            if return_conversation:
                conversation.message_history.append({"role": "assistant", "content": full_message})
                yield conversation

            yield FinishReason("stop")
```

**Примеры**:

```python
# Пример вызова функции create_async_generator
messages = [{"role": "user", "content": "Hello, how are you?"}]
async def main():
    async for message in Yqcloud.create_async_generator(model="gpt-4", messages=messages):
        print(message)

# Пример вызова с использованием прокси
messages = [{"role": "user", "content": "Привет, как дела?"}]
async def main():
    async for message in Yqcloud.create_async_generator(model="gpt-4", messages=messages, proxy="http://your-proxy:8080"):
        print(message)