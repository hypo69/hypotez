# Модуль поддержки инструментов

## Обзор

Модуль `tool_support.py` предоставляет класс `ToolSupportProvider`, который предназначен для работы с инструментами, требующими поддержки в процессе взаимодействия с языковой моделью. Он позволяет интегрировать инструменты, такие как функции, в запросы к модели и обрабатывать ответы в формате JSON. Модуль поддерживает асинхронное взаимодействие с провайдерами моделей, такими как GPT-4.

## Подробней

Этот модуль является частью системы `gpt4free` и предназначен для расширения возможностей языковых моделей за счет использования внешних инструментов. Он обеспечивает стандартизированный способ интеграции и вызова инструментов, позволяя моделям выполнять более сложные задачи. Модуль использует асинхронные генераторы для обработки потоковых ответов от моделей и поддерживает передачу медиа-данных.

## Классы

### `ToolSupportProvider`

**Описание**:
Класс `ToolSupportProvider` является асинхронным провайдером, который поддерживает использование инструментов в запросах к языковой модели.

**Наследует**:
- `AsyncGeneratorProvider`: Наследует функциональность асинхронного генератора провайдера.

**Атрибуты**:
- `working` (bool): Указывает, работает ли провайдер. По умолчанию `True`.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для взаимодействия с моделью с поддержкой инструментов.

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
    Создает асинхронный генератор для взаимодействия с моделью с поддержкой инструментов.

    Args:
        model (str): Имя модели для использования. Может включать имя провайдера через `:`.
        messages (Messages): Список сообщений для отправки в модель.
        stream (bool, optional): Флаг, указывающий, следует ли использовать потоковый режим. По умолчанию `True`.
        media (MediaListType, optional): Список медиа-файлов для отправки в модель. По умолчанию `None`.
        tools (list[str], optional): Список инструментов для использования. Поддерживается только один инструмент. По умолчанию `None`.
        response_format (dict, optional): Формат ответа. По умолчанию `None`.
        **kwargs: Дополнительные аргументы для передачи в провайдер модели.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий чанки данных от модели.

    Raises:
        ValueError: Если передано больше одного инструмента.
        Exception: Если возникает ошибка в процессе взаимодействия с моделью.
    """
```

**Назначение**:
Метод `create_async_generator` создает асинхронный генератор, который обеспечивает взаимодействие с языковой моделью с поддержкой инструментов. Он обрабатывает параметры, подготавливает сообщения, вызывает соответствующий провайдер и возвращает асинхронный генератор, который выдает чанки данных от модели.

**Как работает функция**:
1. **Разбор параметров**:
   - Извлекает имя провайдера и модели из параметра `model`, если они указаны через `:`.
   - Получает экземпляр провайдера и имя модели с помощью функции `get_model_and_provider`.
2. **Обработка инструментов**:
   - Проверяет, передан ли список инструментов `tools`. Если да, то:
     - Убеждается, что передан только один инструмент. Если инструментов больше одного, вызывает исключение `ValueError`.
     - Если `response_format` не указан, устанавливает его в `{"type": "json"}`.
     - Извлекает параметры инструмента и формирует строку с описанием формата ответа в формате JSON.
     - Добавляет сообщение с инструкцией о формате ответа в начало списка сообщений `messages`.
3. **Взаимодействие с провайдером**:
   - Получает асинхронный генератор от провайдера с помощью метода `get_async_create_function`.
   - Итерируется по чанкам, возвращаемым генератором:
     - Если чанк является строкой, добавляет его в список `chunks`.
     - Если чанк является экземпляром `Usage`, выдает его и устанавливает флаг `has_usage`.
     - Если чанк является экземпляром `FinishReason`, сохраняет его и завершает цикл.
     - В противном случае выдает чанк.
4. **Обработка результатов**:
   - Если не было информации об использовании (`has_usage` is `False`), создает и выдает объект `Usage` на основе длины собранных чанков.
   - Объединяет все чанки в одну строку `chunks`.
   - Если использовались инструменты, формирует объект `ToolCalls` с информацией о вызванной функции и ее аргументах, полученных из `chunks`, и выдает его.
   - Выдает объединенную строку `chunks`.
   - Если был получен `finish`, выдает его.

**Внутренние функции**:
- В данном методе нет внутренних функций.

**Примеры**:

1. **Использование с указанием модели и сообщения**:

```python
model = "gpt-4"
messages = [{"role": "user", "content": "Напиши JSON с данными о погоде в Москве."}]
async for chunk in ToolSupportProvider.create_async_generator(model=model, messages=messages):
    print(chunk)
```

2. **Использование с указанием инструмента**:

```python
model = "gpt-4"
messages = [{"role": "user", "content": "Сгенерируй JSON с данными о погоде в Москве."}]
tools = [{
    "function": {
        "name": "get_weather",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string"},
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
            },
            "required": ["location"]
        }
    }
}]
async for chunk in ToolSupportProvider.create_async_generator(model=model, messages=messages, tools=tools):
    print(chunk)
```