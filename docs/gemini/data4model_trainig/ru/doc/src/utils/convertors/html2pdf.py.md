# Модуль для конвертации HTML

## Обзор

Модуль `html2pdf.py` предоставляет набор утилит для конвертации HTML в различные форматы, включая экранированные последовательности, словари, объекты SimpleNamespace и PDF. Он включает функции для экранирования и деэкранирования HTML-тегов, преобразования HTML в словари и объекты, а также для генерации PDF-файлов из HTML.

## Подробней

Этот модуль предназначен для обработки HTML-контента, предоставляя удобные способы преобразования и анализа HTML-данных. Он использует стандартные библиотеки Python, такие как `html.parser` и `types`, а также сторонние библиотеки, такие как `xhtml2pdf` и `weasyprint`, для расширения функциональности.

## Классы

В данном модуле определен внутренний класс `HTMLToDictParser`, который используется для преобразования HTML в словарь.

### `HTMLToDictParser`

**Описание**: Класс `HTMLToDictParser` используется для парсинга HTML-строки и преобразования ее в словарь, где ключами являются теги HTML, а значениями - их содержимое.

**Наследует**: `HTMLParser`

**Атрибуты**:

-   `result` (dict): Словарь, хранящий результаты парсинга HTML.
-   `current_tag` (str | None): Текущий обрабатываемый тег HTML.

**Методы**:

-   `handle_starttag(self, tag, attrs)`: Обрабатывает начало тега HTML, устанавливая текущий тег.
-   `handle_endtag(self, tag)`: Обрабатывает конец тега HTML, сбрасывая текущий тег.
-   `handle_data(self, data)`: Обрабатывает данные внутри тега HTML, добавляя их в словарь результатов.

#### `handle_starttag`

```python
def handle_starttag(self, tag, attrs):
    """
    Обрабатывает начало тега HTML, устанавливая текущий тег.

    Args:
        tag (str): Тег HTML.
        attrs (list): Список атрибутов тега.
    """
    ...
```

#### `handle_endtag`

```python
def handle_endtag(self, tag):
    """
    Обрабатывает конец тега HTML, сбрасывая текущий тег.

    Args:
        tag (str): Тег HTML.
    """
    ...
```

#### `handle_data`

```python
def handle_data(self, data):
    """
    Обрабатывает данные внутри тега HTML, добавляя их в словарь результатов.

    Args:
        data (str): Данные внутри тега HTML.
    """
    ...
```

## Функции

### `html2escape`

```python
def html2escape(input_str: str) -> str:
    """
    Преобразует HTML в экранированные последовательности.

    Args:
        input_str (str): HTML-код.

    Returns:
        str: HTML, преобразованный в экранированные последовательности.

    Example:
        >>> html = "<p>Hello, world!</p>"
        >>> result = html2escape(html)
        >>> print(result)
        &lt;p&gt;Hello, world!&lt;/p&gt;
    """
    ...
```

**Как работает функция**:
Функция `html2escape` принимает строку HTML-кода и преобразует ее в экранированные последовательности, заменяя специальные символы HTML (например, `<`, `>`, `&`) на их соответствующие escape-последовательности (например, `&lt;`, `&gt;`, `&amp;`). Это полезно для предотвращения интерпретации HTML-кода браузером или другими обработчиками HTML. Внутри функция вызывает метод `StringFormatter.escape_html_tags(input_str)`, который и выполняет преобразование.

**Примеры**:

```python
html = "<p>Hello, world!</p>"
result = html2escape(html)
print(result)
# Вывод: &lt;p&gt;Hello, world!&lt;/p&gt;
```

### `escape2html`

```python
def escape2html(input_str: str) -> str:
    """
    Преобразует экранированные последовательности в HTML.

    Args:
        input_str (str): Строка с экранированными последовательностями.

    Returns:
        str: Экранированные последовательности, преобразованные обратно в HTML.

    Example:
        >>> escaped = "&lt;p&gt;Hello, world!&lt;/p&gt;"
        >>> result = escape2html(escaped)
        >>> print(result)
        <p>Hello, world!</p>
    """
    ...
```

