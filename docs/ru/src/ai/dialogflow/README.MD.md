# Документация модуля `src.ai.dialogflow`

## Обзор

Этот модуль предназначен для интеграции с платформой Dialogflow и предоставляет инструменты для создания разговорных AI-приложений. Он включает в себя функции определения намерений пользователя, извлечения сущностей, управления контекстом диалога и интеграции с различными платформами.

## Подробней

Модуль `src.ai.dialogflow` предоставляет возможности интеграции с Dialogflow, платформой для разработки разговорных интерфейсов. Он позволяет создавать AI-приложения, способные понимать естественный язык, извлекать ключевую информацию из фраз пользователя и поддерживать контекст в диалоге. Модуль поддерживает интеграцию с различными платформами, такими как Google Assistant, Facebook Messenger, Slack и Telegram, а также позволяет использовать webhook для взаимодействия с внешними сервисами и API.

## Функциональность

- **Определение намерений (Intent Detection):** Позволяет определять намерения пользователя на основе введенного текста.
- **Распознавание сущностей (Entity Recognition):** Извлекает ключевые данные из фраз пользователя.
- **Контексты (Contexts):** Управляет диалогом, сохраняя информацию о текущем состоянии разговора.
- **Интеграции (Integrations):** Поддерживает интеграцию с различными платформами, такими как Google Assistant, Facebook Messenger, Slack, Telegram и другие.
- **Webhook:** Поддерживает интеграцию с Webhook для вызова внешних сервисов и API.

## Классы

### `Dialogflow`

**Описание**: Класс `Dialogflow` предназначен для взаимодействия с API Dialogflow. Он позволяет определять намерения пользователя, извлекать сущности, управлять контекстами и интегрироваться с различными платформами.

**Принцип работы**:

1.  **Инициализация**: При инициализации класса `Dialogflow` необходимо указать идентификатор проекта Dialogflow и идентификатор сессии.
2.  **Определение намерений**: Метод `detect_intent` используется для определения намерения пользователя на основе введенного текста.
3.  **Управление намерениями**: Методы `list_intents`, `create_intent` и `delete_intent` позволяют управлять намерениями в проекте Dialogflow.

**Методы**:

*   `__init__`: Инициализирует клиент Dialogflow.
*   `detect_intent`: Определяет намерение пользователя на основе введенного текста.
*   `list_intents`: Возвращает список всех намерений в проекте Dialogflow.
*   `create_intent`: Создает новое намерение в проекте Dialogflow.
*   `delete_intent`: Удаляет указанное намерение из проекта Dialogflow.

## Функции

### `detect_intent`

```python
def detect_intent(self, text: str, language_code: str = "ru") -> str:
    """Определение намерения пользователя на основе текста
    Args:
        text (str): Текст запроса пользователя.
        language_code (str): Язык запроса. По умолчанию "ru".

    Returns:
        str: Ответ Dialogflow.

    Raises:
        Exception: В случае ошибки при взаимодействии с API Dialogflow.

    Example:
        >>> dialogflow_client = Dialogflow(project_id, session_id)
        >>> dialogflow_client.detect_intent("Привет")
        'Привет! Как я могу помочь?'
    """
```

**Назначение**: Функция `detect_intent` определяет намерение пользователя на основе введенного текста, используя API Dialogflow.

**Параметры**:

*   `text` (str): Текст запроса пользователя.
*   `language_code` (str): Язык запроса. По умолчанию "ru".

**Возвращает**:

*   `str`: Ответ Dialogflow.

**Вызывает исключения**:

*   `Exception`: В случае ошибки при взаимодействии с API Dialogflow.

**Как работает функция**:

1.  Функция принимает текст запроса пользователя и язык запроса.
2.  Формирует запрос к API Dialogflow для определения намерения пользователя.
3.  Получает ответ от API Dialogflow и возвращает его.

**ASII flowchart**:

```
Запрос пользователя (text)
    ↓
Формирование запроса к API Dialogflow
    ↓
Отправка запроса к API Dialogflow
    ↓
Получение ответа от API Dialogflow
    ↓
Возврат ответа Dialogflow
```

**Примеры**:

```python
dialogflow_client = Dialogflow(project_id, session_id)
response = dialogflow_client.detect_intent("Привет")
print(response)  # Вывод: 'Привет! Как я могу помочь?'
```

### `list_intents`

```python
def list_intents(self) -> list:
    """Получение списка всех намерений в Dialogflow
    Returns:
        list: Список объектов Intent.

    Raises:
        Exception: В случае ошибки при взаимодействии с API Dialogflow.

    Example:
        >>> dialogflow_client = Dialogflow(project_id, session_id)
        >>> dialogflow_client.list_intents()
        [<Intent object>, <Intent object>, ...]
    """
```

