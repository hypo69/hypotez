## Как использовать этот блок кода
=========================================================================================

### Описание
-------------------------
Этот блок кода содержит набор функций для преобразования HTML-кода. Он предоставляет следующие возможности:

* **`html2escape(input_str: str) -> str`**: Преобразует HTML-код в escape-последовательности.
* **`escape2html(input_str: str) -> str`**: Преобразует escape-последовательности обратно в HTML-код.
* **`html2dict(html_str: str) -> Dict[str, str]`**: Преобразует HTML-код в словарь, где ключи - это теги, а значения - их содержимое.
* **`html2ns(html_str: str) -> SimpleNamespace`**: Преобразует HTML-код в объект `SimpleNamespace`, где теги - это атрибуты, а значения - их содержимое.
* **`html2pdf(html_str: str, pdf_file: str | Path) -> bool | None`**: Преобразует HTML-код в PDF-файл с помощью библиотеки `WeasyPrint`. 
* **`html_to_docx(html_file: str, output_docx: Path | str) -> bool`**: Преобразует HTML-файл в документ Word (.docx) с помощью LibreOffice.

### Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**: 
    - `re` (регулярные выражения)
    - `typing` (типизация)
    - `pathlib` (работа с путями)
    - `logger` (модуль логгирования)
    - `types` (работа с типами данных)
    - `html.parser` (работа с HTML-парсером)
    - `xhtml2pdf` (преобразование HTML в PDF)
    - `subprocess` (выполнение командной строки)
    - `weasyprint` (преобразование HTML в PDF)

2. **Определение функций**: 
    - **`html2escape(input_str: str) -> str`**: 
        - Принимает строку HTML-кода в качестве аргумента.
        - Возвращает строку с escape-последовательностями, соответствующими HTML-тегам.
    - **`escape2html(input_str: str) -> str`**: 
        - Принимает строку с escape-последовательностями в качестве аргумента.
        - Возвращает строку с HTML-тегами, полученными из escape-последовательностей.
    - **`html2dict(html_str: str) -> Dict[str, str]`**: 
        - Принимает строку HTML-кода в качестве аргумента.
        - Возвращает словарь, где ключи - это теги HTML, а значения - их содержимое.
        - Для этого использует класс `HTMLToDictParser`, который наследуется от `HTMLParser`.
    - **`html2ns(html_str: str) -> SimpleNamespace`**:
        - Принимает строку HTML-кода в качестве аргумента.
        - Возвращает объект `SimpleNamespace`, где атрибуты - это теги HTML, а значения - их содержимое.
        - Использует функцию `html2dict` для преобразования HTML в словарь.
    - **`html2pdf(html_str: str, pdf_file: str | Path) -> bool | None`**:
        - Принимает строку HTML-кода и путь к выходному PDF-файлу в качестве аргументов.
        - Преобразует HTML в PDF с помощью библиотеки `WeasyPrint`. 
        - Возвращает `True`, если преобразование успешно, и `None` в случае ошибки. 
    - **`html_to_docx(html_file: str, output_docx: Path | str) -> bool`**:
        - Принимает путь к входному HTML-файлу и путь к выходному DOCX-файлу в качестве аргументов.
        - Преобразует HTML в DOCX с помощью LibreOffice. 
        - Возвращает `True`, если преобразование успешно, и `False` в случае ошибки.

### Пример использования
-------------------------
```python
from src.utils.convertors.html import html2escape, escape2html, html2dict, html2ns, html2pdf, html_to_docx

# Преобразование HTML в escape-последовательности
html_code = "<p>Hello, world!</p>"
escaped_html = html2escape(html_code)
print(escaped_html)  # Вывод: &lt;p&gt;Hello, world!&lt;/p&gt;

# Преобразование escape-последовательностей в HTML
escaped_html = "&lt;p&gt;Hello, world!&lt;/p&gt;"
html_code = escape2html(escaped_html)
print(html_code)  # Вывод: <p>Hello, world!</p>

# Преобразование HTML в словарь
html_code = "<p>Hello</p><a href='link'>World</a>"
html_dict = html2dict(html_code)
print(html_dict)  # Вывод: {'p': 'Hello', 'a': 'World'}

# Преобразование HTML в SimpleNamespace
html_code = "<p>Hello</p><a href='link'>World</a>"
html_ns = html2ns(html_code)
print(html_ns.p)  # Вывод: Hello
print(html_ns.a)  # Вывод: World

# Преобразование HTML в PDF
html_code = "<p>This is a sample HTML document.</p>"
pdf_file = "output.pdf"
result = html2pdf(html_code, pdf_file)
if result:
    print(f"PDF file {pdf_file} successfully created.")
else:
    print(f"Error during PDF generation.")

# Преобразование HTML в DOCX
html_file = "input.html"
docx_file = "output.docx"
result = html_to_docx(html_file, docx_file)
if result:
    print(f"DOCX file {docx_file} successfully created.")
else:
    print(f"Error during DOCX generation.")
```