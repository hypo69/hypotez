# Модуль для работы с PDF файлами (pdf.py)

## Обзор

Этот модуль предоставляет набор утилит для преобразования HTML-контента или файлов в PDF с использованием различных библиотек.

## Подробней

Модуль `src.utils.pdf` предоставляет функциональность для создания PDF-файлов из HTML-контента или файлов, используя различные библиотеки, такие как `pdfkit`, `fpdf`, `weasyprint` и `xhtml2pdf`. Это позволяет генерировать PDF-отчеты и документы из различных источников.

## Классы

### `PDFUtils`

**Описание**: Класс для работы с PDF-файлами, предоставляющий статические методы для сохранения HTML-контента в PDF с использованием различных библиотек.

**Методы**:

-   `save_pdf_pdfkit(data: str | Path, pdf_file: str | Path) -> bool`: Сохраняет HTML-контент или файл в PDF с использованием библиотеки `pdfkit`.
-   `save_pdf_fpdf(data: str, pdf_file: str | Path) -> bool`: Сохраняет текст в PDF с использованием библиотеки `FPDF`.
-   `save_pdf_weasyprint(data: str | Path, pdf_file: str | Path) -> bool`: Сохраняет HTML-контент или файл в PDF с использованием библиотеки `WeasyPrint`.
-   `save_pdf_xhtml2pdf(data: str | Path, pdf_file: str | Path) -> bool`: Сохраняет HTML-контент или файл в PDF с использованием библиотеки `xhtml2pdf`.
-   `html2pdf(html_str: str, pdf_file: str | Path) -> bool | None`: Преобразует HTML-контент в PDF файл с использованием WeasyPrint.
-   `pdf_to_html(pdf_file: str | Path, html_file: str | Path) -> bool`: Конвертирует PDF-файл в HTML-файл.
-   `dict2pdf(data: Any, file_path: str | Path) -> None`: Сохраняет данные словаря в PDF-файл.

#### `save_pdf_pdfkit`

**Назначение**: Сохраняет HTML-контент или файл в PDF с использованием библиотеки `pdfkit`.

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

**Параметры**:

-   `data` (str | Path): HTML-контент (строка) или путь к HTML-файлу (Path).
-   `pdf_file` (str | Path): Путь для сохранения PDF-файла.

**Возвращает**:

-   `bool`: True, если PDF успешно сохранен, иначе False.

**Как работает функция**:

1.  Определяет путь к исполняемому файлу `wkhtmltopdf.exe`.
2.  Проверяет существование `wkhtmltopdf.exe`.
3.  Инициализирует конфигурацию `pdfkit` с указанием пути к `wkhtmltopdf.exe`.
4.  Преобразует HTML-контент или HTML-файл в PDF, используя `pdfkit.from_string` или `pdfkit.from_file` соответственно.
5.  Логирует информацию об успешном сохранении PDF или возникшей ошибке.

#### `save_pdf_fpdf`

**Назначение**: Сохраняет текст в PDF с использованием библиотеки FPDF.

```python
@staticmethod
def save_pdf_fpdf(data: str, pdf_file: str | Path) -> bool:
    """
    Сохранить текст в PDF с использованием библиотеки FPDF.

    Args:
        data (str): Текст, который необходимо сохранить в PDF.
        pdf_file (str | Path): Путь к сохраняемому PDF-файлу.

    Returns:
        bool: `True`, если PDF успешно сохранен, иначе `False`.\
    """
    ...
```

**Параметры**:

-   `data` (str): Текст, который необходимо сохранить в PDF.
-   `pdf_file` (str | Path): Путь к сохраняемому PDF-файлу.

**Возвращает**:

-   `bool`: `True`, если PDF успешно сохранен, иначе `False`.

**Как работает функция**:

1.  Импортирует библиотеку `fpdf`.
2.  Создает объект `FPDF`.
3.  Добавляет страницу в PDF.
4.  Устанавливает автоматический перенос строк и отступы.
5.  Загружает шрифты из файла `fonts.json`.
6.  Добавляет шрифты в PDF.
7.  Устанавливает шрифт по умолчанию.
8.  Добавляет текст в PDF.
9.  Сохраняет PDF в указанный файл.
10. Логирует информацию об успешном сохранении PDF или возникшей ошибке.

#### `save_pdf_weasyprint`

**Назначение**: Сохраняет HTML-контент или файл в PDF с использованием библиотеки `WeasyPrint`.

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

**Параметры**:

-   `data` (str | Path): HTML-контент (строка) или путь к HTML-файлу (Path).
-   `pdf_file` (str | Path): Путь для сохранения PDF-файла.

**Возвращает**:

-   `bool`: `True`, если PDF успешно сохранен, иначе `False`.

