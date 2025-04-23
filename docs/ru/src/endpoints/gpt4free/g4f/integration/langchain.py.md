# Документация модуля langchain.py

## Обзор

Модуль `langchain.py` предназначен для интеграции библиотеки `g4f` с `langchain`, обеспечивая взаимодействие с моделями OpenAI. Он содержит класс `ChatAI`, который расширяет функциональность `ChatOpenAI` из библиотеки `langchain_community`. Модуль также переопределяет функцию `convert_message_to_dict`, чтобы корректно обрабатывать сообщения с инструментами (tool_calls).

## Подробней

Этот модуль позволяет использовать модели OpenAI через библиотеку `g4f` в цепочках `langchain`. Он предоставляет удобный способ настройки и использования моделей, а также обеспечивает поддержку дополнительных параметров, таких как `api_key` и `provider`.

## Классы

### `ChatAI`

**Описание**: Класс `ChatAI` наследуется от `ChatOpenAI` и предназначен для интеграции с моделями OpenAI через библиотеку `g4f`. Он позволяет использовать модели OpenAI в цепочках `langchain` с дополнительными параметрами, такими как `api_key` и `provider`.

**Наследует**: `ChatOpenAI`

**Атрибуты**:
- `model_name` (str): Имя модели, используемой по умолчанию. По умолчанию "gpt-4o".

**Методы**:
- `validate_environment`: Валидирует окружение и создает клиентов для синхронного и асинхронного взаимодействия с API.

### `ChatAI.validate_environment`

```python
def validate_environment(cls, values: dict) -> dict:
    """Валидирует окружение и создает клиентов для синхронного и асинхронного взаимодействия с API.

    Args:
        cls (class): Класс, для которого выполняется валидация.
        values (dict): Словарь с параметрами окружения.

    Returns:
        dict: Обновленный словарь с параметрами, содержащий клиентов для взаимодействия с API.

    
    - Извлекает `api_key` и `provider` из словаря `values`.
    - Создает синхронного клиента `Client` и асинхронного клиента `AsyncClient` для взаимодействия с API `g4f`.
    - Добавляет клиентов в словарь `values` для дальнейшего использования.

    Примеры:
    >>> values = {"api_key": "test_key", "model_kwargs": {"provider": "test_provider"}}
    >>> ChatAI.validate_environment(values)
    {'api_key': 'test_key', 'model_kwargs': {'provider': 'test_provider'}, 'client': <g4f.client.sync.SyncChatCompletion object at ...>, 'async_client': <g4f.client.asyncio.AsyncChatCompletion object at ...>}
    """
```

## Функции

### `new_convert_message_to_dict`

```python
def new_convert_message_to_dict(message: BaseMessage) -> dict:
    """Конвертирует объект сообщения в словарь, обрабатывая сообщения с инструментами (tool_calls).

    Args:
        message (BaseMessage): Объект сообщения для конвертации.

    Returns:
        dict: Словарь, представляющий сообщение.

    
    - Проверяет, является ли сообщение экземпляром `ChatCompletionMessage`.
    - Если да, то формирует словарь с полями `role`, `content` и `tool_calls`.
    - Если сообщение содержит `tool_calls`, то преобразует их в формат словаря и добавляет в результирующий словарь.
    - Если поле `content` пустое, устанавливает его в `None`.
    - Если сообщение не является экземпляром `ChatCompletionMessage`, использует стандартную функцию `convert_message_to_dict` для преобразования.

    Примеры:
    >>> from g4f.client.stubs import ChatCompletionMessage, ToolCall, Function
    >>> message = ChatCompletionMessage(role="assistant", content="test", tool_calls=[ToolCall(id="1", type="function", function=Function(name="test", arguments="{}"))])
    >>> new_convert_message_to_dict(message)
    {'role': 'assistant', 'content': 'test', 'tool_calls': [{'id': '1', 'type': 'function', 'function': Function(name='test', arguments='{}')}]}
    """