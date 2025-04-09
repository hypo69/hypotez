# Модуль конвертации PDF в HTML

## Обзор

Модуль предназначен для конвертации PDF-файлов в HTML-формат. В основном, он использует утилиты для работы с PDF из модуля `src.utils.pdf` и глобальные настройки из модуля `src.gs`.

## Подробней

Этот модуль предоставляет функцию `pdf2html`, которая принимает путь к PDF-файлу и путь для сохранения HTML-файла. Затем он использует метод `pdf_to_html` из класса `PDFUtils` для выполнения конвертации.

## Функции

### `pdf2html`

```python
def pdf2html(pdf_file, html_file):
    """ """
    PDFUtils.pdf_to_html(pdf_file, html_file)
```

**Назначение**: Конвертирует PDF-файл в HTML-файл.

**Параметры**:
- `pdf_file` (str): Путь к PDF-файлу, который необходимо конвертировать.
- `html_file` (str): Путь для сохранения сгенерированного HTML-файла.

**Возвращает**: Ничего (None). Функция выполняет конвертацию и сохраняет результат в указанный HTML-файл.

**Как работает функция**:

1. Функция `pdf2html` принимает два параметра: `pdf_file` и `html_file`, представляющие собой пути к исходному PDF-файлу и целевому HTML-файлу соответственно.
2. Функция вызывает метод `PDFUtils.pdf_to_html`, передавая ему параметры `pdf_file` и `html_file`. Этот метод выполняет фактическую конвертацию PDF в HTML и сохраняет результат.

```ascii
   Начало
     ↓
   PDFUtils.pdf_to_html(pdf_file, html_file)
     ↓
   Конец
```

**Примеры**:
```python
pdf_file = gs.path.root / 'assets' / 'materials' / '101_BASIC_Computer_Games_Mar75.pdf'
html_file = gs.path.root / 'assets' / 'materials' / '101_BASIC_Computer_Games_Mar75.html'

pdf2html(pdf_file, html_file)
```
В этом примере `pdf_file` указывает на PDF-файл, который нужно конвертировать, а `html_file` — на место, где будет сохранён HTML-файл.

```python
from pathlib import Path
pdf_file = Path('/path/to/your/pdf_file.pdf')
html_file = Path('/path/to/your/html_file.html')

pdf2html(pdf_file, html_file)
```

В этом примере показано использование объектов `Path` из модуля `pathlib` для указания путей к файлам.

```python
import os
pdf_file = os.path.join('/path/to/your', 'pdf_file.pdf')
html_file = os.path.join('/path/to/your', 'html_file.html')

pdf2html(pdf_file, html_file)
```

В этом примере показано использование функции `os.path.join` для формирования путей к файлам.