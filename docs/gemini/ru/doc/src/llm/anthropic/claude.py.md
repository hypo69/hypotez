# Модуль для работы с ассистентом Claude
=================================================

Модуль содержит класс :class:`ClaudeClient`, который используется для взаимодействия с языковой моделью Claude от Anthropic.
Предоставляет функции для генерации текста, анализа тональности и перевода.

## Обзор

Модуль `claude.py` обеспечивает доступ к модели Claude через API Anthropic.
Он предоставляет класс `ClaudeClient`, который позволяет взаимодействовать с моделью Claude для выполнения различных задач,
таких как генерация текста, анализ тональности, перевод текста и т.д. 

## Подробней

Модуль `claude.py` импортирует библиотеку `anthropic` для работы с API Anthropic.
Класс `ClaudeClient`  инициализирует клиент модели Claude с использованием предоставленного API-ключа.
Он предоставляет следующие методы:

- `generate_text(prompt: str, max_tokens_to_sample: int = 100) -> str`: Генерирует текст на основе заданного запроса.
- `analyze_sentiment(text: str) -> str`: Анализирует тональность текста.
- `translate_text(text: str, source_language: str, target_language: str) -> str`: Переводит текст с одного языка на другой.

## Классы

### `ClaudeClient`

**Описание**: Класс, реализующий интерфейс для взаимодействия с языковой моделью Claude.

**Наследует**: 
    `object`

**Атрибуты**:
    - `client (anthropic.Client)`: Клиент API Anthropic.

**Методы**:
    - `__init__(api_key: str) -> None`: Инициализирует клиент Claude с предоставленным API-ключом.
    - `generate_text(prompt: str, max_tokens_to_sample: int = 100) -> str`: Генерирует текст на основе предоставленного запроса.
    - `analyze_sentiment(text: str) -> str`: Анализирует тональность предоставленного текста.
    - `translate_text(text: str, source_language: str, target_language: str) -> str`: Переводит предоставленный текст с исходного языка на целевой язык.

## Методы класса

### `__init__`

```python
    def __init__(self, api_key: str) -> None:
        """
        Инициализирует клиент Claude с предоставленным API-ключом.

        Args:
            api_key (str): API-ключ для доступа к сервисам Claude.

        Example:
            >>> claude_client = ClaudeClient('your_api_key')
        """
        self.client = anthropic.Client(api_key)
```

**Назначение**: Инициализирует объект `ClaudeClient` с использованием предоставленного API-ключа.
Создает экземпляр клиента API Anthropic, который будет использоваться для всех последующих запросов.

**Параметры**:
    - `api_key (str)`: API-ключ для доступа к сервисам Claude.

**Возвращает**:
    - `None`:  Функция не возвращает значения.

**Пример**:

```python
    claude_client = ClaudeClient('your_api_key')
```

### `generate_text`

```python
    def generate_text(self, prompt: str, max_tokens_to_sample: int = 100) -> str:
        """
        Генерирует текст на основе предоставленного запроса.

        Args:
            prompt (str): Запрос для генерации текста.
            max_tokens_to_sample (int, optional): Максимальное количество токенов для генерации. По умолчанию 100.

        Returns:
            str: Сгенерированный текст.

        Example:
            >>> claude_client.generate_text('Write a short story.')
            'A short story about...'
        """
        response = self.client.completion(
            prompt=prompt,
            model='claude-v1',
            max_tokens_to_sample=max_tokens_to_sample,
            stop_sequences=['\n\nHuman:']
        )
        return response['completion']
```

**Назначение**: 
Функция генерирует текст на основе предоставленного запроса с использованием модели Claude.
Она использует метод `completion` API Anthropic, чтобы получить ответ от модели Claude.

**Параметры**:
    - `prompt (str)`: Запрос для генерации текста.
    - `max_tokens_to_sample (int, optional)`: Максимальное количество токенов для генерации. По умолчанию 100.

**Возвращает**:
    - `str`: Сгенерированный текст.

**Пример**:

```python
    generated_text = claude_client.generate_text('Write a short story.')
    print('Generated Text:', generated_text)
```

### `analyze_sentiment`

```python
    def analyze_sentiment(self, text: str) -> str:
        """
        Анализирует тональность предоставленного текста.

        Args:
            text (str): Текст для анализа.

        Returns:
            str: Результат анализа тональности.

        Example:
            >>> claude_client.analyze_sentiment('I am very happy!')
            'Positive'
        """
        response = self.client.completion(
            prompt=f'Analyze the sentiment of the following text: {text}',
            model='claude-v1',
            max_tokens_to_sample=50,
            stop_sequences=['\n\nHuman:']
        )
        return response['completion']
```

**Назначение**: 
Функция анализирует тональность текста с помощью модели Claude. 
Она отправляет запрос модели с текстом и получает ответ, содержащий анализ тональности.

**Параметры**:
    - `text (str)`: Текст для анализа.

**Возвращает**:
    - `str`: Результат анализа тональности.

**Пример**:

```python
    text_to_analyze = 'I am very happy today!'
    sentiment_analysis = claude_client.analyze_sentiment(text_to_analyze)
    print('Sentiment Analysis:', sentiment_analysis)
```

### `translate_text`

```python
    def translate_text(self, text: str, source_language: str, target_language: str) -> str:
        """
        Переводит предоставленный текст с исходного языка на целевой язык.

        Args:
            text (str): Текст для перевода.
            source_language (str): Код исходного языка.
            target_language (str): Код целевого языка.

        Returns:
            str: Переведенный текст.

        Example:
            >>> claude_client.translate_text('Hello', 'en', 'es')
            'Hola'
        """
        response = self.client.completion(
            prompt=f'Translate the following text from {source_language} to {target_language}: {text}',
            model='claude-v1',
            max_tokens_to_sample=100,
            stop_sequences=['\n\nHuman:']
        )
        return response['completion']
```

**Назначение**:
Функция переводит текст с одного языка на другой с помощью модели Claude.
Она отправляет запрос модели с текстом и кодами исходного и целевого языков.

**Параметры**:
    - `text (str)`: Текст для перевода.
    - `source_language (str)`: Код исходного языка.
    - `target_language (str)`: Код целевого языка.

**Возвращает**:
    - `str`: Переведенный текст.

**Пример**:

```python
    text_to_translate = 'Hello, how are you?'
    source_language = 'en'
    target_language = 'es'
    translated_text = claude_client.translate_text(text_to_translate, source_language, target_language)
    print('Translated Text:', translated_text)
```

## Примеры использования

### Генерация текста

```python
    # Пример генерации текста
    prompt = 'Write a short story about a robot learning to love.'
    generated_text = claude_client.generate_text(prompt)
    print('Generated Text:', generated_text)
```

### Анализ тональности

```python
    # Пример анализа тональности
    text_to_analyze = 'I am very happy today!'
    sentiment_analysis = claude_client.analyze_sentiment(text_to_analyze)
    print('Sentiment Analysis:', sentiment_analysis)
```

### Перевод текста

```python
    # Пример перевода текста
    text_to_translate = 'Hello, how are you?'
    source_language = 'en'
    target_language = 'es'
    translated_text = claude_client.translate_text(text_to_translate, source_language, target_language)
    print('Translated Text:', translated_text)