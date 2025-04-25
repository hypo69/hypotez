# Модуль для перевода текста с использованием OpenAI API

## Обзор

Модуль `src.ai.openai.translator` предоставляет функцию `translate` для перевода текста с использованием OpenAI API. 

## Подробнее

Функция `translate` отправляет текст для перевода на указанный язык с помощью модели OpenAI и возвращает переведённый текст. 

## Функции

### `translate`

**Назначение**: Функция переводит текст с использованием OpenAI API.

**Параметры**:
- `text` (str): Текст для перевода.
- `source_language` (str): Язык исходного текста.
- `target_language` (str): Язык для перевода.

**Возвращает**:
- `str`: Переведённый текст.

**Вызывает исключения**:
- `Exception`: Если возникает ошибка во время перевода.

**Как работает функция**:
- Функция `translate` формирует запрос к OpenAI API, используя заданный текст, исходный язык и язык перевода.
- Она отправляет этот запрос к OpenAI API с помощью `openai.Completion.create`.
- Извлекает перевод из ответа API и возвращает его.

**Примеры**:
```python
>>> source_text = "Привет, как дела?"
>>> source_language = "Russian"
>>> target_language = "English"
>>> translation = translate(source_text, source_language, target_language)
>>> print(f"Translated text: {translation}")
Translated text: Hello, how are you?
```

**Внутренние функции**:
- Внутри функции `translate` нет внутренних функций.

**Пример использования**:
```python
from src.ai.openai.translator import translate

source_text = "Привет, как дела?"
source_language = "Russian"
target_language = "English"

translation = translate(source_text, source_language, target_language)

print(f"Translated text: {translation}")
```