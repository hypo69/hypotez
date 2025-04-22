# Модуль `html`

## Обзор

Модуль `html` предоставляет утилиты для конвертации HTML в различные форматы данных и обратно.
Он включает функции для экранирования и деэкранирования HTML-тегов, преобразования HTML в словари и объекты `SimpleNamespace`, а также для конвертации HTML в PDF и DOCX форматы.

## Подробнее

Модуль содержит функции для выполнения следующих операций:

- Преобразование HTML в escape-последовательности и обратно.
- Преобразование HTML в словари, где теги являются ключами, а содержимое - значениями.
- Преобразование HTML в объекты `SimpleNamespace`, где теги являются атрибутами, а содержимое - значениями.
- Конвертация HTML в PDF с использованием библиотеки `WeasyPrint` или `xhtml2pdf`.
- Конвертация HTML-файлов в документы Word (`.docx`) с использованием LibreOffice.

## Классы

В данном модуле используются следующие классы:
- `HTMLParser` из библиотеки `html.parser` (внутренний класс `HTMLToDictParser`).

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
    return StringFormatter.escape_html_tags(input_str)
```

**Назначение**: Преобразует HTML-код в escape-последовательности.

**Параметры**:
- `input_str` (str): HTML-код, который необходимо преобразовать.

**Возвращает**:
- `str`: HTML, преобразованный в escape-последовательности.

**Как работает функция**:
- Функция вызывает метод `escape_html_tags` класса `StringFormatter` для преобразования HTML-кода в escape-последовательности.

**Примеры**:

```python
html = "<p>Hello, world!</p>"
result = html2escape(html)
print(result)  # Вывод: &lt;p&gt;Hello, world!&lt;/p&gt;
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
    return StringFormatter.unescape_html_tags(input_str)
```

**Назначение**: Преобразует escape-последовательности обратно в HTML-код.

**Параметры**:
- `input_str` (str): Строка с escape-последовательностями.

**Возвращает**:
- `str`: HTML-код, полученный из escape-последовательностей.

**Как работает функция**:
- Функция вызывает метод `unescape_html_tags` класса `StringFormatter` для преобразования escape-последовательностей в HTML-код.

**Примеры**:

```python
escaped = "&lt;p&gt;Hello, world!&lt;/p&gt;"
result = escape2html(escaped)
print(result)  # Вывод: <p>Hello, world!</p>
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
    class HTMLToDictParser(HTMLParser):
        """
        Внутренний класс, наследующий HTMLParser, для преобразования HTML в словарь.
        Inherits:
            HTMLParser: Базовый класс для парсинга HTML.

        Attributes:
            result (dict): Словарь, содержащий результаты парсинга HTML.
            current_tag (str): Текущий обрабатываемый тег.

        Methods:
            handle_starttag(tag, attrs): Обрабатывает начальный тег HTML.
            handle_endtag(tag): Обрабатывает конечный тег HTML.
            handle_data(data): Обрабатывает данные между тегами HTML.
        """
        def __init__(self):
            super().__init__()
            self.result = {}
            self.current_tag = None

        def handle_starttag(self, tag, attrs):
            """
            Обрабатывает начальный тег HTML.
            Args:
                tag (str): Имя начального тега.
                attrs (list): Список атрибутов тега.
            """
            self.current_tag = tag

        def handle_endtag(self, tag):
            """
            Обрабатывает конечный тег HTML.
            Args:
                tag (str): Имя конечного тега.
            """
            self.current_tag = None

        def handle_data(self, data):
            """
            Обрабатывает данные между тегами HTML.
            Args:
                data (str): Данные между тегами.
            """
            if self.current_tag:
                self.result[self.current_tag] = data.strip()

    parser = HTMLToDictParser()
    parser.feed(html_str)
    return parser.result
```

**Назначение**: Преобразует HTML-код в словарь, где ключами являются теги, а значениями - их содержимое.

**Параметры**:
- `html_str` (str): HTML-код для преобразования.

**Возвращает**:
- `dict`: Словарь, где теги являются ключами, а их содержимое - значениями.

**Внутренние функции**:
- `HTMLToDictParser`: Внутренний класс, наследующий `HTMLParser`, для парсинга HTML и создания словаря.
    - `__init__`: Конструктор класса, инициализирует словарь `result` и переменную `current_tag`.
    - `handle_starttag(tag, attrs)`: Метод, вызываемый при обнаружении начального тега. Устанавливает `current_tag` равным имени тега.
    - `handle_endtag(tag)`: Метод, вызываемый при обнаружении конечного тега. Сбрасывает `current_tag` в `None`.
    - `handle_data(data)`: Метод, вызываемый при обнаружении данных между тегами. Если `current_tag` установлен, добавляет данные в словарь `result` с ключом `current_tag`.

**Как работает функция**:
1. Определяется внутренний класс `HTMLToDictParser`, наследующий `HTMLParser`.
2. Создается экземпляр `HTMLToDictParser`.
3. Вызывается метод `feed` парсера с HTML-кодом.
4. Возвращается словарь `result` из парсера.

**Примеры**:

```python
html = "<p>Hello</p><a href='link'>World</a>"
result = html2dict(html)
print(result)  # Вывод: {'p': 'Hello', 'a': 'World'}
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
    html_dict = html2dict(html_str)
    return SimpleNamespace(**html_dict)
