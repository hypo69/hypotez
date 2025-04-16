### Анализ кода `hypotez/src/utils/convertors/json.py.md`

## Обзор

Модуль предоставляет утилиты для преобразования JSON-данных в различные форматы.

## Подробнее

Этот модуль содержит функции для преобразования JSON-данных из различных источников (строка, список, словарь или путь к файлу) в другие форматы. Он использует библиотеки `json` для работы с JSON, `csv` для работы с CSV, `types.SimpleNamespace` для создания объектов с атрибутами, `src.utils.convertors.dict` для преобразования в XML и `src.utils.xls` для преобразования в XLS.

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
    ...
```

**Назначение**:
Преобразует JSON-данные или JSON-файл в формат CSV с разделителем-запятой.

**Параметры**:

*   `json_data` (str | list | dict | Path): JSON-данные в виде строки, списка словарей, словаря или пути к JSON-файлу.
*   `csv_file_path` (str | Path): Путь к CSV-файлу для записи.

**Возвращает**:

*   `bool`: `True`, если преобразование прошло успешно, `False` в противном случае.

**Вызывает исключения**:

*   `ValueError`: Если тип входных данных `json_data` не поддерживается.
*   `Exception`: Если не удается проанализировать JSON или записать CSV.

**Как работает функция**:

1.  Загружает JSON-данные из входного параметра, который может быть строкой, списком, словарем или путем к файлу.
2.  В зависимости от типа входных данных:

    *   Если это словарь, преобразует его в список, содержащий этот словарь.
    *   Если это строка, пытается распарсить JSON из строки.
    *   Если это список, использует его напрямую.
    *   Если это путь к файлу, читает JSON из файла.
    *   Если тип не поддерживается, выбрасывает исключение `ValueError`.
3.  Вызывает функцию `save_csv_file` для сохранения данных в CSV-файл.
4.  Логирует ошибки, если преобразование не удалось.

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

*   `json_data` (str | dict | Path): JSON-данные в виде строки, словаря или пути к JSON-файлу.

**Возвращает**:

*   `SimpleNamespace`: Распарсенные JSON-данные в виде объекта `SimpleNamespace`.

**Вызывает исключения**:

*   `ValueError`: Если тип входных данных `json_data` не поддерживается.
*   `Exception`: Если не удается проанализировать JSON.

**Как работает функция**:

1.  Загружает JSON-данные из входного параметра, который может быть строкой, словарем или путем к файлу.
2.  В зависимости от типа входных данных:

    *   Если это словарь, использует его напрямую.
    *   Если это строка, пытается распарсить JSON из строки.
    *   Если это путь к файлу, читает JSON из файла.
    *   Если тип не поддерживается, выбрасывает исключение `ValueError`.
3.  Создает объект `SimpleNamespace` на основе полученных данных.
4.  Логирует ошибки, если преобразование не удалось.

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

*   `json_data` (str | dict | Path): JSON-данные в виде строки, словаря или пути к JSON-файлу.
*   `root_tag` (str, optional): Корневой элемент для XML. По умолчанию `"root"`.

**Возвращает**:

*   `str`: Результирующая XML-строка.

**Вызывает исключения**:

*   `ValueError`: Если тип входных данных `json_data` не поддерживается.
*   `Exception`: Если не удается проанализировать JSON или преобразовать в XML.

**Как работает функция**:

1.  Вызывает функцию `dict2xml` для преобразования JSON-данных в XML.
2.  Возвращает XML-строку.

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

*   `json_data` (str | list | dict | Path): JSON-данные в виде строки, списка словарей, словаря или пути к JSON-файлу.
*   `xls_file_path` (str | Path): Путь к XLS-файлу для записи.

**Возвращает**:

*   `bool`: `True`, если преобразование прошло успешно, `False` в противном случае.

**Вызывает исключения**:

*   `ValueError`: Если тип входных данных `json_data` не поддерживается.
*   `Exception`: Если не удается проанализировать JSON или записать XLS.

**Как работает функция**:

1.  Вызывает функцию `save_xls_file` для сохранения JSON-данных в XLS-файл.
2.  Возвращает результат, возвращённый функцией `save_xls_file`.

## Константы

Отсутствуют.

## Примеры использования

```python
from src.utils.convertors.json import json2csv, json2ns, json2xml, json2xls
from pathlib import Path
import json

# Пример использования json2csv
data = [{"name": "John", "age": 30}, {"name": "Alice", "age": 25}]
json2csv(data, "output.csv")

# Пример использования json2ns
data = {"name": "John", "age": 30}
ns = json2ns(data)
print(ns.name)

# Пример использования json2xml
data = {"root": {"name": "John", "age": 30}}
xml_data = json2xml(data)
print(xml_data)

# Пример использования json2xls
data_to_save = {'Sheet1': [{'column1': 'value1', 'column2': 'value2'}]}
json2xls(data_to_save, 'output.xlsx')
```

## Зависимости

*   `json`: Для работы с JSON-данными.
*   `csv`: Для работы с CSV-файлами.
*   `typing.List, typing.Dict, typing.Union`: Для аннотаций типов.
*   `types.SimpleNamespace`: Для создания объектов `SimpleNamespace`.
*   `pathlib.Path`: Для работы с путями к файлам.
*   `src.utils.csv`: Для вызова `save_csv_file`
*   `src.utils.jjson`: Для вызова `j_dumps`
*   `src.utils.xls`: Для вызова `save_xls_file`
*   `src.utils.convertors.dict`: Для вызова `dict2xml`
* `src.logger.logger`:  Для логирования ошибок и информации

## Взаимосвязи с другими частями проекта

*   Модуль предоставляет утилиты для преобразования JSON-данных и используется другими модулями проекта `hypotez`, где требуется обработка JSON, а также в подсистеме логирования.
*   Использует `src.logger.logger` для логирования.
*   Использует `src.utils.csv`, `src.utils.jjson`, `src.utils.xls` и `src.utils.convertors.dict` для выполнения фактических преобразований в другие форматы.