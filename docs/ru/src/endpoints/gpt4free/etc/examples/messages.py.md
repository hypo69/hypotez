# Модуль обработки диалогов с использованием g4f

## Обзор

Этот модуль предоставляет класс `ConversationHandler`, который упрощает взаимодействие с языковыми моделями, такими как `gpt-4`, используя библиотеку `g4f`. Он позволяет поддерживать историю разговоров и получать ответы от модели.

## Подробнее

Модуль предназначен для организации диалогов с AI-моделями. Он хранит историю сообщений и использует клиент `g4f` для отправки запросов и получения ответов. Это упрощает реализацию ботов и других приложений, требующих взаимодействия с языковыми моделями.

## Классы

### `ConversationHandler`

**Описание**: Класс для управления диалогом с использованием языковой модели.

**Принцип работы**:
1.  Инициализируется с указанием модели (по умолчанию `gpt-4`).
2.  Поддерживает историю сообщений в атрибуте `conversation_history`.
3.  Позволяет добавлять сообщения пользователя и получать ответы от модели.

**Атрибуты**:

*   `client` (Client): Клиент для взаимодействия с API `g4f`.
*   `model` (str): Название используемой языковой модели (например, `gpt-4`).
*   `conversation_history` (list): Список словарей, представляющих историю сообщений в диалоге. Каждый словарь содержит ключи `"role"` (роль отправителя: `"user"` или `"assistant"`) и `"content"` (содержание сообщения).

**Методы**:

*   `__init__(model="gpt-4")`: Инициализирует экземпляр класса `ConversationHandler`.
*   `add_user_message(content: str)`: Добавляет сообщение пользователя в историю разговоров.
*   `get_response() -> str`: Отправляет историю разговоров модели и возвращает ответ ассистента.

## Функции

### `ConversationHandler.__init__`

```python
    def __init__(self, model="gpt-4"):
        """
        Инициализирует экземпляр класса ConversationHandler.
        
        Args:
            model (str, optional): Название используемой языковой модели. По умолчанию "gpt-4".
        
        """
```

**Назначение**: Инициализация объекта `ConversationHandler`.

**Параметры**:

*   `model` (str): Название языковой модели, которую нужно использовать для диалога. По умолчанию используется `"gpt-4"`.

**Как работает функция**:

1.  Инициализирует клиент `g4f` для взаимодействия с API.
2.  Сохраняет название модели в атрибуте `model`.
3.  Создает пустой список `conversation_history` для хранения истории сообщений.

```ascii
Инициализация
     │
     │
Создание клиента g4f
     │
     │
Сохранение названия модели
     │
     │
Создание пустого списка истории сообщений
     │
     │
Конец
```

### `ConversationHandler.add_user_message`

```python
    def add_user_message(self, content: str):
        """
        Добавляет сообщение пользователя в историю разговоров.
        
        Args:
            content (str): Содержание сообщения пользователя.
        
        """
```

**Назначение**: Добавление сообщения пользователя в историю разговоров.

**Параметры**:

*   `content` (str): Текст сообщения пользователя.

**Как работает функция**:

1.  Создает словарь с ролью `"user"` и переданным содержимым.
2.  Добавляет этот словарь в список `conversation_history`.

```ascii
Получение сообщения пользователя
     │
     │
Создание словаря сообщения
     │
     │
Добавление словаря в историю
     │
     │
Конец
```

**Примеры**:

```python
conversation = ConversationHandler()
conversation.add_user_message("Привет!")
```

### `ConversationHandler.get_response`

```python
    def get_response(self) -> str:
        """
        Отправляет историю разговоров модели и возвращает ответ ассистента.

        Returns:
            str: Содержание ответа ассистента.
        """
```

**Назначение**: Получение ответа от языковой модели на основе истории разговоров.

**Возвращает**:

*   `str`: Текст ответа ассистента.

**Как работает функция**:

1.  Отправляет запрос в API `g4f` с указанием модели и истории сообщений.
2.  Извлекает роль и содержимое сообщения ассистента из ответа API.
3.  Добавляет сообщение ассистента в историю разговоров.
4.  Возвращает содержимое сообщения ассистента.

```ascii
Отправка запроса в API g4f
     │
     │
Получение ответа от API
     │
     │
Извлечение сообщения ассистента
     │
     │
Добавление сообщения в историю
     │
     │
Возврат ответа ассистента
     │
     │
Конец
```

**Примеры**:

```python
conversation = ConversationHandler()
conversation.add_user_message("Как дела?")
response = conversation.get_response()
print("Assistant:", response)
```
```python
conversation = ConversationHandler(model='gpt-4')
conversation.add_user_message("Напиши код на python, который выводит 'Hello World!'")
response = conversation.get_response()
print(response)
```
```python
conversation = ConversationHandler(model='gpt-4')
conversation.add_user_message("Расскажи мне о Python")
response = conversation.get_response()
print(response)
```
```python
conversation = ConversationHandler(model='gpt-4')
conversation.add_user_message("Что такое машинное обучение?")
response = conversation.get_response()
print(response)
```
```python
conversation = ConversationHandler(model='gpt-4')
conversation.add_user_message("Как создать сайт на Flask?")
response = conversation.get_response()
print(response)
```
```python
conversation = ConversationHandler(model='gpt-4')
conversation.add_user_message("Напиши мне самый простой код для телеграмм бота на aiogram")
response = conversation.get_response()
print(response)