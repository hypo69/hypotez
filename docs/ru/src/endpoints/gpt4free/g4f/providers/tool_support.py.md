# Модуль поддержки инструментов (`tool_support.py`)

## Обзор

Модуль `tool_support.py` предоставляет класс `ToolSupportProvider`, который позволяет использовать инструменты (tools) с асинхронными генераторами в различных моделях, таких как GPT-4. Он поддерживает выполнение функций с заданными параметрами и форматирование ответов в формате JSON.

## Подробней

Этот модуль предназначен для интеграции с различными провайдерами и моделями, обеспечивая поддержку инструментов (tools) при генерации ответов. Он фильтрует JSON-ответы, обрабатывает использование токенов и возвращает результаты в нужном формате.

## Классы

### `ToolSupportProvider`

**Описание**: Класс `ToolSupportProvider` является асинхронным провайдером, который поддерживает использование инструментов (tools) в запросах к моделям.

**Наследует**:
- `AsyncGeneratorProvider`: Наследует функциональность асинхронного генератора от базового класса `AsyncGeneratorProvider`.

**Атрибуты**:
- `working` (bool): Указывает, работает ли провайдер. По умолчанию `True`.

**Методы**:
- `create_async_generator()`: Создает асинхронный генератор для выполнения запроса с использованием инструментов.

## Методы класса

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
        """Создает асинхронный генератор для выполнения запроса с использованием инструментов.

        Args:
            model (str): Имя модели для использования. Может включать имя провайдера через `:`.
            messages (Messages): Список сообщений для передачи в модель.
            stream (bool): Флаг, указывающий, использовать ли потоковую передачу данных. По умолчанию `True`.
            media (MediaListType): Список медиафайлов для передачи в модель. По умолчанию `None`.
            tools (list[str]): Список инструментов для использования. Поддерживается только один инструмент. По умолчанию `None`.
            response_format (dict): Формат ответа, например `{"type": "json"}`. По умолчанию `None`.
            **kwargs: Дополнительные аргументы для передачи в провайдер.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий чанки данных, `Usage` и `ToolCalls`.

        Raises:
            ValueError: Если указано больше одного инструмента.

        
            1. Разделяет `model` на `provider` и `model`, если в `model` есть `:`.
            2. Получает модель и провайдер с помощью `get_model_and_provider`.
            3. Проверяет, что указан только один инструмент.
            4. Если инструменты указаны, устанавливает формат ответа в JSON и добавляет инструкции в сообщения.
            5. Создает асинхронный генератор, который итерируется по чанкам данных от провайдера.
            6. Обрабатывает чанки данных, возвращая объекты `Usage`, `FinishReason` и `ToolCalls`.
            7. Фильтрует JSON-ответ с помощью `filter_json`.
            8. Возвращает результаты в виде `ToolCalls` и финального ответа.

        Примеры:
            Пример использования с одним инструментом:
            ```python
            async for chunk in ToolSupportProvider.create_async_generator(
                model="gemini",
                messages=[{"role": "user", "content": "Do something with tools"}],
                tools=[{"function": {"name": "tool_name", "parameters": {"properties": {}}}}],
                response_format={"type": "json"}
            ):
                print(chunk)
            ```

            Пример использования без инструментов:
            ```python
            async for chunk in ToolSupportProvider.create_async_generator(
                model="openai",
                messages=[{"role": "user", "content": "Hello"}],
            ):
                print(chunk)
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
```

## Параметры класса

- `model` (str): Имя модели для использования. Может включать имя провайдера через `:`.
- `messages` (Messages): Список сообщений для передачи в модель.
- `stream` (bool): Флаг, указывающий, использовать ли потоковую передачу данных. По умолчанию `True`.
- `media` (MediaListType): Список медиафайлов для передачи в модель. По умолчанию `None`.
- `tools` (list[str]): Список инструментов для использования. Поддерживается только один инструмент. По умолчанию `None`.
- `response_format` (dict): Формат ответа, например `{"type": "json"}`. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы для передачи в провайдер.

## Примеры

Пример использования с одним инструментом:

```python
async for chunk in ToolSupportProvider.create_async_generator(
    model="gemini",
    messages=[{"role": "user", "content": "Do something with tools"}],
    tools=[{"function": {"name": "tool_name", "parameters": {"properties": {}}}}],
    response_format={"type": "json"}
):
    print(chunk)
```

Пример использования без инструментов:

```python
async for chunk in ToolSupportProvider.create_async_generator(
    model="openai",
    messages=[{"role": "user", "content": "Hello"}],
):
    print(chunk)
```