### Анализ кода модуля `hypotez/src/utils/convertors/json.py`

## Обзор

Этот модуль предоставляет утилиты для преобразования данных из формата JSON в другие форматы, такие как CSV, SimpleNamespace, XML и XLS.

## Подробнее

Модуль содержит функции, упрощающие преобразование JSON-данных в различные форматы, используемые в проекте, обеспечивая гибкость при работе с данными.

## Функции

### `json2csv`

```python
def json2csv(json_data: str | list | dict | Path, csv_file_path: str | Path, exc_info: bool = True) -> bool:
    """
    Convert JSON data or JSON file to CSV format with a comma delimiter.

    Args:
        json_data (str | list | dict | Path): JSON data as a string, list of dictionaries, or file path to a JSON file.
        csv_file_path (str | Path): Path to the CSV file to write.
        exc_info (bool, optional): If True, includes traceback information in the log. Defaults to True.

    Returns:
        bool: True if successful, False otherwise.

    Raises:
        ValueError: If unsupported type for json_data.
        Exception: If unable to parse JSON or write CSV.
    """
    ...
```

**Назначение**:
Преобразует JSON-данные или JSON-файл в формат CSV с разделителем-запятой.

**Параметры**:
- `json_data` (str | list | dict | Path): JSON-данные в виде строки, списка словарей, словаря или пути к JSON-файлу.
- `csv_file_path` (str | Path): Путь к CSV-файлу для записи.
- `exc_info` (bool, optional): Если True, включает информацию об отслеживании в лог. По умолчанию True.

**Возвращает**:
- `bool`: True, если преобразование выполнено успешно, иначе False.

**Вызывает исключения**:
- `ValueError`: Если тип `json_data` не поддерживается.
- `Exception`: Если не удается разобрать JSON или записать CSV.

**Как работает функция**:
1. Загружает JSON-данные в зависимости от типа `json_data`.
2. Если загрузка успешна, вызывает функцию `save_csv_file` из модуля `src.utils.csv` для сохранения данных в CSV-файл.

**Примеры**:

```python
from src.utils.convertors import json2csv

json_data = '[{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]'
csv_file_path = 'data.csv'
success = json2csv(json_data, csv_file_path)
if success:
    print('CSV file saved successfully')
```

### `json2ns`

```python
def json2ns(json_data: str | dict | Path) -> SimpleNamespace:
    """
    Convert JSON data or JSON file to SimpleNamespace object.

    Args:
        json_data (str | dict | Path): JSON data as a string, dictionary, or file path to a JSON file.

    Returns:
        SimpleNamespace: Parsed JSON data as a SimpleNamespace object.
    
    Raises:
        ValueError: If unsupported type for json_data.
        Exception: If unable to parse JSON.
    """
    ...
```

**Назначение**:
Преобразует JSON-данные или JSON-файл в объект `SimpleNamespace`.

**Параметры**:
- `json_data` (str | dict | Path): JSON-данные в виде строки, словаря или пути к JSON-файлу.

**Возвращает**:
- `SimpleNamespace`: JSON-данные, преобразованные в объект `SimpleNamespace`.

**Вызывает исключения**:
- `ValueError`: Если тип `json_data` не поддерживается.
- `Exception`: Если не удается разобрать JSON.

**Как работает функция**:
1. Загружает JSON-данные в зависимости от типа `json_data`.
2. Если загрузка успешна, создает объект `SimpleNamespace` из загруженных данных.

**Примеры**:

```python
from src.utils.convertors import json2ns

json_data = '{"name": "John", "age": 30}'
ns = json2ns(json_data)
print(ns.name)
print(ns.age)
```

### `json2xml`

```python
def json2xml(json_data: str | dict | Path, root_tag: str = "root") -> str:
    """
    Convert JSON data or JSON file to XML format.

    Args:
        json_data (str | dict | Path): JSON data as a string, dictionary, or file path to a JSON file.
        root_tag (str): The root element tag for the XML.

    Returns:
        str: The resulting XML string.

    Raises:
        ValueError: If unsupported type for json_data.
        Exception: If unable to parse JSON or convert to XML.
    """
    ...
```

**Назначение**:
Преобразует JSON-данные или JSON-файл в формат XML.

**Параметры**:
- `json_data` (str | dict | Path): JSON-данные в виде строки, словаря или пути к JSON-файлу.
- `root_tag` (str, optional): Корневой элемент для XML. По умолчанию "root".

**Возвращает**:
- `str`: Результирующая XML-строка.

**Вызывает исключения**:
- `ValueError`: Если тип `json_data` не поддерживается.
- `Exception`: Если не удается разобрать JSON или преобразовать в XML.

**Как работает функция**:
1. Вызывает функцию `dict2xml` из модуля `src.utils.convertors.dict`, передавая ей `json_data` и `root_tag`.
2. Возвращает результат, полученный от `dict2xml`.

**Примеры**:

```python
from src.utils.convertors import json2xml

json_data = '{"name": "John", "age": 30}'
xml_data = json2xml(json_data, root_tag="person")
print(xml_data)
```

### `json2xls`

```python
def json2xls(json_data: str | list | dict | Path, xls_file_path: str | Path) -> bool:
    """
    Convert JSON data or JSON file to XLS format.

    Args:
        json_data (str | list | dict | Path): JSON data as a string, list of dictionaries, or file path to a JSON file.
        xls_file_path (str | Path): Path to the XLS file to write.

    Returns:
        bool: True if successful, False otherwise.

    Raises:
        ValueError: If unsupported type for json_data.
        Exception: If unable to parse JSON or write XLS.
    """
    ...
```

**Назначение**:
Преобразует JSON-данные или JSON-файл в формат XLS.

**Параметры**:
- `json_data` (str | list | dict | Path): JSON-данные в виде строки, списка словарей, словаря или пути к JSON-файлу.
- `xls_file_path` (str | Path): Путь к XLS-файлу для записи.

**Возвращает**:
- `bool`: True, если преобразование выполнено успешно, иначе False.

**Вызывает исключения**:
- `ValueError`: Если тип `json_data` не поддерживается.
- `Exception`: Если не удается разобрать JSON или записать XLS.

**Как работает функция**:
1. Вызывает функцию `save_xls_file` из модуля `src.utils.xls`, передавая ей `json_data` и `xls_file_path`.
2. Возвращает результат, полученный от `save_xls_file`.

**Примеры**:

```python
from src.utils.convertors import json2xls

json_data = '[{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]'
xls_file_path = 'data.xls'
success = json2xls(json_data, xls_file_path)
if success:
    print('XLS file saved successfully')
```

## Переменные

Отсутствуют

## Запуск

Для использования этого модуля необходимо установить библиотеки `json_repair`, `pandas`, `xlwt` и `XlsxWriter`.

```bash
pip install json_repair pandas xlwt XlsxWriter
```

Пример использования функций:

```python
from src.utils.convertors import json2csv, json2ns, json2xml, json2xls
from pathlib import Path

# Преобразование JSON в CSV
json_data = '[{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]'
success = json2csv(json_data, 'data.csv')

# Преобразование JSON в SimpleNamespace
data = '{"name": "John", "age": 30}'
ns = json2ns(data)

# Преобразование JSON в XML
xml_data = json2xml(data, root_tag="person")

# Преобразование JSON в XLS
success = json2xls(json_data, 'data.xls')