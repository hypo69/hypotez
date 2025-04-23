# Модуль `tool_support.py`

## Обзор

Модуль предназначен для поддержки инструментов в асинхронных запросах к различным провайдерам моделей. Он позволяет использовать инструменты (tools) при взаимодействии с моделями, такими как Google Gemini и OpenAI, и обрабатывает ответы в формате JSON.

## Более подробно

Модуль `tool_support.py` предоставляет класс `ToolSupportProvider`, который является асинхронным провайдером. Он позволяет создавать асинхронные генераторы для взаимодействия с различными моделями и провайдерами, поддерживающими инструменты. Модуль обрабатывает запросы с использованием инструментов, форматирует запросы и ответы в формате JSON и возвращает результаты в виде асинхронного генератора.

## Классы

### `ToolSupportProvider`

**Описание**:
Класс `ToolSupportProvider` является асинхронным провайдером для поддержки инструментов при взаимодействии с моделями.

**Наследует**:
- `AsyncGeneratorProvider`: Наследует функциональность асинхронного генератора от базового класса `AsyncGeneratorProvider`.

**Атрибуты**:
- `working` (bool): Указывает, работает ли провайдер. По умолчанию `True`.

**Методы**:
- `create_async_generator()`: Создает асинхронный генератор для выполнения запросов с использованием инструментов.

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
    """
    Создает асинхронный генератор для выполнения запросов к моделям с поддержкой инструментов.

    Args:
        cls (type): Ссылка на класс.
        model (str): Имя модели для использования. Может включать имя провайдера через `:`.
        messages (Messages): Список сообщений для отправки в модель.
        stream (bool, optional): Флаг потоковой передачи данных. По умолчанию `True`.
        media (MediaListType, optional): Список медиафайлов для отправки. По умолчанию `None`.
        tools (list[str], optional): Список инструментов для использования. Поддерживается только один инструмент. По умолчанию `None`.
        response_format (dict, optional): Формат ответа. По умолчанию `None`, но устанавливается в `{"type": "json"}`, если используются инструменты.
        **kwargs: Дополнительные аргументы для передачи в провайдер модели.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий чанки данных от провайдера модели.

    Raises:
        ValueError: Если передано более одного инструмента.
        Exception: Прочие исключения, возникающие в процессе выполнения запроса.

    Как работает функция:
    - Извлекает провайдера и имя модели из входного параметра `model`.
    - Если указаны инструменты (`tools`):
        - Проверяет, что указан только один инструмент. Если передано более одного инструмента, вызывает исключение `ValueError`.
        - Устанавливает формат ответа в `{"type": "json"}`, если он не был установлен ранее.
        - Формирует структуру запроса, добавляя описание формата ответа в виде JSON.
    - Вызывает асинхронный генератор провайдера модели для получения чанков данных.
    - Обрабатывает чанки данных:
        - Если чанк является строкой, добавляет его в список `chunks`.
        - Если чанк является объектом `Usage`, возвращает его и устанавливает флаг `has_usage`.
        - Если чанк является объектом `FinishReason`, завершает генерацию.
        - В противном случае возвращает чанк.
    - После завершения генерации:
        - Объединяет все строковые чанки в одну строку.
        - Если использовались инструменты, формирует объект `ToolCalls` с информацией об имени инструмента и аргументах в формате JSON.
        - Возвращает итоговую строку или объект `ToolCalls`.
        - Возвращает объект `FinishReason`, если он был получен.
    """
    ...
```

## Примеры вызова функции

```python
# Пример использования create_async_generator с указанием модели, сообщений и инструментов
model = "gemini:test"
messages = [{"role": "user", "content": "Напиши JSON с информацией о товаре."}]
tools = [{"function": {"name": "get_product", "parameters": {"properties": {"name": {"type": "string"}}}}}]

async def test():
    result = ToolSupportProvider.create_async_generator(model=model, messages=messages, tools=tools)
    async for item in result:
        print(item)
```
```python
# Пример использования create_async_generator с указанием модели, сообщений, инструментов и формата ответа
model = "openai:gpt-3.5-turbo-16k"
messages = [{"role": "user", "content": "Напиши JSON с информацией о погоде."}]
tools = [{"function": {"name": "get_weather", "parameters": {"properties": {"city": {"type": "string"}}}}}]
response_format = {"type": "json_object"}

async def test():
    result = ToolSupportProvider.create_async_generator(model=model, messages=messages, tools=tools, response_format=response_format)
    async for item in result:
        print(item)
```
```python
# Пример использования create_async_generator без указания инструментов
model = "openai:gpt-4"
messages = [{"role": "user", "content": "Привет!"}]

async def test():
    result = ToolSupportProvider.create_async_generator(model=model, messages=messages)
    async for item in result:
        print(item)