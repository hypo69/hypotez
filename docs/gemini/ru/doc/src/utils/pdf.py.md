# Модуль `src.utils.pdf`

## Обзор

Модуль предназначен для преобразования HTML-контента или файлов в PDF с использованием различных библиотек Python. Он предоставляет статические методы класса `PDFUtils` для выполнения этих преобразований, поддерживая такие библиотеки, как `pdfkit`, `FPDF`, `WeasyPrint` и `xhtml2pdf`.

## Подробнее

Модуль предоставляет функциональность для работы с PDF-файлами, позволяя сохранять HTML-контент в PDF различными способами. Он использует несколько библиотек для достижения этой цели, предоставляя гибкость в выборе метода преобразования.

## Классы

### `PDFUtils`

**Описание**: Класс `PDFUtils` предоставляет статические методы для сохранения HTML-контента в PDF с использованием различных библиотек.

**Методы**:

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
```

**Назначение**: Сохраняет HTML-контент или файл в PDF, используя библиотеку `pdfkit`.

**Параметры**:
- `data` (str | Path): HTML-контент в виде строки или путь к HTML-файлу.
- `pdf_file` (str | Path): Путь к сохраняемому PDF-файлу.

**Возвращает**:
- `bool`: `True`, если PDF успешно сохранен, иначе `False`.

**Вызывает исключения**:
- `pdfkit.PDFKitError`: Возникает при ошибке генерации PDF через `pdfkit`.
- `OSError`: Возникает при ошибке доступа к файлу.
- `FileNotFoundError`: Если `wkhtmltopdf.exe` не найден по указанному пути.

**Как работает функция**:
1. Определяет путь к исполняемому файлу `wkhtmltopdf.exe`.
2. Проверяет существование `wkhtmltopdf.exe`. Если файл не найден, логирует ошибку и вызывает исключение `FileNotFoundError`.
3. Настраивает конфигурацию `pdfkit`, указывая путь к `wkhtmltopdf.exe`.
4. Устанавливает опцию `enable-local-file-access` для обеспечения доступа к локальным файлам.
5. Проверяет тип входных данных (`data`):
   - Если `data` является строкой, преобразует HTML-контент в PDF.
   - Если `data` является путем к файлу, преобразует HTML-файл в PDF.
6. Логирует информацию об успешном сохранении PDF-файла.
7. Возвращает `True` в случае успеха.
8. В случае возникновения исключений, логирует ошибку и возвращает `False`.

**Примеры**:

```python
from pathlib import Path

# Пример с HTML-контентом
html_content = "<html><body><h1>Hello, World!</h1></body></html>"
pdf_file_path = "example.pdf"
result = PDFUtils.save_pdf_pdfkit(html_content, pdf_file_path)
print(f"PDF saved successfully: {result}")

# Пример с HTML-файлом
html_file_path = Path("example.html")
html_file_path.write_text("<html><body><h1>Hello, World!</h1></body></html>")
pdf_file_path = "example.pdf"
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
```

**Назначение**: Сохраняет текст в PDF с использованием библиотеки `FPDF`.

**Параметры**:
- `data` (str): Текст, который необходимо сохранить в PDF.
- `pdf_file` (str | Path): Путь к сохраняемому PDF-файлу.

**Возвращает**:
- `bool`: `True`, если PDF успешно сохранен, иначе `False`.

**Вызывает исключения**:
- `FileNotFoundError`: Если JSON-файл со шрифтами или файл шрифта не найден.
- Различные исключения, которые могут возникнуть в процессе работы с `FPDF`.

**Как работает функция**:
1. Импортирует библиотеку `FPDF`.
2. Создает экземпляр класса `FPDF`.
3. Добавляет страницу в PDF-документ.
4. Устанавливает автоматический перенос строк.
5. Определяет путь к файлу `fonts.json`, содержащему информацию о шрифтах.
6. Открывает и загружает JSON-файл со шрифтами. Если файл не найден, логирует ошибку и вызывает исключение `FileNotFoundError`.
7. Добавляет шрифты, указанные в JSON-файле, в PDF-документ. Если файл шрифта не найден, логирует ошибку и вызывает исключение `FileNotFoundError`.
8. Устанавливает шрифт по умолчанию.
9. Добавляет текст в PDF-документ с использованием метода `multi_cell`.
10. Сохраняет PDF-документ в указанный файл.
11. Логирует информацию об успешном сохранении PDF-файла.
12. Возвращает `True` в случае успеха.
13. В случае возникновения исключений, логирует ошибку и возвращает `False`.

**Примеры**:

```python
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
```

**Назначение**: Сохраняет HTML-контент или файл в PDF с использованием библиотеки `WeasyPrint`.

**Параметры**:
- `data` (str | Path): HTML-контент в виде строки или путь к HTML-файлу.
- `pdf_file` (str | Path): Путь к сохраняемому PDF-файлу.

**Возвращает**:
- `bool`: `True`, если PDF успешно сохранен, иначе `False`.

**Вызывает исключения**:
- Различные исключения, которые могут возникнуть в процессе работы с `WeasyPrint`.

**Как работает функция**:
1. Импортирует библиотеку `WeasyPrint`.
2. Проверяет тип входных данных (`data`):
   - Если `data` является строкой, преобразует HTML-контент в PDF.
   - Если `data` является путем к файлу, преобразует HTML-файл в PDF.
3. Логирует информацию об успешном сохранении PDF-файла.
4. Возвращает `True` в случае успеха.
5. В случае возникновения исключений, логирует ошибку и возвращает `False`.

**Примеры**:

```python
from pathlib import Path

