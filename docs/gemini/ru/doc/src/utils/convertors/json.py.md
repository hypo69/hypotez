# Модуль конвертации JSON данных

## Обзор

Модуль `src.utils.convertors.json` предоставляет функции для преобразования данных в формате JSON в различные форматы: CSV, SimpleNamespace, XML и XLS. 

## Подробнее

Модуль используется для преобразования JSON-данных, которые могут быть представлены строкой, списком словарей или путем к JSON-файлу, в другие форматы данных. 

## Функции

### `json2csv`

**Назначение**: Преобразует JSON-данные в CSV-формат с разделителем-запятой.

**Параметры**:
- `json_data` (str | list | dict | Path): JSON-данные в виде строки, списка словарей или пути к JSON-файлу.
- `csv_file_path` (str | Path): Путь к CSV-файлу для записи.

**Возвращает**:
- `bool`: `True`, если преобразование прошло успешно, `False` в противном случае.

**Вызывает исключения**:
- `ValueError`: Если указан неподдерживаемый тип для `json_data`.
- `Exception`: Если невозможно разобрать JSON или записать CSV.

**Как работает функция**:
- Функция извлекает JSON-данные из предоставленного аргумента `json_data`. Она поддерживает различные типы данных: строку, список словарей, словарь и путь к JSON-файлу. 
-  Функция преобразует JSON-данные в CSV-формат с использованием библиотеки `csv` и сохраняет их в указанном файле с помощью функции `save_csv_file`. 

**Примеры**:
```python
from src.utils.convertors.json import json2csv

# Преобразование из строки JSON
json_data = '{"name": "John Doe", "age": 30}'
csv_file_path = 'data.csv'
result = json2csv(json_data, csv_file_path)
print(f'JSON converted to CSV: {result}') # Вывод: JSON converted to CSV: True

# Преобразование из списка словарей
json_data = [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 35}]
csv_file_path = 'people.csv'
result = json2csv(json_data, csv_file_path)
print(f'JSON converted to CSV: {result}') # Вывод: JSON converted to CSV: True

# Преобразование из JSON-файла
json_file_path = 'data.json'
csv_file_path = 'data_from_file.csv'
result = json2csv(json_file_path, csv_file_path)
print(f'JSON converted to CSV: {result}') # Вывод: JSON converted to CSV: True 
```

### `json2ns`

**Назначение**: Преобразует JSON-данные в объект `SimpleNamespace`.

**Параметры**:
- `json_data` (str | dict | Path): JSON-данные в виде строки, словаря или пути к JSON-файлу.

**Возвращает**:
- `SimpleNamespace`: Разобранные JSON-данные в виде объекта `SimpleNamespace`.

**Вызывает исключения**:
- `ValueError`: Если указан неподдерживаемый тип для `json_data`.
- `Exception`: Если невозможно разобрать JSON.

**Как работает функция**:
-  Функция извлекает JSON-данные из предоставленного аргумента `json_data`, поддерживая строку, словарь и путь к JSON-файлу. 
-  JSON-данные разбираются с помощью библиотеки `json` и преобразуются в объект `SimpleNamespace` с помощью функции `SimpleNamespace()`, чтобы обеспечить доступ к данным через атрибуты.

**Примеры**:
```python
from src.utils.convertors.json import json2ns

# Преобразование из строки JSON
json_data = '{"name": "John Doe", "age": 30}'
ns = json2ns(json_data)
print(f'Name: {ns.name}, Age: {ns.age}') # Вывод: Name: John Doe, Age: 30

# Преобразование из словаря
json_data = {"name": "Alice", "age": 25}
ns = json2ns(json_data)
print(f'Name: {ns.name}, Age: {ns.age}') # Вывод: Name: Alice, Age: 25

# Преобразование из JSON-файла
json_file_path = 'data.json'
ns = json2ns(json_file_path)
print(f'Name: {ns.name}, Age: {ns.age}') # Вывод: Name: John Doe, Age: 30 
```

### `json2xml`

**Назначение**: Преобразует JSON-данные в XML-формат.

**Параметры**:
- `json_data` (str | dict | Path): JSON-данные в виде строки, словаря или пути к JSON-файлу.
- `root_tag` (str): Тег корневого элемента для XML.

**Возвращает**:
- `str`: Результирующая строка XML.

**Вызывает исключения**:
- `ValueError`: Если указан неподдерживаемый тип для `json_data`.
- `Exception`: Если невозможно разобрать JSON или преобразовать в XML.

**Как работает функция**:
-  Функция извлекает JSON-данные из предоставленного аргумента `json_data`, поддерживая строку, словарь и путь к JSON-файлу.
-  Функция использует функцию `dict2xml` из модуля `src.utils.convertors.dict` для преобразования JSON-данных в XML-формат.

**Примеры**:
```python
from src.utils.convertors.json import json2xml

# Преобразование из строки JSON
json_data = '{"name": "John Doe", "age": 30}'
xml_string = json2xml(json_data, root_tag="person")
print(xml_string) # Вывод: <person><name>John Doe</name><age>30</age></person>

# Преобразование из словаря
json_data = {"name": "Alice", "age": 25}
xml_string = json2xml(json_data) # используем  root_tag='root' по умолчанию
print(xml_string) # Вывод: <root><name>Alice</name><age>25</age></root>

# Преобразование из JSON-файла
json_file_path = 'data.json'
xml_string = json2xml(json_file_path) 
print(xml_string) # Вывод: <root><name>John Doe</name><age>30</age></root>
```

### `json2xls`

**Назначение**: Преобразует JSON-данные в XLS-формат.

**Параметры**:
- `json_data` (str | list | dict | Path): JSON-данные в виде строки, списка словарей или пути к JSON-файлу.
- `xls_file_path` (str | Path): Путь к XLS-файлу для записи.

**Возвращает**:
- `bool`: `True`, если преобразование прошло успешно, `False` в противном случае.

**Вызывает исключения**:
- `ValueError`: Если указан неподдерживаемый тип для `json_data`.
- `Exception`: Если невозможно разобрать JSON или записать XLS.

**Как работает функция**:
-  Функция извлекает JSON-данные из предоставленного аргумента `json_data`, поддерживая строку, список словарей, словарь и путь к JSON-файлу.
-  Функция использует функцию `save_xls_file` из модуля `src.utils.xls` для преобразования JSON-данных в XLS-формат и сохранения их в указанном файле.

**Примеры**:
```python
from src.utils.convertors.json import json2xls

# Преобразование из строки JSON
json_data = '{"name": "John Doe", "age": 30}'
xls_file_path = 'data.xls'
result = json2xls(json_data, xls_file_path)
print(f'JSON converted to XLS: {result}') # Вывод: JSON converted to XLS: True

# Преобразование из списка словарей
json_data = [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 35}]
xls_file_path = 'people.xls'
result = json2xls(json_data, xls_file_path)
print(f'JSON converted to XLS: {result}') # Вывод: JSON converted to XLS: True

# Преобразование из JSON-файла
json_file_path = 'data.json'
xls_file_path = 'data_from_file.xls'
result = json2xls(json_file_path, xls_file_path)
print(f'JSON converted to XLS: {result}') # Вывод: JSON converted to XLS: True