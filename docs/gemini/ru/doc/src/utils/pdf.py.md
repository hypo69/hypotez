# Модуль для работы с PDF-файлами

## Обзор

Модуль `src/utils/pdf.py` предоставляет набор функций и класс для преобразования HTML-контента или файлов в PDF, используя различные библиотеки: `pdfkit`, `FPDF`, `WeasyPrint` и `xhtml2pdf`. 

## Подробнее

Этот модуль предоставляет функциональность для работы с PDF-файлами, включая:

* Сохранение HTML-контента или файлов в PDF.
* Конвертирование PDF-файлов в HTML-файлы.
* Сохранение данных словаря в PDF-файл.

## Классы

### `PDFUtils`

**Описание**: Класс `PDFUtils` содержит набор статических методов для работы с PDF-файлами. 

**Атрибуты**: 
* Нет атрибутов.

**Методы**:

#### `save_pdf_pdfkit(data: str | Path, pdf_file: str | Path) -> bool`

**Назначение**: Сохранить HTML-контент или файл в PDF с использованием библиотеки `pdfkit`.

**Параметры**:
* `data (str | Path)`: HTML-контент или путь к HTML-файлу.
* `pdf_file (str | Path)`: Путь к сохраняемому PDF-файлу.

**Возвращает**:
* `bool`: `True` если PDF успешно сохранен, иначе `False`.

**Вызывает исключения**:
* `pdfkit.PDFKitError`: Ошибка генерации PDF через `pdfkit`.
* `OSError`: Ошибка доступа к файлу.

**Как работает функция**: 
* Функция `save_pdf_pdfkit` использует библиотеку `pdfkit` для преобразования HTML-контента или файлов в PDF. 
* Функция проверяет наличие `wkhtmltopdf.exe` в системе, чтобы убедиться, что установлена необходимая программа.
* В случае успешной конвертации функция записывает PDF-файл в указанный путь.
* В случае ошибки функция записывает в лог информацию об ошибке.

**Примеры**:

```python
from src.utils.pdf import PDFUtils
from pathlib import Path

# Преобразование HTML-контента в PDF
html_content = "<html><body><h1>Пример HTML-кода</h1></body></html>"
pdf_file_path = Path('output.pdf')
PDFUtils.save_pdf_pdfkit(html_content, pdf_file_path)

# Преобразование HTML-файла в PDF
html_file_path = Path('index.html')
pdf_file_path = Path('output.pdf')
PDFUtils.save_pdf_pdfkit(html_file_path, pdf_file_path)
```

#### `save_pdf_fpdf(data: str, pdf_file: str | Path) -> bool`

**Назначение**: Сохранить текст в PDF с использованием библиотеки `FPDF`.

**Параметры**:
* `data (str)`: Текст, который необходимо сохранить в PDF.
* `pdf_file (str | Path)`: Путь к сохраняемому PDF-файлу.

**Возвращает**:
* `bool`: `True`, если PDF успешно сохранен, иначе `False`.

**Как работает функция**: 
* Функция `save_pdf_fpdf` использует библиотеку `FPDF` для создания PDF-файла из текста.
* Функция добавляет страницу, устанавливает автоматическую разбивку страницы.
* Загружает шрифты из `fonts.json` файла.
* Устанавливает шрифт по умолчанию и добавляет текст на страницу.
* Сохраняет PDF-файл в указанном пути.

**Примеры**:
```python
from src.utils.pdf import PDFUtils
from pathlib import Path

# Преобразование текста в PDF
text_content = "Пример текста для PDF-файла."
pdf_file_path = Path('output.pdf')
PDFUtils.save_pdf_fpdf(text_content, pdf_file_path)
```


#### `save_pdf_weasyprint(data: str | Path, pdf_file: str | Path) -> bool`

**Назначение**: Сохранить HTML-контент или файл в PDF с использованием библиотеки `WeasyPrint`.

**Параметры**:
* `data (str | Path)`: HTML-контент или путь к HTML-файлу.
* `pdf_file (str | Path)`: Путь к сохраняемому PDF-файлу.

**Возвращает**:
* `bool`: `True` если PDF успешно сохранен, иначе `False`.

**Как работает функция**: 
* Функция `save_pdf_weasyprint` использует библиотеку `WeasyPrint` для преобразования HTML-контента или файлов в PDF.
* Функция проверяет, является ли `data` строкой или путем к файлу.
* В случае успешной конвертации функция записывает PDF-файл в указанный путь.
* В случае ошибки функция записывает в лог информацию об ошибке.

**Примеры**:
```python
from src.utils.pdf import PDFUtils
from pathlib import Path

# Преобразование HTML-контента в PDF
html_content = "<html><body><h1>Пример HTML-кода</h1></body></html>"
pdf_file_path = Path('output.pdf')
PDFUtils.save_pdf_weasyprint(html_content, pdf_file_path)

# Преобразование HTML-файла в PDF
html_file_path = Path('index.html')
pdf_file_path = Path('output.pdf')
PDFUtils.save_pdf_weasyprint(html_file_path, pdf_file_path)
```

#### `save_pdf_xhtml2pdf(data: str | Path, pdf_file: str | Path) -> bool`

**Назначение**: Сохранить HTML-контент или файл в PDF с использованием библиотеки `xhtml2pdf`.

**Параметры**:
* `data (str | Path)`: HTML-контент или путь к HTML-файлу.
* `pdf_file (str | Path)`: Путь к сохраняемому PDF-файлу.

