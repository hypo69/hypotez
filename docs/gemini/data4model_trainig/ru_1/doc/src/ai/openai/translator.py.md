# Модуль для перевода текста с использованием OpenAI API

## Обзор

Модуль предназначен для перевода текста с одного языка на другой, используя API OpenAI. Он предоставляет функцию `translate`, которая принимает текст, исходный и целевой языки в качестве аргументов и возвращает переведенный текст.

## Подробнее

Этот модуль позволяет интегрировать функции перевода текста в ваши приложения, используя возможности OpenAI. Он обрабатывает запросы к API OpenAI, извлекает переведенный текст из ответов и обрабатывает возможные ошибки.

## Функции

### `translate`

**Назначение**: Перевод текста с использованием OpenAI API.

**Параметры**:
- `text` (str): Текст для перевода.
- `source_language` (str): Язык исходного текста.
- `target_language` (str): Язык для перевода.

**Возвращает**:
- `str`: Переведенный текст.

**Вызывает исключения**:
- `Exception`: Возникает в случае ошибки при обращении к OpenAI API.

**Как работает функция**:

1.  Формирует запрос к OpenAI API, включающий текст для перевода, исходный язык и целевой язык.
2.  Отправляет запрос к OpenAI API с использованием указанной модели (`text-davinci-003`).
3.  Извлекает переведенный текст из ответа API.
4.  Возвращает переведенный текст.
5.  В случае возникновения ошибки при обращении к API, логирует ошибку с помощью `logger.error` и возвращает `None`.

**Примеры**:

```python
from src.ai.openai.translator import translate
from src import gs
# Перед использованием необходимо установить ключ API OpenAI
gs.credentials.openai = "sk-ваш_ключ"

source_text = "Привет, как дела?"
source_language = "Russian"
target_language = "English"
translation = translate(source_text, source_language, target_language)
print(f"Translated text: {translation}")  # Вывод: Translated text: Hello, how are you?
```
```python
from src.ai.openai.translator import translate
from src import gs
gs.credentials.openai = "sk-ваш_ключ"

source_text = "This is a test."
source_language = "English"
target_language = "German"
translation = translate(source_text, source_language, target_language)
print(f"Translated text: {translation}") # Вывод: Translated text: Dies ist ein Test.
```
```python
from src.ai.openai.translator import translate
from src import gs
gs.credentials.openai = "sk-ваш_ключ"

source_text = "Это пример текста для перевода."
source_language = "Russian"
target_language = "French"
translation = translate(source_text, source_language, target_language)
print(f"Translated text: {translation}") # Вывод: Translated text: Ceci est un exemple de texte à traduire.
```
```python
from src.ai.openai.translator import translate
from src import gs
gs.credentials.openai = "sk-ваш_ключ"

source_text = "你好世界"
source_language = "Chinese"
target_language = "English"
translation = translate(source_text, source_language, target_language)
print(f"Translated text: {translation}") # Вывод: Translated text: Hello World