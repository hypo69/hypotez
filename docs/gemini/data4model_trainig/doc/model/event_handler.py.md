## Обработчик событий OpenAI Assistant

### Обзор

Модуль предоставляет инструменты для обработки событий, связанных с ассистентами OpenAI, в частности для управления выводом информации в процессе выполнения задач.

### Подробней

Модуль содержит класс `EventHandler`, который наследует `AssistantEventHandler` из библиотеки `openai` и переопределяет его методы для управления выводом текста, информации о вызовах инструментов и отладочной информации.

## Классы

### `EventHandler`

**Описание**: Класс для обработки событий ассистента OpenAI.

**Наследует**: `AssistantEventHandler`

**Методы**:

*   `on_text_created()`: Обрабатывает событие создания текстового объекта.
*   `on_text_delta()`: Обрабатывает событие получения дельты текстового объекта.
*   `on_tool_call_created()`: Обрабатывает событие создания вызова инструмента.
*   `on_tool_call_delta()`: Обрабатывает событие получения дельты вызова инструмента.

### `on_text_created`

```python
@override
def on_text_created(self, text: Text) -> None:
    print(f"\nassistant > ", end="", flush=True)
```

**Назначение**: Обрабатывает событие создания текстового объекта.

**Параметры**:
*   `text` (Text): Объект, представляющий текстовый фрагмент.

**Как работает функция**:

1.  Выводит в консоль строку `"assistant > "`.

### `on_text_delta`

```python
@override
def on_text_delta(self, delta: TextDelta, snapshot: Text):
    print(delta.value, end="", flush=True)
```

**Назначение**: Обрабатывает событие получения дельты текстового объекта.

**Параметры**:

*   `delta` (TextDelta): Дельта текстового объекта.
*   `snapshot` (Text): Текущий снимок текстового объекта.

**Как работает функция**:

1.  Выводит в консоль значение дельты.

### `on_tool_call_created`

```python
@override
def on_tool_call_created(self, tool_call: ToolCall):
    print(f"\nassistant > {tool_call.type}\\n", flush=True)
```

**Назначение**: Обрабатывает событие создания вызова инструмента.

**Параметры**:

*   `tool_call` (ToolCall): Объект, представляющий вызов инструмента.

**Как работает функция**:

1.  Выводит в консоль тип вызванного инструмента.

### `on_tool_call_delta`

```python
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
```

**Назначение**: Обрабатывает событие получения дельты вызова инструмента.

**Параметры**:

*   `delta` (ToolCallDelta): Дельта вызова инструмента.
*   `snapshot` (ToolCall): Текущий снимок вызова инструмента.

**Как работает функция**:

1.  Проверяет, является ли инструмент интерпретатором кода.
2.  Если является, выводит в консоль входные данные и результаты выполнения кода.

## Общее описание логики работы модуля

Модуль предоставляет класс `EventHandler`, который переопределяет методы `AssistantEventHandler` из библиотеки `openai`, чтобы настроить вывод информации о процессе взаимодействия с моделью OpenAI. Это позволяет отслеживать этапы генерации текста и выполнения инструментов.

## Зависимости

*   `typing_extensions`: Для использования декоратора `@override`.
*   `openai`: Для работы с API OpenAI и классами `AssistantEventHandler`, `Text`, `TextDelta`, `ToolCall`, `ToolCallDelta`.

## Замечания

В коде отсутствует пример использования, но в описании сказано, что модуль можно использовать для "создания Run и стриминга response".

Обратите внимание:
*   Необходимо установить библиотеку `openai` для работы с OpenAI API и иметь активную подписку.
*   В коде не предусмотрена обработка исключений в методах класса `EventHandler`, рекомендуется добавить логирование для более информативной отладки.
*   Не рекомендуется использовать print в production коде, стоит перенести логирование в модуль Logger
*   Используйте более информативные имена для атрибутов, параметров и переменных.