# Модуль для обработки событий модели OpenAI

## Обзор

Модуль `event_handler.py` предоставляет класс `EventHandler`, который используется для обработки событий, возникающих при взаимодействии с моделью OpenAI. 

## Подробней

Класс `EventHandler` наследует от `AssistantEventHandler` библиотеки `openai-python` и переопределяет методы, которые вызываются при возникновении различных событий во время работы модели. 

## Классы

### `EventHandler`

**Описание**: Класс, который обрабатывает события, возникающие при взаимодействии с моделью OpenAI.

**Наследует**: `AssistantEventHandler`

**Методы**:

- `on_text_created(self, text: Text) -> None`
    - **Описание**: Вызывается при создании нового текстового сообщения модели.
    - **Параметры**:
        - `text (Text)`: Объект `Text`, представляющий текст сообщения.
    - **Возвращает**: `None`

- `on_text_delta(self, delta: TextDelta, snapshot: Text) -> None`
    - **Описание**: Вызывается при изменении текстового сообщения модели.
    - **Параметры**:
        - `delta (TextDelta)`: Объект `TextDelta`, представляющий изменение.
        - `snapshot (Text)`: Объект `Text`, представляющий текущий текст сообщения.
    - **Возвращает**: `None`

- `on_tool_call_created(self, tool_call: ToolCall) -> None`
    - **Описание**: Вызывается при создании нового вызова инструмента.
    - **Параметры**:
        - `tool_call (ToolCall)`: Объект `ToolCall`, представляющий вызов инструмента.
    - **Возвращает**: `None`

- `on_tool_call_delta(self, delta: ToolCallDelta, snapshot: ToolCall) -> None`
    - **Описание**: Вызывается при изменении вызова инструмента.
    - **Параметры**:
        - `delta (ToolCallDelta)`: Объект `ToolCallDelta`, представляющий изменение.
        - `snapshot (ToolCall)`: Объект `ToolCall`, представляющий текущий вызов инструмента.
    - **Возвращает**: `None`

**Пример использования**:

```python
from src.ai.openai.model.event_handler import EventHandler

# Создаем экземпляр класса EventHandler
event_handler = EventHandler()

# Используем event_handler для обработки событий модели OpenAI
# ...
```