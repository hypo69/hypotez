# Модуль `src.utils.pdf`

## Обзор

Модуль предназначен для преобразования HTML-контента или файлов в формат PDF с использованием различных библиотек. Он предоставляет статические методы класса `PDFUtils` для выполнения этой задачи.

## Подробнее

Модуль содержит класс `PDFUtils`, который предоставляет методы для сохранения HTML-контента в PDF с использованием различных библиотек, таких как `pdfkit`, `FPDF`, `WeasyPrint` и `xhtml2pdf`. Также модуль содержит функции для конвертации PDF в HTML и словаря в PDF.

## Классы

### `PDFUtils`

Описание: Класс предоставляет статические методы для работы с PDF-файлами, включая сохранение HTML-контента в PDF и конвертацию PDF в HTML.

**Методы:**

- `save_pdf_pdfkit(data: str | Path, pdf_file: str | Path) -> bool`
- `save_pdf_fpdf(data: str, pdf_file: str | Path) -> bool`
- `save_pdf_weasyprint(data: str | Path, pdf_file: str | Path) -> bool`
- `save_pdf_xhtml2pdf(data: str | Path, pdf_file: str | Path) -> bool`
- `html2pdf(html_str: str, pdf_file: str | Path) -> bool | None`
- `pdf_to_html(pdf_file: str | Path, html_file: str | Path) -> bool`
- `dict2pdf(data: Any, file_path: str | Path) -> None`

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
        bool: `True` если PDF успешно сохранен, иначе `False`.

    Raises:
        pdfkit.PDFKitError: Ошибка генерации PDF через `pdfkit`.
        OSError: Ошибка доступа к файлу.
    """
    ...
```

**Назначение**: Сохраняет HTML-контент или HTML-файл в PDF-файл с использованием библиотеки `pdfkit`.

**Параметры**:

- `data` (str | Path): HTML-контент в виде строки или путь к HTML-файлу.
- `pdf_file` (str | Path): Путь к PDF-файлу, в который нужно сохранить данные.

**Возвращает**:

- `bool`: `True`, если PDF успешно сохранен, `False` в противном случае.

**Вызывает исключения**:

- `FileNotFoundError`: Если не найден исполняемый файл `wkhtmltopdf.exe`.
- `pdfkit.PDFKitError`: Если происходит ошибка во время генерации PDF.
- `OSError`: Если происходит ошибка при доступе к файлу.
- `Exception`: Для всех остальных неожиданных ошибок.

**Как работает функция**:
1. Определяется путь к исполняемому файлу `wkhtmltopdf.exe`.
2. Проверяется наличие `wkhtmltopdf.exe` по указанному пути. Если файл не найден, генерируется исключение `FileNotFoundError`.
3. Формируется конфигурация для `pdfkit` с указанием пути к исполняемому файлу `wkhtmltopdf.exe`.
4. Устанавливается опция `enable-local-file-access` для обеспечения доступа к локальным файлам.
5. В зависимости от типа данных (`str` или `Path`) вызывается соответствующая функция `pdfkit` (`from_string` для HTML-контента или `from_file` для HTML-файла) для генерации PDF.
6. В случае успеха возвращается `True`, при возникновении ошибки логируется сообщение об ошибке и возвращается `False`.

**Примеры**:

```python
from pathlib import Path
from src.utils.pdf import PDFUtils

# Пример сохранения HTML-контента в PDF
html_content = "<html><body><h1>Hello, World!</h1></body></html>"
pdf_file_path = "example.pdf"
result = PDFUtils.save_pdf_pdfkit(html_content, pdf_file_path)
print(f"PDF saved successfully: {result}")

# Пример сохранения HTML-файла в PDF
html_file_path = Path("example.html")
with open(html_file_path, "w", encoding="utf-8") as f:
    f.write("<html><body><h1>Hello, World!</h1></body></html>")
pdf_file_path = "example_from_file.pdf"
result = PDFUtils.save_pdf_pdfkit(html_file_path, pdf_file_path)
print(f"PDF saved successfully: {result}")
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
    ...
```

**Назначение**: Сохраняет текст в PDF-файл с использованием библиотеки `FPDF`.

**Параметры**:

- `data` (str): Текст, который необходимо сохранить в PDF.
- `pdf_file` (str | Path): Путь к PDF-файлу, в который нужно сохранить данные.

**Возвращает**:

- `bool`: `True`, если PDF успешно сохранен, `False` в противном случае.

**Вызывает исключения**:

- `FileNotFoundError`: Если не найден файл шрифтов `fonts.json` или какой-либо из файлов шрифтов, указанных в `fonts.json`.
- `Exception`: Если происходит ошибка во время сохранения PDF.

**Как работает функция**:

1. Импортирует класс `FPDF` из библиотеки `fpdf`.
2. Создает экземпляр класса `FPDF`.
3. Добавляет страницу в PDF-документ.
4. Устанавливает автоматический перенос текста и отступ от края страницы.
5. Определяет путь к файлу `fonts.json`, содержащему информацию о шрифтах.
6. Открывает и загружает данные из файла `fonts.json`.
7. Добавляет шрифты, указанные в файле `fonts.json`, в PDF-документ.
8. Устанавливает шрифт по умолчанию.
9. Добавляет текст в PDF-документ с использованием метода `multi_cell`.
10. Сохраняет PDF-документ в указанный файл.
11. В случае успеха возвращает `True`, при возникновении ошибки логируется сообщение об ошибке и возвращается `False`.

**Примеры**:

```python
from src.utils.pdf import PDFUtils

# Пример сохранения текста в PDF
text_data = "Hello, World! This is a test PDF generated with FPDF."
pdf_file_path = "example_fpdf.pdf"
result = PDFUtils.save_pdf_fpdf(text_data, pdf_file_path)
print(f"PDF saved successfully: {result}")
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
        bool: `True` если PDF успешно сохранен, иначе `False`.
    """
    ...
