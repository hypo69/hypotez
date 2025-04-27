# Модуль для работы с PDF-файлами

## Обзор

Модуль предоставляет набор инструментов для работы с PDF-файлами. Он содержит функции для преобразования HTML-контента или файлов в PDF с использованием различных библиотек, таких как `pdfkit`, `FPDF`, `WeasyPrint` и `xhtml2pdf`. 

## Детали

Модуль используется для реализации функциональности, связанной с обработкой PDF-файлов в проекте `hypotez`. 
Он позволяет конвертировать HTML-контент или файлы в PDF, а также извлекать текст из PDF-файлов.

## Классы

### `PDFUtils`

**Описание**: Класс для работы с PDF-файлами, предоставляющий методы для сохранения HTML-контента в PDF с использованием различных библиотек.

**Методы**:

#### `save_pdf_pdfkit(data: str | Path, pdf_file: str | Path) -> bool`

**Цель**: Сохранить HTML-контент или файл в PDF с использованием библиотеки `pdfkit`.

**Параметры**:

- `data (str | Path)`: HTML-контент или путь к HTML-файлу.
- `pdf_file (str | Path)`: Путь к сохраняемому PDF-файлу.

**Возвращает**:

- `bool`: `True` если PDF успешно сохранен, иначе `False`.

**Возможные исключения**:

- `pdfkit.PDFKitError`: Ошибка генерации PDF через `pdfkit`.
- `OSError`: Ошибка доступа к файлу.

**Как работает**:

- Функция использует библиотеку `pdfkit` для преобразования HTML в PDF. 
- Она проверяет наличие `wkhtmltopdf.exe` по заданному пути и использует его для генерации PDF-файла. 
- Если файл не найден, выводится сообщение об ошибке.

**Примеры**:

```python
from src.utils.pdf import PDFUtils

# Сохранение HTML-контента в PDF
html_content = "<html><body><h1>Пример</h1></body></html>"
pdf_file = "example.pdf"
PDFUtils.save_pdf_pdfkit(html_content, pdf_file)

# Сохранение HTML-файла в PDF
html_file = "example.html"
pdf_file = "example.pdf"
PDFUtils.save_pdf_pdfkit(html_file, pdf_file)
```

#### `save_pdf_fpdf(data: str, pdf_file: str | Path) -> bool`

**Цель**: Сохранить текст в PDF с использованием библиотеки FPDF.

**Параметры**:

- `data (str)`: Текст, который необходимо сохранить в PDF.
- `pdf_file (str | Path)`: Путь к сохраняемому PDF-файлу.

**Возвращает**:

- `bool`: `True`, если PDF успешно сохранен, иначе `False`.

**Как работает**:

- Функция использует библиотеку `FPDF` для создания PDF-файла. 
- Она добавляет шрифты из `fonts.json` к PDF-файлу. 
- Затем текст добавляется на страницу, и PDF сохраняется в указанный файл.

**Примеры**:

```python
from src.utils.pdf import PDFUtils

text_data = "Пример текста для сохранения в PDF."
pdf_file = "example.pdf"
PDFUtils.save_pdf_fpdf(text_data, pdf_file)
```

#### `save_pdf_weasyprint(data: str | Path, pdf_file: str | Path) -> bool`

**Цель**: Сохранить HTML-контент или файл в PDF с использованием библиотеки `WeasyPrint`.

**Параметры**:

- `data (str | Path)`: HTML-контент или путь к HTML-файлу.
- `pdf_file (str | Path)`: Путь к сохраняемому PDF-файлу.

**Возвращает**:

- `bool`: `True` если PDF успешно сохранен, иначе `False`.

**Как работает**:

- Функция использует библиотеку `WeasyPrint` для преобразования HTML в PDF. 
- Она создает объект HTML из заданного контента или файла и записывает его в PDF-файл.

**Примеры**:

