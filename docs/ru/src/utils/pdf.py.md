# Модуль `src.utils.pdf`

## Обзор

Модуль предназначен для преобразования HTML-контента или файлов в PDF с использованием различных библиотек. Он предоставляет статические методы класса `PDFUtils` для работы с PDF-файлами. Модуль использует библиотеки `pdfkit`, `FPDF`, `WeasyPrint`, `xhtml2pdf` и `reportlab` для преобразования в PDF.

## Подробней

Модуль содержит класс `PDFUtils`, который предоставляет статические методы для сохранения HTML-контента в PDF с использованием различных библиотек. В частности, модуль может быть использован для сохранения отчетов, сгенерированных на основе HTML-шаблонов, в формате PDF.

## Классы

### `PDFUtils`

**Описание**: Класс для работы с PDF-файлами, предоставляющий методы для сохранения HTML-контента в PDF с использованием различных библиотек.

**Принцип работы**:
Класс предоставляет набор статических методов, каждый из которых использует определенную библиотеку для преобразования HTML в PDF. Методы охватывают различные подходы к генерации PDF, начиная от использования внешних инструментов, таких как `wkhtmltopdf`, и заканчивая библиотеками, написанными на Python, такими как `FPDF` и `WeasyPrint`.

**Методы**:
- `save_pdf_pdfkit(data: str | Path, pdf_file: str | Path) -> bool`: Сохраняет HTML-контент или файл в PDF с использованием библиотеки `pdfkit`.
- `save_pdf_fpdf(data: str, pdf_file: str | Path) -> bool`: Сохраняет текст в PDF с использованием библиотеки `FPDF`.
- `save_pdf_weasyprint(data: str | Path, pdf_file: str | Path) -> bool`: Сохраняет HTML-контент или файл в PDF с использованием библиотеки `WeasyPrint`.
- `save_pdf_xhtml2pdf(data: str | Path, pdf_file: str | Path) -> bool`: Сохраняет HTML-контент или файл в PDF с использованием библиотеки `xhtml2pdf`.
- `html2pdf(html_str: str, pdf_file: str | Path) -> bool | None`: Преобразует HTML-контент в PDF-файл с использованием WeasyPrint.
- `pdf_to_html(pdf_file: str | Path, html_file: str | Path) -> bool`: Конвертирует PDF-файл в HTML-файл.
- `dict2pdf(data: Any, file_path: str | Path) -> None`: Сохраняет данные словаря в PDF-файл.

## Функции

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

**Назначение**: Сохраняет HTML-контент или HTML-файл в PDF-файл, используя библиотеку `pdfkit`.

**Параметры**:
- `data` (str | Path): HTML-контент в виде строки или путь к HTML-файлу.
- `pdf_file` (str | Path): Путь к PDF-файлу, в который будет сохранен результат.

**Возвращает**:
- `bool`: `True`, если PDF успешно сохранен, иначе `False`.

**Вызывает исключения**:
- `pdfkit.PDFKitError`: Если произошла ошибка во время генерации PDF с помощью `pdfkit`.
- `OSError`: Если произошла ошибка при доступе к файлу.
- `FileNotFoundError`: Если не найден исполняемый файл `wkhtmltopdf.exe`.

**Как работает функция**:
1. Определяется путь к исполняемому файлу `wkhtmltopdf.exe`.
2. Проверяется существование `wkhtmltopdf.exe` по указанному пути. Если файл не найден, функция логирует ошибку и вызывает исключение `FileNotFoundError`.
3. Создается конфигурация для `pdfkit`, указывающая путь к `wkhtmltopdf.exe`.
4. Определяются опции, разрешающие локальный доступ к файлам.
5. В зависимости от типа данных (`str` или `Path`), вызывается `pdfkit.from_string` или `pdfkit.from_file` для преобразования HTML в PDF.
6. Логируется информация об успешном сохранении PDF-файла.
7. В случае возникновения исключений, таких как `pdfkit.PDFKitError` или `OSError`, логируется информация об ошибке и возвращается `False`.

```
Проверка наличия wkhtmltopdf.exe
     |
     No
     |
   Выброс FileNotFoundError
     |
     Yes
     |
Создание конфигурации pdfkit
     |
Определение типа данных (HTML-строка или файл)
     |
   HTML-строка
     |
 Преобразование HTML-строки в PDF
     |
   HTML-файл
     |
   Чтение HTML-файла и преобразование в PDF
     |
Сохранение PDF-файла
     |
Успешно
     |
   Логирование успешного сохранения
     |
Ошибка
     |
 Логирование ошибки и возврат False
     |
Возврат True
```

