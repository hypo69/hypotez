# Модуль run_tools
## Обзор
Этот модуль предоставляет функции и классы для обработки вызовов инструментов в рамках взаимодействия с моделями генерации текста, такими как GPT-4 Free.

## Детали
Модуль `run_tools` обеспечивает функциональность для обработки различных типов вызовов инструментов, таких как поиск в Интернете, продолжение текста и использование хранилища данных (Bucket). 

## Классы
### `class ToolHandler`
**Описание**: Класс `ToolHandler` отвечает за обработку различных типов вызовов инструментов.

**Атрибуты**:  Нет

**Методы**: 

 - `validate_arguments(data: dict) -> dict`:  
    **Описание**: Проверяет и парсит аргументы для функций инструментов.
    **Параметры**:
     - `data (dict)`: Словарь, содержащий аргументы функции инструмента.
    **Возвращает**:
     - `dict`: Словарь с отфильтрованными аргументами.
    **Исключения**:
     - `ValueError`: Если аргументы функции инструмента не являются словарем или строкой JSON.

 - `process_search_tool(messages: Messages, tool: dict) -> Messages`: 
    **Описание**: Обрабатывает запросы к инструменту поиска.
    **Параметры**:
     - `messages (Messages)`: Список сообщений.
     - `tool (dict)`: Словарь с описанием инструмента.
    **Возвращает**:
     - `Messages`: Обновленный список сообщений с результатами поиска.

 - `process_continue_tool(messages: Messages, tool: dict, provider: Any) -> Tuple[Messages, Dict[str, Any]]`: 
    **Описание**: Обрабатывает запросы к инструменту продолжения текста.
    **Параметры**:
     - `messages (Messages)`: Список сообщений.
     - `tool (dict)`: Словарь с описанием инструмента.
     - `provider (Any)`: Провайдер модели.
    **Возвращает**:
     - `Tuple[Messages, Dict[str, Any]]`: Кортеж, содержащий обновленный список сообщений и дополнительные аргументы.

 - `process_bucket_tool(messages: Messages, tool: dict) -> Messages`: 
    **Описание**: Обрабатывает запросы к инструменту хранилища данных (Bucket).
    **Параметры**:
     - `messages (Messages)`: Список сообщений.
     - `tool (dict)`: Словарь с описанием инструмента.
    **Возвращает**:
     - `Messages`: Обновленный список сообщений с данными из хранилища.

 - `process_tools(messages: Messages, tool_calls: List[dict], provider: Any) -> Tuple[Messages, Dict[str, Any]]`: 
    **Описание**: Обрабатывает все вызовы инструментов и возвращает обновленные сообщения и дополнительные аргументы.
    **Параметры**:
     - `messages (Messages)`: Список сообщений.
     - `tool_calls (List[dict])`: Список вызовов инструментов.
     - `provider (Any)`: Провайдер модели.
    **Возвращает**:
     - `Tuple[Messages, Dict[str, Any]]`: Кортеж, содержащий обновленный список сообщений, источники информации (sources) и дополнительные аргументы.
  
### `class AuthManager`
**Описание**: Класс `AuthManager` отвечает за управление ключами API.

**Атрибуты**:  Нет

**Методы**:

 - `get_api_key_file(cls) -> Path`: 
    **Описание**: Возвращает путь к файлу с ключом API для провайдера.
    **Параметры**:
     - `cls`: Класс провайдера.
    **Возвращает**:
     - `Path`: Путь к файлу с ключом API.

 - `load_api_key(provider: Any) -> Optional[str]`: 
    **Описание**: Загружает ключ API из конфигурационного файла, если необходимо.
    **Параметры**:
     - `provider (Any)`: Провайдер модели.
    **Возвращает**:
     - `Optional[str]`: Ключ API, если он найден.

### `class ThinkingProcessor`
**Описание**: Класс `ThinkingProcessor` отвечает за обработку фрагментов размышлений (thinking chunks).

**Атрибуты**:  Нет

**Методы**: 

 - `process_thinking_chunk(chunk: str, start_time: float = 0) -> Tuple[float, List[Union[str, Reasoning]]]`: 
    **Описание**: Обрабатывает фрагмент размышлений и возвращает время обработки и результаты.
    **Параметры**:
     - `chunk (str)`: Фрагмент текста.
     - `start_time (float, optional):`: Время начала размышления. По умолчанию 0.
    **Возвращает**:
     - `Tuple[float, List[Union[str, Reasoning]]]`: Кортеж, содержащий время конца размышления и список результатов (строки или объекты Reasoning).
 

## Функции
### `async def perform_web_search(messages: Messages, web_search_param: Any) -> Tuple[Messages, Optional[Sources]]`
**Описание**: Выполняет поиск в Интернете и возвращает обновленные сообщения и источники информации.
**Параметры**:
 - `messages (Messages)`: Список сообщений.
 - `web_search_param (Any)`: Параметр, определяющий запрос поиска (может быть строкой или `True` для автоматического поиска).
