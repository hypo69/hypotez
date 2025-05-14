## \file /sandbox/davidka/experiments/generate_train_data_by_page_type.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для генерации обучающих данных на основе типа страницы.
================================================================
Скрипт обрабатывает JSON-файлы, извлекает структурированную информацию
о товарах и категориях, включая метаданные, описания и другие атрибуты.
Данные извлекаются из словарей (dict), проверяя несколько возможных
мест их нахождения: на верхнем уровне или во вложенном объекте 'ai_analized_content'.
Поддерживает выбор API-ключа Gemini через аргумент командной строки.

 ```rst
 .. module:: sandbox.davidka.experiments.generate_train_data_by_page_type
 ```
"""

import sys
import argparse # Добавлено для парсинга аргументов командной строки
from pathlib import Path
from types import SimpleNamespace 
from typing import Optional, Dict, Any, List, Union 

# -------------------------------------------------------------------
import header
from header import __root__
from src import gs
from src.llm.gemini import GoogleGenerativeAi
from src.webdriver import driver
from src.webdriver.driver import Driver
from src.webdriver.firefox import Firefox
from SANDBOX.davidka.graber import extract_page_data # Предполагается, что этот путь корректен
from src.utils.file import read_text_file, recursively_yield_file_path, get_directory_names
from src.utils.url import extract_pure_domain
from src.utils.jjson import j_loads, j_dumps, j_loads_ns
from src.utils.printer import pprint as print
from src.logger.logger import logger

class Config:
    """Класс конфигурации скрипта."""
    ENDPOINT: Path = __root__ / 'SANDBOX' / 'davidka'
    config:SimpleNamespace = j_loads_ns(ENDPOINT / 'davidka.json') # Загрузка конфигурации из JSON
    actual_storage:str = 'local_storage' # 'local_storage' or 'google_drive'  <- ГДЕ НАХОДИТСЯ ХРАНИЛИЩЕ
    STORAGE:Path = Path(config.local_storage.storage) if actual_storage == 'local_storage' else Path(config.google_drive.storage)
    TRAIN_STORAGE: Path = STORAGE / 'train_data' # Папка для хранения обучающих данных
    SOURCE_DIRS:list[Path] = [STORAGE / 'data_by_supplier_ge', STORAGE/'data_by_supplier_set_1 DONT TOUCH!'] # Папка с файлами
    GEMINI_API_KEY: Optional[str] = None # Будет установлен позже из аргументов командной строки
    GEMINI_MODEL_NAME: str = 'gemini-1.5-flash-latest' # Обновлено на более актуальное имя модели
    system_instructuction: str | None = read_text_file(ENDPOINT / 'instructions/analize_html.md')
    updated_links_file_name: str = 'updated_links.json'
    DELAY_AFTER_LINK_PROCESSING: int = 15
    WINDOW_MODE: str = 'headless'

    # списки отфильтрованных данных
    product:List[Dict[str, Any]] = []
    category:List[Dict[str, Any]] = []
    about_us:List[Dict[str, Any]] = [] # <- `page_type` may be 'about_us' or 'about
    contact:List[Dict[str, Any]] = []
    manuals:List[Dict[str, Any]] = []
    article:List[Dict[str, Any]] = []
    information:List[Dict[str, Any]] = []
    home:List[Dict[str, Any]] = []
    description:List[Dict[str, Any]] = []
    distributors:List[Dict[str, Any]] = []
    service:List[Dict[str, Any]] = []
    faq:List[Dict[str, Any]] = []
    blog:List[Dict[str, Any]] = []
    unknown:List[Dict[str, Any]] = []
    error:List[Dict[str, Any]] = []



# ---------------------------------- Вспомогательные функции извлечения данных ---------------------------

def _get_string_attribute_from_dict_or_ai_content(value_dict: Dict[str, Any], attribute_name: str) -> str:
    """
    Извлекает строковый атрибут из словаря, проверяя верхний уровень,
    а затем вложенный 'ai_analized_content'. Атрибут конвертируется в строку.

    Args:
        value_dict (Dict[str, Any]): Входной словарь.
        attribute_name (str): Имя извлекаемого атрибута.

    Returns:
        str: Значение атрибута в виде строки или пустая строка, если не найдено,
             None, или значение пусто после конвертации и очистки.
    """
    final_value_str: str = ''
    top_level_value: Optional[Any] = None
    current_value_str: str = ''
    ai_content_dict: Optional[Dict[str, Any]] = None
    nested_value: Optional[Any] = None
    current_nested_value_str: str = ''

    if not isinstance(value_dict, dict):
        logger.warning(f"Функция _get_string_attribute_from_dict_or_ai_content: ожидался dict для '{attribute_name}', получен {type(value_dict)}")
        return ''

    top_level_value = value_dict.get(attribute_name)

    if top_level_value is not None:
        if isinstance(top_level_value, str):
            current_value_str = top_level_value.strip()
        else:
            try:
                current_value_str = str(top_level_value).strip()
            except Exception as ex:
                logger.debug(f"Функция _get_string_attribute_from_dict_or_ai_content: ошибка конвертации в строку для '{attribute_name}' (верхний уровень): {top_level_value}", ex)
                current_value_str = ''

    if current_value_str:
        final_value_str = current_value_str

    if not final_value_str:
        ai_content_dict_val = value_dict.get('ai_analized_content') # Используем другую переменную, чтобы не конфликтовать с именем параметра
        if isinstance(ai_content_dict_val, dict):
            nested_value = ai_content_dict_val.get(attribute_name)

            if nested_value is not None:
                if isinstance(nested_value, str):
                    current_nested_value_str = nested_value.strip()
                else:
                    try:
                        current_nested_value_str = str(nested_value).strip()
                    except Exception as ex:
                        logger.debug(f"Функция _get_string_attribute_from_dict_or_ai_content: ошибка конвертации в строку для '{attribute_name}' (ai_analized_content): {nested_value}", ex)
                        current_nested_value_str = ''

            if current_nested_value_str:
                final_value_str = current_nested_value_str

    return final_value_str

def _get_optional_attribute_as_str_dict_or_ai(value_dict: Dict[str, Any], attribute_name: str) -> Optional[str]:
    """
    Извлекает атрибут из словаря (верхний уровень или ai_analized_content),
    конвертирует в строку (если не None и не пустая строка после strip). Возвращает Optional[str].
    """
    val_found: Optional[Any] = None
    # ai_content_dict: Optional[Dict[str, Any]] = None # Не используется в этой версии
    str_val: str = ''

    if not isinstance(value_dict, dict):
        logger.warning(f"Функция _get_optional_attribute_as_str_dict_or_ai: ожидался dict для '{attribute_name}', получен {type(value_dict)}")
        return None

    val_found = value_dict.get(attribute_name)

    if val_found is None:
        ai_content_val = value_dict.get('ai_analized_content')
        if isinstance(ai_content_val, dict):
            val_found = ai_content_val.get(attribute_name)

    if val_found is not None:
        try:
            str_val = str(val_found).strip()
            return str_val if str_val else None
        except Exception as ex:
            logger.debug(f"Функция _get_optional_attribute_as_str_dict_or_ai: ошибка конвертации в строку для '{attribute_name}': {val_found}", ex)
            return None
    return None


def get_meta_keywords_str(value_dict: Dict[str, Any]) -> str:
    """
    Извлекает 'meta_keywords', проверяя value_dict и value_dict.get('ai_analized_content').
    Если значение является списком, объединяет его элементы в строку через ', '.
    Если строка, возвращает ее (очищенную). Иначе пустую строку.
    """
    keywords_result_str: str = ''
    raw_keywords: Optional[Any] = None
    # raw_keywords_top: Optional[Any] = None # Не используется
    # ai_content_dict: Optional[Dict[str, Any]] = None # Не используется
    # raw_keywords_nested: Optional[Any] = None # Не используется
    processed_keywords: List[str] = []

    if not isinstance(value_dict, dict):
        logger.warning(f"Функция get_meta_keywords_str: ожидался dict, получен {type(value_dict)}")
        return ''

    raw_keywords = value_dict.get('meta_keywords')
    if raw_keywords is None:
        ai_content_val = value_dict.get('ai_analized_content')
        if isinstance(ai_content_val, dict):
            raw_keywords = ai_content_val.get('meta_keywords')

    if raw_keywords is not None:
        if isinstance(raw_keywords, list):
            processed_keywords = [str(kw).strip() for kw in raw_keywords if kw is not None and str(kw).strip()]
            if processed_keywords:
                keywords_result_str = ', '.join(processed_keywords)
        elif isinstance(raw_keywords, str):
            keywords_result_str = raw_keywords.strip()
        else:
            try:
                keywords_result_str = str(raw_keywords).strip()
            except Exception as ex:
                logger.debug(f"Функция get_meta_keywords_str: ошибка конвертации в строку: {raw_keywords}", ex)
                keywords_result_str = ''
    return keywords_result_str

# ---------------------------------- Функции-геттеры для полей ------------------------------------

def get_page_type(value_dict: Dict[str, Any]) -> Optional[str]:
    """
    Извлекает значение 'page_type' из словаря,
    проверяя верхний уровень, а затем вложенный 'ai_analized_content'.
    """
    page_type_val: Optional[Any] = None
    # ai_content_dict: Optional[Dict[str, Any]] = None # Не используется
    page_type_nested: Optional[Any] = None

    if not isinstance(value_dict, dict):
        logger.warning(f"Функция get_page_type: ожидался dict, получен {type(value_dict)}")
        return None

    page_type_val = value_dict.get('page_type')
    if page_type_val is not None:
        return str(page_type_val)

    ai_content_val = value_dict.get('ai_analized_content')
    if isinstance(ai_content_val, dict):
        page_type_nested = ai_content_val.get('page_type')
        if page_type_nested is not None:
            return str(page_type_nested)
    return None

def get_product_title(value_dict: Dict[str, Any]) -> str:
    """Функция извлекает 'product_title', используя общую логику."""
    return _get_string_attribute_from_dict_or_ai_content(value_dict, 'product_title')

def get_meta_og_title(value_dict: Dict[str, Any]) -> str:
    """Функция извлекает 'meta_og_title', используя общую логику."""
    return _get_string_attribute_from_dict_or_ai_content(value_dict, 'meta_og_title')

def get_meta_name_title(value_dict: Dict[str, Any]) -> str:
    """Функция извлекает 'meta_name_title', используя общую логику."""
    return _get_string_attribute_from_dict_or_ai_content(value_dict, 'meta_name_title')

def get_meta_description(value_dict: Dict[str, Any]) -> str:
    """Функция извлекает 'meta_description', используя общую логику."""
    return _get_string_attribute_from_dict_or_ai_content(value_dict, 'meta_description')

def get_title_tag_content(value_dict: Dict[str, Any]) -> str:
    """Функция извлекает 'title_tag_content', используя общую логику."""
    return _get_string_attribute_from_dict_or_ai_content(value_dict, 'title_tag_content')

def get_specification(value_dict: Dict[str, Any]) -> str:
    """Функция извлекает 'specification', используя общую логику."""
    return _get_string_attribute_from_dict_or_ai_content(value_dict, 'specification')

def get_sku(value_dict: Dict[str, Any]) -> str:
    """Функция извлекает 'sku', используя общую логику."""
    return _get_string_attribute_from_dict_or_ai_content(value_dict, 'sku')

def get_price(value_dict: Dict[str, Any]) -> str:
    """Функция извлекает 'price', используя общую логику."""
    return _get_string_attribute_from_dict_or_ai_content(value_dict, 'price')

def get_summary(value_dict: Dict[str, Any]) -> str:
    """Функция извлекает 'summary', используя общую логику."""
    return _get_string_attribute_from_dict_or_ai_content(value_dict, 'summary')

def get_description(value_dict: Dict[str, Any]) -> str:
    """Функция извлекает 'description', используя общую логику."""
    return _get_string_attribute_from_dict_or_ai_content(value_dict, 'description')

def get_ai_content_object(value_dict: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Функция извлекает объект 'ai_analized_content' из словаря,
    если он существует и является словарем.
    """
    ai_content_obj: Optional[Any] = None
    if not isinstance(value_dict, dict):
        logger.warning(f"Функция get_ai_content_object: ожидался dict, получен {type(value_dict)}")
        return None

    ai_content_obj = value_dict.get('ai_analized_content')
    if isinstance(ai_content_obj, dict):
        return ai_content_obj
    elif ai_content_obj is not None:
        logger.debug(f"Функция get_ai_content_object: ключ 'ai_analized_content' найден, но значение не является dict (тип: {type(ai_content_obj)})")
    return None

