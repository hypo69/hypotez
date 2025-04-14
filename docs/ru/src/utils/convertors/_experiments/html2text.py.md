# Модуль для конвертации HTML в текст (экспериментальная версия)

## Обзор

Этот модуль содержит экспериментальные функции для преобразования HTML-контента в текст. Он использует сторонние библиотеки для обработки HTML и извлечения текстового содержимого.

## Подробнее

Этот код предназначен для преобразования HTML-файлов в текстовые файлы. Он использует функции из других модулей проекта, таких как `html2text`, `read_text_file` и `save_text_file`. Расположение файла в проекте указывает на то, что это экспериментальная версия конвертора HTML в текст.

## Функции

### `html2text`

```python
from src.utils.convertors import html2text
```

**Назначение**: Преобразует HTML-контент в текст.

**Параметры**:
- Нет явных параметров, так как это импортированная функция.

**Возвращает**:
- Текстовое представление HTML-контента.

**Как работает функция**:

1.  Функция `html2text` принимает HTML-код в качестве входных данных.
2.  HTML преобразуется в удобочитаемый текст с использованием логики, определенной в модуле `src.utils.convertors`.

**Примеры**:
```python
from src.utils.convertors import html2text
html_content = "<p>Hello, world!</p>"
text_content = html2text(html_content)
print(text_content)
```

### `read_text_file`

```python
from src.utils.file import read_text_file
```

**Назначение**: Считывает содержимое текстового файла.

**Параметры**:
- Нет явных параметров, так как это импортированная функция.

**Возвращает**:
- Содержимое файла в виде строки.

**Как работает функция**:

1.  Функция `read_text_file` принимает путь к файлу в качестве входных данных.
2.  Содержимое файла считывается и возвращается в виде строки.
3.  Если файл не найден или происходит ошибка чтения, может быть вызвано исключение.

**Примеры**:
```python
from src.utils.file import read_text_file
file_path = "/path/to/your/file.txt"
text_content = read_text_file(file_path)
print(text_content)
```

### `save_text_file`

```python
from src.utils.file import save_text_file
```

**Назначение**: Сохраняет текст в файл.

**Параметры**:
- Нет явных параметров, так как это импортированная функция.

**Возвращает**:
- Нет возвращаемого значения.

**Как работает функция**:

1.  Функция `save_text_file` принимает текст и путь к файлу в качестве входных данных.
2.  Текст сохраняется в указанный файл.
3.  Если файл не может быть создан или происходит ошибка записи, может быть вызвано исключение.

**Примеры**:
```python
from src.utils.file import save_text_file
text_content = "Hello, world!"
file_path = "/path/to/your/file.txt"
save_text_file(text_content, file_path)
```

### Основной блок кода

```python
import header
from src import gs
from src.utils.convertors import html2text, html2text_file
from src.utils.file import read_text_file, save_text_file

html = read_text_file(gs.path.google_drive / 'html2text' / 'index.html')
text_from_html = html2text(html)
save_text_file(text_from_html, gs.path.google_drive / 'html2text' / 'index.txt')
...
```

**Как работает код**:

1.  Читает HTML-файл `index.html` из указанного места в Google Drive (определяется переменной `gs.path.google_drive`).
2.  Преобразует HTML-содержимое в текст с помощью функции `html2text`.
3.  Сохраняет полученный текст в файл `index.txt` в том же каталоге.

**ASCII flowchart**:

```
Read HTML File --> Convert HTML to Text --> Save Text to File