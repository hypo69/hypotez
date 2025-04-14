# Модуль конвертации PDF в HTML

## Обзор

Модуль предназначен для конвертации PDF-файлов в HTML-формат. Он использует библиотеку `PDFUtils` для выполнения преобразования.

## Подробнее

Данный модуль предоставляет функцию `pdf2html`, которая принимает путь к PDF-файлу и путь для сохранения HTML-файла.  Модуль использует функциональность из `src.utils.pdf.PDFUtils`, чтобы выполнить фактическое преобразование.

## Функции

### `pdf2html`

**Назначение**: Конвертирует PDF-файл в HTML-файл.

**Параметры**:
- `pdf_file` (str): Путь к исходному PDF-файлу.
- `html_file` (str): Путь для сохранения сконвертированного HTML-файла.

**Возвращает**:
- `None`: Функция ничего не возвращает.

**Вызывает исключения**:
- Отсутствуют явные обработки исключений в предоставленном коде.

**Как работает функция**:
- Функция `pdf2html` принимает пути к PDF и HTML файлам.
- Она вызывает метод `pdf_to_html` из класса `PDFUtils`, передавая ему пути к файлам для выполнения конвертации.
- Результат конвертации сохраняется в указанном HTML-файле.

**Примеры**:

```python
import gs
from src.utils.pdf import PDFUtils

def pdf2html(pdf_file: str, html_file: str) -> None:
    """Конвертирует PDF-файл в HTML-файл.

    Args:
        pdf_file (str): Путь к исходному PDF-файлу.
        html_file (str): Путь для сохранения сконвертированного HTML-файла.

    Returns:
        None
    """
    PDFUtils.pdf_to_html(pdf_file, html_file)

pdf_file = gs.path.root / 'assets' / 'materials' / '101_BASIC_Computer_Games_Mar75.pdf'
html_file = gs.path.root / 'assets' / 'materials' / '101_BASIC_Computer_Games_Mar75.html'

pdf2html(pdf_file, html_file)
```

### Переменные модуля

- `pdf_file`: Путь к исходному PDF-файлу, который будет конвертирован. Указывает на файл `'101_BASIC_Computer_Games_Mar75.pdf'`, расположенный в директории `assets/materials`.
- `html_file`: Путь для сохранения сконвертированного HTML-файла. Указывает на файл `'101_BASIC_Computer_Games_Mar75.html'`, расположенный в директории `assets/materials`.