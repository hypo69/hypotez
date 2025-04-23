# Модуль stubs.py

## Обзор

Модуль содержит определения классов, используемых для представления структур данных ответов от API. Эти классы основаны на `pydantic.BaseModel` (если он доступен) и используются для типизации и проверки данных, возвращаемых API. Модуль также содержит вспомогательные функции для фильтрации данных и извлечения URI данных изображений.

## Дополнительные сведения

Модуль предоставляет классы для представления деталей токенов, использования моделей, вызовов инструментов, чат-завершений и ответов изображений. Он также содержит вспомогательные функции для фильтрации `None` значений и markdown. Эти классы и функции используются для обеспечения надежной и последовательной структуры данных при взаимодействии с API.

## Классы

### `BaseModel`

**Описание**: Базовый класс для всех моделей данных.

**Наследует**:

- `pydantic.BaseModel` (если доступен)

**Атрибуты**:

- Нет предопределенных атрибутов.

**Методы**:

- `model_construct(**data)`: Создает экземпляр класса, заполняя его данными из словаря `data`.

```python
class BaseModel():
    """Описание базового класса для всех моделей данных.
    Args:
        **data: Произвольные данные для инициализации модели.
    """
    @classmethod
    def model_construct(cls, **data):
        """Создает экземпляр класса, заполняя его данными из словаря `data`.
        Args:
            **data: Произвольные данные для инициализации модели.
        Returns:
            cls: Экземпляр класса, инициализированный данными.
        """
        new = cls()
        for key, value in data.items():
            setattr(new, key, value)
        return new
```

### `TokenDetails`

**Описание**: Класс для представления деталей токенов.

**Наследует**:

- `BaseModel`

**Атрибуты**:

- `cached_tokens` (int): Количество кэшированных токенов.

```python
class TokenDetails(BaseModel):
    """Класс для представления деталей токенов.
    Args:
        cached_tokens (int): Количество кэшированных токенов.
    """
    cached_tokens: int
```

### `UsageModel`

**Описание**: Класс для представления информации об использовании модели.

**Наследует**:

- `BaseModel`

**Атрибуты**:

- `prompt_tokens` (int): Количество токенов в запросе.
- `completion_tokens` (int): Количество токенов в завершении.
- `total_tokens` (int): Общее количество токенов.
- `prompt_tokens_details` (TokenDetails): Детали токенов запроса.
- `completion_tokens_details` (TokenDetails): Детали токенов завершения.

**Методы**:

- `model_construct(prompt_tokens=0, completion_tokens=0, total_tokens=0, prompt_tokens_details=None, completion_tokens_details=None, **kwargs)`: Создает экземпляр класса, заполняя его данными.

```python
class UsageModel(BaseModel):
    """Класс для представления информации об использовании модели.

    Args:
        prompt_tokens (int): Количество токенов в запросе.
        completion_tokens (int): Количество токенов в завершении.
        total_tokens (int): Общее количество токенов.
        prompt_tokens_details (TokenDetails): Детали токенов запроса.
        completion_tokens_details (TokenDetails): Детали токенов завершения.
        **kwargs: Дополнительные аргументы.
    """
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    prompt_tokens_details: TokenDetails
    completion_tokens_details: TokenDetails

    @classmethod
    def model_construct(cls, prompt_tokens=0, completion_tokens=0, total_tokens=0, prompt_tokens_details=None, completion_tokens_details=None, **kwargs):
        """Создает экземпляр класса, заполняя его данными.
        Args:
            prompt_tokens (int): Количество токенов в запросе.
            completion_tokens (int): Количество токенов в завершении.
            total_tokens (int): Общее количество токенов.
            prompt_tokens_details (TokenDetails): Детали токенов запроса.
            completion_tokens_details (TokenDetails): Детали токенов завершения.
            **kwargs: Дополнительные аргументы.

        Returns:
            UsageModel: Экземпляр класса, инициализированный данными.
        """
        return super().model_construct(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            prompt_tokens_details=TokenDetails.model_construct(**prompt_tokens_details if prompt_tokens_details else {"cached_tokens": 0}),
            completion_tokens_details=TokenDetails.model_construct(**completion_tokens_details if completion_tokens_details else {}),
            **kwargs
        )
```

### `ToolFunctionModel`

**Описание**: Класс для представления модели функции инструмента.

