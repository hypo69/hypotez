# Модуль для работы с PDF-файлами

## Обзор

Модуль `src.utils.pdf` предоставляет инструменты для преобразования HTML-контента или файлов в PDF с использованием различных библиотек. Он включает в себя классы и методы для работы с PDF-файлами, обеспечивая возможность сохранения HTML-контента в PDF и конвертации PDF в HTML.

## Подробнее

Этот модуль предоставляет статические методы для сохранения HTML-контента или файлов в PDF с использованием различных библиотек, таких как `pdfkit`, `FPDF`, `WeasyPrint` и `xhtml2pdf`. Также реализована функция для конвертации PDF-файла в HTML-файл. Модуль использует библиотеку `pdfminer.high_level` для извлечения текста из PDF-файла и сохранения его в HTML-файл.

## Классы

### `PDFUtils`

**Описание**:
Класс `PDFUtils` предоставляет статические методы для работы с PDF-файлами, включая сохранение HTML-контента в PDF с использованием различных библиотек.

**Атрибуты**:
Отсутствуют.

**Методы**:
- `save_pdf_pdfkit(data: str | Path, pdf_file: str | Path) -> bool`: Сохраняет HTML-контент или файл в PDF с использованием библиотеки `pdfkit`.
- `save_pdf_fpdf(data: str, pdf_file: str | Path) -> bool`: Сохраняет текст в PDF с использованием библиотеки `FPDF`.
- `save_pdf_weasyprint(data: str | Path, pdf_file: str | Path) -> bool`: Сохраняет HTML-контент или файл в PDF с использованием библиотеки `WeasyPrint`.
- `save_pdf_xhtml2pdf(data: str | Path, pdf_file: str | Path) -> bool`: Сохраняет HTML-контент или файл в PDF с использованием библиотеки `xhtml2pdf`.
- `html2pdf(html_str: str, pdf_file: str | Path) -> bool | None`: Преобразует HTML-контент в PDF-файл с использованием библиотеки `WeasyPrint`.
- `pdf_to_html(pdf_file: str | Path, html_file: str | Path) -> bool`: Конвертирует PDF-файл в HTML-файл.
- `dict2pdf(data: Any, file_path: str | Path) -> None`: Сохраняет данные словаря в PDF-файл.

## Методы класса

### `save_pdf_pdfkit`

```python
@staticmethod
def save_pdf_pdfkit(data: str | Path, pdf_file: str | Path) -> bool:
    """
    Сохранить HTML-контент или файл в PDF с использованием библиотеки `pdfkit`.

    Args:
        data (str | Path): HTML-контент или путь к HTML-файлу.
        pdf_file (str | Path): Путь к сохраняемому PDF-файлу.

    Returns:
        bool: `True`, если PDF успешно сохранен, иначе `False`.

    Raises:
        pdfkit.PDFKitError: Ошибка генерации PDF через `pdfkit`.
        OSError: Ошибка доступа к файлу.
    """
```

**Назначение**:
Сохраняет HTML-контент или файл в PDF с использованием библиотеки `pdfkit`.

**Параметры**:
- `data` (str | Path): HTML-контент или путь к HTML-файлу.
- `pdf_file` (str | Path): Путь к сохраняемому PDF-файлу.

**Возвращает**:
- `bool`: `True`, если PDF успешно сохранен, иначе `False`.

**Исключения**:
- `pdfkit.PDFKitError`: Возникает при ошибке генерации PDF через `pdfkit`.
- `OSError`: Возникает при ошибке доступа к файлу.

