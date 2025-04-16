# Модуль интеграции Langchain для G4F
## Обзор

Модуль предоставляет интеграцию между библиотекой `g4f` (GenerativeForFree) и фреймворком `Langchain`. Он включает в себя переопределение функции конвертации сообщений и класс `ChatAI`, который расширяет возможности `ChatOpenAI` для работы с моделями, предоставляемыми через `g4f`.

## Подробнее

Этот модуль позволяет использовать модели, доступные через `g4f`, в приложениях `Langchain`, обеспечивая гибкость в выборе моделей и упрощая интеграцию. Модуль содержит класс `ChatAI`, который может быть использован как замена стандартному `ChatOpenAI` с возможностью указания провайдера модели через `model_kwargs`.

## Функции

### `new_convert_message_to_dict`

```python
def new_convert_message_to_dict(message: BaseMessage) -> dict:
    """ Функция преобразует объект сообщения `BaseMessage` в словарь, адаптированный для использования с `g4f`.

    Args:
        message (BaseMessage): Объект сообщения для преобразования.

    Returns:
        dict: Словарь, представляющий сообщение. Включает роль, содержимое и, при наличии, информацию о вызовах инструментов (tool_calls).

    Описание работы:
        Функция проверяет, является ли сообщение экземпляром `ChatCompletionMessage`. Если да, то извлекает информацию о роли, содержимом и вызовах инструментов и формирует словарь. Если сообщение не является экземпляром `ChatCompletionMessage`, то использует стандартную функцию `convert_message_to_dict` из модуля `openai`.

    Пример:
        >>> from langchain_core.messages import AIMessage
        >>> message = AIMessage(content="Hello", additional_kwargs={})
        >>> new_convert_message_to_dict(message)
        {'content': 'Hello', 'role': 'assistant'}
    """
```

## Классы

### `ChatAI`

```python
class ChatAI(ChatOpenAI):
    """ Класс для интеграции моделей `g4f` с `Langchain`.

    Inherits:
        ChatOpenAI: Наследует от `ChatOpenAI` из `langchain_community`.

    Attributes:
        model_name (str): Имя модели по умолчанию "gpt-4o".
    """
```

**Описание**: Класс `ChatAI` расширяет `ChatOpenAI` для использования моделей, предоставляемых через `g4f`. Он позволяет указывать провайдера модели через `model_kwargs` и использует `g4f.Client` для взаимодействия с API.

**Методы**:

#### `validate_environment`

```python
    @classmethod
    def validate_environment(cls, values: dict) -> dict:
        """ Метод для валидации окружения и настройки клиентов `g4f` (синхронного и асинхронного).

        Args:
            values (dict): Словарь с параметрами конфигурации, включающий `api_key` и `model_kwargs`.

        Returns:
            dict: Обновленный словарь `values` с добавленными клиентами `client` и `async_client` для `g4f`.

        Описание работы:
            Метод извлекает `api_key` и провайдера модели из словаря `values` и использует их для инициализации синхронного и асинхронного клиентов `g4f`. Затем добавляет эти клиенты в словарь `values` для дальнейшего использования.

        Пример:
            >>> values = {"api_key": "test_key", "model_kwargs": {"provider": "test_provider"}}
            >>> ChatAI.validate_environment(values)
            {'api_key': 'test_key', 'model_kwargs': {'provider': 'test_provider'}, 'client': <g4f.client.chat.completions object at 0x...>, 'async_client': <g4f.client.chat.completions object at 0x...>}
        """
```

**Параметры класса**:
   - `model_name` (str): Имя модели по умолчанию "gpt-4o".