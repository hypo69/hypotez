# Модуль `stubs.py`

## Обзор

Модуль `stubs.py` содержит определения классов, которые используются для моделирования ответов от GPT-4Free API. Эти классы используются для преобразования ответов API в объекты Python, упрощая их обработку и использование.

## Детали

Модуль предоставляет набор классов, которые соответствуют различным структурам данных, возвращаемым GPT-4Free API. Эти классы используют библиотеку `pydantic` для проверки типов и валидации данных, что обеспечивает правильность и надежность данных, получаемых от API.

## Классы

### `BaseModel`

**Описание**: Базовый класс для всех других классов в модуле.

**Inherits**: `pydantic.BaseModel`

**Attributes**:

- `None`

**Methods**:

- `model_construct(cls, **data)`: Метод, который используется для создания новых экземпляров класса. Он гарантирует, что все атрибуты класса инициализированы с правильными значениями.

### `TokenDetails`

**Описание**: Класс, который моделирует информацию о количестве токенов в запросе и ответе.

**Inherits**: `BaseModel`

**Attributes**:

- `cached_tokens (int)`: Количество кэшированных токенов.

**Methods**:

- `None`

### `UsageModel`

**Описание**: Класс, который моделирует информацию об использовании токенов в запросе и ответе.

**Inherits**: `BaseModel`

**Attributes**:

- `prompt_tokens (int)`: Количество токенов в запросе.
- `completion_tokens (int)`: Количество токенов в ответе.
- `total_tokens (int)`: Общее количество токенов, использованных в запросе и ответе.
- `prompt_tokens_details (TokenDetails)`: Информация о токенах в запросе.
- `completion_tokens_details (TokenDetails)`: Информация о токенах в ответе.

**Methods**:

- `model_construct(cls, prompt_tokens=0, completion_tokens=0, total_tokens=0, prompt_tokens_details=None, completion_tokens_details=None, **kwargs)`: Метод, который используется для создания новых экземпляров класса. Он гарантирует, что все атрибуты класса инициализированы с правильными значениями.

### `ToolFunctionModel`

**Описание**: Класс, который моделирует информацию о функции инструмента, доступной для использования GPT-4Free.

**Inherits**: `BaseModel`

**Attributes**:

- `name (str)`: Имя функции инструмента.
- `arguments (str)`: Аргументы, которые могут быть переданы функции инструмента.

**Methods**:

- `model_construct(cls, function=None, **kwargs)`: Метод, который используется для создания новых экземпляров класса. Он гарантирует, что все атрибуты класса инициализированы с правильными значениями.

### `ToolCallModel`

**Описание**: Класс, который моделирует информацию о вызове функции инструмента.

**Inherits**: `BaseModel`

**Attributes**:

- `id (str)`: Идентификатор вызова функции инструмента.
- `type (str)`: Тип вызова функции инструмента.
- `function (ToolFunctionModel)`: Информация о функции инструмента.

**Methods**:

- `model_construct(cls, function=None, **kwargs)`: Метод, который используется для создания новых экземпляров класса. Он гарантирует, что все атрибуты класса инициализированы с правильными значениями.

### `ChatCompletionChunk`

**Описание**: Класс, который моделирует информацию об отдельном фрагменте ответа от GPT-4Free API.

**Inherits**: `BaseModel`

**Attributes**:

- `id (str)`: Идентификатор фрагмента ответа.
- `object (str)`: Тип фрагмента ответа.
- `created (int)`: Время создания фрагмента ответа.
- `model (str)`: Имя модели GPT-4Free.
- `provider (Optional[str])`: Провайдер модели GPT-4Free.
- `choices (List[ChatCompletionDeltaChoice])`: Список изменений, которые были применены к тексту ответа.
- `usage (UsageModel)`: Информация об использовании токенов в запросе и ответе.

**Methods**:

- `model_construct(cls, content: str, finish_reason: str, completion_id: str = None, created: int = None, usage: UsageModel = None)`: Метод, который используется для создания новых экземпляров класса. Он гарантирует, что все атрибуты класса инициализированы с правильными значениями.

### `ChatCompletionMessage`

**Описание**: Класс, который моделирует информацию о сообщении, которое было отправлено GPT-4Free API.

**Inherits**: `BaseModel`

**Attributes**:

- `role (str)`: Роль отправителя сообщения.
- `content (str)`: Текст сообщения.
- `tool_calls (list[ToolCallModel])`: Список вызовов функций инструментов, которые были сделаны в процессе генерации ответа.

**Methods**:

- `model_construct(cls, content: str, tool_calls: list = None)`: Метод, который используется для создания новых экземпляров класса. Он гарантирует, что все атрибуты класса инициализированы с правильными значениями.
- `save(self, filepath: str, allowd_types = None)`: Метод, который используется для сохранения сообщения в файл.

### `ChatCompletionChoice`

**Описание**: Класс, который моделирует информацию о выборе ответа, который был получен от GPT-4Free API.

**Inherits**: `BaseModel`

**Attributes**:

- `index (int)`: Индекс выбранного ответа.
- `message (ChatCompletionMessage)`: Сообщение, которое было отправлено GPT-4Free API.
- `finish_reason (str)`: Причина окончания генерации ответа.