**Возвращает**:
* `bool`: `True` если PDF успешно сохранен, иначе `False`.

**Как работает функция**: 
* Функция `save_pdf_xhtml2pdf` использует библиотеку `xhtml2pdf` для преобразования HTML-контента или файлов в PDF.
* Функция открывает файл для записи в двоичном режиме.
* В случае успешной конвертации функция записывает PDF-файл в указанный путь.
* В случае ошибки функция записывает в лог информацию об ошибке.

**Примеры**:
```python
from src.utils.pdf import PDFUtils
from pathlib import Path

# Преобразование HTML-контента в PDF
html_content = "<html><body><h1>Пример HTML-кода</h1></body></html>"
pdf_file_path = Path('output.pdf')
PDFUtils.save_pdf_xhtml2pdf(html_content, pdf_file_path)

# Преобразование HTML-файла в PDF
html_file_path = Path('index.html')
pdf_file_path = Path('output.pdf')
PDFUtils.save_pdf_xhtml2pdf(html_file_path, pdf_file_path)
```

#### `html2pdf(html_str: str, pdf_file: str | Path) -> bool | None`

**Назначение**: Преобразует HTML-контент в PDF-файл с использованием `WeasyPrint`.

**Параметры**:
* `html_str (str)`: HTML-контент.
* `pdf_file (str | Path)`: Путь к сохраняемому PDF-файлу.

**Возвращает**:
* `bool | None`: `True`, если PDF успешно сохранен, иначе `None`.

**Как работает функция**: 
* Функция `html2pdf` использует библиотеку `WeasyPrint` для преобразования HTML-контента в PDF.
* Функция пытается выполнить конвертацию, и в случае успешной конвертации записывает PDF-файл в указанный путь.
* В случае ошибки функция печатает сообщение об ошибке и возвращает `None`.


**Примеры**:
```python
from src.utils.pdf import PDFUtils
from pathlib import Path

# Преобразование HTML-контента в PDF
html_content = "<html><body><h1>Пример HTML-кода</h1></body></html>"
pdf_file_path = Path('output.pdf')
result = PDFUtils.html2pdf(html_content, pdf_file_path)
if result:
    print("PDF успешно сохранен.")
else:
    print("Ошибка при конвертации в PDF.")
```


#### `pdf_to_html(pdf_file: str | Path, html_file: str | Path) -> bool`

**Назначение**: Конвертирует PDF-файл в HTML-файл.

**Параметры**:
* `pdf_file (str | Path)`: Путь к исходному PDF-файлу.
* `html_file (str | Path)`: Путь к сохраняемому HTML-файлу.

**Возвращает**:
* `bool`: `True`, если конвертация прошла успешно, иначе `False`.

**Как работает функция**: 
* Функция `pdf_to_html` извлекает текст из PDF-файла с помощью библиотеки `pdfminer.high_level`.
* Затем функция записывает полученный текст в HTML-файл, создавая простую HTML-структуру.
* В случае успешной конвертации функция печатает сообщение об успешной конвертации.
* В случае ошибки функция печатает сообщение об ошибке и возвращает `False`.

**Примеры**:
```python
from src.utils.pdf import PDFUtils
from pathlib import Path

# Преобразование PDF-файла в HTML
pdf_file_path = Path('document.pdf')
html_file_path = Path('output.html')
PDFUtils.pdf_to_html(pdf_file_path, html_file_path)
```

#### `dict2pdf(data: Any, file_path: str | Path) -> None`

**Назначение**: Сохранить данные словаря в PDF-файл.

**Параметры**:
* `data (dict | SimpleNamespace)`: Словарь, который нужно конвертировать в PDF.
* `file_path (str | Path)`: Путь к выходному PDF-файлу.

**Возвращает**:
* `None`

**Как работает функция**: 
* Функция `dict2pdf` преобразует словарь в PDF-файл, используя библиотеку `reportlab`.
* Функция создает холст для PDF-файла и устанавливает шрифт.
* Затем она итерирует по парам ключ-значение словаря, рисует текст на холсте и переходит на новую строку.
* Если места на странице не хватает, функция создает новую страницу.
* В конце функция сохраняет PDF-файл.

**Примеры**:
```python
from src.utils.pdf import PDFUtils
from pathlib import Path

# Преобразование словаря в PDF
data = {'имя': 'Иван', 'возраст': 30, 'город': 'Москва'}
file_path = Path('data.pdf')
PDFUtils.dict2pdf(data, file_path)
```

## Параметры класса

* Нет параметров класса. 

## Примеры

### Пример преобразования HTML-контента в PDF:

```python
from src.utils.pdf import PDFUtils

html_content = """
<!DOCTYPE html>
<html>
<head>
<title>Пример HTML-кода</title>
</head>
<body>
<h1>Заголовок</h1>
<p>Текст страницы.</p>
</body>
</html>
"""

pdf_file_path = "output.pdf"

PDFUtils.save_pdf_pdfkit(html_content, pdf_file_path)
```

### Пример преобразования PDF-файла в HTML:

```python
from src.utils.pdf import PDFUtils

pdf_file_path = "document.pdf"
html_file_path = "output.html"

PDFUtils.pdf_to_html(pdf_file_path, html_file_path)
```

### Пример сохранения данных словаря в PDF:

```python
from src.utils.pdf import PDFUtils

data = {'имя': 'Иван', 'возраст': 30, 'город': 'Москва'}
file_path = 'data.pdf'
PDFUtils.dict2pdf(data, file_path)