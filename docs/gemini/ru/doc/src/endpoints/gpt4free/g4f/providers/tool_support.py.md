# Модуль `tool_support.py`

## Обзор

Этот модуль предоставляет класс `ToolSupportProvider`, который позволяет использовать инструменты (например, функции) в запросах к модели GPT-4Free. Класс расширяет базовый класс `AsyncGeneratorProvider`, обеспечивая возможность обработки вызовов инструментов. 

## Классы

### `class ToolSupportProvider`

**Описание**: Класс, реализующий поддержку использования инструментов в запросах к GPT-4Free.

**Наследует**: 
    - `AsyncGeneratorProvider`

**Атрибуты**:
    - `working` (bool): Флаг, указывающий, что класс доступен для работы.

**Методы**:
    - `create_async_generator()`: Асинхронный генератор, который обрабатывает запросы к модели GPT-4Free с использованием инструментов.

### Метод `create_async_generator()`

**Назначение**: 
    - Асинхронно генерирует ответы от модели GPT-4Free с использованием инструментов.
    - Проверяет корректность параметров инструментов и формата ответа.
    - Вызывает асинхронный генератор базового класса `AsyncGeneratorProvider` для обработки запроса.
    - Обрабатывает и возвращает результаты вызовов инструментов в JSON формате.

**Параметры**:
    - `model` (str): Имя модели GPT-4Free.
    - `messages` (Messages): Список сообщений для модели.
    - `stream` (bool): Флаг, указывающий на потоковый режим обработки. По умолчанию `True`.
    - `media` (MediaListType): Список медиафайлов для обработки. По умолчанию `None`.
    - `tools` (list[str]): Список инструментов для использования. По умолчанию `None`.
    - `response_format` (dict): Формат ответа. По умолчанию `None`.

**Возвращает**:
    - `AsyncResult`: Асинхронный результат обработки.

**Вызывает исключения**:
    - `ValueError`: Если указано более одного инструмента.

**Пример**:

```python
from hypotez.src.endpoints.gpt4free.g4f.providers.tool_support import ToolSupportProvider
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Инициализируем список сообщений для модели
messages: Messages = [{"role": "user", "content": "Какие инструменты вы можете использовать?"}]

# Создаем объект класса ToolSupportProvider
provider = ToolSupportProvider()

# Вызываем метод create_async_generator() для обработки запроса с использованием инструмента
async_result = await provider.create_async_generator(
    model="gpt-3.5-turbo",
    messages=messages,
    tools=["my_tool"]
)

# Обрабатываем результаты
async for chunk in async_result:
    print(chunk)