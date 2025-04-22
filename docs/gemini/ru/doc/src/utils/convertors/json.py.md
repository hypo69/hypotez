# Модуль `json`

## Обзор

Модуль предназначен для преобразования данных из формата JSON в различные другие форматы, такие как CSV, SimpleNamespace, XML и XLS. Он включает функции для выполнения этих преобразований.

## Подробнее

Модуль содержит функции для преобразования JSON-данных в различные форматы, что может быть полезно для интеграции данных между различными системами и приложениями. Модуль использует другие модули проекта `hypotez`, такие как `src.utils.csv`, `src.utils.jjson`, `src.utils.xls` и `src.utils.convertors.dict`, для выполнения преобразований.

## Функции

### `json2csv`

```python
def json2csv(json_data: str | list | dict | Path, csv_file_path: str | Path) -> bool:
    """
    Преобразует JSON-данные или JSON-файл в формат CSV с разделителем-запятой.

    Args:
        json_data (str | list | dict | Path): JSON-данные в виде строки, списка словарей или пути к JSON-файлу.
        csv_file_path (str | Path): Путь к CSV-файлу для записи.

    Returns:
        bool: True, если преобразование выполнено успешно, False в противном случае.

    Raises:
        ValueError: Если передан неподдерживаемый тип для json_data.
        Exception: Если не удается разобрать JSON или записать CSV.
    """
    ...
```

**Как работает функция**:

Функция `json2csv` принимает JSON-данные в различных форматах (строка, список, словарь или путь к файлу) и преобразует их в формат CSV, сохраняя результат в указанный файл. Функция выполняет следующие шаги:

1.  Определяет тип входных JSON-данных и загружает их соответствующим образом. Если `json_data` является словарем, он преобразуется в список, содержащий этот словарь. Если `json_data` является строкой, она анализируется как JSON. Если `json_data` является путем к файлу, файл открывается и его содержимое анализируется как JSON.

2.  Вызывает функцию `save_csv_file` из модуля `src.utils.csv` для записи данных в CSV-файл.

3.  В случае возникновения исключений, функция логирует ошибку с использованием `logger.error`.

**Примеры**:

```python
from pathlib import Path
from src.utils.convertors.json import json2csv

# Пример 1: Преобразование JSON-строки в CSV-файл
json_string = '[{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]'
csv_file = "output.csv"
result = json2csv(json_string, csv_file)
print(f"Результат преобразования: {result}")

# Пример 2: Преобразование JSON-файла в CSV-файл
json_file_path = Path("data.json")  # Предполагается, что data.json существует
csv_file_path = Path("output.csv")
result = json2csv(json_file_path, csv_file_path)
print(f"Результат преобразования: {result}")

# Пример 3: Преобразование JSON-словаря в CSV-файл
json_data = {"name": "Alice", "age": 30}
csv_file = "output.csv"
result = json2csv(json_data, csv_file)
print(f"Результат преобразования: {result}")
```

### `json2ns`

```python
def json2ns(json_data: str | dict | Path) -> SimpleNamespace:
    """
    Преобразует JSON-данные или JSON-файл в объект SimpleNamespace.

    Args:
        json_data (str | dict | Path): JSON-данные в виде строки, словаря или пути к JSON-файлу.

    Returns:
        SimpleNamespace: Разобранные JSON-данные в виде объекта SimpleNamespace.

    Raises:
        ValueError: Если передан неподдерживаемый тип для json_data.
        Exception: Если не удается разобрать JSON.
    """
    ...
```

**Как работает функция**:

Функция `json2ns` преобразует JSON-данные в объект `SimpleNamespace`, что позволяет обращаться к элементам JSON как к атрибутам объекта. Функция выполняет следующие шаги:

1.  Определяет тип входных JSON-данных и загружает их соответствующим образом. Если `json_data` является словарем, он используется напрямую. Если `json_data` является строкой, она анализируется как JSON. Если `json_data` является путем к файлу, файл открывается и его содержимое анализируется как JSON.

2.  Создает объект `SimpleNamespace` из JSON-данных с использованием оператора `**`, который распаковывает словарь в именованные аргументы конструктора `SimpleNamespace`.

