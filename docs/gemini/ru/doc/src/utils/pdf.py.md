# Модуль `src.utils.pdf`

## Обзор

Модуль `src.utils.pdf` предназначен для преобразования HTML-контента или файлов в PDF с использованием различных библиотек, таких как `pdfkit`, `FPDF`, `WeasyPrint` и `xhtml2pdf`. Он предоставляет статические методы для сохранения HTML-контента в PDF и конвертации PDF в HTML.

## Подробней

Этот модуль предоставляет набор инструментов для работы с PDF-файлами, позволяя сохранять HTML-контент в PDF с использованием разных библиотек и конвертировать PDF-файлы в HTML. Он использует библиотеки `pdfkit`, `FPDF`, `WeasyPrint`, `xhtml2pdf` и `pdfminer`.

## Классы

### `PDFUtils`

**Описание**: Класс `PDFUtils` предоставляет статические методы для работы с PDF-файлами, включая сохранение HTML-контента в PDF с использованием различных библиотек.

**Атрибуты**:
- Нет атрибутов класса.

**Методы**:
- `save_pdf_pdfkit(data: str | Path, pdf_file: str | Path) -> bool`: Сохраняет HTML-контент или файл в PDF с использованием библиотеки `pdfkit`.
- `save_pdf_fpdf(data: str, pdf_file: str | Path) -> bool`: Сохраняет текст в PDF с использованием библиотеки `FPDF`.
- `save_pdf_weasyprint(data: str | Path, pdf_file: str | Path) -> bool`: Сохраняет HTML-контент или файл в PDF с использованием библиотеки `WeasyPrint`.
- `save_pdf_xhtml2pdf(data: str | Path, pdf_file: str | Path) -> bool`: Сохраняет HTML-контент или файл в PDF с использованием библиотеки `xhtml2pdf`.
- `html2pdf(html_str: str, pdf_file: str | Path) -> bool | None`: Преобразует HTML-контент в PDF-файл, используя WeasyPrint.
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

**Назначение**: Сохраняет HTML-контент или файл в PDF с использованием библиотеки `pdfkit`.

**Параметры**:
- `data` (str | Path): HTML-контент или путь к HTML-файлу.
- `pdf_file` (str | Path): Путь к сохраняемому PDF-файлу.

**Возвращает**:
- `bool`: `True`, если PDF успешно сохранен, иначе `False`.

**Вызывает исключения**:
- `pdfkit.PDFKitError`: Если возникает ошибка при генерации PDF через `pdfkit`.
- `OSError`: Если возникает ошибка доступа к файлу.

**Как работает функция**:
1. Определяется путь к исполняемому файлу `wkhtmltopdf.exe`.
2. Проверяется наличие `wkhtmltopdf.exe` по указанному пути. Если файл не найден, регистрируется ошибка и выбрасывается исключение `FileNotFoundError`.
3. Создается конфигурация для `pdfkit` с указанием пути к `wkhtmltopdf.exe`.
4. Определяются опции, разрешающие доступ к локальным файлам.
5. В зависимости от типа входных данных (строка или путь), вызывается `pdfkit.from_string` для HTML-контента или `pdfkit.from_file` для HTML-файла.
6. В случае успешного сохранения PDF, регистрируется информационное сообщение и возвращается `True`.
7. В случае возникновения исключения, регистрируется ошибка и возвращается `False`.

**Примеры**:

```python
from pathlib import Path
from src.utils.pdf import PDFUtils

# Пример сохранения HTML-контента в PDF
html_content = "<html><body><h1>Hello, PDF!</h1></body></html>"
pdf_file = "example.pdf"
result = PDFUtils.save_pdf_pdfkit(html_content, pdf_file)
print(f"Результат сохранения HTML-контента в PDF: {result}")

# Пример сохранения HTML-файла в PDF
html_file = Path("example.html")
html_file.write_text("<html><body><h1>Hello, PDF!</h1></body></html>")
pdf_file = "example_file.pdf"
result = PDFUtils.save_pdf_pdfkit(html_file, pdf_file)
print(f"Результат сохранения HTML-файла в PDF: {result}")
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

**Назначение**: Сохраняет текст в PDF с использованием библиотеки `FPDF`.

**Параметры**:
- `data` (str): Текст, который необходимо сохранить в PDF.
- `pdf_file` (str | Path): Путь к сохраняемому PDF-файлу.

**Возвращает**:
- `bool`: `True`, если PDF успешно сохранен, иначе `False`.

**Как работает функция**:
1. Импортируется класс `FPDF` из библиотеки `fpdf`.
2. Создается экземпляр класса `FPDF`.
3. Добавляется новая страница в PDF-документ.
4. Устанавливается автоматический перенос по страницам.
5. Определяется путь к файлу `fonts.json`, содержащему информацию о шрифтах.
6. Проверяется наличие файла `fonts.json`. Если файл не найден, регистрируется ошибка и выбрасывается исключение `FileNotFoundError`.
7. Загружается информация о шрифтах из файла `fonts.json`.
8. Добавляются шрифты, указанные в файле `fonts.json`, в PDF-документ.
9. Устанавливается шрифт по умолчанию.
10. Добавляется текст в PDF-документ с использованием метода `multi_cell`.
11. Сохраняется PDF-документ в указанный файл.
12. В случае успешного сохранения PDF, регистрируется информационное сообщение и возвращается `True`.
13. В случае возникновения исключения, регистрируется ошибка и возвращается `False`.

**Примеры**:

```python
from pathlib import Path
from src.utils.pdf import PDFUtils

# Пример сохранения текста в PDF
text_content = "Hello, PDF!"
pdf_file = "example_fpdf.pdf"
result = PDFUtils.save_pdf_fpdf(text_content, pdf_file)
print(f"Результат сохранения текста в PDF (FPDF): {result}")
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

**Назначение**: Сохраняет HTML-контент или файл в PDF с использованием библиотеки `WeasyPrint`.

**Параметры**:
- `data` (str | Path): HTML-контент или путь к HTML-файлу.
- `pdf_file` (str | Path): Путь к сохраняемому PDF-файлу.

**Возвращает**:
- `bool`: `True`, если PDF успешно сохранен, иначе `False`.

**Как работает функция**:
1. Импортируется класс `HTML` из библиотеки `weasyprint`.
2. В зависимости от типа входных данных (строка или путь), вызывается `HTML(string=data).write_pdf(pdf_file)` для HTML-контента или `HTML(filename=str(data)).write_pdf(pdf_file)` для HTML-файла.
3. В случае успешного сохранения PDF, регистрируется информационное сообщение и возвращается `True`.
4. В случае возникновения исключения, регистрируется ошибка и возвращается `False`.

**Примеры**:

```python
from pathlib import Path
from src.utils.pdf import PDFUtils

# Пример сохранения HTML-контента в PDF
html_content = "<html><body><h1>Hello, PDF!</h1></body></html>"
pdf_file = "example_weasyprint.pdf"
result = PDFUtils.save_pdf_weasyprint(html_content, pdf_file)
print(f"Результат сохранения HTML-контента в PDF (WeasyPrint): {result}")

# Пример сохранения HTML-файла в PDF
html_file = Path("example.html")
html_file.write_text("<html><body><h1>Hello, PDF!</h1></body></html>")
pdf_file = "example_file_weasyprint.pdf"
result = PDFUtils.save_pdf_weasyprint(html_file, pdf_file)
print(f"Результат сохранения HTML-файла в PDF (WeasyPrint): {result}")
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

**Назначение**: Сохраняет HTML-контент или файл в PDF с использованием библиотеки `xhtml2pdf`.

**Параметры**:
- `data` (str | Path): HTML-контент или путь к HTML-файлу.
- `pdf_file` (str | Path): Путь к сохраняемому PDF-файлу.

**Возвращает**:
- `bool`: `True`, если PDF успешно сохранен, иначе `False`.

**Как работает функция**:
1. Импортируется модуль `pisa` из библиотеки `xhtml2pdf`.
2. Открывается PDF-файл для записи в бинарном режиме.
3. В зависимости от типа входных данных (строка или путь):
   - Если входные данные - строка, кодирует строку в UTF-8 и создает PDF из строки.
   - Если входные данные - путь к файлу, открывает файл, читает его содержимое в кодировке UTF-8 и создает PDF из содержимого файла.
4. В случае успешного сохранения PDF, регистрируется информационное сообщение и возвращается `True`.
5. В случае возникновения исключения, регистрируется ошибка и возвращается `False`.

**Примеры**:

```python
from pathlib import Path
from src.utils.pdf import PDFUtils

