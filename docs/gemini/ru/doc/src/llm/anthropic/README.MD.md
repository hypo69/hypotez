# Модуль для работы с Claude Anthropic

## Обзор

Этот модуль Python предоставляет простой интерфейс для взаимодействия с языковой моделью Claude от Anthropic. Он включает в себя основные функции для генерации текста, анализа тональности и перевода текста.

## Подробнее

Этот модуль позволяет упростить взаимодействие с API Claude, предоставляя готовые функции для выполнения различных задач обработки текста. Он предназначен для того, чтобы разработчики могли легко интегрировать возможности Claude в свои приложения.

## Содержание

- [Установка](#installation)
- [Использование](#usage)
  - [Инициализация](#initialization)
  - [Генерация текста](#generate-text)
  - [Анализ тональности](#analyze-sentiment)
  - [Перевод текста](#translate-text)
- [Пример кода](#example-code)
- [Методы](#methods)
  - [`generate_text`](#generate_textprompt-max_tokens_to_sample100)
  - [`analyze_sentiment`](#analyze_sentimenttext)
  - [`translate_text`](#translate_texttext-source_language-target_language)
- [Вклад](#contributing)
- [Лицензия](#license)

## Установка

Для использования этого модуля необходимо установить библиотеку `anthropic`:

```bash
pip install anthropic
```

## Использование

### Инициализация

Сначала инициализируйте `ClaudeClient` с вашим ключом API Anthropic:

```python
from claude_client import ClaudeClient

api_key = "your-api-key"
claude_client = ClaudeClient(api_key)
```

### Генерация текста

Сгенерируйте текст на основе заданного запроса:

```python
prompt = "Напиши короткий рассказ о роботе, который учится любить."
generated_text = claude_client.generate_text(prompt)
print("Сгенерированный текст:", generated_text)
```

### Анализ тональности

Проанализируйте тональность заданного текста:

```python
text_to_analyze = "Я очень счастлив сегодня!"
sentiment_analysis = claude_client.analyze_sentiment(text_to_analyze)
print("Анализ тональности:", sentiment_analysis)
```

### Перевод текста

Переведите текст с одного языка на другой:

```python
text_to_translate = "Hello, how are you?"
source_language = "en"
target_language = "es"
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
prompt = "Напиши короткий рассказ о роботе, который учится любить."
generated_text = claude_client.generate_text(prompt)
print("Сгенерированный текст:", generated_text)

# Анализ тональности
text_to_analyze = "Я очень счастлив сегодня!"
sentiment_analysis = claude_client.analyze_sentiment(text_to_analyze)
print("Анализ тональности:", sentiment_analysis)

# Перевод текста
text_to_translate = "Hello, how are you?"
source_language = "en"
target_language = "es"
translated_text = claude_client.translate_text(text_to_translate, source_language, target_language)
print("Переведенный текст:", translated_text)
```

## Методы

### `generate_text(prompt, max_tokens_to_sample=100)`

Генерирует текст на основе заданного запроса.

**Параметры**:

- `prompt` (str): Запрос для генерации текста.
- `max_tokens_to_sample` (int): Максимальное количество токенов для генерации (по умолчанию: 100).

**Возвращает**:

- `str`: Сгенерированный текст.

### `analyze_sentiment(text)`

Анализирует тональность заданного текста.

**Параметры**:

- `text` (str): Текст для анализа.

**Возвращает**:

- `str`: Результат анализа тональности.

### `translate_text(text, source_language, target_language)`

Переводит заданный текст с исходного языка на целевой язык.

**Параметры**:

- `text` (str): Текст для перевода.
- `source_language` (str): Код исходного языка.
- `target_language` (str): Код целевого языка.

**Возвращает**:

- `str`: Переведенный текст.

## Вклад

Приветствуются вклады! Не стесняйтесь отправлять запросы на включение внесенных изменений или открывать проблему, если вы столкнулись с какими-либо проблемами или у вас есть предложения по улучшению.

## Лицензия

Этот проект лицензирован в соответствии с лицензией MIT. Подробности см. в файле [LICENSE](LICENSE).

---

**Примечание:** Замените `"your-api-key"` на свой фактический ключ API Anthropic.