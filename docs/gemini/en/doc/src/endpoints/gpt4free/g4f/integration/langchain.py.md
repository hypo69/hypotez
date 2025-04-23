# Модуль интеграции Langchain с g4f

## Обзор

Этот модуль обеспечивает интеграцию между библиотекой Langchain и g4f (GenerativeForFree), позволяя использовать модели g4f в качестве чат-моделей Langchain. Модуль содержит класс `ChatAI`, который расширяет `ChatOpenAI` из Langchain и адаптирует его для работы с клиентами g4f.

## Подробнее

Модуль позволяет использовать модели g4f в качестве альтернативы моделям OpenAI в Langchain. Это достигается путем переопределения метода `convert_message_to_dict` и расширения класса `ChatOpenAI` для использования клиентов g4f.

## Функции

### `new_convert_message_to_dict`

```python
def new_convert_message_to_dict(message: BaseMessage) -> dict:
    """Преобразует объект сообщения в словарь для использования в API чат-моделей.

    Args:
        message (BaseMessage): Объект сообщения для преобразования.

    Returns:
        dict: Словарь, представляющий сообщение.

    """
```

**Назначение**:
Эта функция преобразует объекты сообщений (типа `BaseMessage`) в формат словаря, который требуется для взаимодействия с API чат-моделей. Она обрабатывает как стандартные сообщения, так и сообщения с `tool_calls`.

**Параметры**:
- `message` (BaseMessage): Объект сообщения, который необходимо преобразовать.

**Возвращает**:
- `dict`: Словарь, представляющий сообщение.

**Как работает**:
- Функция проверяет, является ли сообщение экземпляром `ChatCompletionMessage`. Если да, то создается словарь с полями `"role"` и `"content"` из атрибутов сообщения.
- Если в сообщении присутствуют `tool_calls`, они также преобразуются в формат словаря и добавляются в результирующий словарь.
- Если сообщение не является экземпляром `ChatCompletionMessage`, используется стандартная функция `convert_message_to_dict` из `langchain_community.chat_models.openai`.

**Примеры**:
```python
# Пример использования функции new_convert_message_to_dict
from langchain_core.messages import BaseMessage, HumanMessage
message = HumanMessage(content="Hello")
message_dict = new_convert_message_to_dict(message)
print(message_dict)
# {'content': 'Hello', 'additional_kwargs': {}, 'type': 'human'}
```

## Классы

### `ChatAI`

```python
class ChatAI(ChatOpenAI):
    """Чат-модель, адаптированная для использования g4f с Langchain.

    Inherits:
        ChatOpenAI: Расширяет класс ChatOpenAI из Langchain.

    Attributes:
        model_name (str): Имя модели, по умолчанию "gpt-4o".

    Methods:
        validate_environment(): Проверяет и устанавливает окружение для работы с клиентами g4f.
    """
```

**Описание**:
Класс `ChatAI` расширяет `ChatOpenAI` из Langchain и предназначен для использования моделей g4f в качестве чат-моделей Langchain.

**Наследует**:
- `ChatOpenAI`: Расширяет класс `ChatOpenAI` из Langchain.

**Атрибуты**:
- `model_name` (str): Имя модели, по умолчанию `"gpt-4o"`.

**Методы**:

#### `validate_environment`

```python
@classmethod
def validate_environment(cls, values: dict) -> dict:
    """Проверяет и устанавливает окружение для работы с клиентами g4f.

    Args:
        values (dict): Словарь с параметрами окружения.

    Returns:
        dict: Обновленный словарь с параметрами окружения.

    """
```

**Назначение**:
Этот метод проверяет и устанавливает окружение, необходимое для работы с клиентами g4f. Он создает экземпляры `Client` и `AsyncClient` из g4f и сохраняет их в словаре `values`.

**Параметры**:
- `values` (dict): Словарь с параметрами окружения, такими как `api_key` и `model_kwargs`.

**Возвращает**:
- `dict`: Обновленный словарь `values` с добавленными клиентами `Client` и `AsyncClient`.

**Как работает**:
- Извлекает параметры `api_key` и `provider` из словаря `values`.
- Создает экземпляры `Client` и `AsyncClient` из g4f, используя извлеченные параметры.
- Сохраняет созданные экземпляры в словаре `values` под ключами `"client"` и `"async_client"`.

**Примеры**:
```python
# Пример использования функции validate_environment
values = {"api_key": "test_key", "model_kwargs": {"provider": "test_provider"}}
updated_values = ChatAI.validate_environment(values)
print(updated_values.keys())
# dict_keys(['api_key', 'model_kwargs', 'client', 'async_client'])
```