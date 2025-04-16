# Модуль для конвертации JSON данных в различные форматы
==================================================================

Модуль `src.utils.convertors.json` предоставляет функции для преобразования JSON данных в различные форматы, такие как CSV, SimpleNamespace, XML и XLS.

## Обзор

Модуль содержит функции для конвертации JSON данных в различные форматы. Он обеспечивает гибкость и удобство при работе с JSON данными, позволяя преобразовывать их в наиболее подходящий формат для конкретной задачи.

## Подробнее

Этот модуль предоставляет набор функций для преобразования JSON данных в различные форматы, такие как CSV, SimpleNamespace, XML и XLS. Каждая функция предназначена для определенного преобразования и принимает JSON данные в различных форматах (строка, словарь, список или путь к файлу). Модуль использует другие утилиты, такие как `save_csv_file`, `dict2xml` и `save_xls_file`, для выполнения фактического преобразования.

## Функции

### `json2csv`

**Назначение**: Преобразует JSON данные или JSON файл в формат CSV с разделителем запятая.

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
    ...
```

**Параметры**:

-   `json_data` (str | list | dict | Path): JSON данные в виде строки, списка словарей или пути к JSON файлу.
-   `csv_file_path` (str | Path): Путь к CSV файлу, в который будут записаны данные.

**Возвращает**:

-   `bool`: `True`, если преобразование прошло успешно, `False` в противном случае.

**Вызывает исключения**:

-   `ValueError`: Если тип `json_data` не поддерживается.
-   `Exception`: Если не удается распарсить JSON или записать CSV.

**Как работает функция**:

Функция `json2csv` принимает JSON данные в различных форматах (строка, список, словарь или путь к файлу) и преобразует их в формат CSV. Сначала функция пытается загрузить JSON данные в зависимости от их типа. Если `json_data` является словарем, он преобразуется в список, содержащий этот словарь. Если это строка, она парсится как JSON. Если это список, он используется напрямую. Если это путь к файлу, функция пытается открыть и прочитать JSON из файла. Если тип `json_data` не поддерживается, вызывается исключение `ValueError`. Затем функция вызывает `save_csv_file` для записи данных в CSV файл. В случае возникновения исключения в процессе, функция логирует ошибку и возвращает `False`.

**Примеры**:

```python
from pathlib import Path

# Преобразование JSON строки в CSV файл
json_string = '[{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]'
csv_file = "data.csv"
result = json2csv(json_string, csv_file)
print(f"JSON string to CSV conversion successful: {result}")  # Вывод: JSON string to CSV conversion successful: True

# Преобразование JSON файла в CSV файл
json_file_path = Path("data.json")
# Допустим, что data.json содержит: [{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]
csv_file = "data_from_file.csv"
result = json2csv(json_file_path, csv_file)
print(f"JSON file to CSV conversion successful: {result}")  # Вывод: JSON file to CSV conversion successful: True
```

### `json2ns`

**Назначение**: Преобразует JSON данные или JSON файл в объект SimpleNamespace.

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

**Параметры**:

-   `json_data` (str | dict | Path): JSON данные в виде строки, словаря или пути к JSON файлу.

**Возвращает**:

-   `SimpleNamespace`: Распарсенные JSON данные в виде объекта SimpleNamespace.

**Вызывает исключения**:

-   `ValueError`: Если тип `json_data` не поддерживается.
-   `Exception`: Если не удается распарсить JSON.

**Как работает функция**:

Функция `json2ns` принимает JSON данные в различных форматах (строка, словарь или путь к файлу) и преобразует их в объект `SimpleNamespace`. Сначала функция пытается загрузить JSON данные в зависимости от их типа. Если `json_data` является словарем, он используется напрямую. Если это строка, она парсится как JSON. Если это путь к файлу, функция пытается открыть и прочитать JSON из файла. Если тип `json_data` не поддерживается, вызывается исключение `ValueError`. Затем функция создает объект `SimpleNamespace` из словаря данных. В случае возникновения исключения в процессе, функция логирует ошибку.

**Примеры**:

```python
from pathlib import Path
from types import SimpleNamespace

# Преобразование JSON строки в SimpleNamespace
json_string = '{"name": "John", "age": 30}'
result = json2ns(json_string)
print(f"JSON string to SimpleNamespace: {result.name}, {result.age}")  # Вывод: JSON string to SimpleNamespace: John, 30

# Преобразование JSON файла в SimpleNamespace
json_file_path = Path("data.json")
# Допустим, что data.json содержит: {"name": "John", "age": 30}
result = json2ns(json_file_path)
print(f"JSON file to SimpleNamespace: {result.name}, {result.age}")  # Вывод: JSON file to SimpleNamespace: John, 30
```

### `json2xml`

**Назначение**: Преобразует JSON данные или JSON файл в формат XML.

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

**Параметры**:

-   `json_data` (str | dict | Path): JSON данные в виде строки, словаря или пути к JSON файлу.
-   `root_tag` (str): Корневой тег для XML. По умолчанию "root".

**Возвращает**:

-   `str`: Результирующая XML строка.

**Вызывает исключения**:

-   `ValueError`: Если тип `json_data` не поддерживается.
-   `Exception`: Если не удается распарсить JSON или преобразовать в XML.

**Как работает функция**:

Функция `json2xml` принимает JSON данные в различных форматах (строка, словарь или путь к файлу) и преобразует их в формат XML. Функция вызывает `dict2xml` для выполнения фактического преобразования.

**Примеры**:

```python
from pathlib import Path

# Преобразование JSON строки в XML
json_string = '{"name": "John", "age": 30}'
result = json2xml(json_string, root_tag="person")
print(f"JSON string to XML: {result}")  # Вывод: JSON string to XML: <person><name>John</name><age>30</age></person>

# Преобразование JSON файла в XML
json_file_path = Path("data.json")
# Допустим, что data.json содержит: {"name": "John", "age": 30}
result = json2xml(json_file_path, root_tag="person")
print(f"JSON file to XML: {result}")  # Вывод: JSON file to XML: <person><name>John</name><age>30</age></person>
```

### `json2xls`

**Назначение**: Преобразует JSON данные или JSON файл в формат XLS.

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

**Параметры**:

-   `json_data` (str | list | dict | Path): JSON данные в виде строки, списка словарей или пути к JSON файлу.
-   `xls_file_path` (str | Path): Путь к XLS файлу, в который будут записаны данные.

**Возвращает**:

-   `bool`: `True`, если преобразование прошло успешно, `False` в противном случае.

**Вызывает исключения**:

-   `ValueError`: Если тип `json_data` не поддерживается.
-   `Exception`: Если не удается распарсить JSON или записать XLS.

**Как работает функция**:

Функция `json2xls` принимает JSON данные в различных форматах (строка, список, словарь или путь к файлу) и преобразует их в формат XLS. Функция вызывает `save_xls_file` для выполнения фактического преобразования.

**Примеры**:

```python
from pathlib import Path

# Преобразование JSON строки в XLS файл
json_string = '[{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]'
xls_file = "data.xls"
result = json2xls(json_string, xls_file)
print(f"JSON string to XLS conversion successful: {result}")  # Вывод: JSON string to XLS conversion successful: True

# Преобразование JSON файла в XLS файл
json_file_path = Path("data.json")
# Допустим, что data.json содержит: [{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]
xls_file = "data_from_file.xls"
result = json2xls(json_file_path, xls_file)
print(f"JSON file to XLS conversion successful: {result}")  # Вывод: JSON file to XLS conversion successful: True