**Как работает**:
1. Определяется путь к исполняемому файлу `wkhtmltopdf.exe`.
2. Проверяется наличие `wkhtmltopdf.exe` по указанному пути. Если файл не найден, регистрируется ошибка и вызывается исключение `FileNotFoundError`.
3. Создается конфигурация для `pdfkit` с указанием пути к `wkhtmltopdf.exe`.
4. Устанавливаются опции, разрешающие доступ к локальным файлам.
5. В зависимости от типа данных (`str` или путь к файлу), вызывается `pdfkit.from_string` или `pdfkit.from_file` для преобразования HTML в PDF.
6. Регистрируется информация об успешном сохранении PDF-файла.
7. В случае возникновения исключений, таких как `pdfkit.PDFKitError` или `OSError`, регистрируется ошибка и возвращается `False`.

**Примеры**:

```python
from pathlib import Path
from src.utils.pdf import PDFUtils

# Пример сохранения HTML-контента в PDF
html_content = "<html><body><h1>Hello, World!</h1></body></html>"
pdf_file = "example.pdf"
result = PDFUtils.save_pdf_pdfkit(html_content, pdf_file)
print(f"PDF сохранен: {result}")

# Пример сохранения HTML-файла в PDF
html_file = Path("example.html")
pdf_file = "example.pdf"
result = PDFUtils.save_pdf_pdfkit(html_file, pdf_file)
print(f"PDF сохранен: {result}")
```

### `save_pdf_fpdf`

```python
@staticmethod
def save_pdf_fpdf(data: str, pdf_file: str | Path) -> bool:
    """
    Сохранить текст в PDF с использованием библиотеки FPDF.

    Args:
        data (str): Текст, который необходимо сохранить в PDF.
        pdf_file (str | Path): Путь к сохраняемому PDF-файлу.

    Returns:
        bool: `True`, если PDF успешно сохранен, иначе `False`.
    """
```

**Назначение**:
Сохраняет текст в PDF с использованием библиотеки FPDF.

**Параметры**:
- `data` (str): Текст, который необходимо сохранить в PDF.
- `pdf_file` (str | Path): Путь к сохраняемому PDF-файлу.

**Возвращает**:
- `bool`: `True`, если PDF успешно сохранен, иначе `False`.

**Как работает**:
1. Импортируется класс `FPDF` из библиотеки `fpdf`.
2. Создается объект `FPDF`.
3. Добавляется новая страница в PDF-документ.
4. Устанавливается автоматический перенос строк.
5. Определяется путь к файлу `fonts.json`, содержащему информацию о шрифтах.
6. Проверяется наличие файла `fonts.json`. Если файл не найден, регистрируется ошибка и вызывается исключение `FileNotFoundError`.
7. Читается информация о шрифтах из файла `fonts.json`.
8. Добавляются шрифты, указанные в файле `fonts.json`, в PDF-документ.
9. Устанавливается шрифт по умолчанию.
10. Добавляется текст в PDF-документ с использованием метода `multi_cell`.
11. Сохраняется PDF-документ в указанный файл.
12. Регистрируется информация об успешном сохранении PDF-файла.
13. В случае возникновения исключений, регистрируется ошибка и возвращается `False`.

**Примеры**:

```python
from pathlib import Path
from src.utils.pdf import PDFUtils

# Пример сохранения текста в PDF
text_data = "Hello, World! This is a test PDF."
pdf_file = "example_fpdf.pdf"
result = PDFUtils.save_pdf_fpdf(text_data, pdf_file)
print(f"PDF сохранен: {result}")
```

### `save_pdf_weasyprint`

```python
@staticmethod
def save_pdf_weasyprint(data: str | Path, pdf_file: str | Path) -> bool:
    """
    Сохранить HTML-контент или файл в PDF с использованием библиотеки `WeasyPrint`.

    Args:
        data (str | Path): HTML-контент или путь к HTML-файлу.
        pdf_file (str | Path): Путь к сохраняемому PDF-файлу.

    Returns:
        bool: `True`, если PDF успешно сохранен, иначе `False`.
    """
```

**Назначение**:
Сохраняет HTML-контент или файл в PDF с использованием библиотеки `WeasyPrint`.

