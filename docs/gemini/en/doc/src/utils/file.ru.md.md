# Модуль `file.py`

## Обзор

Модуль `file.py` предоставляет набор функций для работы с файлами и директориями, включая обработку больших файлов с помощью генераторов и рекурсивный поиск файлов. Функции хорошо структурированы и имеют ясное назначение. Добавленные функции обработки лишних пробелов и экранирования кавычек улучшают функциональность.

## Более детально

Этот модуль содержит набор инструментов для выполнения различных операций с файлами и директориями. Он включает функции для записи и чтения текстовых файлов, рекурсивного поиска файлов, удаления BOM (Byte Order Mark) и других полезных операций. Модуль разработан для обеспечения удобства и эффективности при работе с файловой системой.

## Функции

### `save_text_file`

**Назначение**: Записывает данные в указанный текстовый файл. Поддерживает запись строк, списков строк и словарей (словари сериализуются в JSON).

```python
def save_text_file(data, file_path, mode='w'):
    """
    Записывает данные в указанный текстовый файл.

    Args:
        data (str | list[str] | dict): Данные для записи в файл. Может быть строкой, списком строк или словарем.
        file_path (str | Path): Путь к файлу, куда нужно записать данные. Может быть строкой или объектом `Path` из библиотеки `pathlib`.
        mode (str, optional): Режим открытия файла. По умолчанию 'w' (запись, перезаписывает файл). Можно использовать 'a' (добавление, добавляет данные в конец файла).

    Returns:
        bool: True, если запись прошла успешно, False в случае ошибки.
    """
    ...
```

**Параметры**:
- `data` (str | list[str] | dict): Данные для записи.
- `file_path` (str | Path): Путь к файлу.
- `mode` (str, optional): Режим открытия файла (по умолчанию 'w').

**Возвращает**:
- `bool`: `True`, если запись успешна, `False` в случае ошибки.

**Как работает**:
1. Функция создает директории, если они не существуют.
2. Открывает файл в указанном режиме с кодировкой UTF-8.
3. В зависимости от типа данных, записывает строку, список строк или JSON-представление словаря в файл.
4. Возвращает `True` при успехе, `False` в случае исключения.

**Примеры**:

```python
from pathlib import Path

# Запись строки в файл
save_text_file("Привет, мир!", "example.txt")

# Запись списка строк в файл
save_text_file(["Строка 1", "Строка 2"], "example.txt")

# Запись словаря в файл
save_text_file({"key": "value"}, "example.json")
```

### `read_text_file_generator`

**Назначение**: Читает содержимое файла или директории, используя генератор для эффективной обработки больших файлов. Поддерживает рекурсивный поиск файлов в директориях и фильтрацию по расширениям и шаблонам имен файлов.

```python
def read_text_file_generator(file_path, as_list=False, extensions=None, chunk_size=8192, recursive=False, patterns=None):
    """
    Читает содержимое файла или директории, используя генератор.

    Args:
        file_path (str | Path): Путь к файлу или директории.
        as_list (bool, optional): Если True, возвращает генератор строк. Если False, возвращает строку (для файлов) или объединенную строку из всех файлов директории (для директорий).
        extensions (list[str], optional): Список расширений файлов для фильтрации при чтении директории.
        chunk_size (int, optional): Размер чанка для чтения файла (в байтах).
        recursive (bool, optional): Если True, рекурсивно обходит все поддиректории.
        patterns (str | list[str], optional): Шаблоны для фильтрации файлов.

    Returns:
        Generator[str, None, None] | str | list[str] | None: Генератор строк, строка или None в случае ошибки.
    """
    ...
```

**Параметры**:
- `file_path` (str | Path): Путь к файлу или директории.
- `as_list` (bool, optional): Если `True`, возвращает генератор строк.
- `extensions` (list[str], optional): Список расширений для фильтрации.
- `chunk_size` (int, optional): Размер чанка для чтения файла.
- `recursive` (bool, optional): Рекурсивный обход поддиректорий.
- `patterns` (str | list[str], optional): Шаблоны имен файлов.

**Возвращает**:
- `Generator[str, None, None] | str | list[str] | None`: Генератор строк, строка или `None` в случае ошибки.

**Как работает**:
1. Проверяет, является ли `file_path` файлом или директорией.
2. Для файлов использует `_read_file_lines_generator` или `_read_file_content` в зависимости от `as_list`.
3. Для директорий рекурсивно или не рекурсивно обрабатывает файлы, соответствующие заданным критериям.

