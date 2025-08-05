# Модуль Dialogflow

## Обзор

Модуль `src.ai.dialogflow` предоставляет инструменты для взаимодействия с Google Dialogflow, платформой для создания разговорных ИИ-приложений. 

## Подробнее

Dialogflow - это платформа для создания разговорных ИИ-приложений, которая позволяет создавать чат-ботов, виртуальных помощников и других взаимодействий, которые имитируют человеческое общение. Модуль `src.ai.dialogflow` предоставляет средства для интеграции с Dialogflow, такие как:

- **Определение намерений (Intent Detection):** Определение намерений пользователя на основе введенного текста.
- **Работа с сущностями (Entity Recognition):** Извлечение ключевых данных из пользовательских фраз.
- **Контексты (Contexts):** Управление диалогом, сохраняя информацию о текущем состоянии разговора.
- **Интеграции:** Поддерживает интеграцию с различными платформами, такими как Google Assistant, Facebook Messenger, Slack, Telegram, и другими.
- **Webhook:** Поддерживает Webhook-интеграции для вызова внешних сервисов и API.


## Классы

### `Dialogflow`

**Описание**: Класс для взаимодействия с Google Dialogflow API. 

**Атрибуты**:
- `project_id` (str): ID проекта Dialogflow.
- `session_id` (str): ID сессии пользователя.

**Методы**:

- `detect_intent(text: str) -> dict`: Определяет намерение пользователя на основе введенного текста.

    **Параметры**:
    - `text` (str): Текст, введенный пользователем.

    **Возвращает**:
    - `dict`: Словарь с информацией о распознанном намерении, включая `intent_name` и `fulfillment_text`.

    **Вызывает исключения**:
    - `Exception`: Если возникает ошибка при взаимодействии с Dialogflow API.


- `list_intents() -> list`: Возвращает список всех намерений в проекте Dialogflow.

    **Параметры**:
    - Нет.

    **Возвращает**:
    - `list`: Список словарей, где каждый словарь представляет намерение с `intent_id` и `display_name`.

    **Вызывает исключения**:
    - `Exception`: Если возникает ошибка при взаимодействии с Dialogflow API.


- `create_intent(display_name: str, training_phrases_parts: list, message_texts: list) -> dict`: Создает новое намерение в проекте Dialogflow.

    **Параметры**:
    - `display_name` (str): Отображаемое имя намерения.
    - `training_phrases_parts` (list): Список фрагментов обучающих фраз для намерения.
    - `message_texts` (list): Список текстовых сообщений, которые будут возвращены при активации намерения.

    **Возвращает**:
    - `dict`: Словарь с информацией о созданном намерении, включая `intent_id` и `display_name`.

    **Вызывает исключения**:
    - `Exception`: Если возникает ошибка при взаимодействии с Dialogflow API.


- `delete_intent(intent_id: str) -> None`: Удаляет намерение из проекта Dialogflow.

    **Параметры**:
    - `intent_id` (str): ID намерения, которое нужно удалить.

    **Возвращает**:
    - `None`.

    **Вызывает исключения**:
    - `Exception`: Если возникает ошибка при взаимодействии с Dialogflow API.

## Примеры

```python
from src.ai.dialogflow import Dialogflow

project_id = "your-project-id"
session_id = "unique-session-id"

dialogflow_client = Dialogflow(project_id, session_id)

# Пример использования методов
intent_response = dialogflow_client.detect_intent("Hello")
print("Detected Intent:", intent_response)

intents = dialogflow_client.list_intents()
print("List of Intents:", intents)

new_intent = dialogflow_client.create_intent(
    display_name="NewIntent",
    training_phrases_parts=["new phrase", "another phrase"],
    message_texts=["This is a new intent"]
)
print("Created Intent:", new_intent)

# Удаление намерения (не забудьте заменить intent_id на реальный ID)
# dialogflow_client.delete_intent("your-intent-id")
```