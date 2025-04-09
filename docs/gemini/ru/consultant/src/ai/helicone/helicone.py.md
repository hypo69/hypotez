### **Анализ кода модуля `helicone.py`**

## \file /src/ai/helicone/helicone.py

#### **Качество кода**:
- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Код выполняет основные функции, описанные в комментариях.
    - Присутствуют docstring для функций.
- **Минусы**:
    - Отсутствуют аннотации типов для параметров `__init__`.
    - Docstring написаны на английском языке, требуется перевод на русский.
    - Не используются менеджеры контекста (with ... as) при работе с Helicone и OpenAI.
    - Не обрабатываются исключения.
    - Не используется модуль логирования `logger` из `src.logger`.
    - Зависимость от сторонней библиотеки `header`.
    - Отсутствует описание модуля в начале файла.
    - Не везде используется одинарная кавычка

#### **Рекомендации по улучшению**:
1.  **Добавить описание модуля в начале файла**:
    - Необходимо добавить docstring в начале файла с описанием модуля и примером использования.
2.  **Использовать аннотации типов**:
    - Добавить аннотации типов для параметров в методе `__init__`.
3.  **Перевести docstring на русский язык**:
    - Все docstring должны быть переведены на русский язык в формате UTF-8.
4.  **Обработка исключений**:
    - Добавить обработку исключений с использованием `try...except` и логированием ошибок через `logger.error`.
5.  **Использовать менеджеры контекста**:
    - Использовать `with` для гарантированного закрытия соединения.
6.  **Удалить зависимость от `header`**:
    - Проанализировать и, если возможно, удалить зависимость от неопределенного модуля `header`.
7. **Улучшить форматирование кода**:
    - Использовать одинарные кавычки для строк.
8. **Использовать f-строки**:
    - В функциях `analyze_sentiment`, `summarize_text`, `translate_text` использовать f-строки для форматирования промптов.
9. **Удалить main()**:
    - Код с примерами использования вынести в отдельный файл `/src/ai/helicone/examples.py` или в тесты.
    - Модуль `HeliconeAI` не должен содержать примеров использовния в `main()`

#### **Оптимизированный код**:
```python
"""
Модуль для интеграции с Helicone AI
======================================

Модуль содержит класс :class:`HeliconeAI`, который упрощает взаимодействие с API Helicone AI
для выполнения различных задач, таких как генерация стихов, анализ тональности, суммирование текста и перевод.

Пример использования
----------------------

>>> from src.ai.helicone.helicone import HeliconeAI
>>> helicone_ai = HeliconeAI()
>>> poem = helicone_ai.generate_poem("Напиши мне стихотворение про кота.")
>>> print(poem)
"""

from typing import Optional
from helicone import Helicone
from openai import OpenAI
from src.logger import logger

class HeliconeAI:
    """
    Класс для взаимодействия с Helicone AI.
    """
    def __init__(self) -> None:
        """
        Инициализирует Helicone и OpenAI клиенты.
        """
        try:
            self.helicone = Helicone()
            self.client = OpenAI()
        except Exception as ex:
            logger.error('Ошибка при инициализации Helicone или OpenAI', ex, exc_info=True)
            raise

    def generate_poem(self, prompt: str) -> str:
        """
        Генерирует стихотворение на основе заданного промпта.

        Args:
            prompt (str): Промпт для генерации стихотворения.

        Returns:
            str: Сгенерированное стихотворение.
        """
        try:
            response = self.client.chat.completions.create(
                model='gpt-3.5-turbo',
                messages=[
                    {'role': 'user', 'content': prompt}
                ]
            )
            self.helicone.log_completion(response)
            return response.choices[0].message.content
        except Exception as ex:
            logger.error('Ошибка при генерации стихотворения', ex, exc_info=True)
            return ''

    def analyze_sentiment(self, text: str) -> str:
        """
        Анализирует тональность текста.

        Args:
            text (str): Текст для анализа.

        Returns:
            str: Результат анализа тональности.
        """
        try:
            response = self.client.completions.create(
                model='text-davinci-003',
                prompt=f'Analyze the sentiment of the following text: {text}',
                max_tokens=50
            )
            self.helicone.log_completion(response)
            return response.choices[0].text.strip()
        except Exception as ex:
            logger.error('Ошибка при анализе тональности', ex, exc_info=True)
            return ''

    def summarize_text(self, text: str) -> str:
        """
        Создает краткое изложение текста.

        Args:
            text (str): Текст для изложения.

        Returns:
            str: Краткое изложение текста.
        """
        try:
            response = self.client.completions.create(
                model='text-davinci-003',
                prompt=f'Summarize the following text: {text}',
                max_tokens=100
            )
            self.helicone.log_completion(response)
            return response.choices[0].text.strip()
        except Exception as ex:
            logger.error('Ошибка при создании краткого изложения текста', ex, exc_info=True)
            return ''

    def translate_text(self, text: str, target_language: str) -> str:
        """
        Переводит текст на указанный язык.

        Args:
            text (str): Текст для перевода.
            target_language (str): Целевой язык перевода.

        Returns:
            str: Переведенный текст.
        """
        try:
            response = self.client.completions.create(
                model='text-davinci-003',
                prompt=f'Translate the following text to {target_language}: {text}',
                max_tokens=200
            )
            self.helicone.log_completion(response)
            return response.choices[0].text.strip()
        except Exception as ex:
            logger.error('Ошибка при переводе текста', ex, exc_info=True)
            return ''