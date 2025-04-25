# Модуль run_tools

## Обзор

Модуль `run_tools` содержит функциональность для обработки различных типов инструментов, используемых в модели `GPT4Free`. 

Этот модуль обеспечивает взаимодействие с инструментами, такими как `SEARCH` (поиск в Интернете), `CONTINUE` (продолжение генерации текста) и `BUCKET` (обработка данных из хранилища). 

## Подробности

Модуль `run_tools` содержит следующие основные элементы:

### Классы

#### `class ToolHandler`

**Описание**: Класс `ToolHandler` отвечает за обработку различных типов инструментов, используемых моделью `GPT4Free`.

**Атрибуты**: 

- Отсутствуют. 

**Методы**:

- `validate_arguments(data: dict) -> dict`: Проверяет и преобразовывает аргументы инструмента. Возвращает словарь с отфильтрованными аргументами. 
- `process_search_tool(messages: Messages, tool: dict) -> Messages`: Обрабатывает запросы к инструменту поиска. Возвращает обновленные сообщения и источники информации. 
- `process_continue_tool(messages: Messages, tool: dict, provider: Any) -> Tuple[Messages, Dict[str, Any]]`: Обрабатывает запросы к инструменту продолжения. Возвращает обновленные сообщения и дополнительные аргументы. 
- `process_bucket_tool(messages: Messages, tool: dict) -> Messages`: Обрабатывает запросы к инструменту "bucket". Возвращает обновленные сообщения.
- `process_tools(messages: Messages, tool_calls: List[dict], provider: Any) -> Tuple[Messages, Dict[str, Any]]`: Обрабатывает все вызовы инструментов и возвращает обновленные сообщения, источники информации и дополнительные аргументы.

#### `class AuthManager`

**Описание**: Класс `AuthManager` управляет ключами API для разных провайдеров.

**Атрибуты**: 

- Отсутствуют. 

**Методы**:

- `get_api_key_file(cls) -> Path`: Возвращает путь к файлу с ключом API для заданного провайдера. 
- `load_api_key(provider: Any) -> Optional[str]`: Загружает ключ API из конфигурационного файла, если требуется. Возвращает ключ API или `None`. 

#### `class ThinkingProcessor`

**Описание**: Класс `ThinkingProcessor` обрабатывает фрагменты "мышления" модели.

**Атрибуты**: 

- Отсутствуют. 

**Методы**:

- `process_thinking_chunk(chunk: str, start_time: float = 0) -> Tuple[float, List[Union[str, Reasoning]]]:`: Обрабатывает фрагмент "мышления" и возвращает время обработки и результат. 

### Функции

#### `async def perform_web_search(messages: Messages, web_search_param: Any) -> Tuple[Messages, Optional[Sources]]:`

**Назначение**: Выполняет поиск в Интернете и возвращает обновленные сообщения и источники.

**Параметры**:

- `messages (Messages)`: Список сообщений для обработки. 
- `web_search_param (Any)`: Параметры поиска в Интернете.

**Возвращает**:

- `Tuple[Messages, Optional[Sources]]`: Обновленные сообщения и список источников, если поиск был выполнен.

**Пример**:

```python
messages = [
    {'role': 'user', 'content': 'Расскажи мне о Париже'}
]

messages, sources = await perform_web_search(messages, 'Париж')

print(messages)
print(sources)
```

#### `async def async_iter_run_tools(provider: ProviderType, model: str, messages: Messages, tool_calls: Optional[List[dict]] = None, **kwargs) -> AsyncIterator:`

**Назначение**: Асинхронно запускает инструменты и выдает результаты.

**Параметры**:

- `provider (ProviderType)`: Тип провайдера.
- `model (str)`: Имя модели.
- `messages (Messages)`: Список сообщений для обработки.
- `tool_calls (Optional[List[dict]])`: Список вызовов инструментов.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:

- `AsyncIterator`: Асинхронный итератор, который выдает результаты обработки.

#### `def iter_run_tools(iter_callback: Callable, model: str, messages: Messages, provider: Optional[str] = None, tool_calls: Optional[List[dict]] = None, **kwargs) -> Iterator:`

**Назначение**: Синхронно запускает инструменты и выдает результаты.

**Параметры**:

- `iter_callback (Callable)`: Функция, которая генерирует результаты обработки. 
- `model (str)`: Имя модели. 
- `messages (Messages)`: Список сообщений для обработки. 
- `provider (Optional[str])`: Тип провайдера. 
- `tool_calls (Optional[List[dict]])`: Список вызовов инструментов. 
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:

- `Iterator`: Итератор, который выдает результаты обработки.

### Примеры

```python
# Вызов инструмента поиска
messages = [
    {'role': 'user', 'content': 'Что такое GPT-3?'}
]

tool_calls = [
    {
        'type': 'function',
        'function': {
            'name': 'SEARCH',
            'arguments': {
                'query': 'GPT-3'
            }
        }
    }
]

messages, sources = await ToolHandler.process_tools(messages, tool_calls, provider='OpenaiAccount')

print(messages)
print(sources)

# Вызов инструмента продолжения
messages = [
    {'role': 'user', 'content': 'Однажды, в далекой-далекой галактике...'}
]

tool_calls = [
    {
        'type': 'function',
        'function': {
            'name': 'CONTINUE'
        }
    }
]

messages, extra_kwargs = ToolHandler.process_tools(messages, tool_calls, provider='HuggingFaceAPI')

print(messages)
print(extra_kwargs)

# Вызов инструмента "bucket"
messages = [
    {'role': 'user', 'content': '{"bucket_id": "my_bucket"}'}
]

messages = ToolHandler.process_bucket_tool(messages, {'function': {'name': 'BUCKET'}})

print(messages)