def get_category(value_dict: Dict[str, Any]) -> str:
    """
    Функция извлекает категорию, проверяя ключи 'category', а затем 'category_name'.
    """
    category_val: str = ''
    category_val = _get_string_attribute_from_dict_or_ai_content(value_dict, 'category')
    if category_val:
        return category_val
    category_val = _get_string_attribute_from_dict_or_ai_content(value_dict, 'category_name')
    return category_val

def get_parent_category(value_dict: Dict[str, Any]) -> str:
    """Функция извлекает 'parent_category', используя общую логику."""
    return _get_string_attribute_from_dict_or_ai_content(value_dict, 'parent_category')

def get_featured_products(value_dict: Dict[str, Any]) -> str:
    """Функция извлекает 'featured_products', используя общую логику."""
    return _get_string_attribute_from_dict_or_ai_content(value_dict, 'featured_products')

# ---------------------------------- Основная логика ------------------------------------
def _create_page_data_object(value_dict: Dict[str, Any], page_type_str: Optional[str], original_url: str) -> Dict[str, Any]:
    """
    Создает стандартизированный словарь с данными страницы.
    """
    processed_page_type_str: str = page_type_str if page_type_str is not None else ''
    supplier_domain = extract_pure_domain(original_url) or "unknown_supplier"

    return {
        'html': value_dict.get('html', ''),
        'text': value_dict.get('text', ''),
        'title': get_product_title(value_dict),
        'meta_og_title': get_meta_og_title(value_dict),
        'meta_name_title': get_meta_name_title(value_dict),
        'meta_keywords': get_meta_keywords_str(value_dict),
        'meta_description': get_meta_description(value_dict),
        'title_tag_content': get_title_tag_content(value_dict),
        'supplier': supplier_domain,
        'price': get_price(value_dict),
        'specification': get_specification(value_dict),
        'sku': get_sku(value_dict),
        'summary': get_summary(value_dict),
        'description': get_description(value_dict),
        'page_type': processed_page_type_str,
        'ai_analized_content': get_ai_content_object(value_dict), # Может быть dict или None
        'category': get_category(value_dict),
        'parent_category': get_parent_category(value_dict),
        #'featured_products': get_featured_products(value_dict), # Закомментировано в исходном коде
        'original_internal_url': original_url,
    }

