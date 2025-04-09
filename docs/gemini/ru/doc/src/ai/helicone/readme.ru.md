# Модуль `src.ai.helicone`

## Обзор

Данный модуль предоставляет класс `HeliconeAI`, который упрощает взаимодействие с сервисами Helicone.ai и OpenAI. Он предоставляет методы для генерации стихов, анализа тональности текста, создания кратких изложений и перевода текстов, а также логирования завершений с использованием Helicone.ai.

## Подробней

Этот модуль предназначен для интеграции с Helicone.ai и OpenAI, позволяя разработчикам использовать их API для выполнения различных задач обработки текста. Класс `HeliconeAI` объединяет функциональность этих сервисов, предоставляя удобный интерфейс для работы с ними.

## Классы

### `HeliconeAI`

**Описание**: Класс `HeliconeAI` предназначен для упрощения взаимодействия с Helicone.ai и OpenAI.

**Принцип работы**:
Класс инициализирует клиентов для работы с Helicone и OpenAI. Он предоставляет методы для выполнения различных задач, таких как генерация стихов, анализ тональности, создание кратких изложений и перевод текста. Каждый метод использует соответствующие API OpenAI и логирует завершения с использованием Helicone.

**Атрибуты**:

- `helicone`: Инстанс класса `Helicone` для логирования завершений.
- `client`: Инстанс класса `OpenAI` для взаимодействия с API OpenAI.

**Методы**:

- `__init__(self)`: Инициализирует класс `HeliconeAI` и создает экземпляры `Helicone` и `OpenAI`.
- `generate_poem(self, prompt: str) -> str`: Генерирует стихотворение на основе заданного промпта.
- `analyze_sentiment(self, text: str) -> str`: Анализирует тональность заданного текста.
- `summarize_text(self, text: str) -> str`: Создает краткое изложение заданного текста.
- `translate_text(self, text: str, target_language: str) -> str`: Переводит заданный текст на указанный целевой язык.

---

### `__init__`

```python
def __init__(self):
    self.helicone = Helicone()
    self.client = OpenAI()
```

**Назначение**: Инициализация экземпляра класса `HeliconeAI`.

**Как работает функция**:

1.  **Создание экземпляра Helicone**: Создает экземпляр класса `Helicone`, который будет использоваться для логирования завершений запросов к OpenAI.
2.  **Создание экземпляра OpenAI**: Создает экземпляр класса `OpenAI`, который будет использоваться для взаимодействия с API OpenAI.

```
Создание экземпляра Helicone --> Создание экземпляра OpenAI
```

**Примеры**:

```python
helicone_ai = HeliconeAI()
```

---

### `generate_poem`

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

**Назначение**: Генерирует стихотворение на основе заданного промпта с использованием модели `gpt-3.5-turbo`.

**Параметры**:

- `prompt` (str): Промпт для генерации стихотворения.

**Возвращает**:

- `str`: Сгенерированное стихотворение.

**Как работает функция**:

1.  **Запрос к OpenAI**: Отправляет запрос к API OpenAI для генерации стихотворения на основе заданного промпта. Используется модель `gpt-3.5-turbo`.
2.  **Логирование завершения**: Логирует завершение запроса с использованием `Helicone`.
3.  **Извлечение результата**: Извлекает сгенерированное стихотворение из ответа OpenAI и возвращает его.

```
Запрос к OpenAI --> Логирование завершения --> Извлечение стихотворения
```

**Примеры**:

```python
poem = helicone_ai.generate_poem("Напиши мне стихотворение про кота.")
print("Generated Poem:\n", poem)
```

---

### `analyze_sentiment`

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

**Назначение**: Анализирует тональность заданного текста с использованием модели `text-davinci-003`.

**Параметры**:

- `text` (str): Текст для анализа тональности.

**Возвращает**:

- `str`: Результат анализа тональности.

**Как работает функция**:

1.  **Запрос к OpenAI**: Отправляет запрос к API OpenAI для анализа тональности заданного текста. Используется модель `text-davinci-003`.
2.  **Логирование завершения**: Логирует завершение запроса с использованием `Helicone`.
3.  **Извлечение результата**: Извлекает результат анализа тональности из ответа OpenAI и возвращает его.

```
Запрос к OpenAI --> Логирование завершения --> Извлечение результата анализа
```

**Примеры**:

```python
sentiment = helicone_ai.analyze_sentiment("Сегодня был отличный день!")
print("Sentiment Analysis:\n", sentiment)
```

---

### `summarize_text`

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

**Назначение**: Создает краткое изложение заданного текста с использованием модели `text-davinci-003`.

**Параметры**:

- `text` (str): Текст для создания краткого изложения.

**Возвращает**:

- `str`: Краткое изложение текста.

**Как работает функция**:

1.  **Запрос к OpenAI**: Отправляет запрос к API OpenAI для создания краткого изложения заданного текста. Используется модель `text-davinci-003`.
2.  **Логирование завершения**: Логирует завершение запроса с использованием `Helicone`.
3.  **Извлечение результата**: Извлекает краткое изложение текста из ответа OpenAI и возвращает его.

```
Запрос к OpenAI --> Логирование завершения --> Извлечение краткого изложения
```

**Примеры**:

```python
summary = helicone_ai.summarize_text("Длинный текст для изложения...")
print("Summary:\n", summary)
```

---

### `translate_text`

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

**Назначение**: Переводит заданный текст на указанный целевой язык с использованием модели `text-davinci-003`.

**Параметры**:

- `text` (str): Текст для перевода.
- `target_language` (str): Целевой язык для перевода.

**Возвращает**:

- `str`: Переведенный текст.

**Как работает функция**:

1.  **Запрос к OpenAI**: Отправляет запрос к API OpenAI для перевода заданного текста на указанный целевой язык. Используется модель `text-davinci-003`.
2.  **Логирование завершения**: Логирует завершение запроса с использованием `Helicone`.
3.  **Извлечение результата**: Извлекает переведенный текст из ответа OpenAI и возвращает его.

```
Запрос к OpenAI --> Логирование завершения --> Извлечение переведенного текста
```

**Примеры**:

```python
translation = helicone_ai.translate_text("Hello, how are you?", "русский")
print("Translation:\n", translation)
```

---

## Функции

### `main`

```python
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

**Назначение**: Главная функция, демонстрирующая использование класса `HeliconeAI`.

**Как работает функция**:

1.  **Создание экземпляра `HeliconeAI`**: Создает экземпляр класса `HeliconeAI`.
2.  **Генерация стихотворения**: Вызывает метод `generate_poem` для генерации стихотворения.
3.  **Анализ тональности**: Вызывает метод `analyze_sentiment` для анализа тональности текста.
4.  **Создание краткого изложения**: Вызывает метод `summarize_text` для создания краткого изложения текста.
5.  **Перевод текста**: Вызывает метод `translate_text` для перевода текста на русский язык.
6.  **Вывод результатов**: Выводит результаты каждого вызова метода на консоль.

```
Создание экземпляра HeliconeAI --> Генерация стихотворения --> Анализ тональности --> Создание краткого изложения --> Перевод текста --> Вывод результатов
```

**Примеры**:

```python
main()
```

## Зависимости

- `helicone`
- `openai`

## Лицензия

Этот проект лицензирован под MIT License. Подробности смотрите в файле [LICENSE](LICENSE).