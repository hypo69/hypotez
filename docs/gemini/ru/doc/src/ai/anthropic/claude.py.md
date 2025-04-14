# Модуль для работы с клиентом Claude
=================================================

Модуль содержит класс :class:`ClaudeClient`, который используется для взаимодействия с сервисом Claude для генерации текста, анализа тональности и перевода текста.

[Документация](https://github.com/hypo69/hypotez/blob/master/docs/ru/src/ai/anthropic/claude.py.md)

## Оглавление

- [Обзор](#обзор)
- [Подробнее](#подробнее)
- [Классы](#классы)
    - [ClaudeClient](#claudeclient)
- [Примеры использования](#примеры-использования)

## Обзор

Модуль предоставляет класс `ClaudeClient`, который позволяет взаимодействовать с API Claude для выполнения задач, связанных с обработкой текста, таких как генерация текста на основе запроса, анализ тональности текста и перевод текста с одного языка на другой. Модуль использует библиотеку `anthropic` для взаимодействия с API Claude.

## Подробнее

Модуль предназначен для упрощения работы с сервисом Claude. Он предоставляет удобный интерфейс для выполнения основных операций, таких как генерация текста, анализ тональности и перевод текста. Класс `ClaudeClient` инициализируется с использованием API-ключа, который необходим для аутентификации при взаимодействии с сервисом Claude.

## Классы

### `ClaudeClient`

**Описание**: Класс для взаимодействия с сервисом Claude. Позволяет генерировать текст, анализировать тональность и переводить текст.

**Атрибуты**:
- `client` (anthropic.Client): Клиент для взаимодействия с API Claude.

**Методы**:
- `__init__(api_key: str) -> None`: Инициализирует клиент Claude с предоставленным API-ключом.
- `generate_text(prompt: str, max_tokens_to_sample: int = 100) -> str`: Генерирует текст на основе предоставленного запроса.
- `analyze_sentiment(text: str) -> str`: Анализирует тональность предоставленного текста.
- `translate_text(text: str, source_language: str, target_language: str) -> str`: Переводит предоставленный текст с исходного языка на целевой язык.

#### `__init__`

```python
def __init__(self, api_key: str) -> None
```

**Назначение**: Инициализирует клиент Claude с предоставленным API-ключом.

**Параметры**:
- `api_key` (str): API-ключ для доступа к сервисам Claude.

**Пример**:
```python
claude_client = ClaudeClient('your_api_key')
```

#### `generate_text`

```python
def generate_text(self, prompt: str, max_tokens_to_sample: int = 100) -> str
```

**Назначение**: Генерирует текст на основе предоставленного запроса.

**Параметры**:
- `prompt` (str): Запрос для генерации текста.
- `max_tokens_to_sample` (int, optional): Максимальное количество токенов для генерации. По умолчанию 100.

**Возвращает**:
- `str`: Сгенерированный текст.

**Пример**:
```python
claude_client.generate_text('Write a short story.')
# 'A short story about...'
```

**Как работает функция**:
- Функция отправляет запрос в Claude API для генерации текста на основе предоставленного запроса `prompt`.
- Параметр `max_tokens_to_sample` определяет максимальное количество токенов, которые будут сгенерированы.
- Параметр `stop_sequences` указывает последовательность символов, при обнаружении которой генерация текста должна остановиться.

#### `analyze_sentiment`

```python
def analyze_sentiment(self, text: str) -> str
```

**Назначение**: Анализирует тональность предоставленного текста.

**Параметры**:
- `text` (str): Текст для анализа.

**Возвращает**:
- `str`: Результат анализа тональности.

**Пример**:
```python
claude_client.analyze_sentiment('I am very happy!')
# 'Positive'
```

**Как работает функция**:
- Функция отправляет запрос в Claude API для анализа тональности предоставленного текста `text`.
- Формируется специальный запрос, включающий текст для анализа.
- Параметр `max_tokens_to_sample` ограничивает количество токенов в ответе.
- Параметр `stop_sequences` указывает последовательность символов, при обнаружении которой анализ должен остановиться.

#### `translate_text`

```python
def translate_text(self, text: str, source_language: str, target_language: str) -> str
```

**Назначение**: Переводит предоставленный текст с исходного языка на целевой язык.

**Параметры**:
- `text` (str): Текст для перевода.
- `source_language` (str): Код исходного языка.
- `target_language` (str): Код целевого языка.

**Возвращает**:
- `str`: Переведенный текст.

**Пример**:
```python
claude_client.translate_text('Hello', 'en', 'es')
# 'Hola'
```

**Как работает функция**:
- Функция отправляет запрос в Claude API для перевода текста `text` с исходного языка `source_language` на целевой язык `target_language`.
- Формируется запрос, включающий текст и коды языков.
- Параметр `max_tokens_to_sample` ограничивает количество токенов в ответе.
- Параметр `stop_sequences` указывает последовательность символов, при обнаружении которой перевод должен остановиться.

## Примеры использования

```python
if __name__ == '__main__':
    api_key = 'your-api-key'
    claude_client = ClaudeClient(api_key)

    # Пример генерации текста
    prompt = 'Write a short story about a robot learning to love.'
    generated_text = claude_client.generate_text(prompt)
    print('Generated Text:', generated_text)

    # Пример анализа тональности
    text_to_analyze = 'I am very happy today!'
    sentiment_analysis = claude_client.analyze_sentiment(text_to_analyze)
    print('Sentiment Analysis:', sentiment_analysis)

    # Пример перевода текста
    text_to_translate = 'Hello, how are you?'
    source_language = 'en'
    target_language = 'es'
    translated_text = claude_client.translate_text(text_to_translate, source_language, target_language)
    print('Translated Text:', translated_text)