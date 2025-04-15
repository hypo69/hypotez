# Модуль для работы со Stub моделями

## Обзор

Модуль содержит определения Stub моделей, используемых для представления данных при взаимодействии с различными API.
Он включает в себя классы для представления деталей токенов, использования моделей, вызовов инструментов, чат-завершений и изображений.

## Подробнее

Модуль предоставляет классы `BaseModel`, `TokenDetails`, `UsageModel`, `ToolFunctionModel`, `ToolCallModel`, `ChatCompletionChunk`, `ChatCompletionMessage`, `ChatCompletionChoice`, `ChatCompletion`, `ChatCompletionDelta`, `ChatCompletionDeltaChoice`, `Image` и `ImagesResponse`, которые используются для структурированного представления данных, получаемых и отправляемых при работе с API.

## Классы

### `BaseModel`

**Описание**: Базовый класс для всех моделей данных. Используется `pydantic` для определения структуры данных.
Если `pydantic` не установлен, предоставляет собственную реализацию.

**Атрибуты**:
- Нет явных атрибутов, так как это базовый класс.

**Методы**:
- `model_construct(**data)`: Создает экземпляр класса, устанавливая атрибуты на основе переданных данных.

### `TokenDetails`

**Описание**: Модель для хранения деталей об использовании токенов.

**Наследует**:
- `BaseModel`

**Атрибуты**:
- `cached_tokens` (int): Количество кэшированных токенов.

### `UsageModel`

**Описание**: Модель для хранения информации об использовании токенов при запросах к API.

**Наследует**:
- `BaseModel`

**Атрибуты**:
- `prompt_tokens` (int): Количество токенов, использованных во входном запросе.
- `completion_tokens` (int): Количество токенов, использованных в ответе.
- `total_tokens` (int): Общее количество использованных токенов.
- `prompt_tokens_details` (TokenDetails): Детали об использовании токенов во входном запросе.
- `completion_tokens_details` (TokenDetails): Детали об использовании токенов в ответе.

**Методы**:
- `model_construct(prompt_tokens=0, completion_tokens=0, total_tokens=0, prompt_tokens_details=None, completion_tokens_details=None, **kwargs)`: Создает экземпляр класса, устанавливая атрибуты на основе переданных данных. Если детали токенов не переданы, создает экземпляры `TokenDetails` с `cached_tokens = 0`.

### `ToolFunctionModel`

**Описание**: Модель для представления информации о функции инструмента, используемой в запросах к API.

**Наследует**:
- `BaseModel`

**Атрибуты**:
- `name` (str): Имя функции инструмента.
- `arguments` (str): Аргументы функции инструмента.

### `ToolCallModel`

**Описание**: Модель для представления вызова инструмента в запросах к API.

**Наследует**:
- `BaseModel`

**Атрибуты**:
- `id` (str): Идентификатор вызова инструмента.
- `type` (str): Тип вызова инструмента.
- `function` (ToolFunctionModel): Функция, которую необходимо вызвать.

**Методы**:
- `model_construct(function=None, **kwargs)`: Создает экземпляр класса, устанавливая атрибуты на основе переданных данных. Если функция не передана, создает экземпляр `ToolFunctionModel`.

### `ChatCompletionChunk`

**Описание**: Модель для представления частичного ответа (чанка) из API для чат-завершений.

**Наследует**:
- `BaseModel`

**Атрибуты**:
- `id` (str): Идентификатор чанка.
- `object` (str): Тип объекта (всегда "chat.completion.cunk").
- `created` (int): Временная метка создания чанка.
- `model` (str): Модель, используемая для генерации чанка.
- `provider` (Optional[str]): Провайдер, предоставивший чанк.
- `choices` (List[ChatCompletionDeltaChoice]): Список вариантов выбора для чанка.
- `usage` (UsageModel): Информация об использовании токенов.

**Методы**:
- `model_construct(content: str, finish_reason: str, completion_id: str = None, created: int = None, usage: UsageModel = None)`: Создает экземпляр класса, устанавливая атрибуты на основе переданных данных.

### `ChatCompletionMessage`

**Описание**: Модель для представления сообщения в чате.

**Наследует**:
- `BaseModel`

**Атрибуты**:
- `role` (str): Роль сообщения (например, "assistant").
- `content` (str): Содержимое сообщения.
- `tool_calls` (list[ToolCallModel]): Список вызовов инструментов, связанных с сообщением.

**Методы**:
- `model_construct(content: str, tool_calls: list = None)`: Создает экземпляр класса, устанавливая атрибуты на основе переданных данных.
- `save(self, filepath: str, allowd_types = None)`: Сохраняет содержимое сообщения в файл.

