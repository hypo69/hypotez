# Модуль для перевода текста с использованием OpenAI API

## Обзор

Модуль `translator` предоставляет функцию `translate` для перевода текста с использованием API OpenAI.

## Детали

Модуль импортирует следующие библиотеки:

- `openai`: для взаимодействия с API OpenAI.
- `gs`: для доступа к конфигурационным данным.
- `logger`: для записи логов.

Функция `translate` выполняет перевод текста с помощью модели OpenAI `text-davinci-003`. 

## Функции

### `translate(text, source_language, target_language)`

**Описание**: Переводит текст с использованием OpenAI API.

**Аргументы**:

- `text` (str): Текст для перевода.
- `source_language` (str): Язык исходного текста.
- `target_language` (str): Язык для перевода.

**Возвращает**:

- `str`: Переведённый текст.

**Пример использования**:

```python
>>> source_text = "Привет, как дела?"
>>> source_language = "Russian"
>>> target_language = "English"
>>> translation = translate(source_text, source_language, target_language)
>>> print(f"Translated text: {translation}")
```

**Как работает функция**:

1. Формирует запрос к API OpenAI, включая текст для перевода, исходный язык и язык для перевода.
2. Отправляет запрос к API OpenAI с использованием модели `text-davinci-003`.
3. Извлекает перевод из ответа API.
4. Возвращает переведённый текст.

**Обработка ошибок**:

В случае ошибки при вызове API OpenAI записывает ошибку в лог.