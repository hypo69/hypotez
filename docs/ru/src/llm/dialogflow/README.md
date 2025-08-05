# Документация для модуля `src.ai.dialogflow`

## Обзор

Этот модуль предназначен для интеграции с Dialogflow и предоставляет возможности для понимания естественного языка (NLU) и создания диалоговых AI-приложений. Он включает в себя следующие основные функции:

- **Определение намерений (Intent Detection):** Определяет намерения пользователя на основе входного текста.
- **Распознавание сущностей (Entity Recognition):** Извлекает ключевые данные из фраз пользователя.
- **Контексты (Contexts):** Управляет разговором, сохраняя информацию о текущем состоянии диалога.
- **Интеграции (Integrations):** Поддерживает интеграцию с различными платформами, такими как Google Assistant, Facebook Messenger, Slack, Telegram и другие.
- **Webhook:** Поддерживает интеграции Webhook для вызова внешних сервисов и API.

## Подробнее

Модуль `src.ai.dialogflow` предоставляет инструменты для работы с платформой Dialogflow, позволяя интегрировать возможности обработки естественного языка в различные приложения. Он упрощает взаимодействие с API Dialogflow, предоставляя удобные методы для определения намерений пользователя, извлечения сущностей и управления контекстом диалога. Это позволяет создавать более интеллектуальные и интерактивные приложения.

## Примеры

Пример использования подмодуля **dialogflow**:

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

# Deleting an intent (make sure to replace intent_id with a real ID)
# dialogflow_client.delete_intent("your-intent-id")
```