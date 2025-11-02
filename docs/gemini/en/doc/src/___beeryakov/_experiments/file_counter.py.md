# Модуль подсчета строк и функций в файлах
## Обзор

Модуль `file_counter.py` предназначен для рекурсивного подсчета количества строк в текстовых файлах в заданном каталоге и его подкаталогах, а также подсчета количества классов и функций в этих файлах.

## Детали
Модуль использует функцию `count_lines_in_files` для рекурсивного обхода каталога и подсчета строк, классов и функций в файлах. Функция `is_binary` используется для проверки бинарности файла. Функция `count_classes_and_functions` подсчитывает количество классов и функций в файле.

## Функции

### `count_lines_in_files`
**Назначение**: Рекурсивно подсчитывает количество строк в текстовых файлах в указанном каталоге и его подкаталогах, а также количество классов и функций.

**Параметры**:
- `directory` (str): Путь к каталогу.

**Возвратое значение**:
- `tuple`: Кортеж, содержащий общее количество строк в текстовых файлах, количество классов и количество функций.

**Пример**:
```python
src_directory = 'src'
total_lines, total_classes, total_functions = count_lines_in_files(src_directory)
print(f"Total lines in text files in '{src_directory}': {total_lines}")
print(f"Total classes: {total_classes}")
print(f"Total functions: {total_functions}")
```

### `is_binary`
**Назначение**: Проверяет, является ли файл бинарным.

**Параметры**:
- `filepath` (str): Путь к файлу.

**Возвратое значение**:
- `bool`: True, если файл бинарный, иначе False.

**Пример**:
```python
filepath = 'path/to/file.jpg'
is_binary(filepath)
```

### `count_classes_and_functions`
**Назначение**: Подсчитывает количество классов и функций в файле.

**Параметры**:
- `filepath` (str): Путь к файлу.

**Возвратое значение**:
- `tuple`: Кортеж, содержащий количество классов и количество функций.

**Пример**:
```python
filepath = 'path/to/file.py'
total_classes, total_functions = count_classes_and_functions(filepath)
print(f"Total classes: {total_classes}")
print(f"Total functions: {total_functions}")
```