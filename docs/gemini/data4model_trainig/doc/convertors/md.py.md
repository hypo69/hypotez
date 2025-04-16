### Анализ кода модуля `hypotez/src/utils/convertors/md2dict.py`

## Обзор

Этот модуль предназначен для конвертации строки Markdown в структурированный словарь, включая извлечение JSON содержимого, если оно присутствует.

## Подробнее

Модуль содержит функции для преобразования Markdown в HTML и структурированные словари.

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

**Назначение**:
Конвертирует строку Markdown в HTML.

**Параметры**:
- `md_string` (str): Строка Markdown для конвертации.
- `extras` (list[str], optional): Список расширений markdown2. Defaults to None.

**Возвращает**:
- `str`: HTML-представление Markdown.

**Как работает функция**:
1.  Использует функцию `markdown` из библиотеки `markdown2` для преобразования строки Markdown в HTML.
2.  В случае ошибки логирует информацию об ошибке и возвращает пустую строку.

**Примеры**:

```python
from src.utils.convertors.md2dict import md2html

md_string = "# Hello, world!"
html_output = md2html(md_string)
print(html_output)  # Вывод: <h1>Hello, world!</h1>
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

**Назначение**:
Конвертирует строку Markdown в структурированный словарь.

**Параметры**:
- `md_string` (str): Строка Markdown для конвертации.
- `extras` (List[str], optional): Список расширений `markdown2` для `md2html`. Defaults to `None`.

**Возвращает**:
- `Dict[str, list[str]]`: Структурированное представление содержимого Markdown.

**Как работает функция**:

1. Использует функцию `md2html` для преобразования строки Markdown в HTML.
2. Разделяет HTML-код на строки.
3. Перебирает строки HTML-кода и определяет заголовки и контент.
4. Если строка начинается с тега `<h`, извлекает уровень заголовка и текст заголовка.
5. Если строка является текстом и находится внутри секции, добавляет текст в список строк для текущей секции.
6.  Возвращает словарь, где ключи - заголовки, а значения - списки содержимого секций.

**Примеры**:

```python
from src.utils.convertors import md2dict

md_string = """
# Section 1
Content 1

## Section 2
Content 2
"""
result = md2dict(md_string)
print(result)
```

## Переменные

Отсутствуют