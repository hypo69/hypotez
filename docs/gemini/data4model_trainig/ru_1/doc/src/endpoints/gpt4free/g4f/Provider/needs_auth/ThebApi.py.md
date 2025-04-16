# Модуль ThebApi для работы с API TheB.AI
## Обзор

Модуль `ThebApi.py` предоставляет класс `ThebApi`, который используется для взаимодействия с API TheB.AI. Этот класс наследуется от `OpenaiTemplate` и предназначен для создания асинхронных генераторов для получения ответов от различных моделей, поддерживаемых TheB.AI. Модуль содержит информацию о поддерживаемых моделях и базовые URL для доступа к API.

## Подробней

Модуль содержит словарь `models`, который определяет соответствие между идентификаторами моделей и их отображаемыми именами. Класс `ThebApi` определяет основные параметры для работы с API TheB.AI, такие как базовый URL, необходимость аутентификации и модели по умолчанию.

## Классы

### `ThebApi`

**Описание**: Класс `ThebApi` предназначен для взаимодействия с API TheB.AI. Он наследует функциональность от `OpenaiTemplate` и предоставляет методы для создания асинхронных генераторов для получения ответов от различных моделей.

**Наследует**:

- `OpenaiTemplate`: Класс, предоставляющий базовую функциональность для работы с API, совместимыми с OpenAI.

**Атрибуты**:

- `label` (str): Метка для API ("TheB.AI API").
- `url` (str): URL главной страницы TheB.AI ("https://theb.ai").
- `login_url` (str): URL страницы входа ("https://beta.theb.ai/home").
- `api_base` (str): Базовый URL для API ("https://api.theb.ai/v1").
- `working` (bool): Указывает, работает ли API (True).
- `needs_auth` (bool): Указывает, требуется ли аутентификация (True).
- `default_model` (str): Модель по умолчанию ("theb-ai").
- `fallback_models` (list): Список моделей, которые можно использовать в качестве запасных.

**Принцип работы**:
Класс `ThebApi` использует `OpenaiTemplate` для создания запросов к API TheB.AI. Он переопределяет метод `create_async_generator` для адаптации формата запроса к требованиям TheB.AI, включая передачу системных сообщений и других параметров модели.

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
    Создает асинхронный генератор для получения ответов от API TheB.AI.

    Args:
        model (str): Идентификатор модели для использования.
        messages (Messages): Список сообщений для отправки в API.
        temperature (float, optional): Температура для генерации текста. По умолчанию `None`.
        top_p (float, optional): Значение top_p для генерации текста. По умолчанию `None`.
        **kwargs: Дополнительные параметры для передачи в API.

    Returns:
        CreateResult: Результат создания асинхронного генератора.

    Как работает функция:
    1. Извлекает системные сообщения из списка сообщений и объединяет их в строку `system_message`.
    2. Фильтрует сообщения, удаляя системные сообщения, оставляя только сообщения пользователя и ассистента.
    3. Формирует словарь `data` с параметрами модели, включая `system_prompt`, `temperature` и `top_p`, используя функцию `filter_none` для удаления параметров со значением `None`.
    4. Вызывает метод `create_async_generator` родительского класса `OpenaiTemplate` с передачей сформированных данных.

    Примеры:
    # Пример вызова функции create_async_generator с минимальными параметрами
    ThebApi.create_async_generator(model="theb-ai", messages=[{"role": "user", "content": "Hello"}])

    # Пример вызова функции create_async_generator с указанием температуры и top_p
    ThebApi.create_async_generator(model="theb-ai", messages=[{"role": "user", "content": "Hello"}], temperature=0.7, top_p=0.9)
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

- `label` (str): Метка для API.
- `url` (str): URL главной страницы TheB.AI.
- `login_url` (str): URL страницы входа.
- `api_base` (str): Базовый URL для API.
- `working` (bool): Указывает, работает ли API.
- `needs_auth` (bool): Указывает, требуется ли аутентификация.
- `default_model` (str): Модель по умолчанию.
- `fallback_models` (list): Список моделей, которые можно использовать в качестве запасных.

## Параметры функции `create_async_generator`

- `model` (str): Идентификатор модели для использования.
- `messages` (Messages): Список сообщений для отправки в API.
- `temperature` (float, optional): Температура для генерации текста. По умолчанию `None`.
- `top_p` (float, optional): Значение top_p для генерации текста. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры для передачи в API.