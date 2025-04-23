# Модуль `helicone`

## Обзор

Модуль `helicone` предоставляет класс `HeliconeAI`, который интегрируется с Helicone и OpenAI для выполнения различных задач обработки текста, таких как генерация стихов, анализ тональности, создание кратких изложений и перевод текста. Модуль использует API OpenAI для выполнения этих задач и Helicone для логирования запросов.

## Подробнее

Модуль предназначен для упрощения использования возможностей OpenAI и Helicone в проекте `hypotez`. Он предоставляет удобный интерфейс для выполнения распространенных задач обработки текста и обеспечивает логирование запросов для отслеживания и анализа.

## Классы

### `HeliconeAI`

**Описание**: Класс `HeliconeAI` предоставляет методы для взаимодействия с моделями OpenAI через интеграцию с Helicone.

**Атрибуты**:
- `helicone` (Helicone): Объект Helicone для логирования запросов.
- `client` (OpenAI): Клиент OpenAI для выполнения запросов к API.

**Методы**:
- `generate_poem(prompt: str) -> str`: Генерирует стихотворение на основе заданного промпта.
- `analyze_sentiment(text: str) -> str`: Анализирует тональность текста.
- `summarize_text(text: str) -> str`: Создает краткое изложение текста.
- `translate_text(text: str, target_language: str) -> str`: Переводит текст на указанный язык.

### `__init__`

```python
def __init__(self):
    """
    Инициализирует экземпляры Helicone и OpenAI.

    Args:
        self (HeliconeAI): Экземпляр класса HeliconeAI.

    Returns:
        None
    """
    self.helicone = Helicone()
    self.client = OpenAI()
```

**Как работает функция**:
- Функция инициализирует класс `HeliconeAI` путем создания экземпляров `Helicone` и `OpenAI`.
- `self.helicone` инициализируется как экземпляр класса `Helicone`, который, вероятно, используется для логирования или мониторинга взаимодействия с API OpenAI.
- `self.client` инициализируется как экземпляр класса `OpenAI`, который будет использоваться для выполнения фактических запросов к API OpenAI.

**Примеры**:
```python
helicone_ai = HeliconeAI()
```

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
    response = self.client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    self.helicone.log_completion(response)
    return response.choices[0].message.content
```

**Назначение**:
Функция генерирует стихотворение на основе заданного текстового запроса (промпта) с использованием модели `gpt-3.5-turbo` от OpenAI.

**Параметры**:
- `prompt` (str): Текст запроса, на основе которого генерируется стихотворение.

**Возвращает**:
- `str`: Сгенерированное стихотворение.

**Как работает функция**:
- Функция вызывает API OpenAI для генерации текста на основе предоставленного промпта.
- Используется модель `gpt-3.5-turbo` для создания стихотворения.
- Результат логируется с использованием `self.helicone.log_completion(response)`.
- Возвращается сгенерированное стихотворение из ответа OpenAI.

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
    response = self.client.completions.create(
        model="text-davinci-003",
        prompt=f"Analyze the sentiment of the following text: {text}",
        max_tokens=50
    )
    self.helicone.log_completion(response)
    return response.choices[0].text.strip()
```

**Назначение**:
Функция анализирует тональность предоставленного текста с использованием модели `text-davinci-003` от OpenAI.

**Параметры**:
- `text` (str): Текст, для которого необходимо определить тональность.

**Возвращает**:
- `str`: Результат анализа тональности.

**Как работает функция**:
- Функция вызывает API OpenAI для анализа тональности текста.
- Используется модель `text-davinci-003`.
- Результат логируется с использованием `self.helicone.log_completion(response)`.
- Возвращается результат анализа тональности.

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
    response = self.client.completions.create(
        model="text-davinci-003",
        prompt=f"Summarize the following text: {text}",
        max_tokens=100
    )
    self.helicone.log_completion(response)
    return response.choices[0].text.strip()
```

**Назначение**:
Функция создает краткое изложение предоставленного текста с использованием модели `text-davinci-003` от OpenAI.

**Параметры**:
- `text` (str): Текст, который необходимо изложить кратко.

**Возвращает**:
- `str`: Краткое изложение текста.

**Как работает функция**:
- Функция вызывает API OpenAI для создания краткого изложения текста.
- Используется модель `text-davinci-003`.
- Результат логируется с использованием `self.helicone.log_completion(response)`.
- Возвращается краткое изложение текста.

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
    response = self.client.completions.create(
        model="text-davinci-003",
        prompt=f"Translate the following text to {target_language}: {text}",
        max_tokens=200
    )
    self.helicone.log_completion(response)
    return response.choices[0].text.strip()
```

**Назначение**:
Функция переводит предоставленный текст на указанный целевой язык с использованием модели `text-davinci-003` от OpenAI.

**Параметры**:
- `text` (str): Текст, который необходимо перевести.
- `target_language` (str): Целевой язык для перевода.

**Возвращает**:
- `str`: Переведенный текст.

**Как работает функция**:
- Функция вызывает API OpenAI для перевода текста на указанный язык.
- Используется модель `text-davinci-003`.
- Результат логируется с использованием `self.helicone.log_completion(response)`.
- Возвращается переведенный текст.

**Примеры**:
```python
helicone_ai = HeliconeAI()
translation = helicone_ai.translate_text("Hello, how are you?", "русский")
print(translation)
```

## Функции

### `main`

```python
def main():
    """
    Создает экземпляр HeliconeAI и выполняет несколько задач обработки текста.

    Args:
        None

    Returns:
        None
    """
    helicone_ai = HeliconeAI()

    poem = helicone_ai.generate_poem("Напиши мне стихотворение про кота.")
    print("Generated Poem:\\n", poem)

    sentiment = helicone_ai.analyze_sentiment("Сегодня был отличный день!")
    print("Sentiment Analysis:\\n", sentiment)

    summary = helicone_ai.summarize_text("Длинный текст для изложения...")
    print("Summary:\\n", summary)

    translation = helicone_ai.translate_text("Hello, how are you?", "русский")
    print("Translation:\\n", translation)
```

**Назначение**:
Функция `main` является точкой входа для демонстрации работы класса `HeliconeAI`. Она создает экземпляр `HeliconeAI` и выполняет несколько задач обработки текста, такие как генерация стихов, анализ тональности, создание кратких изложений и перевод текста.

**Как работает функция**:
- Создается экземпляр класса `HeliconeAI`.
- Вызывается метод `generate_poem` для генерации стихотворения на русском языке.
- Вызывается метод `analyze_sentiment` для анализа тональности текста на русском языке.
- Вызывается метод `summarize_text` для создания краткого изложения текста.
- Вызывается метод `translate_text` для перевода текста с английского на русский язык.
- Результаты каждой операции выводятся на экран.

**Примеры**:
```python
if __name__ == "__main__":
    main()