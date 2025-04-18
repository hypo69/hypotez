# Модуль `helicone.py`

## Обзор

Модуль `helicone.py` предоставляет класс `HeliconeAI`, который интегрируется с Helicone и OpenAI для выполнения различных задач, таких как генерация стихов, анализ тональности текста, создание кратких изложений и перевод текста на другие языки.

## Подробней

Этот модуль позволяет использовать возможности Helicone для логирования и мониторинга запросов к OpenAI API. Класс `HeliconeAI` предоставляет удобный интерфейс для выполнения различных задач обработки текста с использованием моделей OpenAI.

## Классы

### `HeliconeAI`

**Описание**: Класс `HeliconeAI` предоставляет методы для взаимодействия с Helicone и OpenAI API для выполнения различных задач обработки текста.

**Атрибуты**:

- `helicone`: Инстанс класса `Helicone` для логирования запросов.
- `client`: Инстанс класса `OpenAI` для взаимодействия с OpenAI API.

**Методы**:

- `generate_poem(prompt: str) -> str`: Генерирует стихотворение на основе заданного промпта.
- `analyze_sentiment(text: str) -> str`: Анализирует тональность текста.
- `summarize_text(text: str) -> str`: Создает краткое изложение текста.
- `translate_text(text: str, target_language: str) -> str`: Переводит текст на указанный язык.

## Методы класса

### `generate_poem`

```python
def generate_poem(self, prompt: str) -> str:
    """
    Генерирует стихотворение на основе заданного промпта.

    Args:
        prompt (str): Промпт для генерации стихотворения.

    Returns:
        str: Сгенерированное стихотворение.
    """
    ...
```

**Назначение**: Генерирует стихотворение на основе заданного промпта, используя модель `gpt-3.5-turbo` от OpenAI.

**Параметры**:

- `prompt` (str): Текст запроса (промпт), на основе которого генерируется стихотворение.

**Возвращает**:

- `str`: Сгенерированное стихотворение.

**Как работает функция**:

1. Функция отправляет запрос к OpenAI API с использованием модели `gpt-3.5-turbo` и заданным промптом.
2. Получает ответ от OpenAI API, содержащий сгенерированное стихотворение.
3. Логирует запрос и ответ с помощью `self.helicone.log_completion(response)`.
4. Извлекает текст стихотворения из ответа и возвращает его.

**Примеры**:

```python
helicone_ai = HeliconeAI()
poem = helicone_ai.generate_poem("Напиши мне стихотворение про кота.")
print(poem)
```

### `analyze_sentiment`

```python
def analyze_sentiment(self, text: str) -> str:
    """
    Анализирует тональность текста.

    Args:
        text (str): Текст для анализа.

    Returns:
        str: Результат анализа тональности.
    """
    ...
```

**Назначение**: Анализирует тональность текста с использованием модели `text-davinci-003` от OpenAI.

**Параметры**:

- `text` (str): Текст, для которого необходимо определить тональность.

**Возвращает**:

- `str`: Результат анализа тональности.

**Как работает функция**:

1. Функция отправляет запрос к OpenAI API с использованием модели `text-davinci-003` и заданным текстом.
2. Запрос включает инструкцию для анализа тональности текста.
3. Получает ответ от OpenAI API, содержащий результат анализа тональности.
4. Логирует запрос и ответ с помощью `self.helicone.log_completion(response)`.
5. Извлекает результат анализа тональности из ответа, удаляет лишние пробелы и возвращает его.

**Примеры**:

```python
helicone_ai = HeliconeAI()
sentiment = helicone_ai.analyze_sentiment("Сегодня был отличный день!")
print(sentiment)
```

### `summarize_text`

```python
def summarize_text(self, text: str) -> str:
    """
    Создает краткое изложение текста.

    Args:
        text (str): Текст для изложения.

    Returns:
        str: Краткое изложение текста.
    """
    ...
```

**Назначение**: Создает краткое изложение текста с использованием модели `text-davinci-003` от OpenAI.

**Параметры**:

- `text` (str): Текст, который необходимо изложить кратко.

**Возвращает**:

- `str`: Краткое изложение текста.

**Как работает функция**:

1. Функция отправляет запрос к OpenAI API с использованием модели `text-davinci-003` и заданным текстом.
2. Запрос включает инструкцию для создания краткого изложения текста.
3. Получает ответ от OpenAI API, содержащий краткое изложение текста.
4. Логирует запрос и ответ с помощью `self.helicone.log_completion(response)`.
5. Извлекает краткое изложение текста из ответа, удаляет лишние пробелы и возвращает его.

**Примеры**:

```python
helicone_ai = HeliconeAI()
summary = helicone_ai.summarize_text("Длинный текст для изложения...")
print(summary)
```

### `translate_text`

```python
def translate_text(self, text: str, target_language: str) -> str:
    """
    Переводит текст на указанный язык.

    Args:
        text (str): Текст для перевода.
        target_language (str): Целевой язык перевода.

    Returns:
        str: Переведенный текст.
    """
    ...
```

**Назначение**: Переводит текст на указанный язык с использованием модели `text-davinci-003` от OpenAI.

**Параметры**:

- `text` (str): Текст, который необходимо перевести.
- `target_language` (str): Язык, на который необходимо перевести текст.

**Возвращает**:

- `str`: Переведенный текст.

**Как работает функция**:

1. Функция отправляет запрос к OpenAI API с использованием модели `text-davinci-003` и заданным текстом и целевым языком.
2. Запрос включает инструкцию для перевода текста на указанный язык.
3. Получает ответ от OpenAI API, содержащий переведенный текст.
4. Логирует запрос и ответ с помощью `self.helicone.log_completion(response)`.
5. Извлекает переведенный текст из ответа, удаляет лишние пробелы и возвращает его.

**Примеры**:

```python
helicone_ai = HeliconeAI()
translation = helicone_ai.translate_text("Hello, how are you?", "русский")
print(translation)
```

## Функция `main`

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

**Назначение**: Главная функция, которая создает экземпляр класса `HeliconeAI` и использует его для выполнения различных задач обработки текста.

**Как работает функция**:

1. Создает экземпляр класса `HeliconeAI`.
2. Вызывает метод `generate_poem` для генерации стихотворения.
3. Вызывает метод `analyze_sentiment` для анализа тональности текста.
4. Вызывает метод `summarize_text` для создания краткого изложения текста.
5. Вызывает метод `translate_text` для перевода текста на другой язык.
6. Выводит результаты выполнения каждой задачи в консоль.

## Параметры класса

- `helicone`: Инстанс класса `Helicone`, используемый для логирования запросов.
- `client`: Инстанс класса `OpenAI`, используемый для взаимодействия с OpenAI API.

## Примеры

Пример использования класса `HeliconeAI` для генерации стихотворения, анализа тональности текста, создания краткого изложения и перевода текста:

```python
helicone_ai = HeliconeAI()

poem = helicone_ai.generate_poem("Напиши мне стихотворение про кота.")
print("Generated Poem:\n", poem)

sentiment = helicone_ai.analyze_sentiment("Сегодня был отличный день!")
print("Sentiment Analysis:\n", sentiment)

summary = helicone_ai.summarize_text("Длинный текст для изложения...")
print("Summary:\n", summary)

translation = helicone_ai.translate_text("Hello, how are you?", "русский")
print("Translation:\n", translation)