def generate_train_data(source_dirs: Optional[list[str, Path] | str | Path] = None) -> bool:
    """
    Загружает JSON-файлы и сохраняет соответствующие секции в TRAIN_STORAGE.

    Если вложенный ключ (секция) не входит в список известных — сохраняет в 'unknown'.
    Данные сохраняются порционно: как только накопится 200 записей в категории — они сбрасываются в файл.
    """

    known_sections = {
        "product", "category", "about_us", "contact", "manuals", "about",
        "article", "information", "home", "description",
        "distributors", "service", "faq", "blog", "error","error page"
    }

    buffer: dict[str, list] = {section: [] for section in known_sections}
    buffer["unknown"] = []

    chunk_counters: dict[str, int] = {section: 0 for section in buffer}
    timestamp: str = gs.now

    def flush(section: str):
        """Сохраняет текущий буфер категории и очищает его."""
        nonlocal buffer, chunk_counters, timestamp

        if not buffer[section]:
            return

        out_path = Config.TRAIN_STORAGE / section / f'{timestamp}_{chunk_counters[section]}.json'
        if not j_dumps(buffer[section], out_path):
            logger.error(f"Ошибка сохранения чанка {chunk_counters[section]} секции {section}", None, True)
        logger.success(f'Успешно сохранен {out_path}')
        chunk_counters[section] += 1
        buffer[section].clear()

    source_dirs: list = (
        source_dirs if isinstance(source_dirs, list)
        else [source_dirs] if source_dirs
        else Config.SOURCE_DIRS if isinstance(Config.SOURCE_DIRS, list)
        else [Config.SOURCE_DIRS]
    )

    for _d in source_dirs:
        suppliers_dirs: list = get_directory_names(_d)
        for supplier_dir in suppliers_dirs:
            for _file in recursively_yield_file_path(_d / supplier_dir, ['*.json']):

                data_from_input_file: Optional[Dict[str, Any]] = j_loads(_file)

                if not data_from_input_file:
                    logger.warning(f'generate_train_data: Нет данных или не удалось загрузить: {_file}.\nБудет изменен суффикс на `.sanitized`')
                    try:
                        sanitized_path = _file.with_suffix(_file.suffix + '.sanitized')
                        sanitized_path.write_text(_file.read_text(encoding='utf-8'), encoding='utf-8')
                        _file.unlink()
                    except Exception as ex:
                        logger.error(f'Не удалось сохранить и переименовать файл {_file} → {sanitized_path}', ex)
                    continue

                for url, section_dict in data_from_input_file.items():
                    if not isinstance(section_dict, dict):
                        logger.warning(f'generate_train_data: Данные по ключу {url} не являются dict в {_file}')
                        continue

                    page_type = section_dict.get("page_type") or "unknown"

                    folder = page_type if page_type in known_sections else "unknown"
                    buffer[folder].append({url:section_dict})

                    if len(buffer[folder]) >= 200:
                        flush(folder)

    # Сохраняем остатки
    for section in buffer:
        flush(section)

    return True


