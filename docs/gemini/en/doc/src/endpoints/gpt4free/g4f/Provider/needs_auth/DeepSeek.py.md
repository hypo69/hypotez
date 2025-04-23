# Документация для модуля DeepSeek

## Обзор

Модуль `DeepSeek` предназначен для работы с API DeepSeek, предоставляя возможности для взаимодействия с моделью `deepseek-chat`. Он наследуется от класса `OpenaiAPI` и реализует специфические настройки для аутентификации и взаимодействия с API DeepSeek.

## Детали

Этот модуль предоставляет класс `DeepSeek`, который упрощает использование API DeepSeek для генерации текста и других задач, поддерживаемых моделью `deepseek-chat`. Он включает в себя поддержку потоковой передачи данных, истории сообщений и требует аутентификации для доступа к API.

## Классы

### `DeepSeek`

**Описание**: Класс для взаимодействия с API DeepSeek.

**Наследует**:
- `OpenaiAPI`: Наследует функциональность для работы с API OpenAI.

**Атрибуты**:
- `label` (str): Метка для идентификации провайдера, значение "DeepSeek".
- `url` (str): URL платформы DeepSeek.
- `login_url` (str): URL для получения ключей API DeepSeek.
- `working` (bool): Флаг, указывающий на работоспособность провайдера, значение `True`.
- `api_base` (str): Базовый URL для API DeepSeek.
- `needs_auth` (bool): Флаг, указывающий на необходимость аутентификации, значение `True`.
- `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи данных, значение `True`.
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений, значение `True`.
- `default_model` (str): Модель, используемая по умолчанию, значение "deepseek-chat".
- `fallback_models` (list[str]): Список моделей для переключения в случае проблем с основной моделью.

**Принцип работы**:
Класс `DeepSeek` наследует от `OpenaiAPI`, что позволяет ему использовать общую логику для взаимодействия с API OpenAI. Он переопределяет некоторые атрибуты, чтобы соответствовать спецификации API DeepSeek, такие как URL, необходимость аутентификации и модель по умолчанию. Это позволяет пользователям легко взаимодействовать с API DeepSeek, используя тот же интерфейс, что и для других API, совместимых с OpenAI.

## Методы класса

В данном коде не предоставляются методы класса, поскольку класс `DeepSeek` в основном переопределяет атрибуты для настройки подключения к API DeepSeek. Однако, поскольку он наследуется от `OpenaiAPI`, он может использовать методы, предоставляемые `OpenaiAPI`.

## Параметры класса

- `label` (str): Метка для идентификации провайдера.
- `url` (str): URL платформы DeepSeek.
- `login_url` (str): URL для получения ключей API DeepSeek.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `api_base` (str): Базовый URL для API DeepSeek.
- `needs_auth` (bool): Флаг, указывающий на необходимость аутентификации.
- `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи данных.
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений.
- `default_model` (str): Модель, используемая по умолчанию.
- `fallback_models` (list[str]): Список моделей для переключения в случае проблем с основной моделью.

**Примеры**
```python
from __future__ import annotations

from .OpenaiAPI import OpenaiAPI

class DeepSeek(OpenaiAPI):
    label = "DeepSeek"
    url = "https://platform.deepseek.com"
    login_url = "https://platform.deepseek.com/api_keys"
    working = True
    api_base = "https://api.deepseek.com"
    needs_auth = True
    supports_stream = True
    supports_message_history = True
    default_model = "deepseek-chat"
    fallback_models = [default_model]