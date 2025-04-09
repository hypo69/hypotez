### **Анализ кода модуля `src.utils.xls`**

**Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Наличие обработки исключений.
  - Использование `logging` для записи информации об операциях и ошибках.
  - Предоставление документации к функциям.
- **Минусы**:
  - Отсутствие аннотации типов для локальных переменных.
  - Использование `Union` вместо `|`.
  - Не используется `logger` из `src.logger.logger`.
  - docstring на английском языке.
  - Неполная документация.
  - Не используются одинарные ковычки.

**Рекомендации по улучшению**:

1.  **Общие улучшения**:
    - Заменить `Union[str, int]` на `str | int` для аннотации типов.
    - Использовать `logger` из `src.logger.logger` вместо стандартного `logging`.
    - Добавить аннотации типов для всех локальных переменных, где это возможно.
    - Перевести все docstring на русский язык.
    - Улучшить и дополнить документацию.
    - Использовать одинарные ковычки.

2.  **`read_xls_as_dict`**:
    - Добавить более подробное описание работы функции в docstring.
    - Явно указать, какие исключения могут быть вызваны и при каких условиях.
    - Добавить примеры использования функции.
    - Использовать `ex` вместо `e` в блоках `except`.
    - Перефразировать комментарии в соответствии с рекомендациями, например, "проверяем существование файла" вместо "получаем путь".

3.  **`save_xls_file`**:
    - Аналогично `read_xls_as_dict`, улучшить документацию, добавить примеры использования и обрабатывать исключения с использованием `ex` вместо `e`.
    - Добавить более конкретное описание ошибок, которые могут возникнуть при сохранении файла.

**Оптимизированный код**:

