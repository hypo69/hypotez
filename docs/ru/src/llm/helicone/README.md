# HeliconeAI: Интеграция с Helicone.ai и OpenAI

## Обзор

Класс `HeliconeAI` предназначен для облегчения взаимодействия с моделями Helicone.ai и OpenAI. Этот класс предоставляет методы для создания стихов, анализа тональности, суммирования текста и перевода текста. Он также включает логирование завершений с использованием Helicone.ai.

## Ключевые особенности

1. **Генерация стихов**:
   - Создает стихотворение на основе заданного запроса, используя модель `gpt-3.5-turbo`.

2. **Анализ тональности**:
   - Анализирует тональность заданного текста, используя модель `text-davinci-003`.

3. **Суммирование текста**:
   - Суммирует заданный текст, используя модель `text-davinci-003`.

4. **Перевод текста**:
   - Переводит заданный текст на указанный целевой язык, используя модель `text-davinci-003`.

5. **Логирование завершений**:
   - Логирует все завершения с использованием Helicone.ai для мониторинга и анализа.

## Установка

Чтобы использовать класс `HeliconeAI`, убедитесь, что у вас установлены необходимые зависимости. Вы можете установить их, используя pip:

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
    """Класс для интеграции с Helicone.ai и OpenAI.

    Attributes:
        helicone (Helicone): Инстанс класса Helicone для логирования завершений.
        client (OpenAI): Инстанс класса OpenAI для взаимодействия с моделями OpenAI.

    Methods:
        generate_poem(prompt: str) -> str: Создает стихотворение на основе заданного запроса.
        analyze_sentiment(text: str) -> str: Анализирует тональность заданного текста.
        summarize_text(text: str) -> str: Суммирует заданный текст.
        translate_text(text: str, target_language: str) -> str: Переводит заданный текст на указанный целевой язык.
    """
    def __init__(self):
        """Инициализирует класс HeliconeAI.
        
        Создает инстансы классов Helicone и OpenAI для дальнейшего использования.
        """
        self.helicone = Helicone()
        self.client = OpenAI()
```

### Методы

#### Generate Poem

Создает стихотворение на основе заданного запроса:

```python
def generate_poem(self, prompt: str) -> str:
    """Создает стихотворение на основе заданного запроса.

    Args:
        prompt (str): Запрос для генерации стихотворения.

    Returns:
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
```

#### Analyze Sentiment

Анализирует тональность заданного текста:

```python
def analyze_sentiment(self, text: str) -> str:
    """Анализирует тональность заданного текста.

    Args:
        text (str): Текст для анализа тональности.

    Returns:
        str: Результат анализа тональности.
    """
    response = self.client.completions.create(
        model="text-davinci-003",
        prompt=f"Analyze the sentiment of the following text: {text}",
        max_tokens=50
    )
    self.helicone.log_completion(response)
    return response.choices[0].text.strip()
```

#### Summarize Text

Суммирует заданный текст:

```python
def summarize_text(self, text: str) -> str:
    """Суммирует заданный текст.

    Args:
        text (str): Текст для суммирования.

    Returns:
        str: Суммированный текст.
    """
    response = self.client.completions.create(
        model="text-davinci-003",
        prompt=f"Summarize the following text: {text}",
        max_tokens=100
    )
    self.helicone.log_completion(response)
    return response.choices[0].text.strip()
```

#### Translate Text

Переводит заданный текст на указанный целевой язык:

```python
def translate_text(self, text: str, target_language: str) -> str:
    """Переводит заданный текст на указанный целевой язык.

    Args:
        text (str): Текст для перевода.
        target_language (str): Целевой язык для перевода.

    Returns:
        str: Переведенный текст.
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

Ниже приведен пример использования класса `HeliconeAI`:

```python
def main():
    """Основная функция для демонстрации работы класса HeliconeAI."""
    helicone_ai = HeliconeAI()

    poem = helicone_ai.generate_poem("Напиши мне стихотворение про кота.")
    print("Generated Poem:\\n", poem)

    sentiment = helicone_ai.analyze_sentiment("Сегодня был отличный день!")
    print("Sentiment Analysis:\\n", sentiment)

    summary = helicone_ai.summarize_text("Длинный текст для изложения...")
    print("Summary:\\n", summary)

    translation = helicone_ai.translate_text("Hello, how are you?", "русский")
    print("Translation:\\n", translation)

if __name__ == "__main__":
    main()
```

## Зависимости

- `helicone`
- `openai`

## Лицензия

Этот проект лицензирован в соответствии с лицензией MIT. Подробности см. в файле [LICENSE](LICENSE).

---

Для получения более подробной информации обратитесь к исходному коду и комментариям в классе `HeliconeAI`.