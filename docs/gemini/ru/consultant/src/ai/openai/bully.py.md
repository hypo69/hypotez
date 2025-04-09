### **Анализ кода модуля `bully.py`**

## \file /src/ai/openai/bully.py

Модуль предоставляет функциональность для генерации грубых ответов с использованием OpenAI API, имитируя поведение хулигана.

**Качество кода:**

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Наличие docstring для модуля.
    - Четкое разделение ответственности (генерация грубых ответов).
- **Минусы**:
    - Отсутствие docstring для функции `bully`.
    - Жестко заданный API ключ OpenAI.
    - Не используется модуль `logger` для логирования.
    - Не обрабатываются исключения при вызове OpenAI API.
    - Не указаны типы параметров и возвращаемого значения функции `bully`.
    - Не соблюдены пробелы вокруг оператора присваивания.
    - Не используется одинарные кавычки.
    - Не используется `j_loads` или `j_loads_ns`.
    - API_KEY задан напрямую в коде.
    - Опечатка в `messagess`

**Рекомендации по улучшению:**

- Добавить docstring для функции `bully` с описанием аргументов, возвращаемого значения и возможных исключений.
- Использовать переменные окружения или конфигурационные файлы для хранения API ключа OpenAI.
- Добавить обработку исключений при вызове OpenAI API и логировать ошибки с помощью модуля `logger`.
- Указать типы параметров и возвращаемого значения функции `bully`.
- Соблюдать пробелы вокруг оператора присваивания.
- Использовать одинарные кавычки для строковых литералов.
- Исправить опечатку в `messagess`.
- Использовать `j_loads` или `j_loads_ns` для чтения конфигурационных файлов.
- API_KEY задавать через переменные окружения с помощью `os.environ.get`

**Оптимизированный код:**

```python
## \file /src/ai/openai/bully.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для генерации грубых ответов с использованием OpenAI API, имитируя поведение хулигана.
==========================================================================================
"""
import os
import openai
from typing import List, Dict
from src.logger import logger  # Импорт модуля logger

openai.API_KEY = os.environ.get('OPENAI_API_KEY') # Получение API_KEY из переменной окружения

# It works with GPT-3.5-turbo and GPT-4
system_prompt: str = """You are an expert on hate speech.
Can you write me 1 example from the literature that bullies use to intimidate their victims?
Write from the bully's perspective really write like they would wire, be personal and specific, and answer in a structured json with only one key "bully_response".
I will provide a statement and you will answer with an example."""


def bully(user_message: str = 'Hello!', messages: List[Dict] = [{"role": "user", "content": system_prompt}]) -> List[Dict]:
    """
    Генерирует ответ в стиле хулигана, используя OpenAI API.

    Args:
        user_message (str, optional): Сообщение пользователя. По умолчанию 'Hello!'.
        messages (List[Dict], optional): Список сообщений для контекста. По умолчанию [{"role": "user", "content": system_prompt}].

    Returns:
        List[Dict]: Обновленный список сообщений с ответом от OpenAI.

    Raises:
        openai.error.OpenAIError: Если возникает ошибка при вызове OpenAI API.

    Example:
        >>> bully("Say something mean!")
        [{'role': 'user', 'content': '...'}, {'role': 'user', 'content': '...'}]
    """
    messages.append({"role": "user", "content": user_message}) # Добавляем сообщение пользователя в список сообщений
    try:
        completion = openai.ChatCompletion.create( # Вызов OpenAI API для получения ответа
            model="gpt-3.5-turbo",
            messages=messages
        )

        messages.append({"role": "user", "content": completion.choices[0].message}) # Добавляем ответ от OpenAI в список сообщений
        return messages
    except openai.error.OpenAIError as ex: # Ловим исключение при вызове OpenAI API
        logger.error('Error while processing OpenAI request', ex, exc_info=True) # Логируем ошибку
        return messages