# Модуль `src.utils.convertors.json`

## Обзор

Модуль `src.utils.convertors.json` предоставляет функции для конвертации данных в формате JSON в различные форматы, такие как CSV, SimpleNamespace, XML и XLS. Он содержит функции для преобразования JSON данных или файлов в различные форматы, облегчая интеграцию с различными системами и приложениями.

## Подробнее

Этот модуль предоставляет набор инструментов для преобразования JSON данных в различные форматы. Он предназначен для обеспечения гибкости при работе с JSON данными, позволяя преобразовывать их в наиболее подходящий формат для конкретной задачи. Модуль использует другие утилиты, такие как `save_csv_file`, `j_dumps`, `save_xls_file` и `dict2xml`, чтобы упростить процесс преобразования.

## Функции

### `json2csv`

```python
def json2csv(json_data: str | list | dict | Path, csv_file_path: str | Path) -> bool:
    """
    Convert JSON data or JSON file to CSV format with a comma delimiter.

    Args:
        json_data (str | list | dict | Path): JSON data as a string, list of dictionaries, or file path to a JSON file.
        csv_file_path (str | Path): Path to the CSV file to write.

    Returns:
        bool: True if successful, False otherwise.

    Raises:
        ValueError: If unsupported type for json_data.
        Exception: If unable to parse JSON or write CSV.
    """
```

**Назначение**: Преобразует JSON данные или JSON файл в формат CSV с разделителем в виде запятой.

**Параметры**:
- `json_data` (str | list | dict | Path): JSON данные в виде строки, списка словарей или пути к JSON файлу.
- `csv_file_path` (str | Path): Путь к CSV файлу для записи.

**Возвращает**:
- `bool`: `True`, если преобразование выполнено успешно, `False` в противном случае.

**Вызывает исключения**:
- `ValueError`: Если тип `json_data` не поддерживается.
- `Exception`: Если не удается разобрать JSON или записать CSV.

**Как работает функция**:

Функция `json2csv` принимает JSON данные или путь к JSON файлу, преобразует их в формат CSV и сохраняет в указанный файл. Функция сначала загружает JSON данные, проверяя их тип. Если данные представлены в виде словаря, они преобразуются в список, содержащий этот словарь. Затем функция вызывает `save_csv_file` для записи данных в CSV файл. В случае возникновения ошибки, функция логирует ошибку и возвращает `False`.

**Примеры**:

```python
from pathlib import Path
from src.utils.convertors.json import json2csv

# Пример 1: Преобразование JSON строки в CSV файл
json_string = '[{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]'
csv_file = "data.csv"
result = json2csv(json_string, csv_file)
print(f"Результат преобразования JSON строки в CSV: {result}")

# Пример 2: Преобразование JSON файла в CSV файл
json_file = Path("data.json")  # Предполагается, что файл data.json существует
json_file.write_text('[{"name": "Charlie", "age": 35}, {"name": "David", "age": 40}]')  # Создаем временный файл
csv_file = "data2.csv"
result = json2csv(json_file, csv_file)
print(f"Результат преобразования JSON файла в CSV: {result}")

# Пример 3: Преобразование словаря в CSV файл
json_dict = {"name": "Eve", "age": 28}
csv_file = "data3.csv"
result = json2csv(json_dict, csv_file)
print(f"Результат преобразования JSON словаря в CSV: {result}")
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
```

**Назначение**: Преобразует JSON данные или JSON файл в объект `SimpleNamespace`.

**Параметры**:
- `json_data` (str | dict | Path): JSON данные в виде строки, словаря или пути к JSON файлу.

**Возвращает**:
- `SimpleNamespace`: Разобранные JSON данные в виде объекта `SimpleNamespace`.

**Вызывает исключения**:
- `ValueError`: Если тип `json_data` не поддерживается.
- `Exception`: Если не удается разобрать JSON.

**Как работает функция**:

Функция `json2ns` принимает JSON данные или путь к JSON файлу, преобразует их в объект `SimpleNamespace` и возвращает его. Функция сначала загружает JSON данные, проверяя их тип. Затем функция создает объект `SimpleNamespace` из JSON данных. В случае возникновения ошибки, функция логирует ошибку.

**Примеры**:

