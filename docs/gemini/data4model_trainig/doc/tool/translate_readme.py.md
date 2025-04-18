# Модуль для перевода README

## Обзор

Модуль `src.endpoints.gpt4free/etc/tool/translate_readme.py` предназначен для перевода файла README.md на другой язык с использованием g4f API.

## Подробней

Модуль использует API для машинного перевода текста и создает новый файл README с переведенным контентом.

## Переменные

*   `iso` (str): Код языка для перевода (значение: `"GE"`).
*   `language` (str): Название языка для перевода (значение: `"german"`).
*   `translate_prompt` (str): Промпт для перевода документа Markdown.
*   `keep_note` (str): Инструкция для сохранения определенного текста без изменений.
*   `blocklist` (list): Список заголовков, которые не нужно переводить.
*   `allowlist` (list): Список заголовков, которые нужно переводить.

## Функции

### `read_text`

```python
def read_text(text):
```

**Назначение**: Извлекает блок кода Python из текста.

**Параметры**:

*   `text` (str): Текст для извлечения кода.

**Возвращает**:

*   `str`: Извлеченный код.

**Как работает функция**:

1.  Ищет код в блоке markdown с помощью регулярного выражения.
2.  Извлекает содержимое блока кода.

### `translate`

```python
async def translate(text):
```

**Назначение**: Переводит текст с использованием g4f API.

**Параметры**:

*   `text` (str): Текст для перевода.

**Возвращает**:

*   `str`: Переведенный текст.

**Как работает функция**:

1.  Формирует промпт для перевода текста.
2.  Добавляет инструкцию для сохранения определенного текста без изменений (если необходимо).
3.  Использует API g4f для получения переведенного текста.
4.  Возвращает переведенный текст.

### `translate_part`

```python
async def translate_part(part, i):
```

**Назначение**: Переводит часть README-файла.

**Параметры**:

*   `part` (str): Часть текста для перевода.
*   `i` (int): Индекс части.

**Возвращает**:

*   `str`: Переведенная часть текста.

**Как работает функция**:

1.  Проверяет, находится ли текущая часть текста в списке исключений (`blocklist`).
2.  Если текст находится в списке исключений, переводит только заголовок и текст из списка разрешений (`allowlist`).
3.  Если текст не находится в списке исключений, переводит его полностью.
4.  Выводит сообщение о завершении перевода части текста.

### `translate_readme`

```python
async def translate_readme(readme) -> str:
```

**Назначение**: Переводит весь README-файл.

**Параметры**:

*   `readme` (str): Содержимое README-файла.

**Возвращает**:

*   `str`: Полностью переведенный текст README-файла.

**Как работает функция**:

1.  Разбивает текст README-файла на части по заголовкам `## `.
2.  Асинхронно переводит каждую часть текста, используя функцию `translate_part`.
3.  Объединяет переведенные части текста в одну строку.

### `main`

**Как работает функция**:

1.  Читает содержимое файла `README.md`.
2.  Переводит README, используя функцию `translate_readme`.
3.  Сохраняет переведенный текст в файл `README-{iso}.md`.