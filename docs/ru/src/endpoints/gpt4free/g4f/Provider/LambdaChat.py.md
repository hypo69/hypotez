# Модуль LambdaChat

## Обзор

Модуль `LambdaChat` предоставляет класс для взаимодействия с чат-моделью Lambda Chat. Он наследуется от класса `HuggingChat` и содержит специфические параметры и настройки для работы с этой моделью.

## Подробней

Этот модуль является частью проекта `hypotez` и предназначен для интеграции с различными AI-моделями для обработки текста. Он определяет параметры подключения и конфигурации для чат-модели `LambdaChat`, что позволяет использовать её в рамках фреймворка `hypotez`.

## Классы

### `LambdaChat`

**Описание**: Класс `LambdaChat` предназначен для взаимодействия с чат-моделью Lambda Chat.

**Наследует**:
- `HuggingChat`: Класс `LambdaChat` наследует функциональность от класса `HuggingChat`, расширяя его для работы с Lambda Chat.

**Атрибуты**:
- `label` (str): Метка для идентификации провайдера Lambda Chat ("Lambda Chat").
- `domain` (str): Доменное имя для Lambda Chat ("lambda.chat").
- `origin` (str): Полный URL для Lambda Chat ("https://lambda.chat").
- `url` (str): URL для Lambda Chat (совпадает с `origin`).
- `working` (bool): Указывает, является ли провайдер рабочим (`True`).
- `use_nodriver` (bool): Указывает, требуется ли использование драйвера (`False`).
- `needs_auth` (bool): Указывает, требуется ли аутентификация (`False`).
- `default_model` (str): Модель, используемая по умолчанию ("deepseek-llama3.3-70b").
- `reasoning_model` (str): Модель для рассуждений ("deepseek-r1").
- `image_models` (list): Список моделей для обработки изображений (пустой список `[]`).
- `fallback_models` (list): Список запасных моделей, используемых в случае недоступности основной модели.
- `models` (list): Копия списка `fallback_models`, представляющая доступные модели.
- `model_aliases` (dict): Словарь псевдонимов моделей, связывающий альтернативные имена моделей с их фактическими именами.

**Методы**:
- Нет специфических методов, описанных в предоставленном коде. Используются методы, унаследованные от `HuggingChat`.

## Функции

В данном коде нет отдельных функций, только определение класса `LambdaChat`. Класс использует атрибуты для настройки соединения и выбора моделей.
```python
    model_aliases = {
        "deepseek-v3": default_model,
        "hermes-3": "hermes-3-llama-3.1-405b-fp8",
        "nemotron-70b": "llama3.1-nemotron-70b-instruct",
        "llama-3.3-70b": "llama3.3-70b-instruct-fp8"
    }
```

### `model_aliases`

**Назначение**:
Словарь `model_aliases` содержит псевдонимы моделей, используемые для упрощения выбора и конфигурации моделей Lambda Chat. Он связывает альтернативные имена моделей с их фактическими именами, что позволяет пользователям указывать псевдонимы вместо полных имен моделей.

**Параметры**:
- Нет параметров, т.к. это словарь, а не функция

**Возвращает**:
-  Словарь, где ключи - это псевдонимы моделей (str), а значения - полные имена моделей (str)

**Вызывает исключения**:
-  Нет

**Как работает `model_aliases`**:
1.  **Определение псевдонимов**: `model_aliases` определен как словарь, где ключи представляют собой псевдонимы моделей, а значения - фактические имена моделей, используемые Lambda Chat.
2.  **Сопоставление псевдонимов с моделями**: При выборе модели по псевдониму происходит поиск соответствующего полного имени модели в словаре `model_aliases`.
3.  **Использование в конфигурации**: Псевдонимы используются для упрощения конфигурации и выбора моделей, позволяя пользователям указывать более короткие и понятные имена моделей.

**Примеры**:

```python
model_aliases = {
        "deepseek-v3": "deepseek-llama3.3-70b",
        "hermes-3": "hermes-3-llama-3.1-405b-fp8",
        "nemotron-70b": "llama3.1-nemotron-70b-instruct",
        "llama-3.3-70b": "llama3.3-70b-instruct-fp8"
    }
# Пример использования:
# Если пользователь укажет "deepseek-v3", будет использована модель "deepseek-llama3.3-70b"
```

### Пример определения класса `LambdaChat` и его атрибутов

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
```
В этом примере показано, как определяется класс `LambdaChat` с различными атрибутами, такими как `label`, `domain`, `default_model` и `model_aliases`, которые используются для настройки и идентификации провайдера Lambda Chat.