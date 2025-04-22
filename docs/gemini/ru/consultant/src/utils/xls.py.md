### **Анализ кода модуля `src.utils.xls`**

## Качество кода:

- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код хорошо структурирован и читаем.
  - Присутствуют docstring для функций, что облегчает понимание их назначения.
  - Обработка исключений присутствует, что делает код более надежным.
  - Используются логи для отслеживания ошибок и записи информации о работе функций.
- **Минусы**:
  - Не все переменные аннотированы типами.
  - Используется `logging` вместо `logger` из модуля `src.logger`.
  - Не хватает более подробных комментариев внутри функций, объясняющих логику работы.
  - В коде используются конструкции `Union[]`, что не соответствует стандартам.

## Рекомендации по улучшению:

- Заменить `logging` на `logger` из `src.logger` для унификации логирования.
- Добавить аннотации типов для всех переменных, чтобы улучшить читаемость и облегчить отладку.
- Переписать docstring на русском языке и привести их в соответствие с требуемым форматом.
- Заменить `Union[]` на `|`.
- Добавить больше комментариев внутри функций для объяснения логики работы.

## Оптимизированный код:

```python
## \file /src/utils/xls.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для работы с Excel (`xls`) файлами: конвертация в JSON и из JSON в Excel (`xls`).
=======================================================================================

Модуль предоставляет функции для конвертации файлов Excel в формат JSON, обработки нескольких листов,
а также сохранения данных JSON обратно в файлы Excel.

Функции:
    read_xls_as_dict(xls_file: str, json_file: str = None, sheet_name: str | int = None) -> dict | list[dict] | bool:
        Читает Excel файл и конвертирует его в JSON. Опционально конвертирует указанный лист
        и сохраняет результат в JSON файл. Обрабатывает ошибки.

    save_xls_file(data: dict[str, list[dict]], file_path: str) -> bool:
        Сохраняет данные JSON в Excel файл. Данные должны быть словарем, где ключи - это названия листов,
        а значения - списки словарей, представляющие строки. Обрабатывает ошибки.

Примеры:
    # Чтение и опциональное сохранение в JSON
    data = read_xls_as_dict('input.xlsx', 'output.json', 'Sheet1')  # Читает лист с именем 'Sheet1'
    if data:
        print(data)  # Вывод будет {'Sheet1': [{...}]}

    # Сохранение из JSON данных
    data_to_save = {'Sheet1': [{'column1': 'value1', 'column2': 'value2'}]}
    success = save_xls_file(data_to_save, 'output.xlsx')
    if success:
        print("Успешно сохранено в output.xlsx")

.. module:: src.utils.xls
"""

import pandas as pd
import json
from typing import List, Dict, Union, Optional
from pathlib import Path
from src.logger import logger  # Используем logger из модуля src.logger


def read_xls_as_dict(
    xls_file: str,
    json_file: str = None,
    sheet_name: str | int = None
) -> dict | list[dict] | bool:
    """
    Читает Excel файл и конвертирует его в JSON.

    Args:
        xls_file (str): Путь к Excel файлу.
        json_file (str, optional): Путь для сохранения JSON файла. Defaults to None.
        sheet_name (str | int, optional): Имя листа для конвертации. Если None, конвертируются все листы. Defaults to None.

    Returns:
        dict | list[dict] | bool: Словарь с данными из Excel, список словарей (если указан sheet_name) или False в случае ошибки.
    
    Raises:
        FileNotFoundError: Если Excel файл не найден.
        Exception: Если возникает ошибка при обработке листов.

    Example:
        >>> data = read_xls_as_dict('input.xlsx', 'output.json', 'Sheet1')
        >>> if data:
        ...     print(data)
    """
    try:
        xls_file_path: Path = Path(xls_file)

        # Проверка существования Excel файла
        if not xls_file_path.exists():
            logger.error(f"Excel файл не найден: {xls_file}")  # Логируем ошибку
            return False  # Функция возвращает False при ошибке

        xls: pd.ExcelFile = pd.ExcelFile(xls_file)

        # Если sheet_name не указан, обрабатываем все листы
        if sheet_name is None:
            data_dict: dict = {}
            # Перебор всех листов в Excel файле
            for sheet in xls.sheet_names:
                try:
                    df: pd.DataFrame = pd.read_excel(xls, sheet_name=sheet)
                    data_dict[sheet] = df.to_dict(orient='records')  # Преобразуем DataFrame в словарь
                except Exception as ex:
                    logger.error(f"Ошибка при обработке листа '{sheet}': {ex}", ex, exc_info=True)  # Логируем ошибку
                    return False  # Функция возвращает False при ошибке

        # Если sheet_name указан, обрабатываем только его
        else:
            try:
                df: pd.DataFrame = pd.read_excel(xls, sheet_name=sheet_name)
                data_dict: list[dict] = df.to_dict(orient='records')  # Преобразуем DataFrame в словарь
            except Exception as ex:
                logger.error(f"Ошибка при обработке листа '{sheet_name}': {ex}", ex, exc_info=True)  # Логируем ошибку
                return False  # Функция возвращает False при ошибке

        # Если указан json_file, сохраняем данные в JSON файл
        if json_file:
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data_dict, f, ensure_ascii=False, indent=4)  # Сохраняем данные в JSON файл
                logger.info(f"JSON данные сохранены в {json_file}")  # Логируем информацию об успешном сохранении

        return data_dict  # Функция возвращает словарь с данными

    except FileNotFoundError as ex:
        logger.error(f"Файл не найден: {ex}", ex, exc_info=True)  # Логируем ошибку
        return False  # Функция возвращает False при ошибке
    except Exception as ex:
        logger.error(f"Произошла ошибка: {ex}", ex, exc_info=True)  # Логируем ошибку
        return False  # Функция возвращает False при ошибке


def save_xls_file(data: Dict[str, List[Dict]], file_path: str) -> bool:
    """
    Сохраняет JSON данные в Excel файл.

    Args:
        data (Dict[str, List[Dict]]): Данные для сохранения, где ключи - названия листов, значения - списки словарей (строки).
        file_path (str): Путь для сохранения Excel файла.

    Returns:
        bool: True в случае успешного сохранения, False в случае ошибки.
    
    Raises:
        Exception: Если возникает ошибка при сохранении Excel файла.

    Example:
        >>> data_to_save = {'Sheet1': [{'column1': 'value1', 'column2': 'value2'}]}
        >>> success = save_xls_file(data_to_save, 'output.xlsx')
        >>> if success:
        ...     print("Успешно сохранено в output.xlsx")
    """
    try:
        # Используем менеджер контекста для автоматического закрытия файла
        with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
            # Перебираем листы и их данные
            for sheet_name, rows in data.items():
                df: pd.DataFrame = pd.DataFrame(rows)
                df.to_excel(writer, sheet_name=sheet_name, index=False)  # Записываем DataFrame в Excel файл
                logger.info(f"Лист '{sheet_name}' сохранен в {file_path}")  # Логируем информацию об успешном сохранении
        return True  # Функция возвращает True при успехе
    except Exception as ex:
        logger.error(f"Ошибка при сохранении Excel файла: {ex}", ex, exc_info=True)  # Логируем ошибку
        return False  # Функция возвращает False при ошибке