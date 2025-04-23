### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Модуль `src.utils.pdf` предоставляет статические методы класса `PDFUtils` для преобразования HTML-контента, файлов, текста и словарей в PDF-файлы, а также для конвертации PDF-файлов в HTML-файлы. Он использует различные библиотеки, такие как `pdfkit`, `fpdf`, `WeasyPrint` и `xhtml2pdf` для создания PDF, а также `pdfminer` для извлечения текста из PDF.

Шаги выполнения
-------------------------
1. **Импорт модуля**: Импортируйте класс `PDFUtils` из модуля `src.utils.pdf`.
2. **Использование статических методов**: Вызовите один из статических методов класса `PDFUtils` для выполнения нужного преобразования:
    - `save_pdf_pdfkit`: Сохраняет HTML-контент или файл в PDF, используя библиотеку `pdfkit`.
    - `save_pdf_fpdf`: Сохраняет текст в PDF, используя библиотеку `fpdf`.
    - `save_pdf_weasyprint`: Сохраняет HTML-контент или файл в PDF, используя библиотеку `WeasyPrint`.
    - `save_pdf_xhtml2pdf`: Сохраняет HTML-контент или файл в PDF, используя библиотеку `xhtml2pdf`.
    - `html2pdf`: Преобразует HTML-контент в PDF, используя библиотеку `WeasyPrint`.
    - `pdf_to_html`: Конвертирует PDF-файл в HTML-файл, используя библиотеку `pdfminer`.
    - `dict2pdf`: Сохраняет данные словаря в PDF-файл, используя `reportlab`.

Пример использования
-------------------------

```python
    from pathlib import Path
    from src.utils.pdf import PDFUtils

    # Пример 1: Сохранение HTML-контента в PDF с использованием pdfkit
    html_content = "<html><body><h1>Hello, PDF!</h1></body></html>"
    pdf_file_path = "example_pdfkit.pdf"
    PDFUtils.save_pdf_pdfkit(html_content, pdf_file_path)

    # Пример 2: Сохранение текста в PDF с использованием FPDF
    text_data = "Hello, PDF using FPDF!"
    pdf_file_path = "example_fpdf.pdf"
    PDFUtils.save_pdf_fpdf(text_data, pdf_file_path)

    # Пример 3: Сохранение HTML-файла в PDF с использованием WeasyPrint
    html_file_path = Path("example.html")
    html_file_path.write_text("<html><body><h1>Hello, WeasyPrint!</h1></body></html>", encoding="utf-8")
    pdf_file_path = "example_weasyprint.pdf"
    PDFUtils.save_pdf_weasyprint(html_file_path, pdf_file_path)
    
    # Пример 4: Сохранение HTML-контента в PDF с использованием xhtml2pdf
    html_content = "<html><body><h1>Hello, xhtml2pdf!</h1></body></html>"
    pdf_file_path = "example_xhtml2pdf.pdf"
    PDFUtils.save_pdf_xhtml2pdf(html_content, pdf_file_path)

    # Пример 5: Конвертация PDF в HTML
    pdf_file_path = "example.pdf"  # Сгенерируйте PDF файл сначала
    html_file_path = "example.html"
    PDFUtils.pdf_to_html(pdf_file_path, html_file_path)

    # Пример 6: Сохранение словаря в PDF
    data = {"name": "John", "age": 30, "city": "New York"}
    pdf_file_path = "example_dict.pdf"
    PDFUtils.dict2pdf(data, pdf_file_path)