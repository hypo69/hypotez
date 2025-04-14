# Модуль `md2dict`

## Обзор

Модуль `md2dict` предназначен для конвертации строк в формате Markdown в структурированный словарь. Он также включает в себя функциональность для извлечения JSON содержимого, если оно присутствует в Markdown строке.

## Подробней

Модуль предоставляет функции для преобразования Markdown в HTML и структурированный словарь. Он использует библиотеку `markdown2` для конвертации Markdown в HTML, а затем анализирует HTML структуру для создания словаря, где ключами являются заголовки разделов, а значениями — список содержимого в этих разделах. Этот модуль полезен для автоматической обработки и анализа Markdown документов.

## Функции

### `md2html`

```python
def md2html(md_string: str, extras: List[str] = None) -> str:
    """
    Конвертирует строку Markdown в HTML.

    Args:
        md_string (str): Строка Markdown для конвертации.
        extras (list, optional): Список расширений markdown2. Defaults to None.

    Returns:
        str: HTML-представление Markdown.
    """
    ...
```

**Назначение**: Конвертирует строку в формате Markdown в HTML.

**Параметры**:
- `md_string` (str): Строка Markdown, которую необходимо конвертировать.
- `extras` (List[str], optional): Список расширений для библиотеки `markdown2`. По умолчанию `None`.

**Возвращает**:
- `str`: HTML-представление входной Markdown строки.

**Вызывает исключения**:
- `Exception`: Логируется ошибка, если происходит исключение в процессе преобразования Markdown в HTML.

**Как работает функция**:
Функция принимает Markdown строку и, при необходимости, список расширений для `markdown2`. Затем она пытается конвертировать строку в HTML с использованием библиотеки `markdown2`. В случае возникновения ошибки, она логирует её и возвращает пустую строку.

**Примеры**:

```python
from src.utils.convertors.md import md2html
markdown_text = "# Hello, world!"
html_output = md2html(markdown_text)
print(html_output)  # doctest: +SKIP
# <h1>Hello, world!</h1>
```

### `md2dict`

```python
def md2dict(md_string: str, extras: List[str] = None) -> Dict[str, list[str]]:
    """
    Конвертирует строку Markdown в структурированный словарь.

    Args:
        md_string (str): Строка Markdown для конвертации.
        extras (list, optional): Список расширений markdown2 для md2html. Defaults to None.

    Returns:
         Dict[str, list[str]]: Структурированное представление Markdown содержимого.
    """
    ...
```

**Назначение**: Конвертирует строку Markdown в структурированный словарь, где ключами являются заголовки разделов, а значениями — список содержимого в этих разделах.

**Параметры**:
- `md_string` (str): Строка Markdown, которую необходимо конвертировать.
- `extras` (List[str], optional): Список расширений для библиотеки `markdown2`, используемый функцией `md2html`. По умолчанию `None`.

**Возвращает**:
- `Dict[str, list[str]]`: Структурированное представление Markdown содержимого в виде словаря.

**Вызывает исключения**:
- `Exception`: Логируется ошибка, если происходит исключение в процессе парсинга Markdown в структурированный словарь.

**Как работает функция**:
Функция сначала преобразует Markdown в HTML с помощью функции `md2html`. Затем она разделяет HTML на строки и анализирует их для определения заголовков разделов и содержимого. Заголовки первого уровня (`<h1>`) используются в качестве ключей словаря, а остальное содержимое добавляется в список значений для соответствующего ключа.

**Примеры**:

```python
from src.utils.convertors.md import md2dict

markdown_text = """
# Section 1
Content for section 1.
## Section 2
Content for section 2.
More content for section 2.
"""
result = md2dict(markdown_text)
print(result) # doctest: +SKIP
# {'Section 1': ['Content for section 1.', 'Section 2', 'Content for section 2.', 'More content for section 2.']}