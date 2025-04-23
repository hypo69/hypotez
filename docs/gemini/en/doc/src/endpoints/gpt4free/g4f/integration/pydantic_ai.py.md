# Модуль для интеграции pydantic-ai с G4F

## Обзор

Модуль предоставляет интеграцию между библиотекой `pydantic-ai` и API G4F (gpt4free), позволяя использовать модели G4F в приложениях, использующих `pydantic-ai`.
Он включает класс `AIModel`, который расширяет `OpenAIModel` из `pydantic-ai`, и функции для вывода и исправления моделей.

## Более подробно

Этот модуль позволяет использовать модели G4F, такие как Google Gemini и OpenAI, в `pydantic-ai`.
Он предоставляет класс `AIModel`, который можно использовать для взаимодействия с API G4F.
Этот модуль также предоставляет функции для вывода и исправления моделей.
Это позволяет пользователям легко переключаться между различными моделями и поставщиками, используя `pydantic-ai`.

## Классы

### `AIModel`

**Описание**: Класс `AIModel` представляет модель искусственного интеллекта, использующую API G4F.

**Наследует**:
- `OpenAIModel`: Класс наследует функциональность `OpenAIModel` из библиотеки `pydantic-ai`.

**Атрибуты**:
- `client` (`AsyncClient`): Асинхронный клиент для взаимодействия с API G4F.
- `system_prompt_role` (`OpenAISystemPromptRole | None`): Роль системного запроса.
- `_model_name` (`str`): Название модели.
- `_provider` (`str`): Поставщик модели.
- `_system` (`Optional[str]`): Используемая система (по умолчанию 'openai').

**Принцип работы**:
Класс `AIModel` расширяет `OpenAIModel` и предоставляет возможность использовать API G4F для взаимодействия с моделями искусственного интеллекта. Он инициализируется с именем модели, поставщиком (опционально) и другими параметрами. Методы класса позволяют выполнять запросы к модели и получать результаты. Атрибут `client` используется для асинхронного взаимодействия с API G4F.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `AIModel`.
- `name`: Возвращает имя модели.

## Методы класса

### `__init__`

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
    """Инициализирует AI модель.

    Args:
        model_name (str): Название AI модели для использования. Список доступных названий моделей
            [здесь](https://github.com/openai/openai-python/blob/v1.54.3/src/openai/types/chat_model.py#L7)
            (К сожалению, несмотря на просьбу, OpenAI не предоставляет файлы `.inv` для своего API).
        system_prompt_role (OpenAISystemPromptRole | None): Роль для использования в системном запросе. Если не указана, по умолчанию используется `'system'`.
            В будущем это может быть выведено из названия модели.
        system (str | None): Используемый провайдер модели, по умолчанию `openai`. Это для целей наблюдаемости, необходимо
            настроить `base_url` и `api_key`, чтобы использовать другого провайдера.
    """
```

**Параметры**:
- `model_name` (`str`): Название модели AI.
- `provider` (`Optional[str]`, optional): Поставщик модели. По умолчанию `None`.
- `system_prompt_role` (`Optional[OpenAISystemPromptRole]`, optional): Роль системного запроса. По умолчанию `None`.
- `system` (`Optional[str]`, optional): Используемая система. По умолчанию `'openai'`.
- `**kwargs`: Дополнительные аргументы, передаваемые клиенту.

**Примеры**:

```python
ai_model = AIModel(model_name='gpt-3.5-turbo', provider='openai')
ai_model = AIModel(model_name='gemini-pro', provider='google', system_prompt_role=OpenAISystemPromptRole.USER)
```

### `name`

```python
def name(self) -> str:
    """Возвращает имя модели.

    Returns:
        str: Имя модели в формате 'g4f:<провайдер>:<название_модели>' или 'g4f:<название_модели>', если провайдер не указан.
    """
```

**Примеры**:

```python
ai_model = AIModel(model_name='gpt-3.5-turbo', provider='openai')
print(ai_model.name())  # Вывод: g4f:openai:gpt-3.5-turbo

ai_model = AIModel(model_name='gemini-pro')
print(ai_model.name())  # Вывод: g4f:gemini-pro
```

## Функции

### `new_infer_model`

```python
def new_infer_model(model: Model | KnownModelName, api_key: str = None) -> Model:
    """Определяет тип модели и возвращает соответствующий экземпляр класса.

    Args:
        model (Model | KnownModelName): Модель или название известной модели.
        api_key (str, optional): API ключ для доступа к модели. По умолчанию `None`.

    Returns:
        Model: Экземпляр класса `AIModel` или результат `infer_model` из `pydantic_ai.models`.
    """
```

**Параметры**:
- `model` (`Model | KnownModelName`): Модель или название известной модели.
- `api_key` (`str`, optional): API ключ для доступа к модели. По умолчанию `None`.

**Как работает функция**:
Функция `new_infer_model` определяет тип модели и возвращает соответствующий экземпляр класса. Если модель начинается с префикса "g4f:", она создает экземпляр класса `AIModel` с указанным именем модели и поставщиком (если указан). Если модель не начинается с префикса "g4f:", она вызывает функцию `infer_model` из `pydantic_ai.models` для определения типа модели.

**Примеры**:

```python
from pydantic_ai.models import KnownModelName

model = new_infer_model(model="g4f:openai:gpt-3.5-turbo")
print(type(model))  # Вывод: <class 'src.endpoints.gpt4free.g4f.integration.pydantic_ai.AIModel'>

model = new_infer_model(model=KnownModelName.GPT_4)
print(type(model))  # Вывод: <class 'pydantic_ai.models.openai.OpenAIModel'>
```

### `patch_infer_model`

```python
def patch_infer_model(api_key: str | None = None):
    """Заменяет функцию `infer_model` в модуле `pydantic_ai.models` на `new_infer_model`.

    Args:
        api_key (str | None): API ключ для доступа к моделям. По умолчанию `None`.
    """
```

**Параметры**:
- `api_key` (`str | None`, optional): API ключ для доступа к моделям. По умолчанию `None`.

**Как работает функция**:
Функция `patch_infer_model` заменяет функцию `infer_model` в модуле `pydantic_ai.models` на `new_infer_model`. Это позволяет использовать модели G4F в приложениях, использующих `pydantic-ai`, без изменения кода приложения.

**Примеры**:

```python
patch_infer_model(api_key="ключ_api")

from pydantic_ai.models import infer_model, KnownModelName

model = infer_model(model="g4f:openai:gpt-3.5-turbo")
print(type(model))  # Вывод: <class 'src.endpoints.gpt4free.g4f.integration.pydantic_ai.AIModel'>

model = infer_model(model=KnownModelName.GPT_4)
print(type(model))  # Вывод: <class 'pydantic_ai.models.openai.OpenAIModel'>