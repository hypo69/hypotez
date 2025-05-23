## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Блок кода представляет собой класс `ToolSupportProvider`, который предоставляет функциональность для работы с инструментами (tools) в модели GPT-4. Он наследуется от класса `AsyncGeneratorProvider`, который обеспечивает асинхронную генерацию ответов от модели. 

Шаги выполнения
-------------------------
1. **Инициализация:** Класс `ToolSupportProvider` инициализируется с помощью метода `create_async_generator`. 
2. **Проверка инструмента:** Метод `create_async_generator` проверяет, был ли передан инструмент. Если инструмент передан, он должен быть один, и формат ответа должен быть в формате JSON.
3. **Формирование подсказки:** Если инструмент передан, формируется подсказка с описанием формата ответа и параметров инструмента.
4. **Вызов генератора:** Метод `create_async_generator` вызывает асинхронный генератор `provider.get_async_create_function()`, который генерирует ответ модели.
5. **Обработка ответов:** Генератор обрабатывает ответы, выделяя информацию о токенах, завершении и вызовах инструментов.
6. **Генерация ответов:**  Генератор возвращает ответы, которые могут содержать информацию об использовании токенов, вызовах инструментов и окончательном результате.

Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.providers.tool_support import ToolSupportProvider
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Определение инструмента
tool = {
    "function": {
        "name": "my_tool",
        "parameters": {
            "type": "object",
            "properties": {
                "input": {
                    "type": "string",
                    "description": "Входные данные для инструмента."
                }
            },
            "required": ["input"]
        }
    }
}

# Создание сообщения
messages: Messages = [
    {"role": "user", "content": "Привет! Используй инструмент 'my_tool' с входными данными 'Hello world'."}
]

# Вызов метода create_async_generator для получения ответа
async for chunk in ToolSupportProvider.create_async_generator(
    model="gpt-4",
    messages=messages,
    tools=[tool]
):
    # Обработка ответа
    print(chunk)
```