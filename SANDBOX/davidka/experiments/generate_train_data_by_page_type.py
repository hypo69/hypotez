## \file /sandbox/davidka/experiments/generate_train_data_by_page_type.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для генерации обучающих данных на основе типа страницы.
================================================================
Скрипт обрабатывает JSON-файлы, извлекает структурированную информацию
о продуктах и категориях, включая метаданные, описания и другие атрибуты.
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
# from types import SimpleNamespace # SimpleNamespace больше не используется напрямую в Config
from typing import Optional, Dict, Any, List, Union # Добавлено Union для Path

# -------------------------------------------------------------------
import header
from header import __root__
from src import gs
from src.llm.gemini import GoogleGenerativeAi
from src.webdriver.driver import Driver
from src.webdriver.firefox import Firefox
from SANDBOX.davidka.graber import extract_page_data # Предполагается, что этот путь корректен
from src.utils.file import read_text_file, recursively_yield_file_path
from src.utils.url import extract_pure_domain
from src.utils.jjson import j_loads, j_dumps # j_loads_ns больше не используется в Config
from src.utils.printer import pprint as print
from src.logger.logger import logger

class Config:
    """Класс конфигурации скрипта."""
    ENDPOINT: Path = __root__ / 'SANDBOX' / 'davidka'
    config_file_path: Path = ENDPOINT / 'davidka.json'
    config_data: Optional[Dict[str, Any]] = j_loads(config_file_path) # Загружаем как dict

    STORAGE: Path
    TRAIN_STORAGE: Path

    if config_data:
        storage_path_str = config_data.get('storage')
        train_storage_path_str = config_data.get('train_storage')

        if storage_path_str:
            STORAGE = Path(storage_path_str)
        else:
            logger.error(f"Ключ 'storage' не найден в {config_file_path}. Установка в текущую директорию.")
            STORAGE = Path.cwd()

        if train_storage_path_str:
            TRAIN_STORAGE = Path(train_storage_path_str)
        else:
            logger.error(f"Ключ 'train_storage' не найден в {config_file_path}. Установка в 'TRAIN' внутри STORAGE.")
            TRAIN_STORAGE = STORAGE / 'TRAIN'
            TRAIN_STORAGE.mkdir(parents=True, exist_ok=True) # Создаем, если не существует
    else:
        logger.critical(f"Не удалось загрузить конфигурационный файл: {config_file_path}. Остановка.")
        sys.exit(1) # Выход, если конфигурация не загружена

    GEMINI_API_KEY: Optional[str] = None # Будет установлен позже из аргументов командной строки
    GEMINI_MODEL_NAME: str = 'gemini-1.5-flash-latest' # Обновлено на более актуальное имя модели
    system_instructuction: str | None = read_text_file(ENDPOINT / 'instructions/analize_html.md')
    updated_links_file_name: str = 'updated_links.json'
    DELAY_AFTER_LINK_PROCESSING: int = 15
    WINDOW_MODE: str = 'headless'
    train_dir: Path = TRAIN_STORAGE # Используем TRAIN_STORAGE


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

def generate_train_data(path: Path, timestamp: str):
    """
    Ищет страницы продуктов в JSON-файле и сохраняет их в файл train_products_{timestamp}.json.
    Args:
        path (Path): Путь к JSON-файлу.
        timestamp (str): Временная метка для имени выходного файла.
    """
    data_from_input_file: Optional[Dict[str, Any]] = j_loads(path)
    if not data_from_input_file:
        logger.warning(f'generate_train_data: Нет данных или не удалось загрузить: {path}')
        return

    products_to_save: Dict[str, Any] = {}
    for key_url, value_data_item in data_from_input_file.items():
        current_value_dict = None
        if isinstance(value_data_item, dict):
            current_value_dict = value_data_item
        elif isinstance(value_data_item, str): # Если данные в value_data_item - это строка JSON
            try:
                parsed_value = j_loads(value_data_item)
                if isinstance(parsed_value, dict):
                    current_value_dict = parsed_value
            except Exception as e:
                logger.warning(f"generate_train_data: Ошибка парсинга JSON-строки для ключа '{key_url}' в '{path.name}': {e}")
        
        if current_value_dict:
            page_type: Optional[str] = get_page_type(current_value_dict)
            if page_type == 'product':
                products_to_save[key_url] = _create_page_data_object(current_value_dict, 'product', key_url)

    if products_to_save:
        output_file_path = Config.train_dir / f'train_products_{timestamp}.json'
        existing_data: Dict[str, Any] = {}
        if output_file_path.exists():
            try:
                loaded_data = j_loads(output_file_path)
                if isinstance(loaded_data, dict): # Убедимся, что загрузили словарь
                    existing_data = loaded_data
                else:
                    logger.error(f"generate_train_data: Файл {output_file_path} не содержит валидный JSON-объект (словарь). Начинаем с пустого.")
            except Exception as e:
                logger.error(f"generate_train_data: Не удалось загрузить или распарсить существующий файл {output_file_path}: {e}. Начинаем с пустого.")
        
        existing_data.update(products_to_save) # Объединяем существующие данные с новыми
        j_dumps(existing_data, output_file_path)
        logger.info(f"generate_train_data: Добавлено/обновлено {len(products_to_save)} продуктов в {output_file_path}")


