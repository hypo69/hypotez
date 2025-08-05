# Модуль `helicone`
## Обзор

Модуль `helicone` предоставляет набор функций для взаимодействия с API Helicone и OpenAI. Используется для генерации текста, анализа тональности, изложения и перевода.

##  Подробности

Модуль `helicone` интегрирует возможности моделей искусственного интеллекта Helicone и OpenAI в проект `hypotez`. Он предоставляет набор функций для:

- Генерации стихотворений;
- Анализа тональности текста;
- Изложения текста;
- Перевода текста.

##  Содержание
- [Классы](#классы)
    - [HeliconeAI](#heliconeai)
- [Функции](#функции)
    - [main](#main)

## Классы

### `HeliconeAI`

**Описание**: Класс `HeliconeAI`  предоставляет набор функций для взаимодействия с API Helicone и OpenAI.

**Attributes**:

- `helicone` (Helicone): Экземпляр класса `Helicone` для работы с API Helicone.
- `client` (OpenAI): Экземпляр класса `OpenAI` для работы с API OpenAI.

**Methods**:

- `generate_poem(prompt: str) -> str`:  Генерирует стихотворение на основе заданного промпта.
- `analyze_sentiment(text: str) -> str`: Анализирует тональность текста.
- `summarize_text(text: str) -> str`: Создает краткое изложение текста.
- `translate_text(text: str, target_language: str) -> str`: Переводит текст на указанный язык.

#### `generate_poem(prompt: str) -> str`

**Purpose**: Генерирует стихотворение на основе заданного промпта.

**Parameters**:

- `prompt` (str): Промпт для генерации стихотворения.

**Returns**:

- `str`: Сгенерированное стихотворение.

**How the Function Works**:
Функция использует модель `gpt-3.5-turbo` из API OpenAI для генерации текста. 
Она формирует сообщение с заданным промптом и отправляет его в API OpenAI. 
Полученный ответ, содержащий сгенерированный текст, логируется с помощью API Helicone, а затем возвращается в качестве результата.

**Examples**:

```python
>>> helicone_ai = HeliconeAI()
>>> poem = helicone_ai.generate_poem("Напиши мне стихотворение про кота.")
>>> print(poem) 
```


#### `analyze_sentiment(text: str) -> str`

**Purpose**: Анализирует тональность текста.

**Parameters**:

- `text` (str): Текст для анализа.

**Returns**:

- `str`: Результат анализа тональности.

**How the Function Works**:
Функция использует модель `text-davinci-003` из API OpenAI для анализа тональности текста. 
Она формирует промпт, включающий текст для анализа, и отправляет его в API OpenAI. 
Полученный ответ, содержащий анализ тональности, логируется с помощью API Helicone, а затем возвращается в качестве результата.

**Examples**:

```python
>>> helicone_ai = HeliconeAI()
>>> sentiment = helicone_ai.analyze_sentiment("Сегодня был отличный день!")
>>> print(sentiment) 
```

#### `summarize_text(text: str) -> str`

**Purpose**: Создает краткое изложение текста.

**Parameters**:

- `text` (str): Текст для изложения.

**Returns**:

- `str`: Краткое изложение текста.

**How the Function Works**:
Функция использует модель `text-davinci-003` из API OpenAI для создания краткого изложения текста. 
Она формирует промпт, включающий текст для изложения, и отправляет его в API OpenAI. 
Полученный ответ, содержащий краткое изложение, логируется с помощью API Helicone, а затем возвращается в качестве результата.

**Examples**:

```python
>>> helicone_ai = HeliconeAI()
>>> summary = helicone_ai.summarize_text("Длинный текст для изложения...")
>>> print(summary) 
```

#### `translate_text(text: str, target_language: str) -> str`

**Purpose**: Переводит текст на указанный язык.

**Parameters**:

- `text` (str): Текст для перевода.
- `target_language` (str): Целевой язык перевода.

**Returns**:

- `str`: Переведенный текст.

**How the Function Works**:
Функция использует модель `text-davinci-003` из API OpenAI для перевода текста. 
Она формирует промпт, включающий текст для перевода и целевой язык, и отправляет его в API OpenAI. 
Полученный ответ, содержащий переведенный текст, логируется с помощью API Helicone, а затем возвращается в качестве результата.

**Examples**:

```python
>>> helicone_ai = HeliconeAI()
>>> translation = helicone_ai.translate_text("Hello, how are you?", "русский")
>>> print(translation)
```

## Функции

### `main`

**Purpose**: Точка входа для запуска основного кода.

**How the Function Works**:
Функция `main` создает экземпляр класса `HeliconeAI` и демонстрирует использование его методов для:

- Генерации стихотворения;
- Анализа тональности;
- Изложения текста;
- Перевода текста.

**Examples**:

```python
>>> if __name__ == "__main__":
>>>    main()
```