# Пример сохранения HTML-контента в PDF
html_content = "<html><body><h1>Hello, PDF!</h1></body></html>"
pdf_file = "example_xhtml2pdf.pdf"
result = PDFUtils.save_pdf_xhtml2pdf(html_content, pdf_file)
print(f"Результат сохранения HTML-контента в PDF (xhtml2pdf): {result}")

# Пример сохранения HTML-файла в PDF
html_file = Path("example.html")
html_file.write_text("<html><body><h1>Hello, PDF!</h1></body></html>")
pdf_file = "example_file_xhtml2pdf.pdf"
result = PDFUtils.save_pdf_xhtml2pdf(html_file, pdf_file)
print(f"Результат сохранения HTML-файла в PDF (xhtml2pdf): {result}")
```

### `html2pdf`

```python
    @staticmethod
    def html2pdf(html_str: str, pdf_file: str | Path) -> bool | None:
        """Converts HTML content to a PDF file using WeasyPrint."""
        ...
```

**Назначение**: Преобразует HTML-контент в PDF-файл, используя `WeasyPrint`.

**Параметры**:
- `html_str` (str): HTML-контент для преобразования.
- `pdf_file` (str | Path): Путь к сохраняемому PDF-файлу.

**Возвращает**:
- `bool | None`: `True`, если преобразование прошло успешно, иначе `None`.

**Как работает функция**:
1. Импортируется класс `HTML` из библиотеки `weasyprint`.
2. Используется `HTML(string=html_str).write_pdf(pdf_file)` для записи HTML-контента в PDF-файл.
3. В случае успешного преобразования возвращается `True`.
4. В случае возникновения исключения выводится сообщение об ошибке и возвращается `None`.

**Примеры**:

```python
from pathlib import Path
from src.utils.pdf import PDFUtils

# Пример преобразования HTML-контента в PDF
html_content = "<html><body><h1>Hello, PDF!</h1></body></html>"
pdf_file = "example_html2pdf.pdf"
result = PDFUtils.html2pdf(html_content, pdf_file)
print(f"Результат преобразования HTML-контента в PDF (html2pdf): {result}")
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

**Как работает функция**:
1. Импортируется функция `extract_text` из библиотеки `pdfminer.high_level`.
2. Извлекается текст из PDF-файла с использованием `extract_text`.
3. Открывается HTML-файл для записи в кодировке UTF-8.
4. Записывается HTML-разметка с извлеченным текстом в файл.
5. В случае успешной конвертации возвращается `True`.
6. В случае возникновения исключения выводится сообщение об ошибке и возвращается `False`.

**Примеры**:

```python
from pathlib import Path
from src.utils.pdf import PDFUtils

# Пример конвертации PDF-файла в HTML
pdf_file = "example.pdf"
html_file = "example.html"
result = PDFUtils.pdf_to_html(pdf_file, html_file)
print(f"Результат конвертации PDF-файла в HTML: {result}")
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
- `data` (dict | SimpleNamespace): Словарь для конвертации в PDF.
- `file_path` (str | Path): Путь к сохраняемому PDF-файлу.

**Как работает функция**:
1. Проверяется, является ли `data` экземпляром `SimpleNamespace`, и преобразует его в словарь, если это так.
2. Создается объект `canvas.Canvas` с указанным путем к файлу и размером страницы A4.
3. Устанавливается шрифт `Helvetica` размером 12.
4. Итерируется по элементам словаря.
5. Для каждой пары ключ-значение формируется строка и выводится на PDF-страницу.
6. Если текущая позиция по высоте становится меньше 50, создается новая страница.
7. Сохраняется PDF-файл.

**Примеры**:

```python
from pathlib import Path
from types import SimpleNamespace
from src.utils.pdf import PDFUtils

# Пример сохранения словаря в PDF
data = {"name": "John", "age": 30, "city": "New York"}
pdf_file = "example_dict.pdf"
PDFUtils.dict2pdf(data, pdf_file)
print(f"Результат сохранения словаря в PDF: {pdf_file}")

# Пример сохранения SimpleNamespace в PDF
data = SimpleNamespace(name="Alice", age=25, city="Los Angeles")
pdf_file = "example_simplenamespace.pdf"
PDFUtils.dict2pdf(data, pdf_file)
print(f"Результат сохранения SimpleNamespace в PDF: {pdf_file}")