**Параметры**:
- `data` (str | Path): HTML-контент или путь к HTML-файлу.
- `pdf_file` (str | Path): Путь к сохраняемому PDF-файлу.

**Возвращает**:
- `bool`: `True`, если PDF успешно сохранен, иначе `False`.

**Как работает**:
1. Импортируется класс `HTML` из библиотеки `weasyprint`.
2. В зависимости от типа данных (`str` или путь к файлу), вызывается `HTML(string=data).write_pdf(pdf_file)` или `HTML(filename=str(data)).write_pdf(pdf_file)` для преобразования HTML в PDF.
3. Регистрируется информация об успешном сохранении PDF-файла.
4. В случае возникновения исключений, регистрируется ошибка и возвращается `False`.

**Примеры**:

```python
from pathlib import Path
from src.utils.pdf import PDFUtils

# Пример сохранения HTML-контента в PDF
html_content = "<html><body><h1>Hello, World!</h1></body></html>"
pdf_file = "example_weasyprint.pdf"
result = PDFUtils.save_pdf_weasyprint(html_content, pdf_file)
print(f"PDF сохранен: {result}")

# Пример сохранения HTML-файла в PDF
html_file = Path("example.html")
pdf_file = "example_weasyprint.pdf"
result = PDFUtils.save_pdf_weasyprint(html_file, pdf_file)
print(f"PDF сохранен: {result}")
```

### `save_pdf_xhtml2pdf`

```python
@staticmethod
def save_pdf_xhtml2pdf(data: str | Path, pdf_file: str | Path) -> bool:
    """
    Сохранить HTML-контент или файл в PDF с использованием библиотеки `xhtml2pdf`.

    Args:
        data (str | Path): HTML-контент или путь к HTML-файлу.
        pdf_file (str | Path): Путь к сохраняемому PDF-файлу.

    Returns:
        bool: `True`, если PDF успешно сохранен, иначе `False`.
    """
```

**Назначение**:
Сохраняет HTML-контент или файл в PDF с использованием библиотеки `xhtml2pdf`.

**Параметры**:
- `data` (str | Path): HTML-контент или путь к HTML-файлу.
- `pdf_file` (str | Path): Путь к сохраняемому PDF-файлу.

**Возвращает**:
- `bool`: `True`, если PDF успешно сохранен, иначе `False`.

**Как работает**:
1. Импортируется класс `pisa` из библиотеки `xhtml2pdf`.
2. Открывается файл для записи PDF-контента.
3. В зависимости от типа данных (`str` или путь к файлу):
   - Если данные - строка, кодируется в UTF-8.
   - Если данные - путь к файлу, файл открывается для чтения, и его содержимое считывается.
4. Вызывается `pisa.CreatePDF` для преобразования HTML в PDF.
5. Регистрируется информация об успешном сохранении PDF-файла.
6. В случае возникновения исключений, регистрируется ошибка и возвращается `False`.

**Примеры**:

```python
from pathlib import Path
from src.utils.pdf import PDFUtils

# Пример сохранения HTML-контента в PDF
html_content = "<html><body><h1>Hello, World!</h1></body></html>"
pdf_file = "example_xhtml2pdf.pdf"
result = PDFUtils.save_pdf_xhtml2pdf(html_content, pdf_file)
print(f"PDF сохранен: {result}")

# Пример сохранения HTML-файла в PDF
html_file = Path("example.html")
pdf_file = "example_xhtml2pdf.pdf"
result = PDFUtils.save_pdf_xhtml2pdf(html_file, pdf_file)
print(f"PDF сохранен: {result}")
```

### `html2pdf`

```python
@staticmethod
def html2pdf(html_str: str, pdf_file: str | Path) -> bool | None:
    """Converts HTML content to a PDF file using WeasyPrint."""
```

**Назначение**:
Преобразует HTML-контент в PDF-файл с использованием библиотеки `WeasyPrint`.

