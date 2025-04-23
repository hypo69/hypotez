### **Как использовать этот блок кода**
=========================================================================================

Описание
-------------------------
Этот модуль содержит набор утилит для преобразования HTML в различные форматы, такие как escape-последовательности, словари, объекты SimpleNamespace и PDF-файлы. Он также предоставляет функцию для конвертации HTML-файлов в документы Word с использованием LibreOffice.

Шаги выполнения
-------------------------
1. **Установка зависимостей**:
   - Убедитесь, что установлены необходимые библиотеки, такие как `beautifulsoup4`, `lxml`, `xhtml2pdf` и `weasyprint`.
   - Для конвертации в DOCX требуется установленный LibreOffice.

2. **Импорт модуля**:
   - Импортируйте модуль `src.utils.convertors.html` в свой проект.

3. **Использование функций**:
   - Используйте функции `html2escape`, `escape2html`, `html2dict`, `html2ns`, `html2pdf` и `html_to_docx` для выполнения нужных преобразований.

Пример использования
-------------------------

```python
from src.utils.convertors.html import (
    html2escape,
    escape2html,
    html2dict,
    html2ns,
    html2pdf,
    html_to_docx,
)
from pathlib import Path

# Преобразование HTML в escape-последовательности
html = "<p>Hello, world!</p>"
escaped_html = html2escape(html)
print(f"Escaped HTML: {escaped_html}")

# Преобразование escape-последовательностей обратно в HTML
unescaped_html = escape2html(escaped_html)
print(f"Unescaped HTML: {unescaped_html}")

# Преобразование HTML в словарь
html_dict = html2dict("<p>Hello</p><a href='link'>World</a>")
print(f"HTML as dictionary: {html_dict}")

# Преобразование HTML в SimpleNamespace
html_ns = html2ns("<p>Hello</p><a href='link'>World</a>")
print(f"HTML as SimpleNamespace: {html_ns.p}, {html_ns.a}")

# Преобразование HTML в PDF
html_content = "<html><body><h1>Hello, world!</h1></body></html>"
pdf_file = "output.pdf"
if html2pdf(html_content, pdf_file):
    print(f"PDF успешно создан: {pdf_file}")
else:
    print("Не удалось создать PDF")

# Преобразование HTML-файла в DOCX
html_file = "input.html"
docx_file = "output.docx"
# Создайте файл input.html для примера
Path(html_file).write_text(html_content)
if html_to_docx(html_file, docx_file):
    print(f"DOCX успешно создан: {docx_file}")
else:
    print("Не удалось создать DOCX")