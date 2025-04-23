# Модуль для работы с инструментами (tools) g4f
## Обзор

Модуль `run_tools.py` предоставляет функциональность для выполнения различных инструментов, таких как поиск в интернете, продолжение генерации текста и работа с "bucket"-хранилищем. Он также включает в себя управление ключами API и обработку промежуточных результатов (thinking chunks).

## Подробней

Этот модуль содержит классы и функции, необходимые для работы с инструментами, используемыми в g4f. Он включает в себя:

*   Обработчик инструментов (`ToolHandler`) для выполнения различных типов инструментов.
*   Менеджер аутентификации (`AuthManager`) для управления ключами API.
*   Процессор этапов размышления (`ThinkingProcessor`) для обработки промежуточных результатов.
*   Асинхронные и синхронные функции для запуска инструментов.

## Классы

### `ToolHandler`

**Описание**: Обработчик различных типов инструментов.

**Методы**:

*   `validate_arguments(data: dict) -> dict`: Валидирует и парсит аргументы инструментов.
*   `process_search_tool(messages: Messages, tool: dict) -> Messages`: Обрабатывает запросы инструмента поиска.
*   `process_continue_tool(messages: Messages, tool: dict, provider: Any) -> Tuple[Messages, Dict[str, Any]]`: Обрабатывает запросы инструмента продолжения генерации.
*   `process_bucket_tool(messages: Messages, tool: dict) -> Messages`: Обрабатывает запросы инструмента bucket.
*   `process_tools(messages: Messages, tool_calls: List[dict], provider: Any) -> Tuple[Messages, Dict[str, Any]]`: Обрабатывает все вызовы инструментов и возвращает обновленные сообщения и kwargs.

**Принцип работы**:
Класс `ToolHandler` предоставляет статические методы для обработки различных типов инструментов. `validate_arguments` проверяет и преобразует аргументы инструментов в словарь. `process_search_tool` выполняет поиск в интернете и обновляет сообщения. `process_continue_tool` подготавливает сообщения для продолжения генерации текста. `process_bucket_tool` обрабатывает запросы к "bucket"-хранилищу. `process_tools` координирует вызов и обработку нескольких инструментов.

### `AuthManager`

**Описание**: Управляет ключами API.

**Методы**:

*   `get_api_key_file(cls) -> Path`: Возвращает путь к файлу ключа API для провайдера.
*   `load_api_key(provider: Any) -> Optional[str]`: Загружает ключ API из файла конфигурации, если необходимо.

**Принцип работы**:
Класс `AuthManager` предоставляет статические методы для управления ключами API. `get_api_key_file` определяет местоположение файла, в котором хранится ключ API для конкретного провайдера. `load_api_key` пытается загрузить ключ API из этого файла, если провайдеру требуется аутентификация.

### `ThinkingProcessor`

**Описание**: Обрабатывает промежуточные этапы размышления.

**Методы**:

*   `process_thinking_chunk(chunk: str, start_time: float = 0) -> Tuple[float, List[Union[str, Reasoning]]]`: Обрабатывает "thinking chunk" и возвращает время и результаты.

**Принцип работы**:
Класс `ThinkingProcessor` предоставляет статический метод `process_thinking_chunk`, который анализирует текст на наличие специальных тегов `<think>` и `</think>`, используемых для обозначения начала и конца этапов "размышления". Метод извлекает текст до, между и после этих тегов, а также вычисляет продолжительность этапа "размышления" и возвращает результаты в виде списка, содержащего либо строки с текстом, либо объекты `Reasoning`, представляющие этапы "размышления".

## Функции

### `validate_arguments`

```python
@staticmethod
def validate_arguments(data: dict) -> dict:
    """Validate and parse tool arguments"""
    if "arguments" in data:
        if isinstance(data["arguments"], str):
            data["arguments"] = json.loads(data["arguments"])
        if not isinstance(data["arguments"], dict):
            raise ValueError("Tool function arguments must be a dictionary or a json string")
        else:
            return filter_none(**data["arguments"])
    else:
        return {}
```

**Назначение**: Валидирует и преобразует аргументы инструментов в словарь.

**Параметры**:

*   `data` (dict): Словарь, содержащий данные инструмента, включая аргументы.

**Возвращает**:

*   `dict`: Словарь с валидированными и отфильтрованными аргументами.

**Вызывает исключения**:

*   `ValueError`: Если аргументы инструмента не являются словарем или JSON-строкой.

**Как работает функция**:

1.  Проверяет наличие ключа `"arguments"` в словаре `data`.
2.  Если ключ `"arguments"` присутствует, проверяет, является ли значение строкой. Если да, пытается преобразовать его из JSON в словарь.
3.  Проверяет, является ли `data["arguments"]` словарем. Если нет, вызывает исключение `ValueError`.
4.  Если `data["arguments"]` является словарем, вызывает функцию `filter_none` для удаления элементов со значением `None` и возвращает результат.
5.  Если ключ `"arguments"` отсутствует, возвращает пустой словарь.

### `process_search_tool`

```python
@staticmethod
async def process_search_tool(messages: Messages, tool: dict) -> Messages:
    """Process search tool requests"""
    messages = messages.copy()
    args = ToolHandler.validate_arguments(tool["function"])
    messages[-1]["content"], sources = await do_search(
        messages[-1]["content"],
        **args
    )
    return messages, sources
```

**Назначение**: Обрабатывает запросы инструмента поиска.

**Параметры**:

*   `messages` (Messages): Список сообщений.
*   `tool` (dict): Словарь, содержащий информацию об инструменте.

**Возвращает**:

*   `Messages`: Обновленный список сообщений с результатами поиска.

**Как работает функция**:

1.  Создает копию списка сообщений `messages`.
2.  Извлекает и валидирует аргументы инструмента из `tool["function"]`, используя `ToolHandler.validate_arguments`.
3.  Вызывает асинхронную функцию `do_search` с контентом последнего сообщения и валидированными аргументами.
4.  Обновляет контент последнего сообщения в списке `messages` результатом поиска.
5.  Возвращает обновленный список сообщений и источники поиска.

### `process_continue_tool`

```python
@staticmethod
def process_continue_tool(messages: Messages, tool: dict, provider: Any) -> Tuple[Messages, Dict[str, Any]]:
    """Process continue tool requests"""
    kwargs = {}
    if provider not in ("OpenaiAccount", "HuggingFaceAPI"):
        messages = messages.copy()
        last_line = messages[-1]["content"].strip().splitlines()[-1]
        content = f"Carry on from this point:\\n{last_line}"
        messages.append({"role": "user", "content": content})
    else:
        # Enable provider native continue
        kwargs["action"] = "continue"
    return messages, kwargs
```

**Назначение**: Обрабатывает запросы инструмента продолжения генерации.

**Параметры**:

*   `messages` (Messages): Список сообщений.
*   `tool` (dict): Словарь, содержащий информацию об инструменте.
*   `provider` (Any): Провайдер, используемый для генерации.

**Возвращает**:

*   `Tuple[Messages, Dict[str, Any]]`: Обновленный список сообщений и словарь с дополнительными аргументами.

**Как работает функция**:

1.  Инициализирует пустой словарь `kwargs`.
2.  Проверяет, является ли провайдер одним из "OpenaiAccount" или "HuggingFaceAPI".
3.  Если провайдер не является одним из них, создает копию списка сообщений `messages`, извлекает последнюю строку из контента последнего сообщения и добавляет новое сообщение с ролью "user" и контентом, содержащим запрос на продолжение генерации с последней строки.
4.  Если провайдер является одним из них, добавляет в словарь `kwargs` ключ `"action"` со значением `"continue"`.
5.  Возвращает обновленный список сообщений и словарь `kwargs`.

### `process_bucket_tool`

```python
@staticmethod
def process_bucket_tool(messages: Messages, tool: dict) -> Messages:
    """Process bucket tool requests"""
    messages = messages.copy()

    def on_bucket(match):
        return "".join(read_bucket(get_bucket_dir(match.group(1))))

    has_bucket = False
    for message in messages:
        if "content" in message and isinstance(message["content"], str):
            new_message_content = re.sub(r'{"bucket_id":"([^"]*)"}', on_bucket, message["content"])
            if new_message_content != message["content"]:
                has_bucket = True
                message["content"] = new_message_content

    last_message_content = messages[-1]["content"]
    if has_bucket and isinstance(last_message_content, str):
        if "\\nSource: " in last_message_content:
            messages[-1]["content"] = last_message_content + BUCKET_INSTRUCTIONS

    return messages
```

**Назначение**: Обрабатывает запросы инструмента bucket.

**Параметры**:

*   `messages` (Messages): Список сообщений.
*   `tool` (dict): Словарь, содержащий информацию об инструменте.

**Возвращает**:

