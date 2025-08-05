# Модуль для обработки диалогов с использованием GPT-4 Free API

## Обзор

Модуль `messages.py` предоставляет класс `ConversationHandler`, который используется для взаимодействия с моделью GPT-4 Free API через библиотеку `g4f.client`.  Класс позволяет вести диалог с AI-моделью, сохраняя историю сообщений.

## Классы

### `ConversationHandler`

**Описание**: Класс для управления диалогом с моделью GPT-4 Free API.

**Атрибуты**:

- `client` (`Client`): Экземпляр класса `Client` из библиотеки `g4f.client`, который используется для взаимодействия с API.
- `model` (`str`): Имя модели GPT-4, с которой ведется диалог (например, "gpt-4").
- `conversation_history` (`list`): Список сообщений в диалоге.

**Методы**:

- `add_user_message(content)`: Добавляет сообщение пользователя в историю диалога.

  **Параметры**:

  - `content` (`str`): Сообщение пользователя.

- `get_response()`: Получает ответ от модели GPT-4 и добавляет его в историю диалога.

  **Возвращает**:

  - `str`: Текстовый ответ от модели GPT-4.

## Примеры

```python
# Создание экземпляра класса ConversationHandler
conversation = ConversationHandler()

# Добавление сообщения пользователя
conversation.add_user_message("Hello!")

# Получение ответа от модели GPT-4
print("Assistant:", conversation.get_response())

# Добавление нового сообщения пользователя
conversation.add_user_message("How are you?")

# Получение ответа от модели GPT-4
print("Assistant:", conversation.get_response())