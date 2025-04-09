# Модуль ThebApi

## Обзор

Модуль `ThebApi` представляет собой реализацию интерфейса для взаимодействия с API сервиса TheB.AI. Он наследует функциональность от класса `OpenaiTemplate` и предназначен для генерации ответов на основе предоставленных сообщений с использованием различных моделей, поддерживаемых TheB.AI. Модуль включает в себя определение поддерживаемых моделей, URL для доступа к API, а также методы для настройки и выполнения запросов к API TheB.AI.

## Подробнее

Модуль `ThebApi` является частью системы `gpt4free` в проекте `hypotez` и обеспечивает возможность использования моделей TheB.AI для генерации текста. Этот модуль предоставляет интерфейс, совместимый с OpenAI, что упрощает интеграцию с другими компонентами системы.

## Переменные модуля

- `models (dict)`: Словарь, содержащий соответствия между идентификаторами моделей, используемыми в `gpt4free`, и названиями моделей, используемыми в TheB.AI.
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

**Описание**: Класс `ThebApi` предназначен для взаимодействия с API TheB.AI. Он наследуется от класса `OpenaiTemplate` и предоставляет методы для создания запросов к API TheB.AI и получения ответов.

**Принцип работы**:
Класс `ThebApi` использует API TheB.AI для генерации ответов на основе предоставленных сообщений. Он преобразует сообщения в формат, ожидаемый API TheB.AI, и отправляет запрос на генерацию текста. Полученный ответ возвращается в формате, совместимом с OpenAI.

**Атрибуты**:
- `label (str)`: Метка, идентифицирующая провайдера TheB.AI API. Значение: `"TheB.AI API"`.
- `url (str)`: URL главной страницы TheB.AI. Значение: `"https://theb.ai"`.
- `login_url (str)`: URL страницы для входа в TheB.AI. Значение: `"https://beta.theb.ai/home"`.
- `api_base (str)`: Базовый URL для API TheB.AI. Значение: `"https://api.theb.ai/v1"`.
- `working (bool)`: Флаг, указывающий, что API TheB.AI в настоящее время работает. Значение: `True`.
- `needs_auth (bool)`: Флаг, указывающий, что для использования API TheB.AI требуется аутентификация. Значение: `True`.
- `default_model (str)`: Модель, используемая по умолчанию. Значение: `"theb-ai"`.
- `fallback_models (list)`: Список моделей, которые могут быть использованы в случае недоступности модели по умолчанию. Значение: `list(models)`.

**Методы**:

- `create_async_generator(model: str, messages: Messages, temperature: float = None, top_p: float = None, **kwargs) -> CreateResult`

## Функции

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
    """Создает асинхронный генератор для взаимодействия с API TheB.AI.

    Args:
        model (str): Идентификатор модели, используемой для генерации текста.
        messages (Messages): Список сообщений, используемых для генерации текста.
        temperature (float, optional): Температура генерации текста. По умолчанию `None`.
        top_p (float, optional): Значение Top-P для генерации текста. По умолчанию `None`.
        **kwargs: Дополнительные аргументы, передаваемые в функцию `super().create_async_generator()`.

    Returns:
        CreateResult: Результат создания асинхронного генератора.

    Как работает функция:
     1. Извлекает системные сообщения из списка `messages` и объединяет их в строку `system_message`.
     2. Фильтрует список `messages`, удаляя системные сообщения.
     3. Формирует словарь `data`, содержащий параметры модели, такие как `system_prompt`, `temperature` и `top_p`.
     4. Вызывает метод `create_async_generator` родительского класса `OpenaiTemplate` с передачей модели, сообщений и дополнительных данных.

    ASCII flowchart:

    Извлечение системных сообщений --> Фильтрация сообщений --> Формирование словаря data --> Вызов create_async_generator родительского класса
    A                         --> B                      --> C                      --> D

    Примеры:
        >>> ThebApi.create_async_generator(model="theb-ai", messages=[{"role": "user", "content": "Hello"}])
        <async_generator object OpenaiTemplate.create_async_generator at 0x...>
    """
    ...
```

**Назначение**: Создает асинхронный генератор для взаимодействия с API TheB.AI.

**Параметры**:
- `model` (str): Идентификатор модели, используемой для генерации текста.
- `messages` (Messages): Список сообщений, используемых для генерации текста.
- `temperature` (float, optional): Температура генерации текста. По умолчанию `None`.
- `top_p` (float, optional): Значение Top-P для генерации текста. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы, передаваемые в функцию `super().create_async_generator()`.

**Возвращает**:
- `CreateResult`: Результат создания асинхронного генератора.

**Как работает функция**:
1. **Извлечение системных сообщений**: Функция извлекает все сообщения с ролью "system" из списка сообщений и объединяет их в одну строку `system_message`.
2. **Фильтрация сообщений**:  Фильтрует `messages`, оставляя только те сообщения, у которых роль не "system".
3. **Формирование словаря `data`**: Формирует словарь `data`, который будет передан в API TheB.AI. В этот словарь включаются параметры модели, такие как `system_prompt`, `temperature` и `top_p`. Функция `filter_none` используется для удаления параметров со значением `None`.
4. **Вызов `super().create_async_generator`**: Вызывает метод `create_async_generator` родительского класса `OpenaiTemplate`, передавая ему модель, отфильтрованные сообщения и сформированный словарь `data`.

**ASCII flowchart**:

```
Извлечение системных сообщений (A)
    ↓
Фильтрация сообщений (B)
    ↓
Формирование словаря data (C)
    ↓
Вызов create_async_generator родительского класса (D)
```

**Примеры**:

```python
>>> ThebApi.create_async_generator(model="theb-ai", messages=[{"role": "user", "content": "Hello"}])
<async_generator object OpenaiTemplate.create_async_generator at 0x...>