def process_files_and_generate_data():
    """
    Основная функция для обработки файлов и генерации структурированных данных.
    """
    driver: Optional[Driver] = None
    llm_instance: Optional[GoogleGenerativeAi] = None

    try:
        driver = Driver(Firefox, window_mode=Config.WINDOW_MODE)
        logger.info('Инстанс WebDriver Firefox успешно инициализирован.')
    except Exception as ex:
        logger.error(f'Не удалось инициализировать WebDriver Firefox: {ex}', exc_info=True)
        # Решение о выходе или продолжении без WebDriver зависит от требований
        # Если WebDriver критичен для всех операций, можно сделать sys.exit(1)

    # Инициализация LLM с использованием ключа, установленного из аргументов командной строки
    if Config.GEMINI_API_KEY and Config.system_instructuction:
        try:
            llm_instance = GoogleGenerativeAi(
                Config.GEMINI_API_KEY,
                Config.GEMINI_MODEL_NAME,
                {'response_mime_type': 'application/json'},
                Config.system_instructuction
            )
            logger.info(f'Инстанс GoogleGenerativeAi успешно инициализирован с ключом пользователя.')
        except Exception as ex:
            logger.critical(f'Не удалось инициализировать GoogleGenerativeAi: {ex}', ex, exc_info=True)
            # sys.exit(1) # Раскомментируйте, если LLM абсолютно необходим
    elif not Config.GEMINI_API_KEY:
        logger.error(f'GEMINI_API_KEY не был установлен. LLM-функциональность недоступна.')
    elif not Config.system_instructuction:
        logger.error(f'system_instructuction не настроен. LLM-функциональность недоступна.')

    current_timestamp: str = gs.now
    file_counter: int = 0

    # Список префиксов файлов, которые нужно пропускать
    skip_prefixes = (
        'processed_internal_links', 'updated_links', 'train_products',
        'home_', 'about_', 'careers_', 'privacy_police_', 'terms_',
        'service_', 'contact_', 'brands_', 'distributors_',
        'products_', 'categories_', 'other_types_'
    )

    for path in recursively_yield_file_path(Config.STORAGE, ['*.json']):
        if any(path.stem.startswith(prefix) for prefix in skip_prefixes):
            logger.info(f'Пропуск служебного или уже обработанного файла: {path}')
            continue

        # ------------------------ Обновление словаря товаров ------------------------
        file_counter += 1
        if file_counter > 0 and file_counter % 300 == 0: # Обновляем временную метку каждые 300 файлов (после первого блока)
            current_timestamp = gs.now
        
        generate_train_data(path, current_timestamp)
        
        # Важно: Если этот `continue` активен, то код ниже (классификация LLM и сохранение по типам)
        # НЕ БУДЕТ выполнен для этого файла. 
        # Если вам нужна и генерация `train_products_...` и последующая классификация/сохранение
        # по типам для каждого файла, ЗАКОММЕНТИРУЙТЕ или УДАЛИТЕ строку `continue` ниже.
        continue # Закомментируйте эту строку, если нужна полная обработка каждого файла

        # ------------------------------------------------------------------------
        # Следующий блок кода (определение типов через LLM и сохранение по типам)
        # будет выполнен, только если `continue` выше закомментирован или удален.
        # ------------------------------------------------------------------------

        data_from_input_file: Optional[Dict[str, Any]] = j_loads(path)
        if not data_from_input_file:
            logger.warning(f'Нет данных или не удалось загрузить для основной обработки: {path}')
            continue

        path_to_target_dir: Optional[Path] = None
        anchor_directory_name: str = 'data_by_supplier'
        try:
            path_parts: List[str] = list(path.parts) # Преобразуем в list для .index
            anchor_index: int = path_parts.index(anchor_directory_name)
            if anchor_index + 1 < len(path_parts):
                path_to_target_dir = Path(*path_parts[:anchor_index + 2])
                path_to_target_dir.mkdir(parents=True, exist_ok=True) # Убедимся, что директория существует
            else:
                logger.error(f'Не удалось определить структуру целевой директории из частей пути: {path.parts} для файла {path}')
                continue
        except ValueError:
            logger.warning(f"Анкерная директория '{anchor_directory_name}' не найдена в пути: {path.parts} для файла {path}")
            # Если анкерной директории нет, можно сохранять в Config.STORAGE или другую дефолтную директорию
            path_to_target_dir = Config.STORAGE / "categorized_data_default" / path.parent.name # Добавим имя родительской директории файла
            path_to_target_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Данные для {path.name} будут сохранены в дефолтную директорию: {path_to_target_dir}")
            # continue # или continue, если это критично
        except Exception as ex:
            logger.error(f"Неожиданная ошибка при определении целевой директории для {path}: {ex}", ex, exc_info=True)
            continue


        collections: Dict[str, Dict[str, Any]] = {
            "products": {}, "categories": {}, "about": {},
            "home": {}, "service": {}, "careers": {}, "other_types": {}
        }

        items_to_update_status_in_source_file : Dict[str, Dict[str, Any]] = {}

        for key_url, value_data_item in data_from_input_file.items():
            value_dict: Optional[Dict[str, Any]] = None
            if isinstance(value_data_item, dict):
                value_dict = value_data_item
            elif isinstance(value_data_item, str):
                try:
                    parsed_str_data = j_loads(value_data_item)
                    if isinstance(parsed_str_data, dict):
                        value_dict = parsed_str_data
                        # data_from_input_file[key_url] = value_dict # Обновляем в исходном словаре, если нужно перезаписывать исходный файл
                    else:
                        logger.warning(f"Данные для ключа '{key_url}' в '{path.name}' (строка) не распарсились в dict: '{value_data_item[:100]}...'")
                except Exception as e:
                    logger.warning(f"Ошибка парсинга JSON-строки для ключа '{key_url}' в '{path.name}': {e}. Строка: '{value_data_item[:100]}...'")
            else:
                logger.warning(f"Неожиданный тип данных для '{key_url}' в '{path.name}': {type(value_data_item)}. Ожидался dict или JSON-строка.")

            if not value_dict:
                logger.warning(f"Пропуск элемента для ключа '{key_url}' в '{path.name}' из-за проблем с данными или форматом.")
                continue

            original_page_type: Optional[str] = get_page_type(value_dict) # Сохраняем исходный тип
            current_page_type: Optional[str] = original_page_type # Текущий тип, который может быть обновлен LLM
            
            if llm_instance and driver: # Попытка LLM классификации
                logger.info(f"Тип страницы для '{key_url}' исходно '{original_page_type}'. Попытка LLM-классификации.")
                html_for_llm: Optional[str] = driver.fetch_html(key_url)
                if html_for_llm:
                    data_for_llm: Dict[str, Any] = extract_page_data(html_for_llm, key_url)
                    llm_input_content: str = str(data_for_llm.get('raw_content', '')).strip()

                    if llm_input_content:
                        llm_response: Any = llm_instance.ask(f'`{llm_input_content}`')
                        if llm_response:
                            llm_data_from_response: Optional[dict] = None
                            try:
                                parsed_llm_response = j_loads(str(llm_response))
                                if isinstance(parsed_llm_response, dict):
                                    llm_data_from_response = parsed_llm_response
                                else:
                                    logger.warning(f"Ответ LLM для '{key_url}' распарсился, но не в dict. Тип: {type(parsed_llm_response)}. Ответ: '{str(llm_response)[:200]}'")
                            except Exception as ex_llm_parse:
                                logger.error(f"Ошибка парсинга JSON-ответа LLM для '{key_url}': {ex_llm_parse}. Ответ LLM: '{str(llm_response)[:200]}'", exc_info=True)

                            if llm_data_from_response:
                                llm_determined_page_type = llm_data_from_response.get('page_type', "")
                                logger.info(f"LLM определил тип страницы для '{key_url}' как '{llm_determined_page_type}'")
                                # Обновляем value_dict всеми данными от LLM.
                                # Это важно, так как LLM может вернуть и другие поля.
                                value_dict.update(llm_data_from_response) 
                                current_page_type = llm_determined_page_type # Используем тип от LLM
                            else:
                                logger.warning(f"Не удалось получить структурированные данные от LLM для '{key_url}'. Ответ: '{str(llm_response)[:200]}'")
                        else:
                            logger.warning(f"Отсутствует ответ от LLM для '{key_url}'. Исходный тип: '{original_page_type}'")
                    else:
                        logger.warning(f"Отсутствует 'raw_content' для отправки в LLM для ключа '{key_url}'. Исходный тип: '{original_page_type}'")
                else:
                    logger.warning(f"Не удалось получить HTML для LLM-классификации ключа '{key_url}'.")
            elif not llm_instance:
                 logger.debug('LLM не инициализирован. Пропуск LLM-классификации.') # Debug, т.к. это может быть ожидаемо
            elif not driver:
                 logger.debug('WebDriver не инициализирован. Пропуск LLM-классификации.')

            final_page_type_for_obj: str = current_page_type or "other_types"
            page_obj = _create_page_data_object(value_dict, final_page_type_for_obj, key_url)

            # Распределение по коллекциям
            collection_key = final_page_type_for_obj if final_page_type_for_obj in collections else "other_types"
            collections[collection_key][key_url] = page_obj
            
            if page_obj: # page_obj был успешно создан
                 logger.info(f"Обработанные данные для ключа '{key_url}' (тип: {final_page_type_for_obj}) в '{path.name}'")
                 # Сохраняем обновленный value_dict для последующей перезаписи исходного файла
                 items_to_update_status_in_source_file[key_url] = value_dict
                 # Обновляем статус непосредственно в value_dict, который будет использоваться для _create_page_data_object
                 value_dict['status'] = 'checked_and_categorized'
                 value_dict['page_type'] = final_page_type_for_obj # Убедимся, что page_type обновлен после LLM


        if path_to_target_dir:
            # Обновляем исходный файл data_from_input_file только теми элементами, которые были обработаны
            # и для которых обновился value_dict (например, добавился статус или данные от LLM)
            source_file_needs_update = False
            for key_url_updated, updated_value_dict in items_to_update_status_in_source_file.items():
                if key_url_updated in data_from_input_file: # Убедимся, что ключ все еще там
                    data_from_input_file[key_url_updated] = updated_value_dict
                    source_file_needs_update = True
            
            if source_file_needs_update:
                j_dumps(data_from_input_file, path)
                logger.info(f"Обновленный файл '{path.name}' сохранен с обновленными статусами и данными от LLM.")

            # Сохраняем сгруппированные данные
            for type_name_coll, data_collection_coll in collections.items():
                if data_collection_coll:
                    output_filename_coll = f'{type_name_coll}_{current_timestamp}.json'
                    # Проверяем, существует ли уже файл для этого timestamp и типа, и если да, объединяем
                    target_coll_file_path = path_to_target_dir / output_filename_coll
                    final_data_to_save = data_collection_coll
                    if target_coll_file_path.exists():
                        try:
                            existing_coll_data = j_loads(target_coll_file_path)
                            if isinstance(existing_coll_data, dict):
                                existing_coll_data.update(data_collection_coll) # Новые данные перезапишут старые с тем же ключом
                                final_data_to_save = existing_coll_data
                            else:
                                logger.error(f"Файл {target_coll_file_path} не содержит JSON-объект. Будет перезаписан.")
                        except Exception as e_coll_load:
                             logger.error(f"Ошибка загрузки существующего файла коллекции {target_coll_file_path}: {e_coll_load}. Будет перезаписан.")
                    
                    j_dumps(final_data_to_save, target_coll_file_path)
                    logger.info(f"Сохранено/обновлено {len(data_collection_coll)} элементов типа '{type_name_coll}' в {output_filename_coll} в {path_to_target_dir}")
        else:
            logger.error(f"Целевая директория не была установлена для файла {path}, агрегированные данные по типам не сохранены.")

    if driver:
        driver.quit()
        logger.info('WebDriver Firefox закрыт.')

