# Модуль для работы с моделью AIModel, использующей API G4F

## Обзор

Этот модуль предоставляет класс `AIModel`, который представляет собой модель, использующую API G4F (GPT-4 Free). Класс `AIModel` наследует от `OpenAIModel` и добавляет поддержку G4F API.

## Детали

Этот модуль интегрирует G4F API в pydantic-ai framework, расширяя возможности модели `OpenAIModel` для работы с G4F API.

## Классы

### `class AIModel`

**Описание**: Класс `AIModel` представляет собой модель, использующую API G4F (GPT-4 Free).

**Inherits**: `OpenAIModel`

**Attributes**:

- `client (AsyncClient)`: Асинхронный клиент для взаимодействия с API G4F.
- `system_prompt_role (OpenAISystemPromptRole | None)`: Роль для системного запроса. По умолчанию `None`.
- `_model_name (str)`: Имя модели.
- `_provider (str)`: Провайдер модели.
- `_system (Optional[str])`: Системный параметр.

**Methods**:

- `__init__(self, model_name: str, provider: str | None = None, *, system_prompt_role: OpenAISystemPromptRole | None = None, system: str | None = 'openai', **kwargs)`: Инициализирует модель `AIModel`.

    **Parameters**:

    - `model_name (str)`: Имя модели. Доступные модели [здесь](https://github.com/openai/openai-python/blob/v1.54.3/src/openai/types/chat_model.py#L7) (OpenAI, к сожалению, не предоставляет `.inv` файлы для своего API, несмотря на просьбу).
    - `provider (str | None)`: Провайдер модели. По умолчанию `None`.
    - `system_prompt_role (OpenAISystemPromptRole | None)`: Роль для системного запроса. По умолчанию `None`.
    - `system (str | None)`: Провайдер модели. По умолчанию `'openai'`. Используется для целей отслеживания. Необходимо настроить `base_url` и `api_key` для использования другого провайдера.

- `name(self) -> str`: Возвращает имя модели.

## Функции

### `new_infer_model(model: Model | KnownModelName, api_key: str = None) -> Model`

**Purpose**: Функция для инференса модели.

**Parameters**:

- `model (Model | KnownModelName)`: Модель, которую нужно использовать для инференса.
- `api_key (str)`: Ключ API. По умолчанию `None`.

**Returns**:

- `Model`: Модель, которая будет использоваться для инференса.

**How the Function Works**:

Функция `new_infer_model` принимает модель или имя модели и возвращает модель, готовую к использованию. 

### `patch_infer_model(api_key: str | None = None)`

**Purpose**: Функция для патчинга функции `infer_model`.

**Parameters**:

- `api_key (str | None)`: Ключ API. По умолчанию `None`.

**Returns**:

- `None`

**How the Function Works**:

Функция `patch_infer_model` патчит функцию `infer_model` для использования `new_infer_model` вместо стандартной функции `infer_model`.

**Examples**:

```python
from pydantic_ai.models import KnownModelName
from hypotez.src.endpoints.gpt4free.g4f.integration.pydantic_ai import AIModel, new_infer_model, patch_infer_model

# Использование AIModel
model = AIModel("gpt-3.5-turbo", provider="gpt4free")
print(model.name())  # Вывод: g4f:gpt4free:gpt-3.5-turbo

# Использование new_infer_model
model = new_infer_model(KnownModelName("g4f:gpt4free:gpt-3.5-turbo"), api_key="YOUR_API_KEY")
print(model.name())  # Вывод: g4f:gpt4free:gpt-3.5-turbo

# Использование patch_infer_model
patch_infer_model(api_key="YOUR_API_KEY")
model = infer_model("g4f:gpt4free:gpt-3.5-turbo")
print(model.name())  # Вывод: g4f:gpt4free:gpt-3.5-turbo
```