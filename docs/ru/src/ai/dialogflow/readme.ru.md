# Модуль `src.ai.dialogflow`

## Обзор

Модуль `src.ai.dialogflow` предназначен для интеграции с Google Dialogflow. Он предоставляет инструменты для обработки естественного языка (NLU) и создания разговорных ИИ-приложений.

## Подробнее

Этот модуль позволяет определять намерения пользователя, извлекать ключевые данные, управлять контекстами диалога и интегрироваться с различными платформами. Он упрощает взаимодействие с Google Dialogflow API и предоставляет удобные методы для выполнения основных задач, таких как определение намерений, создание и удаление интентов.

## Классы

### `Dialogflow`

**Описание**: Класс `Dialogflow` обеспечивает взаимодействие с Google Dialogflow API.

**Принцип работы**: Класс инициализируется с использованием ID проекта и ID сессии, после чего может использоваться для выполнения различных операций, таких как определение намерений, создание, удаление и перечисление интентов.

**Методы**:
- `detect_intent`: Определяет намерение пользователя на основе введенного текста.
- `list_intents`: Возвращает список всех интентов в проекте.
- `create_intent`: Создает новый интент с заданными параметрами.
- `delete_intent`: Удаляет интент по его ID.

**Параметры**:
- `project_id` (str): ID проекта в Google Cloud Platform.
- `session_id` (str): Уникальный ID сессии для Dialogflow.

**Примеры**
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

## Функции

В данном файле отсутствуют отдельные функции, только методы класса `Dialogflow`.

### `detect_intent`

**Назначение**: Определяет намерение пользователя на основе введенного текста.

**Параметры**:
- `text` (str): Текст запроса пользователя.
- `language_code` (str, optional): Языковой код. По умолчанию "ru-RU".

**Возвращает**:
- `DetectIntentResponse`: Объект ответа от Dialogflow API с информацией о найденном намерении.

**Вызывает исключения**:
- `google.api_core.exceptions.ApiException`: В случае ошибок при вызове Dialogflow API.

**Как работает функция**:

1. **Создание запроса**: Формируется запрос к Dialogflow API для определения намерения на основе входного текста и языкового кода.
2. **Отправка запроса**: Запрос отправляется к Dialogflow API.
3. **Обработка ответа**: Полученный ответ от Dialogflow API обрабатывается и возвращается.

```
Создание запроса --> Отправка запроса --> Обработка ответа
```

**Примеры**:
```python
from src.ai.dialogflow import Dialogflow

project_id = "your-project-id"
session_id = "unique-session-id"

dialogflow_client = Dialogflow(project_id, session_id)
intent_response = dialogflow_client.detect_intent("Привет")
print("Detected Intent:", intent_response)
```

### `list_intents`

**Назначение**: Возвращает список всех интентов в проекте Dialogflow.

**Параметры**:
- Нет параметров.

**Возвращает**:
- `list`: Список объектов `Intent` от Dialogflow API, представляющих все интенты в проекте.

**Вызывает исключения**:
- `google.api_core.exceptions.ApiException`: В случае ошибок при вызове Dialogflow API.

**Как работает функция**:

1. **Формирование запроса**: Создается запрос к Dialogflow API для получения списка всех интентов в проекте.
2. **Отправка запроса**: Запрос отправляется к Dialogflow API.
3. **Обработка ответа**: Полученный ответ от Dialogflow API обрабатывается, и список интентов возвращается.

```
Формирование запроса --> Отправка запроса --> Обработка ответа
```

**Примеры**:
```python
from src.ai.dialogflow import Dialogflow

project_id = "your-project-id"
session_id = "unique-session-id"

dialogflow_client = Dialogflow(project_id, session_id)
intents = dialogflow_client.list_intents()
print("List of Intents:", intents)
```

### `create_intent`

**Назначение**: Создает новый интент в проекте Dialogflow.

**Параметры**:
- `display_name` (str): Отображаемое имя нового интента.
- `training_phrases_parts` (list): Список фраз для обучения модели.
- `message_texts` (list): Список ответов, которые будут отправлены пользователю при срабатывании интента.
- `language_code` (str, optional): Языковой код. По умолчанию "ru-RU".

**Возвращает**:
- `Intent`: Объект созданного `Intent` от Dialogflow API.

**Вызывает исключения**:
- `google.api_core.exceptions.ApiException`: В случае ошибок при вызове Dialogflow API.

**Как работает функция**:

1. **Подготовка данных**: Формируются данные для создания нового интента, включая фразы для обучения и ответы.
2. **Создание запроса**: Создается запрос к Dialogflow API для создания нового интента с использованием подготовленных данных.
3. **Отправка запроса**: Запрос отправляется к Dialogflow API.
4. **Обработка ответа**: Полученный ответ от Dialogflow API обрабатывается, и объект созданного интента возвращается.

```
Подготовка данных --> Создание запроса --> Отправка запроса --> Обработка ответа
```

**Примеры**:
```python
from src.ai.dialogflow import Dialogflow

project_id = "your-project-id"
session_id = "unique-session-id"

dialogflow_client = Dialogflow(project_id, session_id)
new_intent = dialogflow_client.create_intent(
    display_name="NewIntent",
    training_phrases_parts=["new phrase", "another phrase"],
    message_texts=["This is a new intent"]
)
print("Created Intent:", new_intent)
```

### `delete_intent`

**Назначение**: Удаляет интент из проекта Dialogflow по его ID.

**Параметры**:
- `intent_id` (str): ID интента, который необходимо удалить.

**Возвращает**:
- `None`.

**Вызывает исключения**:
- `google.api_core.exceptions.ApiException`: В случае ошибок при вызове Dialogflow API.

**Как работает функция**:

1. **Формирование запроса**: Создается запрос к Dialogflow API для удаления интента с указанным ID.
2. **Отправка запроса**: Запрос отправляется к Dialogflow API.
3. **Обработка ответа**: Полученный ответ от Dialogflow API обрабатывается.

```
Формирование запроса --> Отправка запроса --> Обработка ответа
```

**Примеры**:
```python
from src.ai.dialogflow import Dialogflow

project_id = "your-project-id"
session_id = "unique-session-id"

dialogflow_client = Dialogflow(project_id, session_id)
# dialogflow_client.delete_intent("your-intent-id")