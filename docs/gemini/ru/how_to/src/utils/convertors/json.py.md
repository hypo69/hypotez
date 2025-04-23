## \file /src/utils/convertors/json.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
.. module:: src.utils.convertors.json 
\t:platform: Windows, Unix
\t:synopsis: convert JSON data into various formats: CSV, SimpleNamespace, XML, and XLS

Functions:
    - `json2csv`: Convert JSON data to CSV format.
    - `json2ns`: Convert JSON data to SimpleNamespace object.
    - `json2xml`: Convert JSON data to XML format.
    - `json2xls`: Convert JSON data to XLS format.
"""

import json
import csv
from types import SimpleNamespace
from pathlib import Path
from typing import List, Dict

from src.utils.csv import save_csv_file
from src.utils.jjson import j_dumps
from src.utils.xls import save_xls_file
from src.utils.convertors.dict import dict2xml
from src.logger.logger import logger


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
    try:
        # Load JSON data
        if isinstance(json_data, dict):
            data = [json_data]
        elif isinstance(json_data, str):
            data = json.loads(json_data)
        elif isinstance(json_data, list):
            data = json_data
        elif isinstance(json_data, Path):
            with open(json_data, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
        else:
            raise ValueError("Unsupported type for json_data")

        save_csv_file(data, csv_file_path)
        return True
    except Exception as ex:
        logger.error(f"json2csv failed", ex, True)
        ...


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
    try:
        if isinstance(json_data, dict):
            data = json_data
        elif isinstance(json_data, str):
            data = json.loads(json_data)
        elif isinstance(json_data, Path):
            with open(json_data, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
        else:
            raise ValueError("Unsupported type for json_data")
        
        return SimpleNamespace(**data)
    except Exception as ex:
        logger.error(f"json2ns failed", ex, True)


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
    return dict2xml(json_data)


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
    return save_xls_file(json_data, file_path)
        

```

Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код предоставляет набор функций для преобразования данных из формата JSON в различные другие форматы, такие как CSV, SimpleNamespace, XML и XLS. Он включает функции для загрузки JSON данных из строк, словарей, списков или файлов, а также для сохранения данных в соответствующие форматы файлов.

Шаги выполнения
-------------------------
1. **Загрузка JSON данных**:
   - Функция проверяет тип входных данных `json_data`.
   - Если `json_data` это словарь, он преобразуется в список, содержащий этот словарь.
   - Если `json_data` это строка, она парсится как JSON с использованием `json.loads`.
   - Если `json_data` это путь к файлу, файл открывается, и JSON данные загружаются из файла с использованием `json.load`.
   - Если тип `json_data` не поддерживается, вызывается исключение `ValueError`.

2. **Преобразование в CSV**:
   - Функция `json2csv` вызывает функцию `save_csv_file` для сохранения JSON данных в формате CSV по указанному пути `csv_file_path`.
   - Возвращает `True` при успешном выполнении, `False` в случае ошибки.

3. **Преобразование в SimpleNamespace**:
   - Функция `json2ns` преобразует JSON данные в объект `SimpleNamespace`, что позволяет обращаться к элементам JSON как к атрибутам объекта.
   - Возвращает объект `SimpleNamespace`, созданный из JSON данных.

4. **Преобразование в XML**:
   - Функция `json2xml` вызывает функцию `dict2xml` для преобразования JSON данных в формат XML.
   - Возвращает XML строку.

5. **Преобразование в XLS**:
   - Функция `json2xls` вызывает функцию `save_xls_file` для сохранения JSON данных в формате XLS по указанному пути `xls_file_path`.
   - Возвращает результат выполнения `save_xls_file`.

Пример использования
-------------------------

```python
from pathlib import Path
from src.utils.convertors.json import json2csv, json2ns, json2xml, json2xls

# Пример JSON данных
json_data = '{"name": "John", "age": 30, "city": "New York"}'

# Преобразование JSON в CSV
csv_file_path = "output.csv"
json2csv(json_data, csv_file_path)

# Преобразование JSON в SimpleNamespace
namespace = json2ns(json_data)
print(namespace.name)  # Вывод: John

# Преобразование JSON в XML
xml_data = json2xml(json_data)
print(xml_data)

# Преобразование JSON в XLS
xls_file_path = "output.xls"
json2xls(json_data, xls_file_path)

# Чтение JSON из файла
json_file_path = Path("input.json")
json_file_path.write_text(json_data) # Создаем файл input.json с данными выше
json2csv(json_file_path, "file_output.csv")