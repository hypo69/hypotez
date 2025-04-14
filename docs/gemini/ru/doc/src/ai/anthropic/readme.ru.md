# Документация для модуля `src.ai.anthropic`

## Обзор

Этот модуль представляет собой клиент для взаимодействия с моделью Claude от Anthropic. Он предоставляет простой интерфейс для выполнения таких задач, как генерация текста, анализ тональности и перевод текста.

## Подробнее

Модуль предназначен для упрощения интеграции с языковой моделью Claude в проекте `hypotez`. Он предоставляет удобные методы для выполнения основных операций, связанных с обработкой текста.

## Содержание

- [Установка](#установка)
- [Использование](#использование)
  - [Инициализация](#инициализация)
  - [Генерация текста](#генерация-текста)
  - [Анализ тональности](#анализ-тональности)
  - [Перевод текста](#перевод-текста)
- [Пример кода](#пример-кода)
- [Методы](#методы)
  - [`generate_text`](#generate_textprompt-max_tokens_to_sample100)
  - [`analyze_sentiment`](#analyze_sentimenttext)
  - [`translate_text`](#translate_texttext-source_language-target_language)
- [Вклад](#вклад)
- [Лицензия](#лицензия)

## Установка

Для использования данного модуля необходимо установить библиотеку `anthropic`:

```bash
pip install anthropic
```

## Использование

### Инициализация

Для начала работы необходимо инициализировать `ClaudeClient` с вашим API-ключом от Anthropic:

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

Полный пример использования `ClaudeClient`:

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

**Пример использования:**

```python
prompt = "Напишите короткий стих о лете."
generated_text = claude_client.generate_text(prompt, max_tokens_to_sample=50)
print(generated_text)
```

### `analyze_sentiment(text)`

Анализирует тональность заданного текста.

**Параметры:**

- `text` (str): Текст для анализа.

**Возвращает:**

- `str`: Результат анализа тональности. <Заготовка: сюда нужно вставить тип данных, который возвращает функция>

**Пример использования:**

```python
text_to_analyze = "Этот фильм был невероятно захватывающим!"
sentiment = claude_client.analyze_sentiment(text_to_analyze)
print(sentiment)
```

### `translate_text(text, source_language, target_language)`

Переводит заданный текст с одного языка на другой.

**Параметры:**

- `text` (str): Текст для перевода.
- `source_language` (str): Код исходного языка.
- `target_language` (str): Код целевого языка.

**Возвращает:**

- `str`: Переведенный текст.

**Пример использования:**

```python
text_to_translate = "Как дела?"
source_language = "ru"
target_language = "en"
translated_text = claude_client.translate_text(text_to_translate, source_language, target_language)
print(translated_text)
```

## Вклад

Приветствуется вклад в развитие проекта. Вы можете отправлять pull request или открывать issue, если у вас есть предложения по улучшению или вы столкнулись с какими-либо проблемами.

## Лицензия

Этот проект лицензирован под MIT License. Подробности смотрите в файле [LICENSE](LICENSE).

**Примечание:** Не забудьте заменить `"your-api-key"` на ваш реальный API-ключ от Anthropic.