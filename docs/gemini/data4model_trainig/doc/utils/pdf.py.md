### Анализ кода модуля `hypotez/src/utils/pdf.py`

## Обзор

Этот модуль предоставляет утилиты для преобразования HTML-контента или файлов в PDF с использованием различных библиотек.

## Подробнее

Модуль предоставляет набор статических методов класса `PDFUtils` для генерации PDF из HTML-контента или HTML-файлов, а также для конвертации PDF в HTML и сохранения данных из словаря в PDF. Используются библиотеки `pdfkit`, `FPDF`, `WeasyPrint` и `xhtml2pdf`.

## Классы

### `PDFUtils`

```python
class PDFUtils:
    """
    Класс для работы с PDF-файлами, предоставляющий методы для сохранения HTML-контента в PDF с использованием различных библиотек.
    """
```

**Описание**:
Класс `PDFUtils` предоставляет статические методы для работы с PDF-файлами.

**Атрибуты**:
- Нет

**Методы**:
- `save_pdf_pdfkit(data: str | Path, pdf_file: str | Path) -> bool`: Сохраняет HTML-контент или файл в PDF с использованием библиотеки `pdfkit`.
- `save_pdf_fpdf(data: str, pdf_file: str | Path) -> bool`: Сохраняет текст в PDF с использованием библиотеки FPDF.
- `save_pdf_weasyprint(data: str | Path, pdf_file: str | Path) -> bool`: Сохраняет HTML-контент или файл в PDF с использованием библиотеки `WeasyPrint`.
- `save_pdf_xhtml2pdf(data: str | Path, pdf_file: str | Path) -> bool`: Сохраняет HTML-контент или файл в PDF с использованием библиотеки `xhtml2pdf`.
- `html2pdf(html_str: str, pdf_file: str | Path) -> bool | None`: Конвертирует HTML-контент в PDF-файл, используя WeasyPrint.
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
        bool: `True` если PDF успешно сохранен, иначе `False`.

    Raises:
        pdfkit.PDFKitError: Ошибка генерации PDF через `pdfkit`.
        OSError: Ошибка доступа к файлу.
    """
    ...
```

**Назначение**:
Сохраняет HTML-контент или файл в PDF с использованием библиотеки `pdfkit`.

**Параметры**:
- `data` (str | Path): HTML-контент или путь к HTML-файлу.
- `pdf_file` (str | Path): Путь к сохраняемому PDF-файлу.

**Возвращает**:
- `bool`: `True`, если PDF успешно сохранен, иначе `False`.

**Как работает функция**:

1. Определяет путь к исполняемому файлу `wkhtmltopdf.exe`.
2. Конфигурирует `pdfkit` для использования указанного исполняемого файла.
3. Определяет параметры для доступа к локальным файлам.
4. Преобразует HTML-контент или HTML-файл в PDF, используя `pdfkit.from_string` или `pdfkit.from_file`.
5. Логирует информацию об успешном сохранении PDF-файла.
6. Перехватывает возможные исключения, логирует ошибки и возвращает `False`.

**Примеры**:

```python
html_content = "<html><body><h1>Hello, PDF!</h1></body></html>"
pdf_file = "output.pdf"
success = PDFUtils.save_pdf_pdfkit(html_content, pdf_file)
print(f"PDF saved successfully: {success}")
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

**Назначение**:
Сохраняет текст в PDF с использованием библиотеки FPDF.

**Параметры**:
- `data` (str): Текст, который необходимо сохранить в PDF.
- `pdf_file` (str | Path): Путь к сохраняемому PDF-файлу.

**Возвращает**:
- `bool`: `True`, если PDF успешно сохранен, иначе `False`.

**Как работает функция**:

1.  Создает объект `FPDF`.
2.  Добавляет страницу в PDF-документ.
3.  Устанавливает автоматический перенос страниц и отступы.
4.  Загружает информацию о шрифтах из JSON-файла.
5.  Добавляет шрифты в PDF-документ.
6.  Устанавливает шрифт по умолчанию.
7.  Добавляет текст в PDF-документ.
8.  Сохраняет PDF-документ в файл.
9.  В случае возникновения ошибок логирует информацию об ошибке и возвращает `False`.

**Примеры**:

```python
text_data = "Hello, PDF!"
pdf_file = "output.pdf"
success = PDFUtils.save_pdf_fpdf(text_data, pdf_file)
print(f"PDF saved successfully: {success}")
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

**Назначение**:
Сохраняет HTML-контент или файл в PDF с использованием библиотеки `WeasyPrint`.

**Параметры**:
- `data` (str | Path): HTML-контент или путь к HTML-файлу.
- `pdf_file` (str | Path): Путь к сохраняемому PDF-файлу.

**Возвращает**:
- `bool`: `True`, если PDF успешно сохранен, иначе `False`.

**Как работает функция**:
1. Проверяет, является ли `data` строкой или путем к файлу.
2. Использует `weasyprint.HTML` для создания PDF из строки или файла.
3. Логирует информацию об успешном сохранении PDF-файла.
4. В случае возникновения ошибок логирует информацию об ошибке и возвращает `False`.

**Примеры**:

```python
html_content = "<html><body><h1>Hello, PDF!</h1></body></html>"
pdf_file = "output.pdf"
success = PDFUtils.save_pdf_weasyprint(html_content, pdf_file)
print(f"PDF saved successfully: {success}")
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

**Назначение**:
Сохраняет HTML-контент или файл в PDF с использованием библиотеки `xhtml2pdf`.

**Параметры**:
- `data` (str | Path): HTML-контент или путь к HTML-файлу.
- `pdf_file` (str | Path): Путь к сохраняемому PDF-файлу.

**Возвращает**:
- `bool`: `True`, если PDF успешно сохранен, иначе `False`.

**Как работает функция**:
1. Проверяет, является ли `data` строкой или путем к файлу.
2. В зависимости от типа `data`:
    - Если `data` - строка, то преобразует ее в кодировку UTF-8 и передает в функцию `pisa.CreatePDF` для генерации PDF.
    - Если `data` - путь к файлу, то читает содержимое файла в кодировке UTF-8 и передает в функцию `pisa.CreatePDF`.
3.  Логирует информацию об успешном сохранении PDF-файла.
4.  В случае возникновения ошибок логирует информацию об ошибке и возвращает `False`.

**Примеры**:

```python
html_content = "<html><body><h1>Hello, PDF!</h1></body></html>"
pdf_file = "output.pdf"
success = PDFUtils.save_pdf_xhtml2pdf(html_content, pdf_file)
print(f"PDF saved successfully: {success}")
```

### `html2pdf`

```python
@staticmethod
def html2pdf(html_str: str, pdf_file: str | Path) -> bool | None:
    """Converts HTML content to a PDF file using WeasyPrint."""
    ...
```

**Назначение**:
Конвертирует HTML-контент в PDF-файл, используя WeasyPrint.

**Параметры**:
- `html_str` (str): HTML-контент для преобразования.
- `pdf_file` (str | Path): Путь к сохраняемому PDF-файлу.

**Возвращает**:
- `bool | None`: `True`, если конвертация прошла успешно, `None` в противном случае.

**Как работает функция**:
1. Использует `weasyprint.HTML(string=html_str).write_pdf(pdf_file)` для преобразования HTML-контента в PDF-файл.
2. Возвращает `True` в случае успеха, `None` в случае ошибки.

**Примеры**:

```python
html_content = "<html><body><h1>Hello, PDF!</h1></body></html>"
pdf_file = "output.pdf"
success = PDFUtils.html2pdf(html_content, pdf_file)
print(f"PDF saved successfully: {success}")
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

**Назначение**:
Конвертирует PDF-файл в HTML-файл.

**Параметры**:
- `pdf_file` (str | Path): Путь к исходному PDF-файлу.
- `html_file` (str | Path): Путь к сохраняемому HTML-файлу.

**Возвращает**:
- `bool`: `True`, если конвертация прошла успешно, иначе `False`.

**Как работает функция**:
1. Извлекает текст из PDF-файла с помощью `pdfminer.high_level.extract_text`.
2. Создает HTML-файл и записывает извлеченный текст в теги `<html><body>`.
3. Возвращает `True` в случае успеха, `False` в случае ошибки.

**Примеры**:

```python
pdf_file = "input.pdf"
html_file = "output.html"
success = PDFUtils.pdf_to_html(pdf_file, html_file)
print(f"HTML saved successfully: {success}")
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

**Назначение**:
Сохраняет данные словаря в PDF-файл.

**Параметры**:
- `data` (Any): Словарь или SimpleNamespace для преобразования в PDF.
- `file_path` (str | Path): Путь к выходному PDF-файлу.

**Возвращает**:
- None

**Как работает функция**:
1. Если входные данные - `SimpleNamespace`, преобразует их в словарь.
2. Создает объект `canvas.Canvas` для генерации PDF.
3. Устанавливает шрифт по умолчанию.
4. Перебирает пары ключ-значение в словаре и записывает их в PDF, перенося строки и создавая новые страницы при необходимости.
5. Сохраняет PDF-файл.

**Примеры**:

```python
from pathlib import Path
from types import SimpleNamespace
from src.utils.pdf import PDFUtils

data = {"name": "John Doe", "age": 30, "city": "New York"}
file_path = "data.pdf"
PDFUtils.dict2pdf(data, file_path)
```

## Переменные

Отсутствуют

## Запуск

Для использования этого модуля необходимо установить библиотеки `pdfkit`, `fpdf`, `WeasyPrint`, `xhtml2pdf`, `pdfminer.six` и `Pillow`.

```bash
pip install pdfkit fpdf WeasyPrint xhtml2pdf pdfminer.six Pillow
```

Кроме того, для корректной работы `pdfkit` необходимо установить `wkhtmltopdf`.

```bash
# Например, для Ubuntu:
sudo apt-get install wkhtmltopdf
```

После установки можно использовать функции модуля для работы с PDF-файлами.

```python
from src.utils.pdf import PDFUtils
from pathlib import Path

html_content = "<html><body><h1>Hello, PDF!</h1></body></html>"
pdf_file = "output.pdf"
success = PDFUtils.save_pdf_pdfkit(html_content, pdf_file)
print(f"PDF saved successfully: {success}")