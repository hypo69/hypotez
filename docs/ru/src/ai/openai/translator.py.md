# Модуль `translator`

## Обзор

Модуль `translator` предназначен для перевода текста с использованием OpenAI API. Он содержит функцию `translate`, которая принимает текст, исходный язык и целевой язык в качестве аргументов и возвращает переведенный текст.

## Подробней

Этот модуль предоставляет возможность автоматического перевода текста между различными языками, используя возможности OpenAI. Функция `translate` отправляет запрос к OpenAI API, получает переведенный текст и возвращает его.

## Функции

### `translate`

```python
def translate(text: str, source_language: str, target_language: str) -> str:
    """
    Перевод текста с использованием OpenAI API.

    Этот метод отправляет текст для перевода на указанный язык с помощью модели OpenAI и возвращает переведённый текст.

    Args:
        text (str): Текст для перевода.
        source_language (str): Язык исходного текста.
        target_language (str): Язык для перевода.

    Returns:
        str: Переведённый текст.

    Raises:
        Exception: Если происходит ошибка во время запроса к OpenAI API.

    Example:
        >>> source_text = "Привет, как дела?"
        >>> source_language = "Russian"
        >>> target_language = "English"
        >>> translation = translate(source_text, source_language, target_language)
        >>> print(f"Translated text: {translation}")
    """
```

**Назначение**: Перевод текста с одного языка на другой с использованием OpenAI API.

**Параметры**:
- `text` (str): Текст, который необходимо перевести.
- `source_language` (str): Язык, с которого нужно перевести текст.
- `target_language` (str): Язык, на который нужно перевести текст.

**Возвращает**:
- `str`: Переведенный текст.

**Вызывает исключения**:
- `Exception`: Возникает, если во время выполнения запроса к OpenAI API происходит ошибка.

**Как работает функция**:

1. **Формирование запроса**: Функция формирует запрос к OpenAI API, включая исходный текст, язык оригинала и язык перевода.
2. **Отправка запроса**: Запрос отправляется к OpenAI API для получения перевода. Используется модель `text-davinci-003`.
3. **Извлечение перевода**: Из ответа API извлекается переведенный текст.
4. **Обработка ошибок**: Если во время выполнения запроса происходит ошибка, она логируется, и функция возвращает `None`.

```
A: Формирование запроса к OpenAI
|
B: Отправка запроса к OpenAI API
|
C: Извлечение перевода из ответа API
|
D: Обработка ошибок
```

**Примеры**:

```python
source_text = "Привет, как дела?"
source_language = "Russian"
target_language = "English"
translation = translate(source_text, source_language, target_language)
print(f"Translated text: {translation}")

source_text = "This is a test."
source_language = "English"
target_language = "French"
translation = translate(source_text, source_language, target_language)
print(f"Translated text: {translation}")