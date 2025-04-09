# Модуль интеграции pydantic-ai с g4f
## Обзор

Модуль предоставляет интеграцию для использования моделей G4F (gpt4free) с библиотекой pydantic-ai. Он содержит класс `AIModel`, который расширяет возможности OpenAIModel, позволяя использовать модели, предоставляемые через API G4F. Также модуль предоставляет функции для расширения `infer_model` и `patch_infer_model` из `pydantic_ai.models` для работы с моделями G4F.

## Подорбней

Модуль позволяет легко интегрировать модели, предоставляемые через API gpt4free, в приложения, использующие pydantic-ai. Он предоставляет класс `AIModel`, который можно использовать как замену стандартным моделям OpenAI.

## Классы

### `AIModel`

**Описание**: Класс `AIModel` представляет собой модель, которая использует API G4F.

**Наследует**:

- `OpenAIModel`:  Класс наследует `OpenAIModel` из `pydantic_ai.models.openai`. Это позволяет использовать `AIModel` как замену стандартным моделям OpenAI, сохраняя совместимость с существующим кодом.

**Аттрибуты**:

- `client` (AsyncClient): Асинхронный клиент для взаимодействия с API G4F.
- `system_prompt_role` (OpenAISystemPromptRole | None): Роль системного промпта. Может быть `None`.
- `_model_name` (str): Внутреннее имя модели.
- `_provider` (str): Внутреннее имя провайдера модели.
- `_system` (Optional[str]): Внутренняя настройка, указывающая на систему (по умолчанию 'openai').

**Методы**:

- `__init__`: Инициализирует экземпляр класса `AIModel`.
- `name`: Возвращает имя модели в формате `g4f:{provider}:{model_name}` или `g4f:{model_name}`, если провайдер не указан.

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
    """Initialize an AI model.

    Args:
        model_name: The name of the AI model to use. List of model names available
            [here](https://github.com/openai/openai-python/blob/v1.54.3/src/openai/types/chat_model.py#L7)
            (Unfortunately, despite being ask to do so, OpenAI do not provide `.inv` files for their API).
        system_prompt_role: The role to use for the system prompt message. If not provided, defaults to `'system'`.
            In the future, this may be inferred from the model name.
        system: The model provider used, defaults to `openai`. This is for observability purposes, you must
            customize the `base_url` and `api_key` to use a different provider.
    """
```

**Назначение**: Инициализирует экземпляр класса `AIModel`.

**Параметры**:

- `model_name` (str): Имя используемой AI-модели. Список доступных имен моделей можно найти [здесь](https://github.com/openai/openai-python/blob/v1.54.3/src/openai/types/chat_model.py#L7).
- `provider` (str | None): Провайдер модели. По умолчанию `None`.
- `system_prompt_role` (OpenAISystemPromptRole | None): Роль, используемая для системного промпта. Если не указана, по умолчанию используется `'system'`. В будущем это может быть выведено из имени модели. По умолчанию `None`.
- `system` (str | None): Используемый провайдер модели, по умолчанию `'openai'`. Это необходимо для целей наблюдаемости. Необходимо настроить `base_url` и `api_key` для использования другого провайдера.
- `**kwargs`: Дополнительные аргументы, которые будут переданы в `AsyncClient`.

**Как работает функция**:

1.  Сохраняет имя модели в атрибуте `_model_name`.
2.  Сохраняет имя провайдера в атрибуте `_provider`.
3.  Создает экземпляр `AsyncClient` с указанным провайдером и дополнительными аргументами.
4.  Сохраняет роль системного промпта в атрибуте `system_prompt_role`.
5.  Устанавливает атрибут `_system` в значение параметра `system`.

```text
A: Присвоение model_name атрибуту _model_name
│
B: Присвоение provider атрибуту _provider
│
C: Создание экземпляра AsyncClient и присвоение атрибуту client
│
D: Присвоение system_prompt_role атрибуту system_prompt_role
│
E: Присвоение system атрибуту _system
```

#### `name`

```python
def name(self) -> str:
    """ """
