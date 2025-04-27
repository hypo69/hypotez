# ChatGpt.py

## Обзор

Этот модуль содержит класс `ChatGpt`, который предоставляет интерфейс для взаимодействия с моделью ChatGPT от OpenAI.  

## Подробности

Этот модуль является частью проекта `hypotez` и используется для интеграции с  сервисом ChatGPT.  

## Классы

### `ChatGpt`

**Описание**: Класс `ChatGpt` реализует `AbstractProvider` и `ProviderModelMixin` для предоставления возможностей по работе с  ChatGPT.

**Inherits**:
- `AbstractProvider`:  Базовый класс для всех провайдеров, определяет общий интерфейс для работы с моделями AI.
- `ProviderModelMixin`:  Добавляет функциональность для работы с различными моделями AI.

**Attributes**:
- `label` (str):  Метка, используемая для идентификации провайдера.
- `url` (str):  Базовый URL провайдера.
- `working` (bool):  Флаг, указывающий на то, работает ли провайдер.
- `supports_message_history` (bool):  Указывает, поддерживает ли провайдер историю сообщений.
- `supports_system_message` (bool):  Указывает, поддерживает ли провайдер системные сообщения.
- `supports_stream` (bool):  Указывает, поддерживает ли провайдер потоковую передачу.
- `default_model` (str):  Модель по умолчанию, используемая провайдером.
- `models` (list):  Список доступных моделей.
- `model_aliases` (dict):  Словарь, содержащий псевдонимы моделей.

**Methods**:

- `get_model(model: str) -> str`:  Возвращает модель, соответствующую данному `model`, или `default_model` в случае отсутствия.
- `create_completion(model: str, messages: Messages, stream: bool, **kwargs) -> CreateResult`:  Создает ответ модели ChatGPT.

**Как работает метод `create_completion`**:

- Получает модель AI, список сообщений и флаг, указывающий на то, должна ли  передача ответа быть потоковой.
- Проверяет доступность модели.
- Инициализирует сессию с `init_session`.
- Получает конфигурационные данные и токен для проверки пользователя.
- Отправляет запрос на `chatgpt.com/backend-anon/sentinel/chat-requirements`, чтобы получить токен для  входа.
- Обрабатывает токен для проверки.
- Формирует запрос на `chatgpt.com/backend-anon/conversation`.
- Отправляет запрос и возвращает ответ модели.

**Пример**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.ChatGpt import ChatGpt

gpt = ChatGpt()
response = gpt.create_completion(model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': 'Hello'}], stream=False)
print(response)
```


## Функции

### `format_conversation(messages: list) -> list`:

**Purpose**: Форматирует список сообщений для передачи в API ChatGPT.

**Parameters**:
- `messages` (list):  Список сообщений.

**Returns**:
- `list`:  Список отформатированных сообщений.

**Как работает функция**:

- Создает список отформатированных сообщений, преобразуя исходные сообщения в формат, ожидаемый API ChatGPT.

### `init_session(user_agent: str) -> Session`:

**Purpose**: Инициализирует сессию для взаимодействия с API ChatGPT.

**Parameters**:
- `user_agent` (str):  Строка user-agent, используемая для идентификации браузера.

**Returns**:
- `Session`:  Объект `Session`, готовый для отправки запросов.

**Как работает функция**:

- Создает объект `Session` с соответствующими настройками, например, куки, заголовками, и отправляет тестовый запрос на `chatgpt.com`.

### `get_config(user_agent: str) -> dict`:

**Purpose**: Возвращает конфигурацию для API ChatGPT.

**Parameters**:
- `user_agent` (str):  Строка user-agent, используемая для идентификации браузера.

**Returns**:
- `dict`:  Словарь с конфигурационными данными для ChatGPT.

**Как работает функция**:

- Получает данные конфигурации из `openai.new.get_config`.

### `get_requirements_token(config: dict) -> str`:

**Purpose**: Возвращает токен для  входа в API ChatGPT.

**Parameters**:
- `config` (dict):  Конфигурационные данные.

**Returns**:
- `str`:  Токен для  входа.

**Как работает функция**:

- Получает токен из `openai.new.get_requirements_token`.

### `process_turnstile(turnstile_dx: str, pow_req: str) -> str`:

**Purpose**: Обрабатывает токен проверки.

**Parameters**:
- `turnstile_dx` (str):  Токен для проверки пользователя.
- `pow_req` (str):  Токен, используемый для получения данных.

**Returns**:
- `str`:  Токен проверки пользователя.

**Как работает функция**:

- Обрабатывает токен для проверки из `openai.new.process_turnstile`.

### `get_answer_token(seed: str, difficulty: str, config: dict) -> str`:

**Purpose**:  Получает токен для  ответа API ChatGPT.

**Parameters**:
- `seed` (str):  Ключ, используемый для генерации токена.
- `difficulty` (str):  Сложность проверки.
- `config` (dict):  Конфигурационные данные.

**Returns**:
- `str`:  Токен ответа.

**Как работает функция**:

- Получает токен ответа из `openai.new.get_answer_token`.