**Примеры**:

```python
from pathlib import Path

# Чтение файла как генератора строк
file_path = Path("example.txt")
generator = read_text_file_generator(file_path, as_list=True)
for line in generator:
    print(line)

# Чтение директории рекурсивно и объединение файлов в строку
directory_path = Path("example_directory")
content = read_text_file_generator(directory_path, recursive=True)
print(content)
```

### `read_text_file`

**Назначение**: Читает содержимое файла или директории. Более простая версия, чем `read_text_file_generator`, не использующая генераторы.

```python
def read_text_file(file_path, as_list=False, extensions=None, exc_info=True, chunk_size=8192):
    """
    Читает содержимое файла или директории.

    Args:
        file_path (str | Path): Путь к файлу или директории.
        as_list (bool, optional): Если True, возвращает список строк.
        extensions (list[str], optional): Список расширений файлов для фильтрации.
        exc_info (bool, optional): Флаг для логирования информации об исключении.
        chunk_size (int, optional): Размер чанка для чтения файла.

    Returns:
        str | list[str] | None: Строка или список строк, или None в случае ошибки.
    """
    ...
```

**Параметры**:
- `file_path` (str | Path): Путь к файлу или директории.
- `as_list` (bool, optional): Если `True`, возвращает список строк.
- `extensions` (list[str], optional): Список расширений для фильтрации.
- `exc_info` (bool, optional): Флаг для логирования информации об исключении.
- `chunk_size` (int, optional): Размер чанка для чтения файла.

**Возвращает**:
- `str | list[str] | None`: Строка или список строк, или `None` в случае ошибки.

**Как работает**:
1. Проверяет, является ли `file_path` файлом или директорией.
2. Для директорий рекурсивно считывает все файлы, соответствующие `extensions`.
3. Объединяет содержимое в строку или список строк в зависимости от `as_list`.

**Примеры**:

```python
from pathlib import Path

# Чтение файла как строки
file_path = Path("example.txt")
content = read_text_file(file_path)
print(content)

# Чтение файла как списка строк
file_path = Path("example.txt")
lines = read_text_file(file_path, as_list=True)
print(lines)
```

### `yield_text_from_files`

**Назначение**: Читает файл и возвращает его содержимое как генератор строк (`as_list=True`) или как одну строку (`as_list=False`). Вспомогательная функция для `read_text_file_generator`.

```python
def yield_text_from_files(file_path, as_list=False, chunk_size=8192):
    """
    Читает файл и возвращает его содержимое как генератор строк или как одну строку.

    Args:
        file_path (str | Path): Путь к файлу.
        as_list (bool, optional): Флаг, указывающий на возврат генератора или строки.
        chunk_size (int, optional): Размер чанка для чтения.

    Returns:
        Generator[str, None, None] | str | None: Генератор строк или строка, или None при ошибке.
    """
    ...
```

**Параметры**:
- `file_path` (str | Path): Путь к файлу.
- `as_list` (bool, optional): Флаг, указывающий на возврат генератора или строки.
- `chunk_size` (int, optional): Размер чанка для чтения.

**Возвращает**:
- `Generator[str, None, None] | str | None`: Генератор строк или строка, или `None` при ошибке.

**Как работает**:
1. Использует `_read_file_lines_generator` или `_read_file_content` в зависимости от значения `as_list`.

**Примеры**:

```python
from pathlib import Path

# Получение генератора строк из файла
file_path = Path("example.txt")
generator = yield_text_from_files(file_path, as_list=True)
for line in generator:
    print(line)

# Получение содержимого файла как строки
file_path = Path("example.txt")
content = yield_text_from_files(file_path)
print(content)
```

### `_read_file_content`

**Назначение**: Вспомогательная функция для чтения содержимого файла по чанкам и возврата его как одной строки. Используется для повышения эффективности при работе с очень большими файлами.

```python
def _read_file_content(file_path, chunk_size):
    """
    Читает содержимое файла по чанкам и возвращает его как одной строки.

    Args:
        file_path (Path): Путь к файлу.
        chunk_size (int): Размер чанка.

    Returns:
        str: Содержимое файла как одна строка.
    """
    ...
```

**Параметры**:
- `file_path` (Path): Путь к файлу.
- `chunk_size` (int): Размер чанка.

**Возвращает**:
- `str`: Содержимое файла как одна строка.

**Как работает**:
1. Читает файл по частям размером `chunk_size`.
2. Накапливает данные в переменной `content`.
3. Возвращает итоговую строку.

