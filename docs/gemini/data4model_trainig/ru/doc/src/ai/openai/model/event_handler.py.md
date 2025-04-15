# Модуль для обработки событий Assistant API от OpenAI

## Обзор

Модуль `event_handler.py` предназначен для обработки событий, генерируемых Assistant API от OpenAI. Он содержит класс `EventHandler`, который определяет, как обрабатывать различные события в потоке ответов от ассистента. Этот модуль позволяет реагировать на создание текста, изменение текста, создание вызовов инструментов и другие события в реальном времени.

## Подробней

Этот модуль предоставляет механизм для обработки событий, связанных с взаимодействием с ассистентом OpenAI. Он использует класс `AssistantEventHandler` из библиотеки `openai` для определения обработчиков событий. Модуль особенно полезен для приложений, которым требуется реагировать на события ассистента в реальном времени, такие как отображение текста по мере его генерации или обработка вызовов инструментов.

## Классы

### `EventHandler`

**Описание**: Класс `EventHandler` наследуется от `AssistantEventHandler` и предоставляет переопределенные методы для обработки различных событий, генерируемых Assistant API от OpenAI.

**Наследует**:
- `AssistantEventHandler` из библиотеки `openai`.

**Методы**:

- `on_text_created(self, text: Text) -> None`: Обработчик события создания текста.
- `on_text_delta(self, delta: TextDelta, snapshot: Text) -> None`: Обработчик события изменения текста.
- `on_tool_call_created(self, tool_call: ToolCall) -> None`: Обработчик события создания вызова инструмента.
- `on_tool_call_delta(self, delta: ToolCallDelta, snapshot: ToolCall) -> None`: Обработчик события изменения вызова инструмента.

**Принцип работы**:

Класс `EventHandler` переопределяет методы `on_text_created`, `on_text_delta`, `on_tool_call_created` и `on_tool_call_delta` для обработки соответствующих событий. При получении события вызывается соответствующий метод, который выполняет определенные действия, такие как печать текста или обработка вызовов инструментов.

## Методы класса

### `on_text_created`

```python
def on_text_created(self, text: Text) -> None:
    """Обработчик события создания текста.

    Выводит символ ">" в консоль.

    Args:
        text (Text): Объект `Text`, представляющий созданный текст.

    Returns:
        None

    Example:
        >>> event_handler = EventHandler()
        >>> from openai.types.beta.threads import Text
        >>> text = Text(id='text_id', value='Привет, мир!', created_at=1680000000, thread_id='thread_id', run_id='run_id', type='text')
        >>> event_handler.on_text_created(text)
        
        assistant >
    """
    print(f"\nassistant > ", end="", flush=True)
```

### `on_text_delta`

```python
def on_text_delta(self, delta: TextDelta, snapshot: Text):
    """Обработчик события изменения текста.

    Выводит изменение текста в консоль.

    Args:
        delta (TextDelta): Объект `TextDelta`, представляющий изменение текста.
        snapshot (Text): Объект `Text`, представляющий текущий снимок текста.

    Returns:
        None

    Example:
        >>> event_handler = EventHandler()
        >>> from openai.types.beta.threads import TextDelta, Text
        >>> delta = TextDelta(id='delta_id', value='!', created_at=1680000000, thread_id='thread_id', run_id='run_id', type='text', text=None)
        >>> snapshot = Text(id='text_id', value='Привет, мир', created_at=1680000000, thread_id='thread_id', run_id='run_id', type='text')
        >>> event_handler.on_text_delta(delta, snapshot)
        !
    """
    print(delta.value, end="", flush=True)
```

### `on_tool_call_created`

```python
def on_tool_call_created(self, tool_call: ToolCall):
    """Обработчик события создания вызова инструмента.

    Выводит тип инструмента в консоль.

    Args:
        tool_call (ToolCall): Объект `ToolCall`, представляющий вызов инструмента.

    Returns:
        None

    Example:
        >>> event_handler = EventHandler()
        >>> from openai.types.beta.threads.runs import ToolCall
        >>> tool_call = ToolCall(id='tool_call_id', type='code_interpreter', code_interpreter=None, function=None)
        >>> event_handler.on_tool_call_created(tool_call)
        
        assistant > code_interpreter
    """
    print(f"\nassistant > {tool_call.type}\n", flush=True)
```

### `on_tool_call_delta`

```python
def on_tool_call_delta(self, delta: ToolCallDelta, snapshot: ToolCall):
    """Обработчик события изменения вызова инструмента.

    Обрабатывает изменения, связанные с code_interpreter, такие как ввод и вывод.

    Args:
        delta (ToolCallDelta): Объект `ToolCallDelta`, представляющий изменение вызова инструмента.
        snapshot (ToolCall): Объект `ToolCall`, представляющий текущий снимок вызова инструмента.

    Returns:
        None

    Example:
        >>> event_handler = EventHandler()
        >>> from openai.types.beta.threads.runs import ToolCallDelta, ToolCall
        >>> from openai.types.beta.threads.runs import CodeInterpreter, CodeInterpreterDelta
        >>> delta = ToolCallDelta(id='delta_id', type='code_interpreter', code_interpreter=CodeInterpreterDelta(input='print("Hello")', outputs=None), function=None)
        >>> snapshot = ToolCall(id='tool_call_id', type='code_interpreter', code_interpreter=CodeInterpreter(input='print("Hello")', outputs=None), function=None)
        >>> event_handler.on_tool_call_delta(delta, snapshot)
        print("Hello")
    """
    if delta.type == "code_interpreter" and delta.code_interpreter:
      if delta.code_interpreter.input:
        print(delta.code_interpreter.input, end="", flush=True)
      if delta.code_interpreter.outputs:
        print(f"\n\noutput >", flush=True)
        for output in delta.code_interpreter.outputs:
          if output.type == "logs":
            print(f"\n{output.logs}", flush=True)
```

## Примеры

```python
# Пример использования класса EventHandler
from openai import OpenAI
from src.ai.openai.model.event_handler import EventHandler

# Создание клиента OpenAI
client = OpenAI()

# Создание ассистента (пример)
assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="You are a personal math tutor. Write and run code to answer math questions.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4"
)

# Создание потока (thread)
thread = client.beta.threads.create()

# Добавление сообщения в поток
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="I need to solve the equation `3x + 11 = 14`. Can you help me?"
)

# Запуск (run) с использованием EventHandler
run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
  event_handler=EventHandler(), # Использование EventHandler
  instructions="Please be verbose and explain your steps."
)

# Ожидание завершения запуска
while run.status != "completed":
    run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    print(f"Run status: {run.status}")

# Получение сообщений из потока
messages = client.beta.threads.messages.list(thread_id=thread.id)
print(messages.data)