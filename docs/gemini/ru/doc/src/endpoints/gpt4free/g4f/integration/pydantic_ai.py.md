# Документация модуля `pydantic_ai` для интеграции с `g4f`

## Обзор

Модуль предназначен для интеграции библиотеки `pydantic-ai` с API `g4f` (GPT4Free). Он позволяет использовать модели, доступные через `g4f`, в качестве моделей `pydantic-ai`, обеспечивая удобный интерфейс для работы с ними.

## Подробнее

Этот модуль расширяет возможности `pydantic-ai`, позволяя использовать модели `g4f` (GPT4Free). Он содержит класс `AIModel`, который представляет собой адаптацию модели OpenAI для работы с `g4f`, и функции для подмены стандартной функции `infer_model` из `pydantic-ai`, чтобы она могла распознавать и создавать экземпляры `AIModel` для моделей `g4f`.

## Классы

### `AIModel`

**Описание**: Класс `AIModel` представляет собой модель, использующую API `G4F`. Он наследует `OpenAIModel` и адаптирует его для работы с асинхронным клиентом `AsyncClient` из `g4f`.

**Наследует**: `OpenAIModel`

**Атрибуты**:

-   `client` (AsyncClient): Асинхронный клиент для взаимодействия с API `G4F`.
-   `system_prompt_role` (OpenAISystemPromptRole | None): Роль системного промпта, используемая для сообщений.
-   `_model_name` (str): Имя модели.
-   `_provider` (str): Провайдер модели.
-   `_system` (Optional[str]): Используемая система (по умолчанию 'openai').

**Методы**:

-   `__init__`: Инициализирует экземпляр класса `AIModel`.
-   `name`: Возвращает имя модели в формате `g4f:{provider}:{model_name}` или `g4f:{model_name}`, если провайдер не указан.

#### `__init__`

```python
def __init__(
    self,
    model_name: str,
    provider: str | None = None,
    *,
    system_prompt_role: OpenAISystemPromptRole | None = None,
    system: str | None = 'openai',
    **kwargs
) -> None:
    """
    Инициализирует AI модель.

    Args:
        model_name (str): Имя используемой AI модели. Список доступных имен моделей можно найти
            [здесь](https://github.com/openai/openai-python/blob/v1.54.3/src/openai/types/chat_model.py#L7)
            (К сожалению, несмотря на просьбу, OpenAI не предоставляет `.inv` файлы для своего API).
        system_prompt_role (OpenAISystemPromptRole | None): Роль, используемая для системного промпт сообщения. Если не указана, по умолчанию используется `'system'`.
            В будущем это может быть выведено из имени модели.
        system (str | None): Используемый провайдер модели, по умолчанию 'openai'. Это для целей наблюдаемости, вы должны
            настроить `base_url` и `api_key`, чтобы использовать другого провайдера.
        **kwargs: Дополнительные аргументы, передаваемые асинхронному клиенту.
    """
```

**Параметры**:

-   `model_name` (str): Имя AI модели.
-   `provider` (Optional[str]): Провайдер модели (например, 'openai').
-   `system_prompt_role` (Optional[OpenAISystemPromptRole]): Роль системного промпта.
-   `system` (Optional[str]): Используемая система (по умолчанию 'openai').
-   `**kwargs`: Дополнительные аргументы, передаваемые асинхронному клиенту.

**Как работает функция**:

1.  Инициализирует атрибуты `_model_name`, `_provider`, `system_prompt_role` и `_system` на основе переданных аргументов.
2.  Создает экземпляр `AsyncClient` с указанным провайдером и дополнительными аргументами.

```
Инициализация аргументов
↓
Создание экземпляра AsyncClient
```

#### `name`

```python
def name(self) -> str:
    """
    Возвращает имя модели.

    Returns:
        str: Имя модели в формате 'g4f:{provider}:{model_name}' или 'g4f:{model_name}', если провайдер не указан.
    """
```

**Возвращает**:

-   `str`: Имя модели.

**Как работает функция**:

1.  Проверяет, указан ли провайдер (`self._provider`).
2.  Если провайдер указан, возвращает имя в формате `g4f:{self._provider}:{self._model_name}`.
3.  Если провайдер не указан, возвращает имя в формате `g4f:{self._model_name}`.

```
Проверка наличия провайдера
↓
Формирование имени модели
```

**Примеры**:

```python
model = AIModel(model_name='gpt-3.5-turbo', provider='openai')
print(model.name())  # Вывод: g4f:openai:gpt-3.5-turbo

model = AIModel(model_name='gpt-4')
print(model.name())  # Вывод: g4f:gpt-4
```

## Функции

### `new_infer_model`

```python
def new_infer_model(model: Model | KnownModelName, api_key: str = None) -> Model:
    """
    Создает экземпляр модели на основе имени модели.

    Args:
        model (Model | KnownModelName): Имя модели или экземпляр класса Model.
        api_key (str, optional): API ключ. По умолчанию None.

    Returns:
        Model: Экземпляр AIModel или результат infer_model.
    """
```

**Параметры**:

-   `model` (Model | KnownModelName): Имя модели или экземпляр класса `Model`.
-   `api_key` (str, optional): API ключ. По умолчанию `None`.

**Возвращает**:

-   `Model`: Экземпляр `AIModel` или результат `infer_model`.

**Как работает функция**:

1.  Проверяет, является ли `model` экземпляром класса `Model`. Если да, возвращает его.
2.  Проверяет, начинается ли имя модели с "g4f:".
3.  Если да, обрезает "g4f:" и проверяет, содержит ли имя модели ":". Если да, разделяет имя на провайдера и имя модели и создает экземпляр `AIModel` с указанными параметрами. Если нет, создает экземпляр `AIModel` только с именем модели.
4.  Если имя модели не начинается с "g4f:", вызывает стандартную функцию `infer_model` с переданным именем модели и возвращает результат.

```
Проверка типа model
↓
Проверка префикса "g4f:"
↓
Создание экземпляра AIModel или вызов infer_model
```

**Примеры**:

```python
model = new_infer_model('g4f:openai:gpt-3.5-turbo')
print(model.name())  # Вывод: g4f:openai:gpt-3.5-turbo

model = new_infer_model('g4f:gpt-4')
print(model.name())  # Вывод: g4f:gpt-4

model = new_infer_model('gpt-3.5-turbo')
print(type(model))  # Вывод: <class 'pydantic_ai.models.openai.OpenAIModel'>
```

### `patch_infer_model`

```python
def patch_infer_model(api_key: str | None = None) -> None:
    """
    Заменяет стандартную функцию infer_model в модуле pydantic_ai.models на новую функцию new_infer_model.

    Args:
        api_key (str | None, optional): API ключ. По умолчанию None.
    """
```

**Параметры**:

-   `api_key` (str, optional): API ключ. По умолчанию `None`.

**Как работает функция**:

1.  Импортирует модуль `pydantic_ai.models`.
2.  Заменяет функцию `pydantic_ai.models.infer_model` на `partial(new_infer_model, api_key=api_key)`.
3.  Присваивает класс `AIModel` атрибуту `pydantic_ai.models.AIModel`.

```
Импорт модуля pydantic_ai.models
↓
Замена infer_model и AIModel
```

**Примеры**:

```python
import pydantic_ai.models

patch_infer_model()
model = pydantic_ai.models.infer_model('g4f:gpt-3.5-turbo')
print(type(model))  # Вывод: <class '__main__.AIModel'>