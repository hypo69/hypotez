## Как использовать этот блок кода
=========================================================================================

### Описание
-------------------------
Данный блок кода предоставляет описание модуля `dialogflow`, который интегрируется с Google Dialogflow.

### Шаги выполнения
-------------------------
1. **Импорт модуля:** 
    - Импортируй модуль `Dialogflow` из `src.ai.dialogflow`.
2. **Инициализация клиента:** 
    - Создай экземпляр класса `Dialogflow`, передав в него:
        - `project_id`: Идентификатор проекта в Dialogflow.
        - `session_id`: Уникальный идентификатор сессии.
3. **Использование методов:** 
    - Используй методы клиента `Dialogflow` для работы с Dialogflow API:
        - `detect_intent(text: str) -> dict`:  Выполняет определение намерения (intent) на основе введенного текста.
        - `list_intents() -> list`:  Получает список всех намерений (intents) в проекте.
        - `create_intent(display_name: str, training_phrases_parts: list, message_texts: list) -> dict`: Создает новое намерение (intent) с заданным описанием, примерами фраз (training_phrases_parts) и ответами (message_texts).
        - `delete_intent(intent_id: str) -> None`: Удаляет намерение (intent) с заданным идентификатором.

### Пример использования
-------------------------

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