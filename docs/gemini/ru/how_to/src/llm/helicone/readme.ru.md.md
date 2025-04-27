## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода представляет класс `HeliconeAI`, который предоставляет набор функций для взаимодействия с API Helicone.ai и OpenAI. Он упрощает такие задачи, как генерация стихов, анализ тональности, создание краткого изложения и перевод текста.

Шаги выполнения
-------------------------
1. **Инициализация класса `HeliconeAI`:**
   - Создайте экземпляр класса `HeliconeAI` с использованием `helicone_ai = HeliconeAI()`.
   - Внутри класса создаются экземпляры классов `Helicone` и `OpenAI` для работы с соответствующими API.

2. **Использование методов:**
   - Класс `HeliconeAI` предоставляет следующие методы:
     - `generate_poem(prompt: str)`: генерирует стихотворение на основе заданного промпта с использованием модели `gpt-3.5-turbo`.
     - `analyze_sentiment(text: str)`: анализирует тональность текста с использованием модели `text-davinci-003`.
     - `summarize_text(text: str)`: создает краткое изложение текста с использованием модели `text-davinci-003`.
     - `translate_text(text: str, target_language: str)`: переводит текст на указанный язык с использованием модели `text-davinci-003`.

3. **Логирование завершений:**
   - Класс `HeliconeAI` использует `self.helicone.log_completion(response)` для логирования завершений, полученных от API Helicone.ai.

Пример использования
-------------------------

```python
from helicone import Helicone
from openai import OpenAI

class HeliconeAI:
    def __init__(self):
        self.helicone = Helicone()
        self.client = OpenAI()

    def generate_poem(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        self.helicone.log_completion(response)
        return response.choices[0].message.content

    def analyze_sentiment(self, text: str) -> str:
        response = self.client.completions.create(
            model="text-davinci-003",
            prompt=f"Analyze the sentiment of the following text: {text}",
            max_tokens=50
        )
        self.helicone.log_completion(response)
        return response.choices[0].text.strip()

    def summarize_text(self, text: str) -> str:
        response = self.client.completions.create(
            model="text-davinci-003",
            prompt=f"Summarize the following text: {text}",
            max_tokens=100
        )
        self.helicone.log_completion(response)
        return response.choices[0].text.strip()

    def translate_text(self, text: str, target_language: str) -> str:
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
```

## Зависимости
- `helicone`
- `openai`