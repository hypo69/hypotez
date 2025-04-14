# Модуль для запуска инструментов

## Обзор

Этот модуль предоставляет функциональность для выполнения различных инструментов, таких как поиск в интернете, продолжение разговора и работа с хранилищем (bucket). Он включает классы для обработки инструментов, управления ключами API и обработки промежуточных результатов (thinking chunks). Модуль поддерживает как асинхронный, так и синхронный режимы работы.

## Подробней

Этот модуль является ключевым компонентом системы, отвечающим за интеграцию различных инструментов (tools) в процесс генерации ответов. Он обеспечивает возможность использования этих инструментов для расширения функциональности и улучшения качества генерируемых ответов.

## Классы

### `ToolHandler`

**Описание**: Класс предназначен для обработки различных типов инструментов.

**Методы**:

- `validate_arguments(data: dict) -> dict`:
    ```python
    @staticmethod
    def validate_arguments(data: dict) -> dict:
        """Проверяет и разбирает аргументы инструмента.

        Args:
            data (dict): Словарь, содержащий данные для проверки и разбора.

        Returns:
            dict: Словарь с проверенными и отфильтрованными аргументами.

        Raises:
            ValueError: Если аргументы функции инструмента не являются словарем или JSON-строкой.

        Как работает функция:
        - Если в `data` есть ключ "arguments", код проверяет, является ли значение по этому ключу строкой.
        - Если да, то пытается распарсить эту строку как JSON.
        - Если значение не является словарем после этого, вызывается исключение `ValueError`.
        - В противном случае, функция вызывает `filter_none` для удаления всех элементов со значением `None` из словаря аргументов и возвращает результат.
        - Если ключа "arguments" нет в `data`, возвращается пустой словарь.
        """
    ```

- `process_search_tool(messages: Messages, tool: dict) -> Messages`:
    ```python
    @staticmethod
    async def process_search_tool(messages: Messages, tool: dict) -> Messages:
        """Обрабатывает запросы инструмента поиска.

        Args:
            messages (Messages): Список сообщений.
            tool (dict): Словарь, содержащий информацию об инструменте.

        Returns:
            Messages: Обновленный список сообщений и источники.

        Как работает функция:
        - Создает копию списка сообщений.
        - Вызывает `ToolHandler.validate_arguments` для проверки и извлечения аргументов инструмента из `tool["function"]`.
        - Вызывает асинхронную функцию `do_search` для выполнения поиска.
        - Обновляет содержимое последнего сообщения в списке сообщений результатом поиска и источниками.
        - Возвращает обновленный список сообщений и источники.
        """
    ```

- `process_continue_tool(messages: Messages, tool: dict, provider: Any) -> Tuple[Messages, Dict[str, Any]]`:
    ```python
    @staticmethod
    def process_continue_tool(messages: Messages, tool: dict, provider: Any) -> Tuple[Messages, Dict[str, Any]]:
        """Обрабатывает запросы инструмента продолжения.

        Args:
            messages (Messages): Список сообщений.
            tool (dict): Словарь, содержащий информацию об инструменте.
            provider (Any): Провайдер.

        Returns:
            Tuple[Messages, Dict[str, Any]]: Обновленный список сообщений и дополнительные аргументы.

        Как работает функция:
        - Инициализирует словарь `kwargs` для дополнительных аргументов.
        - Если провайдер не "OpenaiAccount" и не "HuggingFaceAPI", создается копия списка сообщений.
        - Извлекается последняя строка последнего сообщения, добавляется префикс "Carry on from this point:\\n" и добавляется новое сообщение с ролью "user" и сгенерированным содержимым.
        - Если провайдер "OpenaiAccount" или "HuggingFaceAPI", в `kwargs` добавляется ключ "action" со значением "continue".
        - Возвращает обновленный список сообщений и `kwargs`.
        """
    ```

