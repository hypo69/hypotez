# Документация для `ThebApi.py`

## Обзор

Файл `ThebApi.py` является частью проекта `hypotez` и содержит класс `ThebApi`, который предоставляет интерфейс для взаимодействия с API TheB.AI. Этот класс наследуется от `OpenaiTemplate` и предназначен для генерации текста на основе различных моделей, поддерживаемых TheB.AI.

## Более подробно

В файле определены модели, поддерживаемые TheB.AI, такие как "theb-ai", "gpt-3.5-turbo", "gpt-4" и другие. Класс `ThebApi` предоставляет методы для создания асинхронных генераторов текста с использованием этих моделей. Класс требует аутентификации для работы.

## Классы

### `ThebApi`

**Описание**: Класс `ThebApi` предоставляет интерфейс для взаимодействия с API TheB.AI.

**Наследует**:
- `OpenaiTemplate`: Этот класс наследует функциональность шаблона OpenAI, что позволяет использовать общие методы и атрибуты для взаимодействия с API.

**Атрибуты**:
- `label` (str): Метка для API ("TheB.AI API").
- `url` (str): URL для API ("https://theb.ai").
- `login_url` (str): URL для входа в систему ("https://beta.theb.ai/home").
- `api_base` (str): Базовый URL для API ("https://api.theb.ai/v1").
- `working` (bool): Указывает, работает ли API (True).
- `needs_auth` (bool): Указывает, требуется ли аутентификация (True).
- `default_model` (str): Модель по умолчанию ("theb-ai").
- `fallback_models` (list): Список запасных моделей.

**Принцип работы**:
Класс `ThebApi` предназначен для упрощения взаимодействия с API TheB.AI. Он наследует функциональность от `OpenaiTemplate`, что позволяет использовать общие методы для создания запросов и обработки ответов. Класс также определяет атрибуты, специфичные для API TheB.AI, такие как URL, базовый URL API и модель по умолчанию.

## Методы класса

### `create_async_generator`

```python
@classmethod
def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    temperature: float = None,
    top_p: float = None,
    **kwargs
) -> CreateResult:
    """
    Создает асинхронный генератор для генерации текста с использованием API TheB.AI.

    Args:
        cls (ThebApi): Класс ThebApi.
        model (str): Название модели для использования.
        messages (Messages): Список сообщений для передачи в API.
        temperature (float, optional): Температура генерации. По умолчанию `None`.
        top_p (float, optional): Значение top_p. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        CreateResult: Результат создания генератора.

    Как работает функция:
    - Извлекает системные сообщения из списка сообщений.
    - Фильтрует сообщения, чтобы оставить только те, которые не являются системными.
    - Создает словарь `data` с параметрами модели, такими как `system_prompt`, `temperature` и `top_p`.
    - Вызывает метод `create_async_generator` родительского класса `OpenaiTemplate` для создания генератора.
    """
    system_message = "\n".join([message["content"] for message in messages if message["role"] == "system"])
    messages = [message for message in messages if message["role"] != "system"]
    data = {
        "model_params": filter_none(
            system_prompt=system_message,
            temperature=temperature,
            top_p=top_p,
        )
    }
    return super().create_async_generator(model, messages, extra_data=data, **kwargs)
```

## Параметры класса

- `cls` (ThebApi): Класс ThebApi.
- `model` (str): Название модели для использования.
- `messages` (Messages): Список сообщений для передачи в API.
- `temperature` (float, optional): Температура генерации. По умолчанию `None`.
- `top_p` (float, optional): Значение top_p. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Примеры**:

Пример вызова функции `create_async_generator`:

```python
from src.endpoints.gpt4free.g4f.Provider.needs_auth.ThebApi import ThebApi
from src.endpoints.gpt4free.g4f.typing import Messages

messages: Messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"}
]

result = ThebApi.create_async_generator(
    model="theb-ai",
    messages=messages,
    temperature=0.7,
    top_p=0.9
)

print(result)