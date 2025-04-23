# Модуль `Yqcloud`

## Обзор

Модуль `Yqcloud` предоставляет асинхронтный генератор для взаимодействия с API `api.binjie.fun` через провайдера `chat9.yqcloud.top`. Этот модуль предназначен для получения ответов в режиме потока (stream) и поддерживает системные сообщения и историю сообщений.

## Подробней

Модуль использует `aiohttp` для асинхронных запросов и предоставляет класс `Yqcloud`, который наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`. Он конфигурирует заголовки запросов, формирует полезную нагрузку (payload) и обрабатывает ответы, возвращая их в виде асинхронного генератора.

## Классы

### `Conversation`

**Описание**: Класс `Conversation` предназначен для хранения истории сообщений и идентификатора пользователя в рамках одного диалога с API.

**Наследует**: `JsonConversation`

**Атрибуты**:

-   `userId` (str): Уникальный идентификатор пользователя для данного диалога. По умолчанию `None`.
-   `message_history` (Messages): Список сообщений, составляющих историю диалога. По умолчанию пустой список `[]`.
-   `model` (str): Модель, используемая в разговоре.

**Методы**:

-   `__init__(self, model: str)`:
    *   **Назначение**: Инициализирует новый экземпляр класса `Conversation`.
    *   **Параметры**:
        *   `model` (str): Модель, используемая в разговоре.
    *   **Как работает функция**:
        *   Устанавливает атрибут `model` экземпляра класса.
        *   Генерирует уникальный `userId` на основе текущего времени и присваивает его атрибуту `userId`.

### `Yqcloud`

**Описание**: Класс `Yqcloud` предоставляет интерфейс для взаимодействия с API `api.binjie.fun` через провайдера `chat9.yqcloud.top`. Он поддерживает потоковую передачу ответов, системные сообщения и историю сообщений.

**Наследует**: `AsyncGeneratorProvider`, `ProviderModelMixin`

**Атрибуты**:

-   `url` (str): URL провайдера. Значение: `"https://chat9.yqcloud.top"`.
-   `api_endpoint` (str): URL API для генерации потока. Значение: `"https://api.binjie.fun/api/generateStream"`.
-   `working` (bool): Указывает, работает ли провайдер. Значение: `True`.
-   `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу. Значение: `True`.
-   `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения. Значение: `True`.
-   `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений. Значение: `True`.
-   `default_model` (str): Модель, используемая по умолчанию. Значение: `"gpt-4"`.
-   `models` (list[str]): Список поддерживаемых моделей. Значение: `[default_model]`.

## Методы класса

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
```

**Назначение**: Создает асинхронный генератор для получения ответов от API.

**Параметры**:

-   `model` (str): Модель для использования.
-   `messages` (Messages): Список сообщений для отправки.
-   `stream` (bool, optional): Определяет, использовать ли потоковую передачу. По умолчанию `True`.
-   `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
-   `conversation` (Conversation, optional): Объект `Conversation` для поддержания истории. По умолчанию `None`.
-   `return_conversation` (bool, optional): Возвращать ли объект `Conversation` в конце генерации. По умолчанию `False`.
-   `**kwargs`: Дополнительные параметры.

**Возвращает**:

-   `AsyncResult`: Асинхронный генератор, возвращающий части ответа от API.

**Вызывает исключения**:

-   `Exception`: Если возникает ошибка при выполнении запроса к API.

**Как работает функция**:

1.  Извлекает модель, используя `cls.get_model(model)`.
2.  Определяет заголовки запроса, включая `content-type`, `origin`, `referer` и `user-agent`.
3.  Если объект `conversation` не предоставлен, создает новый экземпляр класса `Conversation` и устанавливает историю сообщений.
4.  Если `conversation` предоставлен, добавляет последнее сообщение в историю.
5.  Извлекает системное сообщение, если оно присутствует в начале списка сообщений.
6.  Формирует `prompt` для отправки в API.
7.  Создает `data` (полезную нагрузку) для отправки в API, включающую `prompt`, `userId`, `network`, `system`, `withoutContext` и `stream`.
8.  Отправляет POST-запрос к `cls.api_endpoint` с использованием `aiohttp.ClientSession`.
9.  Обрабатывает ответ от API в асинхронном режиме, декодирует каждый чанк и возвращает его через генератор.
10. Если `return_conversation` равен `True`, добавляет ответ ассистента в историю сообщений и возвращает объект `Conversation` в конце генерации.
11. В конце возвращает `FinishReason("stop")`.

**Примеры**:

```python
# Пример использования create_async_generator
messages = [{"role": "user", "content": "Hello, how are you?"}]
async for message in Yqcloud.create_async_generator(model="gpt-4", messages=messages):
    print(message)