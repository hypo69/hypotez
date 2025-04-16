### Анализ кода `hypotez/src/utils/convertors/html.py.md`

## Обзор

Модуль предоставляет утилиты для работы с HTML-контентом, включая преобразование в escape-последовательности, словари и объекты SimpleNamespace.

## Подробнее

Этот модуль содержит функции для обработки HTML-данных, такие как преобразование HTML в escape-последовательности и обратно, извлечение данных в виде словаря, а также преобразование HTML-кода в объект SimpleNamespace. Кроме того, модуль предоставляет функции для конвертации HTML в PDF.

## Функции

### `html2escape`

```python
def html2escape(input_str: str) -> str:
    """
    Convert HTML to escape sequences.

    Args:
        input_str (str): The HTML code.

    Returns:
        str: HTML converted into escape sequences.

    Example:
        >>> html = "<p>Hello, world!</p>"
        >>> result = html2escape(html)
        >>> print(result)
        &lt;p&gt;Hello, world!&lt;/p&gt;
    """
    ...
```

**Назначение**:
Преобразует HTML в escape-последовательности.

**Параметры**:

*   `input_str` (str): HTML-код.

**Возвращает**:

*   `str`: HTML, преобразованный в escape-последовательности.

**Как работает функция**:

1.  Вызывает метод `escape_html_tags` из класса `StringFormatter` (код которого не предоставлен) для выполнения преобразования.

### `escape2html`

```python
def escape2html(input_str: str) -> str:
    """
    Convert escape sequences to HTML.

    Args:
        input_str (str): The string with escape sequences.

    Returns:
        str: The escape sequences converted back into HTML.

    Example:
        >>> escaped = "&lt;p&gt;Hello, world!&lt;/p&gt;"
        >>> result = escape2html(escaped)
        >>> print(result)
        <p>Hello, world!</p>
    """
    ...
```

**Назначение**:
Преобразует escape-последовательности в HTML.

**Параметры**:

*   `input_str` (str): Строка с escape-последовательностями.

**Возвращает**:

*   `str`: Строка с преобразованными escape-последовательностями в HTML.

**Как работает функция**:

1.  Вызывает метод `unescape_html_tags` из класса `StringFormatter` (код которого не предоставлен) для выполнения преобразования.

### `html2dict`

```python
def html2dict(html_str: str) -> Dict[str, str]:
    """
    Convert HTML to a dictionary where tags are keys and content are values.

    Args:
        html_str (str): The HTML string to convert.

    Returns:
        dict: A dictionary with HTML tags as keys and their content as values.

    Example:
        >>> html = "<p>Hello</p><a href='link'>World</a>"
        >>> result = html2dict(html)
        >>> print(result)
        {'p': 'Hello', 'a': 'World'}
    """
    ...
```

**Назначение**:
Преобразует HTML в словарь, где теги являются ключами, а содержимое — значениями.

**Параметры**:

*   `html_str` (str): HTML-строка для преобразования.

**Возвращает**:

*   `dict`: Словарь с HTML-тегами в качестве ключей и их содержимым в качестве значений.

**Как работает функция**:

1.  Определяет внутренний класс `HTMLToDictParser`, который наследуется от `HTMLParser.HTMLParser`.
2.  В классе `HTMLToDictParser` переопределяются методы `handle_starttag`, `handle_endtag` и `handle_data` для извлечения тегов и данных из HTML.
3.  Создает экземпляр `HTMLToDictParser` и передает ему HTML-строку для обработки.
4.  Возвращает словарь `result`, сформированный парсером.

### `html2ns`

```python
def html2ns(html_str: str) -> SimpleNamespace:
    """
    Convert HTML to a SimpleNamespace object where tags are attributes and content are values.

    Args:
        html_str (str): The HTML string to convert.

    Returns:
        SimpleNamespace: A SimpleNamespace object with HTML tags as attributes and their content as values.

    Example:
        >>> html = "<p>Hello</p><a href='link'>World</a>"
        >>> result = html2ns(html)
        >>> print(result.p)
        Hello
        >>> print(result.a)
        World
    """
    ...
```

**Назначение**:
Преобразует HTML в объект `SimpleNamespace`, где теги являются атрибутами, а содержимое — значениями.

**Параметры**:

*   `html_str` (str): HTML-строка для преобразования.

**Возвращает**:

*   `SimpleNamespace`: Объект `SimpleNamespace` с HTML-тегами в качестве атрибутов и их содержимым в качестве значений.

**Как работает функция**:

1.  Преобразует HTML-строку в словарь с помощью функции `html2dict`.
2.  Создает объект `SimpleNamespace` на основе полученного словаря.

### `html2pdf`

```python
def html2pdf(html_str: str, pdf_file: str | Path) -> bool | None:
    """Converts HTML content to a PDF file using WeasyPrint."""
    ...
```

**Назначение**:
Преобразует HTML-контент в PDF-файл с использованием библиотеки WeasyPrint.

**Параметры**:

*   `html_str` (str): HTML-контент для преобразования.
*   `pdf_file` (str | Path): Путь к сохраняемому PDF-файлу.

**Возвращает**:

*   `bool | None`: `True`, если преобразование прошло успешно, `None` в противном случае.

**Как работает функция**:

1.  Импортирует `HTML` из библиотеки `weasyprint`.
2.  Использует `HTML(string=html_str).write_pdf(pdf_file)` для преобразования HTML в PDF и сохранения его в указанный файл.
3.  В случае успеха возвращает `True`.
4.  При возникновении ошибки возвращает `None`.

## Константы

Отсутствуют.

## Примеры использования

```python
from src.utils.convertors.html import html2escape, escape2html, html2dict, html2ns

# Преобразование HTML в escape-последовательности
html = "<p>Hello, world!</p>"
escaped_html = html2escape(html)
print(escaped_html)

# Преобразование escape-последовательностей в HTML
escaped = "&lt;p&gt;Hello, world!&lt;/p&gt;"
unescaped_html = escape2html(escaped)
print(unescaped_html)

# Преобразование HTML в словарь
html = "<p>Hello</p><a href='link'>World</a>"
html_dict = html2dict(html)
print(html_dict)

# Преобразование HTML в SimpleNamespace
html = "<p>Hello</p><a href='link'>World</a>"
html_ns = html2ns(html)
print(html_ns.p)
print(html_ns.a)
```

## Зависимости

*   `re`: Для работы с регулярными выражениями.
*   `typing.Dict`: Для аннотаций типов.
*   `pathlib.Path`: Для работы с путями к файлам.
*   `src.logger.logger`: Для логирования.
*   `types.SimpleNamespace`: Для создания объектов `SimpleNamespace`.
*   `html.parser.HTMLParser`: Для парсинга HTML.
*   `xhtml2pdf`: Для преобразования HTML в PDF.
*   `weasyprint`: Для преобразования HTML в PDF.

## Взаимосвязи с другими частями проекта

Модуль `html.py` предоставляет утилиты для работы с HTML-контентом и может использоваться в различных частях проекта `hypotez`, где требуется обработка HTML, например, для извлечения данных из веб-страниц, создания отчетов в формате HTML или преобразования HTML в другие форматы (например, PDF). Он зависит от модуля логирования