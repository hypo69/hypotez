# Документация для модуля `ThebApi.py`

## Обзор

Модуль `ThebApi.py` предназначен для взаимодействия с API сервиса TheB.AI. Он предоставляет класс `ThebApi`, который наследуется от `OpenaiTemplate` и реализует методы для создания асинхронных генераторов ответов от моделей TheB.AI. Модуль содержит информацию о поддерживаемых моделях, URL для доступа к API и необходимые настройки для аутентификации.

## Подробнее

Модуль определяет соответствия между именами моделей, используемыми в проекте `hypotez`, и именами, используемыми в API TheB.AI. Класс `ThebApi` предоставляет методы для аутентификации и создания запросов к API.

## Переменные модуля

- `models (dict)`: Словарь, сопоставляющий имена моделей в проекте `hypotez` с их представлениями в API TheB.AI.
    - `"theb-ai"`: `"TheB.AI"`
    - `"gpt-3.5-turbo"`: `"GPT-3.5"`
    - `"gpt-4-turbo"`: `"GPT-4 Turbo"`
    - `"gpt-4"`: `"GPT-4"`
    - `"claude-3.5-sonnet"`: `"Claude"`
    - `"llama-2-7b-chat"`: `"Llama 2 7B"`
    - `"llama-2-13b-chat"`: `"Llama 2 13B"`
    - `"llama-2-70b-chat"`: `"Llama 2 70B"`
    - `"code-llama-7b"`: `"Code Llama 7B"`
    - `"code-llama-13b"`: `"Code Llama 13B"`
    - `"code-llama-34b"`: `"Code Llama 34B"`
    - `"qwen-2-72b"`: `"Qwen"`

## Классы

### `ThebApi`

**Описание**: Класс для взаимодействия с API TheB.AI.

**Наследует**: `OpenaiTemplate`

**Атрибуты**:
- `label (str)`: Метка для API ("TheB.AI API").
- `url (str)`: URL для доступа к сервису ("https://theb.ai").
- `login_url (str)`: URL для входа в аккаунт ("https://beta.theb.ai/home").
- `api_base (str)`: Базовый URL для API ("https://api.theb.ai/v1").
- `working (bool)`: Указывает, что API в рабочем состоянии (`True`).
- `needs_auth (bool)`: Указывает, что для доступа к API требуется аутентификация (`True`).
- `default_model (str)`: Модель, используемая по умолчанию ("theb-ai").
- `fallback_models (list)`: Список моделей для переключения в случае неудачи с основной моделью.

**Методы**:
- `create_async_generator()`: Создает асинхронный генератор ответов от модели TheB.AI.

**Принцип работы**:

Класс `ThebApi` предоставляет интерфейс для взаимодействия с API TheB.AI. Он наследует функциональность от `OpenaiTemplate` и переопределяет метод `create_async_generator` для создания асинхронных генераторов, использующих API TheB.AI. Класс также определяет атрибуты, содержащие информацию о URL, необходимости аутентификации и поддерживаемых моделях.

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
    """Создает асинхронный генератор ответов от модели TheB.AI.

    Args:
        model (str): Имя модели для использования.
        messages (Messages): Список сообщений для отправки в API.
        temperature (float, optional): Параметр temperature для управления случайностью генерации. По умолчанию `None`.
        top_p (float, optional): Параметр top_p для управления разнообразием генерации. По умолчанию `None`.
        **kwargs: Дополнительные параметры.

    Returns:
        CreateResult: Результат создания асинхронного генератора.

    
    - Функция принимает имя модели, список сообщений и дополнительные параметры.
    - Извлекает системные сообщения из списка сообщений и объединяет их в строку `system_message`.
    - Оставляет в списке `messages` только те сообщения, у которых роль не "system".
    - Формирует словарь `data`, содержащий параметры модели, такие как `system_prompt`, `temperature` и `top_p`.
    - Вызывает метод `create_async_generator` из родительского класса `OpenaiTemplate`, передавая ему имя модели, список сообщений и дополнительные данные.

    Примеры:
        Пример вызова функции с разными параметрами:

        >>> ThebApi.create_async_generator(model="theb-ai", messages=[{"role": "user", "content": "Hello"}])
        <async_generator object create_async_generator at 0x...>

        >>> ThebApi.create_async_generator(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello"}], temperature=0.7, top_p=0.9)
        <async_generator object create_async_generator at 0x...>
    """
```
## Параметры класса

- `model (str)`: Имя модели для использования.
- `messages (Messages)`: Список сообщений для отправки в API.
- `temperature (float, optional)`: Параметр temperature для управления случайностью генерации. По умолчанию `None`.
- `top_p (float, optional)`: Параметр top_p для управления разнообразием генерации. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры.