# Модуль Yqcloud
## Обзор
Модуль `Yqcloud` предоставляет реализацию асинхронного генератора для получения ответов от модели `gpt-4` с использованием API-сервиса `yqcloud`. 

## Подробней
Модуль `Yqcloud` реализует класс `Yqcloud`, который наследует классы `AsyncGeneratorProvider` и `ProviderModelMixin`. Это позволяет использовать класс `Yqcloud` для асинхронного получения ответов от модели `gpt-4`, а также  включает поддержку модели `gpt-4`.

## Классы

### `class Yqcloud`

**Описание**:
- Реализует асинхронный генератор для получения ответов от модели `gpt-4` с использованием API-сервиса `yqcloud`.
- Наследует классы `AsyncGeneratorProvider` и `ProviderModelMixin`, которые обеспечивают поддержку асинхронного генератора и работы с моделями.

**Атрибуты**:

- `url`: URL-адрес веб-сайта `yqcloud`.
- `api_endpoint`: URL-адрес API-endpoint `yqcloud`.
- `working`: Флаг, указывающий, доступен ли сервис `yqcloud`.
- `supports_stream`: Флаг, указывающий, поддерживает ли сервис `yqcloud` потоковую передачу ответов.
- `supports_system_message`: Флаг, указывающий, поддерживает ли сервис `yqcloud` системные сообщения.
- `supports_message_history`: Флаг, указывающий, поддерживает ли сервис `yqcloud` историю сообщений.
- `default_model`:  Модель `gpt-4` по умолчанию.
- `models`: Список доступных моделей, в данный момент содержит только модель `gpt-4`.

**Методы**:

- `create_async_generator(model: str, messages: Messages, stream: bool = True, proxy: str = None, conversation: Conversation = None, return_conversation: bool = False, **kwargs) -> AsyncResult`:
    - Метод для создания асинхронного генератора для получения ответов от модели `gpt-4`.
    - Метод выполняет следующий набор действий:
        1. Получает модель `gpt-4` с использованием метода `get_model`.
        2. Собирает заголовки запроса.
        3. Проверяет, была ли передана переменная `conversation` и создает объект `Conversation`, если она не была передана.
        4. Извлекает системное сообщение, если оно было предоставлено.
        5. Форматирует подсказку для отправки модели `gpt-4` с использованием метода `format_prompt`.
        6. Создает запрос к API-endpoint `yqcloud` и отправляет его.
        7. Проверяет статус ответа и выводит ошибки, если они возникают.
        8. Возвращает асинхронный генератор, который позволяет получать ответы от модели `gpt-4` по частям.

**Пример**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.Yqcloud import Yqcloud
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создание экземпляра класса Yqcloud
yqcloud = Yqcloud()

# Подготовка запроса для модели gpt-4
messages: Messages = [
    {"role": "user", "content": "Hello, how are you?"}
]

# Создание асинхронного генератора
async_generator = yqcloud.create_async_generator(model="gpt-4", messages=messages)

# Получение ответа от модели gpt-4 по частям
async for chunk in async_generator:
    print(chunk) 
```
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
```

**Назначение**: 
- Метод создает асинхронный генератор для получения ответов от модели `gpt-4`.
- Генератор позволяет получать ответ по частям, что особенно полезно для обработки больших ответов.

**Параметры**:

- `model` (str):  Название модели, с которой необходимо взаимодействовать.
- `messages` (Messages): Список сообщений для модели `gpt-4`.
- `stream` (bool, optional): Флаг, указывающий, использовать ли потоковую передачу ответов. По умолчанию `True`.
- `proxy` (str, optional): Прокси-сервер для использования при отправке запроса. По умолчанию `None`.
- `conversation` (Conversation, optional):  Объект `Conversation`, который содержит информацию о сессии общения с моделью. По умолчанию `None`.
- `return_conversation` (bool, optional): Флаг, указывающий, возвращать ли обновленный объект `Conversation` после получения ответа. По умолчанию `False`.
- `**kwargs`: Дополнительные параметры, которые могут быть использованы в запросе.

**Возвращает**: 
- `AsyncResult`: Асинхронный генератор, который позволяет получать ответы от модели `gpt-4` по частям.

**Как работает функция**:

1. **Получение модели**: Метод `get_model` используется для получения имени модели.
2. **Создание заголовков**: Создаются заголовки запроса, которые передаются в API-endpoint `yqcloud`.
3. **Инициализация объекта `Conversation`**:  Если объект `Conversation` не был передан в качестве параметра, он создается с использованием текущей модели и списка сообщений.
4. **Форматирование подсказки**:  С использованием метода `format_prompt` формируется подсказка для отправки в API-endpoint `yqcloud`.
5. **Отправка запроса**:  Отправляется запрос к API-endpoint `yqcloud` с использованием библиотеки `aiohttp`.
6. **Обработка ответа**: Проверяется статус ответа. Если ответ успешен, то возвращается асинхронный генератор, который позволяет получать ответ от модели `gpt-4` по частям.
7. **Обновление объекта `Conversation`**:  Если параметр `return_conversation` установлен в `True`, объект `Conversation` обновляется последним сообщением от модели `gpt-4`, а затем возвращается в качестве элемента асинхронного генератора.

**Примеры**:

```python
# Пример 1: Простое общение с моделью gpt-4
async def simple_chat():
    yqcloud = Yqcloud()
    messages = [
        {"role": "user", "content": "Привет!"},
    ]
    async_generator = yqcloud.create_async_generator(model="gpt-4", messages=messages)
    async for chunk in async_generator:
        print(chunk)

# Пример 2: Общение с моделью gpt-4 с использованием объекта Conversation
async def chat_with_conversation():
    yqcloud = Yqcloud()
    conversation = Conversation(model="gpt-4")
    conversation.message_history = [
        {"role": "user", "content": "Какой твой любимый цвет?"},
    ]
    async_generator = yqcloud.create_async_generator(
        model="gpt-4", 
        conversation=conversation, 
        return_conversation=True
    )
    async for chunk in async_generator:
        if isinstance(chunk, Conversation):
            print(f"Conversation history: {chunk.message_history}")
        else:
            print(chunk)
```

## Параметры класса

- `url` (str): URL-адрес веб-сайта `yqcloud`.
- `api_endpoint` (str): URL-адрес API-endpoint `yqcloud`.
- `working` (bool): Флаг, указывающий, доступен ли сервис `yqcloud`.
- `supports_stream` (bool): Флаг, указывающий, поддерживает ли сервис `yqcloud` потоковую передачу ответов.
- `supports_system_message` (bool): Флаг, указывающий, поддерживает ли сервис `yqcloud` системные сообщения.
- `supports_message_history` (bool): Флаг, указывающий, поддерживает ли сервис `yqcloud` историю сообщений.
- `default_model` (str): Модель `gpt-4` по умолчанию.
- `models` (list): Список доступных моделей, в данный момент содержит только модель `gpt-4`.


```markdown