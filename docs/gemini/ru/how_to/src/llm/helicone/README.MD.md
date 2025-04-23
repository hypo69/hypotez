## \file hypotez/src/llm/helicone/README.MD
# HeliconeAI: Интеграция с Helicone.ai и OpenAI

## Обзор

Класс `HeliconeAI` разработан для облегчения взаимодействия с моделями Helicone.ai и OpenAI. Этот класс предоставляет методы для создания стихов, анализа тональности, обобщения текста и перевода текста. Он также включает логирование завершений с использованием Helicone.ai.

## Ключевые особенности

1. **Генерация стихов**:
   - Генерирует стих на основе заданного запроса, используя модель `gpt-3.5-turbo`.

2. **Анализ тональности**:
   - Анализирует тональность заданного текста, используя модель `text-davinci-003`.

3. **Обобщение текста**:
   - Обобщает заданный текст, используя модель `text-davinci-003`.

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
    def __init__(self):
        self.helicone = Helicone()
        self.client = OpenAI()
```

### Методы

#### Генерация стиха

Сгенерируйте стих на основе заданного запроса:

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

Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот метод генерирует стих на основе заданного текстового запроса. Он использует модель `gpt-3.5-turbo` от OpenAI для создания стиха и логирует завершение с помощью Helicone.

Шаги выполнения
-------------------------
1. Метод принимает текстовый запрос `prompt` в качестве входного параметра.
2. Вызывается метод `create` класса `client` (экземпляр `OpenAI`) для генерации стиха на основе запроса. Модель `gpt-3.5-turbo` используется для создания ответа.
3. Функция `helicone.log_completion` выполняет логирование сгенерированного ответа.
4. Извлекается текстовое содержимое сгенерированного стиха из ответа и возвращается.

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

def main():
    helicone_ai = HeliconeAI()
    poem = helicone_ai.generate_poem("Напиши мне стихотворение про кота.")
    print("Generated Poem:\\n", poem)

if __name__ == "__main__":
    main()
```

#### Анализ тональности

Анализирует тональность заданного текста:

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

Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот метод анализирует тональность заданного текста. Он использует модель `text-davinci-003` от OpenAI для анализа тональности текста и логирует завершение с помощью Helicone.

Шаги выполнения
-------------------------
1. Метод принимает текст `text` в качестве входного параметра.
2. Вызывается метод `create` класса `client` (экземпляр `OpenAI`) для анализа тональности текста. Модель `text-davinci-003` используется для анализа.
3. Функция `helicone.log_completion` выполняет логирование сгенерированного ответа.
4. Извлекается результат анализа тональности из ответа и возвращается.

Пример использования
-------------------------

```python
from helicone import Helicone
from openai import OpenAI

class HeliconeAI:
    def __init__(self):
        self.helicone = Helicone()
        self.client = OpenAI()

    def analyze_sentiment(self, text: str) -> str:
        response = self.client.completions.create(
            model="text-davinci-003",
            prompt=f"Analyze the sentiment of the following text: {text}",
            max_tokens=50
        )
        self.helicone.log_completion(response)
        return response.choices[0].text.strip()

def main():
    helicone_ai = HeliconeAI()
    sentiment = helicone_ai.analyze_sentiment("Сегодня был отличный день!")
    print("Sentiment Analysis:\\n", sentiment)

if __name__ == "__main__":
    main()
```

#### Обобщение текста

Обобщает заданный текст:

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

Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот метод обобщает заданный текст. Он использует модель `text-davinci-003` от OpenAI для создания краткого изложения текста и логирует завершение с помощью Helicone.

Шаги выполнения
-------------------------
1. Метод принимает текст `text` в качестве входного параметра.
2. Вызывается метод `create` класса `client` (экземпляр `OpenAI`) для обобщения текста. Модель `text-davinci-003` используется для обобщения.
3. Функция `helicone.log_completion` выполняет логирование сгенерированного ответа.
4. Извлекается краткое изложение текста из ответа и возвращается.

Пример использования
-------------------------

```python
from helicone import Helicone
from openai import OpenAI

class HeliconeAI:
    def __init__(self):
        self.helicone = Helicone()
        self.client = OpenAI()

    def summarize_text(self, text: str) -> str:
        response = self.client.completions.create(
            model="text-davinci-003",
            prompt=f"Summarize the following text: {text}",
            max_tokens=100
        )
        self.helicone.log_completion(response)
        return response.choices[0].text.strip()

def main():
    helicone_ai = HeliconeAI()
    summary = helicone_ai.summarize_text("Длинный текст для изложения...")
    print("Summary:\\n", summary)

if __name__ == "__main__":
    main()
```

#### Перевод текста

Переводит заданный текст на указанный целевой язык:

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

Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот метод переводит заданный текст на указанный целевой язык. Он использует модель `text-davinci-003` от OpenAI для перевода текста и логирует завершение с помощью Helicone.

Шаги выполнения
-------------------------
1. Метод принимает текст `text` и целевой язык `target_language` в качестве входных параметров.
2. Вызывается метод `create` класса `client` (экземпляр `OpenAI`) для перевода текста. Модель `text-davinci-003` используется для перевода.
3. Функция `helicone.log_completion` выполняет логирование сгенерированного ответа.
4. Извлекается переведенный текст из ответа и возвращается.

Пример использования
-------------------------

```python
from helicone import Helicone
from openai import OpenAI

class HeliconeAI:
    def __init__(self):
        self.helicone = Helicone()
        self.client = OpenAI()

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
    translation = helicone_ai.translate_text("Hello, how are you?", "русский")
    print("Translation:\\n", translation)

if __name__ == "__main__":
    main()
```

### Пример использования

Вот пример того, как использовать класс `HeliconeAI`:

```python
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
```

## Зависимости

- `helicone`
- `openai`

## Лицензия

Этот проект лицензирован в соответствии с лицензией MIT. Подробности см. в файле [LICENSE](LICENSE).

---

Для получения более подробной информации обратитесь к исходному коду и комментариям в классе `HeliconeAI`.