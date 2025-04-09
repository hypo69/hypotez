### **Анализ кода модуля `jjson.py`**

## \file /hypotez/src/utils/jjson.py

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Наличие функций для работы с JSON данными (загрузка, выгрузка, преобразование).
    - Обработка исключений с логированием ошибок.
    - Поддержка различных типов входных данных для загрузки JSON.
    - Использование `SimpleNamespace` для удобного доступа к данным.
- **Минусы**:
    - Не все функции имеют подробные docstring.
    - Не все переменные аннотированы типами.
    - Некоторые участки кода требуют рефакторинга для повышения читаемости.
    - Использование `Union` вместо `|` для обозначения типов.

**Рекомендации по улучшению:**

1.  **Документирование функций**:
    - Добавить подробные docstring для всех функций, включая описание аргументов, возвращаемых значений и возможных исключений.
    - Описать назначение каждой функции и привести примеры использования.
2.  **Улучшение обработки исключений**:
    - Указывать конкретные типы исключений в блоках `except`.
    - Добавить контекстную информацию в сообщения об ошибках.
3.  **Рефакторинг**:
    - Избавиться от лишних комментариев и неиспользуемого кода.
    - Разбить сложные функции на более простые и понятные.
4.  **Аннотации типов**:
    - Добавить аннотации типов для всех переменных и аргументов функций.
5.  **Использование `|` вместо `Union`**:
    - Заменить `Union[type1, type2]` на `type1 | type2`.
6. **Использовать `logger` из `src.logger.logger`:**
    - Всегда используй модуль `logger` из `src.logger.logger`.
    - Ошибки должны логироваться с использованием `logger.error`.
    - Пример:
        ```python
            try:
                ...
            except Exception as ex:
                logger.error('Error while processing data', ех, exc_info=True)
        ```
7. **Использовать одинарные ковычки**
   - Всегда используй одинарные кавычки (`'`) в Python-коде. Например:
     ```python
     a = 'A1'
     b = ['a', 'b']
     c = {'key': 'value'}
     ```

**Оптимизированный код:**

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


class Config:
    """
    Класс, содержащий константы для режимов записи файлов.
    =======================================================
    Содержит константы, определяющие режимы записи в файл: перезапись, добавление в начало и добавление в конец.

    Атрибуты класса:
        MODE_WRITE (str): Режим перезаписи файла ('w').
        MODE_APPEND_START (str): Режим добавления данных в начало файла ('a+').
        MODE_APPEND_END (str): Режим добавления данных в конец файла ('+a').

    Пример использования:
        >>> Config.MODE_WRITE
        'w'
    """
    MODE_WRITE: str = 'w'
    MODE_APPEND_START: str = 'a+'
    MODE_APPEND_END: str = '+a'


def _convert_to_dict(value: Any) -> Any:
    """
    Преобразует SimpleNamespace и списки в словари.

    Args:
        value (Any): Значение для преобразования.

    Returns:
        Any: Преобразованное значение в виде словаря, списка или исходного значения.
    """
    if isinstance(value, SimpleNamespace):
        return {key: _convert_to_dict(val) for key, val in vars(value).items()}
    if isinstance(value, dict):
        return {key: _convert_to_dict(val) for key, val in value.items()}
    if isinstance(value, list):
        return [_convert_to_dict(item) for item in value]
    return value


def _read_existing_data(path: Path, exc_info: bool = True) -> dict:
    """
    Считывает существующие JSON данные из файла.

    Args:
        path (Path): Путь к файлу.
        exc_info (bool, optional): Логировать ли информацию об исключении. Defaults to True.

    Returns:
        dict: Словарь с данными из файла или пустой словарь в случае ошибки.
    """
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError as ex:
        logger.error(f'Ошибка при декодировании JSON в файле {path}: {ex}', exc_info=exc_info)
        return {}
    except Exception as ex:
        logger.error(f'Ошибка при чтении файла {path=}: {ex}', exc_info=exc_info)
        return {}