*   `Messages`: Обновленный список сообщений с результатами обработки bucket.

**Внутренние функции**:

*   `on_bucket(match)`: Извлекает содержимое bucket по его ID.

**Как работает функция**:

1.  Создает копию списка сообщений `messages`.
2.  Определяет внутреннюю функцию `on_bucket`, которая принимает объект `match` (результат регулярного выражения) и возвращает содержимое bucket с ID, извлеченным из `match`.
3.  Инициализирует переменную `has_bucket` значением `False`.
4.  Перебирает сообщения в списке `messages`.
5.  Для каждого сообщения проверяет, содержит ли оно ключ `"content"` и является ли его значение строкой.
6.  Если сообщение удовлетворяет условиям, заменяет в его контенте все вхождения шаблона `{"bucket_id":"([^"]*)"}` на результат вызова функции `on_bucket` с соответствующим объектом `match`.
7.  Если после замены контент сообщения изменился, устанавливает `has_bucket` в `True`.
8.  После обработки всех сообщений проверяет, было ли обнаружено использование bucket (`has_bucket == True`) и является ли контент последнего сообщения строкой.
9.  Если оба условия выполняются, добавляет к контенту последнего сообщения инструкцию `BUCKET_INSTRUCTIONS`.
10. Возвращает обновленный список сообщений.

### `process_tools`

```python
@staticmethod
async def process_tools(messages: Messages, tool_calls: List[dict], provider: Any) -> Tuple[Messages, Dict[str, Any]]:
    """Process all tool calls and return updated messages and kwargs"""
    if not tool_calls:
        return messages, {}

    extra_kwargs = {}
    messages = messages.copy()
    sources = None

    for tool in tool_calls:
        if tool.get("type") != "function":
            continue

        function_name = tool.get("function", {}).get("name")

        if function_name == TOOL_NAMES["SEARCH"]:
            messages, sources = await ToolHandler.process_search_tool(messages, tool)

        elif function_name == TOOL_NAMES["CONTINUE"]:
            messages, kwargs = ToolHandler.process_continue_tool(messages, tool, provider)
            extra_kwargs.update(kwargs)

        elif function_name == TOOL_NAMES["BUCKET"]:
            messages = ToolHandler.process_bucket_tool(messages, tool)

    return messages, sources, extra_kwargs
```

**Назначение**: Обрабатывает все вызовы инструментов и возвращает обновленные сообщения и kwargs.

**Параметры**:

*   `messages` (Messages): Список сообщений.
*   `tool_calls` (List[dict]): Список вызовов инструментов.
*   `provider` (Any): Провайдер, используемый для генерации.

**Возвращает**:

*   `Tuple[Messages, Dict[str, Any]]`: Обновленный список сообщений и словарь с дополнительными аргументами.

**Как работает функция**:

1.  Проверяет, является ли список `tool_calls` пустым. Если да, возвращает исходный список сообщений и пустой словарь.
2.  Инициализирует пустой словарь `extra_kwargs`.
3.  Создает копию списка сообщений `messages`.
4.  Перебирает вызовы инструментов в списке `tool_calls`.
5.  Для каждого вызова инструмента проверяет, является ли его тип `"function"`. Если нет, переходит к следующему вызову.
6.  Извлекает имя функции из вызова инструмента.
7.  В зависимости от имени функции вызывает соответствующий метод `ToolHandler` (`process_search_tool`, `process_continue_tool` или `process_bucket_tool`).
8.  Обновляет `extra_kwargs` результатами, полученными от `process_continue_tool`.
9.  Возвращает обновленный список сообщений, источники и словарь `extra_kwargs`.

### `get_api_key_file`

```python
@staticmethod
def get_api_key_file(cls) -> Path:
    """Get the path to the API key file for a provider"""
    return Path(get_cookies_dir()) / f"api_key_{cls.parent if hasattr(cls, 'parent') else cls.__name__}.json"
```

**Назначение**: Возвращает путь к файлу ключа API для провайдера.

**Параметры**:

*   `cls`: Класс провайдера.

**Возвращает**:

*   `Path`: Путь к файлу ключа API.

**Как работает функция**:

1.  Определяет имя файла ключа API, используя имя класса провайдера или имя его родительского класса (если у класса есть родительский класс).
2.  Формирует путь к файлу, объединяя директорию для хранения cookie (полученную с помощью `get_cookies_dir()`) и имя файла.
3.  Возвращает объект `Path`, представляющий путь к файлу ключа API.

