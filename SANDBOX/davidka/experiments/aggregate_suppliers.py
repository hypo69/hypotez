## \file /sandbox/davidka/aggregate_suppliers.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль анализирует JSON файлы с данными веб-страниц, извлекает информацию
и агрегирует её по поставщикам (доменам) в отдельные JSON файлы.
Каждый JSON файл поставщика сохраняется в поддиректории с именем поставщика.
===========================================================================
Скрипт читает JSON файлы из `Config.input_dirs`. Каждый такой файл может
содержать словарь, где ключи - это URL-адреса, а значения - словари с данными
страниц. Скрипт обрабатывает каждую такую URL-запись индивидуально,
определяет поставщика на основе URL-ключа, извлекает текст и внутренние ссылки.
Для каждой успешно обработанной записи, скрипт немедленно обновляет или
создает соответствующий JSON файл поставщика. Файл поставщика
`supplier_name.json` сохраняется в директории `Config.output_dir / supplier_name /`.
Существующие файлы поставщиков дополняются новыми данными по мере их поступления.

```rst
 .. module:: sandbox.davidka.aggregate_suppliers
```
"""

from pathlib import Path
from types import SimpleNamespace
from typing import Optional, Dict, Any, List, Tuple
import threading
import time

# Стандартные импорты проекта
import header
from header import __root__
from src import gs
from src.utils.jjson import j_loads, j_loads_ns, j_dumps, sanitize_json_files
from src.utils.file import recursively_yield_file_path
from src.utils.url import get_domain, normalize_url, extract_pure_domain, COMMON_NON_HTML_EXTENSIONS
from src.logger import logger
# from src.utils.printer import pprint as print


class Config:
    """Класс конфигурации скрипта."""
    ENDPOINT: Path = __root__ / 'SANDBOX' / 'davidka'
    _config_ns: SimpleNamespace = j_loads_ns(ENDPOINT / 'davidka.json') # Используем приватное имя во избежание конфликта имен
    STORAGE: Path = Path(_config_ns.storage)
    input_dirs: list[Path] = [Path(STORAGE / 'search_results')]
    output_dir: Path = Path(STORAGE / 'data_by_supplier_set_2')
    need_sanitize_json_files: bool = getattr(_config_ns, 'need_sanitize_json_files', False)


_locks: Dict[Path, threading.Lock] = {}
_lock_guard = threading.Lock()

def _get_lock(file_path: Path) -> threading.Lock:
    """
    Возвращает или создает объект блокировки для указанного пути файла.

    Args:
        file_path (Path): Путь к файлу.

    Returns:
        threading.Lock: Объект блокировки для данного файла.
    """
    with _lock_guard:
        if file_path not in _locks:
            _locks[file_path] = threading.Lock()
        return _locks[file_path]


# ==============================================================================
# Вспомогательные функции для извлечения данных
# ==============================================================================
def _extract_fields_from_source(data_source: Dict[str, Any], file_path_context: Path) -> Dict[str, Any]:
    """
    Извлекает указанные поля ('category_name', 'title', 'description',
    'original_internal_url', 'text', 'internal_links') из data_source.
    Обрабатывает 'internal_links' для приведения к ожидаемому формату.

    Args:
        data_source (Dict[str, Any]): Словарь (подраздел исходных данных), из которого выполняется извлечение.
        file_path_context (Path): Путь к исходному JSON-файлу (для логирования).

    Returns:
        Dict[str, Any]: Словарь с извлеченными полями.
    """
    category_name_val: Optional[str] = data_source.get('category_name')
    title_val: Optional[str] = data_source.get('title')
    description_val: Optional[str] = data_source.get('description')
    original_internal_url_val: Optional[str] = data_source.get('original_internal_url')

    page_data_text_raw_val: Any = data_source.get('text')
    page_text_val: str = ''
    if isinstance(page_data_text_raw_val, str):
        page_text_val = page_data_text_raw_val
    elif page_data_text_raw_val is not None:
        logger.warning(f"Ключ 'text' в источнике данных ({file_path_context}) не является строкой ({type(page_data_text_raw_val)}). Используется пустая строка ''.")

    processed_internal_links_list: List[Dict[str, Any]] = []
    raw_internal_links_val: Any = data_source.get('internal_links')

    if isinstance(raw_internal_links_val, list):
        link_item_val: Any
        for link_item_val in raw_internal_links_val:
            if isinstance(link_item_val, str):
                normalized_url_str: Optional[str] = normalize_url(link_item_val, excluded_extensions=COMMON_NON_HTML_EXTENSIONS)
                if normalized_url_str:
                     processed_internal_links_list.append({'link': {'href': normalized_url_str}})
                else:
                    logger.warning(f"Невалидная внутренняя ссылка-строка '{link_item_val}' в {file_path_context} пропущена после нормализации.")
            elif isinstance(link_item_val, dict):
                processed_internal_links_list.append(link_item_val)
            else:
                logger.warning(f"Элемент в 'internal_links' не является строкой или словарем ({type(link_item_val)}) в {file_path_context}. Пропущен.")
    elif raw_internal_links_val is not None:
        logger.warning(f"Ключ 'internal_links' в источнике данных ({file_path_context}) не является списком ({type(raw_internal_links_val)}). Используется пустой список [].")

    return {
        'category_name': category_name_val,
        'title': title_val,
        'description': description_val,
        'original_internal_url': original_internal_url_val,
        'page_text': page_text_val,
        'internal_links_processed': processed_internal_links_list,
    }

def extract_structured_data_for_entry(
    url_key_param: str,
    data_for_url_key: Dict[str, Any],
    file_path_context: Path
) -> Optional[Tuple[str, str, Dict[str, Any]]]:
    """
    Извлекает данные для одной записи (определяемой url_key_param и data_for_url_key),
    определяет поставщика и формирует структуру для сохранения.

    Args:
        url_key_param (str): Нормализованный URL, который является ключом для этой записи.
        data_for_url_key (Dict[str, Any]): Словарь с данными, соответствующий этому URL-ключу.
        file_path_context (Path): Путь к исходному JSON файлу (для логирования контекста).

    Returns:
        Optional[Tuple[str, str, Dict[str, Any]]]:
            Кортеж (supplier_name, url_key_param, data_to_store) или None при ошибке.
    """
    main_link_val: str = url_key_param
    url_for_domain_val: str = url_key_param
    supplier_name: Optional[str] = None
    extracted_content_dict: Dict[str, Any]
    data_to_store_dict: Dict[str, Any]
    actual_content_source_dict: Dict[str, Any]

    try:
        supplier_name = get_domain(url_for_domain_val)
    except Exception as ex:
        logger.error(f"Ошибка при вызове get_domain для URL '{url_for_domain_val}' (ключ из {file_path_context}): {ex}", ex, exc_info=True)
        return None
    if not supplier_name:
        logger.error(f"Функция get_domain не вернула домен для URL '{url_for_domain_val}' (ключ из {file_path_context}). Пропуск записи.")
        return None

    actual_content_source_dict = data_for_url_key
    potential_nested_data: Any = data_for_url_key.get('data')
    if isinstance(potential_nested_data, dict):
        actual_content_source_dict = potential_nested_data
        logger.debug(f"Использование вложенного словаря 'data' как источника контента для ключа {main_link_val} из файла {file_path_context}.")

    extracted_content_dict = _extract_fields_from_source(actual_content_source_dict, file_path_context)

    data_to_store_dict = {
        'category_name': extracted_content_dict.get('category_name'),
        'title': extracted_content_dict.get('title'),
        'description': extracted_content_dict.get('description'),
        'original_internal_url': extracted_content_dict.get('original_internal_url'),
        'internal_links': extracted_content_dict.get('internal_links_processed') or [{'link':'root','href':fr'https://{supplier_name}'}],
    }

    logger.info(f"Данные для поставщика '{supplier_name}' извлечены для ключа {main_link_val} (из файла {file_path_context})")
    return supplier_name, main_link_val, data_to_store_dict


# ==============================================================================
# Вспомогательные функции для update_supplier_file
# ==============================================================================
def _prepare_supplier_file_path_and_dir(supplier_name: str, base_output_dir_path: Path) -> Optional[Path]:
    """
    Создает директорию для поставщика (если не существует) и возвращает полный путь к файлу поставщика.

    Args:
        supplier_name (str): Имя поставщика (домен).
        base_output_dir_path (Path): Базовая директория для всех поставщиков.

    Returns:
        Optional[Path]: Путь к файлу поставщика или None в случае ошибки создания директории.
    """
    if not supplier_name:
        logger.error("Попытка подготовки пути файла с пустым именем поставщика.")
        return None

    supplier_specific_dir_path: Path = base_output_dir_path / supplier_name
    try:
        supplier_specific_dir_path.mkdir(parents=True, exist_ok=True)
    except OSError as ex:
        logger.error(f"Не удалось создать директорию для поставщика '{supplier_name}' в {supplier_specific_dir_path}: {ex}", ex, exc_info=True)
        return None
    return supplier_specific_dir_path / f"{supplier_name}.json"


def _add_normalized_link_to_list(
    link_item_to_add: Any,
    seen_hrefs_set: set[str],
    unique_links_output_list: List[Dict[str, Any]],
    is_from_new_links: bool
) -> int:
    """
    Нормализует href в элементе ссылки, добавляет элемент в список (если href уникален)
    и подсчитывает дубликаты из нового набора.

    Args:
        link_item_to_add (Any): Элемент ссылки для добавления (ожидается словарь).
        seen_hrefs_set (set[str]): Множество уже встреченных нормализованных href.
        unique_links_output_list (List[Dict[str, Any]]): Список для добавления уникальных ссылок.
        is_from_new_links (bool): True, если ссылка из нового набора данных (для подсчета дубликатов).

    Returns:
        int: 1, если обнаружен дубликат из нового списка ссылок, иначе 0.
    """
    item_href_normalized_val: Optional[str] = None
    item_link_data_sub_dict: Any = None
    item_href_raw_val: Any = None

    if not isinstance(link_item_to_add, dict):
        logger.warning(f"Пропуск элемента ссылки: элемент не является словарем ({type(link_item_to_add)}). Элемент: {link_item_to_add}")
        return 0

    item_link_data_sub_dict = link_item_to_add.get('link')
    if not isinstance(item_link_data_sub_dict, dict):
        if 'href' in link_item_to_add and isinstance(link_item_to_add.get('href'), str):
             item_link_data_sub_dict = link_item_to_add
        else:
            logger.warning(f"Пропуск элемента ссылки: отсутствует ключ 'link' или он не словарь ({type(item_link_data_sub_dict)}). Элемент: {link_item_to_add}")
            return 0

    item_href_raw_val = item_link_data_sub_dict.get('href')
    if not isinstance(item_href_raw_val, str):
        logger.warning(f"Пропуск элемента ссылки: 'href' отсутствует или не является строкой ({type(item_href_raw_val)}). Элемент: {link_item_to_add}")
        return 0

    item_href_normalized_val = normalize_url(item_href_raw_val, excluded_extensions=COMMON_NON_HTML_EXTENSIONS)
    if not item_href_normalized_val:
        logger.warning(f"Пропуск элемента ссылки: 'href' ('{item_href_raw_val}') стал невалидным после нормализации. Элемент: {link_item_to_add}")
        return 0

    if item_href_normalized_val not in seen_hrefs_set:
        seen_hrefs_set.add(item_href_normalized_val)
        updated_link_item_dict: Dict[str,Any] = link_item_to_add.copy()
        if 'link' in updated_link_item_dict and isinstance(updated_link_item_dict['link'], dict):
            updated_link_item_dict['link'] = updated_link_item_dict['link'].copy()
            updated_link_item_dict['link']['href'] = item_href_normalized_val
        elif 'href' in updated_link_item_dict:
            updated_link_item_dict['href'] = item_href_normalized_val
        else:
             logger.error(f"Критическая ошибка в _add_normalized_link_to_list: неожиданная структура элемента {updated_link_item_dict} после проверок.")
             return 0 # Ошибка, не добавляем
        unique_links_output_list.append(updated_link_item_dict)
    elif is_from_new_links:
        return 1
    return 0


def _perform_link_deduplication(
    old_links_raw_data: Any,
    new_links_raw_data: Any,
    supplier_name_ref: str,
    url_key_ref: str
) -> List[Dict[str, Any]]:
    """
    Выполняет дедупликацию ссылок, объединяя старые и новые, отдавая приоритет старым.

    Args:
        old_links_raw_data (Any): "Сырые" старые ссылки (из существующего файла).
        new_links_raw_data (Any): "Сырые" новые ссылки (из текущей обработки, ожидается List[Dict]).
        supplier_name_ref (str): Имя поставщика (для логирования).
        url_key_ref (str): URL-ключ (для логирования).

    Returns:
        List[Dict[str, Any]]: Список уникальных, нормализованных ссылок.
    """
    old_links_list_val: List[Dict[str, Any]] = []
    new_links_list_val: List[Dict[str, Any]] = []
    seen_hrefs_collection: set[str] = set()
    unique_links_result_list: List[Dict[str, Any]] = []
    duplicates_found_counter: int = 0

    if isinstance(old_links_raw_data, list):
        old_links_list_val = [item for item in old_links_raw_data if isinstance(item, dict)]
        if len(old_links_list_val) != len(old_links_raw_data):
            logger.warning(f"Некоторые элементы в old_links_raw_data для '{url_key_ref}' у '{supplier_name_ref}' не являются словарями и были проигнорированы.")
    elif old_links_raw_data is not None:
        logger.warning(f"Существующий ключ '{url_key_ref}' у '{supplier_name_ref}' содержит 'internal_links', но это не список ({type(old_links_raw_data)}). Старые ссылки игнорируются.")

    if isinstance(new_links_raw_data, list):
        new_links_list_val = [item for item in new_links_raw_data if isinstance(item, dict)]
        if len(new_links_list_val) != len(new_links_raw_data):
             logger.warning(f"Некоторые элементы в new_links_raw_data для '{url_key_ref}' у '{supplier_name_ref}' не являются словарями и были проигнорированы.")
    elif new_links_raw_data is not None:
        logger.warning(f"Новые 'internal_links' для '{url_key_ref}' у '{supplier_name_ref}' не являются списком ({type(new_links_raw_data)}). Новые ссылки игнорируются.")

    link_item_val: Dict[str,Any]
    logger.debug(f"Дедупликация: обработка {len(old_links_list_val)} старых ссылок для '{url_key_ref}' у '{supplier_name_ref}'.")
    for link_item_val in old_links_list_val:
        _add_normalized_link_to_list(link_item_val, seen_hrefs_collection, unique_links_result_list, is_from_new_links=False)

    logger.debug(f"Дедупликация: обработка {len(new_links_list_val)} новых ссылок для '{url_key_ref}' у '{supplier_name_ref}'.")
    for link_item_val in new_links_list_val:
        duplicates_found_counter += _add_normalized_link_to_list(link_item_val, seen_hrefs_collection, unique_links_result_list, is_from_new_links=True)

    if duplicates_found_counter > 0:
        logger.info(f"Удалено {duplicates_found_counter} дублирующихся ссылок (по нормализованному href) при обновлении ключа '{url_key_ref}' для поставщика '{supplier_name_ref}'.")
    logger.debug(f"Итоговый размер дедуплицированного списка 'internal_links' для '{url_key_ref}' у '{supplier_name_ref}': {len(unique_links_result_list)}")

    return unique_links_result_list


def update_supplier_file(
    supplier_name: str,
    url_key_val: str,
    data_to_store_val: Dict[str, Any],
    base_output_dir_path: Path
) -> bool:
    """
    Обновляет (или создает) JSON файл для поставщика в его собственной поддиректории.
    Добавляет/перезаписывает данные для URL-ключа и удаляет дубликаты в 'internal_links'.

    Args:
        supplier_name (str): Имя поставщика (домен).
        url_key_val (str): URL, используемый как ключ в JSON файле.
        data_to_store_val (Dict[str, Any]): Словарь новых данных для сохранения.
        base_output_dir_path (Path): Базовая директория, где будут создаваться поддиректории поставщиков.

    Returns:
        bool: True в случае успеха, False в случае ошибки.
    """
    supplier_file_path_val: Optional[Path]
    file_access_lock: threading.Lock
    existing_supplier_data: Dict[str, Any]
    unique_deduplicated_links_list: List[Dict[str, Any]]
    current_entry_for_url_key: Dict[str, Any]

    supplier_file_path_val = _prepare_supplier_file_path_and_dir(supplier_name, base_output_dir_path)
    if not supplier_file_path_val:
        return False

    file_access_lock = _get_lock(supplier_file_path_val)
    logger.debug(f"Попытка обновления файла {supplier_file_path_val} для ключа {url_key_val}...")

    with file_access_lock:
        existing_supplier_data = {}
        if supplier_file_path_val.exists():
            loaded_data_val: Optional[Dict[str, Any] | List[Any]] = j_loads(supplier_file_path_val)
            if isinstance(loaded_data_val, dict):
                existing_supplier_data = loaded_data_val
                logger.debug(f"Файл {supplier_file_path_val} успешно прочитан.")
            else:
                logger.warning(f"Данные из {supplier_file_path_val} не являются словарем (получено: {type(loaded_data_val)}) или файл пуст/поврежден. Начинаем с пустого словаря.")
                existing_supplier_data = {}

        old_links_raw_val: Any = None
        if url_key_val in existing_supplier_data:
            old_entry_val: Any = existing_supplier_data.get(url_key_val)
            if isinstance(old_entry_val, dict):
                old_links_raw_val = old_entry_val.get('internal_links')
            elif old_entry_val is not None:
                 logger.warning(f"Существующий ключ '{url_key_val}' в {supplier_file_path_val} не является словарем ({type(old_entry_val)}). Старые ссылки игнорируются.")

        new_links_raw_val: Any = data_to_store_val.get('internal_links')

        unique_deduplicated_links_list = _perform_link_deduplication(
            old_links_raw_val, new_links_raw_val, supplier_name, url_key_val
        )

        logger.debug(f"Обновление/добавление ключа '{url_key_val}' в данных для {supplier_name}...")
        if not isinstance(data_to_store_val, dict):
             logger.error(f"Критическая ошибка: data_to_store_val не является словарем ({type(data_to_store_val)}) для {supplier_name}, {url_key_val}. Запись не будет произведена.")
             return False

        current_entry_for_url_key = existing_supplier_data.get(url_key_val, {})
        if not isinstance(current_entry_for_url_key, dict):
            logger.warning(f"Данные под ключом '{url_key_val}' в {supplier_file_path_val} не являются словарем ({type(current_entry_for_url_key)}). Будут перезаписаны.")
            current_entry_for_url_key = {}

        current_entry_for_url_key.update(data_to_store_val)
        current_entry_for_url_key['internal_links'] = unique_deduplicated_links_list or {'link':data_to_store_val['internal_links']}
        existing_supplier_data[url_key_val] = current_entry_for_url_key

        logger.debug(f"Запись итоговых данных в {supplier_file_path_val}...")
        if j_dumps(existing_supplier_data, supplier_file_path_val):
            logger.info(f"Файл {supplier_file_path_val} успешно обновлен для ключа '{url_key_val}'.")
            return True
        else:
             logger.error(f"Функция j_dumps сообщила об ошибке при записи файла {supplier_file_path_val} (ключ: {url_key_val}).")
             return False
    # Эта точка не должна быть достигнута, если with блок всегда возвращает значение.
    logger.error(f"Выход из функции update_supplier_file для {supplier_file_path_val} (ключ: {url_key_val}) произошел неожиданно без явного return из блока 'with'.")
    return False


# ==============================================================================
# Функции основного блока выполнения
# ==============================================================================
def _process_file_entry(
    file_path_to_process: Path,
    base_output_dir_ref: Path,
    processing_stats: Dict[str, int]
) -> None:
    """
    Обрабатывает один входной JSON-файл. Файл может содержать словарь URL-ключей.
    Для каждого URL-ключа извлекаются данные и обновляется/создается файл поставщика.
    Обновляет словарь статистики `processing_stats`.

    Args:
        file_path_to_process (Path): Путь к обрабатываемому JSON-файлу.
        base_output_dir_ref (Path): Базовая директория для файлов поставщиков.
        processing_stats (Dict[str, int]): Словарь для сбора статистики (изменяется по месту).
    """
    # Эта функция теперь обрабатывает один файл, который может содержать много записей.
    # total_files_scanned инкрементируется в вызывающей функции.
    logger.debug(f"Начало обработки файла: {file_path_to_process}")

    raw_content_from_file: Optional[Dict[str, Any] | List[Any]] = j_loads(file_path_to_process)

    if not isinstance(raw_content_from_file, dict):
        logger.warning(f"Пропуск файла: содержимое {file_path_to_process} не является словарем (получено: {type(raw_content_from_file)}).")
        processing_stats['error_loading_files_count'] += 1 # Считаем как ошибку загрузки файла
        return

    if not raw_content_from_file:
        logger.info(f"Файл {file_path_to_process} является пустым словарем. Пропуск.")
        # Не считаем это ошибкой, просто нет данных для обработки.
        return

    entries_in_file_count: int = 0
    for entry_key, entry_data_value in raw_content_from_file.items():
        entries_in_file_count += 1
        logger.debug(f"Обработка записи с ключом '{entry_key}' из файла {file_path_to_process}...")

        if not isinstance(entry_data_value, dict):
            logger.warning(f"Пропуск записи с ключом '{entry_key}' в файле {file_path_to_process}: значение не является словарем (тип: {type(entry_data_value)}).")
            processing_stats['error_extracting_data_count'] += 1
            continue

        normalized_url_key: Optional[str] = normalize_url(entry_key, excluded_extensions=COMMON_NON_HTML_EXTENSIONS)
        if not normalized_url_key:
            logger.warning(f"Пропуск записи с ключом '{entry_key}' в файле {file_path_to_process}: ключ не является валидным URL после нормализации.")
            processing_stats['error_extracting_data_count'] += 1
            continue

        entry_data_value['internal_links']:list = []
        entry_data_value['internal_links'].append(
                                {'link':{
                                        "href": f"https://{extract_pure_domain(entry_key)}",
                                        "text": "root" }}
                                )
        extracted_info_tuple: Optional[Tuple[str, str, Dict[str, Any]]] = None
        try:
             extracted_info_tuple = extract_structured_data_for_entry(
                url_key_param=normalized_url_key,
                data_for_url_key=entry_data_value,
                file_path_context=file_path_to_process
            )
        except Exception as ex_extract:
            logger.error(f"Непредвиденная ошибка при вызове extract_structured_data_for_entry для ключа '{normalized_url_key}' из {file_path_to_process}: {ex_extract}", ex_extract, exc_info=True)
            processing_stats['error_extracting_data_count'] += 1
            continue

        if not extracted_info_tuple:
            processing_stats['error_extracting_data_count'] += 1
            continue

        supplier_name_val: str
        returned_url_key: str
        data_for_supplier_file: Dict[str, Any]
        supplier_name_val, returned_url_key, data_for_supplier_file = extracted_info_tuple

        # returned_url_key должен совпадать с normalized_url_key
        if returned_url_key != normalized_url_key:
            logger.warning(f"Возвращенный URL-ключ '{returned_url_key}' не совпадает с ожидаемым '{normalized_url_key}' для записи из файла {file_path_to_process}. Используется ожидаемый '{normalized_url_key}'.")
            # Это может указывать на проблему, если extract_structured_data_for_entry пытается изменить url_key_param

        write_was_successful: bool = False
        try:
            write_was_successful = update_supplier_file(
                supplier_name=supplier_name_val,
                url_key_val=normalized_url_key, # Используем нормализованный ключ из файла
                data_to_store_val=data_for_supplier_file,
                base_output_dir_path=base_output_dir_ref
            )
        except Exception as ex_update:
            logger.error(f"Непредвиденная ошибка при вызове update_supplier_file для {supplier_name_val}/{normalized_url_key} (из {file_path_to_process}): {ex_update}", ex_update, exc_info=True)
            processing_stats['error_writing_files_count'] += 1
            continue

        if write_was_successful:
            processing_stats['processed_records_count'] += 1
        else:
            processing_stats['error_writing_files_count'] += 1
    logger.debug(f"Завершение обработки файла {file_path_to_process}, обработано записей: {entries_in_file_count}.")


def main_processing_loop() -> None:
    """
    Основной цикл обработки: итерирует по директориям и файлам,
    выполняет санацию (если включено) и агрегацию данных.
    Собирает и выводит статистику.
    """
    stats_accumulator: Dict[str, int] = {
        'processed_records_count': 0,       # Теперь считаем записи, а не файлы
        'error_loading_files_count': 0,     # Ошибки на уровне целого файла
        'error_extracting_data_count': 0,   # Ошибки на уровне отдельной записи
        'error_writing_files_count': 0,     # Ошибки на уровне отдельной записи
        'total_files_scanned': 0,
    }
    base_output_directory: Path = Config.output_dir
    perform_sanitize: bool = Config.need_sanitize_json_files
    input_dir_path: Path
    current_file_path: Path

    for input_dir_path in Config.input_dirs:
        logger.info(f"Обработка файлов из директории: {input_dir_path}")
        logger.info(f"Файлы поставщиков будут сохранены в поддиректории {base_output_directory}/<имя_поставщика>/")

        if perform_sanitize:
            logger.info(f"--- Запуск санации JSON файлов в {input_dir_path} ---")
            try:
                sanitize_json_files(input_dir_path)
                logger.info(f"Санация JSON файлов в {input_dir_path} успешно завершена.")
            except Exception as ex_sanitize_call:
                 logger.error(f"Ошибка во время вызова sanitize_json_files для {input_dir_path}: {ex_sanitize_call}", ex_sanitize_call, exc_info=True)
            logger.info(f"--- Санация завершена для {input_dir_path} ---")

        logger.info(f"--- Начало обработки JSON файлов из {input_dir_path} ---")
        try:
            for current_file_path in recursively_yield_file_path(input_dir_path, '*.json'):
                stats_accumulator['total_files_scanned'] += 1
                _process_file_entry(current_file_path, base_output_directory, stats_accumulator)
        except Exception as ex_main_file_iteration:
            logger.critical(f"Критическая ошибка во время итерации по файлам в {input_dir_path}: {ex_main_file_iteration}", ex_main_file_iteration, exc_info=True)
        logger.info(f"--- Обработка файлов из {input_dir_path} завершена ---")

    logger.info("========== Итоговая статистика по всем директориям ==========")
    logger.info(f" - Всего просканировано файлов: {stats_accumulator['total_files_scanned']}")
    logger.info(f" - Успешно обработано записей (записано/обновлено): {stats_accumulator['processed_records_count']}")
    logger.info(f" - Ошибок загрузки/формата файлов: {stats_accumulator['error_loading_files_count']}")
    logger.info(f" - Ошибок извлечения структурированных данных из записей: {stats_accumulator['error_extracting_data_count']}")
    logger.info(f" - Ошибок записи в файлы поставщиков: {stats_accumulator['error_writing_files_count']}")
    logger.info(f"--- Работа скрипта {Path(__file__).name} завершена ---")


# ==============================================================================
# Основной блок выполнения скрипта
# ==============================================================================
if __name__ == '__main__':
    main_processing_loop()
