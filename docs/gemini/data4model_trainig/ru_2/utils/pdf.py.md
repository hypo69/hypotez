### Анализ кода `hypotez/src/utils/pdf.py.md`

## Обзор

Модуль предназначен для преобразования HTML-контента или файлов в PDF с использованием различных библиотек.

## Подробнее

Этот модуль предоставляет набор статических методов класса `PDFUtils` для сохранения HTML-контента или файлов в формат PDF с использованием нескольких библиотек: `pdfkit`, `fpdf`, `WeasyPrint` и `xhtml2pdf`. Также реализована функция для конвертации PDF в HTML и для сохранения данных из словаря в PDF.

## Классы

### `PDFUtils`

```python
class PDFUtils:
    """
    Класс для работы с PDF-файлами, предоставляющий методы для сохранения HTML-контента в PDF с использованием различных библиотек.
    """
    ...
```

**Описание**:
Класс для работы с PDF-файлами, предоставляющий статические методы для сохранения HTML-контента в PDF с использованием различных библиотек.

**Методы**:

*   `save_pdf_pdfkit(data: str | Path, pdf_file: str | Path) -> bool`: Сохраняет HTML-контент или файл в PDF с использованием библиотеки `pdfkit`.
*   `save_pdf_fpdf(data: str, pdf_file: str | Path) -> bool`: Сохраняет текст в PDF с использованием библиотеки `FPDF`.
*   `save_pdf_weasyprint(data: str | Path, pdf_file: str | Path) -> bool`: Сохраняет HTML-контент или файл в PDF с использованием библиотеки `WeasyPrint`.
*   `save_pdf_xhtml2pdf(data: str | Path, pdf_file: str | Path) -> bool`: Сохраняет HTML-контент или файл в PDF с использованием библиотеки `xhtml2pdf`.
*   `html2pdf(html_str: str, pdf_file: str | Path) -> bool | None`: Конвертирует HTML-контент в PDF-файл с использованием WeasyPrint.
*   `pdf_to_html(pdf_file: str | Path, html_file: str | Path) -> bool`: Конвертирует PDF-файл в HTML-файл.
*   `dict2pdf(data: Any, file_path: str | Path) -> None`: Сохраняет данные из словаря в PDF-файл.

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

**Назначение**: Сохраняет HTML-контент или файл в PDF с использованием библиотеки `pdfkit`.

**Параметры**:

*   `data` (str | Path): HTML-контент или путь к HTML-файлу.
*   `pdf_file` (str | Path): Путь к сохраняемому PDF-файлу.

**Возвращает**:

*   `bool`: `True`, если PDF успешно сохранен, иначе `False`.

**Вызывает исключения**:

*   `pdfkit.PDFKitError`: Ошибка генерации PDF через `pdfkit`.
*   `OSError`: Ошибка доступа к файлу.

**Как работает функция**:

1.  Определяет путь к исполняемому файлу `wkhtmltopdf.exe`.
2.  Создает объект конфигурации `pdfkit`.
3.  В зависимости от типа данных (строка или путь) вызывает `pdfkit.from_string` или `pdfkit.from_file` для преобразования HTML в PDF.
4.  Логирует ошибки, если преобразование не удалось.

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

**Назначение**: Сохраняет текст в PDF с использованием библиотеки FPDF.

**Параметры**:

*   `data` (str): Текст для сохранения.
*   `pdf_file` (str | Path): Путь к сохраняемому PDF-файлу.

**Возвращает**:

*   `bool`: `True`, если PDF успешно сохранен, иначе `False`.

**Как работает функция**:

1.  Импортирует `FPDF` из библиотеки `fpdf`.
2.  Создает объект `FPDF`.
3.  Добавляет страницу в PDF-документ.
4.  Устанавливает автоматический перенос строк.
5.  Загружает шрифты из файла `fonts.json`.
6.  Устанавливает шрифт по умолчанию.
7.  Добавляет текст на страницу.
8.  Сохраняет PDF-файл.
9.  Логирует ошибки, если сохранение не удалось.

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

**Назначение**: Сохраняет HTML-контент или файл в PDF с использованием библиотеки `WeasyPrint`.

**Параметры**:

*   `data` (str | Path): HTML-контент или путь к HTML-файлу.
*   `pdf_file` (str | Path): Путь к сохраняемому PDF-файлу.

**Возвращает**:

*   `bool`: `True`, если PDF успешно сохранен, иначе `False`.

**Как работает функция**:

