### **Как использовать этот блок кода**

=========================================================================================

Описание
-------------------------
Этот блок кода определяет класс `HeliconeAI`, который предоставляет интерфейс для взаимодействия с API OpenAI через Helicone для выполнения различных задач, таких как генерация стихов, анализ тональности текста, создание кратких изложений и перевод текста на другие языки.

Шаги выполнения
-------------------------
1. **Инициализация класса `HeliconeAI`**:
   - Создается экземпляр класса `HeliconeAI`. В конструкторе инициализируются клиенты `Helicone` и `OpenAI`.

2. **Генерация стихотворения**:
   - Вызывается метод `generate_poem` с текстовым промптом.
   - Метод отправляет запрос в OpenAI для генерации стихотворения на основе предоставленного промпта.
   - Ответ OpenAI логируется с помощью `Helicone`.
   - Возвращается сгенерированное стихотворение.

3. **Анализ тональности**:
   - Вызывается метод `analyze_sentiment` с текстом для анализа.
   - Метод отправляет запрос в OpenAI для анализа тональности текста.
   - Ответ OpenAI логируется с помощью `Helicone`.
   - Возвращается результат анализа тональности.

4. **Создание краткого изложения**:
   - Вызывается метод `summarize_text` с текстом для изложения.
   - Метод отправляет запрос в OpenAI для создания краткого изложения текста.
   - Ответ OpenAI логируется с помощью `Helicone`.
   - Возвращается краткое изложение текста.

5. **Перевод текста**:
   - Вызывается метод `translate_text` с текстом для перевода и целевым языком.
   - Метод отправляет запрос в OpenAI для перевода текста на указанный язык.
   - Ответ OpenAI логируется с помощью `Helicone`.
   - Возвращается переведенный текст.

Пример использования
-------------------------

```python
## \file /src/ai/helicone/helicone.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.ai.helicone 
    :platform: Windows, Unix
    :synopsis:

"""


# https://docs.helicone.ai/guides/overview
import header 

from helicone import Helicone
from openai import OpenAI

class HeliconeAI:
    def __init__(self):
        self.helicone = Helicone()
        self.client = OpenAI()

    def generate_poem(self, prompt: str) -> str:
        """
        Генерирует стихотворение на основе заданного промпта.

        Аргументы:
            prompt (str): Промпт для генерации стихотворения.

        Возвращает:
            str: Сгенерированное стихотворение.
        """
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        self.helicone.log_completion(response)
        return response.choices[0].message.content

    def analyze_sentiment(self, text: str) -> str:
        """
        Анализирует тональность текста.

        Аргументы:
            text (str): Текст для анализа.

        Возвращает:
            str: Результат анализа тональности.
        """
        response = self.client.completions.create(
            model="text-davinci-003",
            prompt=f"Analyze the sentiment of the following text: {text}",
            max_tokens=50
        )
        self.helicone.log_completion(response)
        return response.choices[0].text.strip()

    def summarize_text(self, text: str) -> str:
        """
        Создает краткое изложение текста.

        Аргументы:
            text (str): Текст для изложения.

        Возвращает:
            str: Краткое изложение текста.
        """
        response = self.client.completions.create(
            model="text-davinci-003",
            prompt=f"Summarize the following text: {text}",
            max_tokens=100
        )
        self.helicone.log_completion(response)
        return response.choices[0].text.strip()

    def translate_text(self, text: str, target_language: str) -> str:
        """
        Переводит текст на указанный язык.

        Аргументы:
            text (str): Текст для перевода.
            target_language (str): Целевой язык перевода.

        Возвращает:
            str: Переведенный текст.
        """
        response = self.client.completions.create(
            model="text-davinci-003",
            prompt=f"Translate the following text to {target_language}: {text}",
            max_tokens=200
        )
        self.helicone.log_completion(response)
        return response.choices[0].text.strip()

def main():
    helicone_ai = HeliconeAI()

    poem = helicone_ai.generate_poem("Напиши мне стихотворение про кота.")
    print("Generated Poem:\n", poem)

    sentiment = helicone_ai.analyze_sentiment("Сегодня был отличный день!")
    print("Sentiment Analysis:\n", sentiment)

    summary = helicone_ai.summarize_text("Длинный текст для изложения...")
    print("Summary:\n", summary)

    translation = helicone_ai.translate_text("Hello, how are you?", "русский")
    print("Translation:\n", translation)

if __name__ == "__main__":
    main()