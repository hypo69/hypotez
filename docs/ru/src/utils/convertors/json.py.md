# Модуль для конвертации JSON данных в различные форматы
=================================================================

Модуль содержит функции для конвертации JSON данных в различные форматы, такие как CSV, SimpleNamespace, XML и XLS.

Пример использования
----------------------

```python
>>> from src.utils.convertors.json import json2csv, json2ns, json2xml, json2xls
>>> json_data = '{"name": "John", "age": 30, "city": "New York"}'
>>> csv_file_path = 'data.csv'
>>> json2csv(json_data, csv_file_path)
True
>>> ns = json2ns(json_data)
>>> print(ns.name)
John
>>> xml_data = json2xml(json_data)
>>> print(xml_data)
<root><name>John</name><age>30</age><city>New York</city></root>
>>> xls_file_path = 'data.xls'
>>> json2xls(json_data, xls_file_path)
True
```

## Обзор

Этот модуль предоставляет набор функций для преобразования JSON данных в различные форматы. Он облегчает работу с JSON данными, позволяя конвертировать их в CSV, SimpleNamespace, XML и XLS форматы.

## Подробнее

Модуль содержит функции:
- `json2csv`: Преобразует JSON данные в формат CSV.
- `json2ns`: Преобразует JSON данные в объект `SimpleNamespace`.
- `json2xml`: Преобразует JSON данные в формат XML.
- `json2xls`: Преобразует JSON данные в формат XLS.

Эти функции позволяют легко интегрировать JSON данные с другими форматами, что может быть полезно для различных задач, таких как экспорт данных, создание отчетов и интеграция с другими системами.

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

**Назначение**: Преобразует JSON данные или JSON файл в формат CSV с использованием запятой в качестве разделителя.

**Параметры**:
- `json_data` (str | list | dict | Path): JSON данные в виде строки, списка словарей или пути к JSON файлу.
- `csv_file_path` (str | Path): Путь к CSV файлу для записи.

**Возвращает**:
- `bool`: `True`, если преобразование прошло успешно, `False` в противном случае.

**Вызывает исключения**:
- `ValueError`: Если тип `json_data` не поддерживается.
- `Exception`: Если не удается распарсить JSON или записать CSV.

**Как работает функция**:

1.  **Проверка типа входных данных (`json_data`)**:
    Функция проверяет, какого типа входные данные `json_data` (словарь, строка, список или путь к файлу).
2.  **Загрузка JSON данных**:
    В зависимости от типа данных, функция загружает JSON данные:
    - Если это словарь, он преобразуется в список, содержащий этот словарь.
    - Если это строка, она парсится с использованием `json.loads`.
    - Если это список, он используется напрямую.
    - Если это путь к файлу, файл открывается, и JSON данные загружаются из него.
    - Если тип данных не поддерживается, вызывается исключение `ValueError`.
3.  **Сохранение в CSV файл**:
    JSON данные сохраняются в CSV файл с использованием функции `save_csv_file` из модуля `src.utils.csv`.
4.  **Обработка исключений**:
    Если в процессе возникают исключения, они логируются с использованием `logger.error` из модуля `src.logger.logger`, и функция возвращает `False`.

ASCII схема работы функции:

    Тип данных json_data
    |
    -- Проверка типа json_data (str, list, dict, Path)
    |
    Загрузка JSON данных (json.loads, json.load)
    |
    Сохранение в CSV файл (save_csv_file)
    |
    Успешное завершение или Обработка исключений
    |
    Возврат результата (True или False)

**Примеры**:

```python
>>> from src.utils.convertors.json import json2csv
>>> json_data = '{"name": "John", "age": 30, "city": "New York"}'
>>> csv_file_path = 'data.csv'
>>> json2csv(json_data, csv_file_path)
True
```