```

**Назначение**: Сохраняет HTML-контент или HTML-файл в PDF-файл с использованием библиотеки `WeasyPrint`.

**Параметры**:

- `data` (str | Path): HTML-контент в виде строки или путь к HTML-файлу.
- `pdf_file` (str | Path): Путь к PDF-файлу, в который нужно сохранить данные.

**Возвращает**:

- `bool`: `True`, если PDF успешно сохранен, `False` в противном случае.

**Вызывает исключения**:

- `Exception`: Если происходит ошибка во время сохранения PDF.

**Как работает функция**:

1. Импортирует класс `HTML` из библиотеки `weasyprint`.
2. В зависимости от типа данных (`str` или `Path`) создает объект `HTML` либо из HTML-контента (строки), либо из HTML-файла.
3. Сохраняет PDF-документ в указанный файл с использованием метода `write_pdf`.
4. В случае успеха возвращает `True`, при возникновении ошибки логируется сообщение об ошибке и возвращается `False`.

**Примеры**:

```python
from pathlib import Path
from src.utils.pdf import PDFUtils

# Пример сохранения HTML-контента в PDF
html_content = "<html><body><h1>Hello, World!</h1></body></html>"
pdf_file_path = "example_weasyprint.pdf"
result = PDFUtils.save_pdf_weasyprint(html_content, pdf_file_path)
print(f"PDF saved successfully: {result}")

# Пример сохранения HTML-файла в PDF
html_file_path = Path("example.html")
with open(html_file_path, "w", encoding="utf-8") as f:
    f.write("<html><body><h1>Hello, World!</h1></body></html>")