**Наследует**:

- `BaseModel`

**Атрибуты**:

- `name` (str): Имя функции.
- `arguments` (str): Аргументы функции.

```python
class ToolFunctionModel(BaseModel):
    """Класс для представления модели функции инструмента.

    Args:
        name (str): Имя функции.
        arguments (str): Аргументы функции.
    """
    name: str
    arguments: str
```

### `ToolCallModel`

**Описание**: Класс для представления модели вызова инструмента.

**Наследует**:

- `BaseModel`

**Атрибуты**:

- `id` (str): Идентификатор вызова.
- `type` (str): Тип вызова.
- `function` (ToolFunctionModel): Функция для вызова.

**Методы**:

- `model_construct(function=None, **kwargs)`: Создает экземпляр класса, заполняя его данными.

```python
class ToolCallModel(BaseModel):
    """Класс для представления модели вызова инструмента.
    Args:
        id (str): Идентификатор вызова.
        type (str): Тип вызова.
        function (ToolFunctionModel): Функция для вызова.
    """
    id: str
    type: str
    function: ToolFunctionModel

    @classmethod
    def model_construct(cls, function=None, **kwargs):
        """Создает экземпляр класса, заполняя его данными.
        Args:
            function (ToolFunctionModel): Функция для вызова.
            **kwargs: Дополнительные аргументы.

        Returns:
            ToolCallModel: Экземпляр класса, инициализированный данными.
        """
        return super().model_construct(
            **kwargs,
            function=ToolFunctionModel.model_construct(**function),
        )
```

### `ChatCompletionChunk`

**Описание**: Класс для представления чанка завершения чата.

**Наследует**:

- `BaseModel`

**Атрибуты**:

- `id` (str): Идентификатор чанка.
- `object` (str): Тип объекта.
- `created` (int): Время создания.
- `model` (str): Используемая модель.
- `provider` (Optional[str]): Провайдер.
- `choices` (List[ChatCompletionDeltaChoice]): Список вариантов.
- `usage` (UsageModel): Информация об использовании.

**Методы**:

- `model_construct(content: str, finish_reason: str, completion_id: str = None, created: int = None, usage: UsageModel = None)`: Создает экземпляр класса, заполняя его данными.

```python
class ChatCompletionChunk(BaseModel):
    """Класс для представления чанка завершения чата.
    Args:
        id (str): Идентификатор чанка.
        object (str): Тип объекта.
        created (int): Время создания.
        model (str): Используемая модель.
        provider (Optional[str]): Провайдер.
        choices (List[ChatCompletionDeltaChoice]): Список вариантов.
        usage (UsageModel): Информация об использовании.
    """
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
        """Создает экземпляр класса, заполняя его данными.
        Args:
            content (str): Содержимое чанка.
            finish_reason (str): Причина завершения.
            completion_id (str): Идентификатор завершения.
            created (int): Время создания.
            usage (UsageModel): Информация об использовании.

        Returns:
            ChatCompletionChunk: Экземпляр класса, инициализированный данными.
        """
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
```

### `ChatCompletionMessage`

**Описание**: Класс для представления сообщения завершения чата.

**Наследует**:

- `BaseModel`

**Атрибуты**:

- `role` (str): Роль сообщения (например, "assistant").
- `content` (str): Содержимое сообщения.
- `tool_calls` (list[ToolCallModel]): Список вызовов инструментов.

**Методы**:

- `model_construct(content: str, tool_calls: list = None)`: Создает экземпляр класса, заполняя его данными.
- `save(self, filepath: str, allowd_types = None)`: Сохраняет содержимое сообщения в файл.

```python
class ChatCompletionMessage(BaseModel):
    """Класс для представления сообщения завершения чата.

    Args:
        role (str): Роль сообщения (например, "assistant").
        content (str): Содержимое сообщения.
        tool_calls (list[ToolCallModel]): Список вызовов инструментов.
    """
    role: str
    content: str
    tool_calls: list[ToolCallModel] = None

    @classmethod
    def model_construct(cls, content: str, tool_calls: list = None):
        """Создает экземпляр класса, заполняя его данными.
        Args:
            content (str): Содержимое сообщения.
            tool_calls (list[ToolCallModel]): Список вызовов инструментов.

        Returns:
            ChatCompletionMessage: Экземпляр класса, инициализированный данными.
        """
        return super().model_construct(role="assistant", content=content, **filter_none(tool_calls=tool_calls))

    def save(self, filepath: str, allowd_types = None):
        """Сохраняет содержимое сообщения в файл.

        Args:
            filepath (str): Путь к файлу для сохранения содержимого.
            allowd_types: Разрешенные типы данных.
        """
        if hasattr(self.content, "data"):
            os.rename(self.content.data.replace("/media", images_dir), filepath)
            return
        if self.content.startswith("data:"):
            with open(filepath, "wb") as f:
                f.write(extract_data_uri(self.content))
            return
        content = filter_markdown(self.content, allowd_types)
        if content is not None:
            with open(filepath, "w") as f:
                f.write(content)
```

