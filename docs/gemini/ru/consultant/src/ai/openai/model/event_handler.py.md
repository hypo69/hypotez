### **Анализ кода модуля `event_handler.py`**

**Качество кода:**

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Использование `typing_extensions` для `override`.
    - Класс `EventHandler` структурирован для обработки событий ассистента.
    - Четкое разделение методов для различных типов событий.
- **Минусы**:
    - Отсутствует docstring для модуля, класса и методов.
    - Не используются логирование.
    - Отсутствуют аннотации типов для переменных.
    - Не реализована обработка исключений.
    - Комментарии к коду не соответствуют требованиям к оформлению в проекте.
    - Нет интеграции с `logger` для логирования.

**Рекомендации по улучшению:**

1.  **Добавить docstring для модуля**:
    - Описать назначение модуля, основные классы и примеры использования.

2.  **Добавить docstring для класса `EventHandler`**:
    - Описать роль класса и его методы.

3.  **Добавить docstring для каждого метода класса `EventHandler`**:
    - Описать параметры, возвращаемые значения и возможные исключения.

4.  **Использовать логирование**:
    - Заменить `print` на `logger.info` и `logger.error` для записи информации и ошибок.
    - Добавить обработку исключений с логированием ошибок.

5.  **Добавить аннотации типов**:
    - Указать типы для всех переменных и возвращаемых значений.

6.  **Улучшить обработку ошибок**:
    - Добавить блоки `try-except` для обработки возможных исключений и логирования ошибок.

7.  **Форматирование кода**:
    - Использовать одинарные кавычки для строк.
    - Добавить пробелы вокруг операторов.

**Оптимизированный код:**

```python
                ## \file /src/ai/openai/model/event_handler.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для обработки событий ассистента OpenAI
=================================================

Модуль содержит класс :class:`EventHandler`, который используется для обработки различных событий,
возникающих при взаимодействии с ассистентом OpenAI, таких как создание текста, изменение текста,
вызовы инструментов и т.д.

Пример использования
----------------------

>>> from openai import OpenAI
>>> client = OpenAI()
>>> event_handler = EventHandler()
>>> # some_run = client.beta.threads.runs.create(...)
>>> # stream = client.beta.threads.runs.stream(run_id=some_run.id, event_handler=event_handler)
"""

from typing_extensions import override
from openai import AssistantEventHandler, OpenAI
from openai.types.beta.threads import Text, TextDelta
from openai.types.beta.threads.runs import ToolCall, ToolCallDelta

from src.logger import logger


# First, we create a EventHandler class to define
# how we want to handle the events in the response stream.

class EventHandler(AssistantEventHandler):
  """
    Класс для обработки событий ассистента OpenAI.

    Этот класс переопределяет методы `AssistantEventHandler` для обработки различных событий,
    таких как создание текста, изменение текста и вызовы инструментов.
  """

  @override
  def on_text_created(self, text: Text) -> None:
    """
        Обработчик события создания текста.

        Выводит информацию о создании текста ассистентом.

        Args:
            text (Text): Объект, содержащий информацию о созданном тексте.

        Returns:
            None
        """
    try:
      logger.info("\nassistant > ", end="", flush=True)
    except Exception as ex:
      logger.error("Error in on_text_created", ex, exc_info=True)

  @override
  def on_text_delta(self, delta: TextDelta, snapshot: Text) -> None:
    """
        Обработчик события изменения текста.

        Выводит изменения текста ассистента.

        Args:
            delta (TextDelta): Объект, содержащий информацию об изменении текста.
            snapshot (Text): Объект, содержащий текущий снимок текста.

        Returns:
            None
        """
    try:
      logger.info(delta.value, end="", flush=True)
    except Exception as ex:
      logger.error("Error in on_text_delta", ex, exc_info=True)

  @override
  def on_tool_call_created(self, tool_call: ToolCall) -> None:
    """
        Обработчик события создания вызова инструмента.

        Выводит информацию о создании вызова инструмента ассистентом.

        Args:
            tool_call (ToolCall): Объект, содержащий информацию о вызове инструмента.

        Returns:
            None
        """
    try:
      logger.info(f"\nassistant > {tool_call.type}\n", flush=True)
    except Exception as ex:
      logger.error("Error in on_tool_call_created", ex, exc_info=True)

  @override
  def on_tool_call_delta(self, delta: ToolCallDelta, snapshot: ToolCall) -> None:
    """
        Обработчик события изменения вызова инструмента.

        Выводит изменения, связанные с вызовом инструмента ассистентом, включая ввод и вывод code_interpreter.

        Args:
            delta (ToolCallDelta): Объект, содержащий информацию об изменении вызова инструмента.
            snapshot (ToolCall): Объект, содержащий текущий снимок вызова инструмента.

        Returns:
            None
        """
    try:
      if delta.type == "code_interpreter" and delta.code_interpreter:
        if delta.code_interpreter.input:
          logger.info(delta.code_interpreter.input, end="", flush=True)
        if delta.code_interpreter.outputs:
          logger.info("\n\noutput >", flush=True)
          for output in delta.code_interpreter.outputs:
            if output.type == "logs":
              logger.info(f"\n{output.logs}", flush=True)
    except Exception as ex:
      logger.error("Error in on_tool_call_delta", ex, exc_info=True)

# Then, we use the `stream` SDK helper
# with the `EventHandler` class to create the Run
# and stream the response.