**Параметры**:
- `html_str` (str): HTML-контент для преобразования.
- `pdf_file` (str | Path): Путь к сохраняемому PDF-файлу.

**Возвращает**:
- `bool | None`: `True`, если преобразование прошло успешно, иначе `None`.

**Как работает**:
1. Импортируется класс `HTML` из библиотеки `weasyprint`.
2. Вызывается `HTML(string=html_str).write_pdf(pdf_file)` для преобразования HTML в PDF.
3. Возвращается `True` в случае успеха.
4. В случае возникновения исключений, регистрируется ошибка и возвращается `None`.

**Примеры**:

```python
from pathlib import Path
from src.utils.pdf import PDFUtils

# Пример сохранения HTML-контента в PDF
html_content = "<html><body><h1>Hello, World!</h1></body></html>"
pdf_file = "example_html2pdf.pdf"
result = PDFUtils.html2pdf(html_content, pdf_file)
print(f"PDF сохранен: {result}")
```

### `pdf_to_html`

```python
@staticmethod
def pdf_to_html(pdf_file: str | Path, html_file: str | Path) -> bool:
    """
    Конвертирует PDF-файл в HTML-файл.

    Args:
        pdf_file (str | Path): Путь к исходному PDF-файлу.
        html_file (str | Path): Путь к сохраняемому HTML-файлу.

    Returns:
        bool: `True`, если конвертация прошла успешно, иначе `False`.
    """
```

**Назначение**:
Конвертирует PDF-файл в HTML-файл.

**Параметры**:
- `pdf_file` (str | Path): Путь к исходному PDF-файлу.
- `html_file` (str | Path): Путь к сохраняемому HTML-файлу.

**Возвращает**:
- `bool`: `True`, если конвертация прошла успешно, иначе `False`.

**Как работает**:
1. Импортируется функция `extract_text` из библиотеки `pdfminer.high_level`.
2. Извлекается текст из PDF-файла с помощью `extract_text`.
3. Создается HTML-файл и записывается извлеченный текст в формате HTML.
4. Регистрируется информация об успешном сохранении HTML-файла.
5. В случае возникновения исключений, регистрируется ошибка и возвращается `False`.

**Примеры**:

```python
from pathlib import Path
from src.utils.pdf import PDFUtils

# Пример конвертации PDF в HTML
pdf_file = "example.pdf"
html_file = "example.html"
result = PDFUtils.pdf_to_html(pdf_file, html_file)
print(f"HTML сохранен: {result}")
```

### `dict2pdf`

```python
@staticmethod
def dict2pdf(data: Any, file_path: str | Path) -> None:
    """
    Save dictionary data to a PDF file.

    Args:
        data (dict | SimpleNamespace): The dictionary to convert to PDF.
        file_path (str | Path): Path to the output PDF file.
    """
```

**Назначение**:
Сохраняет данные словаря в PDF-файл.

**Параметры**:
- `data` (dict | SimpleNamespace): Словарь для преобразования в PDF.
- `file_path` (str | Path): Путь к сохраняемому PDF-файлу.

**Как работает**:
1. Создается объект `Canvas` из библиотеки `reportlab.pdfgen.canvas`.
2. Устанавливается шрифт и размер шрифта.
3. Итерируется по элементам словаря.
4. Для каждого элемента создается строка в формате "ключ: значение".
5. Строка добавляется в PDF-документ.
6. Если достигнут конец страницы, создается новая страница.
7. Сохраняется PDF-документ.

**Примеры**:

```python
from pathlib import Path
from src.utils.pdf import PDFUtils
from reportlab.lib.pagesizes import A4

# Пример сохранения словаря в PDF
data = {"name": "John Doe", "age": 30, "city": "New York"}
pdf_file = "example_dict2pdf.pdf"
PDFUtils.dict2pdf(data, pdf_file)
print(f"PDF сохранен: {pdf_file}")
```