### `ChatCompletionChoice`

**Описание**: Класс для представления выбора завершения чата.

**Наследует**:

- `BaseModel`

**Атрибуты**:

- `index` (int): Индекс выбора.
- `message` (ChatCompletionMessage): Сообщение выбора.
- `finish_reason` (str): Причина завершения.

**Методы**:

- `model_construct(message: ChatCompletionMessage, finish_reason: str)`: Создает экземпляр класса, заполняя его данными.

```python
class ChatCompletionChoice(BaseModel):
    """Класс для представления выбора завершения чата.
    Args:
        index (int): Индекс выбора.
        message (ChatCompletionMessage): Сообщение выбора.
        finish_reason (str): Причина завершения.
    """
    index: int
    message: ChatCompletionMessage
    finish_reason: str

    @classmethod
    def model_construct(cls, message: ChatCompletionMessage, finish_reason: str):
        """Создает экземпляр класса, заполняя его данными.
        Args:
            message (ChatCompletionMessage): Сообщение выбора.
            finish_reason (str): Причина завершения.

        Returns:
            ChatCompletionChoice: Экземпляр класса, инициализированный данными.
        """
        return super().model_construct(index=0, message=message, finish_reason=finish_reason)
```

### `ChatCompletion`

**Описание**: Класс для представления завершения чата.

**Наследует**:

- `BaseModel`

**Атрибуты**:

- `id` (str): Идентификатор завершения.
- `object` (str): Тип объекта.
- `created` (int): Время создания.
- `model` (str): Используемая модель.
- `provider` (Optional[str]): Провайдер.
- `choices` (list[ChatCompletionChoice]): Список вариантов.
- `usage` (UsageModel): Информация об использовании.
- `conversation` (dict): Информация о разговоре.

**Методы**:

- `model_construct(content: str, finish_reason: str, completion_id: str = None, created: int = None, tool_calls: list[ToolCallModel] = None, usage: UsageModel = None, conversation: dict = None)`: Создает экземпляр класса, заполняя его данными.

```python
class ChatCompletion(BaseModel):
    """Класс для представления завершения чата.
    Args:
        id (str): Идентификатор завершения.
        object (str): Тип объекта.
        created (int): Время создания.
        model (str): Используемая модель.
        provider (Optional[str]): Провайдер.
        choices (list[ChatCompletionChoice]): Список вариантов.
        usage (UsageModel): Информация об использовании.
        conversation (dict): Информация о разговоре.
    """
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
        """Создает экземпляр класса, заполняя его данными.
        Args:
            content (str): Содержимое.
            finish_reason (str): Причина завершения.
            completion_id (str): Идентификатор завершения.
            created (int): Время создания.
            tool_calls (list[ToolCallModel]): Список вызовов инструментов.
            usage (UsageModel): Информация об использовании.
            conversation (dict): Информация о разговоре.

        Returns:
            ChatCompletion: Экземпляр класса, инициализированный данными.
        """
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
```

### `ChatCompletionDelta`

**Описание**: Класс для представления дельты завершения чата.

**Наследует**:

- `BaseModel`

**Атрибуты**:

- `role` (str): Роль сообщения (например, "assistant").
- `content` (str): Содержимое сообщения.

**Методы**:

- `model_construct(content: Optional[str])`: Создает экземпляр класса, заполняя его данными.

