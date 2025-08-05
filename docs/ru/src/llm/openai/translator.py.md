# Модуль для перевода текста с использованием OpenAI API.

## Обзор

Модуль предназначен для перевода текста с одного языка на другой с использованием API OpenAI. Он предоставляет функцию `translate`, которая принимает текст, язык оригинала и язык перевода в качестве аргументов, а затем возвращает переведенный текст.

## Подробней

Модуль использует библиотеку `openai` для взаимодействия с API OpenAI. Ключ API OpenAI должен быть установлен в переменной `openai.api_key`.
Функция `translate` формирует запрос к API OpenAI, указывая модель для перевода, текст для перевода, а также языки оригинала и перевода. Затем она отправляет запрос к API и извлекает переведенный текст из ответа.

## Функции

### `translate`

**Назначение**: Перевод текста с использованием OpenAI API.

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
```

**Параметры**:

*   `text` (str): Текст для перевода.
*   `source_language` (str): Язык исходного текста.
*   `target_language` (str): Язык для перевода.

**Возвращает**:

*   `str`: Переведенный текст.

**Вызывает исключения**:

*   `Exception`: Возникает в случае ошибки при обращении к OpenAI API.

**Как работает функция**:

1.  Формируется запрос к OpenAI API, включающий текст для перевода и указание языков оригинала и перевода.
2.  Запрос отправляется к OpenAI API с использованием модели `text-davinci-003`.
3.  Извлекается переведенный текст из ответа API.
4.  В случае возникновения ошибки, информация об ошибке логируется с помощью `logger.error`.

**Примеры**:

```python
source_text = "Привет, как дела?"
source_language = "Russian"
target_language = "English"
translation = translate(source_text, source_language, target_language)
print(f"Translated text: {translation}")