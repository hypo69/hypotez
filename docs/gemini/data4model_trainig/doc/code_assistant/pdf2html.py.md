# Модуль `pdf2html`

## Обзор

Модуль `pdf2html` предназначен для конвертации PDF-файлов в HTML-формат.

## Подробней

Модуль содержит код, который использует утилиты из `src.utils.pdf` для преобразования PDF-файла в HTML-файл. Это может быть полезно для дальнейшей обработки содержимого PDF-файла в HTML-формате.

## Функции

### `pdf2html`

```python
def pdf2html(pdf_file,html_file):
    """ """
    PDFUtils.pdf_to_html(pdf_file, html_file)
```

**Назначение**: Конвертирует PDF-файл в HTML-файл.

**Параметры**:
- `pdf_file`: Путь к PDF-файлу.
- `html_file`: Путь для сохранения HTML-файла.

**Как работает функция**:
- Вызывает метод `PDFUtils.pdf_to_html` для выполнения конвертации.

## Переменные

*   `pdf_file` (Path): Путь к PDF-файлу, который нужно конвертировать.
*   `html_file` (Path): Путь для сохранения сгенерированного HTML-файла.

## Используемые модули

*   `src.utils.pdf`: Для работы с PDF файлами и их преобразования.

## Запуск и использование

Для преобразования PDF-файла в HTML необходимо запустить скрипт, указав пути к исходному PDF-файлу и будущему HTML-файлу.

```python
pdf_file = gs.path.root / 'assets' / 'materials' / '101_BASIC_Computer_Games_Mar75.pdf'
html_file = gs.path.root / 'assets' / 'materials' / '101_BASIC_Computer_Games_Mar75.html'

pdf2html(pdf_file, html_file)
```

В данном примере предполагается, что файл `101_BASIC_Computer_Games_Mar75.pdf` находится в директории `assets/materials` относительно корня проекта, а сгенерированный HTML-файл будет сохранен в ту же директорию.

## Замечания

Модуль предназначен для экспериментов, поэтому код может быть неполным и не содержать дополнительных функций. В коде отсутствует обработка исключений и docstring для основной функции.
```python
""" """
```
Данный код указывает на то, что для функции `pdf2html` не предоставлено описание.