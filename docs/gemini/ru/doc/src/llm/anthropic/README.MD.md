# Модуль для работы с языковой моделью Claude от Anthropic

## Обзор

Модуль `claude_client.py` предоставляет простой интерфейс для взаимодействия с языковой моделью Claude от Anthropic. В нем представлены основные функции для генерации текста, анализа настроений и перевода текста.

##  Установка

Для использования этого модуля необходимо установить библиотеку `anthropic`:

```bash
pip install anthropic
```

## Использование

### Инициализация

Сначала инициализируйте `ClaudeClient` с помощью своего API-ключа Anthropic:

```python
from claude_client import ClaudeClient

api_key = "your-api-key"
claude_client = ClaudeClient(api_key)
```

### Генерация текста

Сгенерируйте текст на основе заданного запроса:

```python
prompt = "Напишите короткий рассказ о роботе, который учится любить."
generated_text = claude_client.generate_text(prompt)
print("Сгенерированный текст:", generated_text)
```

### Анализ настроений

Проанализируйте настроение заданного текста:

```python
text_to_analyze = "Я сегодня очень счастлив!"
sentiment_analysis = claude_client.analyze_sentiment(text_to_analyze)
print("Анализ настроений:", sentiment_analysis)
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
prompt = "Напишите короткий рассказ о роботе, который учится любить."
generated_text = claude_client.generate_text(prompt)
print("Сгенерированный текст:", generated_text)

# Анализ настроений
text_to_analyze = "Я сегодня очень счастлив!"
sentiment_analysis = claude_client.analyze_sentiment(text_to_analyze)
print("Анализ настроений:", sentiment_analysis)

# Перевод текста
text_to_translate = "Привет, как дела?"
source_language = "ru"
target_language = "en"
translated_text = claude_client.translate_text(text_to_translate, source_language, target_language)
print("Переведенный текст:", translated_text)
```

## Методы

### `generate_text(prompt, max_tokens_to_sample=100)`

Генерирует текст на основе заданного запроса.

- **Параметры:**
  - `prompt`: Запрос для генерации текста.
  - `max_tokens_to_sample`: Максимальное количество токенов для генерации.
- **Возвращает:** Сгенерированный текст.

### `analyze_sentiment(text)`

Анализирует настроение заданного текста.

- **Параметры:**
  - `text`: Текст для анализа.
- **Возвращает:** Результат анализа настроений.

### `translate_text(text, source_language, target_language)`

Переводит заданный текст с исходного языка на целевой язык.

- **Параметры:**
  - `text`: Текст для перевода.
  - `source_language`: Код исходного языка.
  - `target_language`: Код целевого языка.
- **Возвращает:** Переведенный текст.

## Внесение вклада

Вклад приветствуется! Не стесняйтесь отправлять запрос на слияние или открывать проблему, если вы столкнулись с проблемами или у вас есть предложения по улучшению.

## Лицензия

Этот проект распространяется по лицензии MIT. Подробнее см. в файле [LICENSE](LICENSE).

---

**Примечание:** Замените `"your-api-key"` на свой фактический API-ключ Anthropic.