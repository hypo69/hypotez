## Как использовать класс `HeliconeAI`
=========================================================================================

Описание
-------------------------
Класс `HeliconeAI` предоставляет набор функций для работы с моделью GPT-3.5-turbo и другими моделями OpenAI, используя библиотеку `helicone` для логирования запросов и ответов.

Шаги выполнения
-------------------------
1. **Инициализация класса:** Создай экземпляр класса `HeliconeAI`, который инициализирует объекты `Helicone` и `OpenAI`.
2. **Использование методов:** Вызывай методы класса для выполнения различных задач:
    - `generate_poem(prompt: str)`: Генерирует стихотворение на основе заданного промпта.
    - `analyze_sentiment(text: str)`: Анализирует тональность текста.
    - `summarize_text(text: str)`: Создает краткое изложение текста.
    - `translate_text(text: str, target_language: str)`: Переводит текст на указанный язык.

Пример использования
-------------------------

```python
from src.ai.helicone.helicone import HeliconeAI

helicone_ai = HeliconeAI()

# Генерация стихотворения
poem = helicone_ai.generate_poem("Напиши мне стихотворение про кота.")
print("Generated Poem:\n", poem)

# Анализ тональности
sentiment = helicone_ai.analyze_sentiment("Сегодня был отличный день!")
print("Sentiment Analysis:\n", sentiment)

# Краткое изложение
summary = helicone_ai.summarize_text("Длинный текст для изложения...")
print("Summary:\n", summary)

# Перевод текста
translation = helicone_ai.translate_text("Hello, how are you?", "русский")
print("Translation:\n", translation)
```