### `load_api_key`

```python
@staticmethod
def load_api_key(provider: Any) -> Optional[str]:
    """Load API key from config file if needed"""
    if not getattr(provider, "needs_auth", False):
        return None

    auth_file = AuthManager.get_api_key_file(provider)
    try:
        if auth_file.exists():
            with auth_file.open("r") as f:
                auth_result = json.load(f)
            return auth_result.get("api_key")
    except (json.JSONDecodeError, PermissionError, FileNotFoundError) as ex:
        debug.error(f"Failed to load API key: {ex.__class__.__name__}: {ex}")
    return None
```

**Назначение**: Загружает ключ API из файла конфигурации, если необходимо.

**Параметры**:

*   `provider` (Any): Провайдер, для которого необходимо загрузить ключ API.

**Возвращает**:

*   `Optional[str]`: Ключ API или `None`, если ключ не требуется или не найден.

**Как работает функция**:

1.  Проверяет, требует ли провайдер аутентификацию, используя атрибут `needs_auth`. Если нет, возвращает `None`.
2.  Получает путь к файлу ключа API с помощью метода `AuthManager.get_api_key_file`.
3.  Пытается открыть файл и загрузить из него ключ API.
4.  В случае успеха возвращает ключ API.
5.  В случае ошибки (например, файл не существует, ошибка JSON, нет прав доступа) логирует сообщение об ошибке и возвращает `None`.

### `process_thinking_chunk`

```python
@staticmethod
def process_thinking_chunk(chunk: str, start_time: float = 0) -> Tuple[float, List[Union[str, Reasoning]]]:
    """Process a thinking chunk and return timing and results."""
    results = []

    # Handle non-thinking chunk
    if not start_time and "<think>" not in chunk and "</think>" not in chunk:
        return 0, [chunk]

    # Handle thinking start
    if "<think>" in chunk and "`<think>`" not in chunk:
        before_think, *after = chunk.split("<think>", 1)

        if before_think:
            results.append(before_think)

        results.append(Reasoning(status="🤔 Is thinking...", is_thinking="<think>"))

        if after:
            if "</think>" in after[0]:
                after, *after_end = after[0].split("</think>", 1)
                results.append(Reasoning(after))
                results.append(Reasoning(status="Finished", is_thinking="</think>"))
                if after_end:
                    results.append(after_end[0])
                return 0, results
            else:
                results.append(Reasoning(after[0]))

        return time.time(), results

    # Handle thinking end
    if "</think>" in chunk:
        before_end, *after = chunk.split("</think>", 1)

        if before_end:
            results.append(Reasoning(before_end))

        thinking_duration = time.time() - start_time if start_time > 0 else 0

        status = f"Thought for {thinking_duration:.2f}s" if thinking_duration > 1 else "Finished"
        results.append(Reasoning(status=status, is_thinking="</think>"))

        # Make sure to handle text after the closing tag
        if after and after[0].strip():
            results.append(after[0])

        return 0, results

    # Handle ongoing thinking
    if start_time:
        return start_time, [Reasoning(chunk)]

    return start_time, [chunk]
```

**Назначение**: Обрабатывает "thinking chunk" и возвращает время и результаты.

**Параметры**:

*   `chunk` (str): Строка, содержащая "thinking chunk".
*   `start_time` (float, optional): Время начала обработки "thinking chunk". По умолчанию `0`.

**Возвращает**:

*   `Tuple[float, List[Union[str, Reasoning]]]`: Кортеж, содержащий время (время начала, если "thinking" продолжается, или `0`, если "thinking" закончился или не было "thinking") и список результатов обработки.

**Как работает функция**:

1.  Инициализирует пустой список `results`.
2.  Проверяет, является ли текущий чанк "не-thinking" чанком. Если `start_time` равно `0` и в чанке нет тегов `<think>` и `</think>`, возвращает `0` и список, содержащий исходный чанк.
3.  Проверяет, начинается ли "thinking" этап. Если в чанке есть `<think>`, но нет `` ``, разделяет чанк на части до и после `<think>`.
    *   Если есть текст до `<think>`, добавляет его в `results`.
    *   Добавляет в `results` объект `Reasoning` со статусом "🤔 Is thinking..." и тегом `<think>`.
    *   Если есть текст после `<think>`, проверяет, есть ли в нем `</think>`.
        *   Если есть, разделяет текст на части до и после `</think>`, добавляет в `results` объекты `Reasoning` для каждой части и возвращает `0` и `results`.
        *   Если нет, добавляет в `results` объект `Reasoning` с текстом после `<think>` и возвращает текущее время и `results`.
