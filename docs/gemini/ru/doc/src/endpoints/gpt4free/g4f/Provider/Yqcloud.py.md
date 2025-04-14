# Модуль `Yqcloud.py`

## Обзор

Модуль предоставляет класс `Yqcloud`, который является асинхронным провайдером для взаимодействия с API `chat9.yqcloud.top`. Он поддерживает потоковую передачу данных и предназначен для обмена сообщениями с использованием моделей, таких как `gpt-4`.

## Подробнее

Этот модуль обеспечивает возможность асинхронного взаимодействия с API `Yqcloud` для генерации текста. Он включает поддержку системных сообщений и истории сообщений, что позволяет вести контекстные диалоги. Модуль использует `aiohttp` для выполнения асинхронных HTTP-запросов и предоставляет функциональность для форматирования запросов и обработки ответов.

## Классы

### `Conversation`

**Описание**: Класс `Conversation` представляет собой структуру для хранения истории сообщений и идентификатора пользователя в рамках диалога с `Yqcloud`.

**Наследует**: `JsonConversation`

**Атрибуты**:
- `userId` (str): Уникальный идентификатор пользователя.
- `message_history` (Messages): Список сообщений в истории диалога.
- `model` (str): Модель, используемая для диалога.

**Методы**:

#### `__init__`

```python
def __init__(self, model: str):
    """Инициализирует объект Conversation.

    Args:
        model (str): Модель, используемая для диалога.
    """
    ...
```

### `Yqcloud`

**Описание**: Класс `Yqcloud` предоставляет функциональность для взаимодействия с API `chat9.yqcloud.top`. Он поддерживает асинхронную генерацию текста с использованием потоковой передачи данных.

**Наследует**: `AsyncGeneratorProvider`, `ProviderModelMixin`

**Атрибуты**:
- `url` (str): Базовый URL для `chat9.yqcloud.top`.
- `api_endpoint` (str): URL для API-endpoint генерации текста.
- `working` (bool): Флаг, указывающий, работает ли провайдер.
- `supports_stream` (bool): Флаг, указывающий, поддерживает ли провайдер потоковую передачу данных.
- `supports_system_message` (bool): Флаг, указывающий, поддерживает ли провайдер системные сообщения.
- `supports_message_history` (bool): Флаг, указывающий, поддерживает ли провайдер историю сообщений.
- `default_model` (str): Модель, используемая по умолчанию ("gpt-4").
- `models` (list): Список поддерживаемых моделей.

**Методы**:

#### `create_async_generator`

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
    """Создает асинхронный генератор для взаимодействия с API Yqcloud.

    Args:
        model (str): Модель для использования.
        messages (Messages): Список сообщений для отправки.
        stream (bool, optional): Флаг, указывающий, использовать ли потоковую передачу данных. По умолчанию True.
        proxy (str, optional): URL прокси-сервера. По умолчанию None.
        conversation (Conversation, optional): Объект Conversation для хранения истории диалога. По умолчанию None.
        return_conversation (bool, optional): Флаг, указывающий, возвращать ли объект Conversation после завершения. По умолчанию False.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий сообщения от API.
    """
    ...
```

## Методы класса

### `create_async_generator`

**Назначение**:
Создает асинхронный генератор для взаимодействия с API `Yqcloud`. Этот метод отвечает за подготовку и отправку запроса к API, а также за обработку потоковых ответов.

**Параметры**:

- `model` (str): Модель, используемая для генерации текста.
- `messages` (Messages): Список сообщений, отправляемых в API.
- `stream` (bool, optional): Указывает, использовать ли потоковую передачу данных. По умолчанию `True`.
- `proxy` (str, optional): URL прокси-сервера для использования. По умолчанию `None`.
- `conversation` (Conversation, optional): Объект `Conversation` для хранения истории сообщений. Если не указан, создается новый. По умолчанию `None`.
- `return_conversation` (bool, optional): Указывает, возвращать ли объект `Conversation` после завершения. По умолчанию `False`.
- `**kwargs`: Дополнительные параметры, передаваемые в API.

**Возвращает**:

- `AsyncResult`: Асинхронный генератор, возвращающий сообщения от API.

**Как работает функция**:

1. **Подготовка параметров**:
   - Извлекает модель, приводя ее к поддерживаемому формату с помощью `cls.get_model(model)`.
   - Формирует заголовки запроса, включая `accept`, `accept-language`, `content-type`, `origin`, `referer` и `user-agent`.
   - Если объект `conversation` не предоставлен, создает новый экземпляр класса `Conversation` и инициализирует его историей сообщений из параметра `messages`. В противном случае добавляет последнее сообщение из `messages` в существующую историю.

2. **Обработка системного сообщения**:
   - Извлекает системное сообщение из начала списка сообщений, если оно присутствует. Системное сообщение используется для установки контекста для модели.

3. **Формирование запроса**:
   - Форматирует список сообщений с помощью функции `format_prompt(current_messages)`.
   - Создает словарь `data`, содержащий параметры запроса: `prompt` (отформатированное сообщение), `userId` (идентификатор пользователя из объекта `conversation`), `network`, `system` (системное сообщение), `withoutContext` и `stream`.

4. **Отправка запроса и обработка ответа**:
   - Использует `aiohttp.ClientSession` для отправки асинхронного POST-запроса к `cls.api_endpoint` с использованием подготовленных заголовков, данных и прокси (если указан).
   - Вызывает `raise_for_status(response)` для проверки статуса ответа и выбрасывает исключение в случае ошибки.
   - Итерируется по чанкам в ответе, декодирует каждый чанк и передает его через генератор.

5. **Обработка завершения**:
   - После получения всех чанков добавляет сгенерированное сообщение от ассистента в историю сообщений объекта `conversation`, если `return_conversation` имеет значение `True`.
   - Передает объект `conversation` через генератор, если `return_conversation` имеет значение `True`.
   - Завершает генератор, передавая `FinishReason("stop")`.

**Примеры**:

```python
# Пример вызова create_async_generator с минимальными параметрами
async for message in Yqcloud.create_async_generator(model="gpt-4", messages=[{"role": "user", "content": "Hello"}]):
    print(message)

# Пример вызова create_async_generator с использованием прокси и возвратом conversation
conversation = None
async for message in Yqcloud.create_async_generator(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello"}],
    proxy="http://proxy.example.com",
    return_conversation=True,
    conversation=conversation
):
    if isinstance(message, Conversation):
        conversation = message
    else:
        print(message)