### `ChatCompletionChoice`

**Описание**: Модель для представления выбора в ответе API для чат-завершений.

**Наследует**:
- `BaseModel`

**Атрибуты**:
- `index` (int): Индекс выбора.
- `message` (ChatCompletionMessage): Сообщение, связанное с выбором.
- `finish_reason` (str): Причина завершения выбора.

**Методы**:
- `model_construct(message: ChatCompletionMessage, finish_reason: str)`: Создает экземпляр класса, устанавливая атрибуты на основе переданных данных.

### `ChatCompletion`

**Описание**: Модель для представления полного ответа из API для чат-завершений.

**Наследует**:
- `BaseModel`

**Атрибуты**:
- `id` (str): Идентификатор ответа.
- `object` (str): Тип объекта (всегда "chat.completion").
- `created` (int): Временная метка создания ответа.
- `model` (str): Модель, используемая для генерации ответа.
- `provider` (Optional[str]): Провайдер, предоставивший ответ.
- `choices` (list[ChatCompletionChoice]): Список вариантов выбора в ответе.
- `usage` (UsageModel): Информация об использовании токенов.
- `conversation` (dict): Контекст диалога.

**Методы**:
- `model_construct(content: str, finish_reason: str, completion_id: str = None, created: int = None, tool_calls: list[ToolCallModel] = None, usage: UsageModel = None, conversation: dict = None)`: Создает экземпляр класса, устанавливая атрибуты на основе переданных данных.

### `ChatCompletionDelta`

**Описание**: Модель для представления дельты (изменения) в чат-завершении.

**Наследует**:
- `BaseModel`

**Атрибуты**:
- `role` (str): Роль сообщения (например, "assistant").
- `content` (str): Содержимое сообщения.

**Методы**:
- `model_construct(cls, content: Optional[str])`: Создает экземпляр класса, устанавливая атрибуты на основе переданных данных.

### `ChatCompletionDeltaChoice`

**Описание**: Модель для представления выбора дельты в чат-завершении.

**Наследует**:
- `BaseModel`

**Атрибуты**:
- `index` (int): Индекс выбора.
- `delta` (ChatCompletionDelta): Дельта, связанная с выбором.
- `finish_reason` (Optional[str]): Причина завершения выбора.

**Методы**:
- `model_construct(cls, delta: ChatCompletionDelta, finish_reason: Optional[str])`: Создает экземпляр класса, устанавливая атрибуты на основе переданных данных.

### `Image`

**Описание**: Модель для представления изображения.

**Наследует**:
- `BaseModel`

**Атрибуты**:
- `url` (Optional[str]): URL изображения.
- `b64_json` (Optional[str]): Изображение в формате Base64 JSON.
- `revised_prompt` (Optional[str]): Уточненный запрос, использованный для генерации изображения.

**Методы**:
- `model_construct(cls, url: str = None, b64_json: str = None, revised_prompt: str = None)`: Создает экземпляр класса, устанавливая атрибуты на основе переданных данных.

### `ImagesResponse`

**Описание**: Модель для представления ответа API для генерации изображений.

**Наследует**:
- `BaseModel`

**Атрибуты**:
- `data` (List[Image]): Список сгенерированных изображений.
- `model` (str): Модель, использованная для генерации изображений.
- `provider` (str): Провайдер, предоставивший изображения.
- `created` (int): Временная метка создания ответа.

**Методы**:
- `model_construct(cls, data: List[Image], created: int = None, model: str = None, provider: str = None)`: Создает экземпляр класса, устанавливая атрибуты на основе переданных данных.

## Методы класса

### `ChatCompletionMessage.save`

```python
def save(self, filepath: str, allowd_types = None):
    """Сохраняет содержимое сообщения в файл.

    Args:
        filepath (str): Путь к файлу, в который будет сохранено содержимое.
        allowd_types: Разрешенные типы для сохранения.

    Raises:
        Exception: Если возникает ошибка при сохранении файла.

    Как работает функция:
        Функция `save` сохраняет содержимое объекта `ChatCompletionMessage` в файл, указанный в параметре `filepath`.
        Функция обрабатывает различные типы содержимого:
            - Если содержимое имеет атрибут "data", функция переименовывает файл из временного местоположения в указанный `filepath`.
            - Если содержимое начинается с "data:", функция извлекает данные URI и записывает их в файл как двоичные данные.
            - В противном случае функция фильтрует содержимое как Markdown и записывает его в файл как текст.

    Примеры:
        >>> message = ChatCompletionMessage.model_construct(content="Hello, world!")
        >>> message.save("hello.txt")
    """
    ...