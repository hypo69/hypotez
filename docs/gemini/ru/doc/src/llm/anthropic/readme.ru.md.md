# Документация для модуля `src.ai.anthropic`

## Обзор

Этот модуль предоставляет клиент для взаимодействия с моделью Claude от Anthropic. Он включает базовые функции для генерации текста, анализа тональности и перевода текста.

## Подробней

Этот модуль предназначен для упрощения работы с API Claude от Anthropic. Он предоставляет удобные методы для выполнения основных задач, таких как генерация текста на основе заданного промпта, анализ тональности текста и перевод текста с одного языка на другой. Модуль также содержит инструкции по установке и использованию, а также примеры кода.

## Установка

Для использования этого модуля вам необходимо установить библиотеку `anthropic`:

```bash
pip install anthropic
```

## Использование

### Инициализация

Сначала инициализируйте `ClaudeClient` с вашим API-ключом от Anthropic:

```python
from claude_client import ClaudeClient

api_key = "your-api-key"
claude_client = ClaudeClient(api_key)
```

### Генерация текста

Сгенерируйте текст на основе заданного промпта:

```python
prompt = "Напишите короткую историю о роботе, который учится любить."
generated_text = claude_client.generate_text(prompt)
print("Сгенерированный текст:", generated_text)
```

### Анализ тональности

Проанализируйте тональность заданного текста:

```python
text_to_analyze = "Сегодня я очень счастлив!"
sentiment_analysis = claude_client.analyze_sentiment(text_to_analyze)
print("Анализ тональности:", sentiment_analysis)
```

### Перевод текста

Переведите текст с одного языка на другой:

```python
text_to_translate = "Привет, как дела?"
source_language = "ru"
target_language = "en"
translated_text = claude_client.translate_text(text_to_translate, source_language, target_language)
print("Переведенный текст:", translated_text)
```

## Пример кода

Вот полный пример использования `ClaudeClient`:

```python
from claude_client import ClaudeClient

api_key = "your-api-key"
claude_client = ClaudeClient(api_key)

# Генерация текста
prompt = "Напишите короткую историю о роботе, который учится любить."
generated_text = claude_client.generate_text(prompt)
print("Сгенерированный текст:", generated_text)

# Анализ тональности
text_to_analyze = "Сегодня я очень счастлив!"
sentiment_analysis = claude_client.analyze_sentiment(text_to_analyze)
print("Анализ тональности:", sentiment_analysis)

# Перевод текста
text_to_translate = "Привет, как дела?"
source_language = "ru"
target_language = "en"
translated_text = claude_client.translate_text(text_to_translate, source_language, target_language)
print("Переведенный текст:", translated_text)
```

## Методы

### `generate_text(prompt, max_tokens_to_sample=100)`

Генерирует текст на основе заданного промпта.

**Параметры:**

- `prompt` (str): Промпт для генерации текста.
- `max_tokens_to_sample` (int): Максимальное количество токенов для генерации.

**Возвращает:**

- `str`: Сгенерированный текст.

**Как работает функция:**
- Функция принимает промпт и максимальное количество токенов в качестве параметров.
- Она использует API Claude для генерации текста на основе заданного промпта.
- Возвращает сгенерированный текст.

**Примеры:**

```python
prompt = "Напишите короткую историю о коте, который любит спать."
generated_text = claude_client.generate_text(prompt)
print(generated_text)
```

### `analyze_sentiment(text)`

Анализирует тональность заданного текста.

**Параметры:**

- `text` (str): Текст для анализа.

**Возвращает:**

- `str`: Результат анализа тональности.

**Как работает функция:**
- Функция принимает текст в качестве параметра.
- Она использует API Claude для анализа тональности текста.
- Функция возвращает результат анализа тональности.

**Примеры:**

```python
text_to_analyze = "Я очень рад сегодня!"
sentiment_analysis = claude_client.analyze_sentiment(text_to_analyze)
print(sentiment_analysis)
```

### `translate_text(text, source_language, target_language)`

Переводит заданный текст с одного языка на другой.

**Параметры:**

- `text` (str): Текст для перевода.
- `source_language` (str): Код исходного языка.
- `target_language` (str): Код целевого языка.

**Возвращает:**

- `str`: Переведенный текст.

**Как работает функция:**

- Функция принимает текст, код исходного языка и код целевого языка в качестве параметров.
- Она использует API Claude для перевода текста с одного языка на другой.
- Возвращает переведенный текст.

**Примеры:**

```python
text_to_translate = "Как дела?"
source_language = "ru"
target_language = "en"
translated_text = claude_client.translate_text(text_to_translate, source_language, target_language)
print(translated_text)