**Назначение**: Функция `list_intents` получает список всех намерений в проекте Dialogflow.

**Возвращает**:

*   `list`: Список объектов Intent.

**Вызывает исключения**:

*   `Exception`: В случае ошибки при взаимодействии с API Dialogflow.

**Как работает функция**:

1.  Функция формирует запрос к API Dialogflow для получения списка всех намерений.
2.  Получает ответ от API Dialogflow, содержащий список намерений.
3.  Возвращает список объектов Intent.

**ASII flowchart**:

```
Формирование запроса к API Dialogflow
    ↓
Отправка запроса к API Dialogflow
    ↓
Получение ответа от API Dialogflow
    ↓
Возврат списка Intent объектов
```

**Примеры**:

```python
dialogflow_client = Dialogflow(project_id, session_id)
intents = dialogflow_client.list_intents()
print(intents)  # Вывод: [<Intent object>, <Intent object>, ...]
```

### `create_intent`

```python
def create_intent(self, display_name: str, training_phrases_parts: list, message_texts: list) -> object:
    """Создание нового намерения в Dialogflow
    Args:
        display_name (str): Отображаемое имя намерения.
        training_phrases_parts (list): Список фраз для обучения.
        message_texts (list): Список текстовых сообщений для ответа.

    Returns:
        object: Объект Intent.

    Raises:
        Exception: В случае ошибки при взаимодействии с API Dialogflow.

    Example:
        >>> dialogflow_client = Dialogflow(project_id, session_id)
        >>> dialogflow_client.create_intent("NewIntent", ["Привет", "Здравствуйте"], ["Привет! Как я могу помочь?"])
        <Intent object>
    """
```

**Назначение**: Функция `create_intent` создает новое намерение в проекте Dialogflow.

**Параметры**:

*   `display_name` (str): Отображаемое имя намерения.
*   `training_phrases_parts` (list): Список фраз для обучения.
*   `message_texts` (list): Список текстовых сообщений для ответа.

**Возвращает**:

*   `object`: Объект Intent.

**Вызывает исключения**:

*   `Exception`: В случае ошибки при взаимодействии с API Dialogflow.

**Как работает функция**:

1.  Функция принимает отображаемое имя намерения, список фраз для обучения и список текстовых сообщений для ответа.
2.  Формирует запрос к API Dialogflow для создания нового намерения.
3.  Получает ответ от API Dialogflow, содержащий созданный объект Intent.
4.  Возвращает объект Intent.

**ASII flowchart**:

```
Входные параметры (display_name, training_phrases_parts, message_texts)
    ↓
Формирование запроса к API Dialogflow
    ↓
Отправка запроса к API Dialogflow
    ↓
Получение ответа от API Dialogflow
    ↓
Возврат объекта Intent
```

**Примеры**:

```python
dialogflow_client = Dialogflow(project_id, session_id)
intent = dialogflow_client.create_intent("NewIntent", ["Привет", "Здравствуйте"], ["Привет! Как я могу помочь?"])
print(intent)  # Вывод: <Intent object>
```

### `delete_intent`

```python
def delete_intent(self, intent_id: str) -> None:
    """Удаление намерения из Dialogflow
    Args:
        intent_id (str): ID намерения, которое нужно удалить.

    Raises:
        Exception: В случае ошибки при взаимодействии с API Dialogflow.

    Example:
        >>> dialogflow_client = Dialogflow(project_id, session_id)
        >>> dialogflow_client.delete_intent("intent_id")
    """
```

**Назначение**: Функция `delete_intent` удаляет указанное намерение из проекта Dialogflow.

**Параметры**:

*   `intent_id` (str): ID намерения, которое нужно удалить.

**Возвращает**:

*   `None`: Функция ничего не возвращает.

**Вызывает исключения**:

*   `Exception`: В случае ошибки при взаимодействии с API Dialogflow.

**Как работает функция**:

1.  Функция принимает ID намерения, которое нужно удалить.
2.  Формирует запрос к API Dialogflow для удаления намерения.
3.  Отправляет запрос к API Dialogflow.

**ASII flowchart**:

```
Входной параметр (intent_id)
    ↓
Формирование запроса к API Dialogflow
    ↓
Отправка запроса к API Dialogflow
```

**Примеры**:

```python
dialogflow_client = Dialogflow(project_id, session_id)
dialogflow_client.delete_intent("intent_id")