3.  В случае возникновения исключений, функция логирует ошибку с использованием `logger.error`.

**Примеры**:

```python
from pathlib import Path
from src.utils.convertors.json import json2ns

# Пример 1: Преобразование JSON-строки в SimpleNamespace
json_string = '{"name": "Alice", "age": 30}'
namespace = json2ns(json_string)
print(f"Имя: {namespace.name}, Возраст: {namespace.age}")

# Пример 2: Преобразование JSON-файла в SimpleNamespace
json_file_path = Path("data.json")  # Предполагается, что data.json существует
namespace = json2ns(json_file_path)
print(f"Имя: {namespace.name}, Возраст: {namespace.age}")

# Пример 3: Преобразование JSON-словаря в SimpleNamespace
json_data = {"name": "Alice", "age": 30}
namespace = json2ns(json_data)
print(f"Имя: {namespace.name}, Возраст: {namespace.age}")
```

### `json2xml`

```python
def json2xml(json_data: str | dict | Path, root_tag: str = "root") -> str:
    """
    Преобразует JSON-данные или JSON-файл в формат XML.

    Args:
        json_data (str | dict | Path): JSON-данные в виде строки, словаря или пути к JSON-файлу.
        root_tag (str): Корневой тег для XML.

    Returns:
        str: Результирующая XML-строка.

    Raises:
        ValueError: Если передан неподдерживаемый тип для json_data.
        Exception: Если не удается разобрать JSON или преобразовать в XML.
    """
    ...
```

**Как работает функция**:

Функция `json2xml` преобразует JSON-данные в формат XML. Она вызывает функцию `dict2xml` из модуля `src.utils.convertors.dict` для выполнения преобразования.

**Примеры**:

```python
from pathlib import Path
from src.utils.convertors.json import json2xml

# Пример 1: Преобразование JSON-строки в XML
json_string = '{"name": "Alice", "age": 30}'
xml_string = json2xml(json_string, root_tag="person")
print(f"XML: {xml_string}")

# Пример 2: Преобразование JSON-файла в XML
json_file_path = Path("data.json")  # Предполагается, что data.json существует
xml_string = json2xml(json_file_path, root_tag="person")
print(f"XML: {xml_string}")

# Пример 3: Преобразование JSON-словаря в XML
json_data = {"name": "Alice", "age": 30}
xml_string = json2xml(json_data, root_tag="person")
print(f"XML: {xml_string}")
```

### `json2xls`

```python
def json2xls(json_data: str | list | dict | Path, xls_file_path: str | Path) -> bool:
    """
    Преобразует JSON-данные или JSON-файл в формат XLS.

    Args:
        json_data (str | list | dict | Path): JSON-данные в виде строки, списка словарей или пути к JSON-файлу.
        xls_file_path (str | Path): Путь к XLS-файлу для записи.

    Returns:
        bool: True, если преобразование выполнено успешно, False в противном случае.

    Raises:
        ValueError: Если передан неподдерживаемый тип для json_data.
        Exception: Если не удается разобрать JSON или записать XLS.
    """
    ...
```

**Как работает функция**:

Функция `json2xls` преобразует JSON-данные в формат XLS. Она вызывает функцию `save_xls_file` из модуля `src.utils.xls` для записи данных в XLS-файл.

**Примеры**:

```python
from pathlib import Path
from src.utils.convertors.json import json2xls

# Пример 1: Преобразование JSON-строки в XLS-файл
json_string = '[{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]'
xls_file = "output.xls"
result = json2xls(json_string, xls_file)
print(f"Результат преобразования: {result}")

# Пример 2: Преобразование JSON-файла в XLS-файл
json_file_path = Path("data.json")  # Предполагается, что data.json существует
xls_file_path = Path("output.xls")
result = json2xls(json_file_path, xls_file_path)
print(f"Результат преобразования: {result}")

# Пример 3: Преобразование JSON-словаря в XLS-файл
json_data = {"name": "Alice", "age": 30}
xls_file = "output.xls"
result = json2xls(json_data, xls_file)
print(f"Результат преобразования: {result}")