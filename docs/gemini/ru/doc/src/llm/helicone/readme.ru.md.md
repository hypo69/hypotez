# HeliconeAI: Интеграция с Helicone.ai и OpenAI

## Обзор

Модуль `src.ai.helicone` содержит класс `HeliconeAI`, который упрощает взаимодействие с Helicone.ai и моделями OpenAI. Он предоставляет методы для выполнения различных задач, таких как генерация стихов, анализ тональности, краткое изложение текста и перевод текста. Модуль также включает логирование завершений с использованием Helicone.ai.

## Содержание

- [Установка](#установка)
- [Использование](#использование)
  - [Инициализация](#инициализация)
  - [Методы](#методы)
    - [Генерация стихотворения](#генерация-стихотворения)
    - [Анализ тональности](#анализ-тональности)
    - [Краткое изложение текста](#краткое-изложение-текста)
    - [Перевод текста](#перевод-текста)
- [Пример использования](#пример-использования)
- [Зависимости](#зависимости)
- [Лицензия](#лицензия)

## Установка

Для использования класса `HeliconeAI` убедитесь, что у вас установлены необходимые зависимости. Вы можете установить их с помощью pip:

```bash
pip install openai helicone
```

## Использование

### Инициализация

Инициализируйте класс `HeliconeAI`:

```python
from helicone import Helicone
from openai import OpenAI

class HeliconeAI:
    """
    Класс для взаимодействия с Helicone.ai и OpenAI.

    Attributes:
        helicone (Helicone): Объект Helicone для логирования завершений.
        client (OpenAI): Объект OpenAI для взаимодействия с моделями.
    """
    def __init__(self):
        """
        Инициализирует объект HeliconeAI.
        """
        self.helicone = Helicone()
        self.client = OpenAI()
```

### Методы

#### Генерация стихотворения

Сгенерируйте стихотворение на основе заданного промпта:

```python
def generate_poem(self, prompt: str) -> str:
    """
    Генерирует стихотворение с использованием модели OpenAI GPT-3.5-turbo.

    Args:
        prompt (str): Текст промпта для генерации стихотворения.

    Returns:
        str: Сгенерированное стихотворение.

    Raises:
        Exception: Если возникает ошибка при использовании модели OpenAI.
    """
    response = self.client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    self.helicone.log_completion(response)
    return response.choices[0].message.content
```

#### Анализ тональности

Проанализируйте тональность заданного текста:

```python
def analyze_sentiment(self, text: str) -> str:
    """
    Анализирует тональность текста с использованием модели OpenAI text-davinci-003.

    Args:
        text (str): Текст для анализа тональности.

    Returns:
        str: Описание тональности текста.

    Raises:
        Exception: Если возникает ошибка при использовании модели OpenAI.
    """
    response = self.client.completions.create(
        model="text-davinci-003",
        prompt=f"Analyze the sentiment of the following text: {text}",
        max_tokens=50
    )
    self.helicone.log_completion(response)
    return response.choices[0].text.strip()
```

#### Краткое изложение текста

Создайте краткое изложение заданного текста:

```python
def summarize_text(self, text: str) -> str:
    """
    Создает краткое изложение текста с использованием модели OpenAI text-davinci-003.

    Args:
        text (str): Текст для краткого изложения.

    Returns:
        str: Краткое изложение текста.

    Raises:
        Exception: Если возникает ошибка при использовании модели OpenAI.
    """
    response = self.client.completions.create(
        model="text-davinci-003",
        prompt=f"Summarize the following text: {text}",
        max_tokens=100
    )
    self.helicone.log_completion(response)
    return response.choices[0].text.strip()
```

#### Перевод текста

Переведите заданный текст на указанный целевой язык:

```python
def translate_text(self, text: str, target_language: str) -> str:
    """
    Переводит текст на указанный язык с использованием модели OpenAI text-davinci-003.

    Args:
        text (str): Текст для перевода.
        target_language (str): Целевой язык перевода.

    Returns:
        str: Переведенный текст.

    Raises:
        Exception: Если возникает ошибка при использовании модели OpenAI.
    """
    response = self.client.completions.create(
        model="text-davinci-003",
        prompt=f"Translate the following text to {target_language}: {text}",
        max_tokens=200
    )
    self.helicone.log_completion(response)
    return response.choices[0].text.strip()
```

### Пример использования

Вот пример того, как использовать класс `HeliconeAI`:

```python
def main():
    """
    Пример использования класса HeliconeAI.
    """
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
```

## Зависимости

- `helicone`
- `openai`

## Лицензия

Этот проект лицензирован под MIT License. Подробности смотрите в файле [LICENSE](LICENSE).

---

Для получения более подробной информации обратитесь к исходному коду и комментариям внутри класса `HeliconeAI`.