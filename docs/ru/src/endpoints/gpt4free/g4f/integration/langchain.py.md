# Модуль интеграции g4f с Langchain

## Обзор

Модуль предоставляет интеграцию между библиотекой `g4f` и фреймворком `Langchain` для работы с чат-моделями. Он содержит класс `ChatAI`, который наследуется от `ChatOpenAI` из `langchain_community.chat_models` и позволяет использовать модели `g4f` в качестве чат-моделей Langchain. Также, модуль переопределяет функцию `convert_message_to_dict` для корректной обработки сообщений с `tool_calls`.

## Подробнее

Этот модуль предназначен для упрощения интеграции и использования чат-моделей, предоставляемых `g4f`, в приложениях, использующих `Langchain`. Он обеспечивает совместимость форматов сообщений и позволяет использовать асинхронные клиенты `g4f` для взаимодействия с моделями.

## Функции

### `new_convert_message_to_dict`

```python
def new_convert_message_to_dict(message: BaseMessage) -> dict:
    """Преобразует объект сообщения (BaseMessage) в словарь для совместимости с форматом, ожидаемым Langchain.

    Args:
        message (BaseMessage): Объект сообщения для преобразования.

    Returns:
        dict: Словарь, представляющий сообщение.

    Как работает функция:
    1. Проверяет, является ли сообщение экземпляром класса `ChatCompletionMessage`.
    2. Если это так, то создает словарь с ключами "role" и "content", а также добавляет информацию о `tool_calls`, если она присутствует.
    3. Если поле `content` пустое, то устанавливает его в `None`.
    4. Если сообщение не является экземпляром класса `ChatCompletionMessage`, то вызывает исходную функцию `convert_message_to_dict` для преобразования.

    ASCII flowchart:
    A (Является ли сообщение ChatCompletionMessage?)
    |
    -- Yes --> B (Создать словарь с информацией о роли, содержании и tool_calls)
    |
    -- No --> C (Использовать стандартную функцию convert_message_to_dict)
    |
    D (Вернуть словарь)

    Примеры:
        >>> from langchain_community.messages import HumanMessage
        >>> message = HumanMessage(content="Hello")
        >>> new_convert_message_to_dict(message)
        {'content': 'Hello', 'additional_kwargs': {}, 'type': 'human'}

        >>> from g4f.client.stubs import ChatCompletionMessage, ToolCall, Function
        >>> function = Function(name="test_function", arguments='{}')
        >>> tool_call = ToolCall(id="123", type="function", function=function)
        >>> message = ChatCompletionMessage(content="Hi", role="assistant", tool_calls=[tool_call])
        >>> new_convert_message_to_dict(message)
        {'role': 'assistant', 'content': 'Hi', 'tool_calls': [{'id': '123', 'type': 'function', 'function': function}]}
    """
    ...
```

## Классы

### `ChatAI`

**Описание**: Класс `ChatAI` наследуется от `ChatOpenAI` и предоставляет интеграцию с моделями `g4f`.

**Наследует**:
- `ChatOpenAI`

**Атрибуты**:
- `model_name` (str): Имя модели, используемой по умолчанию "gpt-4o".

**Методы**:
- `validate_environment`: Проверяет и устанавливает параметры окружения для использования `g4f` клиента.

#### `validate_environment`

```python
    @classmethod
    def validate_environment(cls, values: dict) -> dict:
        """Проверяет и устанавливает параметры окружения для использования `g4f` клиента.

        Args:
            values (dict): Словарь с параметрами, переданными при инициализации класса.

        Returns:
            dict: Обновленный словарь с параметрами, включающий инициализированные клиенты `g4f`.

        Как работает функция:
        1. Извлекает параметры `api_key` и `provider` из входного словаря `values`.
        2. Инициализирует синхронного клиента `Client` из библиотеки `g4f`, используя переданные параметры.
        3. Инициализирует асинхронного клиента `AsyncClient` из библиотеки `g4f`, используя те же параметры.
        4. Сохраняет инстансы клиентов в словаре `values` для дальнейшего использования.

        ASCII flowchart:
        A (Извлечение параметров api_key и provider)
        |
        B (Инициализация синхронного клиента g4f.Client)
        |
        C (Инициализация асинхронного клиента g4f.AsyncClient)
        |
        D (Сохранение клиентов в словаре values)
        |
        E (Возврат обновленного словаря values)

        Примеры:
            >>> params = {"api_key": "test_key", "model_kwargs": {"provider": "test_provider"}}
            >>> ChatAI.validate_environment(params)
            {'api_key': 'test_key', 'model_kwargs': {'provider': 'test_provider'}, 'client': <g4f.client.chat.completions object at ...>, 'async_client': <g4f.client.chat.completions object at ...>}
        """
        ...