pdf_file_path = "example_weasyprint_from_file.pdf"
result = PDFUtils.save_pdf_weasyprint(html_file_path, pdf_file_path)
print(f"PDF saved successfully: {result}")
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
        bool: `True` если PDF успешно сохранен, иначе `False`.
    """
    ...
```

**Назначение**: Сохраняет HTML-контент или HTML-файл в PDF-файл с использованием библиотеки `xhtml2pdf`.

**Параметры**:

- `data` (str | Path): HTML-контент в виде строки или путь к HTML-файлу.
- `pdf_file` (str | Path): Путь к PDF-файлу, в который нужно сохранить данные.

**Возвращает**:

- `bool`: `True`, если PDF успешно сохранен, `False` в противном случае.

**Вызывает исключения**:

- `Exception`: Если происходит ошибка во время сохранения PDF.

**Как работает функция**:

1. Импортирует модуль `pisa` из библиотеки `xhtml2pdf`.
2. Открывает PDF-файл для записи в бинарном режиме.
3. В зависимости от типа данных (`str` или `Path`) создает PDF из HTML-контента (строки) или из HTML-файла.
4. Для HTML-контента (строки) кодирует строку в UTF-8 и создает PDF с использованием `pisa.CreatePDF`.
5. Для HTML-файла открывает файл, читает его содержимое и создает PDF с использованием `pisa.CreatePDF`.
6. В случае успеха возвращает `True`, при возникновении ошибки логируется сообщение об ошибке и возвращается `False`.

**Примеры**:

```python
from pathlib import Path
from src.utils.pdf import PDFUtils

# Пример сохранения HTML-контента в PDF
html_content = "<html><body><h1>Hello, World!</h1></body></html>"
pdf_file_path = "example_xhtml2pdf.pdf"
result = PDFUtils.save_pdf_xhtml2pdf(html_content, pdf_file_path)
print(f"PDF saved successfully: {result}")

# Пример сохранения HTML-файла в PDF
html_file_path = Path("example.html")
with open(html_file_path, "w", encoding="utf-8") as f:
    f.write("<html><body><h1>Hello, World!</h1></body></html>")
pdf_file_path = "example_xhtml2pdf_from_file.pdf"
result = PDFUtils.save_pdf_xhtml2pdf(html_file_path, pdf_file_path)
print(f"PDF saved successfully: {result}")
```

### `html2pdf`

```python
@staticmethod
def html2pdf(html_str: str, pdf_file: str | Path) -> bool | None:
    """Converts HTML content to a PDF file using WeasyPrint."""
    ...
```

**Назначение**: Преобразует HTML-контент в PDF-файл с использованием библиотеки `WeasyPrint`.

**Параметры**:

- `html_str` (str): HTML-контент в виде строки.
- `pdf_file` (str | Path): Путь к PDF-файлу, в который нужно сохранить данные.

**Возвращает**:

- `bool | None`: `True`, если PDF успешно сохранен, `None` в случае ошибки.

**Вызывает исключения**:

- Отсутствуют явные исключения, но функция может вызывать исключения, связанные с `WeasyPrint`.

**Как работает функция**:

1. Импортирует класс `HTML` из библиотеки `weasyprint`.
2. Создает объект `HTML` из HTML-контента (строки).
3. Сохраняет PDF-документ в указанный файл с использованием метода `write_pdf`.
4. В случае успеха возвращает `True`, при возникновении ошибки выводит сообщение об ошибке и возвращает `None`.

**Примеры**:

```python
from src.utils.pdf import PDFUtils

# Пример сохранения HTML-контента в PDF
html_content = "<html><body><h1>Hello, World!</h1></body></html>"
pdf_file_path = "example_html2pdf.pdf"
result = PDFUtils.html2pdf(html_content, pdf_file_path)
print(f"PDF saved successfully: {result}")
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
    ...
```

**Назначение**: Конвертирует PDF-файл в HTML-файл.

**Параметры**:

- `pdf_file` (str | Path): Путь к исходному PDF-файлу.
- `html_file` (str | Path): Путь к сохраняемому HTML-файлу.

**Возвращает**:

- `bool`: `True`, если конвертация прошла успешно, иначе `False`.

**Вызывает исключения**:

- Отсутствуют явные исключения, но функция может вызывать исключения, связанные с `pdfminer`.

**Как работает функция**:

1. Импортирует функцию `extract_text` из модуля `pdfminer.high_level`.
2. Извлекает текст из PDF-файла с использованием `extract_text`.
3. Создает HTML-файл и записывает извлеченный текст в формате HTML.
4. В случае успеха возвращает `True`, при возникновении ошибки выводит сообщение об ошибке и возвращает `False`.

**Примеры**:

```python
from pathlib import Path
from src.utils.pdf import PDFUtils

# Пример конвертации PDF в HTML
pdf_file_path = Path("example.pdf")  # Убедитесь, что файл существует
html_file_path = "example.html"
result = PDFUtils.pdf_to_html(pdf_file_path, html_file_path)
print(f"HTML saved successfully: {result}")
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
    ...
```

**Назначение**: Сохраняет данные словаря в PDF-файл.

**Параметры**:

- `data` (Any): Словарь, который нужно преобразовать в PDF.
- `file_path` (str | Path): Путь к PDF-файлу, в который нужно сохранить данные.

**Возвращает**:

- `None`

**Вызывает исключения**:

- Отсутствуют явные исключения, но функция может вызывать исключения, связанные с `reportlab`.

**Как работает функция**:

1. Проверяет, является ли `data` экземпляром `SimpleNamespace`, и если да, преобразует его в словарь.
2. Создает объект `Canvas` из библиотеки `reportlab.pdfgen.canvas` для создания PDF-документа.
3. Устанавливает шрифт и размер шрифта.
4. Перебирает элементы словаря и записывает каждую пару "ключ: значение" в PDF-документ.
5. Если места на странице недостаточно, создает новую страницу.
6. Сохраняет PDF-документ в указанный файл.

**Примеры**:

```python
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Функция для конвертации словаря в PDF
from src.utils.pdf import PDFUtils

# Пример сохранения словаря в PDF
data = {"name": "Alice", "age": 30, "city": "New York"}
pdf_file_path = "example_dict2pdf.pdf"
PDFUtils.dict2pdf(data, pdf_file_path)
print(f"PDF saved successfully: {pdf_file_path}")
```