### **Анализ кода модуля `kazarinov.py`**

## \file /src/ai/openai/model/_experiments/kazarinov.py

Модуль представляет собой эксперимент по интеграции с OpenAI для создания чат-бота. Он включает в себя класс `OpenAIChat` для взаимодействия с OpenAI API и функцию `chat` для организации диалога с пользователем.

**Качество кода:**

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Использование логгера для обработки ошибок.
    - Четкое разделение на классы и функции.
    - Использование `Path` для работы с путями к файлам.
- **Минусы**:
    - Отсутствие аннотаций типов.
    - Неполная документация.
    - Не используются одинарные кавычки.
    - Не используется `j_loads` для загрузки `system_instruction`.
    - Не соблюдается PEP8.
    - Исключение `e` не переименовано в `ex`.
    - Нет обработки случая, когда `system_instruction` не найден.
    - Не все строки соответствуют PEP8 (например, импорты).

**Рекомендации по улучшению:**

1.  **Добавить аннотации типов:** Для всех переменных, аргументов функций и возвращаемых значений необходимо добавить аннотации типов.
2.  **Дополнить документацию:** Добавить docstring к модулю, классам и функциям, описывающие их назначение, аргументы, возвращаемые значения и возможные исключения. Перевести существующую документацию на русский язык.
3.  **Исправить стиль кода:**
    *   Использовать только одинарные кавычки.
    *   Добавить пробелы вокруг операторов присваивания.
    *   Соблюдать PEP8 для импортов (например, импортировать несколько объектов из одного модуля в одной строке).
4.  **Использовать `j_loads`:** Заменить чтение файла `system_instruction` с использованием `open` и `read_text_file` на `j_loads`.
5.  **Переименовать исключение:** Переименовать переменную исключения `e` в `ex` в блоке `try...except`.
6.  **Добавить обработку ошибок:** Добавить проверку на существование файла `system_instruction` и обработку случая, когда файл не найден.
7.  **Улучшить логирование:** Добавить контекстную информацию в логи, чтобы облегчить отладку.
8.  **Добавить примеры использования:** Добавить примеры использования класса `OpenAIChat` и функции `chat` в docstring.

**Оптимизированный код:**

```python
                ## \file /src/ai/openai/model/_experiments/kazarinov.py
# -*- coding: utf-8 -*-

"""
Модуль для экспериментов с интеграцией OpenAI.
==================================================

Модуль содержит класс :class:`OpenAIChat` для взаимодействия с OpenAI API и функцию :func:`chat`
для организации диалога с пользователем.

Пример использования:
----------------------

>>> from src.ai.openai.model._experiments.kazarinov import OpenAIChat, chat
>>> api_key = 'YOUR_API_KEY'  # Замените на ваш фактический API ключ
>>> system_instruction_path = 'path/to/system_instruction.txt'
>>> ai = OpenAIChat(api_key=api_key, system_instruction_path=system_instruction_path)
>>> response = ai.ask(prompt='Hello, OpenAI!')
>>> print(response)

>>> chat() # Запускает интерактивный чат
"""

import openai
from pathlib import Path

from src import gs
from src.logger.logger import logger
from src.utils.file import read_text_file


# Инициализация OpenAI модели
class OpenAIChat:
    """
    Класс для взаимодействия с OpenAI Chat API.

    Args:
        api_key (str): API ключ OpenAI.
        system_instruction_path (str | Path, optional): Путь к файлу с системной инструкцией. Defaults to None.

    Raises:
        FileNotFoundError: Если файл с системной инструкцией не найден.

    Example:
        >>> api_key = 'YOUR_API_KEY'
        >>> system_instruction_path = 'path/to/system_instruction.txt'
        >>> ai = OpenAIChat(api_key=api_key, system_instruction_path=system_instruction_path)
        >>> response = ai.ask(prompt='Hello, OpenAI!')
        >>> print(response)
    """

    def __init__(self, api_key: str, system_instruction_path: str | Path = None) -> None:
        """Инициализация класса OpenAIChat."""
        openai.api_key = gs.credentials
        self.system_instruction = None
        self.messages = []

        if system_instruction_path:
            try:
                self.system_instruction = read_text_file(system_instruction_path)
                if self.system_instruction:
                    self.messages.append({'role': 'system', 'content': self.system_instruction})
            except FileNotFoundError as ex:
                logger.error(f'Файл с системной инструкцией не найден: {system_instruction_path}', ex, exc_info=True)
                raise FileNotFoundError(f'Файл с системной инструкцией не найден: {system_instruction_path}') from ex
            except Exception as ex:
                logger.error(f'Ошибка при чтении файла системной инструкции: {system_instruction_path}', ex, exc_info=True)
                raise

    def ask(self, prompt: str) -> str:
        """
        Отправляет вопрос в модель OpenAI и возвращает ответ.

        Args:
            prompt (str): Вопрос пользователя.

        Returns:
            str: Ответ от OpenAI.
        """
        self.messages.append({'role': 'user', 'content': prompt})

        try:
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=self.messages,
                max_tokens=150,
                temperature=0.7
            )
            answer = response['choices'][0]['message']['content']
            self.messages.append({'role': 'assistant', 'content': answer})
            return answer
        except Exception as ex:
            logger.error('Ошибка при обработке запроса к OpenAI', ex, exc_info=True)
            return 'Произошла ошибка при обработке запроса.'


def chat() -> None:
    """
    Функция для организации интерактивного чата с OpenAI.

    Example:
        >>> chat()
        Добро пожаловать в чат с OpenAI!
        Чтобы завершить чат, напишите 'exit'.

        Введите ваш OpenAI API ключ: YOUR_API_KEY
        > вопрос
        > Hello, OpenAI!
        >> ответ
        >> Hello! How can I assist you today?
    """
    print('Добро пожаловать в чат с OpenAI!')
    print("Чтобы завершить чат, напишите 'exit'.\n")

    # Ввод ключа API и инициализация модели
    api_key = input('Введите ваш OpenAI API ключ: ')
    system_instruction_path = Path('../src/ai/openai/model/_experiments/system_instruction.txt')
    ai = OpenAIChat(api_key=api_key, system_instruction_path=system_instruction_path)

    while True:
        # Получаем вопрос от пользователя
        user_input = input('> вопрос\n> ')

        if user_input.lower() == 'exit':
            print('Чат завершен.')
            break

        # Отправляем запрос модели и получаем ответ
        response = ai.ask(prompt=user_input)

        # Выводим ответ
        print(f'>> ответ\n>> {response}\n')


if __name__ == '__main__':
    chat()