def _merge_data(data: Dict, existing_data: Dict, mode: str) -> Dict:
    """
    Объединяет новые данные с существующими данными в зависимости от режима.

    Args:
        data (Dict): Новые данные для объединения.
        existing_data (Dict): Существующие данные.
        mode (str): Режим объединения (Config.MODE_APPEND_START или Config.MODE_APPEND_END).

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
        logger.error(ex, exc_info=True)
        return {}


def j_dumps(
    data: Dict | SimpleNamespace | List[Dict] | List[SimpleNamespace],
    file_path: Optional[Path] = None,
    ensure_ascii: bool = False,
    mode: str = Config.MODE_WRITE,
    exc_info: bool = True,
) -> Optional[Dict]:
    """
    Выгружает JSON данные в файл или возвращает JSON данные в виде словаря.

    Args:
        data (Dict | SimpleNamespace | List[Dict] | List[SimpleNamespace]): JSON-совместимые данные или объекты SimpleNamespace для выгрузки.
        file_path (Optional[Path], optional): Путь к выходному файлу. Если None, возвращает JSON как словарь. Defaults to None.
        ensure_ascii (bool, optional): Если True, экранирует не-ASCII символы в выводе. Defaults to True.
        mode (str, optional): Режим открытия файла ('w', 'a+', '+a'). Defaults to 'w'.
        exc_info (bool, optional): Если True, логирует исключения с трассировкой. Defaults to True.

    Returns:
        Optional[Dict]: JSON данные в виде словаря в случае успеха, или None в случае ошибки.

    Raises:
        ValueError: Если режим файла не поддерживается.

    Example:
        >>> data = {'key': 'value'}
        >>> file_path = Path('example.json')
        >>> result = j_dumps(data, file_path)
        >>> print(result)
        {'key': 'value'}
    """
    path: Path | None = Path(file_path) if isinstance(file_path, (str, Path)) else None

    if isinstance(data, str):
        try:
            data = repair_json(data)
        except Exception as ex:
            logger.error(f'Ошибка при преобразовании строки: {data}', ex, exc_info=exc_info)
            return None

    data = _convert_to_dict(data)

    if mode not in {Config.MODE_WRITE, Config.MODE_APPEND_START, Config.MODE_APPEND_END}:
        mode = Config.MODE_WRITE

    existing_data: dict = {}
    if path and path.exists() and mode in {Config.MODE_APPEND_START, Config.MODE_APPEND_END}:
        existing_data = _read_existing_data(path, exc_info)

    data = _merge_data(data, existing_data, mode)

    if path:
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            json.dump(data, path.open(mode, encoding='utf-8'), ensure_ascii=ensure_ascii, indent=4)
            # path.write_text(json.dumps(data, ensure_ascii=ensure_ascii, indent=4), encoding='utf-8')
        except Exception as ex:
            logger.error(f'Не удалось записать в файл {path}: ', ex, exc_info=exc_info)
            return None
        return data
    return data


def _decode_strings(data: Any) -> Any:
    """
    Рекурсивно декодирует строки в структуре данных.

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
    """
    Удаляет markdown кавычки и парсит JSON строку.

    Args:
        json_string (str): JSON строка.

    Returns:
        dict: Словарь, полученный из JSON строки.
    """
    if json_string.startswith(('```', '```json')) and json_string.endswith(
        ('```', '```\n')
    ):
        json_string = json_string.strip('`').replace('json', '', 1).strip()
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as ex:
        logger.error(f'Ошибка парсинга JSON:\\n {json_string}', ex, False)
        return {}


def j_loads(
    jjson: dict | SimpleNamespace | str | Path | list, ordered: bool = True
) -> dict | list:
    """
    Загружает JSON или CSV данные из файла, директории, строки или объекта.

    Args:
        jjson (dict | SimpleNamespace | str | Path | list): Путь к файлу/директории, JSON строка или JSON объект.
        ordered (bool, optional): Использовать ли OrderedDict для сохранения порядка элементов. Defaults to True.

    Returns:
        dict | list: Обработанные данные (словарь или список словарей).

    Raises:
        FileNotFoundError: Если указанный файл не найден.
        json.JSONDecodeError: Если JSON данные не могут быть распарсены.

    Example:
        >>> file_path = Path('example.json')
        >>> data = j_loads(file_path)
        >>> print(data)
        {'key': 'value'}
    """
    try:
        if isinstance(jjson, SimpleNamespace):
            jjson = vars(jjson)

        if isinstance(jjson, Path):
            if jjson.is_dir():
                files = list(jjson.glob('*.json'))
                return [j_loads(file, ordered=ordered) for file in files]
            # if jjson.suffix.lower() == ".csv":
            #     return pd.read_csv(jjson).to_dict(orient="records")

            return json.loads(jjson.read_text(encoding='utf-8'))
        if isinstance(jjson, str):
            return _string_to_dict(jjson)
        if isinstance(jjson, list):
            return _decode_strings(jjson)
        if isinstance(jjson, dict):
            return _decode_strings(jjson)
    except FileNotFoundError:
        logger.error(f'Файл не найден: {jjson}', None, False)
        return {}
    except json.JSONDecodeError as ex:
        logger.error(f'Ошибка парсинга JSON:\\n{jjson}\\n', ex, False)
        return {}
    except Exception as ex:
        logger.error(f'Ошибка при загрузке данных: ', ex, False)
        return {}
    return {}


def j_loads_ns(
    jjson: Path | SimpleNamespace | Dict | str, ordered: bool = True
) -> SimpleNamespace | List[SimpleNamespace] | Dict:
    """
    Загружает JSON/CSV данные и преобразует в SimpleNamespace.

    Args:
        jjson (Path | SimpleNamespace | Dict | str): Путь к файлу/директории, JSON строка или JSON объект.
        ordered (bool, optional): Использовать ли OrderedDict для сохранения порядка элементов. Defaults to True.

    Returns:
        SimpleNamespace | List[SimpleNamespace] | Dict: Обработанные данные в виде SimpleNamespace или списка SimpleNamespace.

    Example:
        >>> file_path = Path('example.json')
        >>> data = j_loads_ns(file_path)
        >>> print(data)
        namespace(key='value')
    """
    data = j_loads(jjson, ordered=ordered)
    if data:
        if isinstance(data, list):
            return [dict2ns(item) for item in data]
        return dict2ns(data)
    return {}