**Примеры**:

```python
from pathlib import Path
from src.utils.pdf import PDFUtils

# Пример сохранения HTML-контента в PDF
html_content = "<html><body><h1>Hello, PDF!</h1></body></html>"
pdf_file = "hello.pdf"
result = PDFUtils.save_pdf_pdfkit(html_content, pdf_file)
print(f"Результат сохранения HTML-контента в PDF: {result}")  # Вывод: True

# Пример сохранения HTML-файла в PDF
html_file = Path("example.html")
html_file.write_text("<html><body><h1>Hello from HTML file!</h1></body></html>")
pdf_file = "hello_from_file.pdf"
result = PDFUtils.save_pdf_pdfkit(html_file, pdf_file)
print(f"Результат сохранения HTML-файла в PDF: {result}")  # Вывод: True

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

**Назначение**: Сохраняет текст в PDF-файл, используя библиотеку `FPDF`.

**Параметры**:
- `data` (str): Текст, который необходимо сохранить в PDF.
- `pdf_file` (str | Path): Путь к PDF-файлу, в который будет сохранен результат.

**Возвращает**:
- `bool`: `True`, если PDF успешно сохранен, иначе `False`.

**Вызывает исключения**:
- `FileNotFoundError`: Если не найден файл шрифтов `fonts.json` или какой-либо из файлов шрифтов, указанных в `fonts.json`.
- `Exception`: Если произошла ошибка во время сохранения PDF с помощью `FPDF`.

**Как работает функция**:
1. Импортируется класс `FPDF` из библиотеки `fpdf`.
2. Создается экземпляр класса `FPDF`.
3. Добавляется новая страница в PDF-документ.
4. Устанавливается автоматический перенос строк.
5. Определяется путь к файлу `fonts.json`, содержащему информацию о шрифтах.
6. Проверяется существование файла `fonts.json`. Если файл не найден, функция логирует ошибку и вызывает исключение `FileNotFoundError`.
7. Открывается файл `fonts.json`, считывается информация о шрифтах.
8. Для каждого шрифта, указанного в `fonts.json`, проверяется существование файла шрифта. Если файл не найден, функция логирует ошибку и вызывает исключение `FileNotFoundError`.
9. Добавляется шрифт в PDF-документ с использованием метода `add_font`.
10. Устанавливается шрифт по умолчанию.
11. Добавляется текст в PDF-документ с использованием метода `multi_cell`.
12. Сохраняется PDF-файл.
13. Логируется информация об успешном сохранении PDF-файла.
14. В случае возникновения исключений логируется информация об ошибке и возвращается `False`.

```
Инициализация FPDF
     |
Добавление страницы
     |
Установка параметров страницы
     |
Чтение файла шрифтов fonts.json
     |
Проверка существования файла шрифтов
     |
   Файл не найден
     |
  Выброс FileNotFoundError
     |
   Файл найден
     |
Загрузка параметров шрифтов
     |
Добавление шрифтов
     |
Установка шрифта
     |
Добавление контента
     |
Сохранение PDF
     |
Обработка исключений
```

**Примеры**:

```python
from pathlib import Path
from src.utils.pdf import PDFUtils

# Пример сохранения текста в PDF с использованием FPDF
text_data = "Hello, PDF from FPDF! This is a test."
pdf_file = "hello_fpdf.pdf"
result = PDFUtils.save_pdf_fpdf(text_data, pdf_file)
print(f"Результат сохранения текста в PDF с использованием FPDF: {result}")  # Вывод: True

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

**Назначение**: Сохраняет HTML-контент или HTML-файл в PDF-файл, используя библиотеку `WeasyPrint`.

**Параметры**:
- `data` (str | Path): HTML-контент в виде строки или путь к HTML-файлу.
- `pdf_file` (str | Path): Путь к PDF-файлу, в который будет сохранен результат.

**Возвращает**:
- `bool`: `True`, если PDF успешно сохранен, иначе `False`.

**Вызывает исключения**:
- `Exception`: Если произошла ошибка во время сохранения PDF с помощью `WeasyPrint`.

**Как работает функция**:
1. Импортируется класс `HTML` из библиотеки `weasyprint`.
2. В зависимости от типа данных (`str` или `Path`), вызывается `HTML(string=data).write_pdf(pdf_file)` или `HTML(filename=str(data)).write_pdf(pdf_file)` для преобразования HTML в PDF.
3. Логируется информация об успешном сохранении PDF-файла.
4. В случае возникновения исключений логируется информация об ошибке и возвращается `False`.

