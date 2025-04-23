# Модуль `src.ai.dialogflow`

## Обзор

Модуль `src.ai.dialogflow` предназначен для интеграции с Google Dialogflow. Он предоставляет инструменты для обработки естественного языка (NLU) и создания разговорных ИИ-приложений. Модуль включает функции для определения намерений пользователя, извлечения ключевых данных из фраз, управления контекстом диалога и интеграции с различными платформами и API.

## Подробнее

Этот модуль позволяет упростить взаимодействие с Google Dialogflow, абстрагируя сложные детали API и предоставляя удобные методы для выполнения основных задач, таких как определение намерений, создание, чтение, обновление и удаление намерений.

## Содержание

- [Что такое Dialogflow Model](#что-такое-dialogflow-model)
- [Описание модуля](#описание-модуля)
- [Основные функции](#основные-функции)
- [Пример использования](#пример-использования)

## Основные функции

- **Определение намерений (Intent Detection)**: Определяет намерения пользователя на основе введенного текста.
- **Работа с сущностями (Entity Recognition)**: Извлекает ключевые данные из пользовательских фраз.
- **Контексты (Contexts)**: Управляет диалогом, сохраняя информацию о текущем состоянии разговора.
- **Интеграции**: Поддерживает интеграцию с различными платформами, такими как Google Assistant, Facebook Messenger, Slack, Telegram и другими.
- **Webhook**: Поддерживает Webhook-интеграции для вызова внешних сервисов и API.

## Пример использования

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

# Удаление намерения (не забудьте заменить intent_id на реальный ID)
# dialogflow_client.delete_intent("your-intent-id")