```

**Назначение**: Возвращает имя модели.

**Возвращает**:

- `str`: Имя модели в формате `g4f:{provider}:{model_name}`, если указан провайдер, или `g4f:{model_name}` в противном случае.

**Как работает функция**:

1.  Проверяет, указан ли провайдер (`self._provider`).
2.  Если провайдер указан, формирует имя модели как `g4f:{self._provider}:{self._model_name}`.
3.  Если провайдер не указан, формирует имя модели как `g4f:{self._model_name}`.
4.  Возвращает сформированное имя модели.

```text
A: Проверка наличия провайдера
│
├───> B: Формирование имени с провайдером (g4f:{provider}:{model_name})
│
└───> C: Формирование имени без провайдера (g4f:{model_name})
│
D: Возврат имени модели
```

## Функции

### `new_infer_model`

```python
def new_infer_model(model: Model | KnownModelName, api_key: str | None = None) -> Model:
    """ """
```

**Назначение**: Создает экземпляр модели на основе переданного имени модели или экземпляра `Model`.  Если имя модели начинается с "g4f:", пытается создать экземпляр `AIModel` с указанным провайдером (если он есть в имени) или без него.  В противном случае вызывает оригинальную функцию `infer_model` из `pydantic_ai.models`.

**Параметры**:

- `model` (Model | KnownModelName): Имя модели или экземпляр класса `Model`.
- `api_key` (str | None): Ключ API. Передается в `AIModel`, если создается экземпляр `AIModel`. По умолчанию `None`.

**Возвращает**:

- `Model`: Экземпляр класса `Model` (либо `AIModel`, либо возвращенный из `infer_model`).

**Как работает функция**:

1.  Проверяет, является ли входной параметр `model` экземпляром класса `Model`. Если да, возвращает его.
2.  Проверяет, начинается ли имя модели с "g4f:".
3.  Если да, удаляет префикс "g4f:" из имени модели.
4.  Если в имени модели есть символ ":", разделяет имя на провайдера и имя модели. Создает экземпляр `AIModel` с указанным провайдером и ключом API (если он передан).
5.  Если в имени модели нет символа ":", создает экземпляр `AIModel` с указанным именем модели и ключом API (если он передан).
6.  Если имя модели не начинается с "g4f:", вызывает оригинальную функцию `infer_model` из `pydantic_ai.models` и возвращает ее результат.

```text
A: Проверка, является ли model экземпляром Model
│
├───> B: Возврат model
│
└───> C: Проверка, начинается ли model с "g4f:"
    │
    ├───> D: Удаление префикса "g4f:" из model
    │   │
    │   E: Проверка наличия ":" в model
    │   │
    │   ├───> F: Разделение model на provider и model_name
    │   │   │
    │   │   G: Создание экземпляра AIModel с provider и api_key
    │   │
    │   └───> H: Создание экземпляра AIModel с model_name и api_key
    │
    └───> I: Вызов infer_model из pydantic_ai.models и возврат результата
```

### `patch_infer_model`

```python
def patch_infer_model(api_key: str | None = None) -> None:
    """ """
```

**Назначение**: Заменяет функцию `infer_model` в модуле `pydantic_ai.models` на `new_infer_model`, а также заменяет `pydantic_ai.models.AIModel` на `AIModel` из текущего модуля.  Это позволяет использовать `new_infer_model` для автоматического определения и создания экземпляров моделей G4F при использовании `pydantic-ai`.

**Параметры**:

- `api_key` (str | None): Ключ API, который будет передан в `new_infer_model`. По умолчанию `None`.

**Как работает функция**:

1.  Импортирует модуль `pydantic_ai.models`.
2.  Использует `functools.partial` для создания новой функции `new_infer_model` с фиксированным значением параметра `api_key`.
3.  Заменяет функцию `infer_model` в модуле `pydantic_ai.models` на созданную функцию `new_infer_model`.
4.  Заменяет `pydantic_ai.models.AIModel` на `AIModel` из текущего модуля.

```text
A: Импорт модуля pydantic_ai.models
│
B: Создание partial-функции new_infer_model с api_key
│
C: Замена pydantic_ai.models.infer_model на partial-функцию
│
D: Замена pydantic_ai.models.AIModel на AIModel из текущего модуля
```