```
Инициализация WeasyPrint
     |
Определение типа данных (HTML-строка или файл)
     |
   HTML-строка
     |
  Преобразование HTML-строки в PDF
     |
   HTML-файл
     |
  Чтение HTML-файла и преобразование в PDF
     |
Сохранение PDF-файла
     |
Успешно
     |
 Логирование успешного сохранения
     |
Ошибка
     |
Логирование ошибки и возврат False
     |
Возврат True
```

**Примеры**:

```python
from pathlib import Path
from src.utils.pdf import PDFUtils

# Пример сохранения HTML-контента в PDF с использованием WeasyPrint
html_content = "<html><body><h1>Hello, PDF from WeasyPrint!</h1></body></html>"
pdf_file = "hello_weasyprint.pdf"
result = PDFUtils.save_pdf_weasyprint(html_content, pdf_file)
print(f"Результат сохранения HTML-контента в PDF с использованием WeasyPrint: {result}")  # Вывод: True

# Пример сохранения HTML-файла в PDF с использованием WeasyPrint
html_file = Path("example.html")
html_file.write_text("<html><body><h1>Hello from HTML file!</h1></body></html>")
pdf_file = "hello_from_file_weasyprint.pdf"
result = PDFUtils.save_pdf_weasyprint(html_file, pdf_file)
print(f"Результат сохранения HTML-файла в PDF с использованием WeasyPrint: {result}")  # Вывод: True
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

**Назначение**: Сохраняет HTML-контент или HTML-файл в PDF-файл, используя библиотеку `xhtml2pdf`.

**Параметры**:
- `data` (str | Path): HTML-контент в виде строки или путь к HTML-файлу.
- `pdf_file` (str | Path): Путь к PDF-файлу, в который будет сохранен результат.

**Возвращает**:
- `bool`: `True`, если PDF успешно сохранен, иначе `False`.

**Вызывает исключения**:
- `Exception`: Если произошла ошибка во время сохранения PDF с помощью `xhtml2pdf`.

**Как работает функция**:
1. Импортируется модуль `pisa` из библиотеки `xhtml2pdf`.
2. Открывается PDF-файл для записи в бинарном режиме.
3. В зависимости от типа данных (`str` или `Path`), вызывается `pisa.CreatePDF(data, dest=result_file)` или читается HTML-файл и вызывается `pisa.CreatePDF(source_data, dest=result_file, encoding='UTF-8')` для преобразования HTML в PDF.
4. Логируется информация об успешном сохранении PDF-файла.
5. В случае возникновения исключений логируется информация об ошибке и возвращается `False`.

```
Инициализация xhtml2pdf
     |
Открытие PDF-файла для записи
     |
Определение типа данных (HTML-строка или файл)
     |
  HTML-строка
     |
Преобразование HTML-строки в PDF
     |
  HTML-файл
     |
Чтение HTML-файла и преобразование в PDF
     |
Сохранение PDF-файла
     |
Успешно
     |
Логирование успешного сохранения
     |
Ошибка
     |
Логирование ошибки и возврат False
     |
Возврат True
```

**Примеры**:

```python
from pathlib import Path
from src.utils.pdf import PDFUtils

# Пример сохранения HTML-контента в PDF с использованием xhtml2pdf
html_content = "<html><body><h1>Hello, PDF from xhtml2pdf!</h1></body></html>"
pdf_file = "hello_xhtml2pdf.pdf"
result = PDFUtils.save_pdf_xhtml2pdf(html_content, pdf_file)
print(f"Результат сохранения HTML-контента в PDF с использованием xhtml2pdf: {result}")  # Вывод: True

# Пример сохранения HTML-файла в PDF с использованием xhtml2pdf
html_file = Path("example.html")
html_file.write_text("<html><body><h1>Hello from HTML file!</h1></body></html>")
pdf_file = "hello_from_file_xhtml2pdf.pdf"
result = PDFUtils.save_pdf_xhtml2pdf(html_file, pdf_file)
print(f"Результат сохранения HTML-файла в PDF с использованием xhtml2pdf: {result}")  # Вывод: True
```

### `html2pdf`

```python
@staticmethod
def html2pdf(html_str: str, pdf_file: str | Path) -> bool | None:
    """Converts HTML content to a PDF file using WeasyPrint."""
    ...
