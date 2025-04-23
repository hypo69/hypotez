## \file hypotez/src/llm/anthropic/readme.ru.md
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

```rst
.. module:: src.ai.anthropic
```

<TABLE >
<TR>
<TD>
<A HREF = 'https://github.com/hypo69/hypotez/blob/master/README.MD'>[Root ↑]</A>
</TD>
<TD>
<A HREF = 'https://github.com/hypotez/blob/master/src/README.MD'>src</A> /
<A HREF = 'https://github.com/hypotez/blob/master/src/ai/README.MD'>ai</A>
</TD>
<TD>
<A HREF = 'https://github.com/hypotez/blob/master/src/ai/anthropic/README.MD'>English</A>
</TD>
</TABLE>

### README.md

# Клиент для модели Claude от Anthropic

Этот Python-модуль предоставляет простой интерфейс для взаимодействия с языковой моделью Claude от Anthropic. Он включает базовые функции для генерации текста, анализа тональности и перевода текста.

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

Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода инициализирует клиент `ClaudeClient` для взаимодействия с моделью Claude от Anthropic.

Шаги выполнения
-------------------------
1. Импортируется класс `ClaudeClient` из модуля `claude_client`.
2. Определяется переменная `api_key`, в которой хранится API-ключ для доступа к сервисам Anthropic. **Необходимо заменить "your-api-key" на ваш фактический API-ключ.**
3. Создается экземпляр класса `ClaudeClient` с использованием переданного API-ключа.

Пример использования
-------------------------

```python
from claude_client import ClaudeClient

api_key = "your-api-key"  # Замените на ваш реальный API-ключ
claude_client = ClaudeClient(api_key)
```

### Генерация текста

Сгенерируйте текст на основе заданного промпта:

```python
prompt = "Напишите короткую историю о роботе, который учится любить."
generated_text = claude_client.generate_text(prompt)
print("Сгенерированный текст:", generated_text)
```

Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода демонстрирует генерацию текста с использованием модели Claude от Anthropic на основе заданного запроса (промпта).

Шаги выполнения
-------------------------
1. Определяется переменная `prompt`, содержащая текстовый запрос для генерации истории.
2. Вызывается метод `generate_text` у экземпляра `claude_client`, которому передается промпт. Функция возвращает сгенерированный текст.
3. Выполняется вывод сгенерированного текста на консоль с помощью функции `print`.

Пример использования
-------------------------

```python
from claude_client import ClaudeClient

api_key = "your-api-key"
claude_client = ClaudeClient(api_key)

prompt = "Напишите короткую историю о коте, который путешествует по миру."
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

Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода демонстрирует анализ тональности текста с использованием модели Claude от Anthropic.

Шаги выполнения
-------------------------
1. Определяется переменная `text_to_analyze`, содержащая текст, который необходимо проанализировать на предмет тональности.
2. Вызывается метод `analyze_sentiment` у экземпляра `claude_client`, которому передается текст для анализа. Функция возвращает результат анализа тональности.
3. Выполняется вывод результата анализа тональности на консоль с помощью функции `print`.

Пример использования
-------------------------

```python
from claude_client import ClaudeClient

api_key = "your-api-key"
claude_client = ClaudeClient(api_key)

text_to_analyze = "Я очень расстроен из-за плохой погоды."
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

Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода демонстрирует перевод текста с одного языка на другой с использованием модели Claude от Anthropic.

Шаги выполнения
-------------------------
1. Определяется переменная `text_to_translate`, содержащая текст, который необходимо перевести.
2. Определяется переменная `source_language`, содержащая код исходного языка текста (например, "ru" для русского).
3. Определяется переменная `target_language`, содержащая код целевого языка перевода (например, "en" для английского).
4. Вызывается метод `translate_text` у экземпляра `claude_client`, которому передается текст для перевода, код исходного языка и код целевого языка. Функция возвращает переведенный текст.
5. Выполняется вывод переведенного текста на консоль с помощью функции `print`.

Пример использования
-------------------------

```python
from claude_client import ClaudeClient

api_key = "your-api-key"
claude_client = ClaudeClient(api_key)

text_to_translate = "How are you?"
source_language = "en"
target_language = "fr"
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

Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода представляет собой полный пример использования класса `ClaudeClient` для выполнения различных задач, таких как генерация текста, анализ тональности и перевод текста.

Шаги выполнения
-------------------------
1. Импортируется класс `ClaudeClient` из модуля `claude_client`.
2. Определяется переменная `api_key`, в которой хранится API-ключ для доступа к сервисам Anthropic. **Необходимо заменить "your-api-key" на ваш фактический API-ключ.**
3. Создается экземпляр класса `ClaudeClient` с использованием переданного API-ключа.
4. Вызывается метод `generate_text` для генерации текста на основе заданного промпта.
5. Вызывается метод `analyze_sentiment` для анализа тональности заданного текста.
6. Вызывается метод `translate_text` для перевода текста с одного языка на другой.
7. Результаты каждой операции выводятся на консоль с помощью функции `print`.

Пример использования
-------------------------

```python
from claude_client import ClaudeClient

