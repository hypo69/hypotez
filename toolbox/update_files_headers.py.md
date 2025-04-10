# Модуль для обновления заголовков файлов

## Обзор

Модуль `update_files_headers.py` предназначен для автоматического добавления или обновления заголовков в Python-файлах проекта `hypotez`. Он обеспечивает единообразие структуры файлов, добавляя информацию о кодировке, интерпретаторе и метаданные модуля. Скрипт может быть запущен в различных режимах, включая принудительное обновление и очистку существующих заголовков.

## Подробнее

Скрипт выполняет следующие основные функции:

1.  **Поиск корневой директории проекта**: Определяет корень проекта `hypotez` для правильной работы с относительными путями.
2.  **Добавление/замена заголовков**: Добавляет или заменяет строку кодировки, строки с указанием интерпретатора для Windows и Linux, а также строку документации модуля.
3.  **Режим работы**: Устанавливает режим работы проекта (в данном случае, `development`).
4.  **Очистка заголовков**: Удаляет существующие заголовки, чтобы заменить их новыми или привести к стандартному виду.

## Функции

### `find_project_root`

```python
def find_project_root(start_path: Path, project_root_folder: str) -> Path:
    """Find the project root directory by searching for the specified folder."""
```

**Назначение**:
Функция осуществляет поиск корневой директории проекта, начиная с указанного пути.

**Параметры**:

*   `start_path` (Path): Начальный путь для поиска корневой директории.
*   `project_root_folder` (str): Название папки, которая идентифицирует корень проекта.

**Возвращает**:

*   `Path`: Путь к корневой директории проекта.

**Вызывает исключения**:

*   `FileNotFoundError`: Если корневая папка проекта не найдена.

**Как работает функция**:

Функция поднимается вверх по дереву директорий, начиная с `start_path`, и проверяет наличие папки `project_root_folder` в каждой директории. Если папка найдена, функция возвращает путь к этой папке. Если достигнут корень файловой системы и папка не найдена, вызывается исключение `FileNotFoundError`.

**Примеры**:

```python
from pathlib import Path
start_path = Path('./')
project_root_folder = 'hypotez'
root_path = find_project_root(start_path, project_root_folder)
print(root_path)
```

### `get_interpreter_paths`

```python
def get_interpreter_paths(project_root: Path) -> tuple:
    """Returns paths to Python interpreters for Windows and Linux/macOS."""
```

**Назначение**:
Функция возвращает пути к интерпретаторам Python для операционных систем Windows и Linux/macOS.

**Параметры**:

*   `project_root` (Path): Путь к корневой директории проекта.

**Возвращает**:

*   `tuple`: Кортеж, содержащий пути к интерпретаторам для Windows и Linux. В частности, возвращаются пути к `w_venv_interpreter`, строковый литерал `'py'`, `linux_venv_interpreter`, и `'/usr/bin/python'`.

**Как работает функция**:

Функция определяет пути к интерпретаторам Python, находящимся в виртуальном окружении проекта. Она возвращает эти пути в виде кортежа, который может быть использован для добавления или обновления строк интерпретатора в файлах проекта.

**Примеры**:

```python
from pathlib import Path
project_root = Path('./')
w_venv_interpreter, _, linux_venv_interpreter, _ = get_interpreter_paths(project_root)
print(f"Windows interpreter: {w_venv_interpreter}")
print(f"Linux interpreter: {linux_venv_interpreter}")
```

### `add_or_replace_file_header`

```python
def add_or_replace_file_header(file_path: str, project_root: Path, force_update: bool):
    """Adds or replaces header, interpreter lines, and module docstring."""
```

**Назначение**:
Функция добавляет или заменяет заголовок, строки интерпретатора и строку документации модуля в указанном файле.

**Параметры**:

*   `file_path` (str): Путь к файлу, в котором нужно добавить или заменить заголовок.
*   `project_root` (Path): Путь к корневой директории проекта.
*   `force_update` (bool): Флаг, указывающий, следует ли принудительно обновить заголовок, даже если он уже существует.

**Как работает функция**:

1.  Функция формирует строки заголовка, кодировки, интерпретатора и документации модуля на основе пути к файлу и корневой директории проекта.
2.  Читает содержимое файла и фильтрует строки, удаляя существующие строки заголовков, кодировки и интерпретатора.
3.  Проверяет, требуется ли обновление файла на основе флага `force_update` и сравнения существующих строк с новыми.
4.  Если требуется обновление, функция записывает новые строки заголовка, кодировки, интерпретатора и документации в начало файла, а затем добавляет отфильтрованные строки из исходного файла.
5.  Если обновление не требуется, функция выводит сообщение о том, что файл не нуждается в обновлении.

**Примеры**:

```python
from pathlib import Path
file_path = 'example.py'
project_root = Path('./')
force_update = True
add_or_replace_file_header(file_path, project_root, force_update)
```

### `clean`

```python
def clean(file_path: str):
    """Removes specified header lines from the file and replaces them with empty lines."""
```

**Назначение**:
Функция удаляет указанные строки заголовка из файла и заменяет их пустыми строками.

**Параметры**:

*   `file_path` (str): Путь к файлу, из которого нужно удалить строки заголовка.

**Как работает функция**:

1.  Функция определяет префиксы строк, которые нужно удалить (например, строки с информацией о файле, кодировке, интерпретаторе и документации модуля).
2.  Читает содержимое файла и фильтрует строки, заменяя строки, начинающиеся с определенных префиксов, на пустые строки.
3.  Записывает отфильтрованные строки обратно в файл, удаляя, таким образом, строки заголовка.

**Примеры**:

```python
file_path = 'example.py'
clean(file_path)
```

### `traverse_and_update`

```python
def traverse_and_update(directory: Path, force_update: bool):
    """Traverses the directory and updates headers in Python files."""
```

**Назначение**:
Функция обходит указанную директорию и обновляет заголовки во всех Python-файлах.

**Параметры**:

*   `directory` (Path): Путь к директории, которую нужно обойти.
*   `force_update` (bool): Флаг, указывающий, следует ли принудительно обновить заголовки.

**Как работает функция**:

1.  Функция использует `os.walk` для обхода директории и ее поддиректорий.
2.  Для каждого файла с расширением `.py` вызывает функцию `add_or_replace_file_header` для добавления или замены заголовка.
3.  Исключает из обхода директории, указанные в списке `EXCLUDE_DIRS`.

**Примеры**:

```python
from pathlib import Path
directory = Path('./')
force_update = True
traverse_and_update(directory, force_update)
```

### `traverse_and_clean`

```python
def traverse_and_clean(directory: Path):
    """Traverses the directory and cleans specified headers from Python files."""
```

**Назначение**:
Функция обходит указанную директорию и очищает указанные заголовки из всех Python-файлов.

**Параметры**:

*   `directory` (Path): Путь к директории, которую нужно обойти.

**Как работает функция**:

1.  Функция использует `os.walk` для обхода директории и ее поддиректорий.
2.  Для каждого файла с расширением `.py` вызывает функцию `clean` для удаления строк заголовка.
3.  Исключает из обхода директории, указанные в списке `EXCLUDE_DIRS`.

**Примеры**:

```python
from pathlib import Path
directory = Path('./')
traverse_and_clean(directory)
```

### `main`

```python
def main():
    """Main function to execute the script."""
```

**Назначение**:
Главная функция для выполнения скрипта.

**Как работает функция**:

1.  Определяет корневую директорию проекта.
2.  Вызывает `traverse_and_update` с параметром `True`, чтобы принудительно обновить все заголовки.

**Примеры**:

```python
main()