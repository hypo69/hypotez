# Module OIVSCode

## Обзор

Модуль `OIVSCode` является частью проекта `hypotez` и предоставляет класс `OIVSCode`, который наследуется от `OpenaiTemplate`. Он предназначен для взаимодействия с сервером OI VSCode и предоставляет конфигурацию для работы с моделями OpenAI, такими как GPT-4o-mini и DeepSeek-V3. Модуль определяет базовые URL, поддерживает потоковую передачу, системные сообщения и историю сообщений.

## Подробнее

Модуль содержит настройки для подключения к серверу OI VSCode, включая URL, базовый API, а также списки поддерживаемых моделей. Он также определяет псевдонимы моделей для удобства использования.

## Классы

### `OIVSCode`

**Описание**: Класс `OIVSCode` наследуется от `OpenaiTemplate` и предоставляет конфигурацию для взаимодействия с сервером OI VSCode.

**Наследует**:
- `OpenaiTemplate`: Класс, предоставляющий базовый шаблон для работы с OpenAI.

**Атрибуты**:
- `label` (str): Метка провайдера, в данном случае "OI VSCode Server".
- `url` (str): URL сервера OI VSCode.
- `api_base` (str): Базовый URL API сервера OI VSCode.
- `working` (bool): Указывает, работает ли провайдер (в данном случае `True`).
- `needs_auth` (bool): Указывает, требуется ли аутентификация (в данном случае `False`).
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу (в данном случае `True`).
- `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения (в данном случае `True`).
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений (в данном случае `True`).
- `default_model` (str): Модель по умолчанию, используемая провайдером ("gpt-4o-mini-2024-07-18").
- `default_vision_model` (str): Модель для работы с изображениями по умолчанию, совпадает с `default_model`.
- `vision_models` (List[str]): Список поддерживаемых моделей для работы с изображениями.
- `models` (List[str]): Список всех поддерживаемых моделей.
- `model_aliases` (Dict[str, str]): Словарь псевдонимов моделей для удобства использования.

**Принцип работы**:

Класс `OIVSCode` предоставляет конфигурацию, необходимую для подключения и взаимодействия с сервером OI VSCode. Он определяет URL, поддерживает потоковую передачу, системные сообщения и историю сообщений. Также определяет список поддерживаемых моделей и псевдонимы для удобства использования.

## Методы класса

В данном классе методы отсутствуют.

## Параметры класса

- `label` (str): Метка провайдера.
- `url` (str): URL сервера OI VSCode.
- `api_base` (str): Базовый URL API сервера OI VSCode.
- `working` (bool): Указывает, работает ли провайдер.
- `needs_auth` (bool): Указывает, требуется ли аутентификация.
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу.
- `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения.
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений.
- `default_model` (str): Модель по умолчанию.
- `default_vision_model` (str): Модель для работы с изображениями по умолчанию.
- `vision_models` (List[str]): Список поддерживаемых моделей для работы с изображениями.
- `models` (List[str]): Список всех поддерживаемых моделей.
- `model_aliases` (Dict[str, str]): Словарь псевдонимов моделей.

**Примеры**
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
```
```python
# Создание экземпляра класса OIVSCode
oivscode = OIVSCode()

# Получение URL сервера
url = oivscode.url
print(f"URL сервера: {url}")  # Вывод: URL сервера: https://oi-vscode-server.onrender.com

# Получение списка поддерживаемых моделей
models = oivscode.models
print(f"Поддерживаемые модели: {models}")  # Вывод: Поддерживаемые модели: ['gpt-4o-mini-2024-07-18', 'gpt-4o-mini', 'deepseek-ai/DeepSeek-V3']