# def process_files_and_generate_data(driver:Driver, model:GoogleGenerativeAi):
#     """
#     Основная функция для обработки файлов и генерации структурированных данных.
#     """

#     current_timestamp: str = gs.now
#     file_counter: int = 0

#     # Список префиксов файлов, которые нужно пропускать
#     skip_prefixes = (
#         'processed_internal_links', 'updated_links',
#     )
#     source_dirs:list = 
#     for path in recursively_yield_file_path(Config.STORAGE, ['*.json']):
#         if any(path.stem.startswith(prefix) for prefix in skip_prefixes):
#             logger.info(f'Пропуск служебного или уже обработанного файла: {path}')
#             continue

#         # ------------------------ Обновление словаря товаров ------------------------
#         file_counter += 1
#         if file_counter > 0 and file_counter % 300 == 0: # Обновляем временную метку каждые 300 файлов (после первого блока)
#             current_timestamp = gs.now
        
#         generate_train_data(path, current_timestamp)
        
#         # Важно: Если этот `continue` активен, то код ниже (классификация LLM и сохранение по типам)
#         # НЕ БУДЕТ выполнен для этого файла. 
#         # Если вам нужна и генерация `train_products_...` и последующая классификация/сохранение
#         # по типам для каждого файла, ЗАКОММЕНТИРУЙТЕ или УДАЛИТЕ строку `continue` ниже.
#         continue # Закомментируйте эту строку, если нужна полная обработка каждого файла

