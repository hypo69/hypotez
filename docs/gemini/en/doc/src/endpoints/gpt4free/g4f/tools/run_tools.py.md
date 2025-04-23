# Модуль `run_tools.py`

## Обзор

Модуль `run_tools.py` предназначен для обработки различных инструментов, используемых в проекте `hypotez`, таких как поиск в интернете, продолжение генерации текста и работа с хранилищем (bucket). Он содержит классы и функции для валидации аргументов инструментов, выполнения поисковых запросов, управления ключами API и обработки результатов работы инструментов.

## Подробности

Модуль включает в себя следующие основные компоненты:

- Класс `ToolHandler`: Обрабатывает различные типы инструментов, такие как поиск, продолжение и работа с хранилищем.
- Класс `AuthManager`: Управляет ключами API для различных провайдеров.
- Класс `ThinkingProcessor`: Обрабатывает "размышления" (thinking) в процессе генерации текста.
- Функции `perform_web_search`, `async_iter_run_tools`, `iter_run_tools`: Выполняют поиск в интернете, асинхронно и синхронно запускают инструменты.

## Содержание

- [Классы](#Классы)
    - [ToolHandler](#ToolHandler)
        - [validate_arguments](#validate_arguments)
        - [process_search_tool](#process_search_tool)
        - [process_continue_tool](#process_continue_tool)
        - [process_bucket_tool](#process_bucket_tool)
        - [process_tools](#process_tools)
    - [AuthManager](#AuthManager)
        - [get_api_key_file](#get_api_key_file)
        - [load_api_key](#load_api_key)
    - [ThinkingProcessor](#ThinkingProcessor)
        - [process_thinking_chunk](#process_thinking_chunk)
- [Функции](#Функции)
    - [perform_web_search](#perform_web_search)
    - [async_iter_run_tools](#async_iter_run_tools)
    - [iter_run_tools](#iter_run_tools)

## Классы

### `ToolHandler`

Обработчик различных типов инструментов.

#### `validate_arguments`

```python
    @staticmethod
    def validate_arguments(data: dict) -> dict:
```

Выполняет валидацию и парсинг аргументов инструментов.

**Параметры:**

- `data` (dict): Словарь с данными, содержащий аргументы инструмента.

**Возвращает:**

- `dict`: Отфильтрованный словарь аргументов.

**Как работает:**

- Проверяет наличие ключа `"arguments"` в словаре `data`.
- Если аргументы представлены в виде строки, пытается преобразовать их в словарь JSON.
- Проверяет, является ли тип данных аргументов словарем. Если нет, вызывает исключение `ValueError`.
- Фильтрует `None` значения из словаря аргументов.

#### `process_search_tool`

```python
    @staticmethod
    async def process_search_tool(messages: Messages, tool: dict) -> Messages:
```

Обрабатывает запросы инструмента поиска.

**Параметры:**

- `messages` (Messages): Список сообщений.
- `tool` (dict): Словарь с информацией об инструменте.

**Возвращает:**

- `Messages`: Обновленный список сообщений.
- `Sources`: Источники.

**Как работает:**

- Копирует список сообщений.
- Валидирует и извлекает аргументы инструмента.
- Выполняет поиск с использованием функции `do_search`.
- Обновляет содержимое последнего сообщения результатом поиска и источниками.

#### `process_continue_tool`

```python
    @staticmethod
    def process_continue_tool(messages: Messages, tool: dict, provider: Any) -> Tuple[Messages, Dict[str, Any]]:
```

Обрабатывает запросы инструмента продолжения.

**Параметры:**

- `messages` (Messages): Список сообщений.
- `tool` (dict): Словарь с информацией об инструменте.
- `provider` (Any): Провайдер.

**Возвращает:**

- `Tuple[Messages, Dict[str, Any]]`: Обновленный список сообщений и словарь дополнительных аргументов.

**Как работает:**

- Создает копию списка сообщений.
- Если провайдер не `"OpenaiAccount"` и не `"HuggingFaceAPI"`, добавляет новое сообщение с запросом на продолжение с последней строки предыдущего сообщения.
- Иначе устанавливает параметр `"action"` в `"continue"` для поддержки продолжения на стороне провайдера.

#### `process_bucket_tool`

```python
    @staticmethod
    def process_bucket_tool(messages: Messages, tool: dict) -> Messages:
```

Обрабатывает запросы инструмента хранилища (bucket).

**Параметры:**

- `messages` (Messages): Список сообщений.
- `tool` (dict): Словарь с информацией об инструменте.

**Возвращает:**

- `Messages`: Обновленный список сообщений.

**Как работает:**

- Копирует список сообщений.
- Определяет функцию `on_bucket` для чтения содержимого хранилища по `bucket_id`.
- Заменяет в содержимом каждого сообщения шаблоны `{"bucket_id":"([^"]*)"}` на содержимое соответствующего хранилища.
- Добавляет инструкции по цитированию источников, если в последнем сообщении есть упоминание источника.

#### `process_tools`

```python
    @staticmethod
    async def process_tools(messages: Messages, tool_calls: List[dict], provider: Any) -> Tuple[Messages, Dict[str, Any]]:
```

Обрабатывает все вызовы инструментов и возвращает обновленные сообщения и аргументы.

**Параметры:**

- `messages` (Messages): Список сообщений.
- `tool_calls` (List[dict]): Список вызовов инструментов.
- `provider` (Any): Провайдер.

**Возвращает:**

- `Tuple[Messages, Dict[str, Any]]`: Обновленный список сообщений, источники и словарь дополнительных аргументов.

**Как работает:**

- Копирует список сообщений.
- Итерируется по списку вызовов инструментов.
- Для каждого вызова определяет имя функции и вызывает соответствующий обработчик (`process_search_tool`, `process_continue_tool`, `process_bucket_tool`).
- Обновляет список сообщений и собирает дополнительные аргументы.

### `AuthManager`

Управляет ключами API.

#### `get_api_key_file`

```python
    @staticmethod
    def get_api_key_file(cls) -> Path:
```

Получает путь к файлу ключа API для указанного провайдера.

**Параметры:**

- `cls`: Класс провайдера.

**Возвращает:**

- `Path`: Путь к файлу ключа API.

**Как работает:**

- Формирует имя файла ключа API на основе имени класса провайдера.
- Возвращает путь к файлу в директории cookies.

#### `load_api_key`

```python
    @staticmethod
    def load_api_key(provider: Any) -> Optional[str]:
```

Загружает ключ API из конфигурационного файла, если это необходимо.

**Параметры:**

- `provider` (Any): Провайдер.

**Возвращает:**

- `Optional[str]`: Ключ API или `None`, если ключ не требуется или не найден.

**Как работает:**

- Проверяет, требуется ли провайдеру аутентификация.
- Формирует путь к файлу ключа API.
- Пытается прочитать ключ из файла.
- В случае ошибки логирует информацию об ошибке и возвращает `None`.

### `ThinkingProcessor`

Обрабатывает части "размышлений" (thinking chunks).

#### `process_thinking_chunk`

```python
    @staticmethod
    def process_thinking_chunk(chunk: str, start_time: float = 0) -> Tuple[float, List[Union[str, Reasoning]]]:
```

Обрабатывает часть "размышлений" и возвращает время и результаты.

**Параметры:**

- `chunk` (str): Часть текста для обработки.
- `start_time` (float, optional): Время начала обработки. По умолчанию `0`.

**Возвращает:**

- `Tuple[float, List[Union[str, Reasoning]]]`: Время и список результатов.

**Как работает:**

- Обрабатывает различные случаи:
    - Не "размышления".
    - Начало "размышлений" (`<think>`).
    - Окончание "размышлений" (`</think>`).
    - Продолжение "размышлений".
- Формирует объекты `Reasoning` для представления статуса обработки.
- Вычисляет продолжительность "размышлений".

## Функции

### `perform_web_search`

```python
async def perform_web_search(messages: Messages, web_search_param: Any) -> Tuple[Messages, Optional[Sources]]:
```

Выполняет поиск в интернете и возвращает обновленные сообщения и источники.

**Параметры:**

- `messages` (Messages): Список сообщений.
- `web_search_param` (Any): Параметр для поиска в интернете.

**Возвращает:**

- `Tuple[Messages, Optional[Sources]]`: Обновленный список сообщений и источники.

**Как работает:**

- Копирует список сообщений.
- Если параметр для поиска не указан, возвращает исходные сообщения и `None` в качестве источников.
- Выполняет поиск с использованием функции `do_search`.
- В случае ошибки логирует информацию об ошибке.

### `async_iter_run_tools`

```python
async def async_iter_run_tools(
    provider: ProviderType, 
    model: str, 
    messages: Messages, 
    tool_calls: Optional[List[dict]] = None, 
    **kwargs
) -> AsyncIterator:
```

Асинхронно запускает инструменты и возвращает результаты.

**Параметры:**

- `provider` (ProviderType): Провайдер.
- `model` (str): Модель.
- `messages` (Messages): Список сообщений.
- `tool_calls` (Optional[List[dict]], optional): Список вызовов инструментов. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает:**

- `AsyncIterator`: Асинхронный итератор результатов.

**Как работает:**

- Выполняет поиск в интернете, если указан параметр `web_search`.
- Загружает ключ API, если это необходимо.
- Обрабатывает вызовы инструментов с использованием `ToolHandler.process_tools`.
- Генерирует ответ с использованием `provider.get_async_create_function`.
- Возвращает результаты и источники (если есть).

### `iter_run_tools`

```python
def iter_run_tools(
    iter_callback: Callable,
    model: str,
    messages: Messages,
    provider: Optional[str] = None,
    tool_calls: Optional[List[dict]] = None,
    **kwargs
) -> Iterator:
```

Синхронно запускает инструменты и возвращает результаты.

**Параметры:**

- `iter_callback` (Callable): Функция обратного вызова для итерации.
- `model` (str): Модель.
- `messages` (Messages): Список сообщений.
- `provider` (Optional[str], optional): Провайдер. По умолчанию `None`.
- `tool_calls` (Optional[List[dict]], optional): Список вызовов инструментов. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает:**

- `Iterator`: Итератор результатов.

**Как работает:**

- Выполняет поиск в интернете, если указан параметр `web_search`.
- Загружает ключ API, если это необходимо.
- Обрабатывает вызовы инструментов.
- Обрабатывает части ответа с использованием `ThinkingProcessor`.
- Возвращает результаты и источники (если есть).