# Пример с HTML-контентом
html_content = "<html><body><h1>Hello, World!</h1></body></html>"
pdf_file_path = "example_weasyprint.pdf"
result = PDFUtils.save_pdf_weasyprint(html_content, pdf_file_path)
print(f"PDF saved successfully: {result}")

# Пример с HTML-файлом
html_file_path = Path("example.html")
html_file_path.write_text("<html><body><h1>Hello, World!</h1></body></html>")
pdf_file_path = "example_weasyprint.pdf"
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
```

**Назначение**: Сохраняет HTML-контент или файл в PDF с использованием библиотеки `xhtml2pdf`.

**Параметры**:
- `data` (str | Path): HTML-контент в виде строки или путь к HTML-файлу.
- `pdf_file` (str | Path): Путь к сохраняемому PDF-файлу.

**Возвращает**:
- `bool`: `True`, если PDF успешно сохранен, иначе `False`.

**Вызывает исключения**:
- Различные исключения, которые могут возникнуть в процессе работы с `xhtml2pdf`.

**Как работает функция**:
1. Импортирует библиотеку `xhtml2pdf`.
2. Открывает PDF-файл для записи в бинарном режиме.
3. Проверяет тип входных данных (`data`):
   - Если `data` является строкой, кодирует строку в UTF-8 и создает PDF из HTML-контента.
   - Если `data` является путем к файлу, открывает файл, читает содержимое в кодировке UTF-8 и создает PDF из HTML-файла.
4. Логирует информацию об успешном сохранении PDF-файла.
5. Возвращает `True` в случае успеха.
6. В случае возникновения исключений, логирует ошибку и возвращает `False`.

**Примеры**:

```python
from pathlib import Path

# Пример с HTML-контентом
html_content = "<html><body><h1>Hello, World!</h1></body></html>"
pdf_file_path = "example_xhtml2pdf.pdf"
result = PDFUtils.save_pdf_xhtml2pdf(html_content, pdf_file_path)
print(f"PDF saved successfully: {result}")

# Пример с HTML-файлом
html_file_path = Path("example.html")
html_file_path.write_text("<html><body><h1>Hello, World!</h1></body></html>")
pdf_file_path = "example_xhtml2pdf.pdf"
result = PDFUtils.save_pdf_xhtml2pdf(html_file_path, pdf_file_path)
print(f"PDF saved successfully: {result}")
```

### `html2pdf`

```python
@staticmethod
def html2pdf(html_str: str, pdf_file: str | Path) -> bool | None:
    """Converts HTML content to a PDF file using WeasyPrint."""
```

**Назначение**: Преобразует HTML-контент в PDF-файл, используя библиотеку `WeasyPrint`.

**Параметры**:
- `html_str` (str): HTML-контент в виде строки.
- `pdf_file` (str | Path): Путь к сохраняемому PDF-файлу.

**Возвращает**:
- `bool | None`: `True`, если PDF успешно создан, иначе `None`.

**Вызывает исключения**:
- Различные исключения, которые могут возникнуть в процессе работы с `WeasyPrint`.

**Как работает функция**:
1. Импортирует библиотеку `WeasyPrint`.
2. Преобразует HTML-контент в PDF-файл.
3. Возвращает `True` в случае успеха.
4. В случае возникновения исключений, выводит сообщение об ошибке и возвращает `None`.

**Примеры**:

```python
# Пример преобразования HTML-контента в PDF
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
```

**Назначение**: Конвертирует PDF-файл в HTML-файл.

**Параметры**:
- `pdf_file` (str | Path): Путь к исходному PDF-файлу.
- `html_file` (str | Path): Путь к сохраняемому HTML-файлу.

**Возвращает**:
- `bool`: `True`, если конвертация прошла успешно, иначе `False`.

**Вызывает исключения**:
- Различные исключения, которые могут возникнуть в процессе конвертации PDF в HTML.

**Как работает функция**:
1. Импортирует функцию `extract_text` из библиотеки `pdfminer.high_level`.
2. Извлекает текст из PDF-файла с использованием `extract_text`.
3. Создает HTML-файл и записывает извлеченный текст в формате HTML.
4. Логирует информацию об успешном сохранении HTML-файла.
5. Возвращает `True` в случае успеха.
6. В случае возникновения исключений, выводит сообщение об ошибке и возвращает `False`.

**Примеры**:

```python
from pathlib import Path

# Пример конвертации PDF-файла в HTML-файл
pdf_file_path = Path("example.pdf")  # Укажите путь к существующему PDF-файлу
html_file_path = "example_pdf_to_html.html"
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
```

**Назначение**: Сохраняет данные словаря в PDF-файл.

**Параметры**:
- `data` (Any): Словарь, который нужно преобразовать в PDF.
- `file_path` (str | Path): Путь к выходному PDF-файлу.

**Возвращает**:
- `None`

**Как работает функция**:
1. Проверяет, является ли входной параметр экземпляром `SimpleNamespace`, и, если да, преобразует его в словарь.
2. Создает объект `Canvas` из библиотеки `reportlab` для создания PDF-файла.
3. Устанавливает шрифт и размер шрифта.
4. Перебирает элементы словаря и записывает каждую пару "ключ: значение" в PDF-файл.
5. Если достигнут конец страницы, создает новую страницу.
6. Сохраняет PDF-файл.

**Примеры**:

```python
from pathlib import Path

# Пример сохранения словаря в PDF
data = {"name": "John Doe", "age": 30, "city": "New York"}
pdf_file_path = "example_dict2pdf.pdf"
PDFUtils.dict2pdf(data, pdf_file_path)
print(f"PDF saved successfully: {pdf_file_path}")