**Как работает функция**:
Функция `escape2html` принимает строку с экранированными последовательностями и преобразует ее обратно в HTML, заменяя escape-последовательности (например, `&lt;`, `&gt;`, `&amp;`) на их соответствующие специальные символы HTML (например, `<`, `>`, `&`). Это позволяет восстановить исходный HTML-код из его экранированной версии. Внутри функция вызывает метод `StringFormatter.unescape_html_tags(input_str)`, который и выполняет преобразование.

**Примеры**:

```python
escaped = "&lt;p&gt;Hello, world!&lt;/p&gt;"
result = escape2html(escaped)
print(result)
# Вывод: <p>Hello, world!</p>
```

### `html2dict`

```python
def html2dict(html_str: str) -> Dict[str, str]:
    """
    Преобразует HTML в словарь, где теги являются ключами, а содержимое - значениями.

    Args:
        html_str (str): HTML-строка для преобразования.

    Returns:
        dict: Словарь с HTML-тегами в качестве ключей и их содержимым в качестве значений.

    Example:
        >>> html = "<p>Hello</p><a href='link'>World</a>"
        >>> result = html2dict(html)
        >>> print(result)
        {'p': 'Hello', 'a': 'World'}
    """
    ...
```

**Как работает функция**:
Функция `html2dict` принимает HTML-строку и преобразует ее в словарь, где ключами являются HTML-теги, а значениями - их содержимое. Для этого используется класс `HTMLToDictParser`, который наследует `HTMLParser` из модуля `html.parser`. `HTMLToDictParser` переопределяет методы `handle_starttag`, `handle_endtag` и `handle_data` для извлечения тегов и их содержимого. Функция создает экземпляр парсера, передает ему HTML-строку и возвращает полученный словарь.

**Примеры**:

```python
html = "<p>Hello</p><a href='link'>World</a>"
result = html2dict(html)
print(result)
# Вывод: {'p': 'Hello', 'a': 'World'}
```

### `html2ns`

```python
def html2ns(html_str: str) -> SimpleNamespace:
    """
    Преобразует HTML в объект SimpleNamespace, где теги являются атрибутами, а содержимое - значениями.

    Args:
        html_str (str): HTML-строка для преобразования.

    Returns:
        SimpleNamespace: Объект SimpleNamespace с HTML-тегами в качестве атрибутов и их содержимым в качестве значений.

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

**Как работает функция**:
Функция `html2ns` принимает HTML-строку и преобразует ее в объект `SimpleNamespace`, где теги HTML становятся атрибутами объекта, а их содержимое - значениями атрибутов. Сначала функция вызывает `html2dict` для преобразования HTML в словарь, а затем использует этот словарь для создания объекта `SimpleNamespace` с помощью оператора `**`.

**Примеры**:

```python
html = "<p>Hello</p><a href='link'>World</a>"
result = html2ns(html)
print(result.p)
# Вывод: Hello
print(result.a)
# Вывод: World
```

### `html2pdf`

```python
def html2pdf(html_str: str, pdf_file: str | Path) -> bool | None:
    """Converts HTML content to a PDF file using WeasyPrint."""
    try:
        HTML(string=html_str).write_pdf(pdf_file)
        return True
    except Exception as e:
        print(f"Error during PDF generation: {e}")
        return
```

**Как работает функция**:
Функция `html2pdf` принимает HTML-строку и путь к PDF-файлу и преобразует HTML-контент в PDF-файл, используя библиотеку `weasyprint`. Она оборачивает процесс преобразования в блок `try...except`, чтобы обработать возможные исключения, которые могут возникнуть в процессе генерации PDF. В случае успеха функция возвращает `True`, в случае ошибки - выводит сообщение об ошибке и возвращает `None`.

**Примеры**:

```python
html_string = "<p>Hello, world!</p>"
pdf_filepath = "output.pdf"
result = html2pdf(html_string, pdf_filepath)
if result:
    print("PDF generated successfully!")
else:
    print("PDF generation failed.")