#         # ------------------------------------------------------------------------
#         # Следующий блок кода (определение типов через LLM и сохранение по типам)
#         # будет выполнен, только если `continue` выше закомментирован или удален.
#         # ------------------------------------------------------------------------

#         data_from_input_file: Optional[Dict[str, Any]] = j_loads(path)
#         if not data_from_input_file:
#             logger.warning(f'Нет данных или не удалось загрузить для основной обработки: {path}')
#             continue

#         path_to_target_dir: Optional[Path] = None
#         anchor_directory_name: str = 'data_by_supplier'
#         try:
#             path_parts: List[str] = list(path.parts) # Преобразуем в list для .index
#             anchor_index: int = path_parts.index(anchor_directory_name)
#             if anchor_index + 1 < len(path_parts):
#                 path_to_target_dir = Path(*path_parts[:anchor_index + 2])
#                 path_to_target_dir.mkdir(parents=True, exist_ok=True) # Убедимся, что директория существует
#             else:
#                 logger.error(f'Не удалось определить структуру целевой директории из частей пути: {path.parts} для файла {path}')
#                 continue
#         except ValueError:
#             logger.warning(f"Анкерная директория '{anchor_directory_name}' не найдена в пути: {path.parts} для файла {path}")
#             # Если анкерной директории нет, можно сохранять в Config.STORAGE или другую дефолтную директорию
#             path_to_target_dir = Config.STORAGE / "categorized_data_default" / path.parent.name # Добавим имя родительской директории файла
#             path_to_target_dir.mkdir(parents=True, exist_ok=True)
#             logger.info(f"Данные для {path.name} будут сохранены в дефолтную директорию: {path_to_target_dir}")
#             # continue # или continue, если это критично
#         except Exception as ex:
#             logger.error(f"Неожиданная ошибка при определении целевой директории для {path}: {ex}", ex, exc_info=True)
#             continue


