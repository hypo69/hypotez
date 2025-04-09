# Модуль для работы с клиентом Claude

## Обзор

Модуль предоставляет класс `ClaudeClient`, который позволяет взаимодействовать с сервисами Claude для генерации текста, анализа тональности и перевода текста.
Модуль использует библиотеку `anthropic` для связи с API Claude.

## Подробней

Модуль предназначен для упрощения работы с Claude API, предоставляя удобный интерфейс для выполнения различных задач обработки текста.
Он включает в себя функции для генерации текста на основе запроса, анализа тональности текста и перевода текста с одного языка на другой.

## Классы

### `ClaudeClient`

**Описание**: Класс для взаимодействия с API Claude.

**Принцип работы**:
Класс `ClaudeClient` инициализируется с API-ключом, который используется для аутентификации при взаимодействии с сервисами Claude. Он предоставляет методы для генерации текста, анализа тональности и перевода текста. Каждый метод отправляет запрос к API Claude и возвращает результат.

**Аттрибуты**:
- `client`: Объект клиента `anthropic.Client`, используемый для взаимодействия с API Claude.

**Методы**:
- `__init__(api_key: str) -> None`: Инициализирует клиент Claude с предоставленным API-ключом.
- `generate_text(prompt: str, max_tokens_to_sample: int = 100) -> str`: Генерирует текст на основе предоставленного запроса.
- `analyze_sentiment(text: str) -> str`: Анализирует тональность предоставленного текста.
- `translate_text(text: str, source_language: str, target_language: str) -> str`: Переводит предоставленный текст с исходного языка на целевой язык.

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
```

**Назначение**:
Инициализирует экземпляр класса `ClaudeClient`.

**Параметры**:
- `api_key` (str): API-ключ для доступа к сервисам Claude.

**Как работает функция**:

1. Присваивает переданный `api_key` атрибуту `self.api_key`.
2. Создает экземпляр класса `anthropic.Client` с использованием `api_key` и присваивает его атрибуту `self.client`.

```ascii
  api_key --> Создание клиента anthropic.Client --> self.client
```
**Примеры**:
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
```

**Назначение**:
Генерирует текст на основе предоставленного запроса с использованием API Claude.

**Параметры**:
- `prompt` (str): Запрос для генерации текста.
- `max_tokens_to_sample` (int, optional): Максимальное количество токенов для генерации. По умолчанию 100.

**Возвращает**:
- `str`: Сгенерированный текст.

**Как работает функция**:

1.  Вызывает метод `completion` объекта `self.client` (экземпляр `anthropic.Client`) с параметрами:
    *   `prompt`: Предоставленный запрос для генерации текста.
    *   `model`: Модель для генерации текста (в данном случае `'claude-v1'`).
    *   `max_tokens_to_sample`: Максимальное количество токенов для генерации.
    *   `stop_sequences`: Список последовательностей, при обнаружении которых генерация текста прекращается (в данном случае `['\n\nHuman:']`).
2.  Извлекает сгенерированный текст из ответа, полученного от API, по ключу `'completion'`.
3.  Возвращает сгенерированный текст.

```ascii
prompt, max_tokens_to_sample --> Вызов anthropic.Client.completion() --> response
response --> Извлечение текста из response['completion'] --> generated_text
```

**Примеры**:
```python
claude_client.generate_text('Write a short story.')
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
```

**Назначение**:
Анализирует тональность предоставленного текста с использованием API Claude.

**Параметры**:
- `text` (str): Текст для анализа.

**Возвращает**:
- `str`: Результат анализа тональности.

**Как работает функция**:

1.  Формирует запрос для анализа тональности, включая предоставленный текст.
2.  Вызывает метод `completion` объекта `self.client` (экземпляр `anthropic.Client`) с параметрами:
    *   `prompt`: Запрос для анализа тональности.
    *   `model`: Модель для анализа тональности (в данном случае `'claude-v1'`).
    *   `max_tokens_to_sample`: Максимальное количество токенов для генерации.
    *   `stop_sequences`: Список последовательностей, при обнаружении которых анализ текста прекращается (в данном случае `['\n\nHuman:']`).
3.  Извлекает результат анализа тональности из ответа, полученного от API, по ключу `'completion'`.
4.  Возвращает результат анализа тональности.

```ascii
text --> Формирование запроса --> prompt
prompt --> Вызов anthropic.Client.completion() --> response
response --> Извлечение результата из response['completion'] --> sentiment_analysis
```

**Примеры**:
```python
claude_client.analyze_sentiment('I am very happy!')
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
```

**Назначение**:
Переводит предоставленный текст с исходного языка на целевой язык с использованием API Claude.

**Параметры**:
- `text` (str): Текст для перевода.
- `source_language` (str): Код исходного языка.
- `target_language` (str): Код целевого языка.

**Возвращает**:
- `str`: Переведенный текст.

**Как работает функция**:

1.  Формирует запрос для перевода текста, включая предоставленный текст, исходный язык и целевой язык.
2.  Вызывает метод `completion` объекта `self.client` (экземпляр `anthropic.Client`) с параметрами:
    *   `prompt`: Запрос для перевода текста.
    *   `model`: Модель для перевода текста (в данном случае `'claude-v1'`).
    *   `max_tokens_to_sample`: Максимальное количество токенов для генерации.
    *   `stop_sequences`: Список последовательностей, при обнаружении которых перевод текста прекращается (в данном случае `['\n\nHuman:']`).
3.  Извлекает переведенный текст из ответа, полученного от API, по ключу `'completion'`.
4.  Возвращает переведенный текст.

```ascii
text, source_language, target_language --> Формирование запроса --> prompt
prompt --> Вызов anthropic.Client.completion() --> response
response --> Извлечение текста из response['completion'] --> translated_text
```

**Примеры**:
```python
claude_client.translate_text('Hello', 'en', 'es')
```

## Функции

В данном модуле нет отдельных функций, только методы класса `ClaudeClient`.