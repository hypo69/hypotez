# Module: `src.utils.convertors.json`

## Overview

This module provides functions for converting JSON data to various formats: CSV, SimpleNamespace, XML, and XLS. 

## Table of Contents

-   [Functions](#functions)
    -   [`json2csv`](#json2csv)
    -   [`json2ns`](#json2ns)
    -   [`json2xml`](#json2xml)
    -   [`json2xls`](#json2xls)

## Functions

### `json2csv`

**Purpose**: Преобразует JSON-данные или JSON-файл в формат CSV с разделителем-запятой.

**Parameters**:

-   `json_data` (str | list | dict | Path): JSON-данные в виде строки, списка словарей или пути к JSON-файлу.
-   `csv_file_path` (str | Path): Путь к CSV-файлу для записи.

**Returns**:

-   `bool`: True, если преобразование прошло успешно, False в противном случае.

**Raises Exceptions**:

-   `ValueError`: Если передан неподдерживаемый тип для `json_data`.
-   `Exception`: Если не удалось разобрать JSON или записать CSV.

**How the Function Works**:

-   Функция `json2csv` принимает JSON-данные или путь к файлу в качестве входных данных.
-   Она определяет тип входных данных и загружает JSON-данные соответствующим образом.
-   Затем она использует функцию `save_csv_file` из модуля `src.utils.csv` для записи CSV-файла.

**Examples**:

```python
# Преобразование JSON-строки в CSV-файл
json_data = '{"name": "John Doe", "age": 30}'
csv_file_path = 'data.csv'
success = json2csv(json_data, csv_file_path)
print(f'Conversion successful: {success}')  # Вывод: Conversion successful: True

# Преобразование JSON-файла в CSV-файл
json_file_path = 'data.json'
csv_file_path = 'data.csv'
success = json2csv(json_file_path, csv_file_path)
print(f'Conversion successful: {success}')  # Вывод: Conversion successful: True
```

### `json2ns`

**Purpose**: Преобразует JSON-данные или JSON-файл в объект SimpleNamespace.

**Parameters**:

-   `json_data` (str | dict | Path): JSON-данные в виде строки, словаря или пути к JSON-файлу.

**Returns**:

-   `SimpleNamespace`: Разобранные JSON-данные в виде объекта SimpleNamespace.

**Raises Exceptions**:

-   `ValueError`: Если передан неподдерживаемый тип для `json_data`.
-   `Exception`: Если не удалось разобрать JSON.

**How the Function Works**:

-   Функция `json2ns` принимает JSON-данные или путь к файлу в качестве входных данных.
-   Она определяет тип входных данных и загружает JSON-данные соответствующим образом.
-   Затем она использует `SimpleNamespace(**data)` для создания объекта SimpleNamespace из разобранных JSON-данных.

**Examples**:

```python
# Преобразование JSON-строки в объект SimpleNamespace
json_data = '{"name": "John Doe", "age": 30}'
ns = json2ns(json_data)
print(f'Name: {ns.name}, Age: {ns.age}')  # Вывод: Name: John Doe, Age: 30

# Преобразование JSON-файла в объект SimpleNamespace
json_file_path = 'data.json'
ns = json2ns(json_file_path)
print(f'Name: {ns.name}, Age: {ns.age}')  # Вывод: Name: John Doe, Age: 30
```

### `json2xml`

**Purpose**: Преобразует JSON-данные или JSON-файл в формат XML.

**Parameters**:

-   `json_data` (str | dict | Path): JSON-данные в виде строки, словаря или пути к JSON-файлу.
-   `root_tag` (str): Тег корневого элемента для XML.

**Returns**:

-   `str`: Полученная строка XML.

**Raises Exceptions**:

-   `ValueError`: Если передан неподдерживаемый тип для `json_data`.
-   `Exception`: Если не удалось разобрать JSON или выполнить преобразование в XML.

**How the Function Works**:

-   Функция `json2xml` использует функцию `dict2xml` из модуля `src.utils.convertors.dict` для преобразования JSON-данных в XML-формат.
-   `dict2xml` обрабатывает словарь и рекурсивно строит XML-строку, используя `root_tag` в качестве корневого элемента.

**Examples**:

```python
# Преобразование JSON-строки в XML-строку
json_data = '{"name": "John Doe", "age": 30}'
xml = json2xml(json_data)
print(xml)  # Вывод: <root><name>John Doe</name><age>30</age></root>

# Преобразование JSON-файла в XML-строку
json_file_path = 'data.json'
xml = json2xml(json_file_path)
print(xml)  # Вывод: <root><name>John Doe</name><age>30</age></root>
```

### `json2xls`

**Purpose**: Преобразует JSON-данные или JSON-файл в формат XLS.

**Parameters**:

-   `json_data` (str | list | dict | Path): JSON-данные в виде строки, списка словарей или пути к JSON-файлу.
-   `xls_file_path` (str | Path): Путь к XLS-файлу для записи.

**Returns**:

-   `bool`: True, если преобразование прошло успешно, False в противном случае.

**Raises Exceptions**:

-   `ValueError`: Если передан неподдерживаемый тип для `json_data`.
-   `Exception`: Если не удалось разобрать JSON или записать XLS.

**How the Function Works**:

-   Функция `json2xls` использует функцию `save_xls_file` из модуля `src.utils.xls` для записи XLS-файла.
-   `save_xls_file` обрабатывает JSON-данные и сохраняет их в XLS-файл.

**Examples**:

```python
# Преобразование JSON-строки в XLS-файл
json_data = '[{"name": "John Doe", "age": 30}, {"name": "Jane Doe", "age": 25}]'
xls_file_path = 'data.xls'
success = json2xls(json_data, xls_file_path)
print(f'Conversion successful: {success}')  # Вывод: Conversion successful: True

# Преобразование JSON-файла в XLS-файл
json_file_path = 'data.json'
xls_file_path = 'data.xls'
success = json2xls(json_file_path, xls_file_path)
print(f'Conversion successful: {success}')  # Вывод: Conversion successful: True
```