**Methods**:

- `model_construct(cls, message: ChatCompletionMessage, finish_reason: str)`: Метод, который используется для создания новых экземпляров класса. Он гарантирует, что все атрибуты класса инициализированы с правильными значениями.

### `ChatCompletion`

**Описание**: Класс, который моделирует информацию о завершенном запросе к GPT-4Free API.

**Inherits**: `BaseModel`

**Attributes**:

- `id (str)`: Идентификатор запроса.
- `object (str)`: Тип запроса.
- `created (int)`: Время создания запроса.
- `model (str)`: Имя модели GPT-4Free.
- `provider (Optional[str])`: Провайдер модели GPT-4Free.
- `choices (list[ChatCompletionChoice])`: Список ответов, которые были получены от GPT-4Free API.
- `usage (UsageModel)`: Информация об использовании токенов в запросе и ответе.
- `conversation (dict)`: Данные о текущем разговоре с GPT-4Free.

**Methods**:

- `model_construct(cls, content: str, finish_reason: str, completion_id: str = None, created: int = None, tool_calls: list[ToolCallModel] = None, usage: UsageModel = None, conversation: dict = None)`: Метод, который используется для создания новых экземпляров класса. Он гарантирует, что все атрибуты класса инициализированы с правильными значениями.

### `ChatCompletionDelta`

**Описание**: Класс, который моделирует информацию об изменении, которое было применены к тексту ответа.

**Inherits**: `BaseModel`

**Attributes**:

- `role (str)`: Роль отправителя изменения.
- `content (str)`: Текст изменения.

**Methods**:

- `model_construct(cls, content: Optional[str])`: Метод, который используется для создания новых экземпляров класса. Он гарантирует, что все атрибуты класса инициализированы с правильными значениями.

### `ChatCompletionDeltaChoice`

**Описание**: Класс, который моделирует информацию о выборе изменения, которое было применены к тексту ответа.

**Inherits**: `BaseModel`

**Attributes**:

- `index (int)`: Индекс выбранного изменения.
- `delta (ChatCompletionDelta)`: Информация об изменении.
- `finish_reason (Optional[str])`: Причина окончания генерации ответа.

**Methods**:

- `model_construct(cls, delta: ChatCompletionDelta, finish_reason: Optional[str])`: Метод, который используется для создания новых экземпляров класса. Он гарантирует, что все атрибуты класса инициализированы с правильными значениями.

### `Image`

**Описание**: Класс, который моделирует информацию об изображении, которое было сгенерировано GPT-4Free API.

**Inherits**: `BaseModel`

**Attributes**:

- `url (Optional[str])`: URL изображения.
- `b64_json (Optional[str])`: Base64-кодированное представление изображения в формате JSON.
- `revised_prompt (Optional[str])`: Переработанный текст запроса, который использовался для генерации изображения.

**Methods**:

- `model_construct(cls, url: str = None, b64_json: str = None, revised_prompt: str = None)`: Метод, который используется для создания новых экземпляров класса. Он гарантирует, что все атрибуты класса инициализированы с правильными значениями.

### `ImagesResponse`

**Описание**: Класс, который моделирует информацию об ответе, содержащем список сгенерированных изображений.

**Inherits**: `BaseModel`

**Attributes**:

- `data (List[Image])`: Список изображений, которые были сгенерированы GPT-4Free API.
- `model (str)`: Имя модели GPT-4Free.
- `provider (str)`: Провайдер модели GPT-4Free.
- `created (int)`: Время создания ответа.

**Methods**:

- `model_construct(cls, data: List[Image], created: int = None, model: str = None, provider: str = None)`: Метод, который используется для создания новых экземпляров класса. Он гарантирует, что все атрибуты класса инициализированы с правильными значениями.

## Параметры

- `None`

## Примеры

```python
from hypotez.src.endpoints.gpt4free.g4f.client.stubs import ChatCompletion, ChatCompletionChoice, ChatCompletionMessage

# Создание экземпляра ChatCompletionMessage
message = ChatCompletionMessage.model_construct(
    content="Привет, мир!",
    tool_calls=[
        {
            "id": "tool_call_1",
            "type": "function",
            "function": {
                "name": "get_current_time",
                "arguments": "{}",
            },
        }
    ],
)

# Создание экземпляра ChatCompletionChoice
choice = ChatCompletionChoice.model_construct(
    message=message,
    finish_reason="stop",
)

# Создание экземпляра ChatCompletion
completion = ChatCompletion.model_construct(
    content="Привет, мир! Текущее время: <текущее время>",
    finish_reason="stop",
    choices=[choice],
    usage={
        "prompt_tokens": 10,
        "completion_tokens": 20,
        "total_tokens": 30,
        "prompt_tokens_details": {
            "cached_tokens": 0,
        },
        "completion_tokens_details": {
            "cached_tokens": 0,
        },
    },
)

# Вывод информации о completion
print(completion)
```

## Дополнительная информация

- Модуль `stubs.py` предназначен для использования в проекте `hypotez` для обработки ответов от GPT-4Free API.
- Классы в этом модуле упрощают работу с данными, которые возвращаются от API, делая их доступными в виде объектов Python.
- Документация  представлена в Markdown-формате.