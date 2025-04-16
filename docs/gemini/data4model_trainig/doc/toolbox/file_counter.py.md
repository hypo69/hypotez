# Модуль для подсчета строк, классов и функций в файлах

## Обзор

Этот модуль предназначен для рекурсивного подсчета количества строк в текстовых файлах, а также количества классов и функций в указанной директории и ее поддиректориях.

## Подробнее

Модуль предоставляет функции для подсчета строк, классов и функций в текстовых файлах, исключая бинарные файлы, Jupyter Notebook файлы и файлы из директорий `__pycache__`. Он может быть использован для анализа размера и структуры кодовой базы проекта.

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
Рекурсивно подсчитывает количество строк в текстовых файлах в указанной директории и ее поддиректориях, а также количество классов и функций.

**Параметры**:
- `directory` (str): Путь к директории.

**Возвращает**:
- tuple: Кортеж, содержащий общее количество строк в текстовых файлах, количество классов и количество функций.

**Как работает функция**:
1. Инициализирует переменные `total_lines`, `total_classes` и `total_functions` для хранения общего количества строк, классов и функций.
2. Перебирает все элементы (файлы и поддиректории) в указанной директории.
3. Если элемент является файлом:
    - Проверяет, является ли файл текстовым, не находится ли он в директории `__pycache__`, и не является ли он файлом Jupyter Notebook (`.ipynb`).
    - Если файл соответствует условиям, открывает его, вызывает функцию `count_lines_classes_functions` для подсчета строк, классов и функций в файле, и добавляет результаты к общим счетчикам.
4. Если элемент является директорией:
    - Проверяет, не является ли директория директорией `__pycache__`.
    - Если директория не исключена, рекурсивно вызывает `count_lines_in_files` для этой директории, и добавляет результаты к общим счетчикам.
5. Возвращает кортеж, содержащий общее количество строк, классов и функций.

**Примеры**:

```python
directory_path = "src"
total_lines, total_classes, total_functions = count_lines_in_files(directory_path)
print(f"Total lines: {total_lines}, total classes: {total_classes}, total functions: {total_functions}")
```

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
- `filepath` (str): Путь к файлу.

**Возвращает**:
- bool: `True`, если файл является бинарным, иначе `False`.

**Как работает функция**:
1. Пытается открыть файл в бинарном режиме (`'rb'`).
2. Читает первые 512 байт файла.
3. Проверяет, содержит ли прочитанный блок нулевые байты (`b'\\0'`).
4. Если файл содержит нулевые байты, возвращает `True` (считает файл бинарным).
5. Если при чтении файла возникает ошибка, считает файл бинарным и возвращает `True`.

**Примеры**:

```python
file_path = "image.png"
if is_binary(file_path):
    print("File is binary")
else:
    print("File is not binary")
```

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
- `file` (file object): Объект файла.

**Возвращает**:
- tuple: Кортеж, содержащий количество строк, количество классов и количество функций.

**Как работает функция**:
1. Инициализирует переменные `lines`, `classes_count` и `functions_count` для хранения количества строк, классов и функций.
2. Перебирает строки в файле.
3. Для каждой строки удаляет начальные и конечные пробелы.
4. Если строка не пустая, увеличивает счетчик строк.
5. Если строка начинается с `'class'`, увеличивает счетчик классов.
6. Если строка начинается с `'def'`, увеличивает счетчик функций.
7. Возвращает кортеж, содержащий количество строк, классов и функций.

**Примеры**:

```python
with open("my_file.py", "r") as file:
    lines, classes, functions = count_lines_classes_functions(file)
    print(f"Lines: {lines}, Classes: {classes}, Functions: {functions}")
```

## Запуск

```python
if __name__ == "__main__":
    dir_root = Path(os.getcwd()[:os.getcwd().rfind('hypotez')+7])  # Root directory of the project
    dir_src = Path(dir_root, 'src')
    
    print(f"Counting lines, classes, and functions in files in directory: {dir_src}")
    total_lines, total_classes, total_functions = count_lines_in_files(dir_src)
    print(f"Total lines in text files in '{dir_src}': {total_lines}")
    print(f"Total classes: {total_classes}")
    print(f"Total functions: {total_functions}")
```

При запуске этого скрипта будет вызвана функция `count_lines_in_files`, которая подсчитает количество строк, классов и функций в файлах директории `src` и выведет результаты в консоль.