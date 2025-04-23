Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода реализует асинхронный генератор для работы с провайдерами, поддерживающими инструменты (tools), такие как функции. Он позволяет отправлять запросы к моделям с указанием инструментов и получать ответы в определенном формате, например, JSON. Код обрабатывает сообщения, определяет провайдера и модель, формирует запросы с учетом указанных инструментов и возвращает результаты, включая информацию об использовании токенов и вызовы инструментов.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**: Импортируются классы и типы данных, необходимые для работы асинхронного генератора и обработки ответов.
   ```python
   from __future__ import annotations

   import json

   from ..typing import AsyncResult, Messages, MediaListType
   from ..client.service import get_model_and_provider
   from ..client.helper import filter_json
   from .base_provider import AsyncGeneratorProvider
   from .response import ToolCalls, FinishReason, Usage
   ```
2. **Определение класса `ToolSupportProvider`**: Создается класс `ToolSupportProvider`, наследуемый от `AsyncGeneratorProvider`, который будет использоваться для работы с провайдерами, поддерживающими инструменты.
   ```python
   class ToolSupportProvider(AsyncGeneratorProvider):
       working = True
   ```
3. **Реализация метода `create_async_generator`**: Этот метод создает асинхронный генератор для отправки запросов к моделям с поддержкой инструментов.
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
   ```
4. **Определение провайдера и модели**: Если в имени модели указан провайдер через двоеточие, он извлекается. Затем вызывается функция `get_model_and_provider` для получения экземпляра модели и провайдера.
   ```python
   provider = None
   if ":" in model:
       provider, model = model.split(":", 1)
   model, provider = get_model_and_provider(
       model, provider,
       stream, logging=False,
       has_images=media is not None
   )
   ```
5. **Обработка инструментов (tools)**: Если указаны инструменты, проверяется, что их не больше одного. Формируется запрос с учетом указанного формата ответа (response_format) и описания инструментов.
   ```python
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
   ```
6. **Отправка запроса и получение результатов**: Вызывается асинхронная функция `provider.get_async_create_function()` для отправки запроса к модели. Результаты возвращаются в виде чанков (chunks).
   ```python
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
   ```
7. **Обработка информации об использовании токенов**: Если информация об использовании токенов не была получена, она вычисляется на основе длины полученных чанков.
   ```python
   if not has_usage:
       yield Usage(completion_tokens=len(chunks), total_tokens=len(chunks))
   ```
8. **Обработка вызовов инструментов**: Если указаны инструменты, извлекаются аргументы из полученных чанков и формируется объект `ToolCalls`.
   ```python
   chunks = "".join(chunks)
   if tools is not None:
       yield ToolCalls([{
           "id": "",
           "type": "function",
           "function": {
               "name": tools["function"]["name"],
               "arguments": filter_json(chunks)
           }
       }])
   yield chunks
   ```
9. **Завершение работы генератора**: Если получена причина завершения (finish), она возвращается.
   ```python
   if finish is not None:
       yield finish
   ```

Пример использования
-------------------------

```python
from src.endpoints.gpt4free.g4f.providers.tool_support import ToolSupportProvider
from src.endpoints.gpt4free.g4f.typing import Messages, MediaListType

async def main():
    model = "gpt-3.5-turbo"
    messages: Messages = [
        {"role": "user", "content": "Summarize the following text: Example text."},
    ]
    media: MediaListType = None
    tools = [{
        "type": "function",
        "function": {
            "name": "summarize",
            "description": "Summarizes the given text",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to summarize"
                    }
                },
                "required": ["text"]
            }
        }
    }]
    response_format = {"type": "json"}

    async for chunk in ToolSupportProvider.create_async_generator(
        model=model,
        messages=messages,
        stream=True,
        media=media,
        tools=tools,
        response_format=response_format
    ):
        print(chunk)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())