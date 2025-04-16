# Модуль для подсчета строк, классов и функций в файлах

## Обзор

Модуль предназначен для рекурсивного подсчета количества строк в текстовых файлах, а также количества классов и функций в указанной директории и ее поддиректориях.

## Подробнее

Модуль предоставляет функции для анализа структуры кода в проекте. Он позволяет получить общее представление о размере кодовой базы, количестве классов и функций, что может быть полезно для оценки сложности проекта, отслеживания изменений в коде или для других целей анализа кода.

## Функции

### `count_lines_in_files`

```python
def count_lines_in_files(directory):
    """
    Recursively counts the number of lines in text files in the specified directory and its subdirectories,
    as well as the number of classes and functions.

    @param directory: Path to the directory
    @return: Total number of lines in text files, number of classes, and number of functions
    """
    ...
```

**Назначение**:
Рекурсивно подсчитывает количество строк в текстовых файлах, а также количество классов и функций в указанной директории и ее поддиректориях.

**Параметры**:

-   `directory` (str): Путь к директории.

**Возвращает**:

-   `total_lines` (int): Общее количество строк в текстовых файлах.
-   `total_classes` (int): Общее количество классов.
-   `total_functions` (int): Общее количество функций.

**Как работает функция**:

1.  Инициализирует счетчики `total_lines`, `total_classes` и `total_functions` нулями.
2.  Перебирает все элементы (файлы и поддиректории) в указанной директории.
3.  Если элемент является файлом:

    *   Проверяет, является ли файл текстовым, исключая бинарные файлы, файлы Jupyter Notebook и файл `__init__.py`.
    *   Если файл является текстовым, открывает его, вызывает функцию `count_lines_classes_functions` для подсчета количества строк, классов и функций в файле и добавляет результаты к общим счетчикам.
4.  Если элемент является директорией:

    *   Проверяет, не является ли директория директорией `__pycache__` или скрытой директорией (начинающейся с `.`)
    *   Если директория не исключена, рекурсивно вызывает `count_lines_in_files` для этой директории и добавляет результаты к общим счетчикам.
5.  Возвращает общее количество строк, классов и функций.

### `is_binary`

```python
def is_binary(filepath):
    """
    Checks if the file is binary.

    @param filepath: Path to the file
    @return: True if the file is binary, otherwise False
    """
    ...
```

**Назначение**:
Проверяет, является ли файл бинарным.

**Параметры**:

-   `filepath` (str): Путь к файлу.

**Возвращает**:

-   `bool`: `True`, если файл является бинарным, иначе `False`.

**Как работает функция**:

1.  Пытается открыть файл в бинарном режиме (`'rb'`).
2.  Читает первые 512 байт файла.
3.  Проверяет, содержит ли прочитанный блок нулевые байты (`b'\\0'`). Если да, то файл считается бинарным.
4.  В случае возникновения ошибки при чтении файла, считает файл бинарным.

### `count_lines_classes_functions`

```python
def count_lines_classes_functions(file):
    """
    Counts the number of lines, classes, and functions in the file.

    @param file: File object
    @return: Number of lines, number of classes, and number of functions
    """
    ...
```

**Назначение**:
Подсчитывает количество строк, классов и функций в файле.

**Параметры**:

-   `file` (file object): Объект файла.

**Возвращает**:

-   `lines` (int): Количество строк в файле.
-   `classes_count` (int): Количество классов в файле.
-   `functions_count` (int): Количество функций в файле.

**Как работает функция**:

1.  Инициализирует счетчики `lines`, `classes_count` и `functions_count` нулями.
2.  Перебирает все строки в файле.
3.  Для каждой строки:

    *   Удаляет начальные и конечные пробелы.
    *   Проверяет, не является ли строка пустой.
    *   Если строка не пустая, увеличивает счетчик строк (`lines`).
    *   Если строка начинается с `'class'`, увеличивает счетчик классов (`classes_count`).
    *   Если строка начинается с `'def'`, увеличивает счетчик функций (`functions_count`).
4.  Возвращает количество строк, классов и функций.

## Примеры

### Пример использования модуля

```python
import os
from pathlib import Path
from dev_utils.file_counter import count_lines_in_files

if __name__ == "__main__":
    dir_root = Path(os.getcwd()[:os.getcwd().rfind('hypotez')+7])  # Root directory of the project
    dir_src = Path(dir_root, 'src')
    
    print(f"Counting lines, classes, and functions in files in directory: {dir_src}")
    total_lines, total_classes, total_functions = count_lines_in_files(dir_src)
    print(f"Total lines in text files in '{dir_src}': {total_lines}")
    print(f"Total classes: {total_classes}")
    print(f"Total functions: {total_functions}")
```

Этот код выполняет следующие действия:

1.  Импортирует необходимые модули и функции.
2.  Определяет корневую директорию проекта и путь к директории `src`.
3.  Вызывает функцию `count_lines_in_files` для подсчета количества строк, классов и функций в директории `src`.
4.  Выводит результаты подсчета.