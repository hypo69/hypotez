# Модуль `translator`

## Обзор

Модуль `translator` предназначен для перевода текста с использованием OpenAI API.

## Подробней

Модуль предоставляет функцию `translate`, которая отправляет текст на перевод в OpenAI API и возвращает переведенный текст.

## Функции

### `translate`

```python
def translate(text, source_language, target_language):
    """
    Перевод текста с использованием OpenAI API.

    Этот метод отправляет текст для перевода на указанный язык с помощью модели OpenAI и возвращает переведённый текст.

    Аргументы:
        text (str): Текст для перевода.
        source_language (str): Язык исходного текста.
        target_language (str): Язык для перевода.

    Возвращает:
        str: Переведённый текст.

    Пример использования:
        >>> source_text = "Привет, как дела?"
        >>> source_language = "Russian"
        >>> target_language = "English"
        >>> translation = translate_text(source_text, source_language, target_language)
        >>> print(f"Translated text: {translation}")
    """
    ...
```

**Назначение**: Переводит текст с использованием OpenAI API.

**Параметры**:

*   `text` (str): Текст для перевода.
*   `source_language` (str): Язык исходного текста.
*   `target_language` (str): Язык для перевода.

**Возвращает**:

*   `str`: Переведенный текст.

**Как работает функция**:

1.  Формирует запрос к OpenAI API, включая текст для перевода, исходный язык и целевой язык.
2.  Отправляет запрос к OpenAI API с использованием модели `"text-davinci-003"`.
3.  Извлекает переведенный текст из ответа API.
4.  В случае ошибки логирует ошибку и возвращает `None`.

## Переменные

*   `openai.API_KEY` (str): Ключ API для доступа к OpenAI (должен быть установлен перед использованием функции).

## Зависимости

*   `openai`: Для взаимодействия с OpenAI API.
*   `src.logger.logger`: Для логирования информации о процессе выполнения скрипта.

## Пример

```python
source_text = "Привет, как дела?"
source_language = "Russian"
target_language = "English"
translation = translate_text(source_text, source_language, target_language)
print(f"Translated text: {translation}")
```

## Замечания

*   В данном коде используется конкретная модель OpenAI (`"text-davinci-003"`), которую следует указывать в конфигурационном файле, а не хардкодить.
*   Код предполагает, что переменная `gs.credentials.openai` содержит API-ключ OpenAI.
*   В случае возникновения проблем и/или предложений свяжитесь с разработчиком.
* Обратите внимание на обработку ошибок, и добавление более конкретных исключений в блок try-except, так же можно добавить обертку для повтора попыток.
* Стоит добавить enum, для принимаемых языков

```python
openai.api_key = gs.credentials.openai
```
API key передается в глобальную переменную.
```python
"""#:platform: Windows, Unix
:synopsis: Модуль для перевода текста с использованием OpenAI API."""
```
Данные строки стоит заменить на docstring