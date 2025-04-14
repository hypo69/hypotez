# Модуль OIVSCode

## Обзор

Модуль `OIVSCode` предоставляет класс `OIVSCode`, который является специализированной реализацией `OpenaiTemplate` для взаимодействия с сервером OI VSCode. Этот модуль определяет URL-адреса, модели и другие параметры, специфичные для данного провайдера.

## Подробней

Модуль предназначен для упрощения интеграции с сервером OI VSCode в контексте проекта `hypotez`. Он определяет базовые настройки, такие как URL-адрес API, поддерживаемые модели и флаги, указывающие на поддержку потоковой передачи, системных сообщений и истории сообщений.

## Классы

### `OIVSCode`

**Описание**: Класс `OIVSCode` наследует `OpenaiTemplate` и предоставляет конфигурацию для взаимодействия с сервером OI VSCode.

**Наследует**:
- `OpenaiTemplate`: Базовый класс для шаблонов OpenAI.

**Аттрибуты**:
- `label` (str): Метка провайдера ("OI VSCode Server").
- `url` (str): URL-адрес сервера ("https://oi-vscode-server.onrender.com").
- `api_base` (str): Базовый URL-адрес API ("https://oi-vscode-server-2.onrender.com/v1").
- `working` (bool): Флаг, указывающий, что провайдер работает (True).
- `needs_auth` (bool): Флаг, указывающий, что провайдер не требует аутентификации (False).
- `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи (True).
- `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений (True).
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений (True).
- `default_model` (str): Модель, используемая по умолчанию ("gpt-4o-mini-2024-07-18").
- `default_vision_model` (str): Модель для работы с изображениями, используемая по умолчанию (совпадает с `default_model`).
- `vision_models` (List[str]): Список моделей, поддерживающих работу с изображениями.
- `models` (List[str]): Список всех поддерживаемых моделей.
- `model_aliases` (Dict[str, str]): Словарь псевдонимов моделей.

## Функции

В данном классе функции отсутствуют

**Принцип работы**:

Класс `OIVSCode` используется для настройки параметров, необходимых для взаимодействия с сервером OI VSCode. Он определяет URL-адреса, модели и другие параметры, специфичные для данного провайдера.

**Примеры**:

```python
from .template import OpenaiTemplate

class OIVSCode(OpenaiTemplate):
    label = "OI VSCode Server"
    url = "https://oi-vscode-server.onrender.com"
    api_base = "https://oi-vscode-server-2.onrender.com/v1"

    working = True
    needs_auth = False
    supports_stream = True
    supports_system_message = True
    supports_message_history = True

    default_model = "gpt-4o-mini-2024-07-18"
    default_vision_model = default_model
    vision_models = [default_model, "gpt-4o-mini"]
    models = vision_models + ["deepseek-ai/DeepSeek-V3"]

    model_aliases = {
        "gpt-4o-mini": "gpt-4o-mini-2024-07-18",
        "deepseek-v3": "deepseek-ai/DeepSeek-V3"
    }