```

**Назначение**: Преобразует HTML-контент в PDF-файл, используя WeasyPrint.

**Параметры**:
- `html_str` (str): HTML-контент в виде строки.
- `pdf_file` (str | Path): Путь к PDF-файлу, в который будет сохранен результат.

**Возвращает**:
- `bool | None`: `True`, если PDF успешно сохранен, или `None` в случае ошибки.

**Вызывает исключения**:
- `Exception`: Если произошла ошибка во время генерации PDF.

**Как работает функция**:
1. Импортируется класс `HTML` из библиотеки `weasyprint`.
2. Вызывается `HTML(string=html_str).write_pdf(pdf_file)` для преобразования HTML в PDF.
3. В случае возникновения исключений выводится информация об ошибке и возвращается `None`.

```
Инициализация WeasyPrint
     |
Преобразование HTML-строки в PDF
     |
Сохранение PDF-файла
     |
Успешно
     |
Возврат True
     |
Ошибка
     |
Вывод сообщения об ошибке и возврат None
     |
Возврат None
```

**Примеры**:

```python
from pathlib import Path
from src.utils.pdf import PDFUtils

# Пример сохранения HTML-контента в PDF с использованием WeasyPrint
html_content = "<html><body><h1>Hello, PDF from WeasyPrint!</h1></body></html>"
pdf_file = "hello_weasyprint.pdf"
result = PDFUtils.html2pdf(html_content, pdf_file)
print(f"Результат сохранения HTML-контента в PDF с использованием WeasyPrint: {result}")
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
- `Exception`: Если произошла ошибка во время конвертации PDF в HTML.

**Как работает функция**:
1. Импортируется функция `extract_text` из модуля `pdfminer.high_level`.
2. Извлекается текст из PDF-файла с использованием `extract_text`.
3. Открывается HTML-файл для записи в кодировке UTF-8.
4. Записывается HTML-разметка с извлеченным текстом в файл.
5. В случае возникновения исключений выводится информация об ошибке и возвращается `False`.

```
Инициализация PDFMiner
     |
Извлечение текста из PDF
     |
Создание HTML-файла
     |
Запись текста в HTML-файл
     |
Успешно
     |
Возврат True
     |
Ошибка
     |
Вывод сообщения об ошибке и возврат False
     |
Возврат False
```

**Примеры**:

```python
from pathlib import Path
from src.utils.pdf import PDFUtils

# Пример конвертации PDF-файла в HTML-файл
pdf_file = "example.pdf"  # Замените на путь к вашему PDF-файлу
html_file = "example.html"
result = PDFUtils.pdf_to_html(pdf_file, html_file)
print(f"Результат конвертации PDF в HTML: {result}")
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
- `data` (Any): Словарь для конвертации в PDF.
- `file_path` (str | Path): Путь к выходному PDF-файлу.

**Возвращает**:
- `None`

**Вызывает исключения**:
- Отсутствуют.

**Как работает функция**:
1. Проверяется, является ли входной параметр экземпляром `SimpleNamespace`. Если да, то он преобразуется в словарь.
2. Создается объект `canvas.Canvas` для создания PDF-файла.
3. Устанавливается шрифт "Helvetica" размером 12.
4. Перебираются элементы словаря.
5. Для каждой пары ключ-значение создается строка, которая выводится на PDF-страницу.
6. Если текущая позиция по вертикали становится меньше 50, создается новая страница.
7. Сохраняется PDF-файл.

```
Преобразование SimpleNamespace в словарь (если необходимо)
     |
Создание PDF-документа
     |
Установка шрифта
     |
Перебор элементов словаря
     |
Форматирование строки
     |
Вывод строки на страницу
     |
Проверка на переполнение страницы
     |
Да
     |
Создание новой страницы
     |
Нет
     |
Продолжение
     |
Сохранение PDF-документа
```

**Примеры**:

```python
from pathlib import Path
from types import SimpleNamespace
from src.utils.pdf import PDFUtils

# Пример сохранения словаря в PDF
data = {"name": "John Doe", "age": 30, "city": "New York"}
pdf_file = "dict_example.pdf"
PDFUtils.dict2pdf(data, pdf_file)

# Пример сохранения SimpleNamespace в PDF
data = SimpleNamespace(name="Jane Doe", age=25, city="Los Angeles")
pdf_file = "simplenamespace_example.pdf"
PDFUtils.dict2pdf(data, pdf_file)