```python
from src.utils.pdf import PDFUtils

html_content = "<html><body><h1>Пример</h1></body></html>"
pdf_file = "example.pdf"
PDFUtils.save_pdf_weasyprint(html_content, pdf_file)

html_file = "example.html"
pdf_file = "example.pdf"
PDFUtils.save_pdf_weasyprint(html_file, pdf_file)
```

#### `save_pdf_xhtml2pdf(data: str | Path, pdf_file: str | Path) -> bool`

**Цель**: Сохранить HTML-контент или файл в PDF с использованием библиотеки `xhtml2pdf`.

**Параметры**:

- `data (str | Path)`: HTML-контент или путь к HTML-файлу.
- `pdf_file (str | Path)`: Путь к сохраняемому PDF-файлу.

**Возвращает**:

- `bool`: `True` если PDF успешно сохранен, иначе `False`.

**Как работает**:

- Функция использует библиотеку `xhtml2pdf` для преобразования HTML в PDF. 
- Она открывает файл для записи в двоичном режиме и генерирует PDF-файл из HTML-данных.

**Примеры**:

```python
from src.utils.pdf import PDFUtils

html_content = "<html><body><h1>Пример</h1></body></html>"
pdf_file = "example.pdf"
PDFUtils.save_pdf_xhtml2pdf(html_content, pdf_file)

html_file = "example.html"
pdf_file = "example.pdf"
PDFUtils.save_pdf_xhtml2pdf(html_file, pdf_file)
```

#### `html2pdf(html_str: str, pdf_file: str | Path) -> bool | None`

**Цель**: Преобразовать HTML-контент в PDF-файл с использованием WeasyPrint.

**Параметры**:

- `html_str (str)`: HTML-контент.
- `pdf_file (str | Path)`: Путь к сохраняемому PDF-файлу.

**Возвращает**:

- `bool | None`: `True`, если преобразование прошло успешно, иначе `None`.

**Как работает**:

- Функция использует библиотеку `WeasyPrint` для преобразования HTML-контента в PDF-файл. 
- Она записывает результат в указанный файл.

**Примеры**:

```python
from src.utils.pdf import PDFUtils

html_content = "<html><body><h1>Пример</h1></body></html>"
pdf_file = "example.pdf"
result = PDFUtils.html2pdf(html_content, pdf_file)

if result:
    print("PDF успешно сохранен.")
else:
    print("Ошибка при преобразовании в PDF.")
```

#### `pdf_to_html(pdf_file: str | Path, html_file: str | Path) -> bool`

**Цель**: Конвертирует PDF-файл в HTML-файл.

**Параметры**:

- `pdf_file (str | Path)`: Путь к исходному PDF-файлу.
- `html_file (str | Path)`: Путь к сохраняемому HTML-файлу.

**Возвращает**:

- `bool`: `True`, если конвертация прошла успешно, иначе `False`.

**Как работает**:

- Функция извлекает текст из PDF-файла с использованием `pdfminer`. 
- Затем она создает HTML-файл, содержащий извлеченный текст.

**Примеры**:

```python
from src.utils.pdf import PDFUtils

pdf_file = "example.pdf"
html_file = "example.html"
result = PDFUtils.pdf_to_html(pdf_file, html_file)

if result:
    print("HTML успешно сохранен.")
else:
    print("Ошибка при конвертации в HTML.")
```

#### `dict2pdf(data: Any, file_path: str | Path) -> None`

**Цель**: Сохранить данные из словаря в PDF-файл.

**Параметры**:

- `data (dict | SimpleNamespace)`: Словарь, который необходимо преобразовать в PDF.
- `file_path (str | Path)`: Путь к выходному PDF-файлу.

**Возвращает**:

- `None`.

**Как работает**:

- Функция создает объект `canvas.Canvas` и добавляет текст из словаря на страницу. 
- Она использует цикл для перебора элементов словаря и записи их на страницу. 
- Если места на странице недостаточно, создается новая страница.

**Примеры**:

```python
from src.utils.pdf import PDFUtils

data = {"name": "Alice", "age": 30}
pdf_file = "example.pdf"
PDFUtils.dict2pdf(data, pdf_file)
```