```python
from pathlib import Path
from src.utils.convertors.json import json2ns

# Пример 1: Преобразование JSON строки в SimpleNamespace
json_string = '{"name": "Alice", "age": 30}'
result = json2ns(json_string)
print(f"Результат преобразования JSON строки в SimpleNamespace: {result.name}, {result.age}")

# Пример 2: Преобразование JSON файла в SimpleNamespace
json_file = Path("data.json")  # Предполагается, что файл data.json существует
json_file.write_text('{"name": "Bob", "age": 25}')  # Создаем временный файл
result = json2ns(json_file)
print(f"Результат преобразования JSON файла в SimpleNamespace: {result.name}, {result.age}")

# Пример 3: Преобразование словаря в SimpleNamespace
json_dict = {"name": "Charlie", "age": 35}
result = json2ns(json_dict)
print(f"Результат преобразования JSON словаря в SimpleNamespace: {result.name}, {result.age}")
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
```

**Назначение**: Преобразует JSON данные или JSON файл в формат XML.

**Параметры**:
- `json_data` (str | dict | Path): JSON данные в виде строки, словаря или пути к JSON файлу.
- `root_tag` (str): Корневой тег для XML. По умолчанию "root".

**Возвращает**:
- `str`: Результирующая XML строка.

**Вызывает исключения**:
- `ValueError`: Если тип `json_data` не поддерживается.
- `Exception`: Если не удается разобрать JSON или преобразовать в XML.

**Как работает функция**:

Функция `json2xml` принимает JSON данные или путь к JSON файлу, преобразует их в формат XML и возвращает XML строку. Функция вызывает `dict2xml` для преобразования данных в XML.

**Примеры**:

```python
from pathlib import Path
from src.utils.convertors.json import json2xml

# Пример 1: Преобразование JSON строки в XML
json_string = '{"name": "Alice", "age": 30}'
result = json2xml(json_string, root_tag="person")
print(f"Результат преобразования JSON строки в XML: {result}")

# Пример 2: Преобразование JSON файла в XML
json_file = Path("data.json")  # Предполагается, что файл data.json существует
json_file.write_text('{"name": "Bob", "age": 25}')  # Создаем временный файл
result = json2xml(json_file, root_tag="person")
print(f"Результат преобразования JSON файла в XML: {result}")

# Пример 3: Преобразование словаря в XML
json_dict = {"name": "Charlie", "age": 35}
result = json2xml(json_dict, root_tag="person")
print(f"Результат преобразования JSON словаря в XML: {result}")
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
```

**Назначение**: Преобразует JSON данные или JSON файл в формат XLS.

**Параметры**:
- `json_data` (str | list | dict | Path): JSON данные в виде строки, списка словарей или пути к JSON файлу.
- `xls_file_path` (str | Path): Путь к XLS файлу для записи.

**Возвращает**:
- `bool`: `True`, если преобразование выполнено успешно, `False` в противном случае.

**Вызывает исключения**:
- `ValueError`: Если тип `json_data` не поддерживается.
- `Exception`: Если не удается разобрать JSON или записать XLS.

**Как работает функция**:

Функция `json2xls` принимает JSON данные или путь к JSON файлу, преобразует их в формат XLS и сохраняет в указанный файл. Функция вызывает `save_xls_file` для записи данных в XLS файл.

**Примеры**:

```python
from pathlib import Path
from src.utils.convertors.json import json2xls

# Пример 1: Преобразование JSON строки в XLS файл
json_string = '[{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]'
xls_file = "data.xls"
result = json2xls(json_string, xls_file)
print(f"Результат преобразования JSON строки в XLS: {result}")

# Пример 2: Преобразование JSON файла в XLS файл
json_file = Path("data.json")  # Предполагается, что файл data.json существует
json_file.write_text('[{"name": "Charlie", "age": 35}, {"name": "David", "age": 40}]')  # Создаем временный файл
xls_file = "data2.xls"
result = json2xls(json_file, xls_file)
print(f"Результат преобразования JSON файла в XLS: {result}")

# Пример 3: Преобразование словаря в XLS файл
json_dict = {"name": "Eve", "age": 28}
xls_file = "data3.xls"
result = json2xls(json_dict, xls_file)
print(f"Результат преобразования JSON словаря в XLS: {result}")