```python
class ChatCompletionDelta(BaseModel):
    """Класс для представления дельты завершения чата.
    Args:
        role (str): Роль сообщения (например, "assistant").
        content (str): Содержимое сообщения.
    """
    role: str
    content: str

    @classmethod
    def model_construct(cls, content: Optional[str]):
        """Создает экземпляр класса, заполняя его данными.
        Args:
            content (Optional[str]): Содержимое сообщения.

        Returns:
            ChatCompletionDelta: Экземпляр класса, инициализированный данными.
        """
        return super().model_construct(role="assistant", content=content)
```

### `ChatCompletionDeltaChoice`

**Описание**: Класс для представления выбора дельты завершения чата.

**Наследует**:

- `BaseModel`

**Атрибуты**:

- `index` (int): Индекс выбора.
- `delta` (ChatCompletionDelta): Дельта.
- `finish_reason` (Optional[str]): Причина завершения.

**Методы**:

- `model_construct(delta: ChatCompletionDelta, finish_reason: Optional[str])`: Создает экземпляр класса, заполняя его данными.

```python
class ChatCompletionDeltaChoice(BaseModel):
    """Класс для представления выбора дельты завершения чата.
    Args:
        index (int): Индекс выбора.
        delta (ChatCompletionDelta): Дельта.
        finish_reason (Optional[str]): Причина завершения.
    """
    index: int
    delta: ChatCompletionDelta
    finish_reason: Optional[str]

    @classmethod
    def model_construct(cls, delta: ChatCompletionDelta, finish_reason: Optional[str]):
        """Создает экземпляр класса, заполняя его данными.
        Args:
            delta (ChatCompletionDelta): Дельта.
            finish_reason (Optional[str]): Причина завершения.

        Returns:
            ChatCompletionDeltaChoice: Экземпляр класса, инициализированный данными.
        """
        return super().model_construct(index=0, delta=delta, finish_reason=finish_reason)
```

### `Image`

**Описание**: Класс для представления изображения.

**Наследует**:

- `BaseModel`

**Атрибуты**:

- `url` (Optional[str]): URL изображения.
- `b64_json` (Optional[str]): Изображение в формате base64 JSON.
- `revised_prompt` (Optional[str]): Скорректированный запрос.

**Методы**:

- `model_construct(url: str = None, b64_json: str = None, revised_prompt: str = None)`: Создает экземпляр класса, заполняя его данными.

```python
class Image(BaseModel):
    """Класс для представления изображения.

    Args:
        url (Optional[str]): URL изображения.
        b64_json (Optional[str]): Изображение в формате base64 JSON.
        revised_prompt (Optional[str]): Скорректированный запрос.
    """
    url: Optional[str]
    b64_json: Optional[str]
    revised_prompt: Optional[str]

    @classmethod
    def model_construct(cls, url: str = None, b64_json: str = None, revised_prompt: str = None):
        """Создает экземпляр класса, заполняя его данными.
        Args:
            url (str): URL изображения.
            b64_json (str): Изображение в формате base64 JSON.
            revised_prompt (str): Скорректированный запрос.

        Returns:
            Image: Экземпляр класса, инициализированный данными.
        """
        return super().model_construct(**filter_none(
            url=url,
            b64_json=b64_json,
            revised_prompt=revised_prompt
        ))
```

### `ImagesResponse`

**Описание**: Класс для представления ответа с изображениями.

**Наследует**:

- `BaseModel`

**Атрибуты**:

- `data` (List[Image]): Список изображений.
- `model` (str): Используемая модель.
- `provider` (str): Провайдер.
- `created` (int): Время создания.

**Методы**:

- `model_construct(data: List[Image], created: int = None, model: str = None, provider: str = None)`: Создает экземпляр класса, заполняя его данными.

```python
class ImagesResponse(BaseModel):
    """Класс для представления ответа с изображениями.

    Args:
        data (List[Image]): Список изображений.
        model (str): Используемая модель.
        provider (str): Провайдер.
        created (int): Время создания.
    """
    data: List[Image]
    model: str
    provider: str
    created: int

    @classmethod
    def model_construct(cls, data: List[Image], created: int = None, model: str = None, provider: str = None):
        """Создает экземпляр класса, заполняя его данными.
        Args:
            data (List[Image]): Список изображений.
            created (int): Время создания.
            model (str): Используемая модель.
            provider (str): Провайдер.

        Returns:
            ImagesResponse: Экземпляр класса, инициализированный данными.
        """
        if created is None:
            created = int(time())
        return super().model_construct(
            data=data,
            model=model,
            provider=provider,
            created=created
        )