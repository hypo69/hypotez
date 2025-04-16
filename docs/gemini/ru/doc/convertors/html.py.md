# Модуль для работы с HTML (html.py)

## Обзор

Этот модуль предоставляет утилиты для преобразования HTML-контента в различные форматы, включая escape-последовательности, словари, объекты SimpleNamespace, PDF и DOCX.

## Подробней

Модуль `src.utils.convertors.html` предназначен для обработки HTML-данных. Он предоставляет функции для преобразования HTML в различные представления, что полезно для извлечения, анализа и преобразования HTML-контента.

## Функции

### `html2escape`

**Назначение**: Преобразует HTML в escape-последовательности.

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

**Параметры**:

-   `input_str` (str): HTML-код для преобразования.

**Возвращает**:

-   `str`: HTML, преобразованный в escape-последовательности.

**Как работает функция**:

1.  Использует функцию `StringFormatter.escape_html_tags` для преобразования HTML-тегов в escape-последовательности.

### `escape2html`

**Назначение**: Преобразует escape-последовательности в HTML.

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

**Параметры**:

-   `input_str` (str): Строка с escape-последовательностями.

**Возвращает**:

-   `str`: Escape-последовательности, преобразованные обратно в HTML.

**Как работает функция**:

1.  Использует функцию `StringFormatter.unescape_html_tags` для преобразования escape-последовательностей обратно в HTML-теги.

### `html2dict`

**Назначение**: Преобразует HTML в словарь, где теги являются ключами, а содержимое - значениями.

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

**Параметры**:

-   `html_str` (str): HTML-строка для преобразования.

**Возвращает**:

-   `Dict[str, str]`: Словарь, где ключи - это HTML-теги, а значения - их содержимое.

**Как работает функция**:

1.  Определяет класс `HTMLToDictParser`, который наследует от `HTMLParser`.
2.  В классе `HTMLToDictParser` переопределяет методы `handle_starttag`, `handle_endtag` и `handle_data` для обработки HTML-тегов и содержимого.
3.  Создает экземпляр `HTMLToDictParser` и передает ему HTML-строку для обработки.
4.  Возвращает словарь, полученный в результате парсинга HTML.

### `html2ns`

**Назначение**: Преобразует HTML в объект SimpleNamespace, где теги являются атрибутами, а содержимое - значениями.

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

**Параметры**:

-   `html_str` (str): HTML-строка для преобразования.

**Возвращает**:

-   `SimpleNamespace`: Объект `SimpleNamespace`, где атрибуты - это HTML-теги, а значения - их содержимое.

**Как работает функция**:

1.  Преобразует HTML-строку в словарь, используя функцию `html2dict`.
2.  Создает объект `SimpleNamespace` из полученного словаря.
3.  Возвращает объект `SimpleNamespace`.

### `html2pdf`

**Назначение**: Преобразует HTML-контент в PDF-файл, используя WeasyPrint.

```python
def html2pdf(html_str: str, pdf_file: str | Path) -> bool | None:
    """Converts HTML content to a PDF file using WeasyPrint."""
    ...
```

**Параметры**:

-   `html_str` (str): HTML-контент в виде строки.
-   `pdf_file` (str | Path): Путь для сохранения PDF-файла.

**Возвращает**:

-   `bool | None`: `True` при успешном сохранении, `None` в случае ошибки.

**Как работает функция**:

1.  Импортирует `HTML` из библиотеки `weasyprint`.
2.  Преобразует HTML контент в PDF файл.
3.  Обрабатывает исключения, если возникла ошибка.

### `html_to_docx`

**Назначение**: Преобразует HTML-файл в Word документ, используя LibreOffice.

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

**Параметры**:

-   `html_file` (str): Путь к входному HTML файлу в виде строки.
-   `output_docx` (Path | str): Путь к выходному DOCX файлу.

**Возвращает**:

-   `bool`: `True`, если преобразование прошло успешно, `False` - в противном случае.

**Как работает функция**:

1.  Проверяет, существует ли HTML-файл.
2.  Создает выходную директорию, если она не существует.
3.  Формирует команду для запуска LibreOffice в режиме headless и преобразования HTML в DOCX.
4.  Выполняет команду, используя `subprocess.run`.
5.  Проверяет наличие ошибок в выводе процесса.
6.  Логирует информацию об ошибках и возвращает `True` или `False` в зависимости от результата.

## Переменные модуля

-   В данном модуле отсутствуют переменные, за исключением импортированных библиотек.

## Пример использования

**Преобразование HTML в escape-последовательности:**

```python
from src.utils.convertors import html

html_code = "<p>Hello, world!</p>"
result = html.html2escape(html_code)
print(result)  # Вывод: &lt;p&gt;Hello, world!&lt;/p&gt;
```

**Преобразование HTML в SimpleNamespace:**

```python
from src.utils.convertors import html

html = "<p>Hello</p><a href='link'>World</a>"
result = html.html2ns(html)
print(result.p)
print(result.a)
```

## Взаимосвязь с другими частями проекта

-   Этот модуль использует `src.logger.logger` для логирования ошибок.
-   Он также использует `StringFormatter` (предположительно из другого модуля) для форматирования строк.
-   Модуль может использоваться другими частями проекта `hypotez`, где требуется обработка HTML-контента, например, для извлечения данных из HTML-страниц, преобразования HTML в другие форматы (PDF, DOCX) или для подготовки HTML-контента для отображения в пользовательском интерфейсе.