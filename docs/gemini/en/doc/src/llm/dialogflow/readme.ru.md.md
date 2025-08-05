# Модуль `dialogflow`
## Обзор
Модуль для интеграции с Google Dialogflow, предоставляя возможности для обработки естественного языка (NLU) и создания разговорных ИИ-приложений. 

## Детали
Этот модуль позволяет взаимодействовать с Google Dialogflow API. 

## Содержание
- **[Определение намерений](https://github.com/hypo69/hypotez/blob/master/src/ai/dialogflow/about.ru.md#определение-намерений)**
- **[Работа с сущностями](https://github.com/hypo69/hypotez/blob/master/src/ai/dialogflow/about.ru.md#работа-с-сущностями)**
- **[Контексты](https://github.com/hypo69/hypotez/blob/master/src/ai/dialogflow/about.ru.md#контексты)**
- **[Интеграции](https://github.com/hypo69/hypotez/blob/master/src/ai/dialogflow/about.ru.md#интеграции)**
- **[Webhook](https://github.com/hypo69/hypotez/blob/master/src/ai/dialogflow/about.ru.md#webhook)**
- **[Пример использования](https://github.com/hypo69/hypotez/blob/master/src/ai/dialogflow/readme.ru.md#пример-использования-подмодуля-dialogflow)**

##  Функции
### `Dialogflow`
```python
class Dialogflow:
    """
    Класс для взаимодействия с Google Dialogflow API.

    Attributes:
        project_id (str): ID проекта Dialogflow.
        session_id (str): ID сессии, уникальный для каждого пользователя.

    Methods:
        detect_intent(text: str) -> dict: Определяет намерение пользователя.
        list_intents() -> list: Возвращает список всех намерений.
        create_intent(display_name: str, training_phrases_parts: list, message_texts: list) -> dict: Создает новое намерение.
        delete_intent(intent_id: str) -> None: Удаляет намерение.
    """
    def detect_intent(self, text: str) -> dict:
        """
        Определяет намерение пользователя.

        Args:
            text (str): Текст, введенный пользователем.

        Returns:
            dict: Ответ Dialogflow, содержащий информацию о распознанном намерении.
        """
        pass

    def list_intents(self) -> list:
        """
        Возвращает список всех намерений.

        Returns:
            list: Список намерений.
        """
        pass

    def create_intent(self, display_name: str, training_phrases_parts: list, message_texts: list) -> dict:
        """
        Создает новое намерение.

        Args:
            display_name (str): Имя намерения.
            training_phrases_parts (list): Список фразовых образцов для обучения.
            message_texts (list): Список текстов ответов.

        Returns:
            dict: Информация о созданном намерении.
        """
        pass

    def delete_intent(self, intent_id: str) -> None:
        """
        Удаляет намерение.

        Args:
            intent_id (str): ID намерения.
        """
        pass
```

## Пример использования подмодуля **dialogflow**:
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