- `process_bucket_tool(messages: Messages, tool: dict) -> Messages`:
    ```python
    @staticmethod
    def process_bucket_tool(messages: Messages, tool: dict) -> Messages:
        """Обрабатывает запросы инструмента bucket.

        Args:
            messages (Messages): Список сообщений.
            tool (dict): Словарь, содержащий информацию об инструменте.

        Returns:
            Messages: Обновленный список сообщений.

        Как работает функция:
        - Создает копию списка сообщений.
        - Определяет внутреннюю функцию `on_bucket`, которая читает содержимое bucket с заданным ID.
        - Проходит по всем сообщениям и заменяет все вхождения шаблона `{"bucket_id":"[bucket_id]"}` на содержимое соответствующего bucket, используя `re.sub` и `on_bucket`.
        - Если были найдены и заменены bucket ID, добавляет инструкцию по добавлению источников цитат (`BUCKET_INSTRUCTIONS`) к последнему сообщению, если оно содержит "\\nSource: ".
        - Возвращает обновленный список сообщений.
        """
    ```

- `process_tools(messages: Messages, tool_calls: List[dict], provider: Any) -> Tuple[Messages, Dict[str, Any]]`:
    ```python
    @staticmethod
    async def process_tools(messages: Messages, tool_calls: List[dict], provider: Any) -> Tuple[Messages, Dict[str, Any]]:
        """Обрабатывает все вызовы инструментов и возвращает обновленные сообщения и kwargs.

        Args:
            messages (Messages): Список сообщений.
            tool_calls (List[dict]): Список вызовов инструментов.
            provider (Any): Провайдер.

        Returns:
            Tuple[Messages, Dict[str, Any]]: Обновленный список сообщений, источники и дополнительные аргументы.

        Как работает функция:
        - Если `tool_calls` пуст, возвращает исходный список сообщений и пустой словарь.
        - Инициализирует словарь `extra_kwargs` для хранения дополнительных аргументов, копирует список сообщений и устанавливает `sources` в `None`.
        - Проходит по всем вызовам инструментов (`tool_calls`).
        - Если тип инструмента не "function", пропускает его.
        - Определяет имя функции из `tool["function"]["name"]`.
        - В зависимости от имени функции вызывает соответствующий обработчик:
            - Если имя `TOOL_NAMES["SEARCH"]`, вызывает `ToolHandler.process_search_tool`.
            - Если имя `TOOL_NAMES["CONTINUE"]`, вызывает `ToolHandler.process_continue_tool` и обновляет `extra_kwargs`.
            - Если имя `TOOL_NAMES["BUCKET"]`, вызывает `ToolHandler.process_bucket_tool`.
        - Возвращает обновленный список сообщений, источники и `extra_kwargs`.
        """
    ```

### `AuthManager`

**Описание**: Класс для управления ключами API.

**Методы**:

- `get_api_key_file(cls) -> Path`:
    ```python
    @staticmethod
    def get_api_key_file(cls) -> Path:
        """Получает путь к файлу ключа API для провайдера.

        Args:
            cls: Класс провайдера.

        Returns:
            Path: Путь к файлу ключа API.

        Как работает функция:
        - Возвращает путь к файлу, в котором хранится ключ API для данного провайдера.
        - Имя файла формируется как `api_key_[provider_name].json` в директории cookies.
        """
    ```

- `load_api_key(provider: Any) -> Optional[str]`:
    ```python
    @staticmethod
    def load_api_key(provider: Any) -> Optional[str]:
        """Загружает ключ API из файла конфигурации, если это необходимо.

        Args:
            provider (Any): Провайдер.

        Returns:
            Optional[str]: Ключ API или None, если он не нужен или не найден.

        Как работает функция:
        - Сначала проверяет, требуется ли провайдеру аутентификация, используя `getattr(provider, "needs_auth", False)`.
        - Если аутентификация не требуется, возвращает `None`.
        - Если требуется, формирует путь к файлу с ключом API, используя `AuthManager.get_api_key_file(provider)`.
        - Пытается открыть файл и загрузить ключ API из JSON.
        - В случае успеха возвращает ключ API, в случае неудачи логирует ошибку и возвращает `None`.
        """
    ```

### `ThinkingProcessor`

**Описание**: Класс для обработки промежуточных результатов (thinking chunks).

**Методы**:

- `process_thinking_chunk(chunk: str, start_time: float = 0) -> Tuple[float, List[Union[str, Reasoning]]]`:
    ```python
    @staticmethod
    def process_thinking_chunk(chunk: str, start_time: float = 0) -> Tuple[float, List[Union[str, Reasoning]]]:
        """Обрабатывает чанк и возвращает время и результаты.

        Args:
            chunk (str): Чанк текста.
            start_time (float, optional): Время начала обработки. По умолчанию 0.

        Returns:
            Tuple[float, List[Union[str, Reasoning]]]: Кортеж, содержащий время и список результатов.

        Как работает функция:
        - Обрабатывает различные сценарии, связанные с тегами `<think>` и `</think>`, чтобы определить, находится ли модель в процессе размышления.
        - Если тег `<think>` найден, добавляет `Reasoning` объект в результаты, указывая, что модель начала думать.
        - Если тег `</think>` найден, добавляет `Reasoning` объект в результаты, указывая, что модель закончила думать, а также вычисляет продолжительность размышления.
        - Возвращает обновленное время начала и список результатов.
        """
    ```

## Функции

### `perform_web_search(messages: Messages, web_search_param: Any) -> Tuple[Messages, Optional[Sources]]`

```python
async def perform_web_search(messages: Messages, web_search_param: Any) -> Tuple[Messages, Optional[Sources]]:
    """Выполняет поиск в интернете и возвращает обновленные сообщения и источники.

    Args:
        messages (Messages): Список сообщений.
        web_search_param (Any): Параметр для поиска в интернете.

    Returns:
        Tuple[Messages, Optional[Sources]]: Обновленный список сообщений и источники.

    Как работает функция:
    - Если `web_search_param` не задан, возвращает исходный список сообщений и `None` для источников.
    - Пытается выполнить поиск, используя `do_search`. Если `web_search_param` является строкой и не равен "true", использует его как поисковый запрос. В противном случае использует содержимое последнего сообщения в списке сообщений как поисковый запрос.
    - В случае успеха обновляет содержимое последнего сообщения результатом поиска и возвращает источники.
    - В случае ошибки логирует ошибку и возвращает исходный список сообщений и `None` для источников.
    """
```

### `async_iter_run_tools(provider: ProviderType, model: str, messages: Messages, tool_calls: Optional[List[dict]] = None, **kwargs) -> AsyncIterator`

```python
async def async_iter_run_tools(
    provider: ProviderType, 
    model: str, 
    messages: Messages, 
    tool_calls: Optional[List[dict]] = None, 
    **kwargs
) -> AsyncIterator:
    """Асинхронно запускает инструменты и возвращает результаты.

    Args:
        provider (ProviderType): Провайдер.
        model (str): Модель.
        messages (Messages): Список сообщений.
        tool_calls (Optional[List[dict]], optional): Список вызовов инструментов. По умолчанию None.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncIterator: Асинхронный итератор.

    Как работает функция:
    - Обрабатывает поиск в интернете, используя `perform_web_search`.
    - Загружает ключ API, используя `AuthManager.load_api_key`.
    - Обрабатывает вызовы инструментов, используя `ToolHandler.process_tools`.
    - Генерирует ответ, используя асинхронную функцию создания ответа провайдера.
    - Возвращает результаты в виде асинхронного итератора.
    """
```

### `iter_run_tools(iter_callback: Callable, model: str, messages: Messages, provider: Optional[str] = None, tool_calls: Optional[List[dict]] = None, **kwargs) -> Iterator`

```python
def iter_run_tools(
    iter_callback: Callable,
    model: str,
    messages: Messages,
    provider: Optional[str] = None,
    tool_calls: Optional[List[dict]] = None,
    **kwargs
) -> Iterator:
    """Запускает инструменты синхронно и возвращает результаты.

    Args:
        iter_callback (Callable): Функция обратного вызова для итерации.
        model (str): Модель.
        messages (Messages): Список сообщений.
        provider (Optional[str], optional): Провайдер. По умолчанию None.
        tool_calls (Optional[List[dict]], optional): Список вызовов инструментов. По умолчанию None.
        **kwargs: Дополнительные аргументы.

    Returns:
        Iterator: Итератор.

    Как работает функция:
    - Обрабатывает поиск в интернете, используя `do_search` внутри `asyncio.run`.
    - Загружает ключ API, используя `AuthManager.load_api_key`.
    - Обрабатывает вызовы инструментов, подготавливая аргументы и изменяя сообщения.
    - Обрабатывает чанки ответов, используя `ThinkingProcessor` для извлечения промежуточных результатов.
    - Возвращает результаты в виде итератора.
    """