1.  Импортирует `HTML` из библиотеки `weasyprint`.
2.  В зависимости от типа данных (строка или путь) вызывает `HTML(string=data).write_pdf(pdf_file)` или `HTML(filename=str(data)).write_pdf(pdf_file)` для преобразования HTML в PDF.
3.  Логирует ошибки, если преобразование не удалось.

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

**Назначение**: Сохраняет HTML-контент или файл в PDF с использованием библиотеки `xhtml2pdf`.

**Параметры**:

*   `data` (str | Path): HTML-контент или путь к HTML-файлу.
*   `pdf_file` (str | Path): Путь к сохраняемому PDF-файлу.

**Возвращает**:

*   `bool`: `True`, если PDF успешно сохранен, иначе `False`.

**Как работает функция**:

1.  Импортирует `pisa` из библиотеки `xhtml2pdf`.
2.  Открывает файл для записи в бинарном режиме (`"w+b"`).
3.  В зависимости от типа данных (строка или путь) вызывает `pisa.CreatePDF` для преобразования HTML в PDF.
4.  Логирует ошибки, если преобразование не удалось.

### `html2pdf`

```python
@staticmethod
def html2pdf(html_str: str, pdf_file: str | Path) -> bool | None:
    """Converts HTML content to a PDF file using WeasyPrint."""
    ...
```

**Назначение**:
Преобразует HTML-контент в PDF-файл с использованием библиотеки `WeasyPrint`.

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

### `pdf_to_html`

```python
@staticmethod
def pdf_to_html(pdf_file: str | Path) -> bool:
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

*   `pdf_file` (str | Path): Путь к исходному PDF-файлу.
*   `html_file` (str | Path): Путь к сохраняемому HTML-файлу.

**Возвращает**:

*   `bool`: `True`, если конвертация прошла успешно, иначе `False`.

**Как работает функция**:

1.  Импортирует `extract_text` из библиотеки `pdfminer.high_level`.
2.  Извлекает текст из PDF-файла с помощью `extract_text(str(pdf_file))`.
3.  Создает HTML-файл и записывает в него извлеченный текст, обернутый в теги `<html><body>`.
4.  Возвращает `True` в случае успеха, `False` в случае ошибки.

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
Сохраняет данные из словаря в PDF-файл.

**Параметры**:

*   `data` (Any): Словарь или объект `SimpleNamespace` для сохранения в PDF.
*   `file_path` (str | Path): Путь к выходному PDF-файлу.

**Как работает функция**:

1.  Если входные данные являются объектом `SimpleNamespace`, преобразует его в словарь.
2.  Создает объект `canvas.Canvas` для создания PDF-файла.
3.  Устанавливает шрифт `Helvetica` размером 12.
4.  Перебирает элементы словаря и записывает их в PDF-файл в виде строк "ключ: значение".
5.  Если достигнут конец страницы, создает новую страницу.
6.  Сохраняет PDF-файл.

## Константы

*   Отсутствуют.

## Примеры использования

```python
from src.utils.pdf import PDFUtils
from pathlib import Path

# Пример сохранения HTML-контента в PDF с использованием pdfkit
html_content = "<html><body><h1>Hello, world!</h1></body></html>"
pdf_file = "example.pdf"
PDFUtils.save_pdf_pdfkit(html_content, pdf_file)

# Пример сохранения текста в PDF с использованием FPDF
text = "This is a test PDF file."
pdf_file = "example_fpdf.pdf"
PDFUtils.save_pdf_fpdf(text, pdf_file)
```

## Зависимости

*   `sys`: Для работы с параметрами командной строки и другими системными функциями.
*   `os`: Для работы с операционной системой и файловой системой.
*   `json`: Для работы с JSON-данными.
*   `pathlib.Path`: Для работы с путями к файлам.
*   `typing.Any, typing.Optional, typing.Union`: Для аннотаций типов.
*   `pdfkit`: Для преобразования HTML в PDF (требует установленного wkhtmltopdf).
*   `fpdf`: Для создания PDF-файлов из текста.
*   `xhtml2pdf`: Для преобразования HTML и CSS в PDF.
*   `weasyprint`: Для преобразования HTML в PDF.
*   `reportlab.pdfgen.canvas`: Для низкоуровневого создания PDF-файлов.
*   `pdfminer.high_level`: Для извлечения текста из PDF-файлов.
*   `header`: Модуль, определяющий корень проекта.

## Взаимосвязи с другими частями проекта

Модуль `pdf.py` предоставляет набор утилит для работы с PDF-файлами и может использоваться в других частях проекта `hypotez`, где требуется создание, преобразование или извлечение информации из PDF-документов.  Разные инструменты сохранения позволяют использовать разные библиотеки для достижения наибольшей совместимости с разными типами входных данных (например, HTML или текст)