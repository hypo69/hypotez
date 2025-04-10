# Модуль поддержки инструментов `tool_support.py`

## Обзор

Модуль `tool_support.py` предоставляет класс `ToolSupportProvider`, который используется для поддержки инструментов (tools) в асинхронных генераторах. Он позволяет взаимодействовать с различными провайдерами и моделями, а также форматировать ответы в формате JSON. Модуль предназначен для работы с AI-моделями, поддерживающими использование инструментов для выполнения задач.

## Подробней

Модуль предназначен для расширения функциональности асинхронных генераторов путем добавления поддержки инструментов. Он позволяет указать модель, сообщения, медиа-данные и инструменты, используемые для генерации ответов. В частности, он обрабатывает ответы в формате JSON, если используются инструменты.

## Классы

### `ToolSupportProvider`

**Описание**: Класс `ToolSupportProvider` предоставляет поддержку инструментов для асинхронных генераторов.

**Наследует**:
- `AsyncGeneratorProvider`: Наследует функциональность асинхронного генератора от базового класса `AsyncGeneratorProvider`.

**Атрибуты**:
- `working` (bool): Указывает, работает ли провайдер. По умолчанию `True`.

**Методы**:
- `create_async_generator()`: Создает асинхронный генератор для работы с указанной моделью и инструментами.

## Функции

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        stream: bool = True,
        media: MediaListType = None,
        tools: list[str] = None,
        response_format: dict = None,
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для взаимодействия с указанной моделью и инструментами.

        Args:
            model (str): Имя модели для использования. Может включать имя провайдера, разделенное двоеточием (например, "provider:model").
            messages (Messages): Список сообщений для передачи модели.
            stream (bool, optional): Флаг, указывающий, следует ли использовать потоковый режим. По умолчанию `True`.
            media (MediaListType, optional): Список медиа-данных для передачи модели. По умолчанию `None`.
            tools (list[str], optional): Список инструментов для использования. Поддерживается только один инструмент. По умолчанию `None`.
            response_format (dict, optional): Формат ответа. Если используются инструменты, должен быть указан как `{"type": "json"}`. По умолчанию `None`.
            **kwargs: Дополнительные аргументы для передачи провайдеру.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий чанки данных.

        Raises:
            ValueError: Если указано более одного инструмента.

        Как работает функция:
        1. **Разделение модели и провайдера**: Если в имени модели есть двоеточие, функция разделяет имя модели и провайдера.
        2. **Получение модели и провайдера**: Использует функцию `get_model_and_provider` для получения экземпляра модели и провайдера на основе предоставленных данных.
        3. **Обработка инструментов**:
           - Проверяет, что указан только один инструмент. Если инструментов больше одного, выбрасывает исключение `ValueError`.
           - Устанавливает формат ответа как JSON, если используются инструменты.
           - Преобразует структуру инструментов для соответствия требованиям модели.
        4. **Создание асинхронного генератора**: Вызывает метод `get_async_create_function` провайдера для создания асинхронного генератора.
        5. **Итерирование по чанкам данных**:
           - Получает чанки данных из генератора, предоставляемого провайдером.
           - Обрабатывает различные типы чанков: строки, `Usage`, `FinishReason` и другие.
           - Выдает чанки данных.
        6. **Обработка завершения**:
           - Если генератор завершается с причиной `FinishReason`, сохраняет эту причину.
        7. **Обработка токенов**:
           - Если в процессе генерации не было информации об использовании токенов, вычисляет приблизительное количество токенов на основе длины чанков.
        8. **Обработка инструментов после завершения**:
           - Если используются инструменты, извлекает имя функции и аргументы из сгенерированных чанков.
           - Формирует структуру `ToolCalls` с информацией о вызове инструмента.
        9. **Выдача результатов**:
           - Выдает структуру `ToolCalls`, содержащую информацию о вызове инструмента.
           - Выдает оставшиеся чанки данных.
           - Выдает причину завершения, если она была получена.

        ASCII flowchart:

        A [Разделение модели и провайдера]
        ↓
        B [Получение модели и провайдера]
        ↓
        C [Обработка инструментов]
        ↓
        D [Создание асинхронного генератора]
        ↓
        E [Итерирование по чанкам данных]
        ↓
        F [Обработка завершения]
        ↓
        G [Обработка токенов]
        ↓
        H [Обработка инструментов после завершения]
        ↓
        I [Выдача результатов]

        Примеры:
        1. Использование с указанием модели и сообщения:
           ```python
           model = "gpt-3.5-turbo"
           messages = [{"role": "user", "content": "Hello, world!"}]
           async_generator = await ToolSupportProvider.create_async_generator(model=model, messages=messages)
           ```

        2. Использование с указанием модели, сообщения и инструмента:
           ```python
           model = "gpt-3.5-turbo"
           messages = [{"role": "user", "content": "Hello, world!"}]
           tools = [{"function": {"name": "my_function", "parameters": {"properties": {"param1": {"type": "string"}}}}}]
           async_generator = await ToolSupportProvider.create_async_generator(model=model, messages=messages, tools=tools)
           ```

        3. Использование с указанием модели, сообщения, инструмента и формата ответа:
           ```python
           model = "gpt-3.5-turbo"
           messages = [{"role": "user", "content": "Hello, world!"}]
           tools = [{"function": {"name": "my_function", "parameters": {"properties": {"param1": {"type": "string"}}}}}]
           response_format = {"type": "json"}
           async_generator = await ToolSupportProvider.create_async_generator(model=model, messages=messages, tools=tools, response_format=response_format)
           ```
        """
        provider = None
        if ":" in model:
            provider, model = model.split(":", 1)
        model, provider = get_model_and_provider(
            model, provider,
            stream, logging=False,
            has_images=media is not None
        )
        if tools is not None:
            if len(tools) > 1:
                raise ValueError("Only one tool is supported.")
            if response_format is None:
                response_format = {"type": "json"}
            tools = tools.pop()
            lines = ["Respone in JSON format."]
            properties = tools["function"]["parameters"]["properties"]
            properties = {key: value["type"] for key, value in properties.items()}
            lines.append(f"Response format: {json.dumps(properties, indent=2)}")
            messages = [{"role": "user", "content": "\\n".join(lines)}] + messages

        finish = None
        chunks = []
        has_usage = False
        async for chunk in provider.get_async_create_function()(
            model,
            messages,
            stream=stream,
            media=media,
            response_format=response_format,
            **kwargs
        ):
            if isinstance(chunk, str):
                chunks.append(chunk)
            elif isinstance(chunk, Usage):
                yield chunk
                has_usage = True
            elif isinstance(chunk, FinishReason):
                finish = chunk
                break
            else:
                yield chunk

        if not has_usage:
            yield Usage(completion_tokens=len(chunks), total_tokens=len(chunks))

        chunks = "".join(chunks)
        if tools is not None:
            yield ToolCalls([{\
                "id": "",\
                "type": "function",\
                "function": {\
                    "name": tools["function"]["name"],\
                    "arguments": filter_json(chunks)\
                }\
            }])
        yield chunks

        if finish is not None:
            yield finish