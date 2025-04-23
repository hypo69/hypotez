### **Как использовать этот блок кода**
=========================================================================================

Описание
-------------------------
Этот блок кода определяет класс `EventHandler`, который наследуется от `AssistantEventHandler` из библиотеки `openai`. `EventHandler` переопределяет методы для обработки различных событий, возникающих в процессе выполнения ассистента OpenAI, таких как создание текста, изменение текста, создание вызова инструмента и изменение вызова инструмента. Это позволяет настроить поведение приложения в зависимости от событий, генерируемых ассистентом.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются классы `AssistantEventHandler`, `OpenAI` из библиотеки `openai`.
   - Импортируются классы `Text`, `TextDelta`, `ToolCall`, `ToolCallDelta` из библиотеки `openai.types.beta.threads.runs`.
   - Импортируется декоратор `override` из библиотеки `typing_extensions`.

2. **Создание класса `EventHandler`**:
   - Определяется класс `EventHandler`, наследующий `AssistantEventHandler`.

3. **Переопределение метода `on_text_created`**:
   - Метод вызывается при создании текстового объекта.
   - Функция выводит в консоль строку "assistant >".

4. **Переопределение метода `on_text_delta`**:
   - Метод вызывается при изменении текстового объекта.
   - Функция выводит в консоль добавленное значение (`delta.value`).

5. **Переопределение метода `on_tool_call_created`**:
   - Метод вызывается при создании вызова инструмента.
   - Функция выводит в консоль тип вызванного инструмента (`tool_call.type`).

6. **Переопределение метода `on_tool_call_delta`**:
   - Метод вызывается при изменении вызова инструмента.
   - Функция проверяет, является ли тип инструмента `code_interpreter`.
   - Если тип инструмента `code_interpreter`, то функция выводит в консоль входные и выходные данные интерпретатора кода.

Пример использования
-------------------------

```python
    from openai import OpenAI

    client = OpenAI()

    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="Посчитай сколько будет 10 + 20",
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id="asst_E5Kxx2QV0WjQzk7avyRcWMVa",
        # events are printed to the console
        event_handler=EventHandler(),
    )

    # stream events to the handler
    run = client.beta.threads.runs.stream(run.id, thread_id=thread.id, event_handler=EventHandler())
    run.join()
```