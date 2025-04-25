# Модуль `pydantic_ai.py`

## Обзор

Этот модуль расширяет функциональность библиотеки `pydantic_ai` для работы с API GPT4Free. 

Он предоставляет класс `AIModel`, который наследуется от `OpenAIModel` и обеспечивает взаимодействие с моделями GPT4Free через асинхронный клиент `AsyncClient`.

## Подробнее

Модуль `pydantic_ai.py` позволяет использовать модели GPT4Free в приложениях, основанных на `pydantic_ai`. 
Он предлагает следующие возможности:

- **Инициализация моделей GPT4Free:** Класс `AIModel` позволяет инициализировать модели GPT4Free с помощью API-ключа и 
    настройки базового URL-адреса. 
- **Управление моделями:** Предоставляет возможность выбора модели GPT4Free для использования в приложениях.
- **Асинхронное взаимодействие:**  `AIModel` использует асинхронный клиент `AsyncClient` для эффективной работы с 
    API GPT4Free.

## Классы

### `class AIModel(OpenAIModel)`

**Описание**: 
Этот класс представляет собой модель, которая использует API GPT4Free.

**Наследует**: 
- `OpenAIModel`

**Атрибуты**:

- `client (AsyncClient)`: Асинхронный клиент для взаимодействия с API GPT4Free.
- `system_prompt_role (OpenAISystemPromptRole | None)`: Роль для использования в системном запросе. 
    По умолчанию `None`.
- `_model_name (str)`: Имя используемой модели GPT4Free.
- `_provider (str)`: Имя поставщика модели. 
- `_system (Optional[str])`: Имя системы модели, по умолчанию 'openai'. Используется для целей 
    наблюдаемости.

**Методы**:

- `__init__(self, model_name: str, provider: str | None = None, *, system_prompt_role: OpenAISystemPromptRole | None = None, system: str | None = 'openai', **kwargs)`: 
    Инициализирует модель GPT4Free.

    **Параметры**:

    - `model_name (str)`: Имя используемой модели GPT4Free. Список доступных моделей можно найти 
        [здесь](https://github.com/openai/openai-python/blob/v1.54.3/src/openai/types/chat_model.py#L7).
    - `provider (str | None)`: Имя поставщика модели.
    - `system_prompt_role (OpenAISystemPromptRole | None)`: Роль для использования в системном запросе.
        По умолчанию `None`.
    - `system (str | None)`: Имя системы модели, по умолчанию 'openai'. Используется для целей 
        наблюдаемости.
    - `kwargs`: Дополнительные аргументы для клиента `AsyncClient`.

- `name(self) -> str`: Возвращает полное имя модели GPT4Free, включая поставщика и имя модели.

## Функции

### `new_infer_model(model: Model | KnownModelName, api_key: str = None) -> Model`

**Назначение**: 
Функция определяет, является ли модель GPT4Free, и создает соответствующий экземпляр `AIModel`.

**Параметры**:

- `model (Model | KnownModelName)`: Имя или объект модели.
- `api_key (str)`: API-ключ для доступа к API GPT4Free. 

**Возвращает**:

- `Model`: Объект модели `Model`.

**Как работает функция**:

- Проверяет, начинается ли имя модели с 'g4f:'.
- Если да, то извлекает имя поставщика и имя модели, создает новый экземпляр `AIModel` и возвращает его.
- В противном случае возвращает результат `infer_model(model)`.

### `patch_infer_model(api_key: str | None = None)`

**Назначение**: 
Функция обновляет функцию `infer_model` в `pydantic_ai` для поддержки моделей GPT4Free.

**Параметры**:

- `api_key (str | None)`: API-ключ для доступа к API GPT4Free.

**Как работает функция**:

- Изменяет функцию `infer_model` в `pydantic_ai` на `partial(new_infer_model, api_key=api_key)`.
- Заменяет класс `AIModel` в `pydantic_ai` на `AIModel`.

## Примеры

```python
from pydantic_ai.models import infer_model

# Инициализация модели GPT4Free
model = infer_model('g4f:gpt-3.5-turbo')

# Вызов модели для генерации текста
response = model.generate_text(prompt='Hello, world!')
print(response.text)

# Использование модели с определенным поставщиком
model = infer_model('g4f:google:gemini')
response = model.generate_text(prompt='What is the meaning of life?')
print(response.text)
```