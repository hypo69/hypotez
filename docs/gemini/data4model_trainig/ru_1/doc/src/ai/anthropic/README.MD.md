# Документация модуля `src.ai.anthropic`

## Обзор

Этот модуль предоставляет интерфейс для взаимодействия с языковой моделью Claude от Anthropic. Он включает основные функции для генерации текста, анализа тональности и перевода текста.

## Подробней

Этот модуль позволяет взаимодействовать с API Claude от Anthropic для выполнения различных задач обработки естественного языка. Для работы с модулем требуется установить библиотеку `anthropic` и получить API-ключ от Anthropic. Модуль предоставляет класс `ClaudeClient` для инициализации клиента и выполнения запросов к API.

## Оглавление

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

Для использования этого модуля необходимо установить библиотеку `anthropic`:

```bash
pip install anthropic
```

## Использование

### Инициализация

Сначала инициализируйте `ClaudeClient` с вашим Anthropic API ключом:

```python
from claude_client import ClaudeClient

api_key = "your-api-key"
claude_client = ClaudeClient(api_key)
```

### Генерация текста

Генерация текста на основе заданного запроса:

```python
prompt = "Write a short story about a robot learning to love."
generated_text = claude_client.generate_text(prompt)
print("Generated Text:", generated_text)
```

### Анализ тональности

Анализ тональности заданного текста:

```python
text_to_analyze = "I am very happy today!"
sentiment_analysis = claude_client.analyze_sentiment(text_to_analyze)
print("Sentiment Analysis:", sentiment_analysis)
```

### Перевод текста

Перевод текста с одного языка на другой:

```python
text_to_translate = "Hello, how are you?"
source_language = "en"
target_language = "es"
translated_text = claude_client.translate_text(text_to_translate, source_language, target_language)
print("Translated Text:", translated_text)
```

## Пример кода

Вот полный пример использования `ClaudeClient`:

```python
from claude_client import ClaudeClient

api_key = "your-api-key"
claude_client = ClaudeClient(api_key)

# Generate text
prompt = "Write a short story about a robot learning to love."
generated_text = claude_client.generate_text(prompt)
print("Generated Text:", generated_text)

# Analyze sentiment
text_to_analyze = "I am very happy today!"
sentiment_analysis = claude_client.analyze_sentiment(text_to_analyze)
print("Sentiment Analysis:", sentiment_analysis)

# Translate text
text_to_translate = "Hello, how are you?"
source_language = "en"
target_language = "es"
translated_text = claude_client.translate_text(text_to_translate, source_language, target_language)
print("Translated Text:", translated_text)
```

## Методы

### `generate_text(prompt, max_tokens_to_sample=100)`

Генерирует текст на основе заданного запроса.

**Параметры:**

- `prompt` (str): Запрос, на основе которого генерируется текст.
- `max_tokens_to_sample` (int): Максимальное количество токенов для генерации. По умолчанию 100.

**Возвращает:**

- `str`: Сгенерированный текст.

**Принцип работы:**

- Функция `generate_text` принимает строку запроса `prompt` и опциональный параметр `max_tokens_to_sample`, определяющий максимальное количество токенов в сгенерированном тексте. Она использует API Claude для генерации текста на основе запроса и возвращает сгенерированный текст.

**Примеры:**

```python
from claude_client import ClaudeClient

api_key = "your-api-key"
claude_client = ClaudeClient(api_key)

prompt = "Напиши короткий рассказ о коте, который любит гулять по ночам."
generated_text = claude_client.generate_text(prompt)
print("Сгенерированный текст:", generated_text)

prompt = "Сочини стихотворение о весне."
generated_text = claude_client.generate_text(prompt, max_tokens_to_sample=50)
print("Сгенерированный текст:", generated_text)
```

### `analyze_sentiment(text)`

Анализирует тональность заданного текста.

**Параметры:**

- `text` (str): Текст для анализа.

**Возвращает:**

- `str`: Результат анализа тональности.

**Принцип работы:**

- Функция `analyze_sentiment` принимает строку текста `text` для анализа тональности. Она использует API Claude для анализа тональности текста и возвращает результат анализа.

**Примеры:**

```python
from claude_client import ClaudeClient

api_key = "your-api-key"
claude_client = ClaudeClient(api_key)

text_to_analyze = "Я очень рад сегодня!"
sentiment_analysis = claude_client.analyze_sentiment(text_to_analyze)
print("Анализ тональности:", sentiment_analysis)

text_to_analyze = "Я очень расстроен из-за этой новости."
sentiment_analysis = claude_client.analyze_sentiment(text_to_analyze)
print("Анализ тональности:", sentiment_analysis)
```

### `translate_text(text, source_language, target_language)`

Переводит заданный текст с исходного языка на целевой язык.

**Параметры:**

- `text` (str): Текст для перевода.
- `source_language` (str): Код исходного языка.
- `target_language` (str): Код целевого языка.

**Возвращает:**

- `str`: Переведенный текст.

**Принцип работы:**

- Функция `translate_text` принимает строку текста `text`, код исходного языка `source_language` и код целевого языка `target_language`. Она использует API Claude для перевода текста с исходного языка на целевой язык и возвращает переведенный текст.

**Примеры:**

```python
from claude_client import ClaudeClient

api_key = "your-api-key"
claude_client = ClaudeClient(api_key)

text_to_translate = "Hello, how are you?"
source_language = "en"
target_language = "es"
translated_text = claude_client.translate_text(text_to_translate, source_language, target_language)
print("Переведенный текст:", translated_text)

text_to_translate = "Как дела?"
source_language = "ru"
target_language = "en"
translated_text = claude_client.translate_text(text_to_translate, source_language, target_language)
print("Переведенный текст:", translated_text)
```

## Вклад

Приветствуются вклады! Не стесняйтесь отправлять pull request или открывать issue, если у вас возникнут какие-либо проблемы или предложения по улучшению.

## Лицензия

Этот проект лицензирован в соответствии с лицензией MIT. Подробности см. в файле [LICENSE](LICENSE).

---

**Примечание:** Замените `"your-api-key"` на ваш фактический Anthropic API ключ.