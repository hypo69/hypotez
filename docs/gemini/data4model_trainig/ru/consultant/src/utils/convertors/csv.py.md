### **Анализ кода модуля `csv`**

## \file /src/utils/convertors/csv.py

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Присутствуют docstring для функций и классов, что облегчает понимание кода.
    - Используются аннотации типов для параметров и возвращаемых значений функций.
    - Используется модуль `logger` для логирования ошибок.
- **Минусы**:
    - Некоторые docstring написаны на английском языке.
    - Не все функции имеют подробное описание в docstring.
    - В примере использования JSON to CSV испольуются обратные кавычки
    - Нет обработки конкретных исключений, только общее `Exception`.
    - Не все переменные аннотированы

**Рекомендации по улучшению:**

1.  **Документация**:
    *   Перевести все docstring на русский язык.
    *   Добавить подробное описание для каждой функции, включая описание параметров, возвращаемых значений и возможных исключений.
    *   Добавить примеры использования функций в docstring.

2.  **Обработка ошибок**:
    *   В блоке `try...except` обрабатывать конкретные типы исключений, а не общее `Exception`.
    *   Указывать `exc_info=True` при логировании ошибок, чтобы включить информацию о трассировке.

3.  **Форматирование**:
    *   Убедиться, что код соответствует стандартам PEP8.
    *   Использовать консистентный стиль кавычек (одинарные `'`).

4.  **Использование `j_loads`**:
    *   Для чтения JSON или конфигурационных файлов заменить стандартное использование `open` и `json.load` на `j_loads` или `j_loads_ns`.

5.  **Аннотации**:
    *   Убедиться, что все переменные аннотированы типами.

6.  **Удалить неиспользуемые импорты**:
    *   Удалить импорт `from src.utils.csv import read_csv_as_dict, read_csv_as_ns, save_csv_file, read_csv_file`, так как они переопределяют функции

**Оптимизированный код:**

```python
## \file /src/utils/convertors/csv.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для работы с утилитами преобразования CSV и JSON
=========================================================

Модуль содержит функции для конвертации данных между форматами CSV и JSON.

Функции:
    - `csv2dict`: Преобразует CSV данные в словарь.
    - `csv2ns`: Преобразует CSV данные в объекты SimpleNamespace.

Пример использования:

    # Использование JSON списка словарей
    json_data_list = [{"name": "John", "age": 30, "city": "New York"}, {"name": "Alice", "age": 25, "city": "Los Angeles"}]
    json_file_path = 'data.json'
    csv_file_path = 'data.csv'

    # Преобразование JSON в CSV
    json2csv.json2csv(json_data_list, csv_file_path)

    # Преобразование CSV обратно в JSON
    csv_data = csv_to_json(csv_file_path, json_file_path)
    if csv_data:
        if isinstance(csv_data, list):
            if isinstance(csv_data[0], dict):
                print("CSV data (list of dictionaries):")
            else:
                print("CSV data (list of values):")
            print(csv_data)
        else:
            print("Failed to read CSV data.")
"""

import json
import csv
from pathlib import Path
from typing import List, Dict, Optional
from types import SimpleNamespace
from src.logger.logger import logger


def csv2dict(csv_file: str | Path, *args, **kwargs) -> dict | None:
    """
    Преобразует CSV данные в словарь.

    Args:
        csv_file (str | Path): Путь к CSV файлу для чтения.

    Returns:
        dict | None: Словарь, содержащий данные из CSV, преобразованные в формат JSON,
                     или `None`, если преобразование не удалось.

    Raises:
        Exception: Если не удается прочитать CSV файл.
    """
    try:
        with open(csv_file, 'r', encoding='utf-8') as file: # Открываем csv_file для чтения с указанием кодировки utf-8
            reader = csv.DictReader(file, *args, **kwargs) # Создаем объект DictReader для чтения CSV файла как словаря
            data:List[Dict] = list(reader) # Преобразуем данные из CSV файла в список словарей
        return data # Возвращаем полученные данные
    except FileNotFoundError as ex: # Ловим исключение, если файл не найден
        logger.error(f'Файл {csv_file} не найден', ex, exc_info=True) # Логируем ошибку
        return None # Возвращаем None в случае ошибки
    except Exception as ex: # Ловим другие исключения
        logger.error(f'Не удалось прочитать CSV файл {csv_file}', ex, exc_info=True) # Логируем ошибку
        return None # Возвращаем None в случае ошибки


def csv2ns(csv_file: str | Path, *args, **kwargs) -> SimpleNamespace | None:
    """
    Преобразует CSV данные в объекты SimpleNamespace.

    Args:
        csv_file (str | Path): Путь к CSV файлу для чтения.

    Returns:
        SimpleNamespace | None: Объект SimpleNamespace, содержащий данные из CSV,
                                 или `None`, если преобразование не удалось.

    Raises:
        Exception: Если не удается прочитать CSV файл.
    """
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:  # Открываем csv_file для чтения с указанием кодировки utf-8
            reader = csv.DictReader(file, *args, **kwargs)  # Создаем объект DictReader для чтения CSV файла как словаря
            data: List[Dict] = list(reader)  # Преобразуем данные из CSV файла в список словарей
        
        # Преобразуем список словарей в список объектов SimpleNamespace
        namespace_objects:List[SimpleNamespace] = [SimpleNamespace(**item) for item in data] # для каждого элемента item в data создаем объект SimpleNamespace

        return namespace_objects # Возвращаем полученные данные
    
    except FileNotFoundError as ex:  # Ловим исключение, если файл не найден
        logger.error(f'Файл {csv_file} не найден', ex, exc_info=True) # Логируем ошибку
        return None # Возвращаем None в случае ошибки
    except Exception as ex: # Ловим другие исключения
        logger.error(f'Не удалось прочитать CSV файл {csv_file}', ex, exc_info=True) # Логируем ошибку
        return None # Возвращаем None в случае ошибки

def csv_to_json(
    csv_file_path: str | Path,
    json_file_path: str | Path,
    exc_info: bool = True
) -> List[Dict[str, str]] | None:
    """
    Преобразует CSV файл в формат JSON и сохраняет его в JSON файл.

    Args:
        csv_file_path (str | Path): Путь к CSV файлу для чтения.
        json_file_path (str | Path): Путь к JSON файлу для сохранения.
        exc_info (bool, optional): Если True, включает информацию трассировки в лог. По умолчанию True.

    Returns:
        List[Dict[str, str]] | None: JSON данные в виде списка словарей, или None, если преобразование не удалось.

    Example:
        >>> json_data = csv_to_json('dialogue_log.csv', 'dialogue_log.json')
        >>> print(json_data)
        [{'role': 'user', 'content': 'Hello'}, {'role': 'assistant', 'content': 'Hi there!'}]
    """
    try:
        data: List[Dict[str,str]] | None = csv2dict(csv_file_path) # Читаем CSV файл и преобразуем его в список словарей
        if data is not None: # Проверяем, что данные успешно прочитаны
            with open(json_file_path, 'w', encoding='utf-8') as jsonfile: # Открываем json_file_path для записи с указанием кодировки utf-8
                json.dump(data, jsonfile, indent=4, ensure_ascii=False) # Записываем данные в JSON файл с отступами и без экранирования ASCII
            return data # Возвращаем полученные данные
        return None # Возвращаем None, если данные не были прочитаны
    except FileNotFoundError as ex: # Ловим исключение, если файл не найден
        logger.error(f"Файл {csv_file_path} не найден", ex, exc_info=exc_info) # Логируем ошибку
        return None # Возвращаем None в случае ошибки
    except Exception as ex: # Ловим другие исключения
        logger.error("Failed to convert CSV to JSON", ex, exc_info=exc_info) # Логируем ошибку
        return None # Возвращаем None в случае ошибки