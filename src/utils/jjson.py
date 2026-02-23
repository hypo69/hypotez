## \file /src/utils/jjson.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль JSON утилит для работы с JSON и CSV данными.
==================================================
Предоставляет функции для загрузки, сохранения, обработки и поиска данных
в JSON/CSV объектах и файлах.

Основные функции:
- `j_dumps(...)`: Сохраняет Python объекты в JSON файл.
- `j_loads(...)`: Загружает данные из JSON, CSV, строки, dict, list, SimpleNamespace.
- `j_loads_ns(...)`: Аналогично `j_loads`, но возвращает объекты SimpleNamespace.
- `sanitize_json_files(...)`: Проверяет и исправляет JSON файлы.
- `find_keys(...)`: Рекурсивно ищет ключи в структуре данных.
"""
import json
import csv
import codecs
import re
from pathlib import Path
from typing import Any, List as TypingList, Dict as TypingDict
from collections.abc import Mapping, Sequence
from types import SimpleNamespace
from dataclasses import dataclass
from json_repair import repair_json

from src.logger.logger import logger
from .convertors.dict import dict2ns
from .convertors.list import list2dict


@dataclass
class Config:
    """Конфигурационный класс для хранения констант режимов записи."""
    MODE_WRITE: str = 'w'
    MODE_APPEND_START: str = 'a+'
    MODE_APPEND_END: str = '+a'


def _convert_to_dict(value: Any) -> Any:
    """Рекурсивно конвертирует объекты SimpleNamespace и вложенные структуры в словари."""
    if isinstance(value, SimpleNamespace):
        return {k: _convert_to_dict(v) for k, v in vars(value).items()}
    if isinstance(value, dict):
        return {k: _convert_to_dict(v) for k, v in value.items()}
    if isinstance(value, list):
        return list2dict(value)
    return value


def _read_existing_data(path: Path, exc_info: bool = True) -> dict[Any, Any] | list[Any]:
    """Читает JSON данные из файла."""
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError as ex:
        logger.error(f'Error decoding existing JSON in {path}: {ex}', ex, exc_info=exc_info)
    except FileNotFoundError:
        logger.error(f'File not found for reading existing data: {path}', None, exc_info=exc_info)
    except Exception as ex:
        logger.error(f'Error reading {path=}: {ex}', ex, exc_info=exc_info)
    return {}


def _merge_data(data: dict[Any, Any] | list[Any],
                existing_data: dict[Any, Any] | list[Any],
                mode: str) -> dict[Any, Any] | list[Any]:
    """Объединяет новые данные с существующими согласно режиму."""
    try:
        if mode == Config.MODE_APPEND_START:
            if isinstance(data, list) and isinstance(existing_data, list):
                return data + existing_data
            if isinstance(data, dict) and isinstance(existing_data, dict):
                merged = existing_data.copy()
                merged.update(data)
                return merged
            return existing_data
        elif mode == Config.MODE_APPEND_END:
            if isinstance(data, list) and isinstance(existing_data, list):
                return existing_data + data
            if isinstance(data, dict) and isinstance(existing_data, dict):
                merged = data.copy()
                merged.update(existing_data)
                return merged
            return data
        return data
    except Exception as ex:
        logger.error(f'Error merging data: {ex}', ex, exc_info=True)
        return {}


def _read_csv_file(path: Path, delimiter: str = ';', encoding: str = 'cp1251') -> list[dict[str, Any]]:
    """Читает CSV файл и возвращает список словарей."""
    if not path.exists():
        logger.error(f'CSV file not found: {path}')
        return []
    try:
        with path.open('r', encoding=encoding, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=delimiter)
            rows = list(reader)
        logger.info(f'Loaded CSV file: {path}, rows={len(rows)}')
        return rows
    except Exception as ex:
        logger.error(f'Error reading CSV file: {path}', ex, exc_info=True)
        return []


def j_dumps(data: dict[Any, Any] | SimpleNamespace | list[Any] | str,
            file_path: Path | str | None = None,
            indent: int = 4,
            ensure_ascii: bool = False,
            mode: str = Config.MODE_WRITE,
            exc_info: bool = True) -> bool | dict[Any, Any] | list[Any] | None:
    """Сериализует Python объект в JSON строку или сохраняет его в файл."""
    processed_data: dict[Any, Any] | list[Any] | None
    path: Path | None = None

    if isinstance(data, str):
        data_as_obj = _string_to_dict(data)
        if not data_as_obj and data.strip() and data.strip() not in ('{}', '[]'):
            try:
                repaired_json_str: str = repair_json(data, return_objects=True)
                processed_data = json.loads(repaired_json_str)
            except Exception as ex_repair:
                logger.error(f'Error repairing/parsing JSON string', ex_repair, exc_info=exc_info)
                return False if file_path else None
        else:
            processed_data = data_as_obj
    else:
        processed_data = data

    if isinstance(processed_data, (SimpleNamespace, dict, list)):
        processed_data = _convert_to_dict(processed_data)
    else:
        logger.error(f'Unsupported data type for j_dumps: {type(processed_data)}', None, exc_info=exc_info)
        return False if file_path else None

    if file_path:
        path = Path(file_path)

    if path:
        final_data = processed_data
        if mode in {Config.MODE_APPEND_START, Config.MODE_APPEND_END}:
            if path.exists() and path.is_file():
                existing = _read_existing_data(path, exc_info)
                if isinstance(existing, (dict, list)):
                    final_data = _merge_data(processed_data, existing, mode)
            else:
                logger.info(f'Creating new file for append mode: {path}')
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open(Config.MODE_WRITE, encoding='utf-8') as f:
                json.dump(final_data, f, ensure_ascii=ensure_ascii, indent=indent)
            return True
        except Exception as ex:
            logger.error(f'Failed to write data to {path}', ex, exc_info=exc_info)
            return False
    return processed_data


def _decode_strings(data: Any) -> Any:
    """Рекурсивно декодирует строки из формата unicode_escape."""
    if isinstance(data, str):
        try:
            return codecs.decode(data, 'unicode_escape')
        except Exception:
            return data
    if isinstance(data, list):
        return [_decode_strings(i) for i in data]
    if isinstance(data, dict):
        return {_decode_strings(k): _decode_strings(v) for k, v in data.items()}
    return data


def _string_to_dict(json_string: str, return_objects: bool = False) -> dict[Any, Any] | list[Any]:
    """Удаляет Markdown-обёртки и парсит строку как JSON."""
    if not isinstance(json_string, str):
        logger.warning(f'_string_to_dict expects str, got {type(json_string)}')
        return {}
    cleaned = json_string.strip()
    if cleaned.startswith('```'):
        cleaned = re.sub(r'^```(?:json)?\s*', '', cleaned, count=1)
        cleaned = re.sub(r'\s*```$', '', cleaned, count=1).strip()
    if not cleaned:
        return {}
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        try:
            repaired = repair_json(cleaned)
            return json.loads(repaired)
        except Exception as ex:
            logger.error('Error repairing JSON string', ex)
            return {}
    except Exception as ex:
        logger.error('Unexpected error parsing JSON', ex)
        return {}


def j_loads(jjson: dict[Any, Any] | SimpleNamespace | str | Path | list[Any],
            ordered: bool = True) -> dict[Any, Any] | list[Any]:
    """Загружает JSON или CSV-совместимые данные из различных источников."""
    jjson_internal: Any = jjson
    if isinstance(jjson, SimpleNamespace):
        jjson_internal = vars(jjson)

    try:
        if isinstance(jjson_internal, Path):
            path_obj: Path = jjson_internal

            if not path_obj.exists():
                logger.error(f'Path does not exist: {path_obj}')
                return {}

            # Поддержка CSV
            if path_obj.suffix.lower() == '.csv':
                csv_data = _read_csv_file(path_obj)
                return csv_data if csv_data else {}

            if path_obj.is_dir():
                files: TypingList[Path] = list(path_obj.glob('*.json'))
                return [j_loads(file, ordered=ordered) for file in files]

            if path_obj.is_file():
                try:
                    return json.loads(path_obj.read_text(encoding='utf-8'))
                except Exception as ex:
                    logger.error(f'Ошибка чтения словаря', ex, False)
                    try:
                        with path_obj.open('r', encoding='utf-8') as f:
                            content = f.read()
                            if not content:
                                logger.error(f'В файле {path_obj} нет данных!', None, False)
                                return {}
                        repaired = _string_to_dict(content, return_objects=True)
                        return repaired
                    except Exception as ex:
                        logger.error(f'Error reading file {path_obj}', ex, False)
                        return {}
            logger.error(f'Path is not a file or directory: {path_obj}', None, False)
            return {}

        if isinstance(jjson_internal, str):
            parsed = _string_to_dict(jjson_internal)
            return _decode_strings(parsed)

        if isinstance(jjson_internal, list):
            return _decode_strings(jjson_internal)

        if isinstance(jjson_internal, dict):
            return _decode_strings(jjson_internal)

    except Exception as ex:
        logger.error(f'Error loading data from {type(jjson_internal)}', ex, exc_info=True)
        return {}

    logger.warning(f'Unhandled type for j_loads: {type(jjson_internal)}')
    return {}


def j_loads_ns(jjson: Path | SimpleNamespace | dict[Any, Any] | str | list[Any],
               ordered: bool = True) -> SimpleNamespace | TypingList[SimpleNamespace | Any] | dict[Any, Any]:
    """Загружает JSON или CSV и конвертирует результат в SimpleNamespace."""
    data = j_loads(jjson, ordered=ordered)

    if not data and isinstance(data, dict):
        return {}

    if isinstance(data, list):
        return [dict2ns(item) if isinstance(item, dict) else item for item in data]
    if isinstance(data, dict):
        return dict2ns(data)
    if isinstance(data, list):
        return []
    return {}


def sanitize_json_files(path: Path) -> bool:
    """Проверяет и исправляет JSON файлы в директории или одном файле."""
    all_ok = True

    def process_file(fp: Path) -> bool:
        logger.info(f'Start sanitize file: {fp}')
        if not fp.is_file() or fp.suffix.lower() != '.json':
            logger.error(f'Not a JSON file: {fp}')
            return False
        try:
            with fp.open('r', encoding='utf-8') as f:
                json.load(f)
            logger.info(f'Valid JSON: {fp}')
            return True
        except Exception as ex:
            logger.error(f'Error parsing JSON: {fp}', ex)
            sanitized = fp.with_name(fp.name + '.sanitized')
            try:
                fp.rename(sanitized)
                logger.info(f'Renamed to {sanitized}')
                return True
            except Exception as ex:
                logger.error(f'Failed to rename {fp}', ex)
                return False

    if not path.exists():
        logger.error(f'Path not found: {path}')
        return False

    if path.is_file():
        if not process_file(path):
            all_ok = False
    elif path.is_dir():
        for file in path.rglob('*.json'):
            if '.sanitized' in file.suffixes:
                continue
            if not process_file(file):
                all_ok = False
    else:
        logger.error(f'Invalid path: {path}')
        return False
    return all_ok


def find_keys(obj: Any,
              keys_to_find_input: TypingList[str] | str,
              found: TypingDict[str, TypingList[Any]] | None = None) -> TypingDict[str, TypingList[Any]]:
    """Рекурсивно находит все значения по указанным ключам во вложенной структуре данных."""
    if found is None:
        if isinstance(keys_to_find_input, str):
            keys_list = [keys_to_find_input]
        elif isinstance(keys_to_find_input, list) and all(isinstance(k, str) for k in keys_to_find_input):
            keys_list = keys_to_find_input
        else:
            logger.error(f"keys_to_find_input must be str or list[str], got {type(keys_to_find_input)}")
            return {}
        found = {k: [] for k in keys_list}
    else:
        keys_list = keys_to_find_input

    try:
        if isinstance(obj, Mapping):
            for k, v in obj.items():
                k_str = str(k)
                if k_str in keys_list:
                    if isinstance(v, (list, tuple)):
                        found[k_str].extend(v)
                    else:
                        found[k_str].append(v)
                find_keys(v, keys_list, found)
        elif isinstance(obj, Sequence) and not isinstance(obj, (str, bytes)):
            for i in obj:
                find_keys(i, keys_list, found)
    except Exception as ex:
        logger.error('Error in find_keys', ex, exc_info=True)
    return found