api_key = "YOUR_API_KEY" # Замените на ваш ключ
claude_client = ClaudeClient(api_key)

# Генерация текста
prompt = "Напиши рецепт шоколадного торта."
generated_text = claude_client.generate_text(prompt)
print("Сгенерированный текст:", generated_text)

# Анализ тональности
text_to_analyze = "Я получил повышение на работе!"
sentiment_analysis = claude_client.analyze_sentiment(text_to_analyze)
print("Анализ тональности:", sentiment_analysis)

# Перевод текста
text_to_translate = "The quick brown fox jumps over the lazy dog."
source_language = "en"
target_language = "de"
translated_text = claude_client.translate_text(text_to_translate, source_language, target_language)
print("Переведенный текст:", translated_text)
```

## Методы

### `generate_text(prompt, max_tokens_to_sample=100)`

Генерирует текст на основе заданного промпта.

- **Параметры:**
  - `prompt`: Промпт для генерации текста.
  - `max_tokens_to_sample`: Максимальное количество токенов для генерации.
- **Возвращает:** Сгенерированный текст.

Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода описывает метод `generate_text`, который используется для генерации текста на основе заданного промпта и максимального количества токенов.

Шаги выполнения
-------------------------
1. Метод `generate_text` принимает два параметра: `prompt` (текстовый промпт) и `max_tokens_to_sample` (максимальное количество токенов для генерации).
2. Метод отправляет запрос к модели Claude от Anthropic, используя предоставленный промпт.
3. Модель генерирует текст на основе промпта, ограничивая количество токенов заданным значением `max_tokens_to_sample`.
4. Метод возвращает сгенерированный текст.

Пример использования
-------------------------

```python
from claude_client import ClaudeClient

api_key = "your-api-key"
claude_client = ClaudeClient(api_key)

prompt = "Напиши заголовок для статьи о машинном обучении."
generated_text = claude_client.generate_text(prompt, max_tokens_to_sample=50)
print("Сгенерированный текст:", generated_text)
```

### `analyze_sentiment(text)`

Анализирует тональность заданного текста.

- **Параметры:**
  - `text`: Текст для анализа.
- **Возвращает:** Результат анализа тональности.

Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода описывает метод `analyze_sentiment`, который анализирует тональность заданного текста.

Шаги выполнения
-------------------------
1. Метод `analyze_sentiment` принимает один параметр: `text` (текст для анализа).
2. Метод отправляет запрос к модели Claude от Anthropic для анализа тональности предоставленного текста.
3. Модель анализирует текст и определяет его тональность (например, положительную, отрицательную или нейтральную).
4. Метод возвращает результат анализа тональности.

Пример использования
-------------------------

```python
from claude_client import ClaudeClient

api_key = "your-api-key"
claude_client = ClaudeClient(api_key)

text_to_analyze = "Я в восторге от нового фильма!"
sentiment_analysis = claude_client.analyze_sentiment(text_to_analyze)
print("Анализ тональности:", sentiment_analysis)
```

### `translate_text(text, source_language, target_language)`

Переводит заданный текст с одного языка на другой.

- **Параметры:**
  - `text`: Текст для перевода.
  - `source_language`: Код исходного языка.
  - `target_language`: Код целевого языка.
- **Возвращает:** Переведенный текст.

Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода описывает метод `translate_text`, который переводит заданный текст с одного языка на другой.

Шаги выполнения
-------------------------
1. Метод `translate_text` принимает три параметра: `text` (текст для перевода), `source_language` (код исходного языка) и `target_language` (код целевого языка).
2. Метод отправляет запрос к модели Claude от Anthropic для перевода текста с указанного исходного языка на целевой язык.
3. Модель переводит текст.
4. Метод возвращает переведенный текст.

Пример использования
-------------------------

```python
from claude_client import ClaudeClient

api_key = "your-api-key"
claude_client = ClaudeClient(api_key)

text_to_translate = "Hello, world!"
source_language = "en"
target_language = "es"
translated_text = claude_client.translate_text(text_to_translate, source_language, target_language)
print("Переведенный текст:", translated_text)
```

## Вклад

Вклад приветствуется! Не стесняйтесь отправлять pull request или открывать issue, если вы столкнулись с какими-либо проблемами или имеете предложения по улучшению.

## Лицензия

Этот проект лицензирован под MIT License. Подробности смотрите в файле [LICENSE](LICENSE).

---

**Примечание:** Замените `"your-api-key"` на ваш реальный API-ключ от Anthropic.