4.  Проверяет, заканчивается ли "thinking" этап. Если в чанке есть `</think>`, разделяет чанк на части до и после `</think>`.
    *   Если есть текст до `</think>`, добавляет в `results` объект `Reasoning` с этим текстом.
    *   Вычисляет продолжительность "thinking" этапа и добавляет в `results` объект `Reasoning` со статусом, указывающим на продолжительность или завершение этапа, и тегом `</think>`.
    *   Если есть текст после `</think>`, добавляет его в `results`.
    *   Возвращает `0` и `results`.
5.  Если "thinking" этап продолжается (есть `start_time`), возвращает `start_time` и список, содержащий объект `Reasoning` с исходным чанком.
6.  Если ни одно из вышеперечисленных условий не выполняется, возвращает `start_time` и список, содержащий исходный чанк.

### `perform_web_search`

```python
async def perform_web_search(messages: Messages, web_search_param: Any) -> Tuple[Messages, Optional[Sources]]:
    """Perform web search and return updated messages and sources"""
    messages = messages.copy()
    sources = None

    if not web_search_param:
        return messages, sources

    try:
        search_query = web_search_param if isinstance(web_search_param, str) and web_search_param != "true" else None
        messages[-1]["content"], sources = await do_search(messages[-1]["content"], search_query)
    except Exception as ex:
        debug.error(f"Couldn\'t do web search: {ex.__class__.__name__}: {ex}")

    return messages, sources
```

**Назначение**: Выполняет поиск в интернете и возвращает обновленные сообщения и источники.

**Параметры**:

*   `messages` (Messages): Список сообщений.
*   `web_search_param` (Any): Параметр для поиска в интернете.

**Возвращает**:

*   `Tuple[Messages, Optional[Sources]]`: Обновленный список сообщений и источники поиска.

**Как работает функция**:

1.  Создает копию списка сообщений `messages`.
2.  Если `web_search_param` не задан, возвращает исходный список сообщений и `None`.
3.  Если `web_search_param` является строкой и не равен `"true"`, использует его как поисковый запрос. В противном случае использует контент последнего сообщения как поисковый запрос.
4.  Вызывает асинхронную функцию `do_search` с контентом последнего сообщения и поисковым запросом.
5.  Обновляет контент последнего сообщения в списке `messages` результатом поиска.
6.  В случае ошибки логирует сообщение об ошибке.
7.  Возвращает обновленный список сообщений и источники поиска.

### `async_iter_run_tools`

```python
async def async_iter_run_tools(
    provider: ProviderType,
    model: str,
    messages: Messages,
    tool_calls: Optional[List[dict]] = None,
    **kwargs
) -> AsyncIterator:
    """Asynchronously run tools and yield results"""
    # Process web search
    sources = None
    web_search = kwargs.get('web_search')
    if web_search:
        messages, sources = await perform_web_search(messages, web_search)

    # Get API key if needed
    api_key = AuthManager.load_api_key(provider)
    if api_key and "api_key" not in kwargs:
        kwargs["api_key"] = api_key

    # Process tool calls
    if tool_calls:
        messages, sources, extra_kwargs = await ToolHandler.process_tools(messages, tool_calls, provider)
        kwargs.update(extra_kwargs)

    # Generate response
    create_function = provider.get_async_create_function()
    response = to_async_iterator(create_function(model=model, messages=messages, **kwargs))

    async for chunk in response:
        yield chunk

    # Yield sources if available
    if sources:
        yield sources
```

**Назначение**: Асинхронно запускает инструменты и выдает результаты.

**Параметры**:

*   `provider` (ProviderType): Провайдер, используемый для генерации.
*   `model` (str): Имя модели.
*   `messages` (Messages): Список сообщений.
*   `tool_calls` (Optional[List[dict]], optional): Список вызовов инструментов. По умолчанию `None`.
*   `**kwargs`: Дополнительные аргументы.

**Возвращает**:

*   `AsyncIterator`: Асинхронный итератор, выдающий результаты.

**Как работает функция**:

1.  Выполняет поиск в интернете, если задан параметр `web_search`.
2.  Загружает ключ API, если необходимо.
3.  Обрабатывает вызовы инструментов, если они заданы.
4.  Генерирует ответ с помощью асинхронной функции `create_function` провайдера.
5.  Выдает чанки ответа.
6.  Выдает источники, если они доступны.

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
    """Run tools synchronously and yield results"""
    # Process web search
    web_search = kwargs.get('web_search')
    sources = None

    if web_search:
        try:
            messages = messages.copy()
            search_query = web_search if isinstance(web_search, str) and web_search != "true" else None
            # Note: Using asyncio.run inside sync function is not ideal, but maintaining original pattern
            messages[-1]["content"], sources = asyncio.run(do_search(messages[-1]["content"], search_query))
        except Exception as ex:
            debug.error(f"Couldn\'t do web search: {ex.__class__.__name__}: {ex}")

    # Get API key if needed
    if provider is not None and getattr(provider, "needs_auth", False) and "api_key" not in kwargs:
        api_key = AuthManager.load_api_key(provider)
        if api_key:
            kwargs["api_key"] = api_key

    # Process tool calls
    if tool_calls:
        for tool in tool_calls:
            if tool.get("type") == "function":
                function_name = tool.get("function", {}).get("name")

                if function_name == TOOL_NAMES["SEARCH"]:
                    tool["function"]["arguments"] = ToolHandler.validate_arguments(tool["function"])
                    messages[-1]["content"] = get_search_message(
                        messages[-1]["content"],
                        raise_search_exceptions=True,
                        **tool["function"]["arguments"]
                    )
                elif function_name == TOOL_NAMES["CONTINUE"]:
                    if provider not in ("OpenaiAccount", "HuggingFace"):
                        last_line = messages[-1]["content"].strip().splitlines()[-1]
                        content = f"Carry on from this point:\\n{last_line}"
                        messages.append({"role": "user", "content": content})
                    else:
                        # Enable provider native continue
                        kwargs["action"] = "continue"
                elif function_name == TOOL_NAMES["BUCKET"]:
                    def on_bucket(match):
                        return "".join(read_bucket(get_bucket_dir(match.group(1))))
                    has_bucket = False
                    for message in messages:
                        if "content" in message and isinstance(message["content"], str):
                            new_message_content = re.sub(r'{"bucket_id":"([^"]*)"}', on_bucket, message["content"])
                            if new_message_content != message["content"]:
                                has_bucket = True
                                message["content"] = new_message_content
                    last_message = messages[-1]["content"]
                    if has_bucket and isinstance(last_message, str):
                        if "\\nSource: " in last_message:
                            messages[-1]["content"] = last_message + BUCKET_INSTRUCTIONS

    # Process response chunks
    thinking_start_time = 0
    processor = ThinkingProcessor()

    for chunk in iter_callback(model=model, messages=messages, provider=provider, **kwargs):
        if isinstance(chunk, FinishReason):
            if sources is not None:
                yield sources
                sources = None
            yield chunk
            continue
        elif isinstance(chunk, Sources):
            sources = None
        if not isinstance(chunk, str):
            yield chunk
            continue

        thinking_start_time, results = processor.process_thinking_chunk(chunk, thinking_start_time)

        for result in results:
            yield result

    if sources is not None:
        yield sources
```

**Назначение**: Синхронно запускает инструменты и выдает результаты.

**Параметры**:

*   `iter_callback` (Callable): Функция обратного вызова, которая генерирует чанки ответа.
*   `model` (str): Имя модели.
*   `messages` (Messages): Список сообщений.
*   `provider` (Optional[str], optional): Провайдер, используемый для генерации. По умолчанию `None`.
*   `tool_calls` (Optional[List[dict]], optional): Список вызовов инструментов. По умолчанию `None`.
*   `**kwargs`: Дополнительные аргументы.

**Возвращает**:

*   `Iterator`: Итератор, выдающий результаты.

**Как работает функция**:

1.  Выполняет поиск в интернете, если задан параметр `web_search`.
2.  Загружает ключ API, если необходимо.
3.  Обрабатывает вызовы инструментов, если они заданы.
4.  Обрабатывает чанки ответа с помощью `ThinkingProcessor`.
5.  Выдает результаты обработки.
6.  Выдает источники, если они доступны.

## Параметры

*   `BUCKET_INSTRUCTIONS` (str): Инструкции по добавлению источников для bucket.
*   `TOOL_NAMES` (dict): Словарь с именами инструментов.

## Примеры

Примеры использования этого модуля могут включать вызовы `async_iter_run_tools` и `iter_run_tools` с различными параметрами для выполнения различных инструментов, таких как поиск в интернете или продолжение генерации текста.