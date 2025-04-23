# Документация модуля `pydantic_ai.py`

## Обзор

Модуль предоставляет интеграцию с G4F API для использования в `pydantic-ai`. Он определяет класс `AIModel`, который расширяет `OpenAIModel` и позволяет использовать модели G4F для задач, связанных с искусственным интеллектом. Модуль также включает функции для определения модели и исправления `infer_model` в `pydantic_ai.models`.

## Подробнее

Этот модуль позволяет использовать различные модели ИИ через API G4F, интегрируя их в фреймворк `pydantic-ai`. Он настраивает клиент для асинхронного взаимодействия с API и предоставляет механизм для определения и выбора моделей ИИ.

## Классы

### `AIModel`

**Описание**: Класс `AIModel` представляет модель, использующую G4F API.

**Наследует**:
- `OpenAIModel`: Расширяет класс `OpenAIModel` из `pydantic_ai.models.openai`.

**Атрибуты**:
- `client` (`AsyncClient`): Асинхронный клиент для взаимодействия с G4F API.
- `system_prompt_role` (`OpenAISystemPromptRole | None`): Роль системного запроса. По умолчанию `None`.
- `_model_name` (`str`): Имя модели.
- `_provider` (`str`): Провайдер модели.
- `_system` (`Optional[str]`): Используемая система модели. По умолчанию `openai`.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `AIModel`.
- `name`: Возвращает имя модели.

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
)
```

**Назначение**: Инициализирует модель AI.

**Параметры**:
- `model_name` (`str`): Имя используемой модели AI. Список доступных имен моделей можно найти [здесь](https://github.com/openai/openai-python/blob/v1.54.3/src/openai/types/chat_model.py#L7).
- `provider` (`str | None`, optional): Провайдер модели. По умолчанию `None`.
- `system_prompt_role` (`OpenAISystemPromptRole | None`, optional): Роль для системного запроса. Если не указана, используется `'system'`. По умолчанию `None`.
- `system` (`str | None`, optional): Используемый провайдер модели. По умолчанию `'openai'`.
- `**kwargs`: Дополнительные аргументы для клиента.

**Как работает функция**:

- Функция инициализирует класс `AIModel`, устанавливая имя модели, провайдера и создавая асинхронного клиента `AsyncClient`.
- Она также настраивает роль системного запроса и используемую систему.

**Примеры**:

```python
from src.endpoints.gpt4free.g4f.integration.pydantic_ai import AIModel, OpenAISystemPromptRole

# Пример инициализации AIModel с указанием имени модели и провайдера
model = AIModel(model_name='gpt-3.5-turbo', provider='openai')

# Пример инициализации AIModel с указанием имени модели, провайдера и роли системного запроса
model = AIModel(model_name='gpt-3.5-turbo', provider='openai', system_prompt_role=OpenAISystemPromptRole.USER)

# Пример инициализации AIModel с дополнительными аргументами
model = AIModel(model_name='gpt-3.5-turbo', provider='openai', timeout=10)
```

### `name`

```python
def name(self) -> str:
```

**Назначение**: Возвращает имя модели.

**Возвращает**:
- `str`: Имя модели в формате `g4f:{provider}:{model_name}` или `g4f:{model_name}`, если провайдер не указан.

**Как работает функция**:

- Функция формирует имя модели на основе провайдера и имени модели.
- Если провайдер указан, имя модели будет содержать информацию о провайдере, иначе только имя модели.

**Примеры**:

```python
from src.endpoints.gpt4free.g4f.integration.pydantic_ai import AIModel

# Пример создания экземпляра AIModel
model = AIModel(model_name='gpt-3.5-turbo', provider='openai')

# Пример вызова метода name() для получения имени модели
model_name = model.name()
print(model_name)  # Вывод: g4f:openai:gpt-3.5-turbo

# Пример создания экземпляра AIModel без указания провайдера
model = AIModel(model_name='gpt-3.5-turbo')

# Пример вызова метода name() для получения имени модели
model_name = model.name()
print(model_name)  # Вывод: g4f:gpt-3.5-turbo
```

## Функции

### `new_infer_model`

```python
def new_infer_model(model: Model | KnownModelName, api_key: str = None) -> Model:
```

**Назначение**: Определяет модель AI на основе входных данных.

**Параметры**:
- `model` (`Model | KnownModelName`): Модель или имя известной модели.
- `api_key` (`str`, optional): API-ключ. По умолчанию `None`.

**Возвращает**:
- `Model`: Экземпляр класса `AIModel` или результат функции `infer_model`.

**Как работает функция**:

- Если входной параметр `model` является экземпляром класса `Model`, функция возвращает его без изменений.
- Если `model` является строкой, начинающейся с "g4f:", функция извлекает провайдера и имя модели из строки и создает экземпляр класса `AIModel`.
- Если `model` не начинается с "g4f:", функция вызывает `infer_model` для определения модели.

**Примеры**:

```python
from src.endpoints.gpt4free.g4f.integration.pydantic_ai import new_infer_model
from pydantic_ai.models import Model, KnownModelName

# Пример вызова new_infer_model с именем модели и провайдером
model = new_infer_model(model='g4f:openai:gpt-3.5-turbo')

# Пример вызова new_infer_model с именем модели без провайдера
model = new_infer_model(model='g4f:gpt-3.5-turbo')

# Пример вызова new_infer_model с существующей моделью
existing_model = Model()
model = new_infer_model(model=existing_model)
```

### `patch_infer_model`

```python
def patch_infer_model(api_key: str | None = None):
```

**Назначение**: Исправляет функцию `infer_model` в модуле `pydantic_ai.models`.

**Параметры**:
- `api_key` (`str | None`, optional): API-ключ. По умолчанию `None`.

**Как работает функция**:

- Функция импортирует модуль `pydantic_ai.models`.
- Она заменяет функцию `infer_model` в `pydantic_ai.models` на `new_infer_model` с использованием `partial`, передавая `api_key`.
- Она также присваивает класс `AIModel` атрибуту `AIModel` в `pydantic_ai.models`.

**Примеры**:

```python
from src.endpoints.gpt4free.g4f.integration.pydantic_ai import patch_infer_model

# Пример вызова patch_infer_model без API-ключа
patch_infer_model()

# Пример вызова patch_infer_model с API-ключом
patch_infer_model(api_key='your_api_key')