#         collections: Dict[str, Dict[str, Any]] = {
#             "products": {}, "categories": {}, "about": {},
#             "home": {}, "service": {}, "careers": {}, "other_types": {}
#         }

#         items_to_update_status_in_source_file : Dict[str, Dict[str, Any]] = {}

#         for key_url, value_data_item in data_from_input_file.items():
#             value_dict: Optional[Dict[str, Any]] = None
#             if isinstance(value_data_item, dict):
#                 value_dict = value_data_item
#             elif isinstance(value_data_item, str):
#                 try:
#                     parsed_str_data = j_loads(value_data_item)
#                     if isinstance(parsed_str_data, dict):
#                         value_dict = parsed_str_data
#                         # data_from_input_file[key_url] = value_dict # Обновляем в исходном словаре, если нужно перезаписывать исходный файл
#                     else:
#                         logger.warning(f"Данные для ключа '{key_url}' в '{path.name}' (строка) не распарсились в dict: '{value_data_item[:100]}...'")
#                 except Exception as e:
#                     logger.warning(f"Ошибка парсинга JSON-строки для ключа '{key_url}' в '{path.name}': {e}. Строка: '{value_data_item[:100]}...'")
#             else:
#                 logger.warning(f"Неожиданный тип данных для '{key_url}' в '{path.name}': {type(value_data_item)}. Ожидался dict или JSON-строка.")

#             if not value_dict:
#                 logger.warning(f"Пропуск элемента для ключа '{key_url}' в '{path.name}' из-за проблем с данными или форматом.")
#                 continue

#             original_page_type: Optional[str] = get_page_type(value_dict) # Сохраняем исходный тип
#             current_page_type: Optional[str] = original_page_type # Текущий тип, который может быть обновлен LLM
            
#             if llm_instance and driver: # Попытка LLM классификации
#                 logger.info(f"Тип страницы для '{key_url}' исходно '{original_page_type}'. Попытка LLM-классификации.")
#                 html_for_llm: Optional[str] = driver.fetch_html(key_url)
#                 if html_for_llm:
#                     data_for_llm: Dict[str, Any] = extract_page_data(html_for_llm, key_url)
#                     llm_input_content: str = str(data_for_llm.get('raw_content', '')).strip()

#                     if llm_input_content:
#                         llm_response: Any = llm_instance.ask(f'`{llm_input_content}`')
#                         if llm_response:
#                             llm_data_from_response: Optional[dict] = None
#                             try:
#                                 parsed_llm_response = j_loads(str(llm_response))
#                                 if isinstance(parsed_llm_response, dict):
#                                     llm_data_from_response = parsed_llm_response
#                                 else:
#                                     logger.warning(f"Ответ LLM для '{key_url}' распарсился, но не в dict. Тип: {type(parsed_llm_response)}. Ответ: '{str(llm_response)[:200]}'")
#                             except Exception as ex_llm_parse:
#                                 logger.error(f"Ошибка парсинга JSON-ответа LLM для '{key_url}': {ex_llm_parse}. Ответ LLM: '{str(llm_response)[:200]}'", exc_info=True)

