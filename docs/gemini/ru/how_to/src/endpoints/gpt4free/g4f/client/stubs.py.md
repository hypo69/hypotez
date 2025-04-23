Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода определяет набор моделей данных, используемых для представления различных типов ответов от API чат-ботов, включая текстовые ответы, данные об использовании токенов и изображения. Он также содержит логику для сохранения контента сообщений, включая извлечение и сохранение изображений из URI данных.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**: Импортируются необходимые модули, такие как `os`, `typing`, `time`, а также специфичные для проекта модули, такие как `extract_data_uri`, `images_dir`, `filter_markdown` и `filter_none`.

2. **Определение базовой модели**: Определяется класс `BaseModel`, который служит базовым классом для всех остальных моделей данных. Если библиотека `pydantic` не установлена, создается упрощенная версия `BaseModel` с методом `model_construct`.

3. **Определение моделей данных**: Определяются различные классы моделей данных, такие как `TokenDetails`, `UsageModel`, `ToolFunctionModel`, `ToolCallModel`, `ChatCompletionChunk`, `ChatCompletionMessage`, `ChatCompletionChoice`, `ChatCompletion`, `ChatCompletionDelta`, `ChatCompletionDeltaChoice`, `Image` и `ImagesResponse`. Эти модели используются для представления различных аспектов ответов от API чат-ботов.

4. **Реализация метода `model_construct`**: В каждом классе модели данных реализуется метод `model_construct`, который используется для создания экземпляров класса с заданными параметрами. Этот метод обеспечивает дополнительную гибкость при создании объектов, позволяя устанавливать значения по умолчанию и фильтровать `None` значения.

5. **Реализация метода `save` в `ChatCompletionMessage`**: В классе `ChatCompletionMessage` реализован метод `save`, который используется для сохранения контента сообщения в файл. Этот метод обрабатывает различные типы контента, включая текст и изображения, закодированные в формате URI данных.

Пример использования
-------------------------

```python
from __future__ import annotations

import os
from typing import Optional, List
from time import time

from ..image import extract_data_uri
from ..image.copy_images import images_dir
from ..client.helper import filter_markdown
from .helper import filter_none

try:
    from pydantic import BaseModel
except ImportError:
    class BaseModel():
        @classmethod
        def model_construct(cls, **data):
            new = cls()
            for key, value in data.items():
                setattr(new, key, value)
            return new

class BaseModel(BaseModel):
    @classmethod
    def model_construct(cls, **data):
        if hasattr(super(), "model_construct"):
            return super().model_construct(**data)
        return cls.construct(**data)

class TokenDetails(BaseModel):
    cached_tokens: int

class UsageModel(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    prompt_tokens_details: TokenDetails
    completion_tokens_details: TokenDetails

    @classmethod
    def model_construct(cls, prompt_tokens=0, completion_tokens=0, total_tokens=0, prompt_tokens_details=None, completion_tokens_details=None, **kwargs):
        return super().model_construct(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            prompt_tokens_details=TokenDetails.model_construct(**prompt_tokens_details if prompt_tokens_details else {"cached_tokens": 0}),
            completion_tokens_details=TokenDetails.model_construct(**completion_tokens_details if completion_tokens_details else {}),
            **kwargs
        )

class ToolFunctionModel(BaseModel):
    name: str
    arguments: str

class ToolCallModel(BaseModel):
    id: str
    type: str
    function: ToolFunctionModel

    @classmethod
    def model_construct(cls, function=None, **kwargs):
        return super().model_construct(
            **kwargs,
            function=ToolFunctionModel.model_construct(**function),
        )

class ChatCompletionChunk(BaseModel):
    id: str
    object: str
    created: int
    model: str
    provider: Optional[str]
    choices: List[ChatCompletionDeltaChoice]
    usage: UsageModel

    @classmethod
    def model_construct(
        cls,
        content: str,
        finish_reason: str,
        completion_id: str = None,
        created: int = None,
        usage: UsageModel = None
    ):
        return super().model_construct(
            id=f"chatcmpl-{completion_id}" if completion_id else None,
            object="chat.completion.cunk",
            created=created,
            model=None,
            provider=None,
            choices=[ChatCompletionDeltaChoice.model_construct(
                ChatCompletionDelta.model_construct(content),
                finish_reason
            )],
            **filter_none(usage=usage)
        )

class ChatCompletionMessage(BaseModel):
    role: str
    content: str
    tool_calls: list[ToolCallModel] = None

    @classmethod
    def model_construct(cls, content: str, tool_calls: list = None):
        return super().model_construct(role="assistant", content=content, **filter_none(tool_calls=tool_calls))

    def save(self, filepath: str, allowd_types = None):
        if hasattr(self.content, "data"):
            os.rename(self.content.data.replace("/media", images_dir), filepath)
            return
        if self.content.startswith("data:"):\
            with open(filepath, "wb") as f:\
                f.write(extract_data_uri(self.content))
            return
        content = filter_markdown(self.content, allowd_types)
        if content is not None:
            with open(filepath, "w") as f:
                f.write(content)

class ChatCompletionChoice(BaseModel):
    index: int
    message: ChatCompletionMessage
    finish_reason: str

    @classmethod
    def model_construct(cls, message: ChatCompletionMessage, finish_reason: str):
        return super().model_construct(index=0, message=message, finish_reason=finish_reason)

class ChatCompletion(BaseModel):
    id: str
    object: str
    created: int
    model: str
    provider: Optional[str]
    choices: list[ChatCompletionChoice]
    usage: UsageModel
    conversation: dict

    @classmethod
    def model_construct(
        cls,
        content: str,
        finish_reason: str,
        completion_id: str = None,
        created: int = None,
        tool_calls: list[ToolCallModel] = None,
        usage: UsageModel = None,
        conversation: dict = None
    ):
        return super().model_construct(
            id=f"chatcmpl-{completion_id}" if completion_id else None,
            object="chat.completion",
            created=created,
            model=None,
            provider=None,
            choices=[ChatCompletionChoice.model_construct(
                ChatCompletionMessage.model_construct(content, tool_calls),
                finish_reason,
            )],
            **filter_none(usage=usage, conversation=conversation)
        )

class ChatCompletionDelta(BaseModel):
    role: str
    content: str

    @classmethod
    def model_construct(cls, content: Optional[str]):
        return super().model_construct(role="assistant", content=content)

class ChatCompletionDeltaChoice(BaseModel):
    index: int
    delta: ChatCompletionDelta
    finish_reason: Optional[str]

    @classmethod
    def model_construct(cls, delta: ChatCompletionDelta, finish_reason: Optional[str]):
        return super().model_construct(index=0, delta=delta, finish_reason=finish_reason)

class Image(BaseModel):
    url: Optional[str]
    b64_json: Optional[str]
    revised_prompt: Optional[str]

    @classmethod
    def model_construct(cls, url: str = None, b64_json: str = None, revised_prompt: str = None):
        return super().model_construct(**filter_none(
            url=url,
            b64_json=b64_json,
            revised_prompt=revised_prompt
        ))

class ImagesResponse(BaseModel):
    data: List[Image]
    model: str
    provider: str
    created: int

    @classmethod
    def model_construct(cls, data: List[Image], created: int = None, model: str = None, provider: str = None):
        if created is None:
            created = int(time())
        return super().model_construct(
            data=data,
            model=model,
            provider=provider,
            created=created
        )