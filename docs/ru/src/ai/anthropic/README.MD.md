# Документация модуля `src.ai.anthropic`

## Обзор

Модуль предоставляет простой интерфейс для взаимодействия с языковой моделью Claude от Anthropic. Включает основные функции для генерации текста, анализа тональности и перевода текста.

## Подробнее

Этот модуль позволяет интегрировать возможности Claude AI в ваши Python-приложения. Он предоставляет удобные методы для выполнения различных задач обработки естественного языка, таких как генерация текста на основе заданного запроса, анализ тональности текста и перевод текста между разными языками.

## Установка

Для использования модуля необходимо установить библиотеку `anthropic`:

```bash
pip install anthropic
```

## Использование

### Инициализация

Сначала инициализируйте `ClaudeClient`, указав свой API-ключ Anthropic:

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
text_to_analyze = "Я сегодня очень счастлив!"
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

Полный пример использования `ClaudeClient`:

```python
from claude_client import ClaudeClient

api_key = "your-api-key"
claude_client = ClaudeClient(api_key)

# Сгенерировать текст
prompt = "Напиши короткий рассказ о роботе, который учится любить."
generated_text = claude_client.generate_text(prompt)
print("Сгенерированный текст:", generated_text)

# Анализ тональности
text_to_analyze = "Я сегодня очень счастлив!"
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

### `generate_text(prompt: str, max_tokens_to_sample: int = 100) -> str`

Генерирует текст на основе заданного запроса.

**Параметры:**

- `prompt` (str): Запрос, на основе которого генерируется текст.
- `max_tokens_to_sample` (int): Максимальное количество токенов для генерации. По умолчанию 100.

**Возвращает:**

- `str`: Сгенерированный текст.

**Как работает функция:**

1. Функция принимает текстовый запрос `prompt` и максимальное количество токенов `max_tokens_to_sample` в качестве входных данных.
2. Она использует API Claude для генерации текста на основе предоставленного запроса, ограничивая количество токенов, чтобы предотвратить слишком длинные ответы.
3. Возвращает сгенерированный текст.

```
    Запрос --> Claude API --> Сгенерированный текст
      prompt     max_tokens       Результат
```

**Примеры:**

```python
# Пример генерации текста с использованием запроса
prompt = "Напиши короткий рассказ о коте-детективе."
generated_text = claude_client.generate_text(prompt)
print(generated_text)

# Пример генерации текста с ограничением количества токенов
prompt = "Объясни, что такое машинное обучение."
generated_text = claude_client.generate_text(prompt, max_tokens_to_sample=50)
print(generated_text)
```

### `analyze_sentiment(text: str) -> str`

Анализирует тональность заданного текста.

**Параметры:**

- `text` (str): Текст для анализа.

**Возвращает:**

- `str`: Результат анализа тональности.

**Как работает функция:**

1. Функция принимает текст `text` в качестве входных данных.
2. Она использует API Claude для анализа тональности предоставленного текста.
3. Возвращает результат анализа тональности.

```
    Текст --> Claude API --> Анализ тональности
    text                       Результат
```

**Примеры:**

```python
# Пример анализа тональности положительного текста
text = "Я очень рад этой возможности!"
sentiment = claude_client.analyze_sentiment(text)
print(sentiment)

# Пример анализа тональности отрицательного текста
text = "Я очень разочарован результатом."
sentiment = claude_client.analyze_sentiment(text)
print(sentiment)
```

### `translate_text(text: str, source_language: str, target_language: str) -> str`

Переводит заданный текст с исходного языка на целевой язык.

**Параметры:**

- `text` (str): Текст для перевода.
- `source_language` (str): Код исходного языка.
- `target_language` (str): Код целевого языка.

**Возвращает:**

- `str`: Переведенный текст.

**Как работает функция:**

1. Функция принимает текст `text`, код исходного языка `source_language` и код целевого языка `target_language` в качестве входных данных.
2. Она использует API Claude для перевода предоставленного текста с исходного языка на целевой язык.
3. Возвращает переведенный текст.

```
    Текст, Исходный язык, Целевой язык --> Claude API --> Переведенный текст
    text, source_language, target_language       Результат
```

**Примеры:**

```python
# Пример перевода текста с английского на испанский
text = "Hello, how are you?"
source_language = "en"
target_language = "es"
translated_text = claude_client.translate_text(text, source_language, target_language)
print(translated_text)

# Пример перевода текста с французского на английский
text = "Bonjour, comment allez-vous?"
source_language = "fr"
target_language = "en"
translated_text = claude_client.translate_text(text, source_language, target_language)
print(translated_text)
```

## Вклад

Приветствуются любые вклады! Не стесняйтесь отправлять запросы на включение изменений или открывать issues, если у вас возникнут какие-либо проблемы или предложения по улучшению.

## Лицензия

Этот проект лицензирован в соответствии с лицензией MIT. Подробности см. в файле [LICENSE](LICENSE).

---

**Примечание:** Замените `"your-api-key"` на свой фактический API-ключ Anthropic.