**Примеры**:

```python
from pathlib import Path

# Чтение содержимого файла по чанкам
file_path = Path("example.txt")
content = _read_file_content(file_path, chunk_size=4096)
print(content)
```

### `_read_file_lines_generator`

**Назначение**: Вспомогательная функция для чтения файла построчно с помощью генератора. Эффективна для больших файлов, поскольку не загружает весь файл в память сразу.

```python
def _read_file_lines_generator(file_path, chunk_size):
    """
    Читает файл построчно с помощью генератора.

    Args:
        file_path (Path): Путь к файлу.
        chunk_size (int): Размер чанка.

    Returns:
        Generator[str, None, None]: Генератор, который выдает строки файла по одной.
    """
    ...
```

**Параметры**:
- `file_path` (Path): Путь к файлу.
- `chunk_size` (int): Размер чанка.

**Возвращает**:
- `Generator[str, None, None]`: Генератор, который выдает строки файла по одной.

**Как работает**:
1. Читает файл по чанкам.
2. Разделяет чанк на строки с помощью `splitlines()`.
3. Обрабатывает случай, когда последняя строка в чанке неполная.
4. Возвращает строки файла по одной.

**Примеры**:

```python
from pathlib import Path

# Чтение файла построчно с помощью генератора
file_path = Path("example.txt")
generator = _read_file_lines_generator(file_path, chunk_size=4096)
for line in generator:
    print(line)
```

### `get_filenames_from_directory`

**Назначение**: Возвращает список имен файлов в указанной директории, опционально фильтруя по расширению.

```python
def get_filenames_from_directory(directory, ext='*'):
    """
    Возвращает список имен файлов в указанной директории.

    Args:
        directory (str | Path): Путь к директории.
        ext (str | list[str], optional): Расширение или список расширений файлов для фильтрации.

    Returns:
        list[str]: Список имен файлов.
    """
    ...
```

**Параметры**:
- `directory` (str | Path): Путь к директории.
- `ext` (str | list[str], optional): Расширение или список расширений файлов для фильтрации.

**Возвращает**:
- `list[str]`: Список имен файлов.

**Как работает**:
1. Итерирует по файлам в директории.
2. Возвращает список имен файлов, соответствующих указанному расширению.

**Примеры**:

```python
from pathlib import Path

# Получение списка всех файлов в директории
directory_path = Path("example_directory")
filenames = get_filenames_from_directory(directory_path)
print(filenames)

# Получение списка файлов с расширением .txt
filenames = get_filenames_from_directory(directory_path, ext=".txt")
print(filenames)
```

### `recursively_yield_file_path`

**Назначение**: Рекурсивно итерирует по файлам в указанной директории и её поддиректориях, возвращая пути к файлам, соответствующим заданным шаблонам.

```python
def recursively_yield_file_path(root_dir, patterns='*'):
    """
    Рекурсивно итерирует по файлам в указанной директории и её поддиректориях, возвращая пути к файлам.

    Args:
        root_dir (str | Path): Корневая директория.
        patterns (str | list[str]): Шаблоны имен файлов.

    Returns:
        Generator[Path, None, None]: Генератор, который выдает пути к файлам.
    """
    ...
```

**Параметры**:
- `root_dir` (str | Path): Корневая директория.
- `patterns` (str | list[str]): Шаблоны имен файлов.

**Возвращает**:
- `Generator[Path, None, None]`: Генератор, который выдает пути к файлам.

**Как работает**:
1. Использует `Path.rglob()` для рекурсивного поиска файлов, соответствующих заданным шаблонам.

**Примеры**:

```python
from pathlib import Path

# Рекурсивный поиск всех файлов в директории
root_dir = Path("example_directory")
generator = recursively_yield_file_path(root_dir)
for file_path in generator:
    print(file_path)

# Рекурсивный поиск файлов с расширением .txt
generator = recursively_yield_file_path(root_dir, patterns="*.txt")
for file_path in generator:
    print(file_path)
```

### `recursively_get_file_path`

**Назначение**: Рекурсивно находит все файлы в директории и её поддиректориях, соответствующие указанным шаблонам, и возвращает список их путей.

```python
def recursively_get_file_path(root_dir, patterns='*'):
    """
    Рекурсивно находит все файлы в директории и её поддиректориях, соответствующие указанным шаблонам, и возвращает список их путей.

    Args:
        root_dir (str | Path): Корневая директория.
        patterns (str | list[str]): Шаблоны имен файлов.

    Returns:
        list[Path]: Список путей к файлам.
    """
    ...
```