```python
>>> from src.utils.convertors.json import json2csv
>>> json_data = [{"name": "John", "age": 30, "city": "New York"}, {"name": "Jane", "age": 25, "city": "Los Angeles"}]
>>> csv_file_path = 'data.csv'
>>> json2csv(json_data, csv_file_path)
True
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
- `SimpleNamespace`: Распарсенные JSON данные в виде объекта `SimpleNamespace`.

**Вызывает исключения**:
- `ValueError`: Если тип `json_data` не поддерживается.
- `Exception`: Если не удается распарсить JSON.

**Как работает функция**:

1.  **Проверка типа входных данных (`json_data`)**:
    Функция проверяет, какого типа входные данные `json_data` (словарь, строка или путь к файлу).
2.  **Загрузка JSON данных**:
    В зависимости от типа данных, функция загружает JSON данные:
    - Если это словарь, он используется напрямую.
    - Если это строка, она парсится с использованием `json.loads`.
    - Если это путь к файлу, файл открывается, и JSON данные загружаются из него.
    - Если тип данных не поддерживается, вызывается исключение `ValueError`.
3.  **Преобразование в SimpleNamespace**:
    JSON данные преобразуются в объект `SimpleNamespace` с использованием оператора `**` для распаковки словаря.
4.  **Обработка исключений**:
    Если в процессе возникают исключения, они логируются с использованием `logger.error` из модуля `src.logger.logger`, и функция возвращает `None`.

ASCII схема работы функции:

    Тип данных json_data
    |
    -- Проверка типа json_data (str, dict, Path)
    |
    Загрузка JSON данных (json.loads, json.load)
    |
    Преобразование в SimpleNamespace (SimpleNamespace(**data))
    |
    Успешное завершение или Обработка исключений
    |
    Возврат результата (SimpleNamespace)

**Примеры**:

```python
>>> from src.utils.convertors.json import json2ns
>>> json_data = '{"name": "John", "age": 30, "city": "New York"}'
>>> ns = json2ns(json_data)
>>> print(ns.name)
John
```

```python
>>> from src.utils.convertors.json import json2ns
>>> json_data = {"name": "John", "age": 30, "city": "New York"}
>>> ns = json2ns(json_data)
>>> print(ns.age)
30
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
- `root_tag` (str): Корневой элемент для XML.

**Возвращает**:
- `str`: Результирующая XML строка.

**Вызывает исключения**:
- `ValueError`: Если тип `json_data` не поддерживается.
- `Exception`: Если не удается распарсить JSON или преобразовать в XML.

**Как работает функция**:

1.  **Преобразование в XML**:
    JSON данные преобразуются в XML с использованием функции `dict2xml` из модуля `src.utils.convertors.dict`.

ASCII схема работы функции:

    JSON данные (json_data)
    |
    Преобразование в XML (dict2xml)
    |
    Возврат XML строки

**Примеры**:

```python
>>> from src.utils.convertors.json import json2xml
>>> json_data = '{"name": "John", "age": 30, "city": "New York"}'
>>> xml_data = json2xml(json_data)
>>> print(xml_data)
<root><name>John</name><age>30</age><city>New York</city></root>
```

```python
>>> from src.utils.convertors.json import json2xml
>>> json_data = {"name": "John", "age": 30, "city": "New York"}
>>> xml_data = json2xml(json_data, root_tag="person")
>>> print(xml_data)
<person><name>John</name><age>30</age><city>New York</city></person>
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
- `bool`: `True`, если преобразование прошло успешно, `False` в противном случае.

**Вызывает исключения**:
- `ValueError`: Если тип `json_data` не поддерживается.
- `Exception`: Если не удается распарсить JSON или записать XLS.

**Как работает функция**:

1.  **Преобразование в XLS**:
    JSON данные преобразуются в XLS с использованием функции `save_xls_file` из модуля `src.utils.xls`.

ASCII схема работы функции:

    JSON данные (json_data)
    |
    Преобразование в XLS (save_xls_file)
    |
    Возврат результата (True или False)

**Примеры**:

```python
>>> from src.utils.convertors.json import json2xls
>>> json_data = '{"name": "John", "age": 30, "city": "New York"}'
>>> xls_file_path = 'data.xls'
>>> json2xls(json_data, xls_file_path)
True
```

```python
>>> from src.utils.convertors.json import json2xls
>>> json_data = [{"name": "John", "age": 30, "city": "New York"}, {"name": "Jane", "age": 25, "city": "Los Angeles"}]
>>> xls_file_path = 'data.xls'
>>> json2xls(json_data, xls_file_path)
True