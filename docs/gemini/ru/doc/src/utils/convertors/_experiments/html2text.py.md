# Модуль для преобразования HTML в текст
## Обзор
Модуль `src.utils.convertors._experiments.html2text.py` содержит функции для преобразования HTML-кода в текстовый формат.
## Подробнее
Данный модуль демонстрирует базовое использование функций `html2text` и `html2text_file` из модуля `src.utils.convertors` для преобразования HTML-кода в текстовый формат.
Модуль считывает HTML-файл `index.html` из директории `html2text` в Google Drive, преобразует его в текст с помощью `html2text` и сохраняет полученный текст в файл `index.txt` в той же директории.
## Функции
### `html2text`
**Назначение**: Функция  преобразует HTML-код в текстовый формат.
**Параметры**:
- `html` (str): Строка с HTML-кодом.
**Возвращает**:
- `str`: Преобразованный текст.
**Как работает функция**:
- Функция `html2text` использует библиотеку `BeautifulSoup4` для обработки HTML-кода. Она удаляет HTML-теги и оставляет только текстовое содержимое. 
**Примеры**:
```python
from src.utils.convertors import html2text

html_code = '<h1>Заголовок</h1><p>Текст</p>'
text = html2text(html_code)
print(text)  # Вывод: Заголовок Текст
```
### `html2text_file`
**Назначение**: Функция  преобразует HTML-файл в текстовый файл.
**Параметры**:
- `file_path` (str | Path): Путь к HTML-файлу.
- `output_file_path` (str | Path): Путь к выходному текстовому файлу.
**Возвращает**:
- `None`.
**Как работает функция**:
- Функция `html2text_file`  считывает HTML-файл, преобразует его в текст с помощью `html2text` и сохраняет полученный текст в указанный файл.
**Примеры**:
```python
from src.utils.convertors import html2text_file

html_file_path = 'path/to/index.html'
output_file_path = 'path/to/index.txt'
html2text_file(html_file_path, output_file_path)
```
## Примеры
```python
from src import gs
from src.utils.convertors import html2text, html2text_file
from src.utils.file import read_text_file, save_text_file

html = read_text_file(gs.path.google_drive / 'html2text' / 'index.html')
text_from_html = html2text(html)
save_text_file(text_from_html, gs.path.google_drive / 'html2text' / 'index.txt')
```
## Внутренние функции
### `read_text_file`
**Назначение**: Функция  считывает содержимое текстового файла.
**Параметры**:
- `file_path` (str | Path): Путь к файлу.
- `as_list` (bool): Если `True`, возвращает список строк.
- `extensions` (Optional[List[str]]): Список расширений файлов для чтения из каталога.
- `chunk_size` (int): Размер чанков для чтения файла в байтах.
**Возвращает**:
- `Generator[str, None, None] | str | None`: Генератор строк, объединенная строка или `None` в случае ошибки.
**Как работает функция**:
- Функция считывает содержимое файла по указанному пути, преобразует его в строку и возвращает.
**Примеры**:
```python
from src.utils.file import read_text_file

file_path = 'path/to/file.txt'
content = read_text_file(file_path)
print(content)
```
### `save_text_file`
**Назначение**: Функция  сохраняет текст в файл.
**Параметры**:
- `text` (str): Текст для записи.
- `file_path` (str | Path): Путь к файлу.
- `mode` (str): Режим открытия файла.
- `encoding` (str): Кодировка файла.
**Возвращает**:
- `None`.
**Как работает функция**:
- Функция открывает файл в указанном режиме и кодировке, записывает в него текст и закрывает файл.
**Примеры**:
```python
from src.utils.file import save_text_file

text = 'Текст для записи'
file_path = 'path/to/file.txt'
save_text_file(text, file_path)