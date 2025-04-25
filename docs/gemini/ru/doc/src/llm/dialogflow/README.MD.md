# Модуль Dialogflow

## Обзор

Модуль `dialogflow` обеспечивает интеграцию с сервисом Google Dialogflow для создания и управления диалоговыми ботами.

## Подробней

Dialogflow — это платформа Google для создания и управления диалоговыми ботами. Она предоставляет инструменты для:

- **Распознавания намерений (Intent Detection):** Определение намерения пользователя на основе введенного текста.
- **Распознавания сущностей (Entity Recognition):** Извлечение ключевой информации из фраз пользователя.
- **Контекста (Contexts):** Управление диалогом путем сохранения информации о текущем состоянии.
- **Интеграции (Integrations):** Поддержка интеграции с различными платформами, такими как Google Assistant, Facebook Messenger, Slack, Telegram и другими.
- **Вебхуков (Webhooks):** Поддержка интеграции с вебхуками для вызова внешних служб и API.

Этот модуль предоставляет классы и функции для взаимодействия с API Dialogflow, а также содержит примеры использования.

## Классы

### `Dialogflow`

**Описание**: Класс `Dialogflow` предоставляет методы для взаимодействия с API Dialogflow.

**Наследует**: 

**Атрибуты**:

- `project_id` (str): ID проекта Dialogflow.
- `session_id` (str): Уникальный ID сессии.
- `language_code` (str, optional): Язык по умолчанию. По умолчанию - `ru-RU`.

**Методы**:

- `detect_intent(text: str) -> dict`: Определяет намерение пользователя на основе введенного текста.
    **Параметры**:
    - `text` (str): Введенный текст.
    **Возвращает**:
    - `dict`: Ответ от API Dialogflow.
    **Вызывает исключения**:
    - `Exception`: В случае ошибки при вызове API.
- `list_intents() -> list`: Возвращает список всех имеющихся намерений в проекте.
    **Возвращает**:
    - `list`: Список намерений.
    **Вызывает исключения**:
    - `Exception`: В случае ошибки при вызове API.
- `create_intent(display_name: str, training_phrases_parts: list, message_texts: list) -> dict`: Создает новое намерение в проекте.
    **Параметры**:
    - `display_name` (str): Отображаемое имя намерения.
    - `training_phrases_parts` (list): Список фраз для обучения намерения.
    - `message_texts` (list): Список текстовых сообщений для ответа на намерение.
    **Возвращает**:
    - `dict`: Информация о созданном намерении.
    **Вызывает исключения**:
    - `Exception`: В случае ошибки при вызове API.
- `delete_intent(intent_id: str) -> None`: Удаляет намерение из проекта.
    **Параметры**:
    - `intent_id` (str): ID намерения для удаления.
    **Возвращает**:
    - `None`:
    **Вызывает исключения**:
    - `Exception`: В случае ошибки при вызове API.

**Примеры**:

```python
from src.ai.dialogflow import Dialogflow

project_id = "your-project-id"
session_id = "unique-session-id"

dialogflow_client = Dialogflow(project_id, session_id)

# Пример использования методов
intent_response = dialogflow_client.detect_intent("Привет")
print("Распознанное намерение:", intent_response)

intents = dialogflow_client.list_intents()
print("Список намерений:", intents)

new_intent = dialogflow_client.create_intent(
    display_name="НовоеНамерение",
    training_phrases_parts=["новая фраза", "другая фраза"],
    message_texts=["Это новое намерение"]
)
print("Созданное намерение:", new_intent)

# Удаление намерения (убедитесь, что intent_id заменен на реальный ID)
# dialogflow_client.delete_intent("ваш-intent-id")
```

## Функции

### `get_project_id(path: str) -> str`

**Назначение**: Извлекает ID проекта Dialogflow из файла конфигурации.

**Параметры**:

- `path` (str): Путь к файлу конфигурации.

**Возвращает**:

- `str`: ID проекта Dialogflow.

**Вызывает исключения**:

- `FileNotFoundError`: Если файл конфигурации не найден.
- `KeyError`: Если в файле конфигурации отсутствует ключ `project_id`.

**Примеры**:

```python
from src.ai.dialogflow import get_project_id

project_id = get_project_id("config.json")
print("ID проекта:", project_id)
```

### `get_session_id(path: str) -> str`

**Назначение**: Извлекает ID сессии Dialogflow из файла конфигурации.

**Параметры**:

- `path` (str): Путь к файлу конфигурации.

**Возвращает**:

- `str`: ID сессии Dialogflow.

**Вызывает исключения**:

- `FileNotFoundError`: Если файл конфигурации не найден.
- `KeyError`: Если в файле конфигурации отсутствует ключ `session_id`.

**Примеры**:

```python
from src.ai.dialogflow import get_session_id

session_id = get_session_id("config.json")
print("ID сессии:", session_id)
```

## Параметры

- `project_id` (str): ID проекта Dialogflow, который используется для взаимодействия с API.
- `session_id` (str): Уникальный ID сессии, используемый для идентификации пользователя.
- `language_code` (str, optional): Язык по умолчанию для диалогового бота. По умолчанию - `ru-RU`.

## Примеры

```python
from src.ai.dialogflow import Dialogflow

# Создание экземпляра класса Dialogflow
dialogflow_client = Dialogflow(project_id="your-project-id", session_id="your-session-id")

# Определение намерения пользователя
intent_response = dialogflow_client.detect_intent("Привет")
print("Распознанное намерение:", intent_response)

# Получение списка имеющихся намерений
intents = dialogflow_client.list_intents()
print("Список намерений:", intents)
```