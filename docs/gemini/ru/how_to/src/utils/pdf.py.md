## Как использовать класс PDFUtils 
=========================================================================================

Описание
-------------------------
Класс `PDFUtils` предоставляет набор статических методов для преобразования HTML-контента или файлов в PDF, используя различные библиотеки.  

Шаги выполнения
-------------------------
1. **Инициализация:**  Импортируйте класс `PDFUtils` из модуля `src.utils.pdf`.
2. **Выбор метода:** Выберите один из методов класса `PDFUtils`, соответствующий вашему сценарию:
    - `save_pdf_pdfkit(data, pdf_file)`: Использует библиотеку `pdfkit` для преобразования HTML-контента или файла в PDF. 
    - `save_pdf_fpdf(data, pdf_file)`: Использует библиотеку `FPDF` для преобразования текста в PDF. 
    - `save_pdf_weasyprint(data, pdf_file)`: Использует библиотеку `WeasyPrint` для преобразования HTML-контента или файла в PDF. 
    - `save_pdf_xhtml2pdf(data, pdf_file)`: Использует библиотеку `xhtml2pdf` для преобразования HTML-контента или файла в PDF.
    - `html2pdf(html_str, pdf_file)`: Преобразует HTML-контент в PDF-файл с использованием библиотеки `WeasyPrint`.
    - `pdf_to_html(pdf_file, html_file)`: Конвертирует PDF-файл в HTML-файл.
    - `dict2pdf(data, file_path)`: Сохраняет данные из словаря в PDF-файл.
3. **Вызов метода:**  Передайте HTML-контент или файл, а также путь к выходному PDF-файлу в качестве аргументов метода. 
4. **Обработка результата:** Метод возвращает `True`, если PDF успешно сохранен, и `False` в противном случае.

Пример использования
-------------------------

```python
from src.utils.pdf import PDFUtils 

# Преобразование HTML-контента в PDF с использованием pdfkit
html_content = "<html><body><h1>Заголовок</h1><p>Пример текста</p></body></html>"
pdf_file_path = "output.pdf"
result = PDFUtils.save_pdf_pdfkit(html_content, pdf_file_path)
if result:
    print(f"PDF успешно сохранен: {pdf_file_path}")
else:
    print("Ошибка при сохранении PDF")

# Преобразование текста в PDF с использованием FPDF
text = "Пример текста для преобразования в PDF"
pdf_file_path = "output_fpdf.pdf"
result = PDFUtils.save_pdf_fpdf(text, pdf_file_path)
if result:
    print(f"PDF успешно сохранен: {pdf_file_path}")
else:
    print("Ошибка при сохранении PDF")

# Преобразование HTML-файла в PDF с использованием WeasyPrint
html_file_path = "index.html"
pdf_file_path = "output_weasyprint.pdf"
result = PDFUtils.save_pdf_weasyprint(html_file_path, pdf_file_path)
if result:
    print(f"PDF успешно сохранен: {pdf_file_path}")
else:
    print("Ошибка при сохранении PDF")

# Сохранение словаря в PDF-файл
data = {"Имя": "Иван", "Возраст": 30, "Город": "Москва"}
file_path = "dict_output.pdf"
PDFUtils.dict2pdf(data, file_path)
```