**Как работает функция**:

1.  Импортирует библиотеку `weasyprint`.
2.  Преобразует HTML-контент или HTML-файл в PDF, используя `weasyprint.HTML(string=data).write_pdf(pdf_file)` или `weasyprint.HTML(filename=str(data)).write_pdf(pdf_file)` соответственно.
3.  Логирует информацию об успешном сохранении PDF или возникшей ошибке.

#### `save_pdf_xhtml2pdf`

**Назначение**: Сохраняет HTML-контент или файл в PDF с использованием библиотеки `xhtml2pdf`.

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

**Параметры**:

-   `data` (str | Path): HTML-контент (строка) или путь к HTML-файлу (Path).
-   `pdf_file` (str | Path): Путь для сохранения PDF-файла.

**Возвращает**:

-   `bool`: `True`, если PDF успешно сохранен, иначе `False`.

**Как работает функция**:

1.  Импортирует библиотеку `xhtml2pdf`.
2.  Открывает PDF-файл для записи в бинарном режиме.
3.  В зависимости от типа входных данных (строка или файл) передаёт HTML-контент в функцию `pisa.CreatePDF`.
4.  Логирует информацию об успешном сохранении PDF или возникшей ошибке.

#### `html2pdf`

**Назначение**: Преобразует HTML-контент в PDF-файл с использованием WeasyPrint.

```python
 @staticmethod
    def html2pdf(html_str: str, pdf_file: str | Path) -> bool | None:
        """Converts HTML content to a PDF file using WeasyPrint."""
        ...
```

**Параметры**:
   * html_str (str): HTML контент
   * pdf_file (str | Path): путь, куда необходимо сохранить файл
**Возвращает**:
   * bool | None : True при успешном сохранении, None в случае ошибки

**Как работает функция**:
*   Импортирует HTML из библиотеки weasyprint
*   Записывает HTML контент в pdf файл

#### `pdf_to_html`

**Назначение**: Конвертирует PDF-файл в HTML-файл.

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

**Параметры**:

-   `pdf_file` (str | Path): Путь к исходному PDF-файлу.
-   `html_file` (str | Path): Путь для сохранения HTML-файла.

**Возвращает**:

-   `bool`: `True`, если конвертация прошла успешно, иначе `False`.

**Как работает функция**:

1.  Импортирует функцию `extract_text` из библиотеки `pdfminer.high_level`.
2.  Извлекает текст из PDF-файла с использованием `extract_text`.
3.  Создает HTML-файл и записывает извлеченный текст в формате HTML.
4.  Логирует информацию об успешной конвертации или возникшей ошибке.

#### `dict2pdf`

**Назначение**: Сохраняет данные словаря в PDF-файл.

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

**Параметры**:

-   `data` (Any): Словарь, который нужно преобразовать в PDF.
-   `file_path` (str | Path): Путь к выходному PDF-файлу.

**Как работает функция**:

1.  Преобразует `SimpleNamespace` в `dict`, если входные данные имеют этот тип.
2.  Создает PDF-файл с использованием `reportlab.pdfgen.canvas.Canvas`.
3.  Устанавливает шрифт по умолчанию.
4.  Перебирает элементы словаря и записывает их в PDF-файл в виде строк "key: value".
5.  Если места на странице недостаточно, создает новую страницу.
6.  Сохраняет PDF-файл.

## Переменные модуля

В данном модуле отсутствуют переменные, за исключением констант, используемых внутри функций.

## Пример использования

**Сохранение HTML-контента в PDF с использованием pdfkit:**

```python
from src.utils.pdf import PDFUtils
html_content = "<html><body><h1>Hello, world!</h1></body></html>"
pdf_file = "output.pdf"
success = PDFUtils.save_pdf_pdfkit(html_content, pdf_file)
if success:
    print("PDF успешно создан!")
```

**Преобразование PDF-файла в HTML-файл:**

```python
from src.utils.pdf import PDFUtils

pdf_file = "input.pdf"
html_file = "output.html"
success = PDFUtils.pdf_to_html(pdf_file, html_file)
if success:
    print("HTML файл успешно создан!")
```

## Взаимосвязь с другими частями проекта

-   Модуль `src.utils.pdf` используется другими модулями проекта для генерации PDF-отчетов и документов.
-   Для логирования ошибок используется модуль `src.logger.logger`.
-   Для работы с путями используется модуль `pathlib`.
-   Для работы со строками, преобразованными из HTML, используется кодировка UTF-8, что позволяет корректно отображать текст на разных языках.
-   При использовании библиотеки `fpdf` требуется наличие файла `fonts.json` в директории `assets/fonts` для установки шрифтов. Этот файл должен содержать информацию о используемых шрифтах.