**Возвращает**:
 - `Tuple[Messages, Optional[Sources]]`: Кортеж, содержащий обновленный список сообщений и источники информации.
**Исключения**:
 - `Exception`: Если возникла ошибка при выполнении поиска.

### `async def async_iter_run_tools(provider: ProviderType, model: str, messages: Messages, tool_calls: Optional[List[dict]] = None, **kwargs) -> AsyncIterator`
**Описание**: Асинхронно запускает инструменты и возвращает результаты.
**Параметры**:
 - `provider (ProviderType)`: Провайдер модели.
 - `model (str)`: Название модели.
 - `messages (Messages)`: Список сообщений.
 - `tool_calls (Optional[List[dict]], optional)`: Список вызовов инструментов. По умолчанию `None`.
 - `kwargs (dict)`: Дополнительные аргументы.
**Возвращает**:
 - `AsyncIterator`: Асинхронный итератор, который позволяет получить результаты работы инструментов.

### `def iter_run_tools(iter_callback: Callable, model: str, messages: Messages, provider: Optional[str] = None, tool_calls: Optional[List[dict]] = None, **kwargs) -> Iterator`
**Описание**: Запускает инструменты синхронно и возвращает результаты.
**Параметры**:
 - `iter_callback (Callable)`: Функция-обработчик, возвращающая результаты работы инструментов.
 - `model (str)`: Название модели.
 - `messages (Messages)`: Список сообщений.
 - `provider (Optional[str], optional)`: Провайдер модели. По умолчанию `None`.
 - `tool_calls (Optional[List[dict]], optional)`: Список вызовов инструментов. По умолчанию `None`.
 - `kwargs (dict)`: Дополнительные аргументы.
**Возвращает**:
 - `Iterator`: Итератор, который позволяет получить результаты работы инструментов.

## Параметры
- `messages (Messages)`: Список сообщений, представляющий историю взаимодействия с моделью.
- `tool_calls (List[dict])`: Список вызовов инструментов, где каждый элемент представляет описание инструмента и его аргументов.
- `provider (Any)`: Провайдер модели, определяющий, какая модель используется (например, GPT-4 Free, Google Gemini).
- `model (str)`: Название модели, например, "gpt-4", "gemini-pro".
- `web_search_param (Any)`: Параметр, определяющий запрос поиска (может быть строкой или `True` для автоматического поиска).
- `api_key (str)`: Ключ API для провайдера модели.
- `chunk (str)`: Фрагмент текста, который нужно обработать.
- `start_time (float)`: Время начала размышления.
- `data (dict)`: Словарь с аргументами функции инструмента.
- `tool (dict)`: Словарь с описанием инструмента, включая его тип и аргументы.

## Примеры
- **Пример вызова `ToolHandler.process_tools()`**: 
```python
# Список вызовов инструментов
tool_calls = [
    {"type": "function", "function": {"name": "search_tool", "arguments": {"query": "What is the capital of France?"}}},
    {"type": "function", "function": {"name": "continue_tool"}}
]

# Список сообщений
messages = [
    {"role": "user", "content": "What is the capital of France?"}
]

# Провайдер модели
provider = "OpenaiAccount"

# Вызов функции
messages, sources, extra_kwargs = await ToolHandler.process_tools(messages, tool_calls, provider)
```

- **Пример вызова `ThinkingProcessor.process_thinking_chunk()`**: 
```python
# Фрагмент текста
chunk = "The capital of France is <think>Paris</think>."

# Время начала размышления
start_time = 0

# Вызов функции
thinking_start_time, results = ThinkingProcessor.process_thinking_chunk(chunk, start_time)

# Вывод результатов
print(f"Thinking start time: {thinking_start_time}")
print(f"Results: {results}")
```

- **Пример вызова `async_iter_run_tools()`**:
```python
# Провайдер модели
provider = "OpenaiAccount"

# Название модели
model = "gpt-4"

# Список сообщений
messages = [
    {"role": "user", "content": "What is the capital of France?"}
]

# Вызов функции
async for result in async_iter_run_tools(provider, model, messages):
    print(f"Result: {result}")
```

- **Пример вызова `iter_run_tools()`**:
```python
# Функция-обработчик
def iter_callback(model: str, messages: Messages, provider: Any, **kwargs) -> Iterator:
    # Логика обработки модели
    ...
    yield chunk
    ...

# Название модели
model = "gpt-4"

# Список сообщений
messages = [
    {"role": "user", "content": "What is the capital of France?"}
]

# Вызов функции
for result in iter_run_tools(iter_callback, model, messages):
    print(f"Result: {result}")