### **Как использовать блок кода HeliconeAI**

Описание
-------------------------
Блок кода `HeliconeAI` предназначен для упрощения взаимодействия с Helicone.ai и моделями OpenAI. Он предоставляет методы для генерации стихов, анализа тональности текста, создания краткого изложения текста и перевода текста, а также включает логирование завершений с использованием Helicone.ai.

Шаги выполнения
-------------------------
1.  **Установка зависимостей**:
    - Убедитесь, что у вас установлены необходимые библиотеки `openai` и `helicone`.
    - Если они не установлены, выполните команду:
    ```bash
    pip install openai helicone
    ```

2.  **Инициализация класса `HeliconeAI`**:
    - Создайте экземпляр класса `HeliconeAI` для доступа к его методам.
    ```python
    from helicone import Helicone
    from openai import OpenAI

    class HeliconeAI:
        def __init__(self):
            self.helicone = Helicone()
            self.client = OpenAI()
    ```

3.  **Генерация стихотворения**:
    - Используйте метод `generate_poem` для создания стихотворения на основе заданного промпта.
    ```python
    def generate_poem(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        self.helicone.log_completion(response)
        return response.choices[0].message.content
    ```
    - Метод отправляет запрос в OpenAI с моделью `gpt-3.5-turbo` и возвращает сгенерированное стихотворение.

4.  **Анализ тональности текста**:
    - Используйте метод `analyze_sentiment` для анализа тональности заданного текста.
    ```python
    def analyze_sentiment(self, text: str) -> str:
        response = self.client.completions.create(
            model="text-davinci-003",
            prompt=f"Analyze the sentiment of the following text: {text}",
            max_tokens=50
        )
        self.helicone.log_completion(response)
        return response.choices[0].text.strip()
    ```
    - Метод отправляет запрос в OpenAI с моделью `text-davinci-003` и возвращает результат анализа тональности.

5.  **Создание краткого изложения текста**:
    - Используйте метод `summarize_text` для создания краткого изложения заданного текста.
    ```python
    def summarize_text(self, text: str) -> str:
        response = self.client.completions.create(
            model="text-davinci-003",
            prompt=f"Summarize the following text: {text}",
            max_tokens=100
        )
        self.helicone.log_completion(response)
        return response.choices[0].text.strip()
    ```
    - Метод отправляет запрос в OpenAI с моделью `text-davinci-003` и возвращает краткое изложение текста.

6.  **Перевод текста**:
    - Используйте метод `translate_text` для перевода заданного текста на указанный целевой язык.
    ```python
    def translate_text(self, text: str, target_language: str) -> str:
        response = self.client.completions.create(
            model="text-davinci-003",
            prompt=f"Translate the following text to {target_language}: {text}",
            max_tokens=200
        )
        self.helicone.log_completion(response)
        return response.choices[0].text.strip()
    ```
    - Метод отправляет запрос в OpenAI с моделью `text-davinci-003` и возвращает переведенный текст.

7.  **Логирование завершений**:
    - Все методы используют `self.helicone.log_completion(response)` для логирования запросов и ответов через Helicone.ai.

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