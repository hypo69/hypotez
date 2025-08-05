# Модуль HeliconeAI

## Обзор

Этот модуль предоставляет класс `HeliconeAI`, который использует Helicone для отслеживания и оптимизации использования моделей машинного обучения, таких как OpenAI GPT-3.5-turbo и text-davinci-003. Он позволяет генерировать текст, анализировать тональность, создавать краткие изложения и переводить текст, а также отправляет информацию о выполненных запросах в Helicone для анализа.

## Класс `HeliconeAI`

### Описание

Класс `HeliconeAI` реализует функции, основанные на моделях машинного обучения OpenAI, с использованием Helicone для отслеживания использования моделей.

**Наследует:** 
   - Нет

**Атрибуты:**

   - `helicone` (`Helicone`): Экземпляр класса `Helicone` для отслеживания использования модели.
   - `client` (`OpenAI`): Клиент OpenAI для взаимодействия с моделями.

**Методы:**

   - `generate_poem(prompt: str) -> str`: Генерирует стихотворение на основе заданного промпта.
   - `analyze_sentiment(text: str) -> str`: Анализирует тональность текста.
   - `summarize_text(text: str) -> str`: Создает краткое изложение текста.
   - `translate_text(text: str, target_language: str) -> str`: Переводит текст на указанный язык.

### `generate_poem(prompt: str) -> str`

**Назначение:** 
   - Генерирует стихотворение на основе заданного промпта.

**Параметры:**

   - `prompt` (str): Промпт для генерации стихотворения.

**Возвращает:**

   - `str`: Сгенерированное стихотворение.

**Как работает функция:**

   - Инициализирует модель `gpt-3.5-turbo` для генерации текста.
   - Собирает информацию о модели и запросе.
   - Отправляет запрос в OpenAI с помощью `self.client.chat.completions.create`.
   - Записывает информацию о запросе в Helicone с помощью `self.helicone.log_completion`.
   - Возвращает сгенерированный текст.

**Примеры:**

   ```python
   >>> helicone_ai = HeliconeAI()
   >>> poem = helicone_ai.generate_poem("Напиши мне стихотворение про кота.")
   >>> print(poem)
   ```

### `analyze_sentiment(text: str) -> str`

**Назначение:** 
   - Анализирует тональность текста.

**Параметры:**

   - `text` (str): Текст для анализа.

**Возвращает:**

   - `str`: Результат анализа тональности.

**Как работает функция:**

   - Инициализирует модель `text-davinci-003` для анализа текста.
   - Собирает информацию о модели и запросе.
   - Отправляет запрос в OpenAI с помощью `self.client.completions.create`.
   - Записывает информацию о запросе в Helicone с помощью `self.helicone.log_completion`.
   - Возвращает результат анализа тональности.

**Примеры:**

   ```python
   >>> helicone_ai = HeliconeAI()
   >>> sentiment = helicone_ai.analyze_sentiment("Сегодня был отличный день!")
   >>> print(sentiment)
   ```

### `summarize_text(text: str) -> str`

**Назначение:** 
   - Создает краткое изложение текста.

**Параметры:**

   - `text` (str): Текст для изложения.

**Возвращает:**

   - `str`: Краткое изложение текста.

**Как работает функция:**

   - Инициализирует модель `text-davinci-003` для изложения текста.
   - Собирает информацию о модели и запросе.
   - Отправляет запрос в OpenAI с помощью `self.client.completions.create`.
   - Записывает информацию о запросе в Helicone с помощью `self.helicone.log_completion`.
   - Возвращает краткое изложение текста.

**Примеры:**

   ```python
   >>> helicone_ai = HeliconeAI()
   >>> summary = helicone_ai.summarize_text("Длинный текст для изложения...")
   >>> print(summary)
   ```

### `translate_text(text: str, target_language: str) -> str`

**Назначение:** 
   - Переводит текст на указанный язык.

**Параметры:**

   - `text` (str): Текст для перевода.
   - `target_language` (str): Целевой язык перевода.

**Возвращает:**

   - `str`: Переведенный текст.

**Как работает функция:**

   - Инициализирует модель `text-davinci-003` для перевода текста.
   - Собирает информацию о модели и запросе.
   - Отправляет запрос в OpenAI с помощью `self.client.completions.create`.
   - Записывает информацию о запросе в Helicone с помощью `self.helicone.log_completion`.
   - Возвращает переведенный текст.

**Примеры:**

   ```python
   >>> helicone_ai = HeliconeAI()
   >>> translation = helicone_ai.translate_text("Hello, how are you?", "русский")
   >>> print(translation)
   ```

## Функция `main()`

**Назначение:** 
   - Тестирует функциональность класса `HeliconeAI`.

**Как работает функция:**

   - Создает экземпляр класса `HeliconeAI`.
   - Вызывает методы класса `HeliconeAI` для генерации стихотворения, анализа тональности, создания изложения и перевода текста.
   - Выводит результаты на консоль.

## Примеры

```python
>>> helicone_ai = HeliconeAI()

>>> poem = helicone_ai.generate_poem("Напиши мне стихотворение про кота.")
>>> print(poem)

>>> sentiment = helicone_ai.analyze_sentiment("Сегодня был отличный день!")
>>> print(sentiment)

>>> summary = helicone_ai.summarize_text("Длинный текст для изложения...")
>>> print(summary)

>>> translation = helicone_ai.translate_text("Hello, how are you?", "русский")
>>> print(translation)
```