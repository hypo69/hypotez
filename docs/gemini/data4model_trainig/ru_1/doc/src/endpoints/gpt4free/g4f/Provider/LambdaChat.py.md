# Модуль LambdaChat

## Обзор

Модуль `LambdaChat` предоставляет класс для взаимодействия с чат-моделью Lambda Chat, используя функциональность, унаследованную от класса `HuggingChat`. Он определяет параметры подключения, модели и другие настройки, специфичные для Lambda Chat.

## Подробней

Модуль определяет класс `LambdaChat`, который наследуется от `HuggingChat` и специализируется на работе с сервисом Lambda Chat. Он задает домен, URL, список моделей и другие параметры, необходимые для установления соединения и взаимодействия с чат-сервисом. Класс также включает в себя алиасы для моделей, что упрощает их использование.

## Классы

### `LambdaChat`

**Описание**: Класс для взаимодействия с чат-моделью Lambda Chat.

**Наследует**:
- `HuggingChat`: Наследует функциональность для взаимодействия с чат-моделями Hugging Face.

**Атрибуты**:
- `label` (str): Метка провайдера "Lambda Chat".
- `domain` (str): Доменное имя сервиса "lambda.chat".
- `origin` (str): Полный URL домена сервиса "https://lambda.chat".
- `url` (str): URL сервиса, совпадающий с `origin`.
- `working` (bool): Указывает, что провайдер в рабочем состоянии (`True`).
- `use_nodriver` (bool): Указывает на отсутствие необходимости в использовании веб-драйвера (`False`).
- `needs_auth` (bool): Указывает, что не требуется аутентификация (`False`).
- `default_model` (str): Модель, используемая по умолчанию, `"deepseek-llama3.3-70b"`.
- `reasoning_model` (str): Модель для логических рассуждений, `"deepseek-r1"`.
- `image_models` (list): Список моделей для работы с изображениями (пустой список).
- `fallback_models` (list): Список моделей, используемых в качестве запасных вариантов.
- `models` (list): Список доступных моделей, инициализируется как копия `fallback_models`.
- `model_aliases` (dict): Словарь с алиасами для моделей, упрощающий их использование.

**Принцип работы**:
Класс `LambdaChat` использует атрибуты для настройки соединения с сервисом Lambda Chat. Атрибуты, такие как `domain`, `origin` и `url`, определяют адрес сервиса. Списки `fallback_models` и `models` содержат доступные модели, а `model_aliases` предоставляет удобные псевдонимы для их выбора. Наследование от `HuggingChat` позволяет использовать общую логику для взаимодействия с чат-моделями.

## Методы класса

В классе `LambdaChat` явно не определены методы, помимо унаследованных от `HuggingChat`. Однако используются атрибуты класса.

## Параметры класса

- `label`: Метка, идентифицирующая провайдера как "Lambda Chat".
- `domain`: Доменное имя сервиса Lambda Chat.
- `origin`: URL, с которого происходит взаимодействие с сервисом.
- `url`: URL сервиса Lambda Chat.
- `working`: Флаг, указывающий на работоспособность провайдера.
- `use_nodriver`: Флаг, указывающий на использование или неиспользование веб-драйвера.
- `needs_auth`: Флаг, указывающий на необходимость аутентификации.
- `default_model`: Наименование модели, используемой по умолчанию.
- `reasoning_model`: Наименование модели, используемой для рассуждений.
- `image_models`: Список моделей, поддерживающих работу с изображениями.
- `fallback_models`: Список запасных моделей для использования.
- `models`: Список доступных моделей для использования.
- `model_aliases`: Словарь, содержащий псевдонимы для упрощения выбора моделей.

**Примеры**:

```python
from .hf.HuggingChat import HuggingChat

class LambdaChat(HuggingChat):
    label = "Lambda Chat"
    domain = "lambda.chat"
    origin = f"https://{domain}"
    url = origin
    working = True
    use_nodriver = False
    needs_auth = False

    default_model = "deepseek-llama3.3-70b"
    reasoning_model = "deepseek-r1"
    image_models = []
    fallback_models = [
        default_model,
        reasoning_model,
        "hermes-3-llama-3.1-405b-fp8",
        "llama3.1-nemotron-70b-instruct",
        "lfm-40b",
        "llama3.3-70b-instruct-fp8"
    ]
    models = fallback_models.copy()
    
    model_aliases = {
        "deepseek-v3": default_model,
        "hermes-3": "hermes-3-llama-3.1-405b-fp8",
        "nemotron-70b": "llama3.1-nemotron-70b-instruct",
        "llama-3.3-70b": "llama3.3-70b-instruct-fp8"
    }