# Модуль для конвертации HTML в DOCX с использованием LibreOffice
=================================================================

Модуль содержит функцию :func:`html_to_docx`, которая конвертирует HTML-файл в документ Word (.docx) с использованием LibreOffice.

## Обзор

Этот модуль предоставляет функцию для преобразования HTML-файлов в формат DOCX с использованием LibreOffice в качестве конвертера. Он включает обработку ошибок, проверку наличия необходимых файлов и логирование.

## Подробней

Модуль предназначен для автоматического преобразования HTML-файлов в формат DOCX, что может быть полезно для создания документов на основе веб-контента. Он использует LibreOffice в режиме headless (без графического интерфейса) для выполнения конвертации. Важно, чтобы LibreOffice был установлен в системе и его исполняемый файл `soffice` был доступен через системную переменную `PATH`.

## Функции

### `html_to_docx`

**Назначение**: Конвертирует HTML-файл в документ Word (.docx) с использованием LibreOffice.

**Параметры**:
- `html_file` (str): Путь к входному HTML-файлу в виде строки.
- `output_docx` (Path | str): Путь к выходному DOCX-файлу.

**Возвращает**:
- `bool`: `True`, если конвертация прошла успешно, `False` в противном случае.

**Вызывает исключения**:
- `subprocess.CalledProcessError`: Если LibreOffice не смог выполнить конвертацию.
- `FileNotFoundError`: Если исполняемый файл LibreOffice (`soffice`) не найден.
- `Exception`: При возникновении неожиданной ошибки во время конвертации.

**Как работает функция**:

1.  **Проверка существования HTML-файла**: Функция проверяет, существует ли файл, указанный в `html_file`. Если файл не найден, в лог записывается сообщение об ошибке, и функция возвращает `False`.
2.  **Проверка существования директории для выходного файла**: Функция проверяет, существует ли родительская директория для файла, указанного в `output_docx`. Если директория не существует, она создается.
3.  **Формирование команды для LibreOffice**: Функция формирует команду для запуска LibreOffice в режиме headless с указанием входного HTML-файла, формата конвертации (docx:HTML) и директории для сохранения выходного DOCX-файла.
4.  **Выполнение команды LibreOffice**: Функция выполняет команду LibreOffice с использованием `subprocess.run`. Если во время выполнения команды возникает ошибка, она перехватывается, в лог записывается сообщение об ошибке, и функция возвращает `False`.
5.  **Проверка ошибок в процессе конвертации**: После выполнения команды функция проверяет наличие ошибок, записанных в stderr процесса.
6.  **Обработка исключений**: Функция обрабатывает исключения, которые могут возникнуть во время выполнения, такие как `subprocess.CalledProcessError`, `FileNotFoundError` и `Exception`. В случае возникновения исключения, в лог записывается сообщение об ошибке, и функция возвращает `False`.

**Примеры**:

```python
from pathlib import Path
from src.logger import logger

# Пример использования
html_file = "template.html"  # Замените на ваш HTML-файл
output_docx = Path("output_libreoffice.docx")  # Замените на желаемый выходной файл

if html_to_docx(html_file, output_docx):
    print(f"Успешно конвертировано {html_file} в {output_docx} с использованием LibreOffice!")
else:
    print(f"Не удалось конвертировать {html_file} в {output_docx} с использованием LibreOffice.")