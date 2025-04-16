# Модуль для подсчета строк, классов и функций в файлах

## Обзор

Этот модуль предназначен для рекурсивного подсчета количества строк, классов и функций в текстовых файлах, расположенных в указанной директории и её поддиректориях. Он также определяет, является ли файл бинарным.

## Подробней

Модуль предоставляет инструменты для анализа структуры кода в проекте. Он позволяет получить информацию о количестве строк кода, количестве классов и функций, что может быть полезно для оценки размера и сложности проекта, а также для отслеживания изменений в кодовой базе.

## Функции

### `count_lines_in_files`

**Назначение**: Рекурсивно подсчитывает количество строк в текстовых файлах, а также количество классов и функций в указанной директории и ее поддиректориях.

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

**Параметры**:

-   `directory` (str): Путь к директории.

**Возвращает**:

-   `total_lines` (int): Общее количество строк в текстовых файлах.
-   `total_classes` (int): Общее количество классов.
-   `total_functions` (int): Общее количество функций.

**Как работает функция**:

1.  Инициализирует счетчики `total_lines`, `total_classes` и `total_functions` значением 0.
2.  Перебирает все элементы (файлы и поддиректории) в указанной директории.
3.  Если элемент является файлом:
    -   Проверяет, является ли файл текстовым, не относится ли он к директории `__pycache__`, и не является ли файлом Jupyter Notebook (`.ipynb`).
    -   Если файл соответствует условиям, открывает его, вызывает функцию `count_lines_classes_functions` для подсчета строк, классов и функций в файле, и добавляет результаты к общим счетчикам.
4.  Если элемент является директорией:
    -   Проверяет, не является ли директория `__pycache__` или не начинается ли ее имя с точки (`.`).
    -   Если директория не исключена, рекурсивно вызывает функцию `count_lines_in_files` для подсчета строк, классов и функций в этой директории, и добавляет результаты к общим счетчикам.
5.  Возвращает общее количество строк, классов и функций.

### `is_binary`

**Назначение**: Проверяет, является ли файл бинарным.

```python
def is_binary(filepath):
    """
    Checks if the file is binary.

    @param filepath: Path to the file
    @return: True if the file is binary, otherwise False
    """
    ...
```

**Параметры**:

-   `filepath` (str): Путь к файлу.

**Возвращает**:

-   `bool`: `True`, если файл является бинарным, `False` - если текстовым.

**Как работает функция**:

1.  Пытается открыть файл в бинарном режиме (`'rb'`).
2.  Читает первые 512 байт файла.
3.  Проверяет, содержит ли прочитанный фрагмент нулевые байты (`b'\\0'`). Если содержит, считает файл бинарным и возвращает `True`.
4.  Если в процессе чтения файла возникает ошибка, считает файл бинарным и возвращает `True`.

### `count_lines_classes_functions`

**Назначение**: Подсчитывает количество строк, классов и функций в файле.

```python
def count_lines_classes_functions(file):
    """
    Counts the number of lines, classes, and functions in the file.

    @param file: File object
    @return: Number of lines, number of classes, and number of functions
    """
    ...
```

**Параметры**:

-   `file` (file object): Файловый объект.

**Возвращает**:

-   `lines` (int): Количество строк в файле.
-   `classes_count` (int): Количество классов в файле.
-   `functions_count` (int): Количество функций в файле.

**Как работает функция**:

1.  Инициализирует счетчики `lines`, `classes_count` и `functions_count` значением 0.
2.  Перебирает строки в файле.
3.  Для каждой строки удаляет начальные и конечные пробельные символы.
4.  Если строка не пустая, увеличивает счетчик строк `lines`.
5.  Если строка начинается с `'class'`, увеличивает счетчик классов `classes_count`.
6.  Если строка начинается с `'def'`, увеличивает счетчик функций `functions_count`.
7.  Возвращает количество строк, классов и функций.

## Запуск модуля

В блоке `if __name__ == "__main__":` определяется корневая директория проекта, директория `src`, и вызывается функция `count_lines_in_files` для подсчета строк, классов и функций в файлах, расположенных в директории `src`. Результаты выводятся на экран.

```python
if __name__ == "__main__":
    dir_root = Path(os.getcwd()[:os.getcwd().rfind('hypotez')+7])  # Root directory of the project
    dir_src = Path(dir_root, 'src')
    
    print(f"Counting lines, classes, and functions in files in directory: {dir_src}")
    total_lines, total_classes, total_functions = count_lines_in_files(dir_src)
    print(f"Total lines in text files in '{dir_src}': {total_lines}")
    print(f"Total classes: {total_classes}")
    print(f"Total functions: {total_functions}")