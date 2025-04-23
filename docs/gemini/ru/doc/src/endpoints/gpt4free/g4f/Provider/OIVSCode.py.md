# Документация для модуля `OIVSCode`

## Обзор

Модуль `OIVSCode` предоставляет класс `OIVSCode`, который является подклассом `OpenaiTemplate` и предназначен для взаимодействия с сервером OI VSCode. Этот класс содержит настройки и параметры, специфичные для данного провайдера, такие как URL, API base, поддерживаемые модели и их псевдонимы.

## Подробней

Модуль определяет класс, который наследует функциональность шаблона OpenAI и специализирует его для работы с сервером OI VSCode. Это позволяет легко интегрировать и использовать модели, предоставляемые этим сервером, в рамках проекта `hypotez`.

## Классы

### `OIVSCode`

**Описание**: Класс `OIVSCode` является подклассом `OpenaiTemplate` и предоставляет настройки и параметры для взаимодействия с сервером OI VSCode.

**Наследует**: `OpenaiTemplate`

**Атрибуты**:
- `label` (str): Метка провайдера ("OI VSCode Server").
- `url` (str): URL сервера ("https://oi-vscode-server.onrender.com").
- `api_base` (str): Базовый URL API ("https://oi-vscode-server-2.onrender.com/v1").
- `working` (bool): Указывает, работает ли провайдер (True).
- `needs_auth` (bool): Указывает, требуется ли аутентификация (False).
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу (True).
- `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения (True).
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений (True).
- `default_model` (str): Модель по умолчанию ("gpt-4o-mini-2024-07-18").
- `default_vision_model` (str): Модель для обработки изображений по умолчанию (совпадает с `default_model`).
- `vision_models` (List[str]): Список моделей для обработки изображений.
- `models` (List[str]): Список всех поддерживаемых моделей.
- `model_aliases` (Dict[str, str]): Словарь псевдонимов моделей.

**Принцип работы**:

Класс `OIVSCode` определяет основные параметры для взаимодействия с сервером OI VSCode. Он устанавливает URL, API base, а также списки поддерживаемых моделей и их псевдонимы. Это позволяет унифицировать доступ к различным моделям через единый интерфейс, предоставляемый `OpenaiTemplate`. Класс также указывает, что не требуется аутентификация и поддерживаются потоковая передача, системные сообщения и история сообщений.

## Методы класса

В данном классе нет явно определенных методов, но он наследует методы от класса `OpenaiTemplate`.

## Параметры класса

- `label` (str): Метка провайдера, используемая для идентификации.
- `url` (str): URL сервера OI VSCode.
- `api_base` (str): Базовый URL API для взаимодействия с сервером.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `needs_auth` (bool): Флаг, указывающий на необходимость аутентификации.
- `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи.
- `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений.
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений.
- `default_model` (str): Модель, используемая по умолчанию, если не указана другая.
- `default_vision_model` (str): Модель для обработки изображений, используемая по умолчанию.
- `vision_models` (List[str]): Список поддерживаемых моделей для обработки изображений.
- `models` (List[str]): Полный список поддерживаемых моделей.
- `model_aliases` (Dict[str, str]): Словарь, сопоставляющий псевдонимы моделей с их полными именами.

**Примеры**
```python
from __future__ import annotations

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
```
В данном примере класс `OIVSCode` наследуется от `OpenaiTemplate` и конфигурируется для работы с сервером OI VSCode. Устанавливаются различные параметры, такие как URL, API base, поддерживаемые модели и их псевдонимы. Это позволяет использовать модели, предоставляемые сервером OI VSCode, через интерфейс `OpenaiTemplate`.