if __name__ == '__main__':
    script_name = Path(__file__).name
    parser = argparse.ArgumentParser(
        description="Генерация обучающих данных и классификация типов страниц с использованием LLM.",
        usage=f"python {script_name} [username]",
        epilog=f"Примеры:\n"
               f"  python {script_name}                  # Использует ключ 'onela' из gs.credentials.gemini\n"
               f"  python {script_name} kazarinov        # Использует ключ 'kazarinov' из gs.credentials.gemini",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        'user', type=str, nargs='?', default='onela',
        help="Имя пользователя для выбора Gemini API ключа (например, 'onela', 'kazarinov')."
    )
    args = parser.parse_args()
    username = args.user

    logger.info(f"--- Начало работы скрипта {script_name} для пользователя '{username}' ---")

    # ------------------------- УСТАНОВКА GEMINI API КЛЮЧА --------------------------
    try:
        user_gemini_config = getattr(gs.credentials.gemini, username)
        Config.GEMINI_API_KEY = getattr(user_gemini_config, 'api_key')
        logger.info(f"Успешно получен и установлен Gemini API ключ для пользователя: '{username}'")
    except AttributeError:
        logger.critical(f"Ошибка: не удалось найти конфигурацию или API ключ для пользователя '{username}' в gs.credentials.gemini.{username}.api_key.")
        sys.exit(1)
    except Exception as e: 
        logger.critical(f"Непредвиденная ошибка при доступе к API ключу для пользователя '{username}': {e}", exc_info=True)
        sys.exit(1)

    if not Config.GEMINI_API_KEY:
        logger.critical(f"Ошибка: API ключ для пользователя '{username}' пустой или не найден.")
        sys.exit(1)

    # Убедимся, что директория для train_dir существует
    Config.train_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Директория для обучающих данных: {Config.train_dir.resolve()}")


    process_files_and_generate_data()