#                             if llm_data_from_response:
#                                 llm_determined_page_type = llm_data_from_response.get('page_type', "")
#                                 logger.info(f"LLM определил тип страницы для '{key_url}' как '{llm_determined_page_type}'")
#                                 # Обновляем value_dict всеми данными от LLM.
#                                 # Это важно, так как LLM может вернуть и другие поля.
#                                 value_dict.update(llm_data_from_response) 
#                                 current_page_type = llm_determined_page_type # Используем тип от LLM
#                             else:
#                                 logger.warning(f"Не удалось получить структурированные данные от LLM для '{key_url}'. Ответ: '{str(llm_response)[:200]}'")
#                         else:
#                             logger.warning(f"Отсутствует ответ от LLM для '{key_url}'. Исходный тип: '{original_page_type}'")
#                     else:
#                         logger.warning(f"Отсутствует 'raw_content' для отправки в LLM для ключа '{key_url}'. Исходный тип: '{original_page_type}'")
#                 else:
#                     logger.warning(f"Не удалось получить HTML для LLM-классификации ключа '{key_url}'.")
#             elif not llm_instance:
#                  logger.debug('LLM не инициализирован. Пропуск LLM-классификации.') # Debug, т.к. это может быть ожидаемо
#             elif not driver:
#                  logger.debug('WebDriver не инициализирован. Пропуск LLM-классификации.')

#             final_page_type_for_obj: str = current_page_type or "other_types"
#             page_obj = _create_page_data_object(value_dict, final_page_type_for_obj, key_url)

#             # Распределение по коллекциям
#             collection_key = final_page_type_for_obj if final_page_type_for_obj in collections else "other_types"
#             collections[collection_key][key_url] = page_obj
            
#             if page_obj: # page_obj был успешно создан
#                  logger.info(f"Обработанные данные для ключа '{key_url}' (тип: {final_page_type_for_obj}) в '{path.name}'")
#                  # Сохраняем обновленный value_dict для последующей перезаписи исходного файла
#                  items_to_update_status_in_source_file[key_url] = value_dict
#                  # Обновляем статус непосредственно в value_dict, который будет использоваться для _create_page_data_object
#                  value_dict['status'] = 'checked_and_categorized'
#                  value_dict['page_type'] = final_page_type_for_obj # Убедимся, что page_type обновлен после LLM


#         if path_to_target_dir:
#             # Обновляем исходный файл data_from_input_file только теми элементами, которые были обработаны
#             # и для которых обновился value_dict (например, добавился статус или данные от LLM)
#             source_file_needs_update = False
#             for key_url_updated, updated_value_dict in items_to_update_status_in_source_file.items():
#                 if key_url_updated in data_from_input_file: # Убедимся, что ключ все еще там
#                     data_from_input_file[key_url_updated] = updated_value_dict
#                     source_file_needs_update = True
            
#             if source_file_needs_update:
#                 j_dumps(data_from_input_file, path)
#                 logger.info(f"Обновленный файл '{path.name}' сохранен с обновленными статусами и данными от LLM.")

#             # Сохраняем сгруппированные данные
#             for type_name_coll, data_collection_coll in collections.items():
#                 if data_collection_coll:
#                     output_filename_coll = f'{type_name_coll}_{current_timestamp}.json'
#                     # Проверяем, существует ли уже файл для этого timestamp и типа, и если да, объединяем
#                     target_coll_file_path = path_to_target_dir / output_filename_coll
#                     final_data_to_save = data_collection_coll
#                     if target_coll_file_path.exists():
#                         try:
#                             existing_coll_data = j_loads(target_coll_file_path)
#                             if isinstance(existing_coll_data, dict):
#                                 existing_coll_data.update(data_collection_coll) # Новые данные перезапишут старые с тем же ключом
#                                 final_data_to_save = existing_coll_data
#                             else:
#                                 logger.error(f"Файл {target_coll_file_path} не содержит JSON-объект. Будет перезаписан.")
#                         except Exception as e_coll_load:
#                              logger.error(f"Ошибка загрузки существующего файла коллекции {target_coll_file_path}: {e_coll_load}. Будет перезаписан.")
                    
#                     j_dumps(final_data_to_save, target_coll_file_path)
#                     logger.info(f"Сохранено/обновлено {len(data_collection_coll)} элементов типа '{type_name_coll}' в {output_filename_coll} в {path_to_target_dir}")
#         else:
#             logger.error(f"Целевая директория не была установлена для файла {path}, агрегированные данные по типам не сохранены.")

#     if driver:
#         driver.quit()
#         logger.info('WebDriver Firefox закрыт.')

if __name__ == '__main__':
    generate_train_data()
