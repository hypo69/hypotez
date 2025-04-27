# Модуль Claude Client

## Обзор

Модуль `claude.py` реализует класс `ClaudeClient` для взаимодействия с моделью Claude от Anthropic. 

## Подробности

Модуль `claude.py` предоставляет функциональность для взаимодействия с моделью Claude от Anthropic через API. Класс `ClaudeClient` позволяет выполнять различные задачи, такие как:

* Генерация текста
* Анализ тональности
* Перевод текста

## Классы

### `ClaudeClient`

**Описание**: Класс `ClaudeClient` используется для взаимодействия с моделью Claude от Anthropic. 

**Атрибуты**:
* `client`: Экземпляр класса `anthropic.Client` для взаимодействия с API.

**Методы**:
* `generate_text()`:  Генерирует текст на основе предоставленного запроса.
* `analyze_sentiment()`: Анализирует тональность предоставленного текста.
* `translate_text()`:  Переводит предоставленный текст с исходного языка на целевой язык.

## Функции

### `generate_text`

**Цель**: Функция генерирует текст на основе предоставленного запроса.

**Параметры**:
* `prompt` (str): Запрос для генерации текста.
* `max_tokens_to_sample` (int, optional): Максимальное количество токенов для генерации. По умолчанию 100.

**Возвращает**:
* `str`: Сгенерированный текст.

**Пример**:
```python
>>> claude_client.generate_text('Напиши короткий рассказ.')
'Короткий рассказ о...'
```

### `analyze_sentiment`

**Цель**:  Функция анализирует тональность предоставленного текста.

**Параметры**:
* `text` (str): Текст для анализа.

**Возвращает**:
* `str`: Результат анализа тональности.

**Пример**:
```python
>>> claude_client.analyze_sentiment('Я очень рад!')
'Позитивный'
```

### `translate_text`

**Цель**:  Функция переводит предоставленный текст с исходного языка на целевой язык.

**Параметры**:
* `text` (str): Текст для перевода.
* `source_language` (str): Код исходного языка.
* `target_language` (str): Код целевого языка.

**Возвращает**:
* `str`: Переведенный текст.

**Пример**:
```python
>>> claude_client.translate_text('Привет', 'ru', 'en')
'Hello'
```

## Пример использования

```python
# Пример использования класса
if __name__ == '__main__':
    api_key = 'your-api-key'
    claude_client = ClaudeClient(api_key)

    # Пример генерации текста
    prompt = 'Напиши короткий рассказ о роботе, который учится любить.'
    generated_text = claude_client.generate_text(prompt)
    print('Сгенерированный текст:', generated_text)

    # Пример анализа тональности
    text_to_analyze = 'Я очень рад сегодня!'
    sentiment_analysis = claude_client.analyze_sentiment(text_to_analyze)
    print('Анализ тональности:', sentiment_analysis)

    # Пример перевода текста
    text_to_translate = 'Привет, как дела?'
    source_language = 'ru'
    target_language = 'en'
    translated_text = claude_client.translate_text(text_to_translate, source_language, target_language)
    print('Переведенный текст:', translated_text)
```

## Дополнительные сведения

Модуль `claude.py` реализует функциональность для взаимодействия с API модели Claude от Anthropic. Используйте класс `ClaudeClient` для выполнения различных задач, таких как генерация текста, анализ тональности и перевод.