```python
## \file /src/utils/xls.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для конвертации файлов Excel (`xls`) в JSON и JSON в Excel (`xls`)
=======================================================================

Модуль предоставляет функции для конвертации файлов Excel в формат JSON, обработки нескольких листов,
и сохранения данных JSON обратно в файлы Excel.

Пример использования
----------------------

>>> data = read_xls_as_dict('input.xlsx', 'output.json', 'Sheet1')
>>> if data:
...     print(data)  # Вывод: {'Sheet1': [{...}]}

>>> data_to_save = {'Sheet1': [{'column1': 'value1', 'column2': 'value2'}]}
>>> success = save_xls_file(data_to_save, 'output.xlsx')
>>> if success:
...     print('Файл успешно сохранен в output.xlsx')
"""

import pandas as pd
import json
from typing import List, Dict, Union, Optional
from pathlib import Path
from src.logger import logger  # Используем logger из src.logger

def read_xls_as_dict(
    xls_file: str,
    json_file: Optional[str] = None,
    sheet_name: Optional[str | int] = None
) -> Dict | List[Dict] | bool:
    """
    Читает Excel файл и конвертирует его в JSON. Опционально, конвертирует указанный лист и сохраняет результат в JSON файл.
    Обрабатывает ошибки.

    Args:
        xls_file (str): Путь к Excel файлу.
        json_file (Optional[str]): Путь для сохранения JSON файла (опционально). По умолчанию `None`.
        sheet_name (Optional[str | int]): Имя листа для конвертации (опционально). По умолчанию `None`.

    Returns:
        Dict | List[Dict] | bool:
            - Если `sheet_name` не указан, возвращает словарь, где ключи - имена листов, значения - списки словарей (строки).
            - Если `sheet_name` указан, возвращает список словарей (строки) для этого листа.
            - Возвращает `False` в случае ошибки.

    Raises:
        FileNotFoundError: Если Excel файл не найден.
        Exception: При возникновении других ошибок во время обработки файла.

    Example:
        >>> data = read_xls_as_dict('input.xlsx', 'output.json', 'Sheet1')
        >>> if data:
        ...     print(data)
        {'Sheet1': [{...}]}
    """
    try:
        xls_file_path: Path = Path(xls_file)  # Преобразуем путь к файлу в объект Path
        if not xls_file_path.exists():  # Проверяем, существует ли файл
            logger.error(f'Excel file not found: {xls_file}')  # Логируем ошибку
            return False  # Возвращаем False, указывая на неудачу

        xls: pd.ExcelFile = pd.ExcelFile(xls_file)  # Инициализируем ExcelFile

        if sheet_name is None:  # Если имя листа не указано
            data_dict: Dict = {}  # Инициализируем словарь для хранения данных
            for sheet in xls.sheet_names:  # Перебираем все листы в Excel файле
                try:
                    df: pd.DataFrame = pd.read_excel(xls, sheet_name=sheet)  # Читаем лист в DataFrame
                    data_dict[sheet] = df.to_dict(orient='records')  # Преобразуем DataFrame в список словарей
                except Exception as ex:  # Ловим исключения при обработке листов
                    logger.error(f'Error processing sheet \'{sheet}\': {ex}', exc_info=True)  # Логируем ошибку
                    return False  # Возвращаем False, указывая на неудачу

        else:  # Если имя листа указано
            try:
                df: pd.DataFrame = pd.read_excel(xls, sheet_name=sheet_name)  # Читаем указанный лист в DataFrame
                data_dict: List[Dict] = df.to_dict(orient='records')  # Преобразуем DataFrame в список словарей
            except Exception as ex:  # Ловим исключения при обработке листа
                logger.error(f'Error processing sheet \'{sheet_name}\': {ex}', exc_info=True)  # Логируем ошибку
                return False  # Возвращаем False, указывая на неудачу

        if json_file:  # Если указан файл для сохранения JSON
            with open(json_file, 'w', encoding='utf-8') as f:  # Открываем файл для записи
                json.dump(data_dict, f, ensure_ascii=False, indent=4)  # Записываем данные в JSON файл
                logger.info(f'JSON data saved to {json_file}')  # Логируем информацию об успешном сохранении

        return data_dict  # Возвращаем словарь с данными

    except FileNotFoundError as ex:  # Ловим исключение, если файл не найден
        logger.error(f'File not found: {ex}', exc_info=True)  # Логируем ошибку
        return False  # Возвращаем False, указывая на неудачу
    except Exception as ex:  # Ловим все остальные исключения
        logger.error(f'An error occurred: {ex}', exc_info=True)  # Логируем ошибку
        return False  # Возвращаем False, указывая на неудачу


def save_xls_file(data: Dict[str, List[Dict]], file_path: str) -> bool:
    """
    Сохраняет данные JSON в Excel файл.
    Args:
        data (Dict[str, List[Dict]]): Данные для сохранения. Ключи - имена листов, значения - списки словарей (строки).
        file_path (str): Путь для сохранения Excel файла.
    Returns:
        bool: True в случае успешного сохранения, False в случае ошибки.
    Raises:
        Exception: При возникновении ошибок во время сохранения файла.

    Example:
        >>> data_to_save = {'Sheet1': [{'column1': 'value1', 'column2': 'value2'}]}
        >>> success = save_xls_file(data_to_save, 'output.xlsx')
        >>> if success:
        ...     print('Файл успешно сохранен в output.xlsx')
        Файл успешно сохранен в output.xlsx
    """
    try:
        with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:  # Используем ExcelWriter для записи в Excel файл
            for sheet_name, rows in data.items():  # Перебираем листы и строки данных
                df: pd.DataFrame = pd.DataFrame(rows)  # Преобразуем строки в DataFrame
                df.to_excel(writer, sheet_name=sheet_name, index=False)  # Записываем DataFrame в Excel файл
                logger.info(f'Sheet \'{sheet_name}\' saved to {file_path}')  # Логируем информацию об успешном сохранении
        return True  # Возвращаем True, указывая на успех
    except Exception as ex:  # Ловим исключения при сохранении файла
        logger.error(f'Error saving Excel file: {ex}', exc_info=True)  # Логируем ошибку
        return False  # Возвращаем False, указывая на неудачу