**Параметры**:
- `root_dir` (str | Path): Корневая директория.
- `patterns` (str | list[str]): Шаблоны имен файлов.

**Возвращает**:
- `list[Path]`: Список путей к файлам.

**Как работает**:
1. Использует `Path.rglob()` и собирает все найденные пути в список.

**Примеры**:

```python
from pathlib import Path

# Рекурсивный поиск всех файлов в директории
root_dir = Path("example_directory")
file_paths = recursively_get_file_path(root_dir)
print(file_paths)

# Рекурсивный поиск файлов с расширением .txt
file_paths = recursively_get_file_path(root_dir, patterns="*.txt")
print(file_paths)
```

### `recursively_read_text_files`

**Назначение**: Рекурсивно читает содержимое файлов в указанной директории, соответствующих заданным шаблонам.

```python
def recursively_read_text_files(root_dir, patterns, as_list=False):
    """
    Рекурсивно читает содержимое файлов в указанной директории, соответствующих заданным шаблонам.

    Args:
        root_dir (str | Path): Корневая директория.
        patterns (str | list[str]): Шаблоны имен файлов.
        as_list (bool, optional): Если True, возвращает список строк для каждого файла; иначе – строку для каждого файла.

    Returns:
        list[str]: Список содержимого файлов (либо список списков строк).
    """
    ...
```

**Параметры**:
- `root_dir` (str | Path): Корневая директория.
- `patterns` (str | list[str]): Шаблоны имен файлов.
- `as_list` (bool, optional): Если `True`, возвращает список строк для каждого файла; иначе – строку для каждого файла.

**Возвращает**:
- `list[str]`: Список содержимого файлов (либо список списков строк).

**Как работает**:
1. Использует `os.walk()` для рекурсивного обхода директории.
2. Читает файлы, соответствующие шаблонам.
3. Добавляет их содержимое в результирующий список.

**Примеры**:

```python
from pathlib import Path

# Рекурсивное чтение всех файлов в директории
root_dir = Path("example_directory")
contents = recursively_read_text_files(root_dir, patterns="*")
print(contents)

# Рекурсивное чтение файлов с расширением .txt в виде списка строк
contents = recursively_read_text_files(root_dir, patterns="*.txt", as_list=True)
print(contents)
```

### `get_directory_names`

**Назначение**: Возвращает список имен поддиректорий в указанной директории.

```python
def get_directory_names(directory):
    """
    Возвращает список имен поддиректорий в указанной директории.

    Args:
        directory (str | Path): Путь к директории.

    Returns:
        list[str]: Список имен поддиректорий.
    """
    ...
```

**Параметры**:
- `directory` (str | Path): Путь к директории.

**Возвращает**:
- `list[str]`: Список имен поддиректорий.

**Как работает**:
1. Итерирует по элементам в директории.
2. Возвращает список имен только тех, которые являются директориями.

**Примеры**:

```python
from pathlib import Path

# Получение списка имен поддиректорий
directory_path = Path("example_directory")
directory_names = get_directory_names(directory_path)
print(directory_names)
```

### `remove_bom`

**Назначение**: Удаляет BOM (Byte Order Mark) из текстового файла или из всех `.py` файлов в директории. BOM – это невидимый символ, который может вызывать проблемы в некоторых приложениях.

```python
def remove_bom(path):
    """
    Удаляет BOM (Byte Order Mark) из текстового файла или из всех .py файлов в директории.

    Args:
        path (str | Path): Путь к файлу или директории.
    """
    ...
```

**Параметры**:
- `path` (str | Path): Путь к файлу или директории.

**Как работает**:
1. Если `path` – файл, удаляет BOM из него.
2. Если `path` – директория, рекурсивно обходит все `.py` файлы и удаляет BOM из них.

**Примеры**:

```python
from pathlib import Path

# Удаление BOM из файла
file_path = Path("example.txt")
remove_bom(file_path)

# Удаление BOM из всех .py файлов в директории
directory_path = Path("example_directory")
remove_bom(directory_path)
```

### `main`

**Назначение**: Точка входа для скрипта, который удаляет BOM из всех `.py` файлов в директории `src`.

```python
def main():
    """
    Точка входа для скрипта, который удаляет BOM из всех .py файлов в директории `src`.
    """
    ...
```

**Как работает**:
1. Вызывает `remove_bom()` для директории `src`.

**Примеры**:
```python
# Запуск функции main
main()