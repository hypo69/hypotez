# Модуль для управления обменом сообщений

## Обзор

Модуль `src.endpoints.gpt4free/etc/examples/messages.py` демонстрирует использование класса `ConversationHandler` для управления историей разговоров и получения ответов от языковой модели.

## Подробней

Модуль показывает, как создавать экземпляры `ConversationHandler`, добавлять сообщения пользователя и получать ответы от модели.

## Классы

### `ConversationHandler`

**Описание**: Класс для управления историей разговоров и взаимодействия с языковой моделью.

**Атрибуты**:

*   `client` (Client): Экземпляр класса `Client` для взаимодействия с API.
*   `model` (str): Имя используемой модели (по умолчанию `"gpt-4"`).
*   `conversation_history` (list): Список сообщений в разговоре.

**Методы**:

*   `__init__(self, model="gpt-4")`: Инициализирует объект `ConversationHandler`.
*   `add_user_message(self, content)`: Добавляет сообщение пользователя в историю разговора.
*   `get_response(self)`: Получает ответ от языковой модели на основе истории разговора.

## Методы класса `ConversationHandler`

### `__init__`

```python
def __init__(self, model="gpt-4"):
```

**Назначение**: Инициализирует объект `ConversationHandler`.

**Параметры**:

*   `model` (str, optional): Имя используемой модели. Defaults to `"gpt-4"`.

**Как работает функция**:

1.  Создает экземпляр класса `Client`.
2.  Устанавливает имя модели.
3.  Инициализирует пустой список для хранения истории разговора.

### `add_user_message`

```python
def add_user_message(self, content):
```

**Назначение**: Добавляет сообщение пользователя в историю разговора.

**Параметры**:

*   `content` (str): Текст сообщения пользователя.

**Как работает функция**:

1.  Добавляет словарь с ролью "user" и содержимым сообщения в список `conversation_history`.

### `get_response`

```python
def get_response(self):
```

**Назначение**: Получает ответ от языковой модели на основе истории разговора.

**Возвращает**:

*   `str`: Ответ языковой модели.

**Как работает функция**:

1.  Отправляет запрос к языковой модели, используя метод `client.chat.completions.create` и текущую историю разговора.
2.  Извлекает роль и содержимое ответа из ответа модели.
3.  Добавляет сообщение ответа в историю разговора.
4.  Возвращает содержимое ответа.

## Пример использования

```python
from g4f.client import Client

class ConversationHandler:
    def __init__(self, model="gpt-4"):
        self.client = Client()
        self.model = model
        self.conversation_history = []
        
    def add_user_message(self, content):
        self.conversation_history.append({
            "role": "user",
            "content": content
        })
        
    def get_response(self):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.conversation_history
        )
        assistant_message = {
            "role": response.choices[0].message.role,
            "content": response.choices[0].message.content
        }
        self.conversation_history.append(assistant_message)
        return assistant_message["content"]

# Usage example
conversation = ConversationHandler()
conversation.add_user_message("Hello!")
print("Assistant:", conversation.get_response())

conversation.add_user_message("How are you?")
print("Assistant:", conversation.get_response())
```