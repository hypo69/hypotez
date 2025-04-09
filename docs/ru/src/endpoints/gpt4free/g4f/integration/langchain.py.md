# Модуль интеграции g4f с Langchain

## Обзор

Модуль предназначен для интеграции библиотеки `g4f` (GPT4Free) с фреймворком `Langchain`. Он предоставляет возможность использовать модели `g4f` в качестве чат-моделей `Langchain`, обеспечивая совместимость и расширяя функциональность обеих библиотек. Модуль содержит переопределение стандартной функции преобразования сообщений `Langchain` и класс `ChatAI`, который наследуется от `ChatOpenAI` и адаптирован для работы с `g4f`.

## Подробнее

Модуль позволяет использовать модели, предоставляемые `g4f`, в качестве компонентов `Langchain`, что расширяет возможности для создания чат-ботов и других приложений, использующих обработку естественного языка. Он изменяет способ преобразования сообщений, чтобы корректно обрабатывать сообщения, специфичные для `g4f`, и предоставляет класс `ChatAI` для удобной интеграции с `Langchain`.

## Функции

### `new_convert_message_to_dict`

```python
def new_convert_message_to_dict(message: BaseMessage) -> dict:
    """ Функция преобразует объект сообщения (BaseMessage) в словарь, пригодный для использования в Langchain.

    Args:
        message (BaseMessage): Объект сообщения, который необходимо преобразовать.

    Returns:
        dict: Словарь, представляющий сообщение.

    Как работает функция:
    1. Проверяет, является ли сообщение экземпляром класса `ChatCompletionMessage`.
    2. Если да, создает словарь с ключами "role" (роль) и "content" (содержимое) из атрибутов сообщения.
    3. Если в сообщении есть `tool_calls`, добавляет информацию о них в словарь.
    4. Если содержимое сообщения пустое, устанавливает значение `content` в `None`.
    5. Если сообщение не является экземпляром `ChatCompletionMessage`, использует стандартную функцию `convert_message_to_dict` для преобразования.

    ASCII схема работы функции:
    A (Получение сообщения)
    ↓
    B (Проверка типа сообщения: ChatCompletionMessage?)
    ├── Да → C (Создание словаря с информацией о роли, содержимом и tool_calls (если есть))
    │       ↓
    │       D (Если содержимое пустое, установить content = None)
    └── Нет → E (Использовать стандартную функцию convert_message_to_dict)
    ↓
    F (Возврат словаря)

    Примеры:
    1. Преобразование `ChatCompletionMessage` без `tool_calls`:
        >>> from langchain_community.messages import BaseMessage, HumanMessage
        >>> message = HumanMessage(content="Привет")
        >>> new_convert_message_to_dict(message)
        {'content': 'Привет', 'additional_kwargs': {}, 'type': 'human'}

    2. Преобразование `ChatCompletionMessage` с `tool_calls`:
        >>> from g4f.client.stubs import ChatCompletionMessage, ToolCall, Function
        >>> function = Function(name="get_current_weather", description="Get the current weather in a given location", parameters={"type": "object", "properties": {"location": {"type": "string", "description": "The city and state, e.g. San Francisco, CA"}, "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}}})
        >>> tool_call = ToolCall(id="call_123", type="function", function=function)
        >>> message = ChatCompletionMessage(content="Вызов функции", role="assistant", tool_calls=[tool_call])
        >>> new_convert_message_to_dict(message)
        {'role': 'assistant', 'content': 'Вызов функции', 'tool_calls': [{'id': 'call_123', 'type': 'function', 'function': {'name': 'get_current_weather', 'description': 'Get the current weather in a given location', 'parameters': {'type': 'object', 'properties': {'location': {'type': 'string', 'description': 'The city and state, e.g. San Francisco, CA'}, 'unit': {'type': 'string', 'enum': ['celsius', 'fahrenheit']}}}}}]}

    """
    message_dict: Dict[str, Any]
    if isinstance(message, ChatCompletionMessage):
        message_dict = {"role": message.role, "content": message.content}
        if message.tool_calls is not None:
            message_dict["tool_calls"] = [{
                "id": tool_call.id,
                "type": tool_call.type,
                "function": tool_call.function
            } for tool_call in message.tool_calls]
            if message_dict["content"] == "":
                message_dict["content"] = None
    else:
        message_dict = convert_message_to_dict(message)
    return message_dict
```

## Классы

### `ChatAI`

**Описание**: Класс `ChatAI` представляет собой интеграцию чат-модели `g4f` с `Langchain`.

**Наследует**: `ChatOpenAI`

**Атрибуты**:
- `model_name` (str): Название модели, по умолчанию "gpt-4o".

**Методы**:
- `validate_environment`: Проверяет окружение и устанавливает параметры клиента для `g4f`.

### `ChatAI.validate_environment`

```python
    @classmethod
    def validate_environment(cls, values: dict) -> dict:
        """ Проверяет окружение и устанавливает параметры клиента для `g4f`.

        Args:
            values (dict): Словарь с параметрами конфигурации.

        Returns:
            dict: Обновленный словарь с параметрами, включающий настроенные клиенты `g4f`.

        Как работает функция:
        1. Извлекает параметры `api_key` и `provider` из словаря `values`.
        2. Создает параметры для клиентов `g4f`.
        3. Создает экземпляры `Client` и `AsyncClient` с переданными параметрами.
        4. Присваивает созданные клиенты ключам "client" и "async_client" в словаре `values`.

        ASCII схема работы функции:
        A (Получение словаря значений)
        ↓
        B (Извлечение api_key и provider)
        ↓
        C (Создание параметров клиента)
        ↓
        D (Создание Client и AsyncClient)
        ↓
        E (Добавление клиентов в словарь values)
        ↓
        F (Возврат обновленного словаря)

        Примеры:
        1. Использование с указанием `api_key` и `provider`:
            >>> ChatAI.validate_environment({"api_key": "test_key", "model_kwargs": {"provider": "g4f.models.Model.You"}} )
            {'model_name': 'gpt-4o', 'model': 'gpt-4o', 'client': <g4f.client.sync.SyncClient object at ...>, 'async_client': <g4f.client.async_client.AsyncClient object at ...>, 'api_key': 'test_key', 'model_kwargs': {'provider': 'g4f.models.Model.You'}}

        2. Использование без указания `api_key`:
            >>> ChatAI.validate_environment({"model_kwargs": {"provider": "g4f.models.Model.Ails"}}
            {'model_name': 'gpt-4o', 'model': 'gpt-4o', 'client': <g4f.client.sync.SyncClient object at ...>, 'async_client': <g4f.client.async_client.AsyncClient object at ...>, 'model_kwargs': {'provider': 'g4f.models.Model.Ails'}}
        """
        client_params = {
            "api_key": values["api_key"] if "api_key" in values else None,
            "provider": values["model_kwargs"]["provider"] if "provider" in values["model_kwargs"] else None,
        }
        values["client"] = Client(**client_params).chat.completions
        values["async_client"] = AsyncClient(
            **client_params
        ).chat.completions
        return values
```