```

**Назначение**: Преобразует HTML-код в объект `SimpleNamespace`, где теги становятся атрибутами, а их содержимое - значениями.

**Параметры**:
- `html_str` (str): HTML-код для преобразования.

**Возвращает**:
- `SimpleNamespace`: Объект `SimpleNamespace` с тегами в качестве атрибутов и их содержимым в качестве значений.

**Как работает функция**:
1. Вызывает функцию `html2dict` для преобразования HTML-кода в словарь.
2. Создает объект `SimpleNamespace` из словаря, используя оператор `**`, который распаковывает словарь в именованные аргументы.

**Примеры**:

```python
html = "<p>Hello</p><a href='link'>World</a>"
result = html2ns(html)
print(result.p)  # Вывод: Hello
print(result.a)  # Вывод: World
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

**Назначение**: Преобразует HTML-код в PDF-файл с использованием библиотеки `WeasyPrint`.

**Параметры**:
- `html_str` (str): HTML-код для преобразования.
- `pdf_file` (str | Path): Путь к выходному PDF-файлу.

**Возвращает**:
- `bool | None`: `True`, если PDF-файл успешно создан, `None` в случае ошибки.

**Как работает функция**:
1. Пытается создать PDF-файл из HTML-кода, используя библиотеку `WeasyPrint`.
2. В случае успеха возвращает `True`.
3. В случае ошибки логирует ошибку и возвращает `None`.

**Примеры**:

```python
html = "<p>Hello, world!</p>"
pdf_file = "output.pdf"
result = html2pdf(html, pdf_file)
if result:
    print("PDF file created successfully.")
else:
    print("PDF file creation failed.")
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
    try:
        # Ensure the html_file exists
        if not os.path.exists(html_file):
            logger.error(f"HTML file not found: {html_file}")
            return False

        # Ensure output directory exists
        output_dir = Path(output_docx).parent
        if not output_dir.exists():
            os.makedirs(output_dir)

        # Construct the command for LibreOffice
        command = [
            "soffice",
            "--headless",  # Run LibreOffice in headless mode
            "--convert-to",
            "docx:HTML", # Specify that input is HTML
            html_file, # use html_file as is
            "--outdir",
            str(output_dir)
        ]

        # Execute the LibreOffice command
        process = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True
        )

        # Check for any errors outputted in the process output
        if process.stderr:
           logger.error(f"LibreOffice conversion errors: {process.stderr}")

        return True

    except subprocess.CalledProcessError as ex:
        logger.error(f"LibreOffice failed to convert HTML file: {html_file} to DOCX file: {output_docx}. Error: {ex.stderr}", exc_info=True)
        return False
    except FileNotFoundError:
        logger.error(f"LibreOffice executable (soffice) not found. Ensure it is installed and in your system's PATH.", exc_info=True)
        return False
    except Exception as ex:
        logger.error(f"An unexpected error occurred during conversion. Error: {ex}", exc_info=True)
        return False
```

**Назначение**: Преобразует HTML-файл в документ Word (`.docx`) с использованием LibreOffice.

**Параметры**:
- `html_file` (str): Путь к входному HTML-файлу.
- `output_docx` (Path | str): Путь к выходному DOCX-файлу.

**Возвращает**:
- `bool`: `True`, если преобразование выполнено успешно, `False` в противном случае.

**Как работает функция**:
1. Проверяет существование входного HTML-файла. Если файл не найден, функция логирует ошибку и возвращает `False`.
2. Проверяет существование выходного каталога. Если каталог не существует, он создается.
3. Формирует команду для запуска LibreOffice в режиме командной строки для преобразования HTML-файла в DOCX.
4. Запускает процесс LibreOffice с использованием `subprocess.run`.
5. Проверяет наличие ошибок в выводе процесса LibreOffice. Если ошибки обнаружены, функция логирует их.
6. В случае успеха возвращает `True`.
7. В случае возникновения исключений `subprocess.CalledProcessError`, `FileNotFoundError` или других исключений, функция логирует соответствующие ошибки и возвращает `False`.

**Вызывает исключения**:
- `subprocess.CalledProcessError`: Если LibreOffice возвращает ошибку при конвертации.
- `FileNotFoundError`: Если исполняемый файл LibreOffice (`soffice`) не найден.
- `Exception`: При возникновении любой другой непредвиденной ошибки.

**Примеры**:

```python
html_file = "input.html"
output_docx = "output.docx"
result = html_to_docx(html_file, output_docx)
if result:
    print("HTML file converted to DOCX successfully.")
else:
    print("HTML file conversion to DOCX failed.")
```