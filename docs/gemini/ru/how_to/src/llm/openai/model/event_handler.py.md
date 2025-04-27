## Как использовать блок кода  `EventHandler`

=========================================================================================

Описание
-------------------------
Блок кода `EventHandler`  определяет обработчик событий для  Assistant API,  который обрабатывает  ответы от  Assistant  в реальном времени.  
 
Шаги выполнения
-------------------------
1. **Инициализация:**  Создается  экземпляр  класса  `EventHandler`,  который наследуется от `AssistantEventHandler`  из  библиотеки  `openai`. 
2. **Обработка событий:**   Определяются  методы  для  обработки  событий,  связанных с  Assistant  API:
   - `on_text_created`:  Вызывается при создании  нового  текстового  сообщения  от  Assistant.
   - `on_text_delta`:  Вызывается при обновлении  текстового  сообщения  от  Assistant.
   - `on_tool_call_created`:  Вызывается при  создании  вызова  инструмента  от  Assistant.
   - `on_tool_call_delta`:  Вызывается при  обновлении  вызова  инструмента  от  Assistant.
3. **Обработка данных:**   В  методах  обработки  событий  происходит  вывод  соответствующих  данных  на  консоль  в  формате  потока  данных  в  реальном  времени.

Пример использования
-------------------------

```python
from typing_extensions import override
from openai import AssistantEventHandler, OpenAI
from openai.types.beta.threads import Text, TextDelta
from openai.types.beta.threads.runs import ToolCall, ToolCallDelta

# ... (другой код)

# First, we create a EventHandler class to define
# how we want to handle the events in the response stream.

class EventHandler(AssistantEventHandler):
  """ """

  @override
  def on_text_created(self, text: Text) -> None:
    print(f"\nassistant > ", end="", flush=True)

  @override
  def on_text_delta(self, delta: TextDelta, snapshot: Text):
    print(delta.value, end="", flush=True)

  @override
  def on_tool_call_created(self, tool_call: ToolCall):
    print(f"\nassistant > {tool_call.type}\n", flush=True)

  @override
  def on_tool_call_delta(self, delta: ToolCallDelta, snapshot: ToolCall):
    if delta.type == "code_interpreter" and delta.code_interpreter:
      if delta.code_interpreter.input:
        print(delta.code_interpreter.input, end="", flush=True)
      if delta.code_interpreter.outputs:
        print(f"\n\noutput >", flush=True)
        for output in delta.code_interpreter.outputs:
          if output.type == "logs":
            print(f"\n{output.logs}", flush=True)

# Then, we use the `stream` SDK helper
# with the `EventHandler` class to create the Run
# and stream the response.

# ... (другой код)

```

**Дополнительная информация:**

-  `flush=True`  в  методах  `print`  обеспечивает  немедленный  вывод  данных  на  консоль. 
-   `EventHandler`  может  быть  использован  для  отладки  Assistant  API,  поскольку  он  позволяет  просматривать  данные  ответа  в  реальном  времени. 
-  Этот  класс  можно  настроить  для  обработки  других  событий  Assistant  API  и  выполнения  других  действий,  таких  как  запись  данных  в  файл  или  отправка  данных  на  сервер.