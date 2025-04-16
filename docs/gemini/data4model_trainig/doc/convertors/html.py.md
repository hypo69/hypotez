### Анализ кода модуля `hypotez/src/utils/convertors/html.py`

## Обзор

Этот модуль предоставляет утилиты для преобразования HTML-контента в различные форматы, включая экранированные последовательности, словари, объекты SimpleNamespace и документы Word.

## Подробнее

Модуль содержит функции для обработки HTML-данных, такие как экранирование и удаление HTML-тегов, преобразование HTML в различные форматы данных, а также экспорт HTML-контента в DOCX-файлы с использованием LibreOffice.

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
Преобразует HTML в экранированные последовательности.

**Параметры**:
- `input_str` (str): HTML-код.

**Возвращает**:
- `str`: HTML, преобразованный в экранированные последовательности.

**Как работает функция**:

1. Вызывает функцию `StringFormatter.escape_html_tags(input_str)` (предположительно, из другого модуля) для выполнения преобразования.
2. Возвращает результат.

**Примеры**:

```python
html = "<p>Hello, world!</p>"
result = html2escape(html)
print(result)
```

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
Преобразует экранированные последовательности обратно в HTML.

**Параметры**:
- `input_str` (str): Строка с экранированными последовательностями.

**Возвращает**:
- `str`: Экранированные последовательности, преобразованные обратно в HTML.

**Как работает функция**:

1.  Вызывает функцию `StringFormatter.unescape_html_tags(input_str)` (предположительно, из другого модуля) для выполнения преобразования.
2.  Возвращает результат.

**Примеры**:

```python
escaped = "&lt;p&gt;Hello, world!&lt;/p&gt;"
result = escape2html(escaped)
print(result)
```

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
Преобразует HTML в словарь, где теги являются ключами, а содержимое - значениями.

**Параметры**:
- `html_str` (str): HTML-строка для преобразования.

**Возвращает**:
- `dict`: Словарь с HTML-тегами в качестве ключей и их содержимым в качестве значений.

**Как работает функция**:
1. Определяет внутренний класс `HTMLToDictParser`, наследующий от `html.parser.HTMLParser`.
2.  `HTMLToDictParser` использует методы `handle_starttag` и `handle_data` для извлечения тегов и их содержимого из HTML.
3.  Создает экземпляр парсера `HTMLToDictParser`.
4.  Передает HTML-строку в парсер с помощью `parser.feed(html_str)`.
5.  Возвращает словарь `parser.result`, содержащий теги и их содержимое.

**Примеры**:

```python
html = "<p>Hello</p><a href='link'>World</a>"
result = html2dict(html)
print(result)
```

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
Преобразует HTML в объект `SimpleNamespace`, где теги являются атрибутами, а содержимое - значениями.

**Параметры**:
- `html_str` (str): HTML-строка для преобразования.

**Возвращает**:
- `SimpleNamespace`: Объект `SimpleNamespace` с HTML-тегами в качестве атрибутов и их содержимым в качестве значений.

**Как работает функция**:
1. Преобразует HTML-строку в словарь с помощью `html2dict`.
2. Создает объект `SimpleNamespace` из словаря.
3. Возвращает объект `SimpleNamespace`.

**Примеры**:

```python
html = "<p>Hello</p><a href='link'>World</a>"
result = html2ns(html)
print(result.p)
print(result.a)
```

### `html2pdf`

```python
def html2pdf(html_str: str, pdf_file: str | Path) -> bool | None:
    """Converts HTML content to a PDF file using WeasyPrint."""
    ...
```

**Назначение**:
Преобразует HTML-контент в PDF-файл, используя WeasyPrint.

**Параметры**:
- `html_str` (str): HTML-контент для преобразования.
- `pdf_file` (str | Path): Путь к сохраняемому PDF-файлу.

**Возвращает**:
- `bool | None`: `True`, если преобразование прошло успешно, `None` в противном случае.

**Как работает функция**:

1. Использует библиотеку `weasyprint` для преобразования HTML в PDF.
2. В случае успеха возвращает True, иначе None.
3. Печатает сообщение об ошибке в случае возникновения исключения.

**Примеры**:

```python
html_content = "<html><body><h1>Hello, PDF!</h1></body></html>"
pdf_file = "output.pdf"
success = html2pdf(html_content, pdf_file)
print(f"PDF saved successfully: {success}")
```

### `html_to_docx`

```python
def html_to_docx(html_file: str, output_docx: Path | str) -> bool:
    """Converts an HTML file to a Word document using LibreOffice.

    Args:
        html_file (str): Path to the input HTML file as a string.
        output_docx (Path | str): Path to the output DOCX file.

    Returns:
        bool: True if conversion is successful, False otherwise.
    """
    ...
```

**Назначение**:
Преобразует HTML-файл в документ Word, используя LibreOffice.

**Параметры**:
- `html_file` (str): Путь к входному HTML-файлу в виде строки.
- `output_docx` (Path | str): Путь к выходному DOCX-файлу.

**Возвращает**:
- `bool`: True, если преобразование прошло успешно, False в противном случае.

**Как работает функция**:

1. Проверяет существование HTML-файла.
2. Создает выходную директорию, если она не существует.
3. Формирует команду для запуска LibreOffice в режиме headless.
4. Выполняет команду LibreOffice с использованием `subprocess.run`.
5. Проверяет наличие ошибок в выводе процесса LibreOffice.

**Примеры**:

```python
html_file = "input.html"
output_docx = "output.docx"
success = html_to_docx(html_file, output_docx)
print(f"DOCX saved successfully: {success}")
```

## Переменные

Отсутствуют

## Запуск

Для использования этого модуля необходимо установить библиотеки `beautifulsoup4`, `WeasyPrint`, `xhtml2pdf`, `html5lib` и LibreOffice.

```bash
pip install beautifulsoup4 WeasyPrint xhtml2pdf html5lib
```

Для работы с `html_to_docx` необходимо установить LibreOffice и добавить путь к исполняемому файлу в системную переменную PATH.

Пример использования:

```python
from src.utils.convertors import html2escape, escape2html, html2dict, html2ns, html2pdf, html_to_docx
from pathlib import Path

# Преобразование HTML в экранированные последовательности
html_text = "<p>Hello, world!</p>"
escaped_text = html2escape(html_text)
print(escaped_text)

# Преобразование экранированных последовательностей в HTML
unescaped_text = escape2html(escaped_text)
print(unescaped_text)

# Преобразование HTML в словарь
html_data = "<p>Hello</p><a href='link'>World</a>"
data = html2dict(html_data)
print(data)

# Преобразование HTML в SimpleNamespace
html_data = "<p>Hello</p><a href='link'>World</a>"
ns = html2ns(html_data)
print(ns.p)

# Преобразование HTML в PDF
html_content = "<html><body><h1>Hello, PDF!</h1></body></html>"
pdf_file = "output.pdf"
success = html2pdf(html_content, pdf_file)
print(f"PDF saved successfully: {success}")

# Преобразование HTML в DOCX
html_file = "input.html"
output_docx = "output.docx"
success = html_to_docx(html_file, output_docx)
print(f"DOCX saved successfully: {success}")