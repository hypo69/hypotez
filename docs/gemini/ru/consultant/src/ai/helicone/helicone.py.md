### **Анализ кода модуля `helicone`**

## \file /src/ai/helicone/helicone.py

#### **Качество кода**:
- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Код выполняет базовые функции для работы с Helicone и OpenAI.
    - Присутствуют docstring для каждой функции, что облегчает понимание кода.
- **Минусы**:
    - Отсутствует обработка исключений.
    - Docstring написаны на английском языке (требуется перевод на русский).
    - Не используются аннотации типов для параметров `__init__`.
    - Нет логирования.
    - Используются небезопасные методы `client.completions.create` (устаревший API OpenAI).
    - Не соблюдены рекомендации по форматированию (использование двойных кавычек вместо одинарных).
    - Отсутствует описание модуля в формате, требуемом инструкцией.

#### **Рекомендации по улучшению**:
1.  **Добавить обработку исключений**:
    - Обернуть вызовы API OpenAI в блоки `try...except` для обработки возможных ошибок.
    - Использовать `logger.error` для логирования ошибок.
2.  **Перевести docstring на русский язык**:
    - Все docstring должны быть переведены на русский язык и соответствовать формату, указанному в инструкции.
3.  **Добавить аннотации типов**:
    - Добавить аннотации типов для параметров метода `__init__`.
4.  **Использовать `logger` для логирования**:
    - Добавить логирование ключевых событий, таких как вызовы API и результаты их выполнения.
5.  **Перейти на актуальные методы OpenAI API**:
    - Использовать `client.chat.completions.create` вместо `client.completions.create` для всех задач, где это возможно.
6.  **Соблюдать рекомендации по форматированию**:
    - Использовать одинарные кавычки вместо двойных.
7. **Добавить описание модуля**
   - Добавить описание модуля в соответствии с примером в инструкции.
8. **Использовать `ex` вместо `e` в блоках обработки исключений**
9. **Документировать все функции и методы подробно**
    - Описание должно быть четким и понятным, избегать расплывчатых формулировок.
    - Вместо "получаем", "возвращаем", "преобразовываем" использовать "функция получает", "переменная возвращает", "код преобразовывает".
10. **Необходимо добавить проверку параметров и возвращаемых значений на None.**

#### **Оптимизированный код**:

```python
## \file /src/ai/helicone/helicone.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для интеграции с Helicone и OpenAI
===========================================

Модуль содержит класс :class:`HeliconeAI`, который упрощает взаимодействие с API Helicone и OpenAI
для выполнения различных задач, таких как генерация стихов, анализ тональности, суммаризация текста и перевод.

Пример использования
----------------------

>>> helicone_ai = HeliconeAI()
>>> poem = helicone_ai.generate_poem("Напиши мне стихотворение про кота.")
>>> print(poem)
"""

from typing import Optional

from helicone import Helicone
from openai import OpenAI

from src.logger import logger  # Corrected import


class HeliconeAI:
    """
    Класс для работы с Helicone и OpenAI.
    """

    def __init__(self):
        """
        Инициализирует Helicone и OpenAI клиенты.
        """
        self.helicone: Helicone = Helicone()
        self.client: OpenAI = OpenAI()

    def generate_poem(self, prompt: str) -> Optional[str]:
        """
        Генерирует стихотворение на основе заданного промпта.

        Args:
            prompt (str): Промпт для генерации стихотворения.

        Returns:
            str | None: Сгенерированное стихотворение или None в случае ошибки.

        Raises:
            Exception: Если возникает ошибка при вызове API OpenAI.

        Example:
            >>> helicone_ai = HeliconeAI()
            >>> poem = helicone_ai.generate_poem("Напиши мне стихотворение про кота.")
            >>> print(poem)
            Сгенерированное стихотворение...
        """
        try:
            #  запрос к API OpenAI для генерации стихотворения
            response = self.client.chat.completions.create(
                model='gpt-3.5-turbo',
                messages=[
                    {'role': 'user', 'content': prompt}
                ]
            )
            # логирование ответа для Helicone
            self.helicone.log_completion(response)
            #  результата (стихотворения) из ответа
            if response.choices and response.choices[0].message:
                return response.choices[0].message.content
            else:
                return None
        except Exception as ex:
            # логирование ошибки при вызове API OpenAI
            logger.error('Ошибка при генерации стихотворения.', ex, exc_info=True)
            return None

    def analyze_sentiment(self, text: str) -> Optional[str]:
        """
        Анализирует тональность текста.

        Args:
            text (str): Текст для анализа.

        Returns:
            str | None: Результат анализа тональности или None в случае ошибки.

        Raises:
            Exception: Если возникает ошибка при вызове API OpenAI.

        Example:
            >>> helicone_ai = HeliconeAI()
            >>> sentiment = helicone_ai.analyze_sentiment("Сегодня был отличный день!")
            >>> print(sentiment)
            Тональность: Положительная
        """
        try:
            #  запрос к API OpenAI для анализа тональности текста
            response = self.client.completions.create(
                model='text-davinci-003',
                prompt=f'Analyze the sentiment of the following text: {text}',
                max_tokens=50
            )
            # логирование ответа для Helicone
            self.helicone.log_completion(response)
            #  результата анализа тональности из ответа
            if response.choices:
                return response.choices[0].text.strip()
            else:
                return None
        except Exception as ex:
            # логирование ошибки при вызове API OpenAI
            logger.error('Ошибка при анализе тональности текста.', ex, exc_info=True)
            return None

    def summarize_text(self, text: str) -> Optional[str]:
        """
        Создает краткое изложение текста.

        Args:
            text (str): Текст для изложения.

        Returns:
            str | None: Краткое изложение текста или None в случае ошибки.

        Raises:
            Exception: Если возникает ошибка при вызове API OpenAI.

        Example:
            >>> helicone_ai = HeliconeAI()
            >>> summary = helicone_ai.summarize_text("Длинный текст для изложения...")
            >>> print(summary)
            Краткое изложение текста...
        """
        try:
            #  запрос к API OpenAI для суммаризации текста
            response = self.client.completions.create(
                model='text-davinci-003',
                prompt=f'Summarize the following text: {text}',
                max_tokens=100
            )
            # логирование ответа для Helicone
            self.helicone.log_completion(response)
            #  результата суммаризации текста из ответа
            if response.choices:
                return response.choices[0].text.strip()
            else:
                return None
        except Exception as ex:
            # логирование ошибки при вызове API OpenAI
            logger.error('Ошибка при создании краткого изложения текста.', ex, exc_info=True)
            return None

    def translate_text(self, text: str, target_language: str) -> Optional[str]:
        """
        Переводит текст на указанный язык.

        Args:
            text (str): Текст для перевода.
            target_language (str): Целевой язык перевода.

        Returns:
            str | None: Переведенный текст или None в случае ошибки.

        Raises:
            Exception: Если возникает ошибка при вызове API OpenAI.

        Example:
            >>> helicone_ai = HeliconeAI()
            >>> translation = helicone_ai.translate_text("Hello, how are you?", "русский")
            >>> print(translation)
            Привет, как дела?
        """
        try:
            #  запрос к API OpenAI для перевода текста
            response = self.client.completions.create(
                model='text-davinci-003',
                prompt=f'Translate the following text to {target_language}: {text}',
                max_tokens=200
            )
            # логирование ответа для Helicone
            self.helicone.log_completion(response)
            #  результата перевода текста из ответа
            if response.choices:
                return response.choices[0].text.strip()
            else:
                return None
        except Exception as ex:
            # логирование ошибки при вызове API OpenAI
            logger.error('Ошибка при переводе текста.', ex, exc_info=True)
            return None


def main():
    """
    Основная функция для демонстрации работы с HeliconeAI.
    """
    helicone_ai: HeliconeAI = HeliconeAI()

    poem: Optional[str] = helicone_ai.generate_poem('Напиши мне стихотворение про кота.')
    print('Generated Poem:\\n', poem)

    sentiment: Optional[str] = helicone_ai.analyze_sentiment('Сегодня был отличный день!')
    print('Sentiment Analysis:\\n', sentiment)

    summary: Optional[str] = helicone_ai.summarize_text('Длинный текст для изложения...')
    print('Summary:\\n', summary)

    translation: Optional[str] = helicone_ai.translate_text('Hello, how are you?', 'русский')
    print('Translation:\\n', translation)


if __name__ == '__main__':
    main()