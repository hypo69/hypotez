### **Анализ кода модуля `src.utils.jjson`**

## \file hypotez/src/utils/jjson.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для работы с JSON и SimpleNamespace
=================================================

Модуль содержит функции для загрузки и сохранения JSON данных,
а также для преобразования между JSON и SimpleNamespace объектами.

Пример использования
----------------------

>>> from src.utils.jjson import j_loads, j_dumps
>>> data = {'key': 'value'}
>>> j_dumps(data, 'example.json')
>>> loaded_data = j_loads('example.json')
"""

Качество кода:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Наличие функций для работы с JSON и SimpleNamespace.
    - Обработка исключений при чтении и записи файлов.
    - Использование `logger` для логирования ошибок.
    - Преобразование типов для обеспечения совместимости данных.
- **Минусы**:
    - Не все функции имеют подробные docstring.
    - Отсутствует проверка типов для входных данных в некоторых функциях.
    - Некоторые комментарии не совсем ясны и требуют уточнений.
    - Есть закомментированный код.
    - Не все переменные аннотированы.

Рекомендации по улучшению:

1.  Добавить подробные docstring для каждой функции и метода, описывающие их назначение, параметры, возвращаемые значения и возможные исключения.
2.  Улучшить обработку ошибок, добавив более конкретные исключения и информативные сообщения логирования.
3.  Добавить аннотации типов для всех переменных, чтобы улучшить читаемость и поддерживаемость кода.
4.  Удалить закомментированный код.
5.  Проверить и обновить комментарии, чтобы они были более ясными и точными.
6.  Использовать `_convert_to_dict` при чтении json-файлов.

Оптимизированный код:

```python
import json
import os
import re
import codecs
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from types import SimpleNamespace
#import pandas as pd
from json_repair import repair_json
from collections import OrderedDict


from src.logger.logger import logger
from .convertors.dict import dict2ns

from dataclasses import dataclass, field

@dataclass
class Config:
    MODE_WRITE:str = "w"
    MODE_APPEND_START:str = "a+"
    MODE_APPEND_END:str = "+a"

def _convert_to_dict(value: Any) -> Any:
    """Преобразует SimpleNamespace и списки в словари.

    Args:
        value (Any): Значение для преобразования.

    Returns:
        Any: Преобразованное значение.
    """
    if isinstance(value, SimpleNamespace):
        return {key: _convert_to_dict(val) for key, val in vars(value).items()}
    if isinstance(value, dict):
        return {key: _convert_to_dict(val) for key, val in value.items()}
    if isinstance(value, list):
        return [_convert_to_dict(item) for item in value]
    return value

def _read_existing_data(path: Path, exc_info: bool = True) -> dict:
    """Считывает существующие JSON данные из файла.

    Args:
        path (Path): Путь к файлу.
        exc_info (bool): Логировать ли расширенную информацию об ошибке.

    Returns:
        dict: Словарь с данными из файла или пустой словарь в случае ошибки.
    """
    try:
        # Чтение содержимого файла и преобразование в словарь
        json_string = path.read_text(encoding="utf-8")
        return _convert_to_dict(json.loads(json_string))
    except json.JSONDecodeError as ex:
        logger.error(f"Ошибка при декодировании JSON в файле {path}: {ex}", exc_info=exc_info)
        return {}
    except Exception as ex:
        logger.error(f"Ошибка при чтении файла {path=}: {ex}", exc_info=exc_info)
        return {}

def _merge_data(
    data: Dict, existing_data: Dict, mode: str
) -> Dict:
    """Объединяет новые данные с существующими данными в зависимости от режима.

    Args:
        data (Dict): Новые данные для объединения.
        existing_data (Dict): Существующие данные.
        mode (str): Режим объединения ("w", "a+", "+a").

    Returns:
        Dict: Объединенные данные.
    """
    try:
        if mode == Config.MODE_APPEND_START:
            if isinstance(data, list) and isinstance(existing_data, list):
               return data + existing_data
            if isinstance(data, dict) and isinstance(existing_data, dict):
                 existing_data.update(data)
            return existing_data
        elif mode == Config.MODE_APPEND_END:
            if isinstance(data, list) and isinstance(existing_data, list):
                return existing_data + data
            if isinstance(data, dict) and isinstance(existing_data, dict):
                 data.update(existing_data)
            return data
        return data
    except Exception as ex:
        logger.error(ex)
        return {}

def j_dumps(
    data: Union[Dict, SimpleNamespace, List[Dict], List[SimpleNamespace]],
    file_path: Optional[Path] = None,
    ensure_ascii: bool = False,
    mode: str = Config.MODE_WRITE,
    exc_info: bool = True,
) -> Optional[Dict]:
    """Сохраняет JSON данные в файл или возвращает JSON данные в виде словаря.

    Args:
        data (Dict | SimpleNamespace | List[Dict] | List[SimpleNamespace]): JSON данные для сохранения.
        file_path (Optional[Path], optional): Путь к файлу. Если None, возвращает JSON как словарь. Defaults to None.
        ensure_ascii (bool, optional): Экранировать ли не-ASCII символы. Defaults to True.
        mode (str, optional): Режим открытия файла ("w", "a+", "+a"). Defaults to "w".
        exc_info (bool, optional): Логировать ли расширенную информацию об ошибке. Defaults to True.

    Returns:
        Optional[Dict]: JSON данные в виде словаря при успехе или None при ошибке.

    Raises:
        ValueError: Если указан неподдерживаемый режим файла.
    """

    path = Path(file_path) if isinstance(file_path, (str, Path)) else None

    if isinstance(data, str):
        try:
            # Попытка исправить JSON строку
            data = repair_json(data)
        except Exception as ex:
            logger.error(f"Ошибка при преобразовании строки: {data}", ex, exc_info)
            return None

    # Преобразование данных в словарь
    data = _convert_to_dict(data)

    if mode not in {Config.MODE_WRITE, Config.MODE_APPEND_START, Config.MODE_APPEND_END}:
        mode = Config.MODE_WRITE

    existing_data = {}
    if path and path.exists() and mode in {Config.MODE_APPEND_START, Config.MODE_APPEND_END}:
        existing_data = _read_existing_data(path, exc_info)
    
    data = _merge_data(data, existing_data, mode)
    
    if path:
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            json.dump(data, path.open(mode, encoding="utf-8"), ensure_ascii=ensure_ascii, indent=4)
            #path.write_text(json.dumps(data, ensure_ascii=ensure_ascii, indent=4), encoding='utf-8')
        except Exception as ex:
             logger.error(f"Не удалось записать в файл {path}: ", ex, exc_info=exc_info)
             return None
        return data
    return data

def _decode_strings(data: Any) -> Any:
    """Рекурсивно декодирует строки в структуре данных.

    Args:
        data (Any): Данные для декодирования.

    Returns:
        Any: Декодированные данные.
    """
    if isinstance(data, str):
        try:
           return codecs.decode(data, 'unicode_escape')
        except Exception:
            return data
    if isinstance(data, list):
        return [_decode_strings(item) for item in data]
    if isinstance(data, dict):
        return {
            _decode_strings(key): _decode_strings(value) for key, value in data.items()
        }
    return data

def _string_to_dict(json_string: str) -> dict:
    """Удаляет markdown кавычки и парсит JSON строку.

    Args:
        json_string (str): JSON строка.

    Returns:
        dict: Словарь, полученный из JSON строки.
    """
    # Удаление обрамляющих кавычек markdown
    if json_string.startswith(("```", "```json")) and json_string.endswith(
        ("```", "```\\n")
    ):
        json_string = json_string.strip("`").replace("json", "", 1).strip()
    try:
        # Попытка преобразовать строку в словарь
        return json.loads(json_string)
    except json.JSONDecodeError as ex:
        logger.error(f"Ошибка парсинга JSON:\\n {json_string}", ex, False)
        return {}

def j_loads(
    jjson: Union[dict, SimpleNamespace, str, Path, list], ordered: bool = True
) -> Union[dict, list]:
    """Загружает JSON или CSV данные из файла, каталога, строки или объекта.

    Args:
        jjson (dict | SimpleNamespace | str | Path | list): Путь к файлу/каталогу, JSON строка или JSON объект.
        ordered (bool, optional): Использовать ли OrderedDict для сохранения порядка элементов. Defaults to True.

    Returns:
        dict | list: Обработанные данные (словарь или список словарей).

    Raises:
        FileNotFoundError: Если указанный файл не найден.
        json.JSONDecodeError: Если JSON данные не могут быть распарсены.
    """
    try:
        if isinstance(jjson, SimpleNamespace):
            # Преобразование SimpleNamespace в словарь
            jjson = vars(jjson)

        if isinstance(jjson, Path):
            if jjson.is_dir():
                # Загрузка всех JSON файлов из директории
                files = list(jjson.glob("*.json"))
                return [j_loads(file, ordered=ordered) for file in files]
            # if jjson.suffix.lower() == ".csv":
            #     return pd.read_csv(jjson).to_dict(orient="records")
             
            json_string = jjson.read_text(encoding="utf-8")
            return _string_to_dict(json_string)
        if isinstance(jjson, str):
            # Преобразование JSON строки в словарь
            return _string_to_dict(jjson)
        if isinstance(jjson, list):
             return _decode_strings(jjson)
        if isinstance(jjson, dict):
            # Декодирование строк в словаре
            return _decode_strings(jjson)
    except FileNotFoundError:
        logger.error(f"Файл не найден: {jjson}",None,False)
        return {}
    except json.JSONDecodeError as ex:
        logger.error(f"Ошибка парсинга JSON:\\n{jjson}\\n", ex, False)
        return {}
    except Exception as ex:
        logger.error(f"Ошибка загрузки данных: ", ex, False)
        return {}
    return {}

def j_loads_ns(
    jjson: Union[Path, SimpleNamespace, Dict, str], ordered: bool = True
) -> Union[SimpleNamespace, List[SimpleNamespace], Dict]:
    """Загружает JSON/CSV данные и преобразует в SimpleNamespace.

    Args:
        jjson (Path | SimpleNamespace | Dict | str): Путь к файлу, SimpleNamespace, словарь или JSON строка.
        ordered (bool, optional): Использовать ли OrderedDict для сохранения порядка элементов. Defaults to True.

    Returns:
        Union[SimpleNamespace, List[SimpleNamespace], Dict]: SimpleNamespace, список SimpleNamespace или словарь.
    """
    # Загрузка данных с использованием j_loads
    data = j_loads(jjson, ordered=ordered)
    if data:
        if isinstance(data, list):
            # Преобразование списка словарей в список SimpleNamespace
            return [dict2ns(item) for item in data]
        # Преобразование словаря в SimpleNamespace
        return dict2ns(data)
    return {}