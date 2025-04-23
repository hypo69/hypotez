Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код предоставляет интеграцию с библиотекой `pydantic-ai`, позволяя использовать модели G4F (GPT4Free) API. Он определяет класс `AIModel`, который расширяет возможности `OpenAIModel` из `pydantic-ai`, а также предоставляет функции для корректной инициализации и использования этих моделей. Кроме того, код включает функции `new_infer_model` и `patch_infer_model` для интеграции с системой определения моделей `pydantic-ai`.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются модули для работы с типами, функциями, классами данных и моделями `pydantic-ai`.
   - Импортируется `AsyncClient` для выполнения асинхронных запросов к G4F API.

2. **Определение класса `AIModel`**:
   - Создается класс `AIModel`, который наследуется от `OpenAIModel`. Этот класс представляет модель, использующую G4F API.
   - Определяются поля класса: `client` (асинхронный клиент), `system_prompt_role` (роль системного промта) и внутренние поля `_model_name`, `_provider`, `_system` для хранения информации о модели.
   - Метод `__init__` инициализирует модель, принимая имя модели, провайдера (если есть), роль системного промта и другие параметры. Внутри метода создается экземпляр `AsyncClient` для взаимодействия с API.
   - Метод `name` возвращает имя модели в формате `g4f:{provider}:{model_name}` или `g4f:{model_name}`, если провайдер не указан.

3. **Функция `new_infer_model`**:
   - Эта функция используется для определения и инициализации модели.
   - Если передана модель типа `Model`, она возвращается без изменений.
   - Если имя модели начинается с "g4f:", функция извлекает имя модели и провайдера (если есть) и создает экземпляр `AIModel`.
   - Если имя модели не начинается с "g4f:", вызывается стандартная функция `infer_model` из `pydantic-ai`.

4. **Функция `patch_infer_model`**:
   - Эта функция заменяет стандартную функцию `infer_model` в модуле `pydantic_ai.models` на `new_infer_model`.
   - Также присваивает класс `AIModel` атрибуту `AIModel` в модуле `pydantic_ai.models`.
   - Используется `partial` для передачи `api_key` в `new_infer_model`.

Пример использования
-------------------------

```python
from __future__ import annotations

from typing import Optional
from functools import partial
from dataclasses import dataclass, field

from pydantic_ai.models import Model, KnownModelName, infer_model
from pydantic_ai.models.openai import OpenAIModel, OpenAISystemPromptRole

import pydantic_ai.models.openai
pydantic_ai.models.openai.NOT_GIVEN = None

from ..client import AsyncClient

@dataclass(init=False)
class AIModel(OpenAIModel):
    """A model that uses the G4F API."""

    client: AsyncClient = field(repr=False)
    system_prompt_role: OpenAISystemPromptRole | None = field(default=None)

    _model_name: str = field(repr=False)
    _provider: str = field(repr=False)
    _system: Optional[str] = field(repr=False)

    def __init__(
        self,
        model_name: str,
        provider: str | None = None,
        *,
        system_prompt_role: OpenAISystemPromptRole | None = None,
        system: str | None = 'openai',
        **kwargs
    ):
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
        self._model_name = model_name
        self._provider = provider
        self.client = AsyncClient(provider=provider, **kwargs)
        self.system_prompt_role = system_prompt_role
        self._system = system

    def name(self) -> str:
        if self._provider:
            return f'g4f:{self._provider}:{self._model_name}'
        return f'g4f:{self._model_name}'

def new_infer_model(model: Model | KnownModelName, api_key: str = None) -> Model:
    if isinstance(model, Model):
        return model
    if model.startswith("g4f:"):
        model = model[4:]
        if ":" in model:
            provider, model = model.split(":", 1)
            return AIModel(model, provider=provider, api_key=api_key)
        return AIModel(model)
    return infer_model(model)

def patch_infer_model(api_key: str | None = None):
    import pydantic_ai.models

    pydantic_ai.models.infer_model = partial(new_infer_model, api_key=api_key)
    pydantic_ai.models.AIModel = AIModel

# Пример использования:
# 1. Импортируем необходимые функции
# from your_module import patch_infer_model, AIModel
# 2. Применяем патч для pydantic-ai
# patch_infer_model()
# 3. Теперь можно использовать AIModel напрямую или через infer_model
# model = AIModel(model_name="gpt-3.5-turbo", provider="openai")
# или
# model = infer_model("g4f:openai:gpt-3.5-turbo")
# print(model.name())