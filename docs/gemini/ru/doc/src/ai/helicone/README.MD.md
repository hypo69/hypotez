# Документация модуля `src.ai.helicone`

## Обзор

Модуль `src.ai.helicone` предназначен для интеграции с Helicone.ai и OpenAI. Он предоставляет класс `HeliconeAI`, который облегчает взаимодействие с моделями OpenAI, такими как `gpt-3.5-turbo` и `text-davinci-003`, для выполнения различных задач, таких как генерация стихов, анализ тональности текста, суммирование текста и перевод текста. Также обеспечивает журналирование выполненных задач с использованием Helicone.ai.

## Подробнее

Этот модуль упрощает использование API OpenAI и Helicone.ai, предоставляя удобные методы для выполнения распространенных задач обработки текста и ведения журнала операций. Это позволяет разработчикам легко интегрировать функции ИИ в свои приложения, обеспечивая при этом мониторинг и анализ использования API.

## Классы

### `HeliconeAI`

**Описание**: Класс `HeliconeAI` предназначен для взаимодействия с Helicone.ai и OpenAI. Он предоставляет методы для генерации стихов, анализа тональности, суммирования и перевода текста, а также журналирования выполненных задач с использованием Helicone.ai.
**Наследует**: Не наследует никаких классов.
**Атрибуты**:
- `helicone` (Helicone): Экземпляр класса `Helicone` для логирования завершений.
- `client` (OpenAI): Экземпляр класса `OpenAI` для выполнения запросов к API OpenAI.

**Принцип работы**:
Класс инициализируется с экземплярами `Helicone` и `OpenAI`. Он предоставляет методы для выполнения различных задач обработки текста, используя модели OpenAI. После выполнения каждой задачи результат логируется с использованием `Helicone`. Это позволяет отслеживать использование API и анализировать производительность.

**Методы**:
- `__init__`: Инициализирует класс `HeliconeAI`, создавая экземпляры `Helicone` и `OpenAI`.
- `generate_poem`: Генерирует стихотворение на основе заданного запроса.
- `analyze_sentiment`: Анализирует тональность заданного текста.
- `summarize_text`: Суммирует заданный текст.
- `translate_text`: Переводит заданный текст на указанный язык.

## Методы класса

### `__init__(self)`

**Назначение**: Инициализирует экземпляр класса `HeliconeAI` и создает экземпляры `Helicone` и `OpenAI`.

```python
def __init__(self):
    self.helicone = Helicone()
    self.client = OpenAI()
```

### `generate_poem(self, prompt: str) -> str`

**Назначение**: Генерирует стихотворение на основе заданного запроса, используя модель `gpt-3.5-turbo`.

**Параметры**:
- `prompt` (str): Запрос для генерации стихотворения.

**Возвращает**:
- `str`: Сгенерированное стихотворение.

**Как работает функция**:
Функция принимает запрос `prompt` и использует `self.client.chat.completions.create` для генерации стихотворения с использованием модели `gpt-3.5-turbo`.  Затем функция логирует завершение, вызывая `self.helicone.log_completion(response)`, и возвращает сгенерированное стихотворение.

**Примеры**:

```python
helicone_ai = HeliconeAI()
poem = helicone_ai.generate_poem("Напиши мне стихотворение про кота.")
print(poem)
```

### `analyze_sentiment(self, text: str) -> str`

**Назначение**: Анализирует тональность заданного текста, используя модель `text-davinci-003`.

**Параметры**:
- `text` (str): Текст для анализа тональности.

**Возвращает**:
- `str`: Результат анализа тональности.

**Как работает функция**:
Функция принимает текст `text` и использует `self.client.completions.create` для анализа тональности текста с использованием модели `text-davinci-003`. Затем функция логирует завершение, вызывая `self.helicone.log_completion(response)`, и возвращает результат анализа тональности.

**Примеры**:

```python
helicone_ai = HeliconeAI()
sentiment = helicone_ai.analyze_sentiment("Сегодня был отличный день!")
print(sentiment)
```

### `summarize_text(self, text: str) -> str`

**Назначение**: Суммирует заданный текст, используя модель `text-davinci-003`.

**Параметры**:
- `text` (str): Текст для суммирования.

**Возвращает**:
- `str`: Суммированный текст.

**Как работает функция**:
Функция принимает текст `text` и использует `self.client.completions.create` для суммирования текста с использованием модели `text-davinci-003`. Затем функция логирует завершение, вызывая `self.helicone.log_completion(response)`, и возвращает суммированный текст.

**Примеры**:

```python
helicone_ai = HeliconeAI()
summary = helicone_ai.summarize_text("Длинный текст для изложения...")
print(summary)
```

### `translate_text(self, text: str, target_language: str) -> str`

**Назначение**: Переводит заданный текст на указанный язык, используя модель `text-davinci-003`.

**Параметры**:
- `text` (str): Текст для перевода.
- `target_language` (str): Язык, на который нужно перевести текст.

**Возвращает**:
- `str`: Переведенный текст.

**Как работает функция**:
Функция принимает текст `text` и целевой язык `target_language` и использует `self.client.completions.create` для перевода текста с использованием модели `text-davinci-003`. Затем функция логирует завершение, вызывая `self.helicone.log_completion(response)`, и возвращает переведенный текст.

**Примеры**:

```python
helicone_ai = HeliconeAI()
translation = helicone_ai.translate_text("Hello, how are you?", "русский")
print(translation)
```

## Параметры класса

- `helicone` (Helicone): Экземпляр класса `Helicone`, используемый для логирования выполненных задач.
- `client` (OpenAI): Экземпляр класса `OpenAI`, используемый для выполнения запросов к API OpenAI.

## Примеры

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
    print("Generated Poem:\\n", poem)

    sentiment = helicone_ai.analyze_sentiment("Сегодня был отличный день!")
    print("Sentiment Analysis:\\n", sentiment)

    summary = helicone_ai.summarize_text("Длинный текст для изложения...")
    print("Summary:\\n", summary)

    translation = helicone_ai.translate_text("Hello, how are you?", "русский")
    print("Translation:\\n", translation)

if __name__ == "__main__":
    main()