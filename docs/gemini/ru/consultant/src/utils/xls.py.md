### **Анализ кода модуля `src.utils.xls`**

## \file /src/utils/xls.py

Модуль предоставляет функции для конвертации Excel (`xls`) файлов в JSON формат и обратно.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Наличие docstring для модуля и функций.
    - Обработка исключений.
    - Логирование основных этапов работы.
    - Использование `Pathlib` для работы с путями к файлам.
- **Минусы**:
    - Отсутствие аннотаций типов для переменных внутри функций.
    - Использование `Union` вместо `|` для указания нескольких типов.
    - Не используется модуль `logger` из `src.logger`.
    - Docstring на английском языке.
    - Не все ошибки обрабатываются с использованием `logger.error(..., ex, exc_info=True)`.
    - Не указаны `Args`, `Returns`, `Raises` в docstring.

**Рекомендации по улучшению:**

1.  Добавить аннотации типов для всех переменных внутри функций.
2.  Заменить `Union` на `|` для указания нескольких типов.
3.  Использовать модуль `logger` из `src.logger` для логирования.
4.  Перевести docstring на русский язык и привести к единому стандарту.
5.  Указывать `Args`, `Returns`, `Raises` в docstring.
6.  Все исключения обрабатывать с использованием `logger.error(..., ex, exc_info=True)`.
7.  Использовать одинарные кавычки для строк.

**Оптимизированный код:**

```python
## \file /src/utils/xls.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для работы с Excel (`xls`) файлами.
==========================================

Модуль предоставляет функции для конвертации Excel файлов в JSON формат и обратно.

Пример использования
----------------------

>>> data = read_xls_as_dict('input.xlsx', 'output.json', 'Sheet1')
>>> if data:
...     print(data)
>>> data_to_save = {'Sheet1': [{'column1': 'value1', 'column2': 'value2'}]}
>>> success = save_xls_file(data_to_save, 'output.xlsx')
>>> if success:
...     print("Successfully saved to output.xlsx")
"""

import pandas as pd
import json
from typing import List, Dict, Union, Optional
from pathlib import Path
from src.logger import logger # Используем модуль logger из src.logger


def read_xls_as_dict(
    xls_file: str,
    json_file: Optional[str] = None,
    sheet_name: Optional[str | int] = None
) -> dict | list[dict] | bool:
    """
    Чтение Excel файла и конвертация в JSON.

    Функция читает Excel файл и конвертирует его в JSON формат.
    Опционально, можно указать конкретный лист для конвертации и сохранить результат в JSON файл.

    Args:
        xls_file (str): Путь к Excel файлу.
        json_file (Optional[str], optional): Путь к JSON файлу для сохранения результата. По умолчанию `None`.
        sheet_name (Optional[str | int], optional): Название или индекс листа для конвертации. По умолчанию `None`.

    Returns:
        dict | list[dict] | bool: Возвращает словарь с данными из Excel файла, список словарей, если указан конкретный лист, или `False` в случае ошибки.
    
    Raises:
        FileNotFoundError: Если файл не найден.
        Exception: Если произошла ошибка при обработке файла.
    
    Example:
        >>> data = read_xls_as_dict('input.xlsx', 'output.json', 'Sheet1')
        >>> if data:
        ...     print(data)
    """
    try:
        xls_file_path: Path = Path(xls_file) # Явное указание типа переменной
        if not xls_file_path.exists():
            logger.error(f'Excel file not found: {xls_file}') # Используем logger.error
            return False  # Indicate failure

        xls: pd.ExcelFile = pd.ExcelFile(xls_file) # Явное указание типа переменной

        if sheet_name is None:
            data_dict: dict = {} # Явное указание типа переменной
            for sheet in xls.sheet_names:
                try:
                    df: pd.DataFrame = pd.read_excel(xls, sheet_name=sheet) # Явное указание типа переменной
                    data_dict[sheet]: list[dict] = df.to_dict(orient='records') # Явное указание типа переменной
                except Exception as ex:
                    logger.error(f'Error processing sheet \'{sheet}\'', ex, exc_info=True) # Используем logger.error c exc_info
                    return False

        else:
            try:
                df: pd.DataFrame = pd.read_excel(xls, sheet_name=sheet_name) # Явное указание типа переменной
                data_dict: list[dict] = df.to_dict(orient='records') # Явное указание типа переменной
            except Exception as ex:
                logger.error(f'Error processing sheet \'{sheet_name}\'', ex, exc_info=True) # Используем logger.error c exc_info
                return False

        if json_file:
            try:
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(data_dict, f, ensure_ascii=False, indent=4)
                    logger.info(f'JSON data saved to {json_file}') # Используем logger.info
            except Exception as ex:
                logger.error(f'Error saving JSON file {json_file}', ex, exc_info=True)
                return False

        return data_dict

    except FileNotFoundError as ex:
        logger.error(f'File not found: {ex}', exc_info=True) # Используем logger.error c exc_info
        return False
    except Exception as ex:
        logger.error(f'An error occurred: {ex}', exc_info=True) # Используем logger.error c exc_info
        return False


def save_xls_file(data: Dict[str, List[Dict]], file_path: str) -> bool:
    """
    Сохранение JSON данных в Excel файл.

    Функция сохраняет JSON данные в Excel файл.
    Данные должны быть словарем, где ключи - это названия листов, а значения - списки словарей, представляющие строки.

    Args:
        data (Dict[str, List[Dict]]): Данные для сохранения в формате словаря.
        file_path (str): Путь к Excel файлу.

    Returns:
        bool: `True`, если сохранение прошло успешно, `False` в противном случае.
    
    Raises:
        Exception: Если произошла ошибка при сохранении файла.

    Example:
        >>> data_to_save = {'Sheet1': [{'column1': 'value1', 'column2': 'value2'}]}
        >>> success = save_xls_file(data_to_save, 'output.xlsx')
        >>> if success:
        ...     print("Successfully saved to output.xlsx")
    """
    try:
        with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
            for sheet_name, rows in data.items():
                df: pd.DataFrame = pd.DataFrame(rows) # Явное указание типа переменной
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                logger.info(f'Sheet \'{sheet_name}\' saved to {file_path}') # Используем logger.info
        return True
    except Exception as ex:
        logger.error(f'